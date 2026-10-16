#!/usr/bin/env python3
"""Lint a markdown article against the Rich Article Writer standards.

Usage:
    python lint_article.py article.md --keyword "headless cms migration"
    python lint_article.py article.md --keyword "..." --json

Checks language rules (em dashes, banned words, AI cliches), structure rules
(heading hierarchy, paragraph length, TL;DR, FAQ, tables) and keyword handling.

Exits 1 if any ERROR-level finding is present, so it can gate delivery.
Only the standard library is used.
"""

import argparse
import json
import re
import statistics
import sys
from collections import Counter

# --------------------------------------------------------------------------
# Rule data
# --------------------------------------------------------------------------

BANNED_WORDS = [
    # brand voice list
    "robust", "seamless", "powerful", "cutting-edge", "game-changing",
    "best-in-class", "intuitive", "user-friendly", "world-class",
    "next-generation", "revolutionary",
    # LLM-tell vocabulary
    "delve", "delves", "delving", "leverage", "leverages", "leveraging",
    "utilize", "utilizes", "utilizing", "harness", "harnesses", "harnessing",
    "unlock", "unlocks", "unlocking", "realm", "tapestry", "underscore",
    "underscores", "underpin", "underpins", "spearhead", "spearheads",
    "foster", "fosters", "myriad", "plethora", "crucial", "pivotal",
    "meticulous", "meticulously", "holistic", "paradigm", "synergy",
    "elevate", "elevates", "streamline", "streamlines", "embark", "unleash",
    "transformative", "cornerstone", "ever-evolving", "fast-paced",
]

# words that are fine in some uses but usually filler; reported as warnings
SOFT_WORDS = ["vital", "comprehensive", "seamlessly", "effortlessly", "vibrant"]

CLICHE_PATTERNS = [
    (r"\bit'?s not just\b", "the 'not just X, it's Y' construction"),
    (r"\bnot only\b.{0,60}\bbut also\b", "'not only ... but also' padding"),
    (r"\bthat'?s where\b.{0,40}\bcomes? in\b", "the 'that's where X comes in' pivot"),
    (r"\bwhether you'?re\b", "the 'whether you're an X or a Y' opener"),
    (r"\blet'?s (dive|dig) in\b", "'let's dive in'"),
    (r"\blet'?s unpack\b", "'let's unpack'"),
    (r"\bbuckle up\b", "'buckle up'"),
    (r"\bin today'?s\b", "'in today's [landscape/world/market]'"),
    (r"\bdigital (age|landscape|era)\b", "'digital age/landscape'"),
    (r"\bever[- ]changing\b", "'ever-changing'"),
    (r"\brapidly (changing|evolving)\b", "'rapidly evolving'"),
    (r"\bat the forefront\b", "'at the forefront'"),
    (r"\bit'?s worth noting\b", "'it's worth noting'"),
    (r"\bit'?s important to (note|remember|understand)\b", "'it's important to note'"),
    (r"\bwhen it comes to\b", "'when it comes to'"),
    (r"\bin the world of\b", "'in the world of'"),
    (r"\bat the end of the day\b", "'at the end of the day'"),
    (r"\bthe truth is\b", "'the truth is'"),
    (r"\bhere'?s the thing\b", "'here's the thing'"),
    (r"\bin conclusion\b", "'in conclusion'"),
    (r"\bin summary\b", "'in summary'"),
    (r"\bplays? a (crucial|pivotal|key|vital) role\b", "'plays a crucial role'"),
    (r"\ba testament to\b", "'a testament to'"),
    (r"\bstudies show\b", "'studies show' without a named study"),
    (r"\bexperts agree\b", "'experts agree' without a named expert"),
    (r"\bmany businesses find\b", "vague 'many businesses find'"),
    (r"\bin this (section|article),? (we'?ll|we will|you'?ll)\b", "signposting the obvious"),
    (r"\bnavigat\w+ the (complexit|landscape|challeng)", "'navigating the complexities'"),
    (r"\bgame[- ]?changer\b", "'game-changer'"),
    (r"\bneedle[- ]moving\b", "'needle-moving'"),
    (r"\bsupercharge\b", "'supercharge'"),
    (r"\bdeep dive into\b", "'deep dive into' as filler"),
    (r"^\s*(ever|have you ever) (wondered|noticed|struggled)", "rhetorical question opener"),
]

