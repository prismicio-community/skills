# Staging edits to published posts

This skill edits posts that are already live, so the one question that matters per CMS is: can an edit to a published post be held back until a person republishes it? If yes, edits are **staged**. If no, or if you can't tell from the connector's tools and their descriptions, the outcome is **suggestions only**: an exact list of edits for the user to make.

## Prismic (recommended)

Every edit goes into a release, and nothing in a release is live until someone publishes it. That makes Prismic the safest place to run this skill.

- Create one release for the campaign, named `Interlinking: <article title>`, and write every edit into it.
- Get each post's current version immediately before editing it; a stale version id is rejected.
- Change only the targeted rich-text block or related-posts item. Everything else in the post stays exactly as it is.
- Link positions in Prismic rich text are character offsets into the block's plain text. Recompute them from the plain text after the edit; never count against the markdown.
- Repeatable items (such as related posts) are lists of name-value pairs; ask the connector's field-shapes tool for the exact form before writing.
- Publish this campaign's release only when the user explicitly says to.

## Other CMSs

These describe how these platforms commonly work. Confirm with the connector's own tools before staging anything; when unsure, use suggestions only.

| CMS | Editing published posts |
| --- | --- |
| WordPress | Usually live on save: suggestions only, unless the connector exposes a staging or revision workflow |
| Webflow | Depends on whether the connector writes to staged or live items: confirm first |
| Contentful | Usually staged: changes stay unpublished until the entry is republished |
| Sanity | Usually staged when written as a draft document; writing to the published document goes live |
| HubSpot | Usually staged in the post's draft version until pushed live |
| Storyblok | Usually staged until republished |

## Hard limits

- Never write to a published post in a CMS that would put the change live on save.
- Never publish anything except this campaign's own staged edits, and only on an explicit instruction.
- Never write to a site, space or repository named or described as staging, sandbox, test or dev.
