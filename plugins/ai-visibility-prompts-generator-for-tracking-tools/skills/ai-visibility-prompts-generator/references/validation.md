# Phase 7 — Final Validation Checklist

Run every prompt through all eight gates. A prompt must pass every gate to stay in the library. A removed prompt is replaced only from the frozen draft, within the same stage.

## Gate 1 — Quarantine test (decisive)

- Does the prompt contain any term from the Quarantine List: a product term, feature name, headline promise, differentiator, or the vendor's strategic angle?
- Does it restate a Quarantine List claim or angle in other words?

Either one fails the prompt. This includes positioning that arrived through the user's brief, not only through the product page.

## Gate 2 — Contamination and outsider test (decisive)

Positioning contamination is the most common and most damaging failure. For each prompt, ask:

- Could this prompt have been written by someone who has **never heard of the product**, never seen its website or marketing, and doesn't know where the vendor is heading?
- Does it presuppose the product's specific combination of capabilities — its differentiator or positioning narrative restated as a question?
- If the product's homepage headline were rewritten as a buyer question, would it resemble this prompt?
- **Outsider test:** would a buyer using the category leader, a buyer using a different incumbent, and a buyer using nothing all plausibly type this, word for word?

If a prompt describes the product's exact shape, it fails, even if it names no features and sounds conversational.

Examples (product: a content platform positioned as "monitoring isn't enough — we turn visibility gaps into published pages, grounded in your company's knowledge"):

- ❌ "Is there a platform that both monitors our AI visibility and helps us fix it in one place?" — the positioning narrative as a question
- ❌ "What AI content tools actually write from your company's own knowledge instead of generic web info?" — the differentiator as a question
- ✅ "We track our AI visibility but acting on the gaps is all manual — are there tools that actually create the content to fix them?" — starts from the buyer's observed pain

The test is *origin*: does the phrasing arise naturally from the buyer's situation, or only from having absorbed the vendor's pitch?

## Gate 3 — Jargon test

- Ask of every noun phrase: would a buyer who has never read a vendor website say this?
- Fail any vendor-category jargon or disguised category label ("platform", "solution", "API-first", "-native", "composable", "unified", "end-to-end", "orchestration", and the category-specific terms noted in Phase 0).
- The plain category name buyers use is allowed in Solution-Aware and Category-Aware prompts only. A euphemism for it is not.

## Gate 4 — Category check (decisive)

- Does the prompt have a recorded category-check result from Phase 5?
- Do the tools named in the answer (or, for Unaware prompts, the solutions and sources it points to) belong to the scoped category, per the Phase 1 incumbent list and category boundary?
- Is the prompt free of drift into a neighbouring category? There is no adjacent tier: a prompt answered mainly by another category fails, however natural it sounds.

Example (scoped category: product analytics):

- ❌ "What are the best survey tools for collecting user feedback?" — answered by survey tools
- ❌ "What's the best dashboard tool for our finance team?" — answered by BI tools
- ✅ "Our signups look fine but users drop off during onboarding — what tools show where they get stuck?" — answered by product analytics tools

## Gate 5 — Stage and format test

- Does the prompt carry exactly one stage tag, and does it match the stage definitions in SKILL.md? Check the common mix-ups: a prompt that describes the solution type is not Problem-Aware; a prompt that asks for vendors by category is Category-Aware; a prompt that asks for tools is not Unaware.
- Problem-Aware, Solution-Aware, Category-Aware: would a typical AI assistant answer with a **list of named products**? If not, fix the phrasing within the frozen draft's wording, or remove it.
- Unaware: does the prompt describe a symptom or goal without naming a solution type or the category, and does its answer still route to the category (Gate 4)?

## Gate 6 — Authenticity and requirement test

- Would a real buyer genuinely ask this, in these words, in an AI assistant conversation?
- Does it sound like marketing copy, a product page, or a feature list? (If yes → fail.)
- Does it make the product's differentiator the buying requirement ("…that does X *and* Y", where X+Y is the pitch)? (If yes → fail.)
- Does it trace to a Buyer Phrase Bank situation?

Examples to reject:

- ❌ "Which platforms combine AI content generation with human review before publishing?"
- ❌ "What software helps enterprise marketing teams publish personalised landing pages at scale?"

Buyer-language replacements:

- ✅ "We keep falling behind on content production. What tools do other companies use to scale SEO content?"
- ✅ "What tools help companies publish hundreds of landing pages without hiring dozens of writers?"

## Gate 7 — Product-scope test

- Does the prompt represent a buying decision for the **scoped product** (the offering on the analyzed URLs), per the Category Statement?
- If it represents a buying decision for the vendor's other product lines or flagship offering → remove and record the reason. The vendor's portfolio is not the product.

## Gate 8 — Genuine purchase option test

Imagine the AI's answer names the product. Who typically types this prompt, and what do they expect? Would they treat the product as a real candidate to evaluate and buy, sitting naturally next to the tools seen in the category check?

Mismatch patterns — each alone is disqualifying:

1. **Skill-level mismatch** — the asker expects a no-code or self-serve tool; the product needs developers (or the reverse).
2. **Delivery-model mismatch** — the asker expects a hosted app; the product is an API, framework, add-on, or service (or the reverse).
3. **Buyer-role mismatch** — the asker is an individual or hobbyist; the product is bought by teams through sales (or the reverse).
4. **Job-scope mismatch** — the asker wants an all-in-one suite; the product is a point solution (or the reverse).
5. **Price-band mismatch** — the phrasing implies a budget class the product isn't in ("free", "cheap", "for my side project" vs enterprise pricing).

If the call is still borderline after the evidence check, exclude the prompt, list it under Borderline calls with the evidence for and against, and let the user promote it.

## Tag checks

- ✓ Every prompt has exactly one `stage` tag and at least one other tag
- ✓ Every tag value comes from the tag vocabulary; no ad-hoc tags
- ✓ No tag names a product, vendor, or feature
- ✓ Every vocabulary value is used at least once, or was dropped from the vocabulary
- ✓ Tags describe the prompt accurately (a `persona` tag matches who would plausibly ask it)

## Library-level checks

Verify before returning results:

- ✓ An equal number of prompts per stage (5 Unaware, 5 Problem-Aware, 5 Solution-Aware, 5 Category-Aware by default)
- ✓ No stage was filled by borrowing prompts from another stage or by writing new prompts after the freeze
- ✓ Every prompt passed the quarantine, jargon and outsider tests
- ✓ Every prompt passed the category check, with evidence recorded; no adjacent-category prompts
- ✓ Every prompt traces to a Buyer Phrase Bank situation drawn from primary buyer sources
- ✓ Within each stage, prompts spread across personas and jobs rather than repeating one job
- ✓ Every prompt is unique and represents a distinct buying decision or problem
- ✓ No Brand-Aware, Competitor-Aware, or Feature-Aware prompts
- ✓ The Category Statement was confirmed with the user (or the assumption is stated at the top)
- ✓ The draft universe was frozen before the product fit check
- ✓ No prompt was introduced after Phase 6 began (check this especially on revision turns)
- ✓ Product research was used only to scope the run and confirm fit, never to write or reword prompts
- ✓ The import-ready list matches the library table exactly

Report this checklist, completed, as the final deliverable section.
