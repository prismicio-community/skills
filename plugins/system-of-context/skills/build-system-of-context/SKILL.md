---
name: build-system-of-context
description: "Build a company's System of Context: research its website and internal docs, interview the user for what can't be scraped (claims the product doesn't back, evidence restrictions, off-limits topics), and save positioning, product, offers, ICP, competitors, proof, voice and style as documents the user owns. Use when asked to set up a system of context, truth layer, company context or source of truth for AI, or to stop agents inventing facts."
---

# Build a System of Context

Produce a set of documents, owned by the user, that every assistant reads
before writing about the company: one overview page and twelve pages behind
it. The documents hold facts, not opinions, and are honest about what they do
not know.

The work has five phases. Two of them stop for the user. Do not skip the
stops: these documents are read by unattended runs that publish, so a wrong
fact here gets repeated everywhere.

## The standard to hold

- **Never invent.** If a fact is not found in a source or given by the user,
  it does not go in. Write `[NEEDS SOURCE]` inline or a `> ⚠️ GAP:` note.
  A plausible invented statistic is the single most expensive failure mode.
- **Tag provenance on every fact while drafting:** `[web: url]`,
  `[doc: title, url]`, `[crm]`, `[interview]`. Strip the tags before saving;
  the Status lines and the Sources page carry provenance.
- **A website is a claim, not a fact.** Anything sourced only from marketing
  pages is a public claim until the interview confirms it against the product.
- **Prefer the user's own words.** When the interview contradicts a document,
  use the user's answer and note the conflict.

## Phase 0: Inputs

Ask for whatever is missing, in one batch:

- **Company name**, as the company writes it. Case and spacing matter.
- **Website domain.**
- **Internal sources**, optional: positioning docs, ICP definitions, brand
  guidelines, decks, battlecards. Links or names.
- **Owners**, optional: who owns positioning upstream (often Product
  Marketing), which team owns learnings, who approves refreshes.
- **Where to save it**: Notion, Google Drive, Confluence, project files, or
  another document tool the user has connected.

If a System of Context already exists for this company, do not rebuild it.
Use the context-refresh skill to add sources or close gaps, unless the user
asks for a clean start.

## Phase 1: Harvest

Read `references/harvest.md`. It lists what to read on the website, what to
search for in each kind of connected source, and how to rank source quality.

Collect tagged facts into one scratch list per page. Check which connectors
are available before searching, and try the likeliest one rather than asking
which tool holds the docs.

End with a short harvest summary for the user: sources read, which pages are
strong, thin or empty, and conflicts found. Then go straight into the
interview.

## Phase 2: Interview (stop 1)

Read `references/interview.md` for the question bank and the rules for
asking. Ask only what the harvest did not answer. The must-ask questions cover
claims the product does not fully back, off-limits topics, evidence
restrictions, overloaded terms, the offers table, and absolute style rules.
"Don't know" is a valid answer; it becomes a gap with a named owner.

## Phase 3: Draft

Read `references/file-guide.md` for what each page must contain, the Status
line format, and the quality bar.

Draft every page from its template in `assets/`:

| Page | Template |
|---|---|
| Overview, titled "<Company> System of Context" | `assets/overview.md` |
| Positioning | `assets/positioning.md` |
| Messaging | `assets/messaging.md` |
| Product and offers | `assets/product.md` |
| ICP | `assets/icp.md` |
| Competitive | `assets/competitive.md` |
| Win/loss | `assets/win-loss.md` |
| Evidence | `assets/evidence.md` |
| Ecosystem | `assets/ecosystem.md` |
| Brand voice | `assets/brand-voice.md` |
| Style guide | `assets/style-guide.md` |
| Learnings | `assets/learnings.md` |
| Sources | `assets/sources.md` |

Replace `{{COMPANY}}`, `{{DATE}}`, `{{OWNER}}`, `{{UPSTREAM_OWNER}}` and
`{{LEARNINGS_OWNER}}`. Replace every `<!-- FILL: ... -->` marker with content,
or with a gap note when the fact is unknown. Never leave a marker and never
delete one silently. Leave the Learnings page empty apart from its owner:
learnings are earned, not compiled.

## Phase 4: Review (stop 2)

Show the high-stakes parts for approval, not every page. A reviewer can
approve a table in a minute and cannot meaningfully review thirteen pages.

1. The 30-second version and the non-negotiables from the overview
2. The claim vs reality table and the offers table from Product and offers
3. Evidence restrictions
4. The gaps, page by page

Apply corrections and confirm. Offer the full pages to anyone who wants them.

## Phase 5: Check and save

Before saving, check every page:

- No `FILL` marker, no `{{...}}` placeholder, no provenance tag left
- Every page opens with a **Status:** line
- No gap note inside a table row; gaps go under the table
- The Sources page has a row for every page except Learnings

Fix anything that fails. Then save to the place the user chose:

- **Notion or Confluence:** the overview as a parent page titled
  "<Company> System of Context", with the twelve pages as children.
- **Google Drive or similar:** a folder named "<Company> System of Context"
  holding thirteen documents, the overview first.
- **Project files, or no document tool:** thirteen Markdown files, named after
  the pages, for the user to add to the assistant's project knowledge.

Fill the **Pages** section of the overview with links to each saved page. If
the assistant has memory, record where the System of Context lives.

Tell the user, in plain language: where it is saved, the gaps that matter
most and who could close them, and that the system-of-context skill now loads
it automatically, the claim-check skill audits drafts against it, and the
context-refresh skill should run monthly.

## Compatibility

- **Web search and page fetching** are required for the website harvest.
- **A document tool connector** (Notion, Google Drive, Confluence or similar)
  is recommended, both as a source and as the place to save. Without one, the
  pages are delivered as Markdown files.
- **Optional:** a CRM connector and a call recorder, for win/loss and ICP.
- No code execution needed.
