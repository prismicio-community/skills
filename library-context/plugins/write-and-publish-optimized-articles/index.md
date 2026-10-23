---
title: Write and Publish Optimized Articles
summary: Write SEO-optimized articles, fact-check every claim, and create them as unpublished drafts in your CMS, from one keyword.
description: A free AI plugin that researches, writes, fact-checks and SEO-optimizes articles, then creates them as drafts in your CMS. Prismic recommended.
categories: [content, seo, design]
tags: [seo, content-writing, articles, fact-check, internal-links, cms, prismic]
featured: false
draft: false
problem: Need to publish more without the quality dropping?
output: A fact-checked SEO article, then an unpublished draft in your CMS
requirements:
  - name: Web search
    required: true
    details: Reads the pages that rank, finds real questions on forums, and opens a source for every claim.
  - name: CMS connector
    required: false
    details: "Needed for creating drafts and for linking old posts to new ones. Prismic is recommended: its connector is the tested path, and every draft and every edit to a published post is staged in a release until someone publishes it. Any CMS with a connector can be set up during personalization and checked with a test draft. Without one, you get the finished article and paste-ready HTML."
  - name: Code execution
    required: false
    details: Runs the skills' scripts to lint the draft, check links, draw diagrams and convert the article for your CMS. Without it, the assistant does the same work by hand.
  - name: Document tool connector
    required: false
    details: Notion, Google Drive or wherever your positioning, messaging and research live. The writer mines them for your point of view, and the fact-check checks claims about your brand against them.
  - name: Call recording connector
    required: false
    details: Gong, Modjo, Chorus or similar. The exact words buyers use and the questions they ask. Without it, you can paste transcripts.
skills:
  - name: write-rich-article
    title: Write Rich Article
    summary: Turn a keyword into a researched, SEO-optimized, fact-checked article with a point of view no competitor page has.
    output: A finished markdown article plus a research appendix
    example: Write an article targeting "client onboarding checklist for agencies".
  - name: fact-check-seo-article
    title: Fact-check SEO Article
    summary: Verify every claim and piece of advice in an article, check claims about your brand against your positioning, and get the fixes.
    output: A fact-check report and a marked-up revision of the article
    example: Fact-check this article.
  - name: add-article-external-links
    title: Add Article External Links
    summary: Add 3 to 5 verified links to primary sources in an article draft, never to competitors, with your approval first.
    output: A link approval table, then the draft with approved links in place
    example: Add external sources to this draft.
  - name: add-article-internal-links
    title: Add Article Internal Links
    summary: Add 4 to 8 links from an article draft to live, indexable pages on your own site, with your approval first.
    output: A link approval table, then the draft with approved links in place
    example: Add internal links to this draft.
  - name: plan-article-visuals
    title: Plan Article Visuals
    summary: Decide which sections of an article earn a visual, generate the diagrams and charts, and capture or specify the screenshots.
    output: Diagram and chart files, screenshots of public pages, and a shot list
    example: What images does this article need?
  - name: create-article-cms-draft
    title: Create Article CMS Draft
    summary: Turn any finished article into an unpublished blog post draft in your CMS, mapped onto your own blog structure.
    output: An unpublished blog post draft in your CMS
    example: Create this article as a blog post draft in my CMS.
  - name: link-old-posts-to-new-article
    title: Link Old Posts to New Article
    summary: Once a new post is live, add links to it from 3 to 8 of your existing posts, using words already on the page.
    output: Staged link edits in your CMS, or an exact list of edits to make
    example: The post is live. Interlink it from our existing blog posts.
  - name: personalize-article-writer
    title: Personalize Article Writer
    summary: Set the article writer up for your brand and your CMS in one conversation. No files to edit.
    output: One brand settings document every run reads, and a verified CMS setup
    example: Personalize the article writer for my brand.
customize:
  prompt: Personalize the article writer for my brand.
  note: Run this once after installing. The assistant asks for your website, positioning, voice, competitors and CMS. Point it at a Notion page, a Google Drive doc, a URL or a PDF. It sets up your CMS with a test draft and saves your brand settings in Notion, Google Drive, your project files or its memory.
examples:
  - prompt: "Write an article targeting \"client onboarding checklist for agencies\"."
    note: The full workflow, from keyword to a fact-checked article and, if you want, a draft in your CMS.
  - prompt: Fact-check this article.
    note: Checks any article you paste or link, written by anyone.
  - prompt: Create this article as a blog post draft in my CMS.
    note: Publishing on its own, for any finished article.
---

## How it works

A full content creation workflow. This plugin takes an article from a keyword to an unpublished draft in your CMS. It writes the article, does the SEO work, fact-checks it, and creates it in your CMS as an unpublished draft for someone to review and publish. Use as much of it as you need: stop at the research, at the finished article, or go all the way to the draft.

It installs eight skills that hand work to each other:

- **Write Rich Article** (`write-rich-article`): researches what ranks and what people ask, mines your own docs and calls, interviews you, writes to an outline you approved, and revises the draft with you until you approve it.
- **Fact-check SEO Article** (`fact-check-seo-article`): verifies every claim and piece of advice against a source it opened, and checks claims about your brand against your latest positioning. Runs on its own when you approve a draft.
- **Add Article External Links** (`add-article-external-links`): 3 to 5 links to primary sources, never to competitors.
- **Add Article Internal Links** (`add-article-internal-links`): 4 to 8 links to live pages on your site.
- **Plan Article Visuals** (`plan-article-visuals`): diagrams, charts and a screenshot shot list.
- **Create Article CMS Draft** (`create-article-cms-draft`): creates the finished article as an unpublished draft in your CMS, mapped onto your blog's structure. Never publishes.
- **Link Old Posts to New Article** (`link-old-posts-to-new-article`): once a post is live and you ask, links to it from your existing posts.
- **Personalize Article Writer** (`personalize-article-writer`): sets everything up for your brand and your CMS.

## Customize

Every run reads one "Article writer brand settings" document first: your brand, website, positioning sources, voice, competitors, CMS, and whether articles end with a short section recommending your product. Point the positioning setting at the document your team keeps current, not a copy: the fact-check rereads it on every run.

## How to use

1. Give the assistant a keyword. It researches, interviews you, and stops for your answers, your outline approval, your link approval and your draft approval.
2. Say "approve" when the draft is final, so the full fact-check runs.
3. Ask for it as a draft in your CMS. Check the draft there, and publish it yourself.
4. Once the post is live, ask the assistant to link to it from your existing posts.

## What it isn't

- **Not a content planner.** It writes the article you ask for; it doesn't decide which articles to write.
- **Not autopilot.** It stops for your answers and your approvals at every step.
- **Not a bulk writer.** One article per run, researched properly.
- **Not a publisher.** It creates drafts and stops. Publishing is your decision, made in your CMS.
- **Not a replacement for expert review.** In medical, legal, financial or security topics, the fact-check flags the article for an expert as well.

## Mistakes to avoid

- **Skipping the interview.** The article comes out as a well-written summary of what already ranks. Answer the questions, even in a word each.
- **Approving the outline without reading it.** The outline is the cheapest place to be wrong. Check the angle and the section order first.
- **Pointing positioning at a stale copy.** The fact-check corrects your claims against whatever document you named. Point it at the live one.
- **Skipping the test draft.** A part mapped to the wrong field breaks every post. Check the test draft carefully.
- **Forcing internal links.** A sentence written just to hold a link reads as an ad. Accept fewer links when the article only has room for fewer.
