---
title: Unique Content Ideas from Sales Calls Skill
summary: Find what customers say on your calls that nobody has published yet, prove it with their words, and turn it into article ideas.
description: A free AI skill that reads your sales call transcripts in full, tests every finding for novelty, and proposes article ideas only you can write.
categories: [content, research]
tags: [content-ideas, sales-calls, call-transcripts, customer-insights, content-strategy]
featured: false
draft: false
badge: Any call recorder
output: A document of proven insights, customer quotes and article ideas
platforms: [claude, claude-code]
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
examples:
  - prompt: Personalize the unique content ideas skill for my brand.
    note: Run this once after installing. The assistant asks for a few details and saves your brand settings.
  - prompt: Find unique content ideas in this week's sales calls.
    note: The standard run. The assistant lists what it found and how it'll read them before it starts.
  - prompt: Find unique content ideas in last week's discovery calls only.
    note: Filter by call type. The assistant classifies each call and shows you the list.
  - prompt: Read the latest discovery call and tell me if there's anything in it we could write about.
    note: A single call. "No insights" is a normal answer.
  - prompt: Here are three call transcripts. Find unique content ideas in them.
    note: No call recorder connected? Attach the files. If a transcript only shows first names, the assistant asks once which speakers are yours.
  - prompt: A customer told us clinics pilot new tools at their worst location first. Is that a new angle or is it already out there?
    note: Test one idea you already have, without a full run.
  - prompt: Update the unique content ideas brand settings. We moved to Gong.
    note: Changes one setting without redoing the rest.
---

Point the assistant at a week of recorded sales and customer calls. It reads every transcript in full, one call at a time, pulls out what customers actually do and decide, and tests each finding against what's already published. Only the findings nobody else has written about survive, each with the customer's own words as evidence and a set of article ideas that only you can write.

## How it works

Your company records conversations no competitor can hear. Most of what customers say on them is already in every vendor's "top challenges" post, so the skill applies a hard bar: a finding only counts if it contradicts, or is missing from, the public conversation.

1. **Picks the calls.** Lists the calls in your window and drops the ones that can't carry an insight: internal syncs, no recording, a few minutes long.
2. **Checks the workload.** Says how many calls it found and how it'll read them. It pauses and proposes a split if the run is more than a week, more than about 25 calls, or a mix that would blur audiences.
3. **Reads every transcript in full.** One reader per call, never the summary. It notes what customers do today, what they refuse to touch, who really decides, and the words they use. Quotes are kept verbatim, in the original language, with timestamps. Your own team's words are never evidence.
4. **Judges in one place.** Every candidate gets the same bar: what's the common view, and does this call show something different?
5. **Tests novelty.** A few web searches per candidate, with a verdict: not found, partly discussed, or common knowledge (rejected). Most candidates fail here, and that's the point.
6. **Proposes articles.** Two to four article ideas per surviving insight, each with a real publishable title, format, angle, reader, and one line on how your company fits.
7. **Checks your content.** Marks each idea as new or as an update to a page you already have.

### What you get

One document, strongest insight first. Every insight carries the evidence behind it:

| Field | Example |
| --- | --- |
| Insight | Multi-site clinic groups trial new software at their hardest location first, not their flagship. |
| Evidence | "We always try new stuff at Riverside first. If it survives Riverside, it survives anywhere." (Practice manager, Account A, 14:32) |
| Common view | Pilots run at the head office or the best-run site, where adoption is easiest. |
| Novelty check | Not found in search. |
| Strength | Described workflow, seen independently in two accounts. |
| Article idea | "Why Clinic Groups Pilot New Software at Their Hardest Location First" · Research · New |

The document also lists every call read, every rejected candidate with the reason it failed, which ideas name a customer and how to anonymise them, and the per-call notes and searches behind it all. If nothing survives, you get a short reply saying so, with the closest candidates and why they fell short.

## Setup

1. **Connect your call recorder, or have transcripts ready.** Any recorder whose connector lists calls and returns full transcripts works. Without one, upload the transcripts instead.
2. **Check web search is on.** It's usually on by default.
3. **Optional:** connect the tool your positioning docs and content calendar live in, and your CMS.

## Customize

Personalize the skill once, by asking. You never edit a file.

1. **Ask:** "Personalize the unique content ideas skill for my brand." The assistant replies with the short list of what it needs.
2. **Give your company name and website.** The assistant reads your sitemap so it can tell whether an idea updates a page you have or needs a new one.
3. **Say where your calls come from.** Your call recorder, or uploaded transcripts.
4. **Share your positioning, if you have it.** Any form works: a link, a Notion page, a Google Drive doc, a PDF or pasted text. It's used only for the one line on how your company fits each idea, never to decide what counts as an insight.
5. **Check the draft.** The assistant also researches the complaints buyers in your category make all the time and adds them to the reject list, so they're never reported as insights.
6. **Choose where your settings live.** The assistant saves one short "Unique content ideas brand settings" document in your Notion, your Google Drive, your project files or the assistant's memory. Every run reads it first, and it stays put when the skill updates.

| The assistant asks for | Why it matters |
| --- | --- |
| Company and website | Every idea is checked against your site, and gets a line on how your company fits. |
| Call recorder | Where transcripts come from, or "uploaded transcripts". |
| Positioning and messaging | Optional. Used only for the company-fit line. |
| Where your content lives | Optional. Your CMS and content calendar, read-only, so ideas you've already published or planned are marked as updates. |
| Where to save your settings | Your Notion, Google Drive, project files or the assistant's memory. |

Competitors, personas, keywords and a list of your team aren't asked for. Insights come from your calls, the novelty test searches the web fresh every run, and your people are told apart from customers using your call recorder's labels and your email domain.

## What it is not

- **Not a call summarizer.** It doesn't recap calls or write CRM notes. It reads past the summary for the few things worth publishing, and ignores the rest.
- **Not a sales coaching tool.** It never scores reps or the conversation. Your team's words are set aside entirely.
- **Not a writer.** It finds insights and proposes articles. Drafting them is a separate job.
- **Not a content plan from search data.** It doesn't look at keywords or AI citations. Its raw material is what only your calls contain. Install it alongside GEO Action Plan for pages driven by what AI assistants cite.
- **Not a way to file things.** It never writes to your CRM, call recorder, CMS or content calendar. You decide what gets filed.
- **Not a source of statistics.** A quote from one customer is evidence of a behaviour, not a market figure. Evidence strength is stated on every insight so nobody over-claims.

## Pitfalls

- **Running it on call summaries.** Summaries are written for CRM reporting, and the asides and exact phrasings where insights hide are the first thing they cut. Give it full transcripts.
- **Running a whole month at once.** Too many calls in one run turns close reading into skimming, and the insights get thinner without anything visibly breaking. Run one week at a time, split by call type if it's still big.
- **Quoting a line your rep said first.** A customer agreeing with your pitch is not evidence for it. Check the speaker on every quote you plan to reuse.
- **Pushing for article ideas when nothing survived.** Ideas from rejected candidates are the commodity content the skill exists to avoid. Accept "no insights" and run it on next week's calls.
- **Expecting insights from pricing and security calls.** Late-stage calls are mostly questionnaires and contract terms. Start with discovery, partner and agency calls; agencies describing their clients are some of the best evidence.
- **Publishing with a customer's name in it.** Calls are private. A named example needs that customer's consent. Pick the angles that hold up anonymised.
