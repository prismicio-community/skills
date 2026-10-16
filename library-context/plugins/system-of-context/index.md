---
title: System of Context
summary: Build a truth layer of your company's facts, offers, proof and voice, so AI assistants stop inventing and check drafts before they ship.
description: A free AI plugin that builds your company's System of Context, checks drafts against it, and keeps it current.
categories: [content]
tags: [context, positioning, brand-voice, messaging, fact-checking, content-governance]
featured: false
draft: true
output: A set of documents you own, plus a claim check on every draft
platforms: [claude, claude-code, chatgpt, codex]
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
- **Claim Check** (`claim-check`) audits a draft before it ships and proposes a paste-ready fix for every problem.
- **Context Refresh** (`context-refresh`) checks each page against its source, proposes a reviewed update, and keeps a log of what changed.

Pairs well with **Personalized Landing Pages**, which reads your offers, voice and proof from your System of Context.

## Setup

Connect the document tool where the System of Context should live, such as Notion, Google Drive or Confluence. Turn on web search. Then ask the assistant to build a System of Context for your company.

## Pitfalls

- **Skipping the interview.** The website says what you want to be true. The interview is where you record what the product doesn't do yet, which stories you can't quote, and what is off limits.
- **Editing pages by hand.** Changes made outside a refresh leave no trail. Ask for a refresh instead, so every change is reviewed and logged.
