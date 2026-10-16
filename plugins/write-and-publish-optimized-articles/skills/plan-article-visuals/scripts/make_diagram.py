#!/usr/bin/env python3
"""Render article diagrams to SVG from a small JSON spec.

Usage:
    python make_diagram.py spec.json out.svg

Three diagram types cover most of what an article needs. Everything else is
better hand-written as SVG or plotted with matplotlib.

  categories   labelled groups with items, for "X splits into N kinds"
  flow         left-to-right or top-down steps, for processes and decisions
  bars         horizontal bar chart, for one series of comparable numbers

Spec:
{
  "type": "categories",
  "title": "GEO tools by job",
  "groups": [{"label": "Tracking", "note": "buy first",
              "items": ["Peec AI", "Profound", "Otterly"]}, ...]
}
{
  "type": "flow",
  "title": "From gap to page",
  "steps": [{"label": "Tracker finds gap", "note": "daily"}, ...]
}
{
  "type": "bars",
  "title": "Entry price per month",
  "unit": "$",
  "bars": [{"label": "Otterly", "value": 29}, ...]
}

Colours are deliberately restrained: one accent, one neutral, plenty of white.
A diagram that needs six colours is usually two diagrams.

Standard library only. Output is plain SVG, so it scales and stays legible in
dark mode if you invert the background.
"""

import argparse
import json
import sys
from xml.sax.saxutils import escape

FONT = "system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif"
INK = "#1a1a2e"
MUTED = "#6b7280"
ACCENT = "#5b4ee5"
LINE = "#d8d8e3"
BG = "#ffffff"


def text(x, y, s, size=14, fill=INK, weight="normal", anchor="start"):
    return (f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="{size}" '
            f'fill="{fill}" font-weight="{weight}" text-anchor="{anchor}">'
            f'{escape(str(s))}</text>')


def wrap(s, width):
    words, lines, cur = str(s).split(), [], ""
    for w in words:
        if len(cur) + len(w) + 1 > width and cur:
            lines.append(cur)
            cur = w
        else:
            cur = f"{cur} {w}".strip()
    if cur:
        lines.append(cur)
    return lines


def svg(width, height, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
            f'width="{width}" height="{height}" role="img">'
            f'<rect width="{width}" height="{height}" fill="{BG}"/>{body}</svg>')


def categories(spec):
    groups = spec["groups"]
    n = len(groups)
    col_w, gap, pad = 250, 24, 32
    top = 88 if spec.get("title") else 40
    rows = max(len(g["items"]) for g in groups)
    box_h = 70 + rows * 30
    width = pad * 2 + n * col_w + (n - 1) * gap
    height = top + box_h + pad

    out = []
    if spec.get("title"):
        out.append(text(pad, 46, spec["title"], 22, INK, "600"))
    if spec.get("subtitle"):
        out.append(text(pad, 70, spec["subtitle"], 14, MUTED))

    for i, g in enumerate(groups):
        x = pad + i * (col_w + gap)
        out.append(f'<rect x="{x}" y="{top}" width="{col_w}" height="{box_h}" '
                   f'rx="10" fill="none" stroke="{LINE}" stroke-width="1.5"/>')
        out.append(f'<rect x="{x}" y="{top}" width="{col_w}" height="4" '
                   f'rx="2" fill="{ACCENT}"/>')
        out.append(text(x + 18, top + 34, g["label"], 16, INK, "600"))
        if g.get("note"):
            out.append(text(x + 18, top + 54, g["note"], 12, MUTED))
        for j, item in enumerate(g["items"]):
            y = top + 82 + j * 30
            out.append(f'<circle cx="{x + 22}" cy="{y - 5}" r="3" fill="{ACCENT}"/>')
            out.append(text(x + 36, y, item, 14, INK))
    return svg(width, height, "".join(out))


def flow(spec):
    steps = spec["steps"]
    box_w, box_h, gap, pad = 210, 92, 46, 32
    top = 88 if spec.get("title") else 40
    width = pad * 2 + len(steps) * box_w + (len(steps) - 1) * gap
    height = top + box_h + pad

    out = []
    if spec.get("title"):
        out.append(text(pad, 46, spec["title"], 22, INK, "600"))

    for i, s in enumerate(steps):
        x = pad + i * (box_w + gap)
        out.append(f'<rect x="{x}" y="{top}" width="{box_w}" height="{box_h}" '
                   f'rx="10" fill="none" stroke="{LINE}" stroke-width="1.5"/>')
        out.append(f'<circle cx="{x + 22}" cy="{top + 24}" r="11" fill="{ACCENT}"/>')
        out.append(text(x + 22, top + 29, i + 1, 12, "#fff", "600", "middle"))
        for k, line in enumerate(wrap(s["label"], 24)):
            out.append(text(x + 42, top + 29 + k * 17, line, 14, INK, "600"))
        if s.get("note"):
            for k, line in enumerate(wrap(s["note"], 28)):
                out.append(text(x + 18, top + 68 + k * 15, line, 12, MUTED))
        if i < len(steps) - 1:
            ax = x + box_w + 12
            out.append(f'<path d="M{ax} {top + box_h / 2} h{gap - 24}" '
                       f'stroke="{MUTED}" stroke-width="1.5"/>')
            out.append(f'<path d="M{ax + gap - 24} {top + box_h / 2} l-6 -4 v8 z" '
                       f'fill="{MUTED}"/>')
    return svg(width, height, "".join(out))


def bars(spec):
    data = spec["bars"]
    pad, label_w, bar_h, gap = 32, 170, 26, 14
    top = 88 if spec.get("title") else 40
    track = 420
    width = pad * 2 + label_w + track + 70
    height = top + len(data) * (bar_h + gap) + pad
    peak = max(b["value"] for b in data) or 1
    unit = spec.get("unit", "")

    out = []
    if spec.get("title"):
        out.append(text(pad, 46, spec["title"], 22, INK, "600"))
    if spec.get("subtitle"):
        out.append(text(pad, 70, spec["subtitle"], 14, MUTED))

    for i, b in enumerate(data):
        y = top + i * (bar_h + gap)
        w = max(3, track * b["value"] / peak)
        out.append(text(pad + label_w - 12, y + 18, b["label"], 14, INK, "normal", "end"))
        out.append(f'<rect x="{pad + label_w}" y="{y}" width="{track}" '
                   f'height="{bar_h}" rx="4" fill="#f2f2f7"/>')
        out.append(f'<rect x="{pad + label_w}" y="{y}" width="{w:.1f}" '
                   f'height="{bar_h}" rx="4" fill="{ACCENT}"/>')
        out.append(text(pad + label_w + w + 10, y + 18,
                        f"{unit}{b['value']:,}", 13, MUTED))
    return svg(width, height, "".join(out))


RENDERERS = {"categories": categories, "flow": flow, "bars": bars}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("spec")
    ap.add_argument("out")
    args = ap.parse_args()

    spec = json.load(open(args.spec, encoding="utf-8"))
    kind = spec.get("type")
    if kind not in RENDERERS:
        print(f"Unknown type {kind!r}. Expected one of {', '.join(RENDERERS)}.",
              file=sys.stderr)
        return 1

    out = RENDERERS[kind](spec)
    with open(args.out, "w", encoding="utf-8") as fh:
        fh.write(out)
    print(f"Wrote {args.out} ({len(out):,} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
