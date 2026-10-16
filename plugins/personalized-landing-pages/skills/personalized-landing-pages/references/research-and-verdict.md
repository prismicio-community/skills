# Research and the fit verdict

## CRM: getting real engagement history

Search the company first, then pull its engagements. Engagements are often
attached to contacts rather than to the company, so query both.

Example with HubSpot (adapt the object names to whichever CRM is connected):

```
search_crm_objects(objectType=COMPANY, query="<company name>")
search_crm_objects(objectType=NOTE|MEETING|EMAIL|CALL|DEAL,
  filterGroups=[{associatedWith:[{objectType:"companies",
                                  objectIdValues:[<ids>], operator:"IN"}]}])
```

If company-associated engagements come back empty, repeat the query with
`objectType:"contacts"` and the associated contact IDs. An empty result on one
object type is not evidence the account is cold.

In Salesforce or similar, the equivalent is the Account, its Contacts, and the
Activities, Tasks, Events and Opportunities related to both.

If a call recorder is connected, look for transcripts with the account. They
are the best source of the account's own words.

### The junk-record trap

Companies with consumer-facing subdomains generate auto-created CRM records
from your own colleagues' activity. A travel company will produce records for
its booking subdomains; a retailer will produce records from order
confirmations.

These records look real. They have lifecycle stages, owners and contacts. They
contain no account engagement whatsoever, and the "contacts" on them are often
your own employees or unrelated consumers.

Check what the engagement actually is before using it. If the email is a
holiday booking confirmation rather than a sales conversation, exclude the
record and say you excluded it. Reporting a fake engagement as a warm signal
is worse than reporting a cold account.

### Division and entity mismatches

A call note from a different division than the target account is still
usable, but phrase it at group level rather than as the target's own words.
Flag the mismatch rather than blurring it.

Similarly, a contact who has explicitly declined is a fact about the account,
not an absence of facts. If someone replied that they are not involved in
evaluating tooling, do not build the page around them, and do say so.

## Web research schema

Answer these for every account. Each fact gets a source URL or an uncertainty
flag, and an ID like `W3` so copy can cite it later.

1. How the company makes money and how it sells
2. Its web estate and stack
3. Whether it markets to named accounts or a mass audience
4. Concrete hooks from the last twelve months: numbers, named products, dated events
5. Uncertainties, flagged rather than asserted

Carry the seller's offers table into the research brief, so facts get
collected for a decision rather than as trivia. If the table's fit signals
mention something (stack, team shape, an initiative), research it explicitly.

### Source quality

Rank sources by how hard they are to dismiss:

1. The company's own regulatory filings and earnings materials
2. The company's own newsroom and published posts
3. Their own words in a call transcript or CRM note
4. Established trade press
5. A trade blog or aggregator

Anything at rank 4 or 5 gets softened in the copy. Do not assert a named
partnership on the strength of a single trade blog; describe the underlying
shift instead.

## The verdict

Score the account against each row of the seller's offers table: how many
good-fit signals the research supports, and whether any "not a fit when"
condition is true. One "not a fit" condition is enough to exclude an offer,
however many fit signals it has.

Emit one ranking plus an explicit exclusion list, each with a one-line reason
that cites fact IDs:

```
Offer B > Offer A
Offer C excluded: no named-account motion, consumer brand (W2, W4)
Offer D excluded: in-house stack built last year, far outside ICP (W3)
```

### Sanity checks before locking a verdict

- **Does the account already do this better than we could help with?** A large
  in-house team doing the exact thing an offer sells is a reason to rank that
  offer lower, not higher.
- **Do the CRM contacts match the offer?** Contacts in the wrong function do
  not signal the motion, whatever the company's other divisions look like.
- **Is the account inside the ICP?** If not, say so plainly at the gate. It
  changes how the account owner should use the page.
- **Does the last real conversation point somewhere?** If a logged call spent
  most of its time on one offer, that is the strongest signal available.
  Weight it accordingly.
- **Does a learning apply?** If the seller's context has a confirmed learning
  about this kind of account, apply it and cite it.

### When the verdict conflicts with the base page

This happens whenever the base page was built for one offer and the account
needs another. It matters because the offer is usually baked into sections
classified as fixed: eyebrows, how-it-works steps, FAQ questions, and
functional fields that drive live widgets.

**Stop and present the conflict.** Show which fixed sections hard-code the
wrong offer, then give the options:

- Use a different base page built for the chosen offer, if one exists in the
  repository. Search for it before offering this.
- Keep the base page and reclassify the offending fixed sections as
  personalizable, rewriting the mechanism to match the verdict. Same sections,
  same item counts, same length budget.
- Keep the base page and run its original offer, overriding the verdict. Name
  what is weak about this before anyone picks it.

Do not pick for them. Recommend one, explain why, and wait.

### Functional fields are not copy

Some fields drive behavior rather than display text: identifiers, form links,
feature switches. Changing one to match a rewritten page can break a live
widget or promise something the product does not do yet.

Leave functional fields alone unless someone confirms the new value is
supported, and write the surrounding copy so it does not over-promise. Flag
the gap between what the page says and what the product currently does
rather than papering over it.

## Customer evidence

Use only proof points the seller has approved. Check restrictions before
reusing any customer story. Some are restricted to a direct link and cannot be
quoted, excerpted or rebuilt into a page module, however well they fit.

A restricted story that fits perfectly is still restricted. Mention it to the
account owner as something to send directly, and use an approved story on the
page.

When no approved story exists for the chosen offer, stop and ask which to use.
Then make the page claim only what that story actually proves. A story about
speed does not prove a revenue outcome, and saying so protects the page from
the first hard question it gets.
