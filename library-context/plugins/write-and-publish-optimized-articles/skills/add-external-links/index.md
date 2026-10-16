---
title: Add External Links
summary: Add 3 to 5 verified links to primary sources in an article draft, never to competitors, with your approval first.
description: A free AI skill that picks, verifies and places outbound links to research, data and official docs in an article draft.
categories: [content, seo]
tags: [external-links, citations, sources, seo, articles]
featured: false
draft: true
output: A link approval table, then the draft with approved links in place
platforms: [claude, claude-code]
requirements:
  - name: Web search
    required: true
    details: Finds and opens each primary source before it is proposed.
  - name: Code execution
    required: false
    details: Runs the skill's script to check every URL's status and robots meta. Without it, the assistant checks each page by hand.
examples:
  - prompt: Add external sources to this draft.
    note: Proposes links in a table and waits for your approval.
  - prompt: What should this article cite?
    note: The same proposal, without editing the draft yet.
---

The assistant finds the primary sources an article's claims rest on (studies, datasets, official documentation, policy pages), opens each one, and proposes 3 to 5 links in a table: the source, the anchor text and the sentence it goes in. Nothing is added until you approve.

## How it works

1. **Finds the claims that need a source** in the draft.
2. **Goes upstream** to the original study, dataset or official page, never an aggregator or a vendor blog.
3. **Verifies each URL**: it loads, isn't a redirect to something else, and isn't hidden from search.
4. **Shows the approval table** and waits.
5. **Places only the approved links**, on words already in the sentence.

## Setup

Check web search is on. Personalize once with the Personalize Article Writer skill so your direct competitors are never proposed as sources.

## Pitfalls

- **Linking competitors as sources.** The skill refuses, and needs your competitor list to do it reliably. Confirm it during personalization.
