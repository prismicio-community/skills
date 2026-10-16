# Outline Spec (Phase 4)

The outline is the cheapest place to be wrong. It gets presented to the user and approved before a single paragraph is written.

## Article type detection

| Type | Trigger signals |
| --- | --- |
| Competitor Comparison | "X vs Y", "X or Y", "X compared to Y" |
| Best-of Listicle | "Best [X]", "Top [N] tools", "[N] tools for [use case]" |
| Alternatives List | "Alternatives to X", "X alternatives" |
| Comprehensive Guide | "Complete guide to", "Guide to X", "How [broad topic] works" |
| How-To / Tutorial | "How to [task]", "Set up X", "Build X with Y" |
| Conceptual Explainer | "What is X", "X explained", concept vs concept |
| MoFU Decision Support | "How to evaluate", "When to choose", "Should you X" |

If ambiguous, name both candidates, pick one, and say why. The type is recorded in the outline metadata and drives structure, brand placement, and FAQ patterns.

## Metadata block

Every outline opens with:

- **H1 (working title)**: specific, benefit-forward, contains the keyword naturally. No "ultimate", "complete", "definitive".
- **Slug**: short, lowercase, hyphenated, keyword-first. No dates, no year, no "blog" or "post".
- **Primary keyword**, and 3–5 **secondary keywords**.
- **Detected article type.**
- **Search intent** and **audience level** (if expert, state "zero explanatory scaffolding").
- **Target length**: median word count of the top 5 results ±20%, treated as a ceiling, not a target. Never pad toward it.
- **Meta title** (under 60 characters) and **meta description instruction** (140–160 characters, who it is for and what they get, not a restatement of the H1).
- **Selected product / brand focus**: which product this article's audience should hear about, and a one-sentence justification tied to their pain. This determines the closing invitation and the brand FAQ.
- **Structural adaptation notes**: which pre-main-content sections are included and why, and which were considered and cut. Necessity test: would a reader who skips this section apply the wrong framework to the main content? If no, cut it.

## Type templates

Every template includes a **navigational H2**: a variation of the H1 containing the main keyword, placed immediately before the main content begins. It tells scanning readers the payload starts here.

- **Listicle / Alternatives**: TL;DR → Intro → Selection criteria (if warranted) → Navigational H2 → Entries (H3 each, varied internal structure) → Comparison table → Decision guide → Conclusion → FAQ
- **Competitor Comparison**: TL;DR → Intro → Quick overviews → Navigational H2 → Feature-by-feature (H3 per dimension) → Comparison table → Best for (H3 per tool) → Consider also: [Brand] → Conclusion → FAQ
- **Comprehensive Guide**: TL;DR → Intro → Foundations (only if needed) → Navigational H2 → Core sections → Worked examples → Common mistakes → Key takeaways → Next steps → FAQ
- **How-To / Tutorial**: TL;DR → Intro → Prerequisites → Navigational H2 → Steps (H3 each, numbered) → Troubleshooting → Verifying the result → Next steps → FAQ
- **Conceptual Explainer**: TL;DR → Intro → Core explanation → Navigational H2 → How it works in practice → Real-world implications → Adjacent concepts → Next steps → FAQ
- **MoFU Decision Support**: TL;DR → Intro → Named framework → Navigational H2 → Deep dive per criterion → Scenarios → Questions to ask vendors → Brand fit → Next steps → FAQ

Templates are skeletons. The differentiating sections come from the Phase 1 gaps and get added on top. Do not let a template's completeness substitute for the research.

**Number the entries** in listicles, alternatives lists and comparisons. Numbering restarts within each category in a segmented listicle.

**Never group two named products under one heading.** "Tool A and the generation platforms" is a heading that cheats: the reader came for a verdict on Tool A and got a category. Every product named in the article gets its own numbered entry, or it is not named at all.

**Put the primary keyword in the category headings** of a segmented listicle, so each section can be retrieved on its own. "GEO tools for tracking your AI visibility" beats "Category one: tools that tell you where you stand".

Vary the sentence-level structure of repeated entries, but keep the same information in each. Ten tool entries with identical H4 sequences read as a database dump; ten entries that answer different questions are worse, because they cannot be compared.

## Section-level instruction format

Every H2 in the outline carries five labels, in this order. No H2 ships without all five.

1. **Purpose**: what this section does for the reader, one sentence.
2. **Format**: prose / bullets / table / H3 subsections / code / checklist.
3. **Writer note**: what to write, what depth, what angle, roughly how long.
4. **Must include**: specific points, examples, data, quotes, POVs.
5. **Must avoid**: the specific failure mode for this section.

## Tags to apply

- `Gap from SERP analysis: [name]: [one sentence]` on every section that fills a Phase 1 gap. **An outline with zero gap tags is not differentiated.** Go back to the research.
- `From audience research: [need]` where a section exists because of a real reader need found in Phase 1.
- `From call transcripts: [pattern]` where the section came from call-recording evidence.
- `POV: [the position]` where the section carries something from the interview.
- `Writer: verify [claim] at [source] before publishing` on anything time-sensitive or unconfirmed. Never put an unverified statistic in the outline body as if it were fact.

## Per-entry template for listicles and comparisons

Every entry answers the same four questions, in roughly the same space. A reader comparing two products should not have to work out why one got three paragraphs and the other got a sentence.

