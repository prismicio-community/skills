# Brand claim check: sources and patterns

Phase 3 of the analyzer checks every claim about the brand against the brand's own sources: its latest positioning, its knowledge sources, and its live website and docs. Read everything live in every run. Nothing in this file is itself a source of facts about the brand: it tells you where to look, which source wins, and what to look for.

The sources come from the brand settings in the analyzer's SKILL.md, filled in when the user personalized the workflow. Where a setting is `Not set`, use what the user shared in this conversation, then the public website.

## Step 1: Latest positioning (always read)

Read the Positioning and messaging sources first, for every article that mentions the brand. These decide what the brand is now: its category, value proposition, audience and what makes it different. They can be a positioning doc, a messaging framework, a sales narrative, a pitch deck, or the brand's product pages if nothing formal exists.

Then look for anything newer in the same place: a positioning doc in a knowledge base often has newer drafts or messaging pages beside it. Search the connected knowledge base for `positioning`, `messaging`, `narrative`, plus the topic of the claim, and scan by last-edited date. Positioning drafts and project notes show where positioning is heading. Use them to spot claims that are going out of date, but treat them as drafts, not approved wording (see precedence below).

## Step 2: Knowledge sources (by claim type)

| Claim is about | Look for |
| --- | --- |
| A feature, capability, integration, or how something works | Product docs, feature sheets, release notes |
| A competitor, a comparison, why the brand wins or loses | Competitive pages, battle cards, comparison docs |
| A customer name, case study, quote, testimonial or result | Published case studies, customer evidence pages or docs, including any reuse limits they state |
| Who the brand is for, ICP, personas | The positioning sources, persona or ICP docs |
| Voice, banned words, phrasing, naming | The Brand voice and style guide setting |

When a claim is not settled there, search the connected tools for it directly (the feature name, the number, the customer, the competitor). A roadmap item is not a shipped feature: a claim that something exists today needs a shipped source.

## Step 3: The website and docs

Check what the brand says publicly, through its CMS connector or by fetching the pages:

- Product, feature, solution and integration pages, for what the brand tells customers today.
- Product documentation, for how a capability actually works and its limits. Docs are the strongest source for "can it do X" claims.
- The pricing page, only to confirm a pricing claim is safe to make. If the article states or implies price or plan contents, it must match the pricing page exactly.

## Which source wins

1. **Product docs and shipped feature pages** decide whether a capability exists and what it does.
2. **The latest approved positioning** decides how the brand describes itself: category, value proposition, audience, differentiation.
3. **Evidence sources** decide customer names, quotes, results and their reuse limits.
4. **The website** shows what is already public. A claim that matches the website but contradicts newer positioning is **Drifted (outdated positioning)**: flag it and give the newer wording.
5. **Drafts and notes** never make a claim Supported on their own. If a draft contradicts the approved sources, report it as "positioning in flux" and flag it for whoever owns positioning.

When two sources disagree, report both with links and dates, apply the order above, and flag the conflict rather than silently choosing.

Record for every page used: last-edited date, and any draft or work-in-progress marker.

## What to look for

Most bad claims are not lies. They are plausible sentences nobody sourced. These are the patterns that slip through most often.

**Outdated positioning.** The article describes the brand in an older way (an earlier category label, value proposition or audience) that the latest positioning has replaced.

**Overclaimed capability.** A feature described more broadly than its docs: available on every plan or flow when it is scoped to one, working generally when it works for one use case, or an AI capability described without the human review step the product actually has. Check the scope words: "any", "all", "every", "automatically", "instantly".

**Roadmap stated as shipped.** Something on a roadmap or in a draft described as available today.

**Category slippage.** A claimed category presented as an established fact, or the category quietly upgraded partway through the article.

**Numbers that drift.** A figure restated so it changes meaning: "60 pages in 90 minutes" becoming "dozens of pages in minutes", "5,000+ customers" becoming "thousands of enterprises". Rounding and restating are the most common drift and the hardest to spot, because the new version often sounds more careful than the original.

**Pricing and packaging leakage.** Any sentence a reader could use to infer price, what a plan includes, or what is an add-on, unless the pricing page supports it exactly.

**Restricted evidence.** Customer stories can carry reuse limits. Check every customer mention against the evidence sources, and list each one used.

**Say / don't-say.** Messaging docs often list preferred and avoided phrasings. Flag avoided phrasings and suggest the preferred one.

**Banned vocabulary and punctuation.** Check brand-related sentences against the brand voice and style guide, not from memory: those lists often include ordinary-sounding words that are easy to miss.

**Invented specifics.** Any brand statistic, customer name, quote or product name that appears in none of the sources is a Violation, however plausible.

## Report row

Per brand claim: number, claim (exact quote), verdict, what the source says (quote), source link with its last-edited date and status, any conflicting source, paste-ready replacement line.
