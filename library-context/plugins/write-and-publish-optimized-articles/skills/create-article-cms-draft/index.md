---
title: Create Article CMS Draft
summary: Turn any finished article into an unpublished blog post draft in your CMS, mapped onto your own blog structure.
description: A free AI skill that creates a finished article as an unpublished blog draft in your CMS, with links, related posts and a CTA. Prismic recommended.
categories: [content]
tags: [cms, publishing, blog, drafts, prismic]
featured: false
draft: false
badge: Prismic recommended
output: An unpublished blog post draft in your CMS
platforms: [claude, claude-code]
requirements:
  - name: CMS connector
    required: true
    details: "Prismic is recommended: its connector is the tested path, and every draft is staged in a release until someone publishes it. Other CMSs with a connector are set up and checked with a test draft first. Without a connector, you get the article and paste-ready HTML."
  - name: Code execution
    required: false
    details: Runs the skill's converters, so links and formatting land on the right words. Without it, the assistant builds the body by hand and checks it on the test draft.
examples:
  - prompt: Create this article as a blog post draft in my CMS.
    note: Attach the article or paste it. The standard run.
  - prompt: Stage this for review. Author is Sam Lee, category is Guides.
    note: Name the author and category up front, or the assistant looks them up.
  - prompt: Add a comparison table after the second section of that draft.
    note: A follow-up edit to a draft the skill created.
---

Hand the assistant a finished article from any writer or tool. It maps the article onto your own blog post type, attaches the author, category, related posts and a call to action, and creates it as an unpublished draft in your CMS. It never publishes.

## How it works

1. **Knows your CMS.** The first time, it finds your live site or repository, reads your blog post type, maps each part of an article onto it, and creates a test draft for you to check. Personalization saves this so later runs skip it.
2. **Converts the article** into your CMS's format, with links and formatting computed from the final text.
3. **Resolves the references**: author, category, related posts from your published posts, and a checked call-to-action link.
4. **Creates the draft unpublished**: in Prismic, inside a release named after the article; elsewhere, in the CMS's draft state.
5. **Verifies and reports** where the draft is and anything your model couldn't hold. You publish from your CMS.

## Setup

Connect your CMS's connector. **Prismic is recommended**, as the tested path with every write staged in a release. For any other CMS, personalize with the Personalize Article Writer skill first: it sets up your CMS with you and checks a test draft before any real article goes in.

## What it is not

- **Not a publisher.** It creates drafts and stops. Publishing is your decision, made in your CMS.
- **Not a content modeler.** It never adds fields, blocks or content types.

## Pitfalls

- **Skipping the test draft.** A part mapped to the wrong field breaks every post. Check the test draft carefully.
- **Picking the wrong site.** The skill refuses anything named staging, sandbox, test or dev; confirm the live one.
- **Uploading placeholder images.** A stand-in that reaches a draft tends to reach production. Upload real files only.
