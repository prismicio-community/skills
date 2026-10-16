---
name: plan-article-visuals
description: "Decide which sections of an article earn a visual, generate the diagrams and charts that can be generated, and write captions, alt text and a precise shot list for screenshots. Use for 'what images does this article need', 'make a diagram for this section', 'add visuals before publishing'. Not for photos, illustrations or hero images."
---

# Article Visual Brief

Two jobs. Decide what the article actually needs, then make what can be made and specify the rest precisely.

Most articles are over-illustrated and under-diagrammed. Stock photography of people at laptops adds load time and nothing else. A single diagram that shows the structure of an argument can be the most shared thing on the page.

## Step 1: audit the draft

Go section by section and ask one question: **is there something here a reader would understand faster by seeing it?**

Four honest yeses:

- **A structure the prose has to describe serially.** Categories, hierarchies, relationships. Text reveals these one clause at a time; a diagram shows them at once.
- **A process with order and dependencies.** Steps, decision points, loops.
- **Numbers meant to be compared.** Three or more comparable values.
- **An interface being discussed.** If the article says a tool does something, showing it doing that is proof rather than decoration.

Four honest noes, and these are where most articles go wrong:

- A section that already fits in three sentences.
- An image restating the heading.
- Stock photography, always.
- A logo grid, unless the article is about the logos.

**Two to five visuals suits most articles.** A how-to with eight steps may want one per step. An opinion piece may want none. If a section's visual would only repeat the paragraph above it, cut it.

## Step 2: write the brief

Every planned visual gets a line, in the article and in the appendix:

`[IMAGE | type | what it shows | what the caption must point out | alt text]`

Four rules that decide whether the visual is worth its bytes:

- **The caption does work.** It states what to notice, not what the image is. "The page type after the rebuild" is a label. "The three fields editors never filled in are gone: 22 fields down to 9" is a caption.
- **Alt text describes content, not the file.** One sentence carrying the same substance as the caption, for anyone who cannot see it.
- **Every screenshot carries a capture date** in the appendix. Interfaces move, and an undated screenshot ages invisibly.
- **Name the source.** Generated here, captured by a person, or supplied by the user. This decides what happens in step 3.

## Step 3: make what can be made

```bash
python scripts/make_diagram.py spec.json out.svg
```

Three types, each from a small JSON spec. Read `references/diagram-specs.md` for the full schemas.

- **`categories`** — labelled groups with items. For "X splits into N kinds", which is the most common structural claim in a comparison article.
- **`flow`** — numbered left-to-right steps with notes. For processes and decisions.
- **`bars`** — one series of comparable numbers, sorted.

Output is SVG: it scales, stays sharp, and stays editable. For anything more complex, write the SVG directly or plot with matplotlib rather than forcing it into these three shapes.

To check the result, rasterize and look at it. Do not ship a diagram you have not seen:

```bash
pip install cairosvg --break-system-packages -q
python -c "import cairosvg; cairosvg.svg2png(url='out.svg', write_to='out.png', scale=1.2)"
```

Then `view` the PNG. Text overflow and collisions are obvious visually and invisible in the source.

## Step 4: specify what cannot be made

Write the numbered shot list first, precise enough that it can be worked through without asking questions. Read `references/shot-list.md` for the format and the legal points. Then split it in two.

**Public pages** (pricing, docs, marketing sites, anything reachable without a login) can be captured with Playwright:

```bash
pip install playwright && python -m playwright install chromium
python scripts/capture_shots.py shots.json --out ./images
```

It hides cookie banners and chat widgets, supports cropping to an element, and writes a `manifest.json` with the capture date, final URL and viewport for every shot. Add `--insecure` only inside a sandbox behind a TLS-intercepting proxy, never on an untrusted network.

**Anything behind a login** (product dashboards, which is most of what a tools comparison needs) cannot be captured this way, and storing a competitor's credentials in a script is a bad idea regardless. Hand those shots to a person working in a real browser session, or to a browser-automation tool that drives the user's own already-authenticated browser.

Say plainly which shots you captured and which you handed off. Do not substitute a weaker visual for a screenshot you could not take.

Each entry names the URL or screen, what must be visible in frame, what must not be (personal data, customer names, billing detail), the viewport, and the caption the shot has to support.

A good shot list is an hour of someone's time. A vague one is a meeting.

## Step 5: hand back

Deliver the SVG files, the shot list, and the caption and alt text for every visual including the ones not yet captured. Update the article with placeholders in position so the gaps are visible in context rather than tracked in a separate document.

If the article is going to a CMS, note that placeholders must not reach a release. An unfilled placeholder that gets published is worse than no image.

## Legal points worth holding

Screenshots of a competitor's product in a genuine comparative review are normal and defensible. Three conditions keep them that way: capture from the real product rather than the vendor's marketing site, where images are usually copyrighted; label accurately and do not crop to distort; keep them current, since an outdated screenshot of a competitor is a fairness problem as well as an accuracy one.

Never show another company's customer data, and blur account identifiers in your own.

## Compatibility

- **Scripts** (`scripts/make_diagram.py`, `scripts/capture_shots.py`): need a client that can run Python. Without one, deliver the diagram specs and the shot list for someone else to produce.
- No connectors needed.
