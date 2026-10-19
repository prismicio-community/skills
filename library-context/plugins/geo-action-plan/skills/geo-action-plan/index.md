---
title: GEO Action Plan Skill
summary: Turn the pages AI assistants cite for your tracked prompts into a ranked plan of pages to create or update and sites to get mentioned in.
description: A free AI skill that builds a GEO and AI-search action plan from your AI visibility tool's data, ranked and checked against your own site.
categories: [seo]
tags: [geo, aeo, ai-search, ai-visibility, content-plan, peec-ai]
featured: false
draft: false
badge: Peec AI recommended
output: An Excel workbook of ranked pages to create or update and outreach targets
platforms: [claude, claude-code]
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
examples:
  - prompt: Personalize the GEO action plan skill for my brand.
    note: Run this once after installing. The assistant asks for what it needs and saves your brand settings.
  - prompt: "Build a GEO action plan for the prompt \"best scheduling software for small clinics\". Last 30 days."
    note: The standard run, one tracked prompt and one time window.
  - prompt: Which tracked prompt has the lowest visibility for us? Build the action plan for that one.
    note: Let the assistant pick your weakest prompt. On a tie it shows you the options.
  - prompt: "Run a GEO action plan for every prompt tagged \"comparisons\", last 30 days."
    note: A topic or tag scope, if your tool groups prompts this way. The assistant counts the queries first and asks you to narrow it if there are too many.
  - prompt: Expand the briefs for rows 9 to 14 into full briefs, reading the top pages for each.
    note: A follow-up in the same chat. Lower-priority rows start with short briefs; promote the ones you want to commission.
  - prompt: Update the GEO action plan brand settings. We now compete with Rivalsoft.
    note: Changes one setting without redoing the rest.
---

Point the assistant at a prompt you track in your AI visibility tool. It pulls every page AI assistants cite for that prompt, runs a live search for every follow-up query the assistants make, groups those pages by what they say, and hands you a ranked list of pages to create or update on your site, plus the third-party pages and threads worth getting mentioned in.

## How it works

The plan rests on what AI assistants and search engines already retrieve. Every page that gets cited or ranks for your prompt is evidence of content they want, and the plan gives you your own version of each.

1. **Checks your data.** Confirms your AI visibility tool's connector has the data the plan needs and tells you what's missing.
2. **Confirms the scope.** Pauses to confirm the project, the prompt and the time window, and checks your product details still hold.
3. **Pulls the citation layer.** Every page AI assistants cite for the prompt, plus a few full AI answers to see how they're built.
4. **Builds the search layer.** One live search for every follow-up query the assistants ran.
5. **Clusters the pages.** Groups pages that say the same thing, whatever their format, and writes one real headline per group.
6. **Checks your site.** Maps every topic to your sitemap: update the page you already have, or create one. It also checks crawler access and whether your content is in the delivered HTML.
7. **Ranks every topic.** P0 to P2, by evidence, prompt match, product fit, winnability and readiness. Low-fit topics drop down the list; nothing is cut.
8. **Finds off-site targets.** Pauses to confirm which companies count as competitors, then sorts the third-party sites by who is likely to mention you.
9. **Delivers the workbook.** Builds and validates it, then summarizes the numbers and the two to four findings that matter.

### What you get

One Excel workbook with 11 tabs. Every topic is a row, and every row traces back to the pages that justify it:

| Field | Example |
| --- | --- |
| Priority, action, type | P0 · Update · Comparison |
| Title | Acme vs Rivalsoft: Which Is Better for Small Clinics? |
| Title evidence | "Rivalsoft vs Acme: Which Scheduling Tool?" (cited page title) |
| Existing page | acme.com/compare/rivalsoft |
| Sources to beat | rivalsoft.com/compare/acme, 18 citations (citation layer); g2.com/compare/…, 5 queries (search layer) |
| Why this page | FIT: High. Four pages in this group; none covers no-show rates. |
| Brief | Keep the feature table. Add a "Reminders and no-shows" section. Add an honest "when Rivalsoft is the better fit" section. |
| Depends on | No-show data across customers. Not pulled yet; flagged. |

The Topic Clusters tab lists every page behind every row, and the Cited Sources tab lists every URL the assistants cited, so your team can work from the raw evidence too.

## Setup

1. **Connect your AI visibility tool.** Its connector must provide your tracked prompts and the pages AI assistants cite for them. Fan-out queries, the searches assistants run while answering, make the plan much stronger; without them the assistant searches your tracked prompts instead and says the search layer is thinner. **Peec AI is recommended**: its connector provides everything the plan uses, including fan-out queries. With any other tool, the assistant checks its connector before every run and tells you what's missing. Make sure your prompts have run for a few weeks.
2. **Check web search and code execution are on.** Both are usually on by default.
3. **Optional:** connect your CMS, the tool your positioning docs live in, and Google Drive.

