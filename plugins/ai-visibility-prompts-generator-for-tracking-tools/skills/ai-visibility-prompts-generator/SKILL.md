---
name: ai-visibility-prompts-generator
description: "Generate the prompts to track in an AI visibility tool (Peec AI, Profound, Otterly and similar): a tagged library of buyer prompts for one product, split equally across Unaware, Problem-Aware, Solution-Aware and Category-Aware stages, category-relevant only. Use for 'what prompts should we track', 'build a prompt library', 'would ChatGPT recommend us', or to audit an existing tracked-prompt set."
---

# AI Visibility Prompts Generator

Produce a tightly scoped set of prompts to load into an AI visibility tracking tool. The prompts cover the real buyer journey for one product category, from people who don't yet know they have a problem to people shopping the category by name. Every prompt must be **highly relevant**: when an AI assistant answers it, the answer naturally lands on the product's own category.

You are modelling real buyer conversations, written by buyers who have **never heard of the product, never visited its website, and don't know where the vendor is heading**. You are not generating SEO keywords, marketing messaging, or prompts designed to make the product show up.

## The buyer only knows their reality

This is the rule every other rule serves. Before writing any prompt, picture the person typing it.

**They know:** their stack, their team, the tools they already use, the thing that broke or slowed them down this week, what a colleague or a forum thread told them, and — at later stages — the plain name of the category.

**They don't know:** the vendor's positioning, its differentiators, its feature names, the angle it's pushing this quarter, how it frames the problem, or the vocabulary vendors in the category use to describe themselves.

So a prompt is written from **their situation, in their words**. If the only way someone would phrase a prompt that way is by having absorbed a vendor's pitch, it measures "does AI recommend us when someone describes us" — a false positive that flatters the brand and tells you nothing.

The user's request can carry positioning too. "Focus on our AI insights feature" or "we're moving upmarket" defines **which buyer situations to cover**, not **how the prompts are phrased or which angle they take**. Translate the focus into situations that exist in buyers' lives today ("every Monday I spend two hours building a report to explain why our numbers moved") and write those. Never write the vendor's direction back as a question ("Which analytics platform has AI-generated insights?" is the vendor talking; "Is there a tool that just tells me why our numbers changed this week without me building reports?" is a buyer).

## Why the stages matter

Brands that win category-named prompts ("best product analytics tool for a startup") often lose problem-described prompts ("tool to see why users drop off during onboarding"). On category prompts, AI answers default to the entrenched leaders. On problem prompts, they reward whoever best answers the problem, and that is often a different brand. A library weighted toward category prompts measures where incumbents already win and overstates how the brand is doing. A library with an equal spread across stages shows where the brand wins and where it is losing earlier in the journey.

## The four failure modes this skill exists to prevent

Every hard rule below traces back to one of these.

1. **Positioning contamination (false positives).** Prompts that describe the product's exact shape — its differentiators, its framing, its strategic angle — restated as questions. They come from reading the product's page, from the user's brief, or from knowing the brand already. They make the brand look visible where real buyers would never ask that way.
2. **Vendor-jargon drift.** Prompts phrased in the category's own marketing vocabulary ("warehouse-native", "behavioural data platform", "composable stack", "unified customer view") instead of the words buyers use. These usually come from doing buyer research on vendor sites. Swapping the category name for a vendor euphemism is not "plain words" — it's the category label in disguise.
3. **Category drift.** Prompts that sound plausible but get answered by a different category of tool (a product analytics library full of "best survey tool" or "best BI dashboard" prompts). This skill tracks **one category**. There is no adjacent tier.
4. **Stage imbalance.** Libraries naturally skew toward Category-Aware head prompts because they are easiest to write. The equal-split quota exists to force pain-phrased, early-stage prompts in.

## Core principles

