# Writing Standards (Phase 5)

The target voice is a senior practitioner who has built real systems, hit real edge cases, and has no patience for vagueness. Precise, direct, occasionally dry, never promotional.

## Non-negotiable constraints

Copy these into any brief handed to another writer or model, without paraphrasing.

- **Length:** the fewest words that clearly articulate the points. Never pad toward a target.
- **Information density:** every paragraph introduces at least one new piece of information. If deleting a paragraph does not reduce the reader's understanding, delete it.
- **BLUF:** state the answer, recommendation, or conclusion before the explanation. Do not build toward conclusions.
- **Paragraphs:** maximum 4 lines.
- **Headings:** navigational, not structural labels. No numeric prefixes on section headings, though numbered entry headings (H3/H4) are correct in listicles. No hierarchy skips. Never deeper than H4. No heading that only restates the H1.
- **Tables:** maximum 5 columns.
- **Internal links:** 4 to 8, with descriptive anchor text. Never "click here", "read more", or "here".
- **External links:** 2 to 4, to primary authoritative sources only. No competitor marketing pages. No aggregators where a primary source exists.
- **Sourcing:** every statistic, percentage, count, price, date, named study, or figure carries a source link or explicit in-text attribution. Cite primary sources. No leftover writer notes in the final article.
- **TL;DR:** first section, 4 to 10 real-takeaway bullets, summarizing the whole article rather than teasing it.
- **FAQ:** last content section, 5 to 10 real-user questions, answers 2 to 5 sentences, direct and non-evasive.
- **No em dashes.** See below.
- **No AI-cliché phrasing or structure.** See below.

## Punctuation: the em dash rule

Do not use em dashes (—) anywhere in the article. Do not use double hyphens (--) as a substitute. Do not use spaced en dashes as a substitute either.

En dashes are allowed in one place only: numeric and date ranges (4–8 links, 2020–2024).

Rewrite instead. Every em dash is doing one of four jobs, and each has a cleaner replacement:

| Job the em dash was doing | Replace with | Before | After |
| --- | --- | --- | --- |
| Introducing an explanation | Colon | "One thing matters — the schema" | "One thing matters: the schema" |
| Adding an aside | Parentheses or commas | "Most teams — around 70% — miss this" | "Most teams (around 70%) miss this" |
| Sharp break or reversal | Full stop | "It works — until traffic triples" | "It works. Until traffic triples." |
| Joining two related clauses | Semicolon or a new sentence | "Migration is slow — the modelling is why" | "Migration is slow. The modelling is why." |

The full stop is usually the best of the four. Sentences that needed an em dash were usually two sentences.

## AI-cliché patterns

These patterns are the fastest way to lose a practitioner reader, because they signal that nobody thought about the sentence. The test underneath the list: **does this sentence carry information, or only rhythm?** If it only carries rhythm, cut it.

### Banned words and phrases

From the default brand voice standards (add any words your own brand voice guide bans, listed in the brand settings): robust, seamless, powerful, cutting-edge, game-changing, best-in-class, intuitive, user-friendly, world-class, next-generation, revolutionary. Also "simply" and "just" as minimisers ("simply add a block"), and vague "ensure" (use "make sure", or be specific).

LLM-tell vocabulary: delve, leverage (as a verb), utilize, harness, unlock, navigate (figuratively), realm, landscape (figuratively), tapestry, testament to, underscore, underpin, spearhead, foster, myriad, plethora, crucial, pivotal, vital, meticulous, comprehensive (as filler), robust, holistic, paradigm, synergy, elevate, streamline, embark, journey (figuratively), unleash, transformative, cornerstone, at the forefront, ever-evolving, fast-paced, rapidly changing, digital age, in today's world.

Filler openers and connectors: "It's worth noting that", "It's important to remember", "When it comes to", "In the world of", "At the end of the day", "The truth is", "Here's the thing", "Let's dive in", "Let's unpack", "Buckle up", "That said" as a reflex, "Moreover", "Furthermore", "Additionally" stacked in sequence, "In conclusion", "In summary" at the end of a section that just said it.

