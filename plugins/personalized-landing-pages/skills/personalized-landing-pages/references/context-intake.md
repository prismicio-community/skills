# Context intake

The pages sell the user's own company (the seller). Before researching any
account, collect five things about the seller. Load them from an installed
context skill when one exists; ask only for what is missing.

## What the pipeline needs

| Need | Used in | Without it |
|---|---|---|
| **Offers table** | Step 4, the verdict | No verdict, so no point of view. Cannot skip. |
| Claim vs reality | Steps 6 and 7 | Pages overclaim what the product does. |
| Approved proof points and restrictions | Steps 5 and 6 | Invented or restricted proof ends up on a page. |
| Voice rules and banned words | Steps 6 and 7 | Pages sound generic, and the length check only catches the default list. |
| ICP | Step 4 | Out-of-profile accounts are not flagged. |

## Where to look, in order

1. **A System of Context.** Documents titled "<Company> System of Context",
   built with the build-system-of-context skill. Check the assistant's memory
   and project files, then search the connected document tools. Read:
   - **Product and offers**: the offers table and the claim vs reality table
   - **Evidence**: proof points and restrictions
   - **Brand voice** and **Style guide**
   - **ICP**
   - **Learnings**: anything confirmed about what works on pages
   Respect the non-negotiables on its overview page for the whole run.
2. **Other brand material.** Brand guidelines, a messaging doc, a voice guide,
   a company overview. Use what it covers and note what it doesn't.
3. **The intake below**, for whatever is still missing.

If the seller has no context layer at all, mention once that the
build-system-of-context skill can build one, then run the intake.

## The intake

Ask in one batch. Pre-fill from the seller's website where you can and ask
the user to correct, rather than asking them to write from scratch.

1. **Offers.** "What do you sell, as separate offers? For each: what signals
   tell you an account is a good fit, what tells you it isn't, and which
   customer story proves it?" Produce the table:

   ```
   | Offer | What it is | Good-fit signals | Not a fit when | Proof to use |
   ```

   Signals must be observable from research: business model, how they sell,
   web estate, team shape, stack, stated initiatives. Push back on adjectives
   like "innovative companies".

2. **Claims to avoid.** "Is there anything your site says that the product
   doesn't fully do today, or any topic pages must not mention, such as
   pricing?"

3. **Proof.** "Which customer stories, numbers and quotes are approved for
   pages, and do any have restrictions (link only, no quotes, internal
   only)?"

4. **Voice.** "Any banned words, banned punctuation, or spelling convention?
   Or point me to your brand guidelines."

5. **ICP.** "Who is a great-fit account, in two sentences?"

Save the answers as a document titled "Personalized landing pages seller
settings", in the document tool the user chooses (or the assistant's memory or
project files), and tell the user where it is. At the start of every later run,
look for that document before running the intake again.

## Using the context during the run

- Copy the seller's banned words into `fields.json` so the length check
  enforces them.
- Every capability claim on a page must survive the claim vs reality table.
- Every proof point must come from the approved list, respecting
  restrictions.
- When the context and the user's instruction conflict, surface it; do not
  silently pick one.
