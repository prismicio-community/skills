---
title: Link Old Posts to New Article
summary: Once a new post is live, add links to it from 3 to 8 of your existing posts, using words already on the page.
description: A free AI skill that adds links from your existing blog posts to a new article, staged for review where your CMS allows. Prismic recommended.
categories: [seo, content]
tags: [internal-links, interlinking, backlinks, seo, blog, prismic]
featured: false
draft: false
badge: Prismic recommended
output: Staged link edits in your CMS, or an exact list of edits to make
platforms: [claude, claude-code]
requirements:
  - name: CMS connector
    required: false
    details: Reads your posts and stages the edits. Prismic stages every edit in a release until you publish it. Without a CMS that can stage edits, you get the exact edits to make yourself.
examples:
  - prompt: The post is live. Interlink it from our existing blog posts.
    note: Proposes links in a table and waits for your approval.
  - prompt: Publish the interlinking release.
    note: The only thing the skill ever publishes, and only on these words or plain equivalents.
---

Once a new article is live, the assistant finds 3 to 8 of your existing blog posts that already talk about its topic, and proposes a link from each: by turning words already on the page into a link, or by updating a related-posts block. It never adds sentences. Nothing changes until you approve.

## How it works

1. **Runs only when you ask.** Publishing a post is never enough to start it.
2. **Finds the posts** that overlap the new article most specifically, not the most recent ones.
3. **Finds the placement** on each: existing words to link, or a related-posts slot. Posts with neither are skipped.
4. **Shows the approval table**: the post, the exact words affected, and what changes.
5. **Stages or hands over.** Where your CMS can hold edits to published posts until they're republished (Prismic does, with releases), it stages them. Otherwise it gives you the exact edits to make.

## Setup

Connect your CMS's connector. Prismic is recommended, because every edit stays in a release until you publish it.

## Pitfalls

- **Linking from a dozen posts at once.** Many pages suddenly linking one URL looks like a pattern. Keep to what the skill proposes.
- **Reading "looks good" as "publish".** The skill doesn't. Say "publish it" when you mean it.