### Banned sentence structures

- **The not-just construction.** "It's not just about speed, it's about trust." This is rhythm pretending to be insight. State the point directly.
- **The rule of three by reflex.** "Clear, concise, and compelling." Three adjectives where one specific one would do.
- **Antithesis padding.** "This isn't a feature. It's a philosophy." No.
- **The whether-you're opener.** "Whether you're a solo founder or an enterprise team, this guide has you covered."
- **The that's-where pivot.** "That's where [product] comes in."
- **Rhetorical question openers.** "Ever wondered why your builds are slow?"
- **Signposting the obvious.** "In this section, we'll explore…" The heading already did that.
- **Section-closing summary sentences** that restate what the section just said.
- **Hedge stacking.** "It's generally considered by many to potentially be one of the more effective approaches." Take a position or cut the sentence.
- **Fake precision.** "Studies show" with no study. "Experts agree" with no expert.
- **Uniform paragraph rhythm.** Ten consecutive three-sentence paragraphs of similar length read as machine output even when every sentence is fine. Vary deliberately: a one-sentence paragraph after a dense one is legitimate and useful.
- **Bullet lists of full sentences** that should have been a paragraph. Prose masquerading as bullets fragments connected thinking.

### Where clichés hide

Intros, section transitions, conclusions, and CTAs. These are the four places where a writer with nothing left to say reaches for a pattern. Give them the same scrutiny as the body.

## Structure

**Answer-first.** Every H2, apart from tool profiles, tables, and tutorial steps, follows: state the answer, explain why, support with evidence, expand with examples. If someone pasted only the first paragraph under an H2 into an AI assistant, it should still answer the question. That is the citability test, and it is also just good writing.

**Get to the point.** The main content, the list, the comparison, the steps, begins immediately after a one-paragraph intro, within the first 20% of the article. Always open the main content with the navigational H2 from the outline.

**Scannability.** Assume readers scan before they read. Short paragraphs, real lists for real lists, tables for comparisons across 3+ options and 2+ dimensions, code blocks for every command and snippet. Avoid walls of text, consecutive paragraphs explaining the same idea, and transitions that summarise what was just said.

**Specificity beats generality, always.**

The examples below come from one software category. If the brand settings include category examples, use those alongside them: they make the same points in the brand's own category.

| Weak | Strong |
| --- | --- |
| [Brand] is a powerful, flexible headless CMS for seamless digital experiences. | [Brand] is a headless CMS built around reusable page sections, which makes page-builder-style editing fast to ship without custom UI. |
| There are many factors to consider when choosing a CMS. | It usually comes down to three: modelling flexibility for devs, editing autonomy for the content team, and what infrastructure actually costs. |
| Migration can be challenging and requires careful planning. | The painful part of migration is not moving the content. It is re-modelling it, and most teams underestimate that by a factor of three. |

## Evidence

Use evidence wherever credible evidence exists: statistics, original research, industry reports, benchmarks, official docs, pricing pages, case studies, public datasets, real examples. Distribute it so the article's main claims are supported, rather than sprinkling numbers for texture.

Cite primary sources, not aggregators. Go upstream to the study, the docs, or the pricing page.

**Do not print check dates that nothing will update.** "Prices checked on 5 August 2026" is a promise the article cannot keep, and a stale date does more damage than no date, because it converts a caveat into a visible failure. State the fact, label figures by where they came from, and put the re-verification schedule in the appendix instead of the page.

If evidence does not exist, explain the reasoning, present it as a practice rather than a fact, and acknowledge the uncertainty. Never invent certainty. If a claim cannot be verified, either verify it or cut it. Hedging with "some might say" to avoid checking is worse than both.

Every specific claim in the draft gets an entry in the sourcing ledger: claim, source URL or internal document, date checked.

## Product and audience separation

