---
title: AI Visibility Prompt Generator
summary: Generate the buyer prompts to track in AI visibility tools like Peec AI and Profound, tagged and split across four buyer stages.
description: A free AI plugin that generates category-relevant, tagged buyer prompts for AI visibility tracking tools.
categories: [seo, research]
tags: [ai-visibility, prompt-tracking, geo, aeo, ai-search, peec-ai, profound]
featured: false
draft: false
problem: Not sure if ChatGPT recommends you, or what to even track?
output: A tagged prompt library, ready to import into your tracking tool
requirements:
  - name: Web search
    required: true
    details: Used for category research, buyer research, and checking which tools AI answers recommend for each prompt.
  - name: AI visibility tracking tool connector
    required: false
    details: Lets the assistant add the approved prompts and tags to your tool. Without it, you paste or upload the import-ready list yourself.
skills:
  - name: ai-visibility-prompts-generator
    title: AI Visibility Prompt Generator
    summary: Generate tagged, category-relevant buyer prompts to track in AI visibility tools, split equally across four buyer stages.
    output: 20 tagged prompts, plus an import-ready list
    example: Generate AI visibility tracking prompts for https://example.com/product
examples:
  - prompt: Generate AI visibility tracking prompts for https://example.com/product
    note: The standard run. You confirm the product category before any prompts are written.
  - prompt: Audit the prompts we track in our AI visibility tool against https://example.com/product
    note: Check an existing prompt set for product-shaped, off-category or unbalanced prompts.
---

## How it works

AI visibility tools such as Peec AI, Profound and Otterly measure how often AI assistants mention and cite your brand. They only measure the prompts you give them. If those prompts are written from your product's point of view, your numbers look better than reality.

This plugin installs one skill, **AI Visibility Prompt Generator** (`ai-visibility-prompts-generator`). It writes the prompts real buyers ask, in their own words, and only prompts whose answers land in your product's category. Prompts are split equally across four buyer stages (unaware, problem-aware, solution-aware and category-aware), so you can see where you win and where you lose earlier in the journey.

## What it isn't

- It doesn't measure your visibility. Your tracking tool does that with the prompts this skill writes.
- It doesn't write prompts for neighbouring categories, competitor comparisons or your brand name. Those inflate visibility without telling you whether buyers find you.
- It doesn't write content. Use the prompts' buyer situations to decide what to publish.

## Mistakes to avoid

- **Pushing your positioning into the prompts.** A focus area like "our AI features" decides which buyer situations get covered, not how prompts are worded. Prompts that describe your product make your visibility look better than it is.
- **Judging only the overall score.** Compare visibility by buyer stage. Brands often win category prompts and lose problem prompts, where recommendations are most contested.
- **Treating mentions as wins.** Being named in an answer isn't the same as being cited with a link. Track both.
