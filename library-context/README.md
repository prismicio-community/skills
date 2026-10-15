# Library page content

This folder holds the text and images the Prismic website shows for each plugin and skill. Nothing here is installed. Assistants never see it.

The folders mirror `plugins/`:

```
library-context/
  taxonomy.yml                                 Allowed categories and platforms
  plugins/<plugin>/index.md                    Plugin page
  plugins/<plugin>/assets/                     Plugin page images
  plugins/<plugin>/skills/<skill>/index.md     Skill page
  plugins/<plugin>/skills/<skill>/assets/      Skill page images
```

Every plugin and skill in `plugins/` must have a page here, and every page here must match a plugin or skill. Pages are always named `index.md`, never `SKILL.md`.

## Page format

A page starts with fields between two `---` lines, followed by the page text in Markdown:

```markdown
---
title: Meta Descriptions
summary: Write or review meta descriptions that fit in search results.
description: A free AI skill that writes three meta description options for any page.
categories: [seo]
tags: [meta-descriptions, metadata]
featured: false
draft: false
examples:
  - prompt: Write a meta description for https://example.com/pricing
    note: The standard run.
---

## How it works

...

## Setup

...
```

### Fields

| Field | Required | What it's for | Rules |
| --- | --- | --- | --- |
| `title` | Yes | Card and page title | Under 60 characters |
| `summary` | Yes | One sentence on the card | Under 160 characters |
| `description` | Yes | Page description for search engines and link previews | Under 160 characters |
| `categories` | Yes | Filter categories | One or more ids from `taxonomy.yml` |
| `tags` | Yes | Search keywords | Lowercase words joined by hyphens, 8 or fewer |
| `featured` | No | Highlight the item on the library page | `true` or `false` (default `false`) |
| `draft` | No | Hide the page from the website | `true` or `false` (default `false`) |
| `image` | No | Card image | A path to a file in an `assets/` folder, such as `./assets/cover.png` |
| `badge` | No | A short label on the card, such as "Any CMS" | Under 20 characters |
| `output` | No | What the user gets, shown on the card | Under 80 characters |
| `platforms` | No | Where it works | Ids from `taxonomy.yml` |
| `requirements` | No | Connectors and tools it needs | A list. Each item has `name`, `required` (`true` or `false`), and optional `details` |
| `examples` | Recommended | Prompts visitors can copy | A list. Each item has `prompt` and optional `note` |

Wrap a value in double quotes if it contains a colon followed by a space, or starts with `[`, `{`, `*`, `&`, `!`, `#`, or `@`.

### Sections

Each `## ` heading becomes a section of the page, in the order you write them.

| Section | Required | What to write |
| --- | --- | --- |
| `## How it works` | Yes | What the assistant does, in plain language |
| `## Setup` | Yes | What to connect or turn on first. If nothing, write "No setup is needed." |
| `## Customize` | No | How to adapt it to your brand or process |
| `## Pitfalls` | No | Common mistakes and how to avoid them |

You can add other sections. Don't explain how to install the plugin or skill. The website adds the install steps for every item automatically.

## Categories and platforms

`taxonomy.yml` lists the categories and platforms pages may use. To add one, add an `id` and `label` in the same pull request as the page that uses it.
