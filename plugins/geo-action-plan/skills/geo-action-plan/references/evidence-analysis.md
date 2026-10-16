# Reading the evidence layers

Read this during Step 1 (citation layer) and after Step 2 (SERP layer). It covers what to extract from each layer, how to combine them, and which patterns change the plan.

## Contents
- The citation layer
- The SERP layer
- Combining the layers
- Theme clustering
- Patterns that change the plan

## The citation layer

From the AI visibility tool's cited pages and cited domains (Peec AI: `get_url_report` and `get_domain_report`), scoped to the prompts in question, extract and record internally:

**Page-type distribution.** Count and share of each page type across cited URLs (the tool's classification, or inferred from title and URL if it has none): Listicle, Homepage, Product Page, Comparison, Alternative, Discussion, How-To Guide, Article, Profile, Category Page. This distribution is the single most important input to the plan's portfolio mix, because it says what *kind* of page gets retrieved for these prompts. A typical B2B software dataset lands near listicles 40–55%, vendor-owned pages (homepage + product) 20–30%, comparisons ~10%, UGC 5–10% — but never assume it; count it. If the actual distribution is unusual, the plan follows the actual distribution and the Read Me says so.

**Top domains, and how they win.** Distinguish three shapes, because each implies a different response:
- *Editorial listicle players* (a media site with one strong page per phrasing) — beat with a better page on the same phrasing.
- *Self-citation champions* (vendors whose own product/feature pages get cited) — proof that vendor-owned pages are winnable here; these justify the product-page rows.
- *Aggregators and review platforms* (G2, Capterra) — usually not beatable with content; they belong in the off-site tab as profile work.

**The brand's own presence.** Filter the cited domains for the brand's own domain (Peec AI: `get_domain_report` with `classification: "You"`, or the own domain from `list_brands`). Anything found is a defend/update candidate, and the plan must not field a competing new page against it.

**Competitor concentration.** The brands mentioned on each cited URL (Peec AI: `mentioned_brand_ids`, resolved through `list_brands`) show which brands the cited pages actually name. A page citing five competitors and not the brand is the clearest possible off-site target. With Peec AI, the `gap` filter on both report tools does this directly: `{field: "gap", operator: "gte", value: 2}` returns sources where the own brand is absent but at least two competitors are present.

**UGC share.** Reddit, Quora, YouTube, LinkedIn, forums. These cannot be won with on-site pages. Report the share in chat and the Read Me, and route the specific threads to the off-site tab. Never convert them into content rows.

**Format signals.** Scan cited page titles for "we tested", "we analyzed", years, prices, "vs", "alternatives". These formats outperform in nearly every dataset and should shape the briefs. Reading the top few cited pages (the tool's indexed content, or a fetch) confirms whether the format signal is real (an actual methodology section) or just a title claim.

## The SERP layer

From the searches run in Step 2:

**Dominant domains** — many queries × many distinct URLs is the "one page per phrasing" pattern. Name the domains doing it; it is usually the strategy the plan should copy.

**Cross-query overlap** — what fraction of pages appear for 2+ intents. Low overlap means retrieval is highly phrasing-sensitive, which is the empirical justification for planning separate scoped pages per phrasing rather than one page trying to serve several.

**Per-intent incumbent sets** with appearance counts and weighted scores. When the citation layer is thin for an intent, these stand in as the demand and strength signal.

**Title-format signals** — same scan as above, on ranking rather than cited titles.

## Combining the layers

Join on domain and on URL. Three groups matter:

- **Strong in both layers** — the hardest targets. Flag them; beating them needs a genuine differentiator, not a marginally better version.
- **SERP-only winners** — pages Google ranks that AI does not cite. Often beatable on extractability: self-contained quotable sentences, question-led H2s, answers in the HTML rather than behind JS.
- **Citation-only winners** — pages AI trusts that do not rank. Beatable on classic SEO while matching their substance.

Every "sources to beat" cell must label which layer each incumbent came from, with its real metric. Never merge the two metrics into one invented score.

## Theme clustering

Cluster cited and ranking URLs by topic using keyword matching on title + URL, then sum retrievals (citation layer) or weighted score (SERP layer) per theme. The themes with the most retrieval volume are the demand signal that drives priority.

Build the keyword map from the actual dataset rather than a fixed list: pull the recurring nouns and modifiers out of the fan-out queries and prompt texts in scope, and use those as cluster seeds. A cluster with high volume and no owning plan row is a gap; a cluster with several rows is a cannibalization risk.

## Patterns that change the plan

- **Own domain absent from both layers entirely** — expect this when AI visibility is near zero. It is not an error; it means every row is Create or Fix, and it makes the technical audit more urgent, since invisibility is sometimes a crawler problem rather than a content problem.
- **One domain winning nearly everything** — check whether it is a single page or many. Many pages means the phrasing-per-page strategy works in this category and should be copied.
- **High UGC share** — the on-site plan will be smaller than expected and the off-site tab larger. Say this in chat rather than padding the content plan to look substantial.
- **Thin evidence for a prompt in scope** — few cited sources and weak SERP incumbents is the cheapest possible win. Flag it prominently; these rows usually deserve P0 despite low absolute volume.
