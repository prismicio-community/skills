---
title: Personalized Landing Pages Skill
summary: Research each target account, decide what to sell it, and land a personalized page in Prismic that still fits your designed layout.
description: A free AI skill that builds personalized ABM landing pages in Prismic, grounded in CRM and web research, as drafts in a release.
categories: [content]
tags: [abm, personalization, landing-pages, prismic, account-based-marketing]
featured: false
draft: true
badge: Prismic
output: Draft pages in a Prismic release, with the reasoning attached
platforms: [claude, claude-code]
requirements:
  - name: Prismic connector
    required: true
    details: Reads the base page and creates the drafts inside a release. Nothing is published.
  - name: Web search
    required: true
    details: Researches each account's business model, web estate and recent news.
  - name: Code execution
    required: true
    details: Runs the length check that keeps every field within 10% of the base page. Without it, the check is done by hand.
  - name: CRM connector
    required: false
    details: HubSpot, Salesforce or similar. Adds real engagement history. Without it, pages rest on web research alone.
  - name: Document tool connector
    required: false
    details: Holds your System of Context or saved seller settings, so the intake runs only once.
examples:
  - prompt: Build a personalized landing page for acme.com from our Prismic base page.
    note: One account, the standard run.
  - prompt: Build account pages for these ten domains from our ABM base page.
    note: A batch. The assistant proposes clusters first, then batches the approvals.
  - prompt: Personalize our webinar landing page for Northwind Freight.
    note: Works on any Prismic page, not only ABM templates.
---

## How it works

1. **Loads what you sell.** Reads your offers, claim vs reality, approved proof and voice from your System of Context, or asks a short set of questions once and saves the answers.
2. **Reads the base page as a contract.** Every section is fixed, personalizable or swappable, and every field gets a character budget.
3. **Researches each account.** CRM history first, then the web, with every fact given an ID and a source.
4. **Decides the offer.** A ranked verdict with an explicit "do not pitch" list. You approve all verdicts at once.
5. **Plans the page.** Section by section, each change backed by a fact. You approve all plans at once.
6. **Writes under constraints.** The H1 states the account's stakes, every field stays within 10% of its base length, and voice rules are enforced.
7. **Checks mechanically,** then saves every page as a draft inside one Prismic release. Nothing is published until you say so.

## Setup

Connect Prismic and turn on web search and code execution. Have a base page ready in Prismic. If you have a System of Context, keep its document tool connected.

## Pitfalls

- **Skipping the offers table.** Without a clear view of what you sell and who it isn't for, every page pitches everything and reads like mail merge.
- **Approving copy instead of plans.** Review at the plan stage. A plan takes seconds to approve; finished copy can't be meaningfully reviewed.
- **Treating "created" as "live".** Pages land unpublished in a release. Publish only after review.
