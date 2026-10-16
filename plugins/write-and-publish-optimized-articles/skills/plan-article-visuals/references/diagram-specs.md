# Diagram Specs

`scripts/make_diagram.py spec.json out.svg` takes one JSON object. Three types.

Colours are fixed on purpose: one accent, one neutral, plenty of white. A diagram that needs six colours is usually two diagrams.

## categories

For "X splits into N kinds", the most common structural claim in a comparison article.

```json
{
  "type": "categories",
  "title": "GEO tools by the job they do",
  "subtitle": "Most teams need one from tracking plus one from creation",
  "groups": [
    {"label": "Tracking", "note": "Buy first",
     "items": ["Tool A", "Tool B", "Tool C"]},
    {"label": "Creating", "note": "Closes the gap",
     "items": ["Tool D", "Tool E", "Tool F"]}
  ]
}
```

Four groups fit comfortably at normal article width. More than five or six items in a group makes the boxes tall and thin, so split the diagram or shorten the list.

## flow

For processes and decisions with real order.

```json
{
  "type": "flow",
  "title": "From visibility gap to published page",
  "steps": [
    {"label": "Tracker finds a lost prompt", "note": "Runs daily"},
    {"label": "Decide create or update", "note": "Against existing pages"}
  ]
}
```

Four or five steps is the useful maximum. Labels wrap at roughly 24 characters and notes at 28, so a long label pushes into the note area. Keep labels to a few words.

## bars

One series of comparable numbers. Not for two numbers, which belong in a sentence.

```json
{
  "type": "bars",
  "title": "Reported entry price per month",
  "subtitle": "Confirm with vendors before budgeting",
  "unit": "$",
  "bars": [{"label": "Otterly", "value": 29}, {"label": "Peec AI", "value": 95}]
}
```

Sort deliberately, usually ascending, and say in the caption what the sort means. Bars scale against the largest value, so a single outlier flattens everything else. Split it out or name it in the caption.

**Label uncertain data honestly in the subtitle.** If numbers are reported rather than confirmed, the chart has to say so, because a chart reads as more authoritative than the sentence that qualified it.

## Beyond these three

Write SVG directly, or use matplotlib for statistical plots. Do not distort content to fit one of these shapes. The shape serves the point, not the other way round.

## Always look at the output

```bash
pip install cairosvg --break-system-packages -q
python -c "import cairosvg; cairosvg.svg2png(url='out.svg', write_to='out.png', scale=1.2)"
```

Then `view` the PNG. Text overflow, collisions and bad wrapping are obvious on sight and invisible in the source.
