---
name: personalized-landing-pages
description: "Build personalized landing pages in Prismic for target accounts from company domains and a base page: CRM and web research, an offer fit verdict, a section-by-section plan, copy that fits the layout, then drafts in a Prismic release. Use when asked for an ABM, account or personalized landing page, a page for a named company, or to adapt a Prismic page for an account or segment."
---

# Personalized landing pages

Turn a list of company domains plus one base page into personalized landing
page drafts in Prismic, each grounded in researched facts and each fitting the
base page's designed layout.

What makes these pages work is not find-and-replace. It is deciding **what to
sell this account** before writing anything, then deciding **which sections
carry that story** before writing anything. Two artifacts, produced in that
order, before a single field of copy exists.

## Before anything: load the seller's context

The pages sell the user's company, so the skill needs that company's offers,
voice and proof. Read `references/context-intake.md` and follow it. In short:

1. If the seller has a System of Context (documents titled
   "<Company> System of Context", built with the build-system-of-context
   skill), read its Product and offers, Evidence, Brand voice, Style guide and
   ICP pages.
2. Otherwise look for any brand, voice or company-context material the
   assistant can reach, and use what it has.
3. Fill what is still missing with a short intake. The one thing that can
   never be skipped is the **offers table**: without it there is no verdict,
   and without a verdict the pages are mail merge.

## Inputs

Ask for whatever is missing. Do not guess at a base page or a repository.

| Input | Required | Notes |
|---|---|---|
| Company domains | Yes | One or many. |
| Base page | Yes | Prismic URL or document ID. |
| Prismic repository | Yes | Ask if it cannot be read from the base page URL. |
| Release name | No | Defaults to `<Account> personalized page`, or `<N> account pages, <date>` for a batch. |
| Named contact | No | If omitted, resolve the best contact from the CRM. Company-level if none exists. |

## Two approval gates, and three stop conditions

For a batch, batch the gates. Do not stop once per account; that turns ten
domains into twenty interruptions.

**Gate 1: all fit verdicts together.** Every account's verdict in one table.
Nothing is written until this is approved.

**Gate 2: all page plans together.** Every account's section-by-section plan
in one pass. No copy exists yet.

Between the gates, run research and planning for every account without
stopping.

Three things force an unscheduled stop. Fold them into the nearest gate when
you can, so they cost nothing extra.

1. **The verdict disagrees with the base page.** The base page is built for one
   offer, and the verdict picked a different one. Present the conflict and the
   options, then wait. See `references/research-and-verdict.md`.
2. **No approved proof point exists for the chosen offer.** Ask which customer
   story to use. Never invent a customer, a quote, a logo or a number.
3. **A claim cannot be sourced.** Soften it or cut it. If it is load-bearing
   for the page, ask.

Publishing is never automatic. Create drafts in a release and stop. Publish
only when someone says publish, in that message.

## The pipeline

### 1. Read the base page as a structural contract

Read `references/cms-prismic.md` for how to read the page from Prismic. Then
transcribe every section in order and classify it:

- **fixed**: do not touch. Event recaps, how-it-works, mechanism explanations.
- **personalizable**: copy changes, structure does not. Hero, problem cards,
  CTA bullets.
- **swappable**: the whole module can be replaced or reordered. Feature
  sections, proof modules.

Record per personalizable field: field name, section, base copy, **character
count**. Record the item count of every repeatable group. Mark functional
fields (links, form IDs, identifiers that drive widgets) as not copy. This
table is the length budget, and it is how the page survives contact with a
designed layout.

Reclassification is allowed, but it is a decision, not a shortcut. If the
verdict needs a fixed section rewritten, say so at Gate 1 and let the human
take the call.

### 2. Pull CRM context before touching the web

Query the connected CRM for the company record and its engagements: notes,
calls, meetings, emails, deals. Summarize into typed facts, each with a source
and an ID you can cite later (`C1`, `C2`...).

A thin record is itself a finding. Say "cold account, the page earns attention
on research alone" rather than padding. If no CRM is connected, say so and
continue on web research.

Read `references/research-and-verdict.md` for query patterns, the junk-record
trap and the division-mismatch rule. Both matter more than they sound.

### 3. Web research aimed at the business model

