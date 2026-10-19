---
title: Build System of Context
summary: Research your website and docs, interview you for what isn't written down, and save your company's truth layer as documents you own.
description: A free AI skill that builds a System of Context for your company from your website, internal docs and a short interview.
categories: [content]
tags: [context, positioning, brand-voice, icp, messaging]
featured: false
draft: false
output: Thirteen pages saved in your document tool
platforms: [claude, claude-code, chatgpt, codex]
requirements:
  - name: Web search
    required: true
    details: Reads your website for positioning, product, customers and voice.
  - name: Document tool connector
    required: false
    details: Notion, Google Drive, Confluence or similar, as a source and as the place to save. Without one, you get Markdown files to add to your project.
  - name: CRM connector
    required: false
    details: Adds win/loss and ICP patterns from your closed deals.
examples:
  - prompt: Build a System of Context for our company. Our website is example.com.
    note: The standard run.
  - prompt: Build a System of Context for Acme from acme.com and the positioning docs in our Notion workspace. Save it in Notion.
    note: Better results when internal docs exist.
---

## How it works

1. **Harvests.** Reads your website, including limitation and comparison pages, and searches connected tools for positioning, ICP, battlecards and brand guidelines. Every fact is tagged with where it came from.
2. **Interviews you.** Asks only what the research didn't answer: what the product doesn't do yet, which customer stories can't be quoted, what is off limits, which internal words mean two things, and how to tell which offer fits an account.
3. **Drafts thirteen pages.** An overview with your non-negotiables, then positioning, messaging, product and offers, ICP, competitive, win/loss, evidence, ecosystem, brand voice, style guide, learnings and sources. Unknowns are marked as gaps, never guessed.
4. **Reviews the high-stakes parts with you.** The claim vs reality table, the offers table, evidence restrictions and the gaps.
5. **Saves.** As a Notion or Confluence page tree, a Google Drive folder, or Markdown files.

## Setup

Turn on web search, and connect the document tool where you want the result saved. Have your positioning docs or brand guidelines to hand if you have them.

## Pitfalls

- **Expecting a finished layer from a website alone.** The website gives you the public claims. The interview and your internal docs turn them into facts.
- **Rebuilding instead of refreshing.** Once it exists, use **Context Refresh** to add sources or close gaps.
