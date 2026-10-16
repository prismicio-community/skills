---
name: system-of-context-claim-check
description: "Audit a draft against the company's System of Context before it ships: find invented, drifted or unsupported claims, overclaims, restricted evidence, off-limits topics and banned words, with a paste-ready fix for each. Use on any external copy, agent-written pages included, or when someone asks \"can we say this\", \"is this accurate\" or \"check this before I send it\". To fact-check an SEO article against outside sources, use fact-check-seo-article."
---

# Claim check

Catch unsupported claims before they publish. Most bad marketing claims are
not lies; they are plausible sentences nobody sourced. This skill finds them
and proposes a fix for each.

## Inputs

- **The draft.** Pasted text, a document, or a page from a connected tool. If
  it is missing, ask for it.
- **The System of Context.** Found automatically, see below.

## Find the System of Context

1. Check the assistant's memory and project files for a document titled
   "<Company> System of Context".
2. Otherwise search the connected document tools for "System of Context".
3. If you find one, read its overview page and say in one line which company
   and snapshot date you loaded. If you find more than one, ask which.
4. If you find none, say the check can only flag claims as unverified, and
   offer to build one with the build-system-of-context skill. Then run the
   check anyway, classifying every specific claim as unsupported.

## Procedure

1. Read the pages the draft touches. For anything external always include
   **Brand voice** and **Style guide**, and **Product and offers** for anything
   that describes what the product does.
2. Extract every checkable assertion: statistics, customer names, quotes,
   logos, competitor claims, product capabilities, category claims, and
   anything touching a topic the overview's non-negotiables put off limits.
3. Classify each one:
   - **Supported**: appears in the System of Context, stated the same way
   - **Drifted**: traceable to it but reworded in a way that changes scope, strength, or meaning
   - **Unsupported**: plausible, not established anywhere
   - **Violation**: breaks a non-negotiable (invented fact, overclaimed capability, off-limits topic, restricted evidence, banned word or punctuation)
4. Report violations first, then unsupported, then drifted. Supported claims
   get a count, not a list.
5. For each problem, propose a specific replacement line the person can
   paste. A finding without a fix just moves the work.

## Report format

```
## Violations (fix before shipping)
- [quoted line] → [which rule] → [suggested replacement]

## Unsupported claims
- [quoted line] → [what evidence would be needed] → [suggested replacement]

## Drifted claims
- [quoted line] → [what the source actually says] → [suggested replacement]

## Checked and supported: N claims
## Restricted evidence used: [list, or none]
```

## What to look for

- **Overclaimed capability.** Check every capability against the claim vs
  reality table on **Product and offers**. A claim described more generally
  than the table allows is a violation, even if it sounds reasonable.
- **Category slippage.** The claimed category presented as established fact,
  or one category layer swapped for another. See **Ecosystem**.
- **Numbers that drift.** "A 32% conversion lift" becoming "a third more
  conversions", or "2,000+ customers" becoming "thousands of enterprises".
  Rounding and restating are the most common drift and the hardest to spot,
  because the new version usually sounds more careful than the original.
- **Proof that doesn't match its claim.** A stat about speed under a claim
  about revenue. Check the matching guidance on **Evidence**.
- **Banned vocabulary and punctuation.** Check against the list on **Brand
  voice** rather than from memory.
- **Say/don't-say substitutions.** See **Messaging**.
- **Off-limits leakage.** Any sentence a reader could use to infer something
  the non-negotiables put off limits, such as what a plan includes.
- **Restricted evidence.** Cross-check every customer story, logo and quote
  against **Evidence**.
- **Learnings stated as facts.** A provisional entry from **Learnings**
  presented with the confidence of a compiled fact.

## What to avoid

- **Softening violations.** A soft flag on a real violation gets ignored.
  Report findings plainly, and do not pad the report with praise.
- **Fixing silently.** Report every change; never return a corrected draft
  without the findings that explain it.

## Compatibility

- **A document tool connector** or project files holding the System of
  Context. Without it, the check can only flag claims as unverified.
- No code execution needed.
