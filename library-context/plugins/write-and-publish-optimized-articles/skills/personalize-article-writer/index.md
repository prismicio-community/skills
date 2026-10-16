---
title: Personalize Article Writer
summary: Set the article writer up for your brand and your CMS in one conversation. No files to edit.
description: A free AI skill that collects your positioning, voice, competitors and CMS setup, tests a draft, and saves your article writer brand settings.
categories: [content]
tags: [personalization, brand-settings, setup, cms, prismic]
featured: false
draft: true
output: One brand settings document every run reads, and a verified CMS setup
platforms: [claude, claude-code]
requirements:
  - name: Document tool connector
    required: false
    details: Notion, Google Drive or wherever your positioning lives. Lets the assistant find your docs and save your settings there.
  - name: CMS connector
    required: false
    details: Lets the assistant set up drafts in your CMS and check a test draft with you. Prismic is recommended.
examples:
  - prompt: Personalize the article writer for my brand.
    note: Run this once after installing.
  - prompt: Update the article writer brand settings. We now compete with Rivalsoft.
    note: Changes one setting without redoing the rest.
---

Ask the assistant to personalize the article writer. It tells you what it needs and why, takes it from wherever it lives, sets up your CMS with you, and saves one "Article writer brand settings" document that every article skill reads first.

## How it works

1. **Asks once**, in one message, for your brand, website, positioning material, voice guide, competitors, CMS and call-to-action page, and where to save your settings.
2. **Takes it from wherever it lives**: a link, a Notion page, a Google Drive doc, a PDF or deck, or pasted text. With a document tool connected, it offers to search it for you.
3. **Sets up your CMS together**: finds your live site, reads your blog structure, maps an article onto it, and creates a test draft for you to check.
4. **Shows you the draft settings** to correct.
5. **Saves the document** in your Notion, Google Drive, project files or the assistant's memory.

## Setup

No setup is needed. Connecting your document tool and your CMS first makes it faster. Prismic is the recommended CMS.

## Customize

The positioning setting records where your positioning lives, not a copy, so every run reads the current version. Point it at the document your team keeps up to date.
