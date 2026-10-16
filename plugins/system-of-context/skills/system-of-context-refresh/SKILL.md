---
name: system-of-context-refresh
description: "Keep a System of Context current: check each page against its upstream source, propose a reviewed diff, apply approved changes in the documents, and add, confirm or retire learnings. Use monthly, when the context feels out of date, when someone asks when it was last refreshed, when a page contradicts its source, to add a new source, before a high-stakes deliverable, or to record a new learning."
---

# Context refresh

Compiled context decays silently. This skill makes the decay visible and
proposes a diff, so refreshing becomes a ten-minute review instead of a chore
nobody owns.

## Never edit without approval

Propose the diff first. Change the documents only after the user approves it
in this conversation. An unreviewed automated edit to the truth layer is worse
than a stale one, because nobody knows it happened.

## Find the System of Context

1. Check the assistant's memory and project files for a document titled
   "<Company> System of Context".
2. Otherwise search the connected document tools for "System of Context".
3. If you find more than one, ask which. If you find none, offer to build one
   with the build-system-of-context skill and stop.

Read the overview and the **Sources** page first. Sources says where each page
comes from and what kind of source it is.

## Refresh

### 1. Staleness sweep

For each row on **Sources**, check freshness by source type:

| Type | How to check |
|---|---|
| `notion`, `confluence` | Fetch the page. Record last edited date and verification or approval state if exposed. |
| `drive` | Fetch file metadata. Record modified date and owner. |
| `web` | Fetch the page and compare it with the System of Context page. |
| `crm` | Re-run the query for the latest period. |
| `interview` | List the facts that rest only on the interview and ask the named owner to confirm them. |
| `none` | Note the page is still a gap and ask whether a source now exists. |

Flag: last edited more than 90 days ago, expired or missing verification,
anything still marked incomplete upstream, and any source that no longer
resolves.

### 2. Content diff

Compare each page with its source. Report only substantive changes: a changed
number, a new or removed claim, a reworded value prop, a new competitor, a new
proof point, a changed restriction. Ignore formatting, reordering and
copy-editing.

Look hardest at what moves most and costs most when wrong:

- The claim vs reality table on **Product and offers**: has a capability shipped or narrowed?
- The offers table: new offer, retired offer, changed fit signals?
- Evidence restrictions: has a new one appeared?
- Off-limits topics in the non-negotiables: still off limits?
- The category split on **Ecosystem**
- Gaps: has any `⚠️ GAP` been closed upstream?

Skip **Learnings**. It has no upstream source and is maintained by review.

### 3. Report

```
## Staleness
| Page | Source | Last edited | Verification | Flag |

## Proposed changes
### <Page>
- CHANGE: [current text] → [source text] → [source URL]
- ADD: [new text] → [source URL]
- REMOVE: [text no longer in source]

## Needs an owner decision
- [item, and why the source can't resolve it]

## No change: [list of pages]
```

### 4. Route the decisions

Anything that needs a human decision (sources that contradict each other, a
gap past its promised date, an unclear restriction) goes to its owner, not
into the diff. If a task or ticket tool is connected, offer to create one per
decision.

### 5. Apply, after approval

1. Edit each approved page in place through the document tool. If the System
   of Context lives in project files, give the user the updated pages to
   replace them.
2. Update each changed page's Status line, and the `Last read` column on
   **Sources**.
3. Add a row to the refresh log on **Sources**: date, what changed, who
   approved it.

## Learnings

The **Learnings** page follows its own lifecycle, explained on the page.

- **Add.** Write the entry in the page's format, as provisional, with a
  review-by date one quarter out. Reject entries that fail the page's test (a
  report or a status update is not a learning) and say why.
- **Confirm.** Only with evidence from a second, independent cohort.
- **Retire.** Delete the entry. Do not soften it to "used to be true".
- On every refresh, list provisional entries past their review-by date and
  propose retiring them.

Learnings changes need the same approval as any other edit.

## What to avoid

- **Empty reports on a schedule.** Monthly is the right cadence. If three runs
  in a row find no changes, suggest a longer interval.
- **Diffing taste.** Copy-editing upstream is not a change. Only substance is.

## Compatibility

- **A document tool connector** (Notion, Google Drive, Confluence or similar)
  to read sources and edit the System of Context.
- **Web page fetching** for sources of type `web`.
- **Optional:** a CRM connector for `crm` sources, and a task tool for routing
  decisions.
- No code execution needed.
