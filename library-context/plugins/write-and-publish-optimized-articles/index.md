---
title: Write and Publish Optimized Articles
summary: Write SEO-optimized articles, fact-check every claim, and create them as unpublished drafts in your CMS, from one keyword.
description: A free AI plugin that researches, writes, fact-checks and SEO-optimizes articles, then creates them as drafts in your CMS. Prismic recommended.
categories: [content, seo]
tags: [seo, content-writing, articles, fact-check, internal-links, cms, prismic]
featured: false
draft: false
badge: Prismic recommended
output: A fact-checked SEO article, then an unpublished draft in your CMS
platforms: [claude, claude-code]
examples:
  - prompt: Personalize the article writer for my brand.
    note: Run this once after installing. The assistant asks for what it needs, sets up your CMS with a test draft, and saves your brand settings.
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

See each skill's page for the full guide.

## Setup

1. **Check web search and code execution are on.** Both are usually on by default.
2. **Connect your CMS.** It's needed for creating drafts and for linking old posts to new ones. **Prismic is recommended**: its connector is the tested path, and every draft and every edit to a published post is staged in a release until someone publishes it. Any CMS with a connector can be set up during personalization and checked with a test draft. Without a CMS connector, you get the finished article and paste-ready HTML.
3. **Optional:** connect the tools your positioning docs, research and call recordings live in, such as Notion, Google Drive or Gong.
4. Ask the assistant to "personalize the article writer for my brand".