MINIMISERS = [
    (r"\bsimply (add|use|click|set|run|create|install|configure|update)\b", "'simply' as a minimiser"),
    (r"\bjust (add|use|click|set|run|create|install|configure|update)\b", "'just' as a minimiser"),
    (r"\bensure that\b", "vague 'ensure' (use 'make sure' or be specific)"),
]

WEAK_ANCHORS = {"click here", "read more", "here", "this", "this article",
                "learn more", "more", "link", "this page", "check it out"}

MAX_PARAGRAPH_CHARS = 400   # ~4 rendered lines
MAX_SENTENCE_WORDS = 35
MAX_TABLE_COLUMNS = 5


# --------------------------------------------------------------------------
# Parsing helpers
# --------------------------------------------------------------------------

def strip_code_and_frontmatter(lines):
    """Return list of (line_no, text, in_code, in_frontmatter)."""
    out = []
    in_fence = False
    in_front = False
    for i, raw in enumerate(lines, start=1):
        stripped = raw.strip()
        if i == 1 and stripped == "---":
            in_front = True
            out.append((i, raw, False, True))
            continue
        if in_front:
            out.append((i, raw, False, True))
            if stripped == "---":
                in_front = False
            continue
        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_fence = not in_fence
            out.append((i, raw, True, False))
            continue
        out.append((i, raw, in_fence, False))
    return out


def is_table_row(text):
    s = text.strip()
    return s.startswith("|") and s.count("|") >= 2


def is_table_separator(text):
    s = text.strip()
    return bool(re.fullmatch(r"\|?[\s:\-|]+\|?", s)) and "-" in s and "|" in s


def is_horizontal_rule(text):
    s = text.strip()
    return bool(re.fullmatch(r"(-{3,}|\*{3,}|_{3,})", s))


def prose_lines(parsed):
    """Lines that carry article prose: no code, no frontmatter, no table rules."""
    for no, text, in_code, in_front in parsed:
        if in_code or in_front:
            continue
        if is_table_separator(text) or is_horizontal_rule(text):
            continue
        yield no, text


def split_sentences(text):
    text = re.sub(r"\s+", " ", text).strip()
    if not text:
        return []
    parts = re.split(r"(?<=[.!?])\s+(?=[A-Z0-9\"'(])", text)
    return [p for p in parts if p.strip()]


def strip_markdown(text):
    text = re.sub(r"`[^`]*`", " ", text)
    text = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", text)
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"[*_>#]+", " ", text)
    return text


# --------------------------------------------------------------------------
# Checks
# --------------------------------------------------------------------------

class Report:
    def __init__(self):
        self.items = []

    def add(self, level, rule, line, message, excerpt=""):
        self.items.append({"level": level, "rule": rule, "line": line,
                           "message": message, "excerpt": excerpt.strip()[:160]})

    @property
    def errors(self):
        return [i for i in self.items if i["level"] == "ERROR"]

    @property
    def warnings(self):
        return [i for i in self.items if i["level"] == "WARN"]

    @property
    def problems(self):
        """Errors and warnings. INFO items are reported but never block a clean result."""
        return [i for i in self.items if i["level"] in ("ERROR", "WARN")]


def check_dashes(parsed, rep):
    for no, text in prose_lines(parsed):
        for m in re.finditer(r"—", text):
            rep.add("ERROR", "em-dash", no, "Em dash found. Use a period, colon, comma or parentheses.", text)
        # URLs legitimately contain double hyphens; strip them before checking
        text_no_urls = re.sub(r"\((?:https?|mailto):[^)]*\)", "()", text)
        text_no_urls = re.sub(r"(?:https?)://\S+", " ", text_no_urls)
        for m in re.finditer(r"(?<![-!<])--(?!-)", text_no_urls):
            if is_table_row(text):
                continue
            rep.add("ERROR", "double-hyphen", no, "Double hyphen used as a dash.", text)
        for m in re.finditer(r"–", text):
            start, end = m.start(), m.end()
            before = text[max(0, start - 1):start]
            after = text[end:end + 1]
            if not (before.isdigit() and after.isdigit()):
                rep.add("ERROR", "en-dash", no,
                        "En dash outside a numeric range. Allowed only as 4–8 or 2020–2024.", text)


