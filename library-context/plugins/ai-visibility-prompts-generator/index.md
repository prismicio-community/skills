---
title: AI Visibility Prompt Generator
summary: Generate the buyer prompts to track in AI visibility tools like Peec AI and Profound, tagged and split across four buyer stages.
description: A free AI plugin that generates category-relevant, tagged buyer prompts for AI visibility tracking tools.
categories: [seo, research]
tags: [ai-visibility, prompt-tracking, geo, aeo, ai-search, peec-ai, profound]
featured: false
draft: false
output: A tagged prompt library, ready to import into your tracking tool
platforms: [claude, claude-code]
examples:
  - prompt: Generate AI visibility tracking prompts for https://example.com/product
    note: The standard run. You confirm the product category before any prompts are written.
  - prompt: Audit the prompts we track in our AI visibility tool against https://example.com/product
    note: Check an existing prompt set for product-shaped, off-category or unbalanced prompts.
---

## How it works

AI visibility tools such as Peec AI, Profound and Otterly measure how often AI assistants mention and cite your brand. They only measure the prompts you give them. If those prompts are written from your product's point of view, your numbers look better than reality.

This plugin installs one skill, **AI Visibility Prompt Generator Skill** (`ai-visibility-prompts-generator`). It writes the prompts real buyers ask, in their own words, and only prompts whose answers land in your product's category. Prompts are split equally across four buyer stages (unaware, problem-aware, solution-aware and category-aware), so you can see where you win and where you lose earlier in the journey.

See the skill's page for the full guide: how it works, setup, what it isn't, and pitfalls.

## Setup

No setup is needed. The skill uses web search for its research. If your tracking tool is connected to your assistant, the skill can offer to add the prompts there once you approve them.
