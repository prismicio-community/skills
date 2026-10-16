# Article writer brand settings

Used by the write-rich-article, fact-check-article, add-external-links, add-internal-links, create-cms-draft and link-old-posts-to-new-article skills. Ask the assistant to "update the article writer brand settings" to change anything here; it rereads this document at the start of every run. A field marked `Not set` is asked for when a run needs it.

Last updated: {{date}}

## Brand

- **Brand name:** {{brand name, or Not set}}
- **Website:** {{https://..., or Not set}}
- **Sitemap:** {{URL, or Not set (default: <website>/sitemap.xml)}}
- **What the brand sells:** {{one or two plain sentences, or Not set}}

## Positioning and voice

- **Positioning and messaging sources:** {{where each source lives and how to read it, e.g. "Notion page 'Positioning & Messaging' via the Notion connector"; "Uploaded PDF 'Brand deck 2026', attach again for full detail"; or Not set (the website's product pages are used)}}
- **Brand voice and style guide:** {{where it lives, plus any banned words it lists; or Not set}}
- **Knowledge sources:** {{where internal docs, research and call recordings live and through which connector, e.g. "Google Drive folder 'Research' via the Google Drive connector; Gong via the Gong connector"; or Not set}}

## Competitors

- **Direct competitors:** {{names and domains; never linked as sources; or Not set}}

## Articles

- **Closing section:** {{Product-led articles only | Always | Never | Ask each time}} (whether articles end with a short Final thoughts section that recommends the brand)
- **Category examples:** {{three weak/strong sentence pairs from the brand's own category, same lessons as the table in write-rich-article's writing standards; or leave empty to use the built-in examples}}

## CMS

- **CMS:** {{CMS name, or Not set (recommended: Prismic)}}
- **CMS connector:** {{the connector, or Not connected}}
- **Site, space or repository:** {{the live one; never staging, sandbox, test or dev}}
- **Blog post type:** {{content type id}}
- **Author and category:** {{the author and category types or fields, and any default author}}
- **Body format:** {{Prismic rich text | HTML | Markdown | the CMS's structured format}}
- **How drafts stay unpublished:** {{e.g. "Prismic release, created first"; "draft status"}}
- **Editing published posts:** {{Staged | Suggestions only}}
- **Related-posts block:** {{field or slice id, or None}}
- **Call-to-action destination:** {{URL, or Not set}}
- **Draft naming:** Blog draft: <article title>
- **Verified with a test draft:** {{Yes, on <date> | No}}

### Content model map

Which field or block of the blog post type each part of an article goes into. `null` means the model has no matching part, so it is folded into the main body. Format: the docstring of create-cms-draft's `scripts/md_to_prismic.py`.

```json
{{the map, or {"status": "Not set"}}}
```