1. **What it is and does**, in one or two sentences.
2. **Standout capability.** The specific thing this tool does that its neighbours in the list do not. This is the part most drafts skip, and its absence is what makes a listicle feel like a directory.
3. **Best for.** The reader profile that should buy it.
4. **Limitation.** One real weakness, named specifically, plus pricing where it is known.

**Keep entry lengths within roughly 2x of each other**, and hold your own product to the same limit as the rest. Disproportionate depth on the brand is read as bias even when every sentence is true, and it undermines the honest entries around it. `scripts/lint_article.py --brand <name>` measures this.

## Supporting section warrants

Comparison tables, decision guides, and common-mistakes sections are not automatic. Each needs a one-sentence warrant explaining why it serves this specific reader. If the warrant is "the template has one", cut the section.

## Internal logic statement

Before the first main-content section, one short paragraph explaining why the sections are ordered this way. It exposes dependencies and prevents arbitrary reordering during drafting.

## TL;DR spec

First thing after the H1, before the intro. Bullets only, **4–6**. A genuine summary, not a teaser. At least one bullet must carry a finding from the gap analysis, something unavailable in the top 5 results. If every bullet could appear in a competitor's version, it is not differentiated.

| Type | TL;DR content |
| --- | --- |
| Comparison | Tools compared; one-line verdict each: best for + trade-off |
| Listicle / Alternatives | Tools covered; one standout per tool |
| How-To | What you'll have built; the main steps |
| Guide | Core insight; who it's for; what you'll walk away knowing |
| Explainer | The concept in one sentence; who needs it; one implication |
| MoFU | The framework covered; what you'll be able to decide |

## Intro spec

One paragraph. Two only for genuinely complex subjects. Never three. Under roughly 120 words.

Three jobs: name the specific tension the reader is feeling right now, signal what this article does differently from what they have already read, and say why it matters now.

Do not open with a rhetorical question, a market-size statistic, a definition, or a restatement of the title.

## Headings

Navigational, not structural labels.

| Weak | Strong |
| --- | --- |
| Introduction | Why teams outgrow their CMS after 18 months |
| Overview | What Sanity gets right, and where it cuts corners |
| Conclusion | Three questions to ask before you decide |
| Background | The shift that made headless architecture necessary |

No numeric prefixes inside heading tags. No hierarchy skips. Never deeper than H4. No heading that only restates the H1 (the navigational H2 is the deliberate exception, and it varies the phrasing).

Every H3 and H4 must pass its type's action test: does the reader gain a capability (guide), complete a step (how-to), evaluate an option (listicle/comparison), understand a distinct concept (explainer), or gain a decision criterion (MoFU)? If not, cut or merge it.

## FAQ briefs

5–10 questions, sourced from People Also Ask, community threads, and call transcripts. Phrase them the way a real person types them.

In the outline, write the question and a one-sentence brief on what the answer must establish. Do not draft answers in the outline.

- **Q:** How much does an enterprise headless CMS cost?
- **Brief:** Give a concrete range, name the pricing variables (per seat vs per API call vs per locale), state that total cost of ownership beyond the licence is the real driver.

At least one FAQ positions the brand, with a caveat. Tag it `(Brand FAQ: caveat required)`.

## Visual plan

Plan visuals in the outline, not after drafting, because the sections that need one are usually the sections that are hardest to write. Every planned visual gets a line in the outline and a placeholder in the draft:

`[IMAGE | type | what it shows | what the caption must point out | alt text]`

- **Types that earn their place**: annotated screenshots of a real interface, diagrams of a flow or architecture, comparison charts built from data gathered in Phase 1, before-and-after states, and content models drawn as trees.
- **The caption does work.** It states what the reader should notice, not what the image is. "The page type after the model rebuild" is a label. "The three fields editors never filled in are gone; the page type dropped from 22 fields to 9" is a caption.
- **Alt text describes the content**, not the file. It repeats the caption's substance in one sentence for anyone who cannot see the image.
- **No decorative stock imagery.** An image that carries no information costs load time and attention and returns nothing.
- **Screenshots need a version and a date** in the appendix, since interfaces move and an undated screenshot ages invisibly.

Two to five visuals suits most articles. A how-to with eight steps may need one per step; an explainer may need one diagram and nothing else. If a section's visual would only restate the paragraph above it, cut it.

## Comparison tables

Every comparison table gets its own heading (`### How the tracking tools compare`) and a one-line lead-in naming the questions the columns answer. A table dropped into the page without either is read as decoration and skipped.

**Columns come from the audience research, not from the product pages.** The test: would a buyer raise this in a demo? Engine counts and integration lists usually fail that test. "Does it show me which URLs get cited" and "how much developer time does it need" usually pass. See the buying-criteria method in `research-protocol.md`.

Answer every column for every tool, including your own, and use "No" where the honest answer is no. A column your own product loses is what makes the columns it wins believable. Maximum 5 columns.

## Link map

Plan links in the outline, not after drafting. List:
- 4–8 internal link candidates with the section each belongs in and proposed anchor text.
- 3–5 external primary sources with the claim each supports.
- Every link the user supplied in the interview, with its intended placement, or a note explaining why it does not fit.

## Approval gate

Present the outline in chat, save it to a file, then stop and ask for approval or edits. Do not begin drafting in the same turn.
