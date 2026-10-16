---
name: unique-content-ideas-from-sales-calls
description: "Mine sales and customer call transcripts for insights nobody has published, prove each with verbatim customer quotes and a novelty check, then turn the survivors into article ideas. Use for 'content ideas from our sales calls', 'what can we write about from this week's calls', 'mine our call transcripts', or to check if a call-based idea is new. Not for call summaries or for writing the article."
---

# Unique Content Ideas from Sales Calls

Your company records conversations no competitor can hear. This skill finds the few things in those conversations that **nobody could learn by searching the web**, proves it, and only then turns them into article ideas. The goal is non-commodity content: content only this company can write.

Do not use it to summarize calls, coach reps, write the article, plan pages from AI-citation or search data, or edit a draft.

The order of a run is fixed and never skipped:

**pick calls → workload check → close reading → candidate insights → novelty test → surviving insights with evidence → article ideas → check against existing content → output**

No article idea may appear unless it is derived from a surviving insight. Zero insights is a normal, honest result. The reader standard: *I've never seen anyone articulate this before.*

## Brand settings

This skill holds no brand details. They live in a brand settings document the user owns, titled "Unique content ideas brand settings", created by the personalization flow below from `assets/brand-settings-template.md`. Never write brand details into this skill's own files.

**At the start of every run, look for it.** Check the assistant's memory and project files for "Unique content ideas brand settings", then search the connected document tools (Notion, Google Drive and similar) for a document with that title. If you find it, read it and say in one line which brand you loaded. If you find more than one, ask which to use. If you find none, run without it: ask for the company name and website if you don't know them, and at the end of the run suggest personalizing once ("Personalize the unique content ideas skill for my brand") so later runs skip that question.

How a run uses the settings:

- **Company and website:** the content check in Phase 6 and the "How <company> fits" line on each article idea.
- **Call source:** the call recorder to read from. If its connector isn't available in this session, say so and offer the fallback (uploaded or pasted transcripts).
- **Known pain points in the category:** added to the rejection list in "What counts as an insight". They are rejected as commodity however strongly a customer says them.
- **Positioning sources:** read only to write the "How <company> fits" line. They never decide what counts as an insight and never shape how an insight is stated.
- **Where existing content lives:** the sitemap, CMS and editorial backlog to check in Phase 6, read-only.

A setting marked `Not set` means: ask at the step that needs it, or carry on without it if it's optional.

## Personalizing this skill

When the user asks to personalize, set up or customize this skill for their brand, or to update their settings, follow `references/personalization.md` instead of running. In short: list the few details the skill needs and what each is for, take them from wherever they live, draft what can be worked out, and save the brand settings document wherever the user chooses.

## Hard rules

- **A run never writes to the user's systems.** Not the CRM, the call recorder, the CMS, the content calendar or the team wiki. Read-only lookups are fine. The user approves ideas before anything is filed anywhere, and filing is their job. The only things this skill ever writes are the output document a run produces and the brand settings document during personalization.
- **Output lives with the user.** If at least one insight survives, create a document: the assistant's own document or artifact feature if it has one, a doc in the user's document tool if they ask for that, or otherwise a Markdown file. Give a short summary in the reply. If none survive, say so in the reply only, with no document.
- **Depth over coverage, always.** Every transcript is read in full by a reader that holds only that one transcript. Judging happens in one place so the bar is the same for every call. See "Scale" below.
- **Only the customer's words are evidence.** Ignore what the company's own people say, however well put. A rep's framing of a problem is not proof of the problem. The sales narrative is louder and better articulated than the customer's and will dominate the output unless actively suppressed. If the rep said a phrase first and the customer agreed, it is the rep's phrase.
- **No product marketing.** No feature walkthroughs, documentation, release notes, product comparisons, generic SEO or generic AI content.

## What counts as an insight

An insight is something learned from the call about how customers actually think, decide or work that **contradicts, or is absent from, the public conversation**, and that gives the user an angle they would not have thought of on their own.

The benchmark example:

> To test GEO, an enterprise team was not running experiments on its main website. It built subdomains and throwaway sites to test tactics first, and only then rolled what worked onto the main site.

Why this is an insight: the public GEO conversation assumes tactics are applied to the main site. The call revealed a hidden workflow (sandboxed GEO testing), which implies many enterprises are not yet deploying GEO on their main sites at all. It is behavioural, specific, surprising, and not findable by search.

**Not insights. Reject these, however strongly the customer said them:**

- Known industry pain points restated by a customer: legacy tools are rigid, migrations are hard, rolling changes out across many markets is painful, AI speeds up content creation, teams want personalization, security review slows deals. Add the category's known pain points from the brand settings, if any.
- Anything a competent marketer could argue from first principles or find on the first page of search results.
- Product reactions and feature requests ("they liked the dashboard", "they asked for SSO").
- Generic buying-process facts ("several teams are involved", "they want a pilot first").
- The sales rep's narrative.

