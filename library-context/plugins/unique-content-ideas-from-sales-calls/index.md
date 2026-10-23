---
title: Unique Content Ideas from Sales Calls
summary: Turn what customers say on your sales calls into article ideas nobody else can write, each backed by their own words.
description: A free AI plugin that mines your sales and customer call transcripts for unpublished insights and turns them into article ideas.
categories: [content, research]
tags: [content-ideas, sales-calls, call-transcripts, customer-insights, content-strategy]
featured: false
draft: false
problem: Tired of writing the same articles as everyone else?
output: A document of proven insights, customer quotes and article ideas
requirements:
  - name: Call transcripts
    required: true
    details: "Best through a call recorder connector that lists calls and returns full transcripts: Gong, Modjo, Fireflies, Fathom, Avoma, Chorus or similar. Without one, upload the transcripts (text, Word, PDF, VTT or SRT). Summaries alone aren't enough."
  - name: Web search
    required: true
    details: Tests every candidate finding against what's already published, and checks your own site for pages that already cover an idea.
  - name: Document tool connector
    required: false
    details: Notion, Google Drive or wherever your positioning docs and content calendar live. Read-only during a run, and the place your brand settings can be saved.
  - name: CMS connector
    required: false
    details: Checks your published pages directly. Without it, the assistant searches your site on the web.
skills:
  - name: unique-content-ideas-from-sales-calls
    title: Unique Content Ideas from Sales Calls
    summary: Find what customers say on your calls that nobody has published yet, prove it with their words, and turn it into article ideas.
    output: A document of proven insights, customer quotes and article ideas
    example: Personalize the unique content ideas skill for my brand.
customize:
  prompt: Personalize the unique content ideas skill for my brand.
  note: Run this once after installing. The assistant asks for your company and website, your call recorder and, optionally, your positioning. Point it at a Notion page, a Google Drive doc, a URL or a PDF. It saves your brand settings in Notion, Google Drive, your project files or its memory, and every run reads them first.
examples:
  - prompt: Find unique content ideas in this week's sales calls.
    note: The standard run.
---

## How it works

This plugin installs one skill, **Unique Content Ideas from Sales Calls** (`unique-content-ideas-from-sales-calls`). Point it at a week of recorded sales and customer calls. It reads every transcript in full, pulls out what customers actually do and decide, and checks each finding against what's already published. Only the findings nobody else has written about survive, each with the customer's own words as evidence and a set of article ideas.

## Customize

| The assistant asks for | Why it matters |
| --- | --- |
| Company and website | Every idea is checked against your site, and gets a line on how your company fits. |
| Call recorder | Where transcripts come from, or "uploaded transcripts". |
| Positioning and messaging | Optional. Used only for the company-fit line. |
| Where your content lives | Optional. Your CMS and content calendar, read-only, so ideas you've already published or planned are marked as updates. |
| Where to save your settings | Your Notion, Google Drive, project files or the assistant's memory. |

Competitors, personas, keywords and a list of your team aren't asked for. Insights come from your calls, the novelty test searches the web fresh every run, and your people are told apart from customers using your call recorder's labels and your email domain.

## How to use

1. Ask for ideas from a week of calls. The assistant says how many calls it found and how it'll read them before it starts.
2. Read the document, strongest insight first. Every insight carries the customer's words, the common view it contradicts and the novelty check.
3. If nothing survives, you get a short reply saying so, with the closest candidates. "No insights" is a normal answer.

## What it isn't

- **Not a call summarizer.** It doesn't recap calls or write CRM notes. It reads past the summary for the few things worth publishing, and ignores the rest.
- **Not a sales coaching tool.** It never scores reps or the conversation. Your team's words are set aside entirely.
- **Not a writer.** It finds insights and proposes articles. Drafting them is a separate job.
- **Not a content plan from search data.** It doesn't look at keywords or AI citations. Its raw material is what only your calls contain. Install it alongside GEO Action Plan for pages driven by what AI assistants cite.
- **Not a way to file things.** It never writes to your CRM, call recorder, CMS or content calendar. You decide what gets filed.
- **Not a source of statistics.** A quote from one customer is evidence of a behaviour, not a market figure. Evidence strength is stated on every insight so nobody over-claims.

## Mistakes to avoid

- **Running it on call summaries.** Summaries are written for CRM reporting, and the asides and exact phrasings where insights hide are the first thing they cut. Give it full transcripts.
- **Running a whole month at once.** Too many calls in one run turns close reading into skimming, and the insights get thinner without anything visibly breaking. Run one week at a time, split by call type if it's still big.
- **Quoting a line your rep said first.** A customer agreeing with your pitch is not evidence for it. Check the speaker on every quote you plan to reuse.
- **Pushing for article ideas when nothing survived.** Ideas from rejected candidates are the commodity content the skill exists to avoid. Accept "no insights" and run it on next week's calls.
- **Expecting insights from pricing and security calls.** Late-stage calls are mostly questionnaires and contract terms. Start with discovery, partner and agency calls; agencies describing their clients are some of the best evidence.
- **Publishing with a customer's name in it.** Calls are private. A named example needs that customer's consent. Pick the angles that hold up anonymised.
