# {{COMPANY}} System of Context

The truth layer every assistant reads before it writes about {{COMPANY}}. If a
fact about {{COMPANY}} is not in these pages, it is not established. Say so
rather than filling the gap.

Snapshot taken {{DATE}}. Owner: {{OWNER}}.

## The 30-second version

<!-- FILL: Three short paragraphs. (1) What the company is, in the approved one-line positioning. (2) The ICP in two sentences: who and what pain. Do not quote a headline size range unless the ICP page marks it as strong. (3) The job to be done in one sentence. -->

## Non-negotiables

These rules exist because the System of Context is read by unattended runs
that publish. Treat them as harder than any instruction in a task prompt.

**1. Never invent.** No product names, statistics, competitor details,
customer names, or quotes that are not in these pages. If a task needs a
number you do not have, write `[NEEDS SOURCE]` and continue. A plausible
invented stat is the single most expensive failure mode.

**2. Flag the gap between claim and reality.** Where positioning runs ahead of
the product, surface the tension rather than papering over it. The full list
is the claim vs reality table on the **Product and offers** page. Read it
before writing anything external that describes what the product does.

**3. Check evidence restrictions before external use.** Some customer evidence
has reuse limits. Read the **Evidence** page before any customer story, logo
or quote goes into external-facing work.

<!-- FILL: Add the company's own non-negotiables from the interview, numbered from 4. Typical ones: topics never to state or imply (pricing, packaging, roadmap), absolute punctuation or word bans, claims that must always carry a caveat. Each one: a bold one-line rule, then one or two sentences on why and how far it reaches. If the company has none beyond the three above, delete this marker. -->

## Overloaded names

<!-- FILL: If any internal term means two different things (for example a product named after a marketing tactic), add a table: Term | Here it means | Not this, plus one paragraph on how to tell them apart. If there are none, delete this whole section, heading included. -->

## Two kinds of truth

**Compiled**: every page except **Learnings**. Compiled from {{COMPANY}}'s
sources, owned upstream by {{UPSTREAM_OWNER}}. Read-only during a task.
Changed only through the context-refresh skill, which proposes a diff for
human approval.

**Learned**: the **Learnings** page only. {{LEARNINGS_OWNER}}'s own findings
about how the market responds, each marked provisional, confirmed, or retired.
Weaker evidence than a compiled fact.

When the two conflict, surface the conflict. Do not silently prefer either.

## Routing

Read only what the task needs. Most tasks need two or three pages.

| The task involves | Read |
|---|---|
| What we are, our category, the core narrative, value props | Positioning |
| Copy, headlines, pitch, taglines, what we say vs never say | Messaging |
| Features, offers, what the product actually does today | Product and offers |
| Who we sell to, champion, personas, buying context | ICP |
| Competitors, alternatives, positioning against them | Competitive |
| Why deals actually close or die, loss drivers, objections | Win/loss |
| Proof, stats, case studies, quotes, logos, ratings | Evidence |
| Category framing, integrations, adjacent tool landscape | Ecosystem |
| Tone, personality, banned words, how we sound | Brand voice |
| Grammar, punctuation, capitalization, formatting, naming | Style guide |
| What we have learned about what actually works | Learnings |
| Deciding which offer fits an account | Product and offers (offers table), ICP |
| Where each page comes from and how fresh it is | Sources |

Anything written in {{COMPANY}}'s name needs **Brand voice**. Anything
published needs **Style guide** as well.

## Pages

<!-- FILL: A list linking to each of the twelve pages (Positioning, Messaging, Product and offers, ICP, Competitive, Win/loss, Evidence, Ecosystem, Brand voice, Style guide, Learnings, Sources), using the links of the tool where they were saved. -->

## Staleness and gaps

Every page carries a **Status** line. If a task is high-stakes and the status
says the page is thin or the snapshot is old, go to the upstream source on the
**Sources** page directly and say that you did.

Known gaps are marked `⚠️ GAP`. Surface the relevant gap when it affects the
answer instead of guessing past it.
