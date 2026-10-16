---
title: Write Rich Article
summary: Turn a keyword into a researched, SEO-optimized, fact-checked article with a point of view no competitor page has.
description: A free AI skill that researches a keyword, interviews you, and writes a fact-checked, SEO-optimized article from an outline you approve.
categories: [content, seo]
tags: [seo, content-writing, articles, blog-posts, serp-research, fact-check]
featured: false
draft: true
output: A finished markdown article plus a research appendix
platforms: [claude, claude-code]
requirements:
  - name: Web search
    required: true
    details: Reads the pages that rank, finds real questions on forums, and opens a source for every claim.
  - name: Code execution
    required: false
    details: Runs the skill's scripts to lint the draft, check every link and read your sitemap. Without it, the assistant does the same checks by hand.
  - name: Document tool connector
    required: false
    details: Notion, Google Drive or wherever your positioning, messaging and research live. The writer mines them for your point of view.
  - name: Call recording connector
    required: false
    details: Gong, Modjo, Chorus or similar. The exact words buyers use and the questions they ask. Without it, you can paste transcripts.
  - name: CMS connector
    required: false
    details: Checks whether you already have a page on the topic, and finds internal links. Prismic is recommended. Without it, your sitemap is used.
examples:
  - prompt: "Write an article targeting \"client onboarding checklist for agencies\"."
    note: The standard run, from keyword to finished article.
  - prompt: Draft a comparison of Tool A and Tool B for small marketing teams. Our positioning doc is attached.
    note: Comparisons and lists get balanced entries and an honest "when the other one fits better".
  - prompt: "Research the keyword \"how to reduce churn in SaaS\" and stop at the research brief."
    note: Just the research. What ranks, the gaps, the audience and real questions with links.
  - prompt: Write from this outline. Treat it as approved.
    note: Attach or paste your own outline to skip straight to drafting.
  - prompt: Approve.
    note: Ends the review loop. The full fact-check starts on its own.
---

Give the assistant a keyword. It researches what ranks and what people actually ask, mines your own docs and calls for a point of view, interviews you, and writes the article to an outline you approved. When you approve the draft, it fact-checks every claim and piece of advice before handing you the finished article, and offers to create it as a draft in your CMS.

## How it works

The article carries what no competitor page has: the gaps in what ranks, real questions people asked, the words your customers use, and your own point of view.

1. **Scopes the article.** Two or three quick questions with defaults. Say "go" to accept them.
2. **Researches.** Reads the top-ranking pages, maps what they all cover and what they miss, and collects real questions from forums with links.
3. **Mines your evidence.** Searches your connected docs, files and call recordings, and checks whether your site already has a page on this.
4. **Interviews you.** Five to eight questions, each with a proposed answer you can approve in a word. This is where the article gets a point of view.
5. **Outlines.** Every gap and every point of view placed. Nothing is drafted until you approve it.
6. **Drafts and links.** Writes the article, then proposes external and internal links in tables for your approval.
7. **Checks quality.** Lints, simplifies, removes salesy passages, compares against what ranks, and builds a quick fact-check card.
8. **Revises with you.** You go back and forth on the draft until you say "approve".
9. **Fact-checks.** Runs on its own: every claim and piece of advice gets a verdict and a source. Factual errors are fixed directly; anything you supplied is shown to you before it changes.
10. **Delivers.** The article, the research appendix and a visual plan, then offers to create an unpublished draft in your CMS.

### What you get

- **The article**, with meta title, meta description and slug at the top. It pastes or imports into any CMS.
- **A research appendix**: the gap analysis, audience profile, community questions, your internal evidence, the sourcing ledger, the link inventory and the full fact-check report.
- **A visual plan**: diagrams and charts, screenshots of public pages, and a shot list for anything behind a login.

## Setup

1. **Check web search is on.** Code execution helps too.
2. **Optional:** connect the tools your docs and call recordings live in, and your CMS. Prismic is the recommended CMS.
3. Personalize once with the Personalize Article Writer skill: "Personalize the article writer for my brand."

## Customize

The skill reads one "Article writer brand settings" document at the start of every run: your brand, website, positioning sources, voice, competitors, CMS, and whether articles end with a short section recommending your product. Personalize Article Writer builds it with you by asking, and saves it in your Notion, Google Drive, project files or the assistant's memory. Point the positioning setting at the document your team keeps current: the fact-check rereads it on every run.

## What it is not

- **Not a content planner.** It writes the article you ask for; it doesn't decide which articles to write.
- **Not autopilot.** It stops for your answers, your outline approval, your link approval and your draft approval.
- **Not a bulk writer.** One article per run, researched properly.
- **Not a replacement for expert review.** In medical, legal, financial or security topics, the fact-check flags the article for an expert as well.

## Pitfalls

- **Skipping the interview.** The article comes out as a well-written summary of what already ranks. Answer the questions, even in a word each.
- **Approving the outline without reading it.** The outline is the cheapest place to be wrong. Check the angle and the section order first.
- **Pointing positioning at a stale copy.** The fact-check corrects your claims against whatever document you named. Point it at the live one.
- **Treating the quick fact-check card as the fact-check.** The card only shows which claims have a source from research. Say "approve" when the draft is final so the full check runs.
- **Forcing internal links.** A sentence written just to hold a link reads as an ad. Accept fewer links when the article only has room for fewer.