def check_vocabulary(parsed, rep):
    banned_re = re.compile(r"\b(" + "|".join(re.escape(w) for w in BANNED_WORDS) + r")\b", re.I)
    soft_re = re.compile(r"\b(" + "|".join(re.escape(w) for w in SOFT_WORDS) + r")\b", re.I)
    for no, text in prose_lines(parsed):
        clean = strip_markdown(text)
        for m in banned_re.finditer(clean):
            rep.add("ERROR", "banned-word", no, f"Banned word: '{m.group(0)}'.", text)
        for m in soft_re.finditer(clean):
            rep.add("WARN", "soft-word", no, f"Filler word: '{m.group(0)}'. Replace with something specific.", text)
        for pattern, label in MINIMISERS:
            if re.search(pattern, clean, re.I):
                rep.add("ERROR", "minimiser", no, f"Avoid {label}.", text)


def check_cliches(parsed, rep):
    for no, text in prose_lines(parsed):
        clean = strip_markdown(text)
        for pattern, label in CLICHE_PATTERNS:
            if re.search(pattern, clean, re.I | re.M):
                rep.add("ERROR", "cliche", no, f"AI-cliche pattern: {label}.", text)


def check_headings(parsed, rep):
    headings = []
    for no, text in prose_lines(parsed):
        m = re.match(r"^(#{1,6})\s+(.*)$", text.strip())
        if m:
            headings.append((no, len(m.group(1)), m.group(2).strip()))

    if not headings:
        rep.add("ERROR", "headings", 0, "No headings found.")
        return headings

    h1s = [h for h in headings if h[1] == 1]
    if len(h1s) == 0:
        rep.add("ERROR", "headings", 0, "No H1 found.")
    elif len(h1s) > 1:
        rep.add("ERROR", "headings", h1s[1][0], "More than one H1.")

    h1_text = h1s[0][2].lower().strip() if h1s else ""
    prev_level = None
    for no, level, text in headings:
        if level > 4:
            rep.add("ERROR", "headings", no, f"Heading deeper than H4 (H{level}).", text)
        if prev_level is not None and level > prev_level + 1:
            rep.add("ERROR", "headings", no, f"Hierarchy skip: H{prev_level} to H{level}.", text)
        # Numbered entries (H3/H4) are correct in listicles; numbered section
        # headings (H2) are structural labels and stay banned.
        if re.match(r"^\d+[.)]\s", text) and level <= 2:
            rep.add("ERROR", "headings", no,
                    "Numeric prefix on a section heading.", text)
        if level > 1 and text.lower().strip() == h1_text:
            rep.add("ERROR", "headings", no, "Heading exactly restates the H1.", text)
        if level == 2 and text.strip().lower() in {"introduction", "overview", "conclusion",
                                                   "summary", "background"}:
            rep.add("WARN", "headings", no,
                    "Structural label rather than a navigational heading.", text)
        prev_level = level
    return headings


def get_paragraphs(parsed):
    """Yield (start_line, text) for prose paragraphs (not headings/lists/tables)."""
    buf, start = [], None
    for no, text in prose_lines(parsed):
        s = text.strip()
        is_block = (not s or s.startswith("#") or s.startswith(("-", "*", ">", "|"))
                    or re.match(r"^\d+[.)]\s", s))
        if is_block:
            if buf:
                yield start, " ".join(buf)
                buf, start = [], None
            continue
        if start is None:
            start = no
        buf.append(s)
    if buf:
        yield start, " ".join(buf)


