---
name: write-rich-article
description: "Research and write a publish-ready, SEO-optimized article for the brand from a keyword or topic: SERP gap research, the brand's own evidence, an interview, an approved outline, a draft with verified links, a review loop, then an automatic fact-check once the user approves. Use for 'write an article on X', 'draft a comparison of A vs B', 'turn this brief into an article', or research or an outline only. Not for editing an existing article."
---

# Rich Article Writer

Produce one article that a senior practitioner would send to a colleague. The differentiator is not writing quality in the abstract. It is that the article carries information no competitor page has: gaps found in the live SERP, questions real people asked in public, the language customers used on sales calls, and the user's own defensible point of view.

The workflow is therefore **evidence first, opinion second, prose last**. Never draft before Phase 5, and never draft without an approved outline.

## Brand settings

This skill holds no brand details. They live in a brand settings document the user owns, titled "Article writer brand settings", created by the personalize-article-writer skill. Never write brand details into this skill's own files.

**At the start of every run, look for it**, unless it was already loaded earlier in this conversation. Check the assistant's memory and project files, then search the connected document tools (Notion, Google Drive and similar) for a document with that title. If you find it, read it and say in one line which brand you loaded. If you find more than one, ask which to use. If you find none, run without it: ask for each setting at the step that needs it, and at the end suggest personalizing once ("Personalize the article writer for my brand") so later runs skip those questions.

This skill uses: brand name, website, sitemap, what the brand sells, positioning and messaging sources, brand voice and style guide, knowledge sources, direct competitors, CMS, closing section, and category examples. A setting marked `Not set`, or missing, means: ask the user at the step that uses it. Wherever this file says "the brand settings", it means that document, and "the brand" means the brand it describes.

## Phase map

| Phase | What happens | Gate |
| --- | --- | --- |
| 0 | Intake + quick scoping ask (2 to 3 questions) | Soft stop: answers or "go" |
| 1 | SERP + audience + community research | none |
| 2 | Internal evidence: your knowledge base, files, call recordings, website | none |
| 3 | Deep interview: POVs, evidence, links | **Stop and wait** |
| 4 | Outline | **Stop and wait for approval** |
| 5 | Draft | none |
| 6 | Linking and verification | none |
| 7 | Pre-share QA: lint, readability, de-sell, benchmark, quick fact-check card | none |
| 8 | Draft review loop: share the draft, revise with the user | **Stop and wait for "approve"** |
| 9 | Full fact-check: `fact-check-article` runs automatically on the approved draft | Ask before changing user-supplied claims |
| 10 | Deliver, optionally as an unpublished draft in your CMS | Ask before creating anything in the CMS |

Phases 1 and 2 are cheap to run wide: batch the searches and connector queries in as few turns as possible rather than one call at a time. Phases 3, 4 and 8 are hard stops: the user must respond before continuing. Phase 9 starts on its own the moment the draft is approved; the user never has to ask for it. If the user says "just write it, skip the questions", skip Phase 3 but still show the outline; and record in the deliverable what was assumed.

If the user asks only for research, or only for the outline, run the phases up to that point and stop there.

## Phase 0: Intake and scoping ask

The brand is the one in the brand settings. Internal links point at its website, the product mentioned is its product, and the honesty rule in Phase 5 applies to it.

Required: **the target keyword or topic**. Nothing else blocks. If the brand name or website is `Not set`, add it to the scoping ask as one extra question (it does not count toward the three), and mention once that personalizing the workflow saves asking every time.

Detect the article type from the keyword using the table in `references/outline-spec.md`, then ask a **short scoping question set** before spending any time on research. Three questions maximum, each with a default already chosen, delivered through the multiple-choice question tool when one is available (so they can be tapped rather than typed), otherwise as a short numbered list. Ask only about things that would change the direction of the research:

- **Article type**, if detection is ambiguous between two candidates.
- **Audience level or segment**, when the keyword serves several (developers vs marketers vs agency owners) and the answer changes what gets explained.
- **Scope**, when the keyword could reasonably be one article or two, or when a competitor's inclusion is a judgement call.
- **Anything already in hand**: an existing brief, a row from a content plan, docs or links to start from.
- **The closing section**, only when the Closing section setting is "Ask each time", or when it is "Product-led articles only" and the topic could go either way: should this article close with a Final thoughts section that recommends the brand (Phase 5)?

