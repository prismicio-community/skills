# Library page content

This folder holds the text and images the Prismic website shows for each plugin and prompt, and the short descriptions of each plugin's skills. Nothing here is installed. Assistants never see it.

The folders mirror `plugins/` and `prompts/`:

```
library-context/
  taxonomy.yml                                 Allowed categories
  plugins/<plugin>/index.md                    Plugin page
  plugins/<plugin>/assets/                     Plugin page images
  prompts/<prompt>/index.md                    Prompt page
  prompts/<prompt>/assets/                     Prompt page images
```

Every plugin in `plugins/` and every prompt in `prompts/` must have a page here, and every page here must match a plugin or prompt. Pages are always named `index.md`, never `SKILL.md`.

Plugins and prompts get a card and a panel on the website. Skills have no page of their own. Each one is an item in its plugin page's `skills` list, and the website lists them in the plugin's panel.

## Page format

A page starts with fields between two `---` lines, followed by the page text in Markdown:

```markdown
---
title: Meta Descriptions
summary: Write or review meta descriptions that fit in search results.
description: A free AI plugin that writes three meta description options for any page.
categories: [seo]
tags: [meta-descriptions, metadata]
featured: false
draft: false
problem: Pages showing up in search with cut-off descriptions?
skills:
  - name: write-meta-descriptions
    title: Write Meta Descriptions
    summary: Write three meta description options for any page.
    output: Three meta descriptions with character counts
    example: Write a meta description for https://example.com/pricing
customize:
  prompt: Personalize the meta description writer for my brand.
  note: Run this once. The assistant asks for your brand voice and saves it.
examples:
  - prompt: Write a meta description for https://example.com/pricing
    note: The standard run.
---

## How it works

...

## How to use

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
| `problem` | Plugins and prompts | The reader's problem in one line, highlighted on the card, such as "Need to publish more without the quality dropping?" | 70 characters or fewer |
| `output` | No | What the user gets, shown on the card | Under 80 characters |
| `requirements` | No | Connectors and tools it needs. On a plugin, shown on the Install tab as "What it needs", and the required ones as chips on the card | A list. Each item has `name`, `required` (`true` or `false`), and optional `details` |
| `skills` | Plugins | The plugin's skills, in the order the website lists them | One item per skill folder in the plugin. See below |
| `customize` | Plugins only | A one-time setup, shown on the Customize tab | `note` (required) says what the assistant will ask for, that people can point it at Notion, Drive, a URL, or a PDF, and where the settings are saved. `prompt` (optional) is the setup prompt, such as "Personalize the article writer for my brand." |
| `examples` | Recommended | Prompts visitors can copy, shown on the How to use tab. On a prompt page, use follow-ups that change the result | A list. Each item has `prompt` and optional `note` |

Each item in `skills` describes one skill:

| Field | Required | What it's for | Rules |
| --- | --- | --- | --- |
| `name` | Yes | Which skill | The skill's folder name |
| `title` | Yes | The skill's name in the plugin's panel | Under 60 characters |
| `summary` | Yes | One sentence on what it does | Under 160 characters |
| `output` | Recommended | What the user gets | Under 80 characters |
| `example` | Recommended | A prompt that runs the skill. The website's demo plays skills that have an example and an output | Text |

Wrap a value in double quotes if it contains a colon followed by a space, or starts with `[`, `{`, `*`, `&`, `!`, `#`, or `@`.

### Sections

On plugin and prompt pages, each `## ` heading becomes a tab of the item's panel. Only these headings are allowed. Use `### ` headings to divide a section.

| Section | Required | Tab | What to write |
| --- | --- | --- | --- |
| `## How it works` | Yes | Overview | What the assistant does, in plain language |
| `## Customize` | No | Customize | How to adapt it to your brand or process. Shown after the `customize` prompt and note |
| `## How to use` | No | How to use | How to run it and when the assistant stops for your input. The `examples` follow it |
| `## What it isn't` | No | Pitfalls | What it doesn't do, and what to use instead |
| `## Mistakes to avoid` | No | Pitfalls | Common mistakes and how to avoid them |

What to connect or turn on goes in `requirements`, not in a section. Don't explain how to install the plugin. The website adds the install steps for every item automatically.

On a prompt page, don't paste the prompt itself. The website shows it, with a Copy button, from `prompts/<prompt>.md`.

Skill pages have no required sections, because the website doesn't show their text.

## Categories

`taxonomy.yml` lists the categories pages may use. To add one, add an `id` and `label` in the same pull request as the page that uses it.
