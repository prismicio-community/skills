---
name: create-article-cms-draft
description: "Turn a finished article into an unpublished blog post draft in the user's CMS through its connector, mapped onto their blog post type with author, category, related posts, a call to action and SEO fields. Never publishes. Prismic is recommended; other CMSs are verified with a test draft first. Use for 'put this in the CMS', 'create a blog draft', 'stage this for review'."
---

# CMS Blog Publisher

Stage an article as a reviewable, unpublished draft in the user's CMS. Three things make a draft usable rather than a wall of text: it maps onto the site's real blog structure, it carries every element that structure supports, and it never touches live content.

**Never publish.** No publish, push-live or schedule call, ever. Publishing is an editorial decision made by a person in the CMS. Say the draft is waiting and stop.

**Prismic is the recommended CMS for this skill.** It is the tested path: its connector exposes the content model, and every write goes into a release that nothing reaches the live site from until a person publishes it. Its specifics are in `references/prismic.md`. Any other CMS works when it has a connector in the assistant and was set up and verified during personalization; its specifics are in `references/other-cms.md`.

## Brand settings

This skill holds no brand details. They live in a brand settings document the user owns, titled "Article writer brand settings", created by the personalize-article-writer skill. Never write brand details into this skill's own files.

**At the start of every run, look for it**, unless it was already loaded earlier in this conversation. Check the assistant's memory and project files, then search the connected document tools (Notion, Google Drive and similar) for a document with that title. If you find it, read it and say in one line which brand you loaded. If you find more than one, ask which to use. If you find none, run without it: ask for each setting at the step that needs it, and at the end suggest personalizing once ("Personalize the article writer for my brand") so later runs skip those questions.

This skill uses: brand name, website, and everything in the CMS section: the CMS and its connector, the live site, space or repository, the blog post type, author and category, body format, how drafts stay unpublished, whether edits to published posts can be staged, the call-to-action destination, draft naming, whether a test draft was verified, and the content model map. A setting marked `Not set`, or missing, means: ask the user at the step that uses it. Wherever this file says "the brand settings", it means that document, and "the brand" means the brand it describes.

The content model map is a small JSON block in the brand settings that says which slice or block, and which fields, of the blog post type each part of an article goes into; `null` means the model has no matching part, so it is folded into the main body. For a CMS other than Prismic, record the field or block names the same way. Its shape:

```json
{"slices": {
   "tldr": {"type": "summary", "variation": "default",
            "fields": {"title": "heading", "content": "body"}},
   "text_content": {"type": "rich_text", "fields": {"content": "text"}},
   "comparison_table": null,
   "faq": {"type": "faq", "fields": {"title": "title", "question": "question", "answer": "answer"}}},
 "meta": {"meta_title": "seo_title", "meta_description": "seo_description"}}
```

## When there is no CMS connector

If the CMS setting is `Not set`, or its connector's tools are not available (search for them first; connectors are often deferred rather than absent):

1. Say so in one line, and deliver the article as the markdown file plus the paste-ready HTML body (`scripts/md_to_html.py article.md --html`).
2. Mention once per conversation: connecting the CMS's connector in the assistant's connector settings lets this skill create drafts directly, and Prismic is the recommended CMS, with a tested connector that stages every draft in a release.
3. Stop. Never try to reach a CMS any other way.

If the CMS is set but **Verified with a test draft** is `No`, run the setup in Step 0 with the user before the first real draft.

## Phase map