def check_paragraphs(parsed, rep):
    lengths = []
    for start, text in get_paragraphs(parsed):
        clean = strip_markdown(text)
        lengths.append(len(clean))
        if len(clean) > MAX_PARAGRAPH_CHARS:
            rep.add("WARN", "paragraph-length", start,
                    f"Paragraph is roughly {len(clean)} characters, over the 4-line limit. Split it.", clean)
        for sent in split_sentences(clean):
            wc = len(sent.split())
            if wc > MAX_SENTENCE_WORDS:
                rep.add("WARN", "sentence-length", start,
                        f"Sentence runs {wc} words. Split it.", sent)
    if len(lengths) >= 6:
        spread = statistics.pstdev(lengths)
        if spread < 45:
            rep.add("WARN", "rhythm", 0,
                    f"Paragraph lengths are uniform (stddev {spread:.0f} chars). "
                    "Uniform rhythm reads as machine output. Vary deliberately.")


def check_tables(parsed, rep):
    for no, text in prose_lines(parsed):
        if is_table_row(text):
            cols = len([c for c in text.strip().strip("|").split("|")])
            if cols > MAX_TABLE_COLUMNS:
                rep.add("ERROR", "table-width", no,
                        f"Table row has {cols} columns, over the limit of {MAX_TABLE_COLUMNS}.", text)


def check_tldr_and_faq(parsed, rep, headings):
    body = "\n".join(t for _, t in prose_lines(parsed))

    tldr_idx = None
    for i, (no, level, text) in enumerate(headings):
        if re.search(r"tl;?\s?dr|the short version|in short|key takeaways", text, re.I):
            tldr_idx = i
            break
    if tldr_idx is None:
        rep.add("ERROR", "tldr", 0, "No TL;DR section found. It must be the first section after the H1.")
    else:
        if tldr_idx != 1 and headings[0][1] == 1:
            rep.add("WARN", "tldr", headings[tldr_idx][0],
                    "TL;DR is not the first section after the H1.")
        start_line = headings[tldr_idx][0]
        end_line = headings[tldr_idx + 1][0] if tldr_idx + 1 < len(headings) else 10 ** 9
        bullets = [t for no, t in prose_lines(parsed)
                   if start_line < no < end_line and re.match(r"^\s*[-*]\s+", t)]
        if not 4 <= len(bullets) <= 6:
            rep.add("ERROR", "tldr", start_line,
                    f"TL;DR has {len(bullets)} bullets. Required: 4 to 6.")
        covered = sum(1 for b in bullets if len(strip_markdown(b).split()) >= 12)
        if bullets and covered < len(bullets) * 0.6:
            rep.add("WARN", "tldr", start_line,
                    "Most TL;DR bullets are very short. It should summarize the whole "
                    "article, not tease sections.")

    faq_idx = None
    for i, (no, level, text) in enumerate(headings):
        if re.search(r"\bfaq|frequently asked", text, re.I):
            faq_idx = i
            break
    if faq_idx is None:
        rep.add("ERROR", "faq", 0, "No FAQ section found. It must be the last content section.")
    else:
        start_line = headings[faq_idx][0]
        questions = [t for no, t in prose_lines(parsed)
                     if no > start_line and ("?" in t)
                     and (re.match(r"^#{2,4}\s", t.strip()) or re.match(r"^\s*\*?\*?Q", t.strip()))]
        if not 5 <= len(questions) <= 10:
            rep.add("WARN", "faq", start_line,
                    f"Detected {len(questions)} FAQ questions. Required: 5 to 10 "
                    "(detection relies on questions being headings or 'Q:' lines).")

    if re.search(r"^\s*(Writer:|TODO|TK\b|\[verify)", body, re.I | re.M):
        rep.add("ERROR", "leftovers", 0, "Writer notes or TODO markers left in the article.")


