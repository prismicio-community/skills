# Screenshot Shot List

Every screenshot is specified here first, then captured one of two ways: `scripts/capture_shots.py` for anything reachable without a login, and a real authenticated browser session for everything else. Say plainly which shots went which way, and never substitute a weaker visual for one you could not take.

A good shot list is an hour of someone's time. A vague one is a meeting.

## Format

One numbered entry per shot:

```
SHOT 3 — Peec AI Actions view
URL / screen:  app.peec.ai → Actions tab, any tracked project
Must show:     the opportunity list with gap scores visible, at least 5 rows
Must not show: account name, billing, teammate names, customer domains
Viewport:      1440 x 900, light mode, browser chrome cropped out
Supports:      the claim that Peec turns citations into a scored work queue
Caption:       "Cited sources clustered into owned and earned opportunities,
                scored by gap size, which is what turns a score into a queue"
Alt text:      "Peec AI Actions view listing content opportunities ranked by
                the size of the visibility gap"
Capture date:  record on capture
```

The `Supports` line matters most. A screenshot that does not evidence a specific claim in the article is decoration, and should be cut rather than captured.

## Rules

- **One claim per shot.** A screenshot showing four things evidences none of them.
- **Crop to the evidence.** Full-page captures at article width are unreadable.
- **Consistent viewport across a listicle.** Mixed sizes and themes read as sloppy and make tools look unequal.
- **Never a marketing page.** A screenshot of a vendor's homepage evidences nothing about the product.
- **Trial accounts are fine**, but empty states are not: populate enough data that the interface shows what it does.
- **Redact aggressively.** Never another company's customer data. Blur account identifiers in your own.
- **Record the capture date** for every shot. Interfaces move.

## Capturing the public ones

```bash
python scripts/capture_shots.py shots.json --out ./images
```

The JSON is the shot list in machine form. Only `id`, `name` and `url` are required; `wait_for`, `clip_to`, `hide` and `full_page` handle the awkward pages. Common cookie banners and chat widgets are hidden automatically.

Always look at what came back before using it. A page that loaded a consent wall, an empty state, or a layout shift produces a technically successful capture that evidences nothing.

The `manifest.json` records capture date, final URL and viewport per shot. Copy those dates into the article appendix, since that is what makes a screenshot auditable when the interface changes.

## Ordering

Number shots in article order and reference the numbers from the placeholders in the draft, so whoever captures them can work top to bottom without cross-referencing.

## Legal

Screenshots of a competitor's product in a genuine comparative review are normal and defensible. Three conditions keep them that way:

1. Capture from the real product, not the vendor's marketing site, where images are usually copyrighted.
2. Label accurately and do not crop to distort.
3. Keep them current. An outdated screenshot of a competitor is a fairness problem as well as an accuracy one.

For anything in a paid or regulated context, get someone to check rather than relying on this note.