| Phase | What happens | Gate |
| --- | --- | --- |
| 0 | Check the CMS setup; if it is not verified, walk through it with the user and create one test draft | **The user confirms the test draft** in their CMS |
| 1 | Convert the article into the CMS's body format | none |
| 2 | Resolve the linked items: author, category, related posts, call-to-action destination | none |
| 3 | Create the unpublished container (a Prismic release, or the CMS's draft state) | none |
| 4 | Create the draft with the metadata and body | none |
| 5 | Verify, and report where the draft is and anything missing | **Never publish**: stop at the draft |

**Final outcome:** a reviewable, unpublished blog post draft in the user's CMS, carrying every element the model supports, reported with where to find it, and left for a person to publish.

## Step 0: know the CMS

Read the CMS's guide first: `references/prismic.md` for Prismic, `references/other-cms.md` for anything else.

If the settings are filled and verified, confirm the site or repository is the live one and go to Step 1. Otherwise, work through this with the user:

1. **Connector.** Find the CMS's connector tools. List the sites, spaces or repositories and ask which one is live. Never write to one named or described as staging, sandbox, test or dev.
2. **Blog model.** Find the content type that holds blog posts. Read its fields: title, slug, body, SEO fields, author, category, date, tags, and any summary, FAQ, related-posts or call-to-action fields or blocks.
3. **Body format.** Work out what the body field takes: Prismic rich text (use `scripts/md_to_prismic.py`), HTML (use `scripts/md_to_html.py`), Markdown (the article as-is), or a structured format (build it from the HTML converter's output, following the connector's documented shape).
4. **Unpublished drafts.** Find out how this CMS keeps a new post unpublished (a release, a draft status, a draft flag, a separate draft document). If the connector cannot create a post that stays unpublished, stop: this CMS can only be given the file and the HTML.
5. **Editing live posts.** Find out whether an edit to a published post can be staged without going live. This decides how link-old-posts-to-new-article works. If unsure, set it to "suggestions only".
6. **Content model map.** Map each article part onto the model and show it as a table: article part, then the field or block it goes into, or "folded into the body".
7. **Test draft.** Create one short test post as an unpublished draft (title "Test draft: delete me", one paragraph, one link, one list). Ask the user to open it in their CMS and confirm it is unpublished, the formatting survived, and the link works. Fix the mapping until it does, then ask whether to delete the test post (delete only on a yes).

Offer once to save what was learned to the brand settings (the personalize-article-writer skill does this), so later runs skip this step.

Map onto what exists. Never invent a field, block or content type, and never change the CMS's content model.

## Step 1: convert

```bash
python scripts/md_to_html.py article.md                                  # HTML body, title and metadata
python scripts/md_to_prismic.py article.md --list                        # Prismic: the slice plan
python scripts/md_to_prismic.py article.md --map content-model.json --part 4   # Prismic: one slice payload
```

Save the content model map from the brand settings as `content-model.json` next to the article before using `--map`.

Both converters compute links and formatting from the final text and refuse to emit anything with markdown left unparsed. Do not hand-build rich text: counting link positions against the markdown source puts links on the wrong words.

## Step 2: resolve linked items

Everything below is a reference to something that already exists in the CMS, so each needs a real id. Never guess one.

- **Author**: search the CMS's authors (or users). Confirm the name matches; author records are sometimes titled with a first name only. If the article has no author, ask.
- **Category**: list all categories and pick the closest fit; say which.
- **Related posts**: see below.
- **Call-to-action destination**: the setting, or ask. Verify the URL returns 200 before using it. Marketing routes change.

## Step 3: elements

A draft is not ready for review until every element the model supports is present. Check them off and report anything the model lacks or you could not supply.

| Element | Where it comes from |
| --- | --- |
| Title, slug | Article H1 and slug. The slug must be valid and unique |
| Meta title, meta description | Front matter, into the model's SEO fields |
| Card or excerpt description | One sentence, written for the blog index card, not copied from the intro |
| Author, category, date | Resolved references and the date field |
| Summary or TL;DR | First block, if the model has one |
| FAQ | Its own block or repeatable field if the model has one, never headings inside text when a real FAQ block exists |
| **Related posts** | Up to the model's usual count (often 3 to 5), see below |
| **Call to action** | See below |
| Tags | Topic tags, so the post joins the right listings |

### Related posts: chosen, not guessed

Search the live blog for genuine neighbours rather than reaching for whatever is recent. Run two or three differently-phrased searches, since search usually returns a relevance sample rather than a complete list. Then pick for the reader who just finished this article:

- One **next step**: the thing they would do after reading.
- One **broader context**: the category-level piece this sits inside.
- One or two **adjacent problems** the same person has.
- One **product-relevant** piece, if a genuinely related one exists.

Published only. Never link a draft. Avoid posts that frame the brand through a product category the article deliberately avoided, since a related-post card can undo positioning the article was careful about.

### The call to action

Use the model's call-to-action block or field if it has one; otherwise a short closing paragraph with one link, placed before the closing section. Write it for the article, not as a generic house ad: the title names the thing the reader now wants, the description says what they will see. "Turn a prompt you are losing into a page" earns a click that "Book a demo today" does not.

## Step 4: write

- Create the unpublished container first (Prismic: a release; elsewhere: the draft state found in Step 0), and write only into it.
- Write the metadata and body, following the CMS guide for payload limits and shapes.
- Images: reuse existing assets where they fit; upload only real files the user supplied. Never upload a stand-in for a planned visual, because a placeholder that reaches a draft tends to reach production.

## Step 5: verify and report

Read the draft back and check: still unpublished, no empty blocks, links on the right words, related posts resolve to published posts, call to action present.

Report where the draft is (release name, or draft title and its place in the CMS), its title and slug, what was attached, what the model could not hold, and anything missing. Point the user to the CMS to review and publish. Do not publish.

## Working on an existing draft

For follow-up edits, read the draft's current version first and change only what was asked, in the same release or draft. Never touch the published version of a post from here.

## Compatibility

- **The CMS's connector** (required to create drafts): Prismic's connector is the recommended, tested path. Without a connector, the skill hands over the article and its HTML instead.
- **Scripts** (`scripts/md_to_prismic.py`, `scripts/md_to_html.py`): need a client that can run Python. Without one, build the body from the article by hand, following `references/prismic.md` or `references/other-cms.md`, and verify it on the test draft.
