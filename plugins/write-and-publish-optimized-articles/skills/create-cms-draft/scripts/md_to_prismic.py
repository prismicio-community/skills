#!/usr/bin/env python3
"""Convert a markdown article into Prismic editor-shape slice payloads.

Usage:
    python md_to_prismic.py article.md                 # all slices
    python md_to_prismic.py article.md --part meta     # front-matter fields only
    python md_to_prismic.py article.md --list          # index of parts
    python md_to_prismic.py article.md --part 3        # one slice payload

Why this exists: hyperlink spans in Prismic are character offsets into the FINAL
plain text. Counting them against the markdown source shifts every bold and link
after the first one. This computes them from the rendered text instead.

Emits, in document order:
  - meta            front-matter mapped to blog fields
  - tldr            the first bulleted section (TL;DR / "the short version")
  - text_content    prose between tables
  - comparison_table markdown tables, as the `multicolumn` variation
  - faq             the FAQ section, as repeatable items

Slice and field names default to a reference blog model (tldr, text_content,
comparison_table, faq). Pass --map content-model.json to rename them to the
repository's own slice types, variations and field ids, or to fold a slice the
repository does not have into plain rich text (map it to null):

    {"slices": {
        "tldr": {"type": "summary", "variation": "default",
                 "fields": {"title": "heading", "content": "body"}},
        "text_content": {"type": "rich_text", "fields": {"content": "text"}},
        "comparison_table": null,
        "faq": {"type": "faq", "fields": {"title": "title",
                "question": "question", "answer": "answer"}}},
     "text_slice": "text_content",
     "meta": {"meta_title": "seo_title", "meta_description": "seo_description"}}

A slice mapped to null is emitted as the text slice instead: headings plus
bullets for a TL;DR, heading3 question plus answer for an FAQ, one paragraph
per row for a table.

Paste each payload into create_document / update_document. Insert empty slices
first and fill them with `updates`: the `inserts` parameter has a payload
ceiling that `updates` does not.

Standard library only.
"""

import argparse
import json
import re
import sys
import uuid

TLDR_HEADINGS = re.compile(r"tl;?\s?dr|the short version|in short|key takeaways", re.I)
FAQ_HEADINGS = re.compile(r"\bfaq\b|frequently asked", re.I)


# ---------------------------------------------------------------- inline parse

def parse_inline(md):
    """Return (plain_text, spans) for one line of inline markdown.

    Handles **strong**, *em*, `code` (as the inline-code label) and
    [anchor](url). Offsets are computed against the emitted plain text, which
    is the whole point of this function.
    """
    text, spans, i = "", [], 0
    pattern = re.compile(
        r"\[(?P<anchor>[^\]]+)\]\((?P<url>[^)\s]+)[^)]*\)"
        r"|\*\*(?P<strong>[^*]+)\*\*"
        r"|(?<!\*)\*(?P<em>[^*]+)\*(?!\*)"
        r"|`(?P<code>[^`]+)`"
    )
    for m in pattern.finditer(md):
        text += md[i:m.start()]
        start = len(text)
        if m.group("anchor") is not None:
            text += m.group("anchor")
            url = m.group("url")
            spans.append({"type": "hyperlink", "start": start, "end": len(text),
                          "data": {"__TYPE__": "ExternalLink", "url": url}})
        elif m.group("strong") is not None:
            text += m.group("strong")
            spans.append({"type": "strong", "start": start, "end": len(text)})
        elif m.group("em") is not None:
            text += m.group("em")
            spans.append({"type": "em", "start": start, "end": len(text)})
        else:
            text += m.group("code")
            spans.append({"type": "label", "start": start, "end": len(text),
                          "data": "inline-code"})
        i = m.end()
    text += md[i:]
    return text, spans


def block(kind, md):
    text, spans = parse_inline(md)
    return {"type": kind, "direction": "ltr",
            "content": {"text": text, "spans": spans}}


def rich(blocks):
    return {"__TYPE__": "StructuredTextContent", "value": blocks}


# ---------------------------------------------------------------- md structure

def split_front_matter(raw):
    if raw.startswith("---\n"):
        end = raw.find("\n---", 4)
        if end != -1:
            fm = {}
            for line in raw[4:end].splitlines():
                if ":" in line:
                    k, v = line.split(":", 1)
                    fm[k.strip()] = v.strip().strip('"')
            return fm, raw[end + 4:]
    return {}, raw