## Customize

Personalize the skill once, by asking. You never edit a file.

1. **Ask:** "Personalize the GEO action plan skill for my brand." The assistant replies with one list of what it needs and what each detail is for.
2. **Share what you have, wherever it lives.** A link, a Notion page, a Google Drive doc, a PDF or deck, or pasted text. Any positioning material helps: messaging frameworks, ICP or persona docs, brand guidelines, sales decks, competitor battlecards. If you don't have something, say so; the skill asks for it later only if a run needs it.
3. **Or let the assistant find it.** If your documents live in Notion, Google Drive or a similar tool, connect it. The assistant offers to search it for positioning, messaging and competitor docs, shows you what it found, and reads only the ones you pick.
4. **Check the draft.** The assistant works out what it can on its own (what you sell, the categories you compete in and don't, your sitemap, the page families on your site, suggested competitors from your visibility tool) and shows you the full set to correct.
5. **Choose where your settings live.** The assistant saves one short "GEO action plan brand settings" document in your Notion, your Google Drive, your project files or the assistant's memory. Every run reads it first, and it stays put when the skill updates.

The assistant asks for:

| Detail | Why it matters |
| --- | --- |
| AI visibility tool and project | Required. The plan is built from its data. |
| Website | Every topic is checked against your sitemap, so the plan updates pages you already have instead of creating duplicates. |
| Positioning and messaging | How the assistant learns what you sell and which topics fit you. Tell it where these live so it can reread them later. |
| Direct competitors | Their pages go on the "unlikely to mention you" list instead of the pitch list. |
| Neighbouring vendor groups | Optional. Companies outside your category that still won't mention you, such as website builders for a CMS. |
| CMS | Optional. If its connector is set up, your pages are read through it. |
| Where to keep plans and settings | Google Drive by default for plans; your choice for the settings document. |

Positioning changed, or a new competitor appeared? Ask the assistant to "update the GEO action plan brand settings" and it changes just that setting.

## What it is not

- **Not a writer.** It plans and briefs pages. It doesn't draft articles; hand the briefs to a writer or a writing skill.
- **Not a visibility tracker.** Your AI visibility tool tracks how often you're mentioned. This skill reads that data once per run and turns it into work; it doesn't monitor anything between runs.
- **Not keyword research.** Topics come from what AI assistants actually cite and search for your tracked prompts, not from search volume. If a prompt isn't tracked in your tool, it isn't in the plan.
- **Not a shortlist.** It lists every distinct topic in the evidence, ranked. Deciding what to commission is your call; low-priority rows are there so nothing gets missed.
- **Not a publisher or outreach tool.** It doesn't touch your CMS, send pitches or post comments. Off-site targets come with the ask and an angle; the outreach is yours, done openly.
- **Not a way to raise your visibility score by changing prompts.** Adding or removing tracked prompts changes what's measured, not what assistants say. The plan works on pages and mentions, which is what moves the number.

## Pitfalls

- **Not checking for fan-out queries.** Most AI visibility tools give you prompts and cited pages, but not the searches assistants ran, so the plan is built from fewer ranking pages. Check whether your tool's connector exposes fan-out or search queries; if it doesn't, expect a thinner search layer, which the plan flags.
- **Using a 7-day window.** Too few answers to trust the citation counts. Use 30 days, and keep the same window across runs so plans compare.
- **Starting with the whole project.** Hundreds of follow-up queries in one run means shallow coverage and a workbook nobody reads. Run one prompt at a time, starting with the one you most need to win.
- **Leaving the competitor list to the assistant.** A competitor misread as an independent publisher costs a whole outreach cycle. Check the list carefully when asked, and add the neighbouring vendor groups it missed.
- **Skipping personalization.** The skill still runs, but it asks for your product on every run and teaches itself with examples from another category. Personalize once; every run after is shorter.
- **Deleting low-fit rows.** Some adjacent topics are where a mention still sells. Filter on the FIT label in the Content Plan tab instead of removing rows.
- **Treating every row as a new page.** Creating a page you already have splits your own traffic. Make sure your sitemap URL is right; update rows are usually the cheapest wins in the plan.
- **Filling briefs with numbers nobody gave you.** The skill asks for your data and leaves the gap visible on purpose. Supply the figure, or plan the version that doesn't need it.
- **Posting in threads without saying who you are.** Communities spot undisclosed promotion fast, and Reddit carries a lot of weight in AI answers. Answer the question first and disclose where you work.
