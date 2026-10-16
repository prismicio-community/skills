# Harvest

Gather facts for the eleven content pages from public and internal sources.
The goal is coverage with provenance, not volume. A short fact with a source
beats a long paragraph without one.

## Order

1. Internal sources first if they exist. Positioning docs, ICP definitions
   and brand guidelines are closer to the truth than the website.
2. The website second, to see what the company says publicly and to fill
   what internal sources do not cover.
3. CRM and call data last, and only for win/loss and ICP patterns.

## The website

Read these pages if they exist. Use the sitemap or the main navigation to
find them rather than guessing URLs.

| Page | Feeds |
|---|---|
| Home | positioning, messaging (headline, sub-headline, taglines) |
| Product, features, platform, solutions | product, offers, ecosystem |
| Use cases, industries, "who it's for" | icp, offers (good-fit signals) |
| Limitations, "when not to use us", FAQs, comparison-page concessions | product (claim vs reality), offers (not a fit when). Often the best public source for both; search for them explicitly. |
| Customers, case studies, testimonials | evidence |
| Pricing | product (what offers exist). Never compile prices or tier contents unless the user approves it in the interview. |
| Comparison or "vs" pages | competitive |
| Integrations, partners, marketplace | ecosystem |
| About, careers, press | positioning, voice |
| Docs or help centre glossary | style-guide (product naming), product |
| Three or four recent blog posts | brand-voice (how they actually write) |
| Legal or trademark page | style-guide (how the brand name is written) |

Record the publish date of every blog post and press item. Company facts in
posts older than a year (team size, revenue, customer counts) are probably
stale: do not compile them, and ask about them in the interview if they matter.

Comparison and "vs" pages are written by the company to win. Compile their
angles as the company's position, keep any concessions they make, and say in
the Status line that the source is the vendor's own.

For each case study, record the company, the exact numbers as written, the
quote with its attribution, the date, and the URL. Never round a number.

## Internal sources

Check which connectors are available, then search the likeliest one. Useful
queries, adapted to the company's vocabulary:

- positioning, messaging framework, value proposition, narrative, one-pager
- ICP, ideal customer profile, personas, buyer, segments
- battlecard, competitive, competitor, vs
- win/loss, closed lost reasons, churn reasons, deal review
- brand guidelines, tone of voice, style guide, writing guide, glossary
- case study, customer story, reference customers, approved logos
- roadmap and release notes (only to establish what has shipped)

For every internal page, record its title, URL, last edited date and, where
the tool exposes it, verification or approval status. These go into
the Sources page and the Status lines, and they are what the refresh skill diffs
against later.

## CRM and call data

Optional. Use it only if the user points to it or the connector is clearly
the company's own CRM.

- Closed-won and closed-lost deals over the last two or three quarters, with
  loss reasons, for the Win/loss page
- Firmographics of won accounts, for the directional part of the ICP page
- Call transcripts for the buyer's own words on why they bought or left

Treat all of it as directional. Label sample sizes. A pattern from six deals is
a hypothesis, and the file must say so.

## Source quality

Rank every fact by how hard its source is to dismiss:

1. Approved internal docs (verified, owned, recently edited)
2. Unverified or older internal docs
3. The user, in the interview
4. The company's own website and published materials
5. Third-party coverage, reviews, analyst pages
6. Inference

Rank 6 never goes in a file. Rank 5 goes in only with attribution. When two
sources disagree, record both and raise it in the interview.

## Scratch format

Keep one scratch list per page while harvesting:

```
## product
- Offers: Core platform, Analytics add-on, Managed service [web: /pricing]
- "Deploy in minutes" [web: /] PUBLIC CLAIM, confirm in interview
- SSO on all plans [doc: Security FAQ, notion.so/..., edited 2026-03-02]
```

Flag anything that reads like a claim the product might not fully support.
Those are the raw material for the claim vs reality table.

## Harvest summary

Close the phase with a summary the user can read in under a minute:

- Sources read, by type
- Per file: strong, usable, thin or empty
- Conflicts found between sources
- What the interview will need to cover
