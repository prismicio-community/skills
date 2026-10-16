# Prismic guide

Prismic is the recommended CMS for this workflow and the tested path. Its connector (the Prismic MCP) exposes the content model, and every write goes into a release: nothing reaches the live site until a person publishes the release from the Prismic dashboard. Edits to published posts are staged the same way, so link-old-posts-to-new-article can be staged too.

## Settings for Prismic

| Setting | Prismic value |
| --- | --- |
| CMS connector | Prismic MCP |
| Site, space or repository | The live repository, from `list_repositories` |
| Blog post type | From `list_custom_types` (often `blog`, `blog_post`, `article` or `post`) |
| Body format | Prismic rich text in slices, via `scripts/md_to_prismic.py --map` |
| How drafts are kept unpublished | A release, created first; every write goes into it |
| Editing live posts | Staged (in a release) |

## The flow

1. **Step 0.** `list_repositories`, then `list_custom_types`, `get_custom_type` for the blog post type, and `get_shared_slice` for each slice it allows. Note the UID, title, SEO, author and category link fields (and the custom types they point at), and the slices for a TL;DR or summary, rich text, tables, FAQ, related posts and a call to action. Build the Content model map in the format of the example in `scripts/md_to_prismic.py`'s docstring.
2. **Step 1.** `python scripts/md_to_prismic.py article.md --map content-model.json --list`, then `--part meta` and `--part <n>` for each payload.
3. **Step 2.** `search_documents` with the author type, the category type (`searchMode: "exact"`, `statuses: ["published"]` returns the complete list), and the blog post type for related posts (`statuses: ["published"]`, several phrasings).
4. **Step 3 and 4.** `create_release`, then `create_document` in it with the metadata and the first slices, then insert the remaining slices empty and fill them with `updates` (see below).
5. **Step 5.** `get_document` with the `releaseId` to verify. Never call `publish_release` for a blog draft.

For follow-up edits, get the current version id first, then use `updates` for content changes and `inserts` with `beforeKey` or `afterKey` for placement. `deletes` removes a slice by its path.

# Editor shape and failure modes

Everything here was learned by hitting it. The failures are quiet: the API accepts the payload and the document renders wrong.

## The failures that cost the most calls

**1. `inserts` has a payload ceiling. `updates` does not.**

Inserting a slice with full article content returns `expected array, received string` on the `inserts` parameter. It is a size limit surfacing as a type error, so it looks like a schema problem and is not.

The pattern that works every time:

1. Insert all the empty slices you need in one call, in document order.
2. Read the returned `containers` map for their assigned keys.
3. Fill each one with `updates`, keyed on `slices[<sliceKey>].<field>`.

**2. Hyperlink and strong spans are offsets into the final plain text.**

Not into the markdown. `**Limitation:** its [published pricing](url) starts...` renders as `Limitation: its published pricing starts...`, so the link runs 16 to 33, not wherever it sits in the source. Counting against markdown shifts every span after the first. Use `scripts/md_to_prismic.py`, which computes them from the rendered text.

Spans must satisfy `0 <= start < end <= len(text)`, and `end` is exclusive.

**3. Table cells need `direction: "ltr"`.**

A cell without it validates and then renders as an empty table. Every rich-text block in every cell needs it. The converter adds it.

**4. Booleans are `BooleanContent`, not `FieldContent`.**

```json
{"__TYPE__": "BooleanContent", "value": true}
```

`{"__TYPE__": "FieldContent", "type": "Boolean", ...}` fails validation with `No matching discriminator`.

**5. A stale `baseVersionId` is rejected outright.**

Every write returns a new `versionId`. Chain them. If you lose track, `list_document_versions` gives the current one. The `version.id` from a `get_document` on a release can also go stale between calls.

## Field shapes

```json
Text        {"__TYPE__": "FieldContent", "type": "Text", "value": "..."}
Date        {"__TYPE__": "FieldContent", "type": "Date", "value": "2026-08-05"}
Select      {"__TYPE__": "FieldContent", "type": "Select", "value": "purple"}
Boolean     {"__TYPE__": "BooleanContent", "value": true}
UID         {"__TYPE__": "UIDContent", "value": "my-slug"}
RichText    {"__TYPE__": "StructuredTextContent", "value": [ <blocks> ]}
Doc link    {"__TYPE__": "LinkContent", "value": {"__TYPE__": "DocumentLink", "id": "..."}}
Web link    {"__TYPE__": "LinkContent", "value": {"__TYPE__": "ExternalLink", "url": "...", "target": "_blank"}}
```