- Buyer research always takes priority over product research, and buyer language always beats vendor language.
- The product page may be read early (Phase 0) **only** to scope the run and to build the Quarantine List. It informs *which* buying decisions are in scope, never *how* a prompt is worded.
- The buyer journey defines the prompts. The product never defines the prompts.
- **Every prompt must pass the category check**: when an AI assistant answers it, the tools it names (or, for Unaware prompts, the solutions and sources it points to) belong to the scoped category.
- **Every prompt must pass the outsider test**: a buyer using any incumbent in the category — or none — could plausibly type it, unchanged, without ever having heard of the product.
- Never use the product's terms, feature names, differentiators, or positioning claims, and never use vendor-category jargon buyers only learn from vendor sites. The category's plain name (the one buyers actually say, e.g. "product analytics tool") is fine in Solution-Aware and Category-Aware prompts.

## The four buyer stages

Every prompt gets exactly one stage tag. Use these definitions strictly; most mis-tagging comes from blurring Problem-Aware and Solution-Aware.

| Stage | What the buyer knows | What they ask | Example (product analytics) |
| --- | --- | --- | --- |
| **Unaware** | They see a symptom or have a goal, but don't frame it as a problem a tool could solve | Why something is happening, how to do or measure something | "How do I figure out why so many trial users never come back after day one?" |
| **Problem-Aware** | They know the specific problem and are open to tools, but don't know what kind of solution exists | Describes the pain, asks for tools or help | "Our signups look fine but users drop off during onboarding — what tools show where they get stuck?" |
| **Solution-Aware** | They know the *type* of solution they want and may know its plain name, but aren't shopping vendors yet | Describes what they want the tool to do, in their words; may use the plain category name | "Is there software that tracks every click in our app so we can see the steps people take before they churn?" / "Do I need a product analytics tool for this or can Google Analytics do it?" |
| **Category-Aware** | They know the category by name and are shopping it | Best X, X for situation Y, how to choose an X | "What's the best product analytics tool for a B2B SaaS startup?" |

Never generate Brand-Aware, Competitor-Aware, or Feature-Aware prompts (no vendor names, no "X vs Y", no "X alternatives", no named features). Naming tools the buyer already uses that are *not* category vendors (their framework, their AI assistant, their old platform) is fine and often makes a prompt more real.

**Unaware prompts usually get advice back, not a product shortlist.** That's expected: this is where brands become the natural answer inside advice, and where problem-answering content earns citations. They still must pass the category check: the natural answer should lead to the scoped category. If the honest answer is "hire someone" or "change your process" with no route to the category, the prompt is out. Prompts in the other three stages must be **recommendation-eliciting**: a typical AI assistant answers with a list of named products.

## Tags

Every prompt carries **at least two tags**: one stage tag (required, exactly one) plus at least one more from the tag vocabulary. Aim for two or three non-stage tags where they genuinely apply; never add a tag just to hit a number.

The tag vocabulary is built in Phase 2 from buyer research, as a small controlled list so tags can be reused for filtering and reporting, and imported as tags or tag groups into the tracking tool. Default tag groups:

| Group | What it captures | Example values (product analytics) |
| --- | --- | --- |
| `stage` (required) | Buyer stage, from the four above | `unaware`, `problem-aware`, `solution-aware`, `category-aware` |
| `persona` | Who is typically asking | `product-manager`, `founder`, `growth-marketer`, `data-engineer` |
| `job` | The underlying problem or job the prompt is about | `onboarding-dropoff`, `churn`, `feature-adoption`, `self-serve-reporting` |
| `trigger` | What prompted the search, when buyer research shows a distinct one | `new-product-launch`, `tool-outgrown`, `data-team-bottleneck`, `cost-cutting` |
| `context` | A buying context that changes the shortlist (only when it does) | `startup`, `enterprise`, `regulated-industry`, `open-source` |

Rules: lowercase kebab-case values; no more than about six values per group; every value used at least once or dropped; no product, vendor, or feature names as tags. Add a group only if buyer research shows it changes which tools get recommended or which content would win.

## Inputs

