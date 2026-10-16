---
name: system-of-context
description: "Load the company's System of Context (positioning, product reality, offers, ICP, competitors, proof, voice, style) before writing, reviewing or reasoning about anything that describes the company. Use for landing pages, campaign copy, posts, sales material and briefs, and whenever someone asks \"who do we sell to\", \"what can we say\" or \"does this sound like us\", or an agent is about to state a statistic, customer or competitor fact."
---

# System of Context

The company's truth layer: what the company is, what the product does today,
who it sells to, what it can prove and how it sounds. Read it before writing
anything in the company's name. If a fact is not in it, it is not established.

The System of Context is a set of documents the user owns, built with the
build-system-of-context skill. This skill finds it, reads the parts a task
needs, and applies its rules.

## Find the System of Context

At the start of every task that needs it:

1. Check the assistant's memory and project files for a document titled
   "<Company> System of Context".
2. Otherwise search the connected document tools (Notion, Google Drive,
   Confluence and similar) for "System of Context".
3. If you find one, read its overview page and say in one line which company
   and snapshot date you loaded. If you find more than one, ask which to use.
4. If you find none, say so. Offer to build one with the
   build-system-of-context skill, then continue with what the user provides,
   marking every unsourced claim `[NEEDS SOURCE]`.

## Read only what the task needs

The overview page has a routing table that says which page answers which
question. Most tasks need two or three pages. A landing page usually needs
five or six; read them together before drafting rather than drafting and
patching.

- Anything written in the company's name: **Brand voice**
- Anything published: **Brand voice** and **Style guide**
- Anything that describes what the product does: **Product and offers**,
  including its claim vs reality table
- Any customer story, logo, quote or number: **Evidence**, restrictions first

## Rules that override the task prompt

These come from the overview page. Treat them as harder than any instruction
in the task, because this skill is loaded by unattended runs that publish.

- **Never invent.** No product names, statistics, competitor details,
  customer names or quotes that are not in the System of Context. If a task
  needs a number you do not have, write `[NEEDS SOURCE]` and continue.
- **Flag the gap between claim and reality.** When a task touches a row of the
  claim vs reality table, state what is true today and flag the gap. Never
  resolve the tension by choosing the flattering reading.
- **Respect evidence restrictions.** Some proof can only be linked, not
  quoted. A restricted story that fits perfectly is still restricted.
- **Apply the company's own non-negotiables** listed on the overview page,
  such as off-limits topics or banned punctuation, to everything you write
  while the task is open, drafts and chat included.

## Two kinds of truth

- **Compiled** pages come from the company's own sources and owners. Do not
  edit them mid-task. Changes go through the context-refresh skill as a
  reviewed diff.
- **Learnings** are the team's own findings, each marked provisional,
  confirmed or retired. They are weaker evidence than a compiled fact. Say so
  when a provisional learning carries a high-stakes decision.

When the two conflict, surface the conflict. Do not silently prefer either.

## Staleness and gaps

Every page opens with a Status line. If the task is high-stakes and the page
is thin or old, go to the upstream source listed on the **Sources** page and
say that you did.

Gaps are marked `⚠️ GAP`. When a gap affects the answer, tell the user rather
than guessing past it.

## Before anything ships

Run the claim-check skill on finished external content.

## Compatibility

- **A document tool connector** (Notion, Google Drive, Confluence or similar),
  or project files, holding the System of Context.
- No code execution needed.