def check_links_inline(parsed, rep):
    for no, text in prose_lines(parsed):
        for m in re.finditer(r"\[([^\]]+)\]\(([^)\s]+)[^)]*\)", text):
            anchor = m.group(1).strip().lower()
            if anchor in WEAK_ANCHORS:
                rep.add("ERROR", "anchor-text", no, f"Weak anchor text: '{m.group(1)}'.", text)
            if re.match(r"^https?://", anchor):
                rep.add("ERROR", "anchor-text", no, "Naked URL used as anchor text.", text)
            if len(anchor.split()) > 8:
                rep.add("WARN", "anchor-text", no, "Anchor text longer than 8 words.", text)
        stripped = re.sub(r"\[[^\]]*\]\([^)]*\)", " ", text)
        if re.search(r"(?<![(<])\bhttps?://", stripped):
            rep.add("WARN", "naked-url", no, "Bare URL in body text. Use a markdown link.", text)


def check_entry_balance(parsed, rep, headings, brand):
    """Compare sibling H3/H4 entries under the same H2; flag lopsided brand coverage."""
    if not brand or len(headings) < 3:
        return
    lines = [(n, t) for n, t in prose_lines(parsed) if not is_table_row(t)]

    groups = {}   # parent H2 line -> list of (title, line, words)
    parent = None
    for idx, (no, level, text) in enumerate(headings):
        if level == 2:
            parent = no
            continue
        if level not in (3, 4) or parent is None:
            continue
        nxt = headings[idx + 1][0] if idx + 1 < len(headings) else 10 ** 9
        words = sum(len(strip_markdown(t).split()) for n, t in lines if no < n < nxt)
        groups.setdefault(parent, []).append((text, no, words))

    brand_l = brand.lower()
    for entries in groups.values():
        # In a listicle the entries are numbered. Unnumbered subsections under the
        # same H2 (comparison tables, wrap-ups) are not entries and must not skew
        # the median they are compared against.
        numbered = [e for e in entries if re.match(r"^\d+[.)]\s", e[0])]
        if numbered:
            entries = numbered
        if len(entries) < 3:
            continue
        other = [w for t, _, w in entries if brand_l not in t.lower()]
        mine = [(t, n, w) for t, n, w in entries if brand_l in t.lower()]
        if len(other) < 2:
            continue
        med = statistics.median(other)
        for text, no, words in mine:
            # 2x, not 1.5x: the brand's entry may legitimately carry more, since it
            # usually spans more of the category. Past 2x it reads as bias regardless.
            if med > 0 and words > med * 2.0:
                rep.add("WARN", "entry-balance", no,
                        f"'{text}' runs {words} words against a median of {med:.0f} for "
                        "sibling entries. Disproportionate depth on your own product "
                        "reads as bias.")
        spread = [w for _, _, w in entries]
        if min(spread) and max(spread) > min(spread) * 3:
            rep.add("WARN", "entry-balance", entries[0][1],
                    f"Sibling entries range from {min(spread)} to {max(spread)} words. "
                    "Even out the thin ones or cut the long ones.")


def check_brand_placement(parsed, rep, headings, brand):
    """Report brand density and flag brand mentions outside earned locations."""
    if not brand:
        return
    b = brand.lower()
    lines = list(prose_lines(parsed))
    body = strip_markdown("\n".join(t for _, t in lines))
    words = len(body.split())
    hits = len(re.findall(re.escape(b), body.lower()))
    if words:
        per_1000 = hits * 1000 / words
        level = "WARN" if per_1000 > 8 else "INFO"
        rep.add(level, "brand-density", 0,
                f"'{brand}' appears {hits} times in ~{words} words ({per_1000:.1f} per 1000).")

    # Sections where brand mentions are earned: its own entries, tables, summary,
    # closing invitation, disclosure. Elsewhere, ask what the mention does for a
    # reader who will never buy.
    EARNED = re.compile(r"compare|table|short version|tl;?\s?dr|key takeaways|faq|"
                        r"frequently asked|where to start|disclosure|what you|"
                        r"need to buy|free .*(audit|tools)", re.I)
    for idx, (no, level, text) in enumerate(headings):
        if b in text.lower() or EARNED.search(text):
            continue
        nxt = headings[idx + 1][0] if idx + 1 < len(headings) else 10 ** 9
        seg = [t for n, t in lines if no < n < nxt and not is_table_row(t)]
        seg_words = len(strip_markdown(" ".join(seg)).split())
        seg_hits = sum(len(re.findall(re.escape(b), strip_markdown(t).lower())) for t in seg)
        if seg_hits >= 2 and seg_words < 400:
            rep.add("WARN", "brand-placement", no,
                    f"'{text}' is not a {brand} section but mentions {brand} "
                    f"{seg_hits} times. Check it is not a general section built to "
                    "land on a brand strength.")


