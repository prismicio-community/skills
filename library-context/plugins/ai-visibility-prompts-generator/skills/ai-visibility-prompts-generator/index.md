---
title: AI Visibility Prompt Generator Skill
summary: Generate tagged, category-relevant buyer prompts to track in AI visibility tools, split equally across four buyer stages.
description: A free AI skill that writes the buyer prompts to track in Peec AI, Profound and other AI visibility tools.
categories: [seo, research]
tags: [ai-visibility, prompt-tracking, geo, aeo, ai-search, buyer-research]
featured: false
draft: false
output: 20 tagged prompts, plus an import-ready list
platforms: [claude, claude-code]
requirements:
  - name: Web search
    required: true
    details: Used for category research, buyer research, and checking which tools AI answers recommend for each prompt.
  - name: AI visibility tracking tool connector
    required: false
    details: Lets the skill add the approved prompts and tags to your tool. Without it, you paste or upload the import-ready list yourself.
examples:
  - prompt: Generate AI visibility tracking prompts for https://example.com/product
    note: The standard run. The skill confirms your product category with you first.
  - prompt: Generate 40 tracking prompts for https://example.com/product, focused on teams moving off spreadsheets
    note: A bigger library, focused on one buyer situation. The split across stages stays equal.
  - prompt: Audit the prompts we track in our AI visibility tool against https://example.com/product
    note: Find product-shaped, off-category or unbalanced prompts in a set you already track.
---

## How it works

1. **Scope.** The assistant reads your product page once, to agree the product's category with you and to list every phrase from your positioning. Nothing on that list may appear in a prompt.
2. **Research.** It researches the category and the incumbents AI assistants usually recommend. Then it collects how buyers describe their problems on forums, communities and review sites, not on vendor websites.
3. **Draft.** It writes at least 10 prompts per buyer stage, each traced to a real buyer situation and tagged with the stage plus persona, job, trigger or context.
4. **Check.** It searches every prompt and keeps only the ones whose answers name tools in your category. Prompts answered by a neighbouring category are dropped.
5. **Deliver.** You get 20 prompts by default, five per stage, in a table with tags, evidence and tracking importance. You also get an import-ready list and notes on how to read the results.

## Setup

No setup is needed. To let the skill add prompts to your tracking tool directly, connect that tool to your assistant first.

## What it is not

- It doesn't measure your visibility. Your tracking tool does that with the prompts this skill writes.
- It doesn't write prompts for neighbouring categories, competitor comparisons or your brand name. Those inflate visibility without telling you whether buyers find you.
- It doesn't write content. Use the prompts' buyer situations to decide what to publish.

## Pitfalls

- **Pushing your positioning into the prompts.** A focus area like "our AI features" decides which buyer situations get covered, not how prompts are worded. Prompts that describe your product make your visibility look better than it is.
- **Judging only the overall score.** Compare visibility by buyer stage. Brands often win category prompts and lose problem prompts, where recommendations are most contested.
- **Treating mentions as wins.** Being named in an answer isn't the same as being cited with a link. Track both.
