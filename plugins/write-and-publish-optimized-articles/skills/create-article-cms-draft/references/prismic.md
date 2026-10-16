# Prismic guide

Prismic is the recommended CMS for this workflow and the tested path. Its connector exposes the content model, and every write goes into a release: nothing reaches the live site until a person publishes the release from the Prismic dashboard. Edits to published posts are staged the same way, so link-old-posts-to-new-article can be staged too.

This guide holds workflow rules only. For the exact shape of each field and slice, ask the connector: its field-shapes tool returns the current shapes for the repository, so payloads never drift from what the API accepts. Read it before the first write.

## Settings for Prismic

| Setting | Prismic value |
| --- | --- |
| CMS connector | The Prismic connector |
| Site, space or repository | The live repository, from the connector's list of repositories |
| Blog post type | From the connector's list of custom types (often `blog`, `blog_post`, `article` or `post`) |
| Body format | Prismic rich text in slices, via `scripts/md_to_prismic.py --map` |
| How drafts are kept unpublished | A release, created first; every write goes into it |
| Editing published posts | Staged (in a release) |

## The flow

1. **Step 0.** List the repositories, then the custom types; read the blog post type and each shared slice it allows, and the field shapes. Note the UID, title, SEO, author and category link fields (and the custom types they point at), and the slices for a summary, rich text, tables, FAQ, related posts and a call to action. Build the content model map in the format shown in `scripts/md_to_prismic.py`'s docstring. The converter's built-in slice and field names are placeholders; the map is what makes the output match the repository.
2. **Step 1.** `python scripts/md_to_prismic.py article.md --map content-model.json --list`, then `--part meta` and `--part <n>` for each payload. Check each payload against the field shapes the connector returned.
3. **Step 2.** Search documents of the author type and the category type (an exact search with no term and only published documents returns the complete list), and of the blog post type for related posts (published only, several phrasings).
4. **Steps 3 and 4.** Create a release, then create the document in it with the metadata and the first slices, then insert the remaining slices empty and fill them with updates (see below).
5. **Step 5.** Read the document back from the release to verify. Never publish a release that holds a blog draft.

For follow-up edits, get the current version id first, then update content in place, and insert slices before or after an existing slice key for placement.

## Failures that cost the most calls

The failures are quiet: the API accepts the payload and the document renders wrong.

**1. Inserting a slice has a payload ceiling; updating one does not.** Inserting a slice with full article content fails with an error that looks like a type problem (`expected array, received string`) but is a size limit. Insert all the empty slices you need in one call, in document order, read their assigned keys from the response, then fill each one with an update.

**2. Hyperlink and bold spans are offsets into the final plain text, not the markdown.** `**Limitation:** its [published pricing](url) starts...` renders as `Limitation: its published pricing starts...`, so the link runs from 16 to 33. Counting against the markdown shifts every span after the first. The converter computes them from the rendered text; spans must satisfy `0 <= start < end <= len(text)`, with `end` exclusive.

**3. Table cells need `direction: "ltr"`.** A cell without it validates and then renders as an empty table. The converter adds it.

**4. A stale version id is rejected outright.** Every write returns a new version id; chain them. If you lose track, list the document's versions to get the current one.

**5. Repeatable items are lists of name-value pairs, not objects.** The field-shapes tool shows the exact form. The server assigns item keys; any you pass are ignored.

## Images

Upload only real files the user supplied, through the connector's own upload. If the upload needs a URL, ask the user for one they control. Never send the user's files to a third-party file host. If there is no real file, leave the planned visual as a note in the draft; never upload a stand-in.

Check the upload result is an image with a real width and height, and give every asset a descriptive filename and alt text, since that is what makes the asset library searchable later. Place each image directly after the paragraph whose point it shows.

## Searching the repository

- An exact search with filters and no term gives a **complete** list, with a total and pagination.
- A search with a term gives a **relevance sample**. Never use it to claim completeness, and run several phrasings when picking related posts.
- Only text, rich text, image alt text and link URLs are indexed; other field values are not searchable.
- The index is eventually consistent. A document written seconds ago may not appear yet.

## Repository discipline

Work only in the live repository named in the brand settings. Repositories named or described as staging, sandbox, test or dev are not live, and content there must never be linked from a real post.

Link only to **published** documents. A related post that is still a draft renders as a broken card.

Paid-campaign landing pages are often `noindex, nofollow`. They are fine for a reader clicking through but pass no value and cannot be cited, so check the robots meta tag before using one as a destination, and flag it in the delivery notes.
