# Copy constraints

Write one section at a time, and only after the page plan is approved.

## Fact grounding

Every personalized claim traces to a fact ID from the CRM and web research.
Sentences carry numbers, named products and dated events. Category words are
the failure mode: "global retailer", "leading brand", "industry leader" say
nothing and could sit on any page.

Test each sentence by asking whether it would still be true with a different
company's name in it. If it would, it is not personalization.

Claims about the seller's own product follow the same rule in reverse: each
must be consistent with the seller's claim vs reality table. A capability the
table limits is described as the table limits it.

## Length parity

The page has a designed layout. Personalization changes what a field says,
never how much space it takes.

- Every personalized field stays within **±10% of the base field's character count**.
- Repeatable groups keep their base item count. Nine cards stay nine. Three bullets stay three.
- No new sections, no extra paragraphs, no added bullets.
- When a fact is too long for the field, shorten the fact. Cut the qualifier, keep the number.

The lower bound matters as much as the upper one. A field at half its base
length leaves a visible hole in the layout.

### Tight fields will fight you

Short fields are where this gets hard. A 19-character button label or a
20-character feature heading leaves almost no room. Budget these first and
write the long fields around them, rather than discovering at the end that the
only phrase that fits is the one you already ruled out.

### Approved exceptions

Two things must never be altered to fit a character count: a customer quote,
and a person's name. Both are attributable to a real human who said or is
called that thing.

When one falls outside budget, keep it exact, mark it as an exception, and
report it alongside the passing fields. An exception that is named is fine. An
exception that is quietly padded is a fabricated quote.

## The H1

- States the account's stakes, written from their problem, not from a product feature.
- Contains the company name exactly as the company writes it. Respect lowercase and internal spacing (`adidas`, `ABN AMRO`).
- The name appears once, and generally nowhere else on the page. Repeating it reads as mail merge.
- Stays within the base H1's character count + 10%, company name included.
- If the name does not fit, cut other words to make room. Never extend the line.

Draft three or four candidates at the exact character budget and pick, rather
than writing one and trying to trim it. The strongest H1 is usually a fact the
company has already published about itself.

## Voice

Voice rules come from the seller's context and are hard constraints, not
inspiration. Load the brand voice and style guide rather than working from
memory. The defaults in `scripts/length_check.py` are a floor, not the whole
list; copy the seller's banned words into `fields.json`.

Consistent failure modes to watch:

- Superlatives and filler adjectives
- Product or category names the seller's messaging does not use (check its we say / we don't say list)
- Mixed spelling conventions. Match the base page rather than switching mid-page.
- Anything the seller's context puts off limits, such as pricing or packaging
- Punctuation the seller bans. Em dashes are banned by default in the length check; turn that off in `fields.json` only if the seller's style allows them.

Plain and confident beats polished and vague. Short sentences. Specific nouns.

## Worked examples

These use a fictional account, Northwind Freight, to show the mechanics.

**H1. The base is 40 characters, so the cap is 44. The company name is 17 characters.**

Weak: `Personalized pages for Northwind Freight` (40). States the seller's
feature, not the account's stakes.

Strong: `Northwind Freight lost 6 points of margin` (41). Their own disclosure, one
mention of the name.

**Problem card. The base is 46 characters, so the range is 42 to 50.**

Weak: `Struggling to keep up with content demands?` (43). Could be any company.

Strong: `Fuel cost per shipment rose 14% last quarter?` (45). One sourced number.

**Fact too long for the field.**

Fact: "Northwind Freight reported fuel cost per shipment of $412 in Q2, up 14%
on the previous quarter, while shipment volumes were flat at 1.2 million."

Field budget: 42 to 50 characters.

Result: `Fuel cost per shipment rose 14% last quarter?` (45)

The qualifier went, the number stayed.