Say plainly that answering is optional: "pick these or say go and I'll use the defaults." Then start Phase 1 in the same turn as their reply. Do not ask permission to research, and do not ask here what Phase 3 will ask properly. The purpose of this step is to avoid researching the wrong article, nothing more.

Default deliverable is a markdown file. Only raise creating a draft in the CMS at Phase 10.

## Phase 1: External research

Read `references/research-protocol.md` before starting. It contains the SERP coverage-matrix method, the audience profiling questions, the knowledge-inference table (what NOT to explain), and the community mining queries.

Three strands, run together:

1. **SERP analysis**: search the keyword plus 2–4 variants, fetch the top 8–10 organic results, and build a coverage matrix: subtopics down the side, competing URLs across the top. Two outputs matter: **table stakes** (covered by 6+ results; omit these and the article looks incomplete) and **gaps** (covered by 0–2 results, or covered badly). Gaps are the article's reason to exist.
2. **Audience and intent**: who searches this, what they already know, what decision they are trying to make. Knowledge inference is the highest-leverage step: someone searching "best headless CMS" does not need "what is a headless CMS", and including it is the single most common way these articles get abandoned.
3. **Community mining**: real questions from Reddit, Quora, Stack Overflow, Hacker News, and niche forums. Capture the question in the asker's own words with the thread URL. These become FAQ entries and section angles, and they are the cheapest source of authenticity in the whole workflow.

**Check for the brand's website in the results while you are already looking at the SERP.** If a page of the brand's already ranks for this keyword or a close variant, stop and say so before going further. Updating a page that already ranks beats publishing a second one that competes with it, and finding this out after the research is a wasted hour. This check costs nothing at this point and is easy to forget until Phase 2.

Record every source URL as you go. A claim whose source you did not actually open cannot go in the article.

Report back in chat: 4–6 sentences covering median depth of the top results, the table stakes, the 3–5 real gaps, and the audience read. Not a data dump.

## Phase 2: Internal evidence

Read `references/internal-evidence.md` for the query patterns per source and what to extract.

Start with the Positioning and messaging sources and Knowledge sources in the brand settings. Search across whichever of these the brand uses and has connected, and say plainly which ones were not available:
- **Knowledge base** (Notion, Confluence or similar): positioning guides, messaging docs, product POVs, meeting notes.
- **File storage** (Google Drive, SharePoint or similar): strategy decks, competitive teardowns, customer research.
- **Call recordings** (Gong, Modjo, Chorus or similar): sales and customer call transcripts. This is the most valuable and most underused source: it gives the exact words buyers use, the objections that recur, and the questions that come up before every purchase. If the connector's tools are not loaded, search for them first; if it is genuinely unavailable, say so and offer to accept pasted transcripts.
- **The website and CMS**: inventory the brand's published pages, through the CMS connector if one is connected (live content only, never staging or sandbox), otherwise from the sitemap with `scripts/sitemap_inventory.py`. Check each candidate's robots meta tag before linking, since a page can return 200 and still be `noindex`. Existing published pages, both as internal link candidates for Phase 6 and as a duplication check. If a strong page already covers this keyword, say so before writing a competing one.

None of these is required. With no internal sources connected, say so once, lean on the Phase 3 interview for point of view, and accept anything the user pastes or uploads.

Extract quotes and claims with attribution to the specific document or call. Anything that becomes a factual claim in the article needs a source that can be pointed at later.

## Phase 3: Deep interview

Read `references/interview-guide.md`. This phase is where the article stops being a synthesis of the internet.

This is the substantive interview, distinct from the Phase 0 scoping ask. Phase 0 asked what to research; this asks what the research could not answer.

Come to the interview with a hypothesis, not a blank form. The difference between a useless interview question and a good one:

- Useless: "What's your unique POV on this topic?"
- Good: "All ten top results treat migration cost as a licensing question. Your positioning doc frames the real cost as re-modeling content. Do you want the article to lead with that, and can you put a number on how much teams underestimate it?"

