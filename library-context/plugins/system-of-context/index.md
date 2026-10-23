---
title: System of Context
summary: Build a truth layer of your company's facts, offers, proof and voice, so AI assistants stop inventing and check drafts before they ship.
description: A free AI plugin that builds your company's System of Context, checks drafts against it, and keeps it current.
categories: [content]
tags: [context, positioning, brand-voice, messaging, fact-checking, content-governance]
featured: false
draft: false
problem: AI keeps getting your product, pricing or voice wrong?
output: A set of documents you own, plus a claim check on every draft
requirements:
  - name: Document tool connector
    required: true
    details: Notion, Google Drive, Confluence or similar. A source while building, then where your System of Context is saved and where every other skill reads it. Without one, you get Markdown files to add to your project.
  - name: Web search
    required: true
    details: Reads your website for positioning, product, customers and voice.
  - name: CRM connector
    required: false
    details: Adds win/loss and ICP patterns from your closed deals.
skills:
  - name: build-system-of-context
    title: Build System of Context
    summary: Research your website and docs, interview you for what isn't written down, and save your company's truth layer as documents you own.
    output: Thirteen pages saved in your document tool
    example: Build a System of Context for our company. Our website is example.com.
  - name: system-of-context
    title: System of Context
    summary: Loads your company's facts, offers, proof and voice before an assistant writes or reviews anything about you.
    output: Writing grounded in your own approved facts
    example: Write a landing page for our analytics add-on.
  - name: system-of-context-claim-check
    title: Claim Check
    summary: Audit a draft against your System of Context and get a paste-ready fix for every invented, drifted or overclaimed line.
    output: A report of violations, unsupported and drifted claims, with fixes
    example: Check this draft against our System of Context before it ships.
  - name: system-of-context-refresh
    title: Context Refresh
    summary: Check every page of your System of Context against its source and approve a reviewed update, with a log of what changed.
    output: A staleness report and a proposed diff, applied once you approve
    example: Refresh our System of Context.
examples:
  - prompt: Build a System of Context for our company. Our website is example.com and our positioning docs are in Notion.
    note: Run this once. Plan for 30 to 60 minutes, most of it a short interview.
  - prompt: Write a landing page for our analytics add-on.
    note: Any writing task. The assistant loads your System of Context first.
  - prompt: Check this draft against our System of Context before it ships.
    note: Run on anything external, including what an agent wrote.
---

## How it works

A System of Context is the set of facts every assistant reads before it writes about your company: what you are, who you sell to, what the product does today, what you can prove, how you sound, and where your claims run ahead of the product. Without it, assistants fill gaps with plausible inventions.

This plugin installs four skills:

- **Build System of Context** (`build-system-of-context`) researches your website and internal docs, interviews you for what no website says, and saves thirteen pages as documents you own.
- **System of Context** (`system-of-context`) finds those documents and loads the right pages whenever an assistant writes or reviews something about your company.
- **Claim Check** (`system-of-context-claim-check`) audits a draft before it ships and proposes a paste-ready fix for every problem.
- **Context Refresh** (`system-of-context-refresh`) checks each page against its source, proposes a reviewed update, and keeps a log of what changed.

Pairs well with **Personalized Landing Pages**, which reads your offers, voice and proof from your System of Context.

## How to use

1. Ask the assistant to build a System of Context for your company. Have your positioning docs or brand guidelines to hand if you have them. Plan for 30 to 60 minutes, most of it a short interview.
2. Write as usual. Whenever an assistant writes or reviews something about your company, it loads the right pages first.
3. Run a claim check on anything external before it ships, including what an agent wrote.
4. Ask for a refresh once a month, or whenever a source changes.

## Mistakes to avoid

- **Skipping the interview.** The website says what you want to be true. The interview is where you record what the product doesn't do yet, which stories you can't quote, and what is off limits.
- **Editing pages by hand.** Changes made outside a refresh leave no trail. Ask for a refresh instead, so every change is reviewed and logged.
- **Only checking what humans wrote.** Agent-written drafts drift the most. Run the claim check on those too.
- **Letting it lapse.** A refresh takes ten minutes monthly. A stale page reads exactly like a current one.
