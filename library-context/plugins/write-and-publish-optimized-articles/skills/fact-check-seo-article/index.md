---
title: Fact-check SEO Article
summary: Verify every claim and piece of advice in an article, check claims about your brand against your positioning, and get the fixes.
description: A free AI skill that fact-checks every claim and piece of advice in an article against real sources, then suggests surgical edits.
categories: [content]
tags: [fact-check, editing, content-quality, articles, brand-claims]
featured: false
draft: false
output: A fact-check report and a marked-up revision of the article
platforms: [claude, claude-code]
requirements:
  - name: Web search
    required: true
    details: Every factual check opens a source. Nothing is marked verified from memory.
  - name: Document tool connector
    required: false
    details: Notion, Google Drive or wherever your positioning lives. Without it, claims about your brand are checked against your website only, and labelled that way.
examples:
  - prompt: Fact-check this article.
    note: Paste the article or share a link. Works on anything, written by anyone.
  - prompt: Is this article accurate? Check every claim and the advice too.
    note: The same check, phrased as a question.
---

Paste or link any article. The assistant lists every claim and piece of advice in it, checks each against a source it actually opened, checks claims about your brand against your latest positioning, and hands you a report with a fix for every problem, then a revision with each change marked. It also runs on its own at the end of Write Rich Article, once you approve a draft.

## How it works

1. **Lists every checkable item.** Facts, statistics, prices, quotes, competitor claims, claims about your brand, cited sources, and every piece of advice. Not a sample.
2. **Checks the facts.** Each gets a verdict: verified, outdated, contradicted, source doesn't support it, or unverified. A link that loads isn't enough: the page has to say what the article says.
3. **Checks claims about your brand.** Latest positioning first, then your other docs, then your website and product docs. Each claim is supported, drifted, unsupported or a violation, with replacement wording.
4. **Checks the advice.** Correct and current, supported, right for the audience, complete enough to act on, safe, consistent, and specific.
5. **Reviews the writing.** Clarity, completeness, structure, tone and length, after the fact-check.
6. **Delivers.** The report, a ranked fix list, and the revised article with every change marked and traced to a finding.

## Setup

Check web search is on. To check claims about your brand against your own positioning, personalize once with the Personalize Article Writer skill and connect the tool your positioning lives in.

## Pitfalls

- **Reading only the problem rows.** Verified claims stay in the report on purpose, so you can see what was checked.
- **Expecting expert review.** In medical, legal, financial or security topics, the report recommends an expert check as well.