def check_keyword(parsed, rep, keyword, headings):
    if not keyword:
        return
    kw = keyword.lower().strip()
    body_lines = [t for _, t in prose_lines(parsed)]
    body = strip_markdown("\n".join(body_lines)).lower()
    words = len(body.split())
    count = len(re.findall(re.escape(kw), body))

    h1 = next((h[2] for h in headings if h[1] == 1), "")
    if kw not in h1.lower():
        rep.add("WARN", "keyword", 0, f"Target keyword '{keyword}' not present in the H1.")

    first_para = next((t for _, t in get_paragraphs(parsed)), "")
    if kw not in strip_markdown(first_para).lower():
        rep.add("WARN", "keyword", 0, f"Target keyword '{keyword}' not present in the first paragraph.")

    if words >= 300:
        per_1500 = count * 1500 / words
        if count >= 8 and per_1500 > 7:
            rep.add("ERROR", "keyword", 0,
                    f"Keyword appears {count} times in ~{words} words "
                    f"({per_1500:.1f} per 1500). That reads as stuffing.")
        elif count < 3:
            rep.add("WARN", "keyword", 0,
                    f"Keyword appears only {count} times in ~{words} words.")


def word_count(parsed):
    text = strip_markdown("\n".join(t for _, t in prose_lines(parsed)))
    return len(text.split())


# --------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description="Lint an article against the Rich Article Writer standards.")
    ap.add_argument("path")
    ap.add_argument("--keyword", default="", help="primary target keyword")
    ap.add_argument("--json", action="store_true", help="emit JSON instead of text")
    ap.add_argument("--brand", default="", help="brand name, to check entry-depth balance")
    args = ap.parse_args()

    with open(args.path, encoding="utf-8") as fh:
        lines = fh.read().splitlines()

    parsed = strip_code_and_frontmatter(lines)
    rep = Report()

    check_dashes(parsed, rep)
    check_vocabulary(parsed, rep)
    check_cliches(parsed, rep)
    headings = check_headings(parsed, rep)
    check_paragraphs(parsed, rep)
    check_tables(parsed, rep)
    check_tldr_and_faq(parsed, rep, headings)
    check_links_inline(parsed, rep)
    check_keyword(parsed, rep, args.keyword, headings)
    check_entry_balance(parsed, rep, headings, args.brand)
    check_brand_placement(parsed, rep, headings, args.brand)

    wc = word_count(parsed)

    if args.json:
        print(json.dumps({"word_count": wc, "findings": rep.items}, indent=2))
        return 1 if rep.errors else 0

    by_rule = Counter(i["rule"] for i in rep.problems)
    print(f"Article: {args.path}")
    print(f"Approximate word count: {wc}")
    print(f"Findings: {len(rep.errors)} errors, {len(rep.warnings)} warnings\n")

    for level in ("ERROR", "WARN", "INFO"):
        items = [i for i in rep.items if i["level"] == level]
        if not items:
            continue
        print(f"--- {level} ({len(items)}) ---")
        for i in sorted(items, key=lambda x: (x["rule"], x["line"])):
            loc = f"L{i['line']}" if i["line"] else "-"
            print(f"[{i['rule']}] {loc}: {i['message']}")
            if i["excerpt"]:
                print(f"    > {i['excerpt']}")
        print()

    if by_rule:
        print("Counts by rule:", ", ".join(f"{k}={v}" for k, v in by_rule.most_common()))

    if not rep.problems:
        print("Clean. No errors or warnings." + (" Information lines above are for reference." if rep.items else ""))

    return 1 if rep.errors else 0


if __name__ == "__main__":
    sys.exit(main())
