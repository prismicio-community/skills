---
name: link-old-posts-to-new-article
description: "On explicit request only, add links to a newly published article from 3 to 8 existing blog posts, by linking words already there or updating a related-posts block, never adding prose. Shows an approval table first; stages edits where the CMS allows it (Prismic releases), otherwise hands over the exact edits. Use for 'interlink this post', 'link to it from our old posts'."
---

# Interlinking

Point 3 to 8 existing published blog posts at a new article. This is the only skill in the workflow that touches published content, which is why every step below is gated.

**Three hard rules, none negotiable:**

1. **Runs only on explicit request.** Publishing an article is never, by itself, a reason to start. If the conversation suggests link-old-posts-to-new-article would help, say so and wait to be asked.
2. **No new prose, ever.** A link is placed by linkifying a phrase that already exists on the page, or by updating a related-posts block. Never a new sentence, never a "Related:" callout, never a rewritten paragraph. If neither placement exists on a page, the page is skipped.
3. **Approval before edits, and edits never go straight live.** The table is shown and the user approves rows. Approved edits are then staged, where the CMS can stage edits to published posts, or handed to the user as exact edits to make. Nothing goes live from this skill without an explicit instruction to publish.

## Brand settings

This skill holds no brand details. They live in a brand settings document the user owns, titled "Article writer brand settings", created by the personalize-article-writer skill. Never write brand details into this skill's own files.

**At the start of every run, look for it**, unless it was already loaded earlier in this conversation. Check the assistant's memory and project files, then search the connected document tools (Notion, Google Drive and similar) for a document with that title. If you find it, read it and say in one line which brand you loaded. If you find more than one, ask which to use. If you find none, run without it: ask for each setting at the step that needs it, and at the end suggest personalizing once ("Personalize the article writer for my brand") so later runs skip those questions.

This skill uses: website, CMS and its connector, the live site, space or repository, the blog post type, its related-posts block, and whether edits to published posts can be staged. A setting marked `Not set`, or missing, means: ask the user at the step that uses it. Wherever this file says "the brand settings", it means that document, and "the brand" means the brand it describes.

**Staged** means the CMS keeps edits to a published post unpublished until a person republishes it: Prismic releases do, and so do some other CMSs (see `references/other-cms.md`). **Suggestions only** is the safe default for every other case, and for any CMS without a connector.

## Phase map

| Phase | What happens | Gate |
| --- | --- | --- |
| 0 | Explicit request from the user | **Runs only when asked**; never triggered by publishing alone |
| 1 | Find candidate source pages (published blog posts, capped at 8) | none |
| 2 | For each, find the placement (linkify or related-posts block) or rule it out | none |
| 3 | Show the approval table | **Stop and wait for approval** |
| 4 | Staged: stage approved edits (Prismic: a release named `Interlinking: <article title>`). Suggestions only: hand over the exact edits | none |
| 5 | Report | **Publish only on an explicit instruction to publish**, and only where staged |

**Final outcome:** 3 to 8 existing blog posts linking to the new article, either staged and reported by name, or listed as exact edits for the user to make.

## Step 1: candidate pages

Search the CMS's published blog posts through its connector, with several phrasings of the new article's topic. Without a connector, use the sitemap (`scripts/sitemap_inventory.py <website> --match <terms>`) and read the candidate pages with the web fetch tool; the outcome is then always suggestions only. Blog posts are the whole scope: marketing pages have owners and conversion jobs and are not edited by this skill.

Rank candidates by how specifically their content overlaps the new article, not by recency. A two-year-old post that discusses exactly this topic beats last week's adjacent one, and updating an old post is itself a freshness signal.

Cap at 8 per campaign even when more qualify. A dozen pages suddenly linking one URL inside a week is a pattern; a handful is architecture. Below 3 natural placements, report what exists rather than forcing the minimum.

## Step 2: placement, links only

Read each candidate's actual content. Two legal placements:

**A. Linkify an existing phrase.** Find the passage where the page already talks about what the new article covers, and wrap the existing words in a link. The phrase must read as a natural anchor for the destination as written. In formats that store links as character positions (Prismic rich text, for example), recompute the positions from the block's plain text; positions counted against anything else corrupt every link after the first.

**B. Related-posts block.** If the blog model has one and the page uses it, add the new article as an entry. Most carry 3 to 5 posts; when full, **swap out the least relevant existing entry rather than appending one more**, and show what is being replaced in the table. Choose the swap victim by reader relevance, never by age alone.

Pages with neither placement are skipped and listed as "no natural placement". That outcome is normal and correct.

Anchor variety applies across the campaign: source pages should not all link the new article with identical wording.

## The approval table

Present exactly this, then stop and wait:

| # | Source page | Placement | Exact existing text affected | After the edit | Replaces (related-posts swaps only) |
|---|---|---|---|---|---|

"After the edit" shows the same text with the link marked, or the new related-posts list. The user approves or rejects per row. Say before the table whether approved rows will be staged or handed over as suggestions.

## Step 4: stage or hand over

**Staged:**
- One staging container per campaign (Prismic: a release named `Interlinking: <article title>`).
- Get each page's current version immediately before editing; live pages move, and a stale version is rejected.
- Change only the targeted block or item. Everything else in the post is preserved exactly, including edits people made in the CMS.
- For Prismic, the editor-shape rules in `references/prismic.md` apply.

**Suggestions only:**
- Hand over the approved rows as a checklist: page URL, the exact existing words, the link URL, and where on the page the words sit. The user makes the edits in their CMS.
- Never write to a published post in a CMS that would put the change live on save.

## Step 5: report, and publish only when told

Report what was staged (and where) or the checklist, and stop.

Only where edits are staged: if, and only if, the user explicitly says to publish ("publish it", "push it live", "ship the release"), publish this campaign's own staged edits (Prismic: `publish_release` for this campaign's release), then confirm what went live. Table approval, enthusiasm or "looks good" is not a publish instruction; when unsure, ask the one-line question. Never publish anything other than this campaign's own staged edits.

## Compatibility

- **The CMS's connector** (recommended): reading posts and staging edits. Prismic's connector stages edits in releases. Without a connector, the outcome is always a list of suggested edits.
- **Script** (`scripts/sitemap_inventory.py`): needs a client that can run Python. Without one, fetch the sitemap with the web fetch tool.