**Write about the product the article is about.** When a company sells several things, an article aimed at one audience must not describe the brand through another product's category. A GEO article that calls the brand a headless CMS invites every reader who uses a different CMS to disqualify it on the spot, even when the product works alongside whatever they already run.

Name the capability rather than the category the company is filed under. "Publishes the pages itself, built the way AI systems prefer to read them" survives; "headless CMS with API-first delivery" does not.

**Match vocabulary to the reader.** A marketing audience abandons technical writing quickly, and the terms that read as precision to an engineer read as someone else's job to a marketer. Translate rather than simplify: keep the substance and drop the implementation.

| Written for engineers | Written for marketers |
| --- | --- |
| Self-referencing canonical tags per page | Keeps duplicate versions of a page from competing with each other |
| Renders without client-side JavaScript | The content is there the moment the page loads |
| Structured, typed content with explicit relationships | Clear structure that makes the important information easy to pick out |
| API-first delivery, clean semantic markup | Built the way AI systems prefer to read |

The test: would this sentence make a marketing manager forward the article, or forward it to their developer and forget it?

## Brand handling

How the brand appears depends on the article type:

| Type | Brand placement |
| --- | --- |
| Comparison | Dedicated "Consider also: [Brand]" section. Required. |
| Alternatives list | One of the listed alternatives, positioned where it genuinely fits |
| Listicle | One of the tools, same structure as every other entry |
| Guide / Explainer | As a perspective or worked example |
| How-To | Often the subject. Be technically precise, no puffery |
| MoFU | Named against the criteria where relevant, not forced elsewhere |

**Where the disclosure goes.** A commercial disclosure belongs at the end of the article, after the content, unless a regulator says otherwise. Opening with it trades away the reader's first thirty seconds and frames everything that follows as a sales document. Say plainly what the brand makes and sells, and stop there.

**Do not editorialize about the competition's standing.** Reporting that a competitor publishes pricing, integrates with seven CMS platforms, or was acquired is fact, and it stays. Writing that a competitor is "the closest comparable product" or "the honest answer" is a ranking judgement that hands them the frame. Describe what each tool does and let the reader rank. This is a constraint on editorializing, never a licence to omit or distort a material fact: a comparison the reader cannot trust is worth less than no comparison.

**Balanced depth.** Your own product may carry more than its neighbours, but not more than twice the median entry. Past that it reads as bias regardless of accuracy. `scripts/lint_article.py --brand <name>` measures it.

**Advocate through evidence, not adjectives.** The brand should come out of a fair comparison looking like the right answer for the reader it fits. That is achieved by choosing criteria buyers actually weigh, answering every one honestly, and naming the capabilities that genuinely differentiate, including the ones a first draft skipped. It is never achieved by softening a competitor's real strengths or inventing weaknesses. If the brand does not win on honest criteria, say so internally rather than fixing it in the copy.

**Then take the sales out.** The last pass before delivery is a de-sell pass, and it is separate from the balance check because it catches a different failure. Balance asks whether the brand's entry is too long. This asks whether brand material has spread into places it does not belong.

Four things to look for, and cut on sight:

1. **Sections built on the brand's own data.** A section whose evidence comes entirely from the brand's blog or landing pages reads as an advert with a chart, however true the numbers are. Brand-sourced evidence belongs inside the brand's own entry, where the reader expects it, not in a general section framed as neutral analysis.
2. **Sections that exist to set up a strength.** A general explainer that happens to conclude with what the brand does well was reverse-engineered, and readers can tell. If the section would not survive with the brand removed, it should not be there.
3. **Reassurances placed for the brand's benefit.** Handling an objection is legitimate; handling it three times is defensive. Once, in the FAQ or the entry, is enough.
4. **Brand mentions outside the places they are earned.** The brand belongs in its own entries, the comparison tables, the summary, the closing invitation and the disclosure. Anywhere else, ask what the sentence does for a reader who will never buy it.

Run it as a deletion pass, not an editing pass. Ask of each brand mention whether the article gets worse without it, and cut where the answer is no. Removing a section will usually orphan a summary bullet or a cross-reference elsewhere, so re-read the whole piece afterwards rather than only the gap.