If it could appear in a vendor's "top 5 challenges" listicle, it is not an insight.

## Scale: how much to take on

Quality drops when one reader holds several transcripts at once: early calls survive only as notes, comparison becomes a summary of summaries, and reading turns into skimming. Nothing visibly breaks; the insights just get thinner. So the skill separates **reading** (one reader per transcript) from **judging** (one place, one bar).

- **1 to 3 calls:** read them yourself, one at a time, writing notes for each before opening the next.
- **4 or more calls:** if the assistant can run sub-agents, give each call its own reader (see Phase 3) and do all the judging yourself. If it can't, read the calls yourself in batches of three, writing full notes per call before moving on, and tell the user the run will take longer.
- **Window: one week per run, as a default maximum.** A longer window is allowed only if the user confirms after seeing the workload check. Suggest splitting it into weekly runs.

These are rules of thumb, not hard caps. What matters is that you notice when the work is getting too big to do well and **say so before it happens**, not after delivering thin work.

## Phase 1: Pick the calls

Use the call recorder connector's tool for listing calls, with a date range, and page through until there are no more results. Call lists can be large: if you can run code, save them and filter there rather than reading every record.

If no call recorder is connected, ask the user to attach or paste transcripts (text, Word, PDF, VTT or SRT all work) and treat each file as one call.

- If the user names calls, use them.
- If they ask for "the latest discovery call", take the most recent call whose summary marks it as a first or discovery conversation (not pricing, renewal, internal or partner syncs). Say which call you picked and why in one line.
- If they ask for a type of call over a period ("all discovery calls last week"), classify each call from its name and summary, and list what you are including.
- Drop calls that cannot carry an insight: no summary, under about 10 minutes with no substance, placeholders, recording declined, internal-only syncs. Keep partner and agency calls: an agency describing its clients' behaviour is strong evidence.

## Phase 2: Workload check

Before reading any transcript, tell the user in a few lines: how many calls were found, how many were kept and dropped, a rough breakdown by type (discovery or demo, customer success, partner or agency, later-stage deal), and how you'll run it (read directly, or one reader per call).

**Stop and ask before reading** if any of these hold:

- the window is longer than a week
- there are more than about 25 substantive calls
- the calls are so mixed that one run would blur very different audiences together

When you stop, propose concrete ways to break it down so the user can pick: by week, by call type (discovery first, since it tends to carry the most market insight), by segment (enterprise vs mid-market, agencies vs end customers), or in batches of a stated size. Don't start until they choose.

If none of those hold, state the plan in one line and continue. If many of the calls are later-stage (pricing, security, legal), say up front that they usually carry little market insight, so the user isn't surprised by a short list.

## Phase 3: Close reading

Read the **whole transcript**, never the summary. Summaries are written for CRM reporting and strip out the asides, hesitations and exact phrasings where insights hide. Pull transcripts one call per request.

**Telling customers from the company's own people.** Never ask the user for this up front. Work it out per call: most call recorders label each speaker as internal (a user of the tool) or external (a contact or participant), so use that label. Where there is no label, anyone with an email address on the company's website domain is internal. Only when a speaker still can't be placed (typically an uploaded transcript with bare first names) ask the user, in one question for that run, and treat that speaker as non-evidence until they answer. Never save the answer.

Transcripts come from speech-to-text and garble names, products and jargon. Correct obvious errors in your notes and list the corrections, so the judge can see what was changed.

**Notes for each call** cover the customer's:

- **Actual behaviour and workarounds:** what they do today, including hacks, side projects, shadow tools and manual steps ("we spend a lot of time", "we always", "we never")
- **Sequencing:** what they do first, what they refuse to touch, where they test before committing
- **Trust boundaries:** what they let AI or tools do and what they won't ("we don't trust", "we can't")
- **Who really decides** and who can veto, especially when it differs from the org chart
- **Contradictions:** where what they say they want conflicts with what they describe doing
- **Mental models and language:** the words they use, especially when they differ from vendor vocabulary
- **Surprises:** anything that made you think "that's not how I assumed this worked"

Record every candidate-worthy quote verbatim with speaker, account and timestamp (mm:ss). Keep non-English quotes in the original language with an English gloss. Never silently translate, because the customer's exact word choice is part of the evidence.

A call with no candidates is fine. Note it and move on.

**With one reader per call:** give each reader `references/reader-brief.md` in full, with the call ID, name, account, date, customer speakers and the company's speakers filled in at the top. Readers find candidates generously and return notes plus candidates with quotes; they never search, write article ideas or decide what survives. You judge strictly. If a reader's report shows it skimmed (few quotes, summary-like notes, no timestamps), re-run that call rather than judging on thin notes.

## Phase 4: Novelty test

For each candidate insight, across all calls:

1. **State it in one sentence**, as an observation about the market, not about the company.
2. **Write the public assumption it overturns or fills in:** "The common view is X. This call shows Y." If you cannot name a common view that this differs from, it is probably not an insight.
3. **Search to check, when it helps.** Run 2 to 4 targeted web searches for the claim and its obvious phrasings, and record what exists. Verdict:
   - *Not found:* the behaviour or angle does not appear in what's published.
   - *Partly discussed:* the topic exists, but this specific angle, sequence or behaviour does not. Say exactly what is new.
   - *Common knowledge:* reject.
   Search results are supporting evidence, not the decision. The final test is: **would the user have arrived at this angle without hearing the call?** If yes, reject.
4. **Rate evidence strength:** a passing remark, a clear statement, a described workflow, or the same pattern across independent calls. Be honest. A single remark can still be an insight, but say that it's thin.

When several calls are in the run, look for the same behaviour showing up independently in different accounts. A pattern across unrelated calls is the strongest evidence this skill can produce; say so explicitly, and merge candidates from different calls into one cross-call insight where they describe the same thing.

**Check your load here too.** If there are so many candidates that you cannot give each one a proper novelty check (as a rule of thumb, more than about 15 after obvious rejects), pause. Tell the user how many there are, show the one-line list, and offer to test the strongest first or split the rest into a second pass.

Expect most candidates to die here. Keep a short list of rejected candidates with one line each on why they failed, so the user can see the bar was applied.

## Phase 5: Article ideas, from insights only

For each surviving insight, propose **as many distinct articles as the insight genuinely supports**, usually two to four. Each one takes a different angle: for example the trend piece, the practical how-to, the opinion, the framework.

Each idea needs:

- **A title written as a real, publishable article title for its format.** Not a statement or a thesis sentence. The title must make the format obvious:
  - How-to: "How Enterprise Teams Test GEO Tactics on Subdomains Before Touching Their Main Site"
  - Guide: "The Enterprise Guide to Running GEO Experiments Without Risking Your Main Domain"
  - Listicle: "7 Ways Enterprise Teams Sandbox GEO Experiments (and What They Learn First)"
  - Research or trend: "Why Most Enterprises Aren't Running GEO on Their Main Website Yet"
  - Opinion: "Stop Testing GEO on Your Homepage: The Case for a Sandbox Domain"
  - Bad, a statement rather than a title: "Making one page with AI is easy, changing 10,000 is the problem"
- **Format:** how-to, guide, listicle, opinion, research or trend, framework, comparison, case study
- **Angle:** one sentence on what this piece argues or teaches that only this insight makes possible
- **Reader:** who it's for and what they'll do differently after reading
- **How <company> fits:** two sentences maximum. The company supports the story, never becomes it, and the article must still stand if the company disappeared.

If an insight cuts against the company's own messaging, keep it and say so. That tension usually makes the piece more credible, not less.

## Phase 6: Check against existing content (read-only)

For each article idea, check whether the company already has something close:

- the live site, through web search restricted to the company's domain, or its sitemap
- the CMS, through its connector if one is connected, published content only
- the editorial backlog or content calendar, read-only, if the brand settings say where it lives

Verdict per idea: **New**, or **Update existing** (give the URL and say what the insight would add). Never drop an idea for overlap without saying so.

## Phase 7: Output

**If no insight survived:** reply only. Name the call(s) read, say plainly that there were no insights, and list the two or three closest candidates with one line each on why they failed. No document and no article ideas.

**If one or more insights survived:** create the document with the structure below. Then reply with where it is, each insight in one line, and the strongest article title.

1. **Calls read:** name, date, length, account, and the customer speakers. For multi-call runs, also list calls dropped and why, and calls that produced no candidates.
2. **Insights**, strongest first. For each:
   - The insight in one sentence
   - Evidence: verbatim quotes with speaker, account and timestamp
   - Why it's an insight: the common view, what the call shows instead, and what the searches found
   - Evidence strength (including whether it appeared across independent calls), and what would strengthen it
   - Article ideas derived from it, each with title, format, angle, reader, company fit, and the content-check verdict
3. **Rejected candidates:** one line each on why each failed.
4. **Confidentiality:** which ideas name a customer, and how to anonymise them.
5. **Research appendix:** per-call close-reading notes, and the searches run with links.

## Confidentiality

Account names appear in the document for internal traceability. Flag any article idea whose value depends on naming a customer publicly: it needs that customer's consent before it is written. Prefer angles that still hold up when the customer is anonymised. Never copy a transcript, or long passages of one, into anything outside the document.

## Compatibility

- **Call transcripts are required.** Best through a call recorder connector that lists calls and returns full transcripts (Gong, Modjo, Fireflies, Fathom, Avoma, Chorus and similar). Without one, the user uploads or pastes transcripts. Summaries alone are not enough.
- **Web search is required** for the novelty test and to check the company's own site.
- **Optional connectors:** a document tool such as Notion or Google Drive (positioning material, the content calendar, and the brand settings document) and the company's CMS (to check published content). All are read-only during a run.
- **Sub-agents are optional.** With them, each call gets its own reader; without them, calls are read in batches of three.
