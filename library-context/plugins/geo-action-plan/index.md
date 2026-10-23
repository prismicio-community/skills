---
title: GEO Action Plan
summary: Plan the pages and mentions that get you cited by AI assistants, from your AI visibility tool's data.
description: A free AI plugin that turns your AI visibility data into a ranked GEO action plan of pages to create or update and sites to get mentioned in.
categories: [seo]
tags: [geo, aeo, ai-search, ai-visibility, content-plan, peec-ai]
featured: false
draft: false
problem: Competitors get cited in AI answers and you don't?
output: An Excel workbook of ranked pages to create or update and outreach targets
requirements:
  - name: AI visibility tool connector
    required: true
    details: "The plan is built from its data: your tracked prompts and the pages AI assistants cite for them. Peec AI is recommended because its connector also provides fan-out queries. Exports and pasted data aren't accepted."
  - name: Web search
    required: true
    details: Runs one live search per fan-out query and reads the pages that rank.
  - name: Code execution
    required: true
    details: Builds and validates the Excel workbook with the skill's Python scripts.
  - name: Document tool connector
    required: false
    details: Notion, Google Drive or wherever your positioning docs live. Lets the assistant find them during personalization and keep your brand settings there.
  - name: CMS connector
    required: false
    details: Reads your existing pages directly, so update briefs compare against the live page. Without it, pages are fetched from the web.
  - name: Google Drive connector
    required: false
    details: Turns small plans into a Google Sheet. Without it, you get the Excel file.
skills:
  - name: geo-action-plan
    title: GEO Action Plan
    summary: Turn the pages AI assistants cite for your tracked prompts into a ranked plan of pages to create or update and sites to get mentioned in.
    output: An Excel workbook of ranked pages to create or update and outreach targets
    example: Personalize the GEO action plan skill for my brand.
customize:
  prompt: Personalize the GEO action plan skill for my brand.
  note: Run this once after installing. The assistant asks for your website, positioning, direct competitors and AI visibility project. Point it at a Notion page, a Google Drive doc, a URL or a PDF. It saves your brand settings in Notion, Google Drive, your project files or its memory, and every run reads them first.
examples:
  - prompt: Build a GEO action plan for the tracked prompt with the lowest visibility. Last 30 days.
    note: The standard run.
---

## How it works

This plugin installs one skill, **GEO Action Plan** (`geo-action-plan`). Point it at a prompt you track in your AI visibility tool: it clusters every page AI assistants cite and every page that ranks for their follow-up searches, checks each topic against your site, and delivers a ranked workbook of pages to create or update, plus the third-party sites and threads worth getting mentioned in.

## Customize

| The assistant asks for | Why it matters |
| --- | --- |
| AI visibility tool and project | Required. The plan is built from its data. |
| Website | Every topic is checked against your sitemap, so the plan updates pages you already have instead of creating duplicates. |
| Positioning and messaging | How the assistant learns what you sell and which topics fit you. Tell it where these live so it can reread them later. |
| Direct competitors | Their pages go on the "unlikely to mention you" list instead of the pitch list. |
| Neighbouring vendor groups | Optional. Companies outside your category that still won't mention you, such as website builders for a CMS. |
| CMS | Optional. If its connector is set up, your pages are read through it. |
| Where to keep plans and settings | Google Drive by default for plans; your choice for the settings document. |

Positioning changed, or a new competitor appeared? Ask the assistant to "update the GEO action plan brand settings" and it changes just that setting.

## How to use

1. Make sure your prompts have run in your AI visibility tool for a few weeks.
2. Ask for a plan for one tracked prompt and a time window. The assistant pauses to confirm the scope, and later the list of competitors.
3. Open the workbook. Every row traces back to the pages that justify it.

## What it isn't

- **Not a writer.** It plans and briefs pages. It doesn't draft articles; hand the briefs to a writer or a writing skill.
- **Not a visibility tracker.** Your AI visibility tool tracks how often you're mentioned. This skill reads that data once per run and turns it into work; it doesn't monitor anything between runs.
- **Not keyword research.** Topics come from what AI assistants actually cite and search for your tracked prompts, not from search volume. If a prompt isn't tracked in your tool, it isn't in the plan.
- **Not a shortlist.** It lists every distinct topic in the evidence, ranked. Deciding what to commission is your call; low-priority rows are there so nothing gets missed.
- **Not a publisher or outreach tool.** It doesn't touch your CMS, send pitches or post comments. Off-site targets come with the ask and an angle; the outreach is yours, done openly.
- **Not a way to raise your visibility score by changing prompts.** Adding or removing tracked prompts changes what's measured, not what assistants say. The plan works on pages and mentions, which is what moves the number.

## Mistakes to avoid

- **Not checking for fan-out queries.** Most AI visibility tools give you prompts and cited pages, but not the searches assistants ran, so the plan is built from fewer ranking pages. Check whether your tool's connector exposes fan-out or search queries; if it doesn't, expect a thinner search layer, which the plan flags.
- **Using a 7-day window.** Too few answers to trust the citation counts. Use 30 days, and keep the same window across runs so plans compare.
- **Starting with the whole project.** Hundreds of follow-up queries in one run means shallow coverage and a workbook nobody reads. Run one prompt at a time, starting with the one you most need to win.
- **Leaving the competitor list to the assistant.** A competitor misread as an independent publisher costs a whole outreach cycle. Check the list carefully when asked, and add the neighbouring vendor groups it missed.
- **Skipping personalization.** The skill still runs, but it asks for your product on every run and teaches itself with examples from another category. Personalize once; every run after is shorter.
- **Deleting low-fit rows.** Some adjacent topics are where a mention still sells. Filter on the FIT label in the Content Plan tab instead of removing rows.
- **Treating every row as a new page.** Creating a page you already have splits your own traffic. Make sure your sitemap URL is right; update rows are usually the cheapest wins in the plan.
- **Filling briefs with numbers nobody gave you.** The skill asks for your data and leaves the gap visible on purpose. Supply the figure, or plan the version that doesn't need it.
- **Posting in threads without saying who you are.** Communities spot undisclosed promotion fast, and Reddit carries a lot of weight in AI answers. Answer the question first and disclose where you work.