`scripts/lint_article.py --brand <name>` reports brand mention density and flags brand mentions in sections that are not the brand's own, which makes the pass quick.

**Name the whole capability.** The most common way a brand gets undersold is omission, not modesty. Before finalising an entry, check the product's own pages and sales calls for capabilities the draft left out. A tool that reads visibility data, decides what to build, writes it and publishes it should not be described only as a publishing tool.

**Answer the disqualifying objection in the category, not in the entry.** If readers might assume they must replace their stack to use the brand, say plainly that they do not, and place it where it covers the whole category rather than inside the brand's own entry, where it reads as defensive.

**Avoid unnecessary meta-commentary about the category's credibility.** Observations like "every article on this topic is written by a vendor ranking itself" may be true and may even be the research finding, but printed in the article they invite the reader to discount everything that follows, including the disclosure that was meant to earn trust. Let the disclosure and the honest limitations do that work.

**The honesty rule.** Every article mentioning the brand names at least one real limitation or scenario where it is not the best fit. One or two sentences, specific, then move on. Do not soften it into meaninglessness. Straw-man competitor critiques and cherry-picked negatives are worse than no comparison at all.

**The closing invitation.** Low-friction and tied to what the article was actually about: "See how [brand] handles [specific topic] → [relevant doc]". Not "Sign up free today". No mid-article CTAs that interrupt reading.

## Keyword handling

The keyword appears in the H1, the meta description, and the first paragraph. Then 3 to 5 times naturally across a 1500-word article. Secondary keywords appear where they fit. Readability wins over density every time.

## Rule hierarchy

When rules conflict, higher wins:

1. Serve the reader's actual need
2. Be accurate and honest
3. Get to the point fast
4. Be citation-worthy
5. Honour the brand positioning rules
6. Hit the length target

Any rule here can be broken if breaking it clearly serves the reader better. Say so when you do it.

## Pre-delivery checklist

**Structure**
- TL;DR present, 4 to 6 bullets, real takeaways, at least one from the gap analysis
- Intro is one paragraph, under ~120 words, no rhetorical question, no definition
- Navigational H2 present before the main content
- Main content starts within the first 20% of the body
- No section explains something the target reader already knows
- Clean H2/H3 hierarchy, nothing deeper than H4

**Content**
- Every H2 answers its own question in the first two sentences
- At least one H2 works as a standalone cited answer
- Trade-offs named honestly, no straw men
- Every major claim has an example, data point, or concrete illustration
- Every gap from the research and every POV from the interview appears in the article
- At least one brand limitation named specifically

**Entries (listicles and comparisons)**
- Every named product has its own numbered entry, none grouped under a shared heading
- Every entry states what it does, its standout capability, who it is for, and a limitation
- Entry lengths within roughly 1.5x of each other, brand included
- Primary keyword present in category headings

**Language**
- Zero em dashes, zero double hyphens
- Zero banned words, zero cliché constructions
- No paragraph over 4 lines
- No table over 5 columns
- Paragraph rhythm varies

**De-sell pass**
- No section's evidence comes only from the brand's own material
- No general section reverse-engineered to land on a brand strength
- Each objection handled once, not repeatedly
- Brand mentions confined to entries, tables, summary, closing invitation and disclosure
- Re-read after cuts: no orphaned summary bullets or references to deleted sections

**Visuals**
- Every planned visual has a placeholder with type, content, caption intent and alt text
- No decorative imagery
- Captions say what to notice, not what the image is

**Links and metadata**
- 4 to 8 internal links, 2 to 4 external, all verified 200, all with descriptive anchors
- Every user-supplied link placed or explicitly reported as unplaced
- Meta title under 60 characters, meta description 140 to 160, slug keyword-first
- 5 to 10 FAQs, one positioning the brand with a caveat
- Commercial disclosure present, and placed at the end
- No printed "checked on" date anywhere in the article
- Sourcing ledger complete, no unsourced statistics