def is_table_row(s):
    return s.strip().startswith("|") and s.count("|") >= 2


def is_table_sep(s):
    return bool(re.fullmatch(r"\|?[\s:\-|]+\|?", s.strip())) and "-" in s


def cells(row):
    return [c.strip() for c in row.strip().strip("|").split("|")]


def table_payload(rows):
    """rows: list of markdown table lines, separator already removed."""
    out = []
    for r_i, row in enumerate(rows):
        kind = "tableHeader" if r_i == 0 else "tableCell"
        out.append({
            "key": str(uuid.uuid4()), "type": "tableRow",
            "content": [{"key": str(uuid.uuid4()), "type": kind,
                         "content": rich([block("paragraph", c)])}
                        for c in cells(row)],
        })
    return {"__TYPE__": "TableContent", "content": out}


def line_to_block(s):
    h = re.match(r"^(#{2,6})\s+(.*)$", s)
    if h:
        level = min(len(h.group(1)), 4)
        return block(f"heading{level}", h.group(2).strip())
    if re.match(r"^\s*[-*]\s+", s):
        return block("list-item", re.sub(r"^\s*[-*]\s+", "", s))
    if re.match(r"^\s*\d+[.)]\s+", s):
        return block("o-list-item", re.sub(r"^\s*\d+[.)]\s+", "", s))
    return block("paragraph", s.strip())


# ---------------------------------------------------------------- conversion

def convert(raw):
    fm, body = split_front_matter(raw)
    lines = body.split("\n")

    parts, buf, i = [], [], 0
    in_fence = False
    current_h2 = ""

    def flush(kind="text_content"):
        nonlocal buf
        if buf:
            parts.append({"slice": kind, "blocks": buf})
            buf = []

    while i < len(lines):
        s = lines[i]
        if s.strip().startswith("```"):
            in_fence = not in_fence
            i += 1
            continue
        if in_fence or not s.strip():
            i += 1
            continue

        h1 = re.match(r"^#\s+(.*)$", s)
        if h1:
            parts.append({"slice": "title", "text": h1.group(1).strip()})
            i += 1
            continue

        h2 = re.match(r"^##\s+(.*)$", s)
        if h2:
            current_h2 = h2.group(1).strip()
            if TLDR_HEADINGS.search(current_h2):
                flush()
                bullets, j = [], i + 1
                while j < len(lines) and (not lines[j].strip()
                                          or lines[j].strip().startswith(("-", "*"))):
                    if lines[j].strip():
                        bullets.append(line_to_block(lines[j]))
                    j += 1
                parts.append({"slice": "tldr", "title": current_h2, "blocks": bullets})
                i = j
                continue
            if FAQ_HEADINGS.search(current_h2):
                flush()
                items, j, q, ans = [], i + 1, None, []
                while j < len(lines) and not re.match(r"^##\s", lines[j]):
                    hq = re.match(r"^#{3,4}\s+(.*)$", lines[j])
                    if hq:
                        if q:
                            items.append((q, ans))
                        q, ans = hq.group(1).strip(), []
                    elif lines[j].strip() and q:
                        ans.append(line_to_block(lines[j]))
                    j += 1
                if q:
                    items.append((q, ans))
                parts.append({"slice": "faq", "title": current_h2, "items": items})
                i = j
                continue

        if is_table_row(s):
            flush()
            rows, j = [], i
            while j < len(lines) and is_table_row(lines[j]):
                if not is_table_sep(lines[j]):
                    rows.append(lines[j])
                j += 1
            parts.append({"slice": "comparison_table", "rows": rows,
                          "context": current_h2})
            i = j
            continue

        if s.strip() == "---":
            i += 1
            continue

        buf.append(line_to_block(s))
        i += 1

    flush()
    return fm, parts


# ---------------------------------------------------------------- payloads

def payload_for(part):
    kind = part["slice"]
    if kind == "tldr":
        return {"variation": "default", "primary": {
            "title": rich([block("heading2", part["title"])]),
            "content": rich(part["blocks"])}, "items": []}
    if kind == "text_content":
        return {"variation": "default",
                "primary": {"content": rich(part["blocks"])}, "items": []}
    if kind == "comparison_table":
        return {"variation": "multicolumn", "primary": {
            "table": table_payload(part["rows"]),
            "highlight_first_column": {"__TYPE__": "BooleanContent", "value": True}},
            "items": []}
    if kind == "faq":
        return {"variation": "default",
                "primary": {"title": rich([block("heading2", part["title"])])},
                "items": [{"__TYPE__": "GroupItemContent", "value": [
                    ["question", rich([block("heading3", q)])],
                    ["answer", rich(a)]]} for q, a in part["items"]]}
    return None


