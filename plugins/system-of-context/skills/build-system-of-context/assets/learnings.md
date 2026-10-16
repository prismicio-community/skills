# Learnings

**Status:** Owned by {{LEARNINGS_OWNER}}. Empty at initialization. Entries
arrive once campaigns have run long enough to teach something.

## What belongs here

Generalizable findings about how {{COMPANY}}'s market responds. Not
per-campaign performance, not this week's pipeline. This file holds the
durable statements an agent needs loaded **before** it writes.

The test: would this change how we write the *next* page, for a different
account, in three months?

- ✅ "Account pages that open with the account's own published numbers get replies; generic pain-point openers don't."
- ❌ "The Acme page got 340 views and 2 meetings." That is a report, not a learning.
- ❌ "Six accounts went cold this week." That is a status update.

## Provenance

This is the only file in this skill that {{LEARNINGS_OWNER}} writes.
Everything else is compiled from upstream sources and is read-only here.

A compiled fact is company-approved; a learning is an observation from a
finite sample. When the two conflict, surface the conflict rather than
silently preferring either one.

## Lifecycle

Every entry carries a state. A finding from twenty accounts is a hypothesis,
not a law, and context that accumulates unfalsifiable opinions is worse than
context with gaps in it.

| State | Meaning | Rule |
|---|---|---|
| **Provisional** | Observed once, in one cohort | Use it, but say it's provisional if the stakes are high |
| **Confirmed** | Held up in a second, independent cohort | Treat as established |
| **Retired** | Failed to replicate, or the market moved | Delete. Do not soften to "used to be true" |

A provisional entry that hasn't been confirmed within one quarter gets
retired, not extended. If nobody has tried to replicate it, that is itself
the answer.

## Entry format

```
### [Short claim, stated as a rule]
- **State:** provisional | confirmed | retired
- **Observed:** YYYY-MM-DD, [channel or motion], [what the sample was]
- **Evidence:** [what actually happened, with a link]
- **Applies to:** [channel, surface type, or audience segment]
- **Review by:** YYYY-MM-DD
```

Keep the claim narrow enough to be wrong. "Personalized openers work better"
is unfalsifiable and useless. "Account page openers naming the account's
current tool got replies from 7 of 20 accounts, versus 1 of 20 for generic
openers" can be tested again.

Add, confirm and retire entries through the context-refresh skill.

---

*No entries yet.*
