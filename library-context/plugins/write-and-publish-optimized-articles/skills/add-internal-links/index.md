---
title: Add Internal Links
summary: Add 4 to 8 links from an article draft to live, indexable pages on your own site, with your approval first.
description: A free AI skill that finds, verifies and places internal links from a new article to your existing pages, from your CMS or sitemap.
categories: [seo, content]
tags: [internal-links, seo, site-architecture, sitemap, articles]
featured: false
draft: true
output: A link approval table, then the draft with approved links in place
platforms: [claude, claude-code]
requirements:
  - name: CMS connector
    required: false
    details: Searches your published content directly. Prismic is recommended. Without a CMS connector, your sitemap is used.
  - name: Code execution
    required: false
    details: Runs the skill's scripts to read your sitemap and check each page. Without it, the assistant fetches them by hand.
examples:
  - prompt: Add internal links to this draft.
    note: Proposes links in a table and waits for your approval.
  - prompt: Which of our pages should this article link to?
    note: The same proposal, without editing the draft yet.
---

The assistant lists your live pages, from your CMS or your sitemap, matches them to the points in the article where a reader would want to go next, and proposes 4 to 8 links in a table. Pages hidden from search are flagged, not linked. Nothing is added until you approve.

## How it works

1. **Lists your live pages**, through your CMS connector or your sitemap. Never from guessed URLs.
2. **Maps reader intents**: the reader who wants more depth, the one with a follow-up question, the one who wants proof, the one ready to act.
3. **Verifies each page** loads and is indexable.
4. **Shows the approval table**: destination, anchor, section and the sentence it lives in.
5. **Places only the approved links**, on words already in the text.

## Setup

No setup is needed. Personalize once with the Personalize Article Writer skill so your website and CMS are known; connecting your CMS is recommended.

## Pitfalls

- **Forcing the count.** If the article only has room for three good links, three is right. A sentence written just to hold a link reads as an ad.
