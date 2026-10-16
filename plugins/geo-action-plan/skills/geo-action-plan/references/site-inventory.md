# Existing-site inventory and the create-vs-update framework

Read this during Step 4. The plan's credibility rests on this step: a plan that recommends creating a page the brand already has is worse than no plan, because it spends budget creating a competitor to itself.

## Contents
- Building the inventory
- Reading candidate pages
- The technical audit
- Assigning an Action
- The reverse gap check

## Building the inventory

**The sitemap is the spine.** Semantic search returns a relevance sample; a sample is not an inventory. Start here:

```bash
curl -s https://<site>/sitemap.xml
```

Follow `<sitemapindex>` entries to their child sitemaps and collect every `<loc>`. Record each URL with its path segments and slug keywords. This is cheap, complete, and cacheable across runs — store it in the state JSON so subsequent prompt runs reuse it rather than re-fetching.

If the sitemap is unavailable, say so explicitly and fall back to the CMS connector's document listing (if one is connected) plus any URLs the user provides — but record the limitation in the Read Me, because Action assignment is less reliable without a complete list.

**Filter to plan-relevant candidates.** Match inventory URLs against the planned intents by slug keyword and, where ambiguous, by fetched title. Only candidates need deep reading; the full list still matters for the reverse gap check.

## Reading candidate pages

For each candidate, get the real content — not the slug, not an assumption:

- **If a CMS connector is connected** (the user mentioned their CMS and its connector is available): search it with several phrasings of the topic, since one query returns a relevance sample, then read the full documents that match. Use its content-type listing when it is unclear which document type a URL corresponds to.
- **Otherwise**: fetch the live page and read the rendered content.

Read enough to answer: what does this page currently claim, what sections does it have, when was it last meaningfully updated, does it already cover the target phrasing, and how does it compare to the incumbents for that intent?

This is what makes an Update brief a *diff* rather than a rewrite. An Update brief that does not reference specific existing sections was not written against the real page — go back and read it.

Exclude staging and sandbox environments, and exclude drafts. Only published, live pages count as inventory.

## The technical audit

Run on the site root and on every plan-relevant existing page:

**`<meta name="robots">`** — a `noindex` page is invisible to every AI crawler and to search. This is a shockingly common finding on marketing landing pages (`/lp/` paths especially), and when present it is always row 1 of the plan, P0, Action = Fix. A brand can have excellent content and near-zero AI visibility for this reason alone.

**robots.txt** — check whether GPTBot, ClaudeBot, PerplexityBot, and Google-Extended are allowed. A blocked crawler is a Fix row and explains citation-layer absence better than any content gap.

**llms.txt** — note presence or absence. Do not overclaim its impact; its effect is debated. It is a cheap row, not a priority one.

**Content extractability** — is the substance in the delivered HTML? FAQ answers hidden behind JS accordions, tables rendered client-side, and key claims in images are all invisible to retrieval. This is the most common reason a page ranks but is never cited, and it converts a would-be Create row into a much cheaper Update.

## Assigning an Action

Map every planned intent against the inventory:

**Create** — no existing page targets the phrasing. The default only when the inventory genuinely has no match.

**Update** — an existing page targets it but is weak: thin, stale, unextractable, or missing sections the incumbents have. The brief is a diff against the fetched current page: keep / change / add. Never a from-scratch brief for a page that exists.

**Retarget** — a strong page exists under the wrong phrasing or title. On-page retitling and section edits, not a new page. Common when the brand wrote for its own vocabulary rather than the query's.

**Consolidate** — several existing pages compete for one phrasing. Merge into the strongest and 301 the rest. This fixes self-cannibalization the brand already has, and it is often a bigger win than anything new.

**Keep** — the page already serves the intent well, or already appears in the evidence layers. Recorded with its URL so nobody duplicates it; no work assigned.

**Fix** — technical blockers from the audit.

When in doubt between Create and Update, read the existing page rather than guessing. Guessing produces the exact failure this step exists to prevent.

## The reverse gap check

Scan the full inventory for topic-relevant pages that map to no planned intent. Each gets one of:

- a **Retarget** or **Consolidate** row, if it could be serving an intent in scope, or
- a line in the Read Me under "reviewed, intentionally untouched", with one clause on why.

The plan should account for the whole relevant estate in both directions: every intent has a page, and every relevant page has a disposition.