- **Product URL(s)** — required. Read in Phase 0 for scope and the Quarantine List only. If none is given, ask for the page that describes the product to track.
- **The product's category** — confirmed with the user in Phase 0.
- **Optional context** from the user (focus area, product name, positioning). Treat any positioning or direction in it exactly like the product page: it goes on the Quarantine List.
- **Library size** — 20 (5 per stage) by default. If the user asks for more or no cap, keep the split equal across stages and let the stage with the fewest passing prompts set the per-stage count.

## Phase map

| Phase | What happens | Gate |
| --- | --- | --- |
| 0 | Read the product page; write the Category Statement and the Quarantine List; confirm the Category Statement with the user | Page informs scope only |
| 1 | Category research: definition, synonyms, incumbents | Product not searched |
| 2 | Buyer research from primary buyer sources; build the Buyer Phrase Bank and tag vocabulary | Primary sources only for language |
| 3 | Buyer journey mapping across the four stages | Situations come from the Phrase Bank |
| 4 | Draft the prompt universe (at least 10 per stage), tagged, each traced to a buyer situation; run the language checks | **Freeze**: draft written out verbatim and immutable from here |
| 5 | Category check on every draft prompt, then optimise to an equal split | Product not consulted |
| 6 | Product fit check: confirm each prompt is a buying decision the scoped product genuinely serves | No rewriting, no new prompts |
| 7 | Final validation, including the outsider and quarantine tests | Checklist in `references/validation.md` |

**Final outcome:** the AI visibility prompt library (equal per stage, each prompt with at least two tags), plus the category statement, tag vocabulary, optimisation report, tracking notes, an import-ready list, and the validation statement.

## Workflow

Run the phases strictly in order.

### Phase 0 — Scope, Quarantine List and Category Statement

Read the product URL(s) and any context the user gave. Produce two things.

**Category Statement** (confirm with the user before Phase 1):

- **Scoped product:** the specific offering the URLs describe — never the vendor's wider brand or other product lines.
- **Category:** one category, at most two if the product genuinely competes in both on equal terms. Use the name buyers use, not the vendor's coined label.
- **In-scope buying situations:** the jobs this product is bought for, described as buyer situations ("a product team can't see where new users get stuck"), not as features.

**Quarantine List** (internal, shown in the deliverable): every term, phrase, feature name, differentiator, claim, and strategic angle from the page and the user's brief — e.g. the product's feature names, its headline promise, its "unlike others, we…" claims, the direction the vendor is moving in. Add the category's vendor jargon you notice (terms vendors use to describe the category that buyers don't). Nothing on this list may appear in a prompt or be restated as one; Phase 4 and Phase 7 scan against it.

Close the page after this phase. Don't re-open it before Phase 6. Show the Category Statement to the user and ask them to confirm or correct it. If the user isn't there to answer, take the most reasonable reading, state it at the top of the deliverable, and carry on. Re-read the Category Statement at the start of Phases 5 and 6.

### Phase 1 — Category research

Research the confirmed category with web search. Do not search for the product by name. Output:

- **Category definition** — what tools in this category do, in one or two buyer-language sentences.
- **Category synonyms** — names buyers actually use for it (check these against buyer sources, not vendor pages).
- **Incumbent list** — 8–15 tools that AI answers and "best X" lists commonly name in this category. A measuring tool for the category check only: never put these names into prompts.
- **Category boundary** — the neighbouring categories buyers confuse it with, and how to tell them apart in an AI answer. Listed so the category check can reject them.

Vendor content is fine here, because this phase is about what the category *is*. It must not feed prompt wording.

### Phase 2 — Buyer research and the Buyer Phrase Bank

Ignore the product. Research personas, problems, goals, jobs-to-be-done, buying triggers and blockers, and above all the words buyers use.

**Sources for language: primary buyer sources only** — Reddit and community forums, Q&A sites, public Slack/Discord community posts, practitioner blogs written by people doing the job (not selling a tool), review-site reviewer text, conference talk titles from practitioners. Vendor blogs, docs, landing pages, comparison pages and vendor-written "guides" are **not** buyer sources, however useful they are for Phase 1. If you can't find enough primary sources, say so in the deliverable rather than filling the gap with vendor phrasing.

Output:

- **Buyer Phrase Bank** — 20–40 short entries, each a real buyer situation or phrasing with its source: what happened, how they described it, what they asked. Paraphrase rather than copy long passages.
- **Tag vocabulary** (see "Tags"): the persona, job, trigger, and context values drawn from this research.

### Phase 3 — Buyer journey mapping

Map journeys across the four stages: **Unaware → Problem-Aware → Solution-Aware → Category-Aware**. Start every journey from a Phrase Bank situation, then ask how that same buyer would phrase it at each stage. This is the most reliable way to get genuine early-stage prompts rather than category prompts in disguise, and it keeps each prompt anchored in a real situation rather than in what the product does.

### Phase 4 — Draft the prompt universe and FREEZE it

Generate at least **10 prompts per stage**. Every draft prompt must:

- trace to a Phrase Bank situation (record which one)
- sound like something a buyer would genuinely type into an AI assistant — conversational, natural, first person where fitting, in the words the Phrase Bank shows buyers using
- represent a distinct buying decision or problem
- carry its stage tag plus at least one other tag from the vocabulary
- for Problem-Aware, Solution-Aware, and Category-Aware: be **recommendation-eliciting** ("what tools…", "is there software that…", "best … for…", "any recommendations for…")
- for Unaware: describe the symptom or goal without naming a solution type or the category

**Language checks (run on every draft prompt before freezing; rewrite or drop failures):**

1. **Quarantine scan** — no Quarantine List term, and no Quarantine List claim or angle restated in other words.
2. **Jargon scan** — no vendor-category jargon or disguised category label. Ask of every noun phrase: would a buyer who has never read a vendor website say this? Typical offenders: "platform", "solution", "API-first", "-native", "composable", "unified", "end-to-end", "orchestration", and any category-specific vendor terms you noted in Phase 0. In Solution- and Category-Aware prompts, the plain category name buyers use is allowed; euphemisms for it are not.
3. **Outsider test** — imagine three buyers: one using the category leader, one using a different incumbent, one using nothing. Would all three plausibly ask this, word for word? If the prompt only makes sense to someone who already wants *this product's* particular approach, it's tailor-made: rewrite from the buyer's situation or drop it.
4. **Requirement test** — does the prompt make the product's differentiator the buying requirement ("…that does X *and* Y", where X+Y is the pitch)? Real buyers ask for the outcome they need, not a vendor's feature combination.

Good (Problem-Aware): "Our signups look fine but users drop off during onboarding — what tools show where they get stuck?"
Poor (marketing-shaped): "Which platforms combine behavioural analytics with experimentation?"
Poor (vendor jargon): "Is there an event-driven analytics platform with a warehouse-native architecture?"
Poor (category drift): "What are the best survey tools for collecting user feedback?"

**Freeze rule:** Write out the complete draft universe verbatim, with tags and Phrase Bank references, before proceeding. Every later step — including revisions the user asks for after seeing results — may only select from and lightly reword prompts in this draft. **No new prompt may be introduced after Phase 6 begins, in this run or any follow-up turn.** If the user wants ground the draft doesn't cover, or rejects prompts as product-shaped, rerun Phases 2–4 (new Phrase Bank research, new drafts) rather than patching.

### Phase 5 — Category check, then optimisation

**Category check (every draft prompt).** For each prompt, look at what an AI or search answer actually recommends: run a web search for the prompt (or its closest natural query) and compare what comes back against the Phase 1 incumbent list and category boundary.

- **Pass** — most named tools, or most cited vendor pages, belong to the scoped category. For Unaware prompts: the answer routes to the category's tools, methods, or category vendors' guides.
- **Fail** — the answer is dominated by a neighbouring category, or (for Unaware) never routes to the category at all. Remove and record the reason.
- **Borderline** — mixed results after one search. Exclude by default and list it under Borderline calls with the evidence, so the user can promote it.

Record a short evidence note for every kept prompt (the 2–4 tools or sources seen). Group searches efficiently; a quick check per prompt is enough.