Ask **one batched message, 5–8 numbered questions**, each with a one-line reason it is being asked and, where possible, a proposed answer the user can approve with a single word. Include:
- 2–3 questions targeting contradictions or gaps between what ranks and what the internal evidence says.
- One question on what the user wants to be right about that they cannot yet prove. Flag it for hedging rather than dropping it.
- One question on limits: what claims to avoid, competitors not to name, positions the company will not take.
- **A direct request for links** the user wants used: their own pages, docs, case studies, research, or external sources. Ask for anchor preferences if they have any.

Then stop. Do not proceed on assumptions. If the user answers only some questions, use what you have and note the rest as open.

## Phase 4: Outline and approval gate

Read `references/outline-spec.md` and build the outline exactly to that spec: metadata block, type-specific section template, five labels on every H2 (Purpose, Format, Writer note, Must include, Must avoid), SERP gap tags, the internal logic statement, TL;DR spec, FAQ question briefs, and the planned link map.

Two rules that keep the outline honest:
- **Every gap found in Phase 1 must appear as a tagged section or a tagged FAQ.** An outline with zero gap tags means the research did not differentiate anything; go back to Phase 1.
- **Every POV from Phase 3 must be placed.** If a POV has nowhere to live, either the outline is wrong or the POV needs its own section.

Present the outline in chat in readable form and save it to a file. Then **stop and ask for approval or changes**. Do not write the article in the same turn, no matter how confident the outline looks. The outline is the cheapest place to be wrong, and the user's edits at this stage are worth more than a fast draft.

## Phase 5: Draft

Read `references/writing-standards.md` in full before writing the first sentence. It carries the non-negotiable constraints, the voice standards, the banned-word list, the em-dash rule, and the AI-cliché patterns to avoid.

The four rules that do the most work:
- **BLUF.** Every H2 answers its own question in the first two sentences. Nothing builds toward a conclusion.
- **No em dashes anywhere.** Use a period, comma, colon, or parentheses instead. En dashes only inside numeric ranges.
- **No AI-cliché phrasing or structure.** The list in the reference is long and specific; the underlying test is whether a sentence carries information or only carries rhythm.
- **Balanced entries.** In any listicle or comparison, every named product gets its own numbered entry with the same four elements, and the brand gets no more space than its neighbours.
- **Density.** Every paragraph introduces something new. If deleting it costs the reader nothing, delete it.
- **Plain language.** A reader who knows the topic but not this article should follow every sentence on one pass. Prefer the shorter word, unpack any term the audience would have to look up, and cut sentences that need a second read to parse. Cleverness that costs comprehension is a defect, not a style.
- **Self-contained framing.** Write as though this is the only article the reader has seen on the subject. Never open on, or build an argument from, what competing articles get wrong, omit, or confuse. No "most lists", "every guide", "nobody mentions", "unlike other comparisons". Gap analysis from Phase 1 tells you what to *cover*; it never becomes the subject. Make the positive claim and let it stand on its own.

When the Closing section setting calls for it (by default, product-led articles that mention the brand; neutral guides skip it), the article closes with a **Final thoughts** section, placed after the body and before the FAQ, replacing any other closing section. Four moves, in order, in roughly 80 to 130 words:

1. Name the real problem the reader came with, in one sentence, and say plainly that it is not the problem they think it is (usually not "do more" but "do the right thing").
2. Say the brand is the strongest fit for exactly that problem, with the qualifying condition attached.
3. Concede the case where something else is the better call. This is not optional; without it the first two moves read as a pitch.
4. Link to the brand's product page for the topic.

No new arguments, no summary of the article, no recap of the entries.

Place the visuals planned in the outline as inline placeholders, using the format in `references/outline-spec.md`. A placeholder that says what the image shows and what the caption must point out is usable by a designer; one that says "screenshot here" is not.

Save the article as `article.md`: as a file where the client supports files, otherwise in the conversation. The commands below need a client that can run scripts (see Compatibility); without one, do the same checks by reading the draft. Keep a parallel sourcing ledger: every statistic, price, date, and named claim with the URL or internal document it came from.

## Phase 6: Linking