Omit `key` on links when creating; the server generates it. Keep it when updating.

Rich-text blocks: `paragraph`, `heading1` to `heading6`, `preformatted`, `list-item` (bullet), `o-list-item` (numbered), `image`, `embed`. Each carries `content: {text, spans}` and `direction: "ltr"`.

## The reference blog model

The converter's default names come from this model. Your repository's blog type will differ: Step 0 of the skill maps the article onto your own type, and `--map` renames slices and fields to match. Use this section as a worked example of what a full blog model can hold.

Fields: `title`, `uid`, `image`, `author`, `additional_author`, `category`, `date`, `updated_date`, `learning_objective`, `card_description`, `slices`, plus `meta_title`, `meta_description`, `social_image`, and the guide fields.

Slice choices: `tldr`, `text_content`, `comparison_table`, `faq`, `callout`, `quote`, `code_snippet`, `blog_call_to_action`, `related_posts`, `form_link`, `video`, `quiz`.

### Slice notes

**`comparison_table`** has two variations. `blog` is capped at three categories with boolean or text values per row. `multicolumn` takes a real Table field and handles any column count. **Use `multicolumn` for anything wider than three columns**, which is most tool comparisons. `highlight_first_column` is worth setting.

**`faq`** takes repeatable items of `question` (heading3) and `answer` (multi rich text). Putting FAQs as headings inside a `text_content` slice loses the accordion and the structured-data eligibility.

**`tldr`** takes a `title` (heading2) and `content` (rich text, bullets).

**`related_posts`** takes a `title` and repeatable `related` document links restricted to the `blog` type.

**`blog_call_to_action`** has `default` and `animated`. Fields: `title`, `description`, `color` (purple, blue, orange, pink, green, dark), `image`, `offset_image`, `cta_link`, `cta_label`, `cta_type` (link, form, mail).

## Group item shape

Repeatable items are tuple lists, not objects:

```json
{"__TYPE__": "GroupItemContent",
 "value": [["question", <rich text>], ["answer", <rich text>]]}
```

An object here fails. The server assigns the item key; any key you pass is ignored.

## Uploading images

`upload_asset` fetches a public URL server-side, so local files must be hosted first. Only do this for images that are fine to sit on a public URL for a day, and ask the user before using a third-party host. Two lessons from doing this:

- **tmpfiles.org serves an HTML wrapper at its /dl/ URLs, not the raw file.** Prismic will ingest a 3KB HTML document that reports `kind: "document"` instead of an image. **litterbox.catbox.moe works**: `curl -F "reqtype=fileupload" -F "time=24h" -F "fileToUpload=@shot.png" https://litterbox.catbox.moe/resources/internals/api.php` returns a direct file URL, valid for 24 hours, which is plenty since Prismic copies the file on upload.
- **Check the response.** A correct upload returns `kind: "image"` with real `width` and `height`. A missing width/height or a tiny `size` means the host served something other than the image; re-host and retry.

Give every asset a descriptive filename and alt text at upload time, since that is what makes the asset library searchable later. Include the concrete numbers in alt text where the image is pricing evidence.

Place images inside rich text as an `image` block: `{"type": "image", "direction": "ltr", "data": {"origin": {"id", "url", "width", "height"}, "url", "width", "height", "alt", "edit": {"background": "transparent", "crop": {"x": 0, "y": 0}, "zoom": 1}}}`. Put each screenshot directly after the paragraph whose claim it evidences, not gathered at the end.

## Searching the repository

- `searchMode: "exact"` with filters and an empty term gives a **complete** list, with `total` and pagination.
- `searchMode: "semantic"` (the default when `term` is set) gives a **relevance sample**. Never use it to claim completeness, and run several phrasings when picking related posts.
- Field values are not searchable. Only text, rich text, image alt text and link URLs are indexed.
- The index is eventually consistent. A document written seconds ago may not appear yet.

## Repository discipline

Work only in the live repository named in the skill's settings. Repositories named or described as staging, sandbox, test or dev are not live, and content there must never be linked from a real post.

Link only to **published** documents. A related post that is still a draft renders as a broken card.

Paid-campaign landing pages are frequently `noindex, nofollow`. They are fine for a reader clicking through but pass no value and cannot be cited, so check the robots meta tag with a fetch before relying on one as a destination, and flag it in the delivery notes.
