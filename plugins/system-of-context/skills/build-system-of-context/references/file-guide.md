# File guide

What each page must contain, and the bar it must clear. Every template in
`assets/` has `FILL` markers that match the sections below.

## Rules for every page

**Status line first.** Every file opens with a Status line an agent can use to
decide whether to trust it:

```
**Status:** Compiled from <source names> (<source type>, last edited <date>,
<verified | unverified | n/a>). Confidence: <strong | usable | thin>.
<One sentence on what is weak or most likely to drift.>
```

- **strong**: approved internal source, recently edited
- **usable**: internal but unverified, or website plus interview
- **thin**: website only, or mostly gaps

**Gaps are written, not skipped.** Use this exact form so agents and the
refresh skill can find them:

```
> ⚠️ GAP: <what is missing>. <What to do instead>. Owner: <who could close it>.
```

**Never put a gap inside a table cell.** If a table would have no real rows,
replace the whole table with a gap. If one row is partly known, write
"Unknown" in the empty cells and put the gap note directly under the table.

**Full docs at the end.** List the upstream sources with URLs so an agent can
go to the source on a high-stakes task.

**No provenance tags in the body.** Tags like `[web: ...]` are for drafting.
Strip them; the Status line and Full docs carry provenance.

**Short beats complete.** Each page should be readable in two minutes. If a
page runs past about 120 lines, it is probably carrying content that belongs
upstream.

## Positioning

- One-line positioning
- Three or four core value props, each one line
- What the positioning is against (a competitor, a way of working, inertia)
- Vision, only if the company has an approved one. Otherwise a gap.
- Positioning guardrails: links to the claim vs reality table and ecosystem

## Messaging

- One-liner and one-paragraph pitch, verbatim from the source
- Taglines in use
- We say / we don't say table. These substitutions carry meaning, so state
  why when it isn't obvious.
- Words never to use in messaging (may overlap with brand-voice)

## Product and offers

The most important file and the one most likely to drift.

- Core product in two or three sentences
- Key features, one line each, named exactly as the product names them
- **Offers table.** Required. Downstream skills use it to decide what to sell
  to whom.

  ```
  | Offer | What it is | Good-fit signals | Not a fit when | Proof to use |
  ```

- **Claim vs reality table.** Required, even if the user says there are no
  gaps (then one row stating that, dated). Columns: Claim | Current reality.
- One line telling agents what to do when a task needs one of these claims:
  state what is true today and flag the gap.

## ICP

- Fit profile: the qualitative traits of a great-fit account
- Requirements (technical or organizational), if any
- Firmographics with confidence labels. Never a headline size range without
  its confidence.
- Champion and economic buyer
- Job to be done
- Persona notes, or a gap pointing to where personas live

## Competitive

- Competing alternatives in three tiers: status quo, alternative approaches,
  direct competitors
- One angle per competitor or group, stated honestly
- Where real losses come from (link to win-loss)

## Win/loss

- A banner if the data is thin: sample sizes and confidence
- Why we win, why we lose, with figures only as the source states them
- Named competitors and where they beat us
- Known objections. If responses are not written upstream, say so; never
  invent objection handling.
- Data gaps: what cannot be claimed

If there is no win/loss data at all, the page is one Status line and one gap.
That is a valid outcome.

## Evidence

- **Restrictions first**, in a warning block, before any proof point
- Top proof points with exact numbers, customer, date, URL
- Go-to quotes with full attribution
- Scale and credibility facts (customer count, review-site ratings) with dates
- Matching guidance: which proof backs which offer

## Ecosystem

- **Category table**: claimed, partial, real. How to use each layer.
- Integrations, frameworks or platforms the product works with
- Adjacent tool landscape
- What is table stakes (a qualifier, not a differentiator)

## Brand voice

- The relationship or personality, in a short paragraph
- Core values and qualities, each with a do and a don't example
- Banned words and phrases, absolute
- Absolute punctuation or format bans
- How proportions shift by context, if the source says

## Style guide

- Spelling convention, serial comma, numbers, dates, headings
- Point of view and lists
- Links, emoji, abbreviations
- Company and product naming and capitalization
- If the source is old, say so in the Status line and say which file wins on
  product names (Product and offers)

## Learnings

Starts empty. The template carries the lifecycle (provisional, confirmed,
retired), the entry format, and the test for what belongs. Fill only the team
name and the review cadence. Do not seed it with harvested facts; learnings
are earned, not compiled.

## Sources

One row per page. The system-of-context-refresh skill depends on it.

```
| File | Source | Type | URL or location | Last read | Owner |
```

Type is one of: `notion`, `drive`, `confluence`, `web`, `crm`, `interview`,
`none`. Use `interview` for facts that came only from the user, and name the
person in Owner.