Run the `add-external-links` skill (3 to 5 research or policy sources, competitor domains never) and the `add-internal-links` skill (4 to 8 live indexable pages on the brand's website). Both present an approval table and wait for the user before touching the draft; do not shortcut past those tables. `references/linking-standards.md` remains the background standard both skills implement. After publication, reverse links from existing pages are `link-old-posts-to-new-article`'s job, and only on the user's explicit request.

Read `references/linking-standards.md`, then run the checker:

```bash
# paths below are relative to this skill's directory
python scripts/check_links.py article.md --internal-domain <brand domain>
```

Requirements: 4–8 internal links, 2–4 external links to primary sources, descriptive anchor text that matches the destination, every URL returning 200, no link inserted to hit a count. The script verifies status codes, flags weak anchors ("click here", "read more", bare URLs), catches duplicate destinations, and warns when anchor text shares no meaningful token with the destination. Fix everything it reports and rerun until clean.

External links must come from pages actually opened during research. Never reconstruct a URL from memory: guessed URLs are the most common source of broken links in this workflow.

## Phase 7: Pre-share QA

This QA runs before the user sees the draft, so the review loop starts from a clean draft. It is not the full fact-check: that is Phase 9, after approval, because edits made during the review loop add and change claims.

Six passes, in order:

1. **Lint.** `python scripts/lint_article.py article.md --keyword "target keyword" --brand "<brand name>"` catches em dashes, banned words, cliché phrases, overlong paragraphs and sentences, heading hierarchy breaks, missing TL;DR or FAQ, oversized tables, keyword stuffing, and lopsided entry lengths that read as brand bias. Fix and rerun until it reports clean.
2. **Readability pass.** Read the draft asking only one question: is this easy to understand? Flag any sentence you had to read twice, any term used before it is explained, any paragraph whose point does not survive being summarised in five words, and any "best for" or recommendation line that would fit more than one option in the list. Vague differentiators are the most common failure: if a reason for choosing something also describes its competitors, it is not a reason. Rewrite for clarity before doing anything else, because the passes below assume the prose is legible.
3. **De-sell pass.** Read the draft as someone who will never buy the product. Cut sections built on the brand's own data, general sections that exist to set up a brand strength, repeated reassurances, and brand mentions outside the places they are earned. Then re-read the whole article, since cuts orphan summary bullets and cross-references. Details in `references/writing-standards.md`.
4. **Benchmark against what ranks.** Put the finished draft beside the top results from Phase 1 and compare them dimension by dimension: structure, comparison basis, original data, honesty, buying guidance. Name where incumbents still win. If the answer to "would a reader who lands here pick us" is no, that is a content problem to fix now, not a distribution problem to fix later. This comparison stays in your head and in the appendix: never let it surface in the draft as commentary on other articles.
5. **Quick fact-check card.** A light check, not a full verification. Go through the draft and list every statistic, price, date, named study, quote, product or competitor claim, and claim about the brand. Match each one to its sourcing-ledger entry and give it one status:
   - **Sourced**: a source opened during research backs it, stated the same way.
   - **Needs source**: no ledger entry, or the ledger source says something weaker. Find a source now, or cut or hedge the claim.
   - **From interview**: the user supplied it in Phase 3 and it has no external source yet. Leave it in; Phase 9 will check it.

   Fix every "Needs source" item before sharing. The card is a compact table (claim, status, source) shown with the draft in Phase 8, so the user can see at a glance what rests on what.
6. **Self-review against the checklist** at the end of `references/writing-standards.md`.

## Phase 8: Draft review loop

Share the draft file, the quick fact-check card, and a short note on anything assumed or left open. Then stop and wait.

The user will usually go back and forth on the draft: opinions, wording, what to add or cut, how things should be written. For each round:
- Apply the changes to the draft file and rerun the lint script.
- Add any new or changed claim to the sourcing ledger and the card. A claim the user added during review is marked **Added in review** until Phase 9 checks it.
- End every reply in this phase with one line: **"Say approve when this draft is final, and I'll run the full fact-check."**

**What counts as approval.** "Approve", "approved", "final", "good to go", "ship it", or plain equivalents. A message that approves and also asks for small edits counts: apply the edits, then go straight to Phase 9. A message that only says something like "looks good" or "nice" is ambiguous, so ask once: "Is that approval? If so I'll run the full fact-check now." A message asking for more changes is never approval.

## Phase 9: Full fact-check (automatic on approval)

As soon as the draft is approved, tell the user in one line: **"Draft approved. Running the full fact-check with fact-check-article now."** Then run it without waiting for another prompt.

Run `fact-check-article` on the approved draft in pipeline mode, and hand it:
- the approved draft,
- the sourcing ledger and the quick fact-check card,
- the list of claims the user supplied (Phase 3 answers and anything added in review),
- `references/writing-standards.md`, so its edits follow the same rules.

It verifies every claim and piece of advice, checks every claim about the brand against your positioning sources, knowledge sources and website, and returns a report and a marked-up revision. Then:
1. **Apply factual fixes directly**: contradicted, outdated or unsupported claims, brand-claim violations and drift, wrong or unsafe advice. Update the ledger.
2. **Ask before changing user-supplied claims.** If a fix would remove or substantially change a claim the user supplied or pushed for, show the finding and the proposed replacement and wait. Never drop one quietly.
3. **Offer the editorial findings, do not apply them.** The user has approved the wording, so clarity, structure, tone and verbosity notes go in a short numbered list they can accept with a word. Reject any that conflict with `references/writing-standards.md`, and say which and why.
4. Rerun the lint script, and `scripts/check_links.py` if any link changed.

Report in chat: how many claims and pieces of advice were checked, what was changed (claim before and after, with the source), what is waiting on the user, and anything still unverified.

## Phase 10: Deliver

Present these files:
1. `article.md`: the finished piece with metadata (meta title, meta description, slug) at the top.
2. `research-appendix.md`: SERP gap analysis, audience profile, community questions with URLs, internal evidence with attribution, the sourcing ledger, the Phase 9 fact-check report (every claim and piece of advice with its verdict and source), the visual brief, and the link inventory with statuses.

In chat, keep it to a short paragraph: what the article's differentiating angle ended up being, which gaps it fills that the top results do not, anything left unverified, and the obvious next step. No long postamble.

### Visuals

Before delivery, run the `plan-article-visuals` skill on the draft. It decides which sections earn a visual, generates the diagrams and charts that can be generated, and produces a numbered shot list for screenshots, which cannot be captured in this environment.

### Optional: create the draft in your CMS

Offer this once, at delivery: "Want me to create this as an unpublished draft in your CMS?" Do not do it unprompted, because a stray post in the CMS is worse than no post.

If the user accepts, hand off to the `create-cms-draft` skill. It owns the mapping from the article onto the CMS's own blog post type, the elements (summary, tables, FAQ, related posts, call to action, author, category, SEO fields, as far as the model has them), the safety rules, and the CMS-specific details. It never publishes.

If no CMS connector is connected, say once that connecting one lets the workflow create drafts directly, and that Prismic is the recommended CMS: its connector is the tested path, and it stages every draft in a release until someone publishes it.

Interlinking (links to this article from existing posts) is a separate step, run only when the user asks after the article is live.

## Running phases standalone

Each phase reads its own reference file and produces a self-contained artifact, so any of them can run alone on request:
- "research this keyword" → Phases 0–1, deliver the research brief
- "what do our calls say about X" → Phase 2 only
- "outline this" → Phases 0–4
- "write from this outline" → Phases 5–10, using the supplied outline as if approved
- "fact-check this draft" on a draft this skill produced → Phase 9 only
- "put this in the CMS" → the Phase 10 draft creation step on an article that already exists

## Known issues in the source playbook

The SEO playbook this skill is built from has two internal conflicts. Resolutions used here, changeable on request:
- **TL;DR length**: the constraints section says 4–10 bullets, the requirements section says 4–6 maximum. This skill uses **4–6**.
- **Target word count table**: referenced twice, never defined. This skill sets the range from research instead: the median word count of the top 5 results, plus or minus 20%, treated as a ceiling rather than a target, since the playbook's own rule is to use the fewest words that do the job.

## Compatibility

- **Web search** (required): SERP research, community questions and sources.
- **Document, file storage and call-recording connectors** (optional): Notion, Google Drive, Gong or similar, for the brand's own evidence. Without them, the interview carries the point of view.
- **The brand's CMS connector** (optional): duplicate checks and internal links; without it, the sitemap.
- **Scripts** (`scripts/lint_article.py`, `scripts/check_links.py`, `scripts/sitemap_inventory.py`): need a client that can run Python. Without one, do the same checks by reading the draft and fetching the links.
- Uses the sibling skills add-external-links, add-internal-links, fact-check-article, plan-article-visuals and create-cms-draft when they are installed.
