---
title: System of Context Skill
summary: Loads your company's facts, offers, proof and voice before an assistant writes or reviews anything about you.
description: A free AI skill that loads your company's System of Context before every writing task, so assistants stop inventing facts.
categories: [content]
tags: [context, positioning, brand-voice, messaging]
featured: false
draft: true
output: Writing grounded in your own approved facts
platforms: [claude, claude-code, chatgpt, codex]
requirements:
  - name: Document tool connector
    required: true
    details: Notion, Google Drive, Confluence or project files, wherever your System of Context is saved.
examples:
  - prompt: Write a landing page for our analytics add-on.
    note: Any writing task about your company triggers it.
  - prompt: Who do we sell to, and why do we lose deals?
    note: Answers come from your own pages, with gaps named.
  - prompt: Can we say we integrate with every CMS?
    note: Checked against your claim vs reality table.
---

## How it works

1. **Finds your System of Context.** Looks in the assistant's memory and project files, then searches your connected document tools.
2. **Reads only what the task needs.** A routing table on the overview page points to the two or three pages that answer the question.
3. **Applies your rules.** Never invents a number, flags any claim the product doesn't back yet, respects evidence restrictions, and follows your own non-negotiables, such as topics that are off limits.
4. **Names the gaps.** When a page is thin or a fact is missing, it says so instead of guessing.

## Setup

Build a System of Context first with the **Build System of Context** skill, and keep its document tool connected.

## Pitfalls

- **Treating learnings as facts.** Your team's learnings are marked provisional until they replicate. The assistant says so when one carries a big decision.
