---
title: Claim Check
summary: Audit a draft against your System of Context and get a paste-ready fix for every invented, drifted or overclaimed line.
description: A free AI skill that fact-checks marketing drafts against your company's System of Context before they ship.
categories: [content]
tags: [fact-checking, content-governance, brand-voice, copy-review]
featured: false
draft: true
output: A report of violations, unsupported and drifted claims, with fixes
platforms: [claude, claude-code, chatgpt, codex]
requirements:
  - name: Document tool connector
    required: true
    details: Wherever your System of Context is saved. Without it, the check can only flag claims as unverified.
examples:
  - prompt: Check this draft against our System of Context before it ships.
    note: Paste the draft or link it.
  - prompt: Can we say "used by thousands of enterprises"?
    note: A quick check on one line.
---

## How it works

1. **Loads your System of Context** and the pages the draft touches.
2. **Pulls out every checkable claim:** numbers, customers, quotes, competitors, capabilities, categories, and anything near an off-limits topic.
3. **Sorts them:** supported, drifted, unsupported, or a violation of one of your rules.
4. **Proposes a fix** you can paste for every problem, worst first.

## Setup

Build a System of Context first with the **Build System of Context** skill.

## Pitfalls

- **Only checking what humans wrote.** Agent-written drafts drift the most. Run it on those too.
