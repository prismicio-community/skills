---
name: add-internal-links
description: "Choose, verify and place 4 to 8 links from an article draft to live, indexable pages on the brand's own site, found through the CMS connector or the sitemap, with an approval table before any edit. Use for 'add internal links', 'which of our pages should this link to'. For outbound sources use add-external-links; for links from old posts to a new one use link-old-posts-to-new-article."
---

# Internal Linking

Add 4 to 8 internal links per article, each one a path a real reader would take next. A call-to-action block does not count toward the range; it is its own element with its own job.

## Brand settings

This skill holds no brand details. They live in a brand settings document the user owns, titled "Article writer brand settings", created by the personalize-article-writer skill. Never write brand details into this skill's own files.

**At the start of every run, look for it**, unless it was already loaded earlier in this conversation. Check the assistant's memory and project files, then search the connected document tools (Notion, Google Drive and similar) for a document with that title. If you find it, read it and say in one line which brand you loaded. If you find more than one, ask which to use. If you find none, run without it: ask for each setting at the step that needs it, and at the end suggest personalizing once ("Personalize the article writer for my brand") so later runs skip those questions.

This skill uses: brand name, website, sitemap, CMS and its connector, and the site, space or repository that holds the live site. A setting marked `Not set`, or missing, means: ask the user at the step that uses it. Wherever this file says "the brand settings", it means that document, and "the brand" means the brand it describes.

## Order of work

1. Inventory candidate destinations from the live site.
2. Map the draft's reader intents to destinations.
3. Verify every URL, including robots meta.
4. Show the approval table and stop.
5. Write only the approved rows, then re-run the article's link checker.

## Step 1: inventory, never memory

Candidate pages come from the live site, not from guessed slugs. Use whichever route is available, in this order:

- **CMS connector.** If the brand's CMS has a connector connected, search its published content in the repository or space named in the brand settings, with several phrasings of the article's topic, since semantic search returns a relevance sample. Include marketing pages, tools and blog posts; exclude staging, sandbox and drafts.
- **Sitemap.** Otherwise, or as a cross-check, list the site's pages from its sitemap:

```bash
python scripts/sitemap_inventory.py <website or sitemap URL> --match "<topic>,<subtopic>" --titles 30
```

  It follows sitemap indexes, keeps URLs whose path matches the terms, and fetches titles and robots meta for the first matches. If the script cannot reach the site from this environment, fetch the sitemap with the web fetch tool and filter it the same way. Run it with several term sets: URL paths rarely use the article's exact keyword.
- **The user.** Anything they named in the interview.

Then verify each candidate URL directly:

```bash
python scripts/verify_urls.py candidates.txt
```

**Never link a noindex page as architecture.** Paid-campaign landing pages are frequently `noindex, nofollow`; they work for a clicking reader and pass nothing to anything else. If the best destination for an intent is noindex, flag it to the user as a fix-the-page finding and choose an indexable alternative for the link. A noindex link may survive only when the user explicitly keeps it for reader value, and it is then marked as such in the table.

## Step 2: map reader intents, not keywords

Every draft has readers at different points, and each earns a path:

- **The not-ready reader** wants the strategy piece behind the topic, usually from the closing section.
- **The next-question reader** finishes a section with an obvious follow-up; the answer post gets the link at that exact point.
- **The wants-proof reader** needs the first-party evidence page for a claim the article makes.
- **The ready reader** wants the product or use-case page, linked once, where the text naturally turns to doing the thing.

Priority when choices compete: commercially relevant product and use-case pages where the text genuinely turns toward them, then cluster-relevant blog posts, then tools. A product page forced into an editorial paragraph reads as an ad; the same link in the "where to start" section reads as directions.

## Rules that override placement

- **The naturalness test.** A link is added only where the text already reaches for it. If a sentence must be written so a link can exist, the link is rejected. Linkifying an existing phrase always beats adding a sentence.
- **Product and audience separation.** Never link pages that frame the brand through a product category the article deliberately avoids. A GEO article does not link CMS-positioned pages, however strong they are, because the destination's framing undoes the article's.
- **No homepage links on the brand name.** Readers know where the homepage is. The brand's navigational link is the product or use-case page that fits the article's reader.
- **Anchor variety.** Under 8 words, descriptive, and varied: if the site already links a destination with one anchor, use different wording here. Identical anchors repeated across the site toward one page read as manipulation.
- **One link per destination per article.**

## The approval table

Present exactly this, then stop and wait:

| # | Destination | Anchor text | Section | The sentence it lives in | New or existing sentence | Indexable |
|---|---|---|---|---|---|---|

After approval, write only the approved rows and report the final count against the 4 to 8 range. If natural placements run out below 4, say so and show what exists rather than forcing the minimum; the user decides whether thin is acceptable.

## Handoff

This skill edits the draft in the conversation workspace only. It never touches the CMS or any live page.

## Compatibility

- **The brand's CMS connector** (optional): searches published content. Without it, the sitemap.
- **Scripts** (`scripts/sitemap_inventory.py`, `scripts/verify_urls.py`): need a client that can run Python. Without one, fetch the sitemap and the candidate pages with the web fetch tool.
