# Other CMSs

Any CMS with a connector in the assistant can receive drafts, once it has been set up and verified with the user (Step 0 of the skill, with a test draft they check in their CMS). Prismic is the recommended and tested path (`prismic.md`); everything here is about making any other CMS safe.

## The two questions that decide everything

**1. Can the connector create a post that stays unpublished?** Look for a draft status, a draft flag, a "save without publishing" option, a release or scheduled-content feature, or a separate draft document. If none exists, or you cannot tell from the connector's tools and their descriptions, the CMS gets the markdown file and the HTML body only. Never create a post in a CMS that might publish it on save.

**2. Can an edit to a published post be staged?** Some CMSs keep a separate draft version of a published post until someone republishes it; in others, editing a published post changes the live page immediately. Interlinking edits published posts, so:

- **Staged**: link-old-posts-to-new-article writes its edits into the staged version and stops, as it does in Prismic.
- **Suggestions only**: link-old-posts-to-new-article never writes. It hands the user a table of exact edits (page, existing words, the link to add) to make themselves.

When unsure, choose suggestions only. Record both answers in the settings.

## Finding your way around a connector

The connector's tool list and tool descriptions are the documentation. Before the first write:

1. List the sites, spaces, collections or blogs, and confirm the live one with the user.
2. Find the tool that describes content types or collections and read the blog post type's fields.
3. Find how the body is written (HTML string, Markdown, or a structured rich-text format) by reading the create or update tool's parameter description.
4. Find the tools for authors, categories or tags, and for searching published posts.
5. Find the draft mechanism (question 1) and how published posts are edited (question 2).

Prefer one small test write (the Step 0 test draft) over guessing a payload shape on a real article.

## Body formats

| The body field takes | Build it with |
| --- | --- |
| HTML | `scripts/md_to_html.py article.md --html` |
| Markdown | The article itself, without the front matter and H1 |
| Sections or blocks (one per H2) | `scripts/md_to_html.py article.md --sections`, one block per section |
| A structured rich-text format (JSON) | Start from the HTML converter's output and convert each element to the connector's documented shape; test on the test draft first |

If the model has no table support, tables become a short list per row. If it has no FAQ block, the FAQ stays as headings and paragraphs in the body.

## Notes on common CMSs

These describe how these platforms commonly work. Always confirm with the connector's own tools and the test draft, since connectors differ in what they expose.

| CMS | New posts unpublished? | Editing published posts |
| --- | --- | --- |
| Prismic | Yes, via releases | Staged in a release |
| WordPress | Usually yes, with a draft status | Usually live on save: suggestions only, unless the site has a staging or revision workflow the connector exposes |
| Webflow | Usually yes, as draft collection items | Depends on whether the connector writes to staged or live items: confirm in the test |
| Contentful | Usually yes, entries stay draft until published | Usually staged: changes stay unpublished until the entry is republished |
| Sanity | Usually yes, as draft documents | Usually staged when written as a draft document; writing to the published document goes live |
| HubSpot | Usually yes, as draft blog posts | Usually staged in the post's draft version until pushed live |
| Storyblok | Usually yes, as draft stories | Usually staged until republished |

## Hard limits

- Never call a publish, push-live, schedule or deploy tool.
- Never write to a site, space or repository named or described as staging, sandbox, test or dev.
- Never change the content model: no new fields, blocks or content types.
- Never write to a CMS through anything but its connector.
- If anything about the draft mechanism is unclear mid-run, stop and give the user the file and the HTML.