**Optimisation.** Reduce the survivors to an **equal number per stage** (5 by default). If a stage has fewer survivors than needed, do not borrow from other stages: rerun Phases 3–4 for that stage only (from the Phrase Bank), then check again. Merge prompts only when they represent the same buying decision: would buyers expect different products? would different content be needed to win? would the recommendation set change? If yes, keep both. Within each stage, prefer spread across personas and jobs over variations of one job.

Remove wording variations, geographic variations, company-size variations (unless the `context` tag shows they change the shortlist), and feature variations.

Score each prompt internally on: category-check strength, buyer frequency, commercial intent, naturalness, and how contested the answer set looks.

### Phase 6 — Product fit check

Re-read the Category Statement, then use what you learned in Phase 0 (re-open the page if needed) **only** to confirm that every prompt is a buying decision the scoped product genuinely serves. For each prompt, imagine the AI's answer names the product: would the typical person asking treat it as a real candidate? Check against the mismatch patterns in `references/validation.md` (skill level, delivery model, buyer role, job scope, price band).

- **Keep** — the product genuinely belongs in the answer. Flag prompts where it does not *yet* appear in AI answers; that's the reality being measured, not a reason to drop the prompt.
- **Remove** — the product doesn't fit the asker, or the prompt belongs to the vendor's other product lines. Record the reason, then refill that stage from the frozen draft (prompts that passed the category check), never by writing new ones.

Watch for the opposite problem too: a prompt that fits the product *suspiciously* well — it reads like the page — goes back through the outsider test in Phase 7.

Do not rewrite prompts. Do not add prompts. Do not introduce product terminology.

### Phase 7 — Final validation

Run every prompt through `references/validation.md` (read it now), including the quarantine, jargon and outsider tests.

## Deliverables

Produce, in order:

1. **Category Statement and executive summary** — scoped product, confirmed category, in-scope buying situations, category definition, incumbent list, the main buyer personas and jobs, and the major discovery patterns per stage. Concise.
2. **Quarantine List and Buyer Phrase Bank** — the list used to scan prompts, and the buyer situations with sources.
3. **Tag vocabulary** — every tag group and value, with a one-line definition each.
4. **Optimisation report** — draft universe size per stage, language-check rewrites and drops, category-check removals (with the category that won instead), merges, Phase 6 removals, final count per stage, and a **Borderline calls** subsection with evidence for and against each.
5. **AI visibility prompt library** — one table, grouped by stage in journey order (Unaware → Problem-Aware → Solution-Aware → Category-Aware), sorted by tracking importance within each stage:

| # | Prompt | Stage | Tags | Buyer situation (Phrase Bank) | Category check (seen in answers) | Tracking importance (1–5) |

   - **Tags** lists the non-stage tags as `group:value`. Every row has at least one.
   - **Buyer situation** is the Phrase Bank entry the prompt came from, in one line. It ties the prompt to a real buyer and to the content that would win it.
   - **Category check** names the 2–4 tools or sources seen in answers.

6. **Import-ready list** — the final prompts in a single plain-text block, one per line as `prompt | tag, tag, tag` (stage tag first), so they can be pasted or uploaded into the tracking tool. If the user has a tracking tool connected that can create prompts and tags, offer to add them there; never add them without the user's go-ahead.
7. **Tracking notes** — short and practical:
   - Track **citations and mentions separately**. Being named in a paragraph is not the same as being cited with a link: the citation is what sends the click. A prompt where the product is mentioned but never cited is a content gap, not a win.
   - Report visibility **per stage**, not only in aggregate. Strong Category-Aware numbers next to weak Unaware and Problem-Aware numbers mean the brand wins where buyers already know the category and is absent earlier in the journey.
   - If the tracking tool supports tags or tag groups, import the tag vocabulary so the same cuts are available there.
8. **Validation statement** — the completed checklist from `references/validation.md`.

The prompt library is the primary output.

## Compatibility

- **Web search** is required for category research, buyer research and the category check.
- **A connected AI visibility tracking tool** is optional. Without one, the user pastes or uploads the import-ready list themselves.
