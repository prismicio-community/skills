#!/usr/bin/env python3
"""Convert a markdown article into clean HTML for CMSs whose body field takes HTML.

Usage:
    python md_to_html.py article.md             # JSON: {"meta": {...}, "title": "...", "html": "..."}
    python md_to_html.py article.md --html      # the body HTML only
    python md_to_html.py article.md --sections  # JSON list of {"heading", "html"} per H2 section

Handles front matter (meta_title, meta_description, slug and any other keys),
the H1 (returned as the title, left out of the body), H2 to H4, paragraphs,
bold, italic, inline code, links, bulleted and numbered lists, blockquotes and
tables, fenced code blocks and images. Output is plain semantic HTML with no classes or inline styles, which
most rich-text and HTML fields accept as-is.

Refuses to emit output if any markdown syntax is left unparsed, so a stray
** or [text](url) never reaches a draft. Standard library only.
"""

import argparse
import html
import json
import re
import sys


SEP_RE = re.compile(r"^\s*\|?\s*:?-+:?\s*(\|\s*:?-+:?\s*)*\|?\s*$")


def inline(md):
    out = html.escape(md, quote=False)
    out = re.sub(r"`([^`]+)`", r"<code>\1</code>", out)
    out = re.sub(r"!\[([^\]]*)\]\(([^)\s]+)\)",
                 lambda m: f'<img src="{html.escape(html.unescape(m.group(2)))}" alt="{html.escape(html.unescape(m.group(1)))}">', out)
    out = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)",
                 lambda m: f'<a href="{html.escape(html.unescape(m.group(2)))}">{m.group(1)}</a>', out)
    out = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", out)
    out = re.sub(r"(?<![\w*])\*([^*]+)\*(?![\w*])", r"<em>\1</em>", out)
    out = re.sub(r"(?<![\w_])_([^_]+)_(?![\w_])", r"<em>\1</em>", out)
    return out


def split_front_matter(raw):
    if raw.startswith("---"):
        end = raw.find("\n---", 3)
        if end != -1:
            fm = {}
            for line in raw[3:end].strip().splitlines():
                if ":" in line:
                    k, v = line.split(":", 1)
                    fm[k.strip()] = v.strip().strip('"').strip("'")
            return fm, raw[end + 4:]
    return {}, raw


def cells(row):
    return [c.strip() for c in row.strip().strip("|").split("|")]


def convert(raw):
    fm, body = split_front_matter(raw)
    lines = body.splitlines()
    title, blocks, i = "", [], 0
    while i < len(lines):
        s = lines[i].rstrip()
        if not s.strip():
            i += 1
            continue
        fence = re.match(r"^\s*(```|~~~)\s*([\w+-]*)", s)
        if fence:
            marker, lang = fence.group(1), fence.group(2)
            i += 1
            code = []
            while i < len(lines) and not lines[i].strip().startswith(marker):
                code.append(lines[i])
                i += 1
            i += 1  # closing fence
            cls = f' class="language-{lang}"' if lang else ""
            blocks.append(("c", f"<pre><code{cls}>{html.escape(chr(10).join(code), quote=False)}</code></pre>", "", 0))
            continue
        h = re.match(r"^(#{1,4})\s+(.*)", s)
        if h:
            level = len(h.group(1))
            if level == 1 and not title:
                title = h.group(2).strip()
            else:
                blocks.append(("h", f"<h{level}>{inline(h.group(2).strip())}</h{level}>", h.group(2).strip(), level))
            i += 1
            continue
        if s.lstrip().startswith("|") and i + 1 < len(lines) and SEP_RE.match(lines[i + 1]):
            head = cells(s)
            i += 2
            rows = []
            while i < len(lines) and lines[i].lstrip().startswith("|"):
                rows.append(cells(lines[i]))
                i += 1
            t = "<table><thead><tr>" + "".join(f"<th>{inline(c)}</th>" for c in head) + "</tr></thead><tbody>"
            t += "".join("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>" for r in rows)
            blocks.append(("t", t + "</tbody></table>", "", 0))
            continue
        lm = re.match(r"^\s*([-*+]|\d+[.)])\s+", s)
        if lm:
            ordered = lm.group(1)[0].isdigit()
            items = []
            while i < len(lines) and re.match(r"^\s*([-*+]|\d+[.)])\s+", lines[i]):
                items.append(re.sub(r"^\s*([-*+]|\d+[.)])\s+", "", lines[i]).strip())
                i += 1
            tag = "ol" if ordered else "ul"
            blocks.append(("l", f"<{tag}>" + "".join(f"<li>{inline(x)}</li>" for x in items) + f"</{tag}>", "", 0))
            continue
        if s.startswith(">"):
            quote = []
            while i < len(lines) and lines[i].startswith(">"):
                quote.append(lines[i].lstrip("> ").strip())
                i += 1
            blocks.append(("q", f"<blockquote><p>{inline(' '.join(quote))}</p></blockquote>", "", 0))
            continue
        para = [s.strip()]  # always consume this line, so no input can stall the loop
        i += 1
        while i < len(lines) and lines[i].strip() and not re.match(r"^(#{1,4}\s|\s*([-*+]|\d+[.)])\s|>|\s*\||\s*(```|~~~))", lines[i]):
            para.append(lines[i].strip())
            i += 1
        blocks.append(("p", f"<p>{inline(' '.join(para))}</p>", "", 0))
    return fm, title, blocks


def check(fragment):
    text = re.sub(r"<pre>.*?</pre>", "", fragment, flags=re.S)
    text = re.sub(r"<[^>]+>", "", text)
    problems = []
    if re.search(r"\*\*|\[[^\]]+\]\(|(?<!\w)__\w", text):
        problems.append("unparsed markdown left in the output")
    return problems


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("path")
    ap.add_argument("--html", action="store_true")
    ap.add_argument("--sections", action="store_true")
    args = ap.parse_args()

    fm, title, blocks = convert(open(args.path, encoding="utf-8").read())
    body = "\n".join(b[1] for b in blocks)
    problems = check(body)
    if problems:
        print("VALIDATION PROBLEMS: " + "; ".join(problems), file=sys.stderr)
        return 1
    if args.html:
        print(body)
        return 0
    if args.sections:
        sections, cur = [], {"heading": "", "html": []}
        for kind, frag, text, level in blocks:
            if kind == "h" and level == 2:
                if cur["html"] or cur["heading"]:
                    sections.append(cur)
                cur = {"heading": text, "html": [frag]}
            else:
                cur["html"].append(frag)
        sections.append(cur)
        print(json.dumps([{"heading": s["heading"], "html": "\n".join(s["html"])} for s in sections], indent=2))
        return 0
    print(json.dumps({"meta": fm, "title": title, "html": body}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
