---
title: Personalized Landing Pages
summary: Turn a list of target accounts and one base page into personalized Prismic landing pages, grounded in research and built to fit your layout.
description: A free AI plugin that builds personalized ABM landing pages in Prismic from company domains and a base page.
categories: [content]
tags: [abm, personalization, landing-pages, prismic, account-based-marketing]
featured: false
draft: false
problem: Sales wants a page for every target account?
output: Draft pages in a Prismic release, with the reasoning attached
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
    details: Holds your System of Context or saved seller settings, so the seller intake runs only once.
skills:
  - name: personalized-landing-pages
    title: Personalized Landing Pages
    summary: Research each target account, decide what to sell it, and land a personalized page in Prismic that still fits your designed layout.
    output: Draft pages in a Prismic release, with the reasoning attached
    example: Build a personalized landing page for acme.com from our Prismic base page.
examples:
  - prompt: Build a personalized landing page for acme.com from our Prismic base page.
    note: One account, the standard run.
  - prompt: Build account pages for these ten domains from our ABM base page.
    note: A batch. The assistant clusters the accounts first.
---

## How it works

This plugin installs one skill, **Personalized Landing Pages** (`personalized-landing-pages`). Give it company domains and a base page in Prismic. It researches each account, decides what to sell it and what not to, plans which sections carry that story, writes copy that fits the base page's layout, and saves every page as a draft in a Prismic release for review.

Works best with **System of Context**, which gives it your offers, voice and approved proof.

## How to use

1. Have a base page ready in Prismic. Any page works, not only ABM templates.
2. Give the assistant one or more company domains and the base page.
3. Approve the offer verdicts for all accounts at once, then the page plans.
4. Review the drafts in the Prismic release, and publish them when they're ready.

## Mistakes to avoid

- **Skipping the offers table.** Without a clear view of what you sell and who it isn't for, every page pitches everything and reads like mail merge.
- **Approving copy instead of plans.** Review at the plan stage. A plan takes seconds to approve; finished copy can't be meaningfully reviewed.
- **Treating "created" as "live".** Pages land unpublished in a release. Publish only after review.
