---
title: Context Refresh
summary: Check every page of your System of Context against its source and approve a reviewed update, with a log of what changed.
description: A free AI skill that keeps your company's System of Context current with reviewed, logged updates.
categories: [content]
tags: [context, content-governance, positioning, maintenance]
featured: false
draft: true
output: A staleness report and a proposed diff, applied once you approve
platforms: [claude, claude-code, chatgpt, codex]
requirements:
  - name: Document tool connector
    required: true
    details: Reads the sources and edits your System of Context.
  - name: Web page fetching
    required: false
    details: Needed when pages come from your website.
examples:
  - prompt: Refresh our System of Context.
    note: Run monthly.
  - prompt: Add a learning. Account pages that open with the account's own numbers got replies from 7 of 20 accounts, versus 1 of 20 for generic openers.
    note: Records a provisional learning with a review date.
---

## How it works

1. **Checks freshness.** Looks at every source on the Sources page: last edited, verification, and whether it still resolves.
2. **Diffs the substance.** Changed numbers, new claims, new proof, new restrictions. Formatting changes are ignored.
3. **Proposes a diff** and routes anything that needs a decision to its owner.
4. **Applies what you approve,** updates the Status lines, and logs the change.
5. **Manages learnings:** adds new ones as provisional, confirms them with a second cohort, and retires the ones past their review date.

## Setup

Build a System of Context first with the **Build System of Context** skill, and keep its document tool connected.

## Pitfalls

- **Letting it lapse.** A refresh takes ten minutes monthly. A stale page reads exactly like a current one.
