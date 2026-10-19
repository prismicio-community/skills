---
title: Personalized Landing Pages
summary: Turn a list of target accounts and one base page into personalized Prismic landing pages, grounded in research and built to fit your layout.
description: A free AI plugin that builds personalized ABM landing pages in Prismic from company domains and a base page.
categories: [content]
tags: [abm, personalization, landing-pages, prismic, account-based-marketing]
featured: false
draft: false
badge: Prismic
output: Draft pages in a Prismic release, with the reasoning attached
platforms: [claude, claude-code]
examples:
  - prompt: Build a personalized landing page for acme.com from our Prismic base page.
    note: One account, the standard run.
  - prompt: Build account pages for these ten domains from our ABM base page.
    note: A batch. The assistant clusters the accounts first.
---

## How it works

This plugin installs one skill, **Personalized Landing Pages** (`personalized-landing-pages`). Give it company domains and a base page in Prismic. It researches each account, decides what to sell it and what not to, plans which sections carry that story, writes copy that fits the base page's layout, and saves every page as a draft in a Prismic release for review.

Works best with **System of Context**, which gives it your offers, voice and approved proof.

See the skill's page for the full guide.

## Setup

Connect Prismic. Turn on web search and code execution. A CRM connector adds engagement history, and a System of Context saves you answering the seller intake.