META_MAP = {"meta_title": "meta_title", "meta_description": "meta_description",
            "slug": "uid"}


# ---------------------------------------------------------------- content map

def fold_to_text(part):
    """Rebuild a part as plain text blocks, for a slice the model lacks."""
    kind = part["slice"]
    if kind == "tldr":
        blocks = [block("heading2", part["title"])] + part["blocks"]
    elif kind == "faq":
        blocks = [block("heading2", part["title"])]
        for q, a in part["items"]:
            blocks += [block("heading3", q)] + a
    elif kind == "comparison_table":
        blocks = [block("paragraph", " | ".join(cells(r)))
                  for r in part["rows"]]
    else:
        return part
    return {"slice": "text_content", "blocks": blocks}


def rename_fields(widget, fields):
    if not fields:
        return widget
    widget["primary"] = {fields.get(k, k): v for k, v in widget.get("primary", {}).items()}
    widget["items"] = [{"__TYPE__": it["__TYPE__"],
                        "value": [[fields.get(k, k), v] for k, v in it["value"]]}
                       for it in widget.get("items", [])]
    return widget


def mapped(part, cmap):
    """Return (slice_type, widget) after applying the repository's content map."""
    slices = (cmap or {}).get("slices", {})
    kind = part["slice"]
    if kind in slices and slices[kind] is None:
        part = fold_to_text(part)
        kind = part["slice"]
    widget = payload_for(part)
    spec = slices.get(kind) or {}
    if spec.get("variation"):
        widget["variation"] = spec["variation"]
    widget = rename_fields(widget, spec.get("fields"))
    return spec.get("type", kind), widget


def meta_payload(fm, cmap=None):
    out = {}
    names = dict(META_MAP)
    names.update((cmap or {}).get("meta", {}))
    for src, dest in names.items():
        if src in fm:
            if dest == "uid":
                out["uid"] = {"__TYPE__": "UIDContent", "value": fm[src]}
            else:
                out[dest] = {"__TYPE__": "FieldContent", "type": "Text",
                             "value": fm[src]}
    return out


def validate(parts):
    """Catch the failure modes that silently produce broken documents."""
    problems = []
    for n, part in enumerate(parts):
        for b in part.get("blocks", []) + [x for _, a in part.get("items", []) for x in a]:
            t = b.get("content", {}).get("text", "")
            for sp in b.get("content", {}).get("spans", []):
                if not 0 <= sp["start"] < sp["end"] <= len(t):
                    problems.append(f"part {n}: span {sp} out of range for {len(t)} chars")
            if re.search(r"\*\*|\[[^\]]+\]\(", t):
                problems.append(f"part {n}: unparsed markdown left in plain text: {t[:60]}")
    return problems


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("path")
    ap.add_argument("--part", help="'meta', or a part index from --list")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--map", help="JSON file mapping slices and fields to the repository's model")
    args = ap.parse_args()
    cmap = json.load(open(args.map, encoding="utf-8")) if args.map else None

    fm, parts = convert(open(args.path, encoding="utf-8").read())

    problems = validate(parts)
    if problems:
        print("VALIDATION PROBLEMS:", file=sys.stderr)
        for p in problems:
            print("  " + p, file=sys.stderr)
        return 1

    if args.list:
        print(f"title: {fm.get('meta_title', '(none)')}")
        for n, part in enumerate(parts):
            label = part.get("text") or part.get("title") or part.get("context") or ""
            size = len(part.get("blocks", []) or part.get("rows", []) or part.get("items", []))
            print(f"{n:3}  {part['slice']:18} {size:3} items  {label[:50]}")
        return 0

    if args.part == "meta":
        print(json.dumps(meta_payload(fm, cmap), indent=2))
        return 0

    if args.part is not None:
        name, widget = mapped(parts[int(args.part)], cmap)
        print(json.dumps({"name": name, "widget": widget}, indent=2))
        return 0

    out = []
    for p in parts:
        if p["slice"] == "title":
            continue
        name, widget = mapped(p, cmap)
        out.append({"name": name, "widget": widget})
    print(json.dumps({"meta": meta_payload(fm, cmap), "slices": out}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
