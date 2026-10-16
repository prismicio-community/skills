# Plan methodology

Read this in full before Step 5. It carries the title-derivation rule that defines this skill, the portfolio rules, the priority rubric, and the cannibalization policy.

## Contents
- Title derivation (the core rule)
- The angle
- Portfolio rules
- The evidence ladder
- Priority rubric
- Cannibalization policy
- Worked examples

## Title derivation (the core rule)

The plan builds the brand's version of what already gets retrieved. So **the phrasing is copied from the evidence; only the substance is new.**

Every content row must record two things:

- **Title evidence** — the exact phrasing found in the data.
- **Title evidence source** — which of the four legal origins it came from:
  1. A cited page's title (citation layer)
  2. A ranking page's title (SERP layer)
  3. A fan-out query
  4. A tracked prompt

If a proposed title cannot be traced to one of these, the row does not get created. This is not a formality — untraceable titles are how a plan drifts from "what gets retrieved" to "what sounded good", which is the failure mode this skill exists to prevent.

**Deriving, not copying verbatim.** The working title should carry the retrieved phrasing while being the brand's own page, not a duplicate headline. Legal derivations:

- Keep the query's noun phrase, change the frame: evidence `"I tested the 7 best AEO tools"` → `"The 9 AEO tools we tested for a headless CMS stack"`.
- Convert a question prompt into its statement form: prompt `"What tools help create content that both Google and ChatGPT will surface?"` → `"Tools that get content surfaced by both Google and ChatGPT"`.
- Add the scope qualifier that distinguishes it from a neighbouring row: `"Best GEO tools"` → `"Best GEO tools for the full content stack (not just monitoring)"`.

Illegal: inventing a phrasing nobody searches ("The modern content velocity playbook"), or drifting to the brand's internal vocabulary when the evidence uses different words.

**Phrasing and clusters.** Rows come from content clusters (SKILL.md Step 3), which group pages by what they say, not by how they're phrased. Two phrasings whose pages tell a reader the same thing are one cluster and one row; the title keeps the wording the evidence uses most. Two phrasings whose pages answer different questions are separate clusters and separate rows, each with a guardrail naming what it excludes.

## The angle

The angle is the reason an assistant cites this page rather than the incumbent. It is a judgment, and it must rest on something real.

**Before writing any angle, read the incumbents.** Read the top two or three sources for that intent: the AI visibility tool's indexed copy where it has one (Peec AI: `get_url_content`), otherwise a live fetch. The differentiator must be a gap you actually observed, not one you assumed. "They don't cover pricing" is only usable if you checked and they don't.

Differentiators that work, roughly in order of strength:

- **Original testing or data** — "we tested N tools", "we analyzed N pages". The most-cited format in nearly every dataset.
- **A categorization scheme** the incumbents lack — turning a flat list into a decision structure.
- **Honest pricing** — real numbers in a table, including where the brand is more expensive.
- **A correction** — incumbents carrying stale or wrong facts about the category.
- **Scope discipline** — covering exactly one phrasing properly where incumbents cover it partially inside a broader page.

Every angle names **which brand asset it depends on**. If the brand does not have that asset yet, the row says so explicitly ("requires a tool test the brand has not run — flag before scheduling"), rather than assuming it exists. This is what keeps briefs honest: a brief may *request* a number, never *supply* one.

**Honesty as strategy.** Briefs direct genuine inclusion of competitors, real limitations, and "when you don't need us" sections. Assistants retrieve balanced content for evaluative queries; puffery loses citations. This is not a values note bolted onto a tactic — it is the tactic.

## Portfolio rules

- **Technical fixes first**, if the audit found any. A noindex page makes every content row downstream of it worthless.
- **Portfolio mix follows the observed page-type distribution.** Do not impose a preferred mix. If the evidence says listicles, plan listicles.
- **Vendor-owned pages per capability phrasing**, not per product. Vendors get cited for indexable pages describing a capability in the words of the query. Derive the phrasing list from the prompts in scope plus how cited vendor pages title themselves.
- **Scope solution pages by audience × job**, never audience alone. An audience-only page forces the brand to represent its whole product line and dilutes; offer a product-led playbook article plus a case study instead.
- **Free tools are citation magnets.** If the brand has one or could build one, plan it with methodology content around it.
- **Comparisons** — both brand-vs-competitor and neutral third-party X-vs-Y where the brand credibly referees.
- **One hub page** to concentrate internal links, when the plan has enough rows to warrant it.
- **Evidence assets follow the ladder** (see the section below). Plan the executable rung alongside the blocked one; never plan only a rung the brand cannot start.
- **Cover every prompt in scope.** Prompts with weak incumbents are the cheapest wins; rank their topics up on winnability (see the priority rubric).
- **UGC alone never becomes a content row.** A UGC page can join a content cluster as a demand signal when it asks or answers the same thing, but a cluster made only of UGC goes to the Threads and Off-site tabs, not the content plan.

## The evidence ladder

Receipts win citations, and receipts have a cost gradient. Three rungs, cheapest first:

1. **Synthesis of what others published.** Cross-case analysis of first-person accounts already present in the evidence layers. Costs editorial time only.
2. **Analysis of data the brand already holds.** Support tickets, migration logs, usage patterns, past client work. No new collection.
3. **Original testing or new collection.** A controlled test, a survey, a benchmark. A research commitment with a budget and a calendar.

