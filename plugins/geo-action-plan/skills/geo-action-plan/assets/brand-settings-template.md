# GEO action plan brand settings

Used by the geo-action-plan skill. Ask the assistant to "update the GEO action plan brand settings" to change anything here; it rereads this document at the start of every run. A field marked `Not set` is asked for when a run needs it.

Last updated: {{date}}

## Brand

- **Brand name:** {{brand name, or Not set}}
- **Website:** {{https://..., or Not set}}
- **Sitemap:** {{URL, or Not set (default: <website>/sitemap.xml)}}

## AI visibility tool

- **Tool:** {{e.g. Peec AI, or Not set}}
- **Default project:** {{project, report or category name, or Not set}}
- **What its connector provides:** {{which of D1–D6 from references/data-sources.md, e.g. "prompts, cited pages, fan-out queries, brands, full answers, page content"}}

## Positioning

- **Positioning sources:** {{where each source lives and how to read it, e.g. "Notion page 'Positioning & Messaging' via the Notion connector"; "Uploaded PDF 'Brand deck 2026', attach again for full detail"}}
- **What the product does:** {{two or three sentences in the source's own words}}
- **Competes in:** {{categories}}
- **Does not compete in:** {{categories that sound close to the brand but aren't it}}

## Competitors

- **Direct competitors:** {{names; mark ones suggested from the visibility tool as "(suggested)" until confirmed}}
- **Neighbouring groups that also count as competitors:** {{e.g. website builders, or Not set}}

## Site

- **CMS and how to read it:** {{CMS name, its connector if connected, which repository or space holds the live site, which to exclude; or Not set}}
- **Page families to check for siblings:** {{URL patterns, e.g. /blog/best-*, /compare/*}}

## Output

- **Where to keep plans and run state:** {{e.g. Google Drive folder "GEO plans", or Not set (default: Google Drive if connected, otherwise hand the files to the user)}}

## Category examples

Used in Step 3 of the skill, alongside its built-in examples, to show the clustering rules in this brand's category. Leave empty if the category was unclear.

- **One cluster (same two products, either order):** {{"A vs B" + "B vs A"}}
- **One cluster (same audience, same question):** {{"Best X for enterprise" + "Top X for large companies"}}
- **One cluster (same underlying problem, different formats):** {{three titles}}
- **Two clusters (different product sets):** {{"A vs B" and "A vs B vs C vs D"}}
- **Two clusters (same format, different audience):** {{"Best X for enterprise" and "Best X for agencies"}}
- **Two clusters (destinations vs reasons):** {{"X alternatives" and "Why teams are leaving X"}}
- **Good topic titles:** {{two or three headlines}}