One research run per account against a fixed schema: how they make money and
sell, their web estate, whether they sell to named accounts or a mass
audience, concrete hooks from the last twelve months, and uncertainties
flagged rather than asserted. Each fact gets an ID (`W1`, `W2`...).

Search beyond the account's own domain. Prefer a connected tool over a web
search when the tool owns the number, and say which tool each number came
from.

The best hook is usually the account's own words: a filing, an earnings call,
a published post, or a line from a call transcript in the CRM. A company
quoting its own disclosure back to itself is hard to dismiss as marketing.

### 4. The fit verdict

Score the account against the **offers table** and emit a verdict with three
parts: a ranking, an explicit **do not pitch** list, and a one-line rationale
for each.

The exclusions carry as much weight as the ranking. Naming what you are not
selling an account reads as honesty; a page that pitches everything reads as
a template.

Also check fit against the ICP. An account far outside it is a finding worth
surfacing, not something to quietly ignore.

**This is Gate 1.** Present all verdicts, plus any base-page conflicts, and
wait.

### 5. Page plan

Map each verdict onto the section contract. Per section: keep, reorder, swap,
or rewrite, with the specific fact ID that backs it.

A swap replaces a module; it never appends one. Adding a section requires the
verdict to call for it explicitly, and it must be a section type that already
exists in the repository.

**This is Gate 2.** Present all plans, plus any proof-point gaps, and wait. A
reviewer can approve a plan in seconds and cannot meaningfully review finished
copy.

### 6. Write the copy under constraints

Only now. Read `references/copy-constraints.md` before writing the first
field.

The four constraints in short: every claim traces to a fact ID; the H1 states
the account's stakes and carries the company name exactly as they write it;
every field stays within ±10% of its base character count; voice rules from
the seller's context are hard constraints, not inspiration.

When a fact is too long for its field, shorten the fact. Never stretch the
field. Cut the qualifier, keep the number.

### 7. Verify mechanically

Run `scripts/length_check.py` rather than eyeballing it. Failures loop back to
step 6, not to the human.

```bash
python3 scripts/length_check.py fields.json
```

It checks length parity per field, repeatable group item counts, banned words
and characters, and the H1 rules. Build `fields.json` as you write, with the
seller's banned words copied in from their brand voice. See the script's
header for the shape.

Then check by hand what a script cannot: every claim matched to a sourced
fact, every capability claim consistent with the seller's claim vs reality
table, and verdict conformance, meaning the page leads with the chosen offer
and mentions none of the excluded ones. If the claim-check skill is available,
run it on the finished copy.

Approved exceptions are allowed and should be rare. A customer quote or a
person's name cannot be padded or trimmed to hit a character count, so when
one falls outside budget, report it as an exception rather than altering it.

### 8. Deliver with the reasoning attached

Create every draft inside one named release. Follow the write protocol in
`references/cms-prismic.md`; it contains a failure mode that will otherwise
cost you duplicate releases.

Report back per account: document link and release name, the hook and the fit
verdict with its source, what changed versus the base section by section, the
length check table including exceptions, and anything that could not be
sourced.

End on what is still missing. A page delivered with its gaps named is more
useful than one delivered as finished.

## Batches

For more than one account, propose clusters first and get them approved:
shared pain, shared industry, shared stack. Then run steps 2 through 8 per
account.

Pages in a batch must differ at the narrative level, not just in the company
name. If two accounts produce the same page with a different logo, the
clustering was wrong or the research was thin. Each page still passes its own
length check against the same base.

## Compatibility

- **A Prismic connector** is required, to read the base page and create drafts
  in a release.
- **Web search and page fetching** are required for account research.
- **Code execution** is required for the length check in `scripts/` (Python 3,
  no extra packages). Without it, count characters field by field and say the
  check was manual.
- **Optional:** a CRM connector (HubSpot, Salesforce or similar) and a call
  recorder, for engagement history. A document tool holding the seller's
  System of Context.

## References

- `references/context-intake.md`: finding the seller's context, and the intake when there is none
- `references/research-and-verdict.md`: CRM patterns, the junk-record trap, division mismatches, research schema, verdict logic and the base-page conflict
- `references/copy-constraints.md`: length parity, H1 rules, voice rules, fact grounding, worked examples
- `references/cms-prismic.md`: reading the base page from Prismic, releases, drafts, the silent-success failure mode
- `scripts/length_check.py`: mechanical verification
