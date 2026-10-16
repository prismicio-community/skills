---
name: add-external-links
description: "Choose, verify and place 3 to 5 outbound links to primary sources (research, data, official docs) in an article draft, never to competitors, with an approval table before any edit. Use for 'add sources', 'add external links', 'what should this article cite'. For links to the brand's own pages use add-internal-links."
---

# External Linking

Add 3 to 5 outbound links per article, all research or policy grade. The number is a range, not a quota: if the draft only supports two natural links, say so and show the two rather than forcing a third. A forced link is worse than a missing one.

**Hard stop:** links are proposed in a table and approved by the user before any edit is made to the draft. No exception, even when the user asked for the links in the same message.


## Brand settings

This skill holds no brand details. They live in a brand settings document the user owns, titled "Article writer brand settings", created by the personalize-article-writer skill. Never write brand details into this skill's own files.

**At the start of every run, look for it**, unless it was already loaded earlier in this conversation. Check the assistant's memory and project files, then search the connected document tools (Notion, Google Drive and similar) for a document with that title. If you find it, read it and say in one line which brand you loaded. If you find more than one, ask which to use. If you find none, run without it: ask for each setting at the step that needs it, and at the end suggest personalizing once ("Personalize the article writer for my brand") so later runs skip those questions.

This skill uses: brand name and direct competitors. A setting marked `Not set`, or missing, means: ask the user at the step that uses it. Wherever this file says "the brand settings", it means that document, and "the brand" means the brand it describes.

## Order of work

1. Read the draft and list the claims that reach for outside authority.
2. Find the primary source for each.
3. Verify every URL.
4. Show the approval table and stop.
5. Write only the approved rows into the draft, then re-run the article's link checker.

## What earns an external link

A link is added only where the text already reaches for it:

- **A statistic or research finding** the article states or should state. Link the study, on the page where the finding lives.
- **A definition or origin** the article discusses. The paper or announcement that coined the thing beats a blog explaining it.
- **A policy or rule** the article invokes. Google Search Central, regulator pages, official documentation.
- **A dispute** the article takes a side on. Link the strongest version of the evidence.

If a sentence has to be written *so that* a link can exist, the link is rejected. The test came from real failures: stats bolted onto intros that were already convincing, and research citations attached to arguments that were complete without them. When in doubt, read the paragraph without the link. If nothing is missing, nothing is missing.

## Source hierarchy

Work down, stop at the first hit:

1. Peer-reviewed papers, arXiv, .gov and .edu sources
2. Original research from named institutions: Pew, Bain, Gartner, McKinsey and peers
3. Official documentation: Google Search Central, platform policy pages, standards bodies
4. Reputable journalism reporting a primary source that is itself unlinkable
5. Nothing. A claim without a source at levels 1 to 4 gets rephrased or cut, not linked to a weaker source.

**Never acceptable as sources:** competitor pages of any kind, vendor blogs, SEO-tool content farms, affiliate roundups, and secondary posts citing a study you could link directly. If a stat only exists on a vendor's blog, find the underlying study or drop the stat.

**Competitor rule, absolute:** no links to competitors' domains. When a claim about a competitor needs evidence, use a screenshot of their page or a neutral third-party source. If neither exists, cut the claim. Do not soften this by linking "just their docs" or "just their pricing page"; those are still competitor pages.

## Verification

```bash
python scripts/verify_urls.py candidates.txt
```

Every candidate must return 200 at its final URL. Redirected URLs are replaced with their destination. Fetch the page and confirm the claim actually appears on it: linking a study for a number that lives in a different study is the most common citation error in this category, and it survives every automated check.

Press-release aggregators (PRNewswire and similar) are replaced with the institution's own page for the same content when one exists.

## Anchors

- Under 8 words, descriptive of the destination: "Pew Research finds users click links less often", not "a study" or "research shows".
- The anchor's claim must match what the destination says, at the wording level. "80% of consumers" as an anchor requires the 80% figure on the target page.
- Never "click here", "this study", or a bare URL.

## The approval table

Present exactly this, then stop and wait:

| # | Destination | Anchor text | Section | The sentence it lives in | New or existing sentence |
|---|---|---|---|---|---|

The last column matters: a link into an existing sentence is presumptively natural, a link needing a new sentence carries the burden of proof and the new sentence is shown in full. After approval, write only the approved rows, leave rejected ones out without argument, and show the final count.

## Placement notes

- One link per source per article. A source worth citing twice is worth citing once, well.
- External links cluster naturally in FAQ answers, methodology sections and risk sections, where the reader is asking "says who". They rarely belong in the intro or the summary, where they leak attention before the article has made its case.
- These are follow links. If the site later wants nofollow on externals, that is a frontend template change, not something the CMS link can express.

## Compatibility

- **Web search** (required): finding and opening primary sources.
- **Script** (`scripts/verify_urls.py`): needs a client that can run Python. Without one, open each URL with the web fetch tool and check its status and robots meta.
