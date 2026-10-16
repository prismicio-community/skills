# Linking Standards (Phase 6)

Three things have to be true of every link: it resolves, the anchor text describes where it goes, and it earns its place in the sentence. A link that fails any of the three costs more trust than it adds.

## Internal links: 4 to 8

Sources of candidates, gathered in Phase 2:
- The brand's CMS, through its connector if one is connected (search published content for the topic and its subtopics).
- `curl -s https://<domain>/sitemap.xml`, following sitemap indexes.
- Anything the user supplied in the interview.

What to link to, in order of value:
1. **Deeper content on a subtopic this article only touches.** The reader who wants more gets it, and the article stays tight.
2. **Docs or feature pages** when a specific capability is named.
3. **Adjacent funnel-stage articles.** An awareness piece links to the consideration piece, not to the pricing page.
4. **The cluster pillar**, if one exists.

Placement rules:
- Link at the moment the reader would want more, which is almost never the first paragraph and almost never a block of links at the end.
- One link per destination. Two links to the same URL in one article is a sign the section structure is wrong.
- No link in the TL;DR. It is a summary, not a navigation menu.
- Never insert a link to reach the count of 4. If only three internal links fit honestly, report that instead of padding, and note which planned page would fix it.

## External links: 2 to 4

Primary sources only: official documentation, the actual study or dataset, standards bodies (W3C, MDN, IETF), government or regulator publications, official pricing and changelog pages, recognised engineering publications.

Not: content-marketing blogs restating a study, statistics aggregator sites, SEO listicles, competitor marketing pages (the exception is quoting a competitor's own documented behaviour, where their docs are the primary source).

Go upstream. If a blog cites "a 2024 Gartner finding", find the Gartner page. If the primary source sits behind a paywall, link it anyway and attribute in text, rather than linking a free page that misquotes it.

**Every external URL must be one that was actually opened during research.** Never reconstruct a URL from memory or by pattern-guessing a documentation path. Guessed URLs are the single largest source of broken links in this workflow, and they look exactly like real ones until someone clicks.

## Anchor text

Descriptive, specific, and matching the destination. The reader should be able to predict the page from the anchor alone.

| Bad | Good |
| --- | --- |
| click here | the content modelling docs |
| read more | the 2024 Web Almanac chapter on CMS adoption |
| this article | our guide to component-based page building |
| https://example.com/docs/x | the MDN reference for `fetchpriority` |

Rules:
- 2 to 6 words. A whole sentence as an anchor is hard to scan.
- No naked URLs in body text.
- Do not use the same anchor text for two different destinations.
- Keyword-stuffed anchors that misdescribe the target are worse than generic ones.
- Anchor text should share at least one meaningful word with the destination's title or slug. The checker warns when it does not.

## Contextual fit

Before keeping a link, ask whether a reader clicking it would find what the sentence promised. Three common failures:

- **The tangential link.** The destination is about the topic but not about the claim in the sentence.
- **The self-serving link.** A product page dropped into an explanatory passage where a doc page was what the reader needed.
- **The redundant link.** Linking a term the reader has already seen linked, or linking something they do not need to leave the page to understand.

## Verification

Run the checker before delivery, and again after any edit that touches links:

```bash
python scripts/check_links.py /path/to/article.md --internal-domain <your domain>
```

It reports, per link: HTTP status, redirect chain, internal or external classification, anchor text warnings, duplicate destinations, and anchor-to-destination token overlap. It exits non-zero if anything is broken.

Handling results:
- **404, 410, DNS failure** → find the correct URL by searching, or remove the link and rewrite the sentence so it does not dangle.
- **301 or 302** → update to the final destination. Publishing a redirect chain is sloppy and slow.
- **403 or 429** → often bot blocking rather than a dead page. Verify manually before removing, and note it in the appendix.
- **Timeout** → retry once, then verify manually.

Never ship a link the checker could not confirm without saying so in the delivery notes.

## Link inventory

The research appendix carries a table of every link: anchor text, destination, internal or external, the section it appears in, the claim it supports, HTTP status, and date checked. This is what makes the article auditable six months later when a source moves.