**The rule: never plan only rung 3.** When the angle needs an asset the brand does not have, the dependency flag is where the work starts, not where it ends. Ask what version of the same intent is executable this month, and plan both rows. The executable row takes the priority; the blocked row drops a level and gains the executable row as a prerequisite.

Flagging a blockage and stopping is the failure mode this section exists to prevent. It produces a plan whose most prominent row is the one nobody can start, and it silently transfers the "so what do we do now?" decision back to the user.

**Sequencing is the actual argument, not a consolation.** Rung 1 produces the hypotheses rung 3 tests. A synthesis that finds eleven of twelve teams ended up with exactly one person able to publish tells you precisely what the controlled test should measure and which variants are worth building. Run in that order the expensive rung gets cheaper and sharper, so write the handoff into both briefs: the synthesis ends with "what we would test next", and the test says it must not be briefed until the synthesis has shipped.

### What makes a rung-1 row legitimate

A synthesis earns its row through **comparison across cases**, never through summarising them in sequence. The differentiator is the pattern no single author can see, because each of them ran n=1 and reports their own outcome as the answer. If reading the corpus turns up no cross-case pattern, there is no row — say so rather than shipping a list of links.

Three requirements, all of which belong in the brief:

- **Hunt the survivorship problem.** Published accounts are written by people who finished and were pleased; nobody blogs the abandoned migration. Look in the same dataset for the counterweight — reversal threads, "is this even possible" questions, forum posts asking how to undo it. UGC is usually where it lives. A synthesis without this section is a marketing artifact and reads as one.
- **Sourcing discipline.** Paraphrase and analyse, link out to every source, keep direct quotation short and attributed. Attribute each figure in a comparison table to the author who published it, and never average self-reported numbers from different source cases into a finding of your own.
- **The sources should want the association.** This is an ethical floor and also the practical one: a rung-1 row is usually the strongest outreach asset in the plan, and inclusion in a cross-case study is a far better pitch than a cold ask. Cross-reference it in the Off-site tab and count the work once.

### Bookkeeping

The two rows are separate rows with hard guardrails, not one row with a caveat. They need distinct `title_evidence` — the build script rejects two rows targeting the same phrasing — which is a useful forcing function: each row has to name the specific incumbent it displaces rather than both gesturing at the same one. Draw the guardrails explicitly: the synthesis reports what other people did, the test reports the brand's own results, and neither carries the decision framework if a separate row already owns it.

## Priority rubric

Score each cluster on five things, then assign a priority. List every cluster; priority orders the list, it never removes a row.

1. **Evidence strength** — number of member pages, total retrievals and citations, SERP weight.
2. **Prompt match** — does the topic answer a tracked prompt in scope directly, or only touch it?
3. **Product fit** — High (the brand's category and audience), Medium (adjacent, a mention could still sell), Low (outside the category).
4. **Winnability** — incumbent strength from the combined-layer analysis, and whether the brand already has a page.
5. **Readiness** — whether the brand has the asset the angle needs.

- **P0** — strong evidence, direct prompt match, High fit, startable now; or a prerequisite fix. A topic for a prompt with thin, weak incumbents also qualifies when the match is direct and the fit is High, because it's the cheapest win available. Usually 10–15% of rows. A plan where everything is P0 prioritizes nothing.
- **P1** — strong on most of the five, or High fit with moderate evidence.
- **P2** — everything else, including every Low-fit topic.

## Cannibalization policy

Every row states what it must **not** cover and which row number to link instead. No two rows target the same phrasing. Cross-references are by row number and must all resolve after numbering is final — the build script validates this and fails loudly on a broken reference.

Across runs (multi-prompt accumulation), the same rule applies: a new prompt's intent that matches an existing row's phrasing joins that row rather than creating a second one.

## Worked examples

**Good row**

> **#7 · P1 · Update · Comparison**
> Title: "[Brand] vs [Competitor] for AI-search visibility"
> Title evidence: `"[Competitor] vs [Brand]: Which Is Best?"` — cited page title (citation layer)
> URL: existing `/compare/[competitor]` (fetched; currently 600 words, no AI-search section, last updated 2024)
> Prompts: "What platforms help B2B SaaS grow organic and AI search traffic?"
> Sources to beat: [competitor].com/comparisons/[brand] (18 retrievals, citation layer); g2.com/compare/… (5 queries, w12, SERP layer)
> Angle: incumbent comparison is vendor-owned and omits AI-search behaviour entirely (verified — read the page). Differentiator: a section comparing how each product's default output renders for crawlers, with real HTML samples. **Depends on:** the crawler-rendering test — brand has not run this yet, flag before scheduling.
> Brief (diff): keep the feature table; add an "AI search and crawler rendering" H2 with the samples; rewrite the intro to lead with the comparison question verbatim; add honest "when [Competitor] is the better fit" section.
> Guardrail: does not cover the category in general — that is row #3. Does not cover pricing depth — row #11.

**Bad row (and why)**

> #7 · P0 · Create · Article — "The Content Velocity Playbook for Modern Teams"
> Sources to beat: various competitor blogs
> Brief: write a comprehensive guide showing why our approach is better. Include the 47% improvement figure.

Four failures: the title traces to no phrasing in the evidence; "various competitor blogs" names no URL and no metric; "why our approach is better" is not a differentiator; and the 47% figure was invented rather than requested from the brand.
