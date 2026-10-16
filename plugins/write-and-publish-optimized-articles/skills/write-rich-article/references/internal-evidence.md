# Internal Evidence (Phase 2)

Public research tells you what everyone knows. Internal evidence is where the article gets something no competitor can copy: the company's actual positioning, and the words real buyers used.

Work through every source listed under Knowledge sources and Positioning and messaging sources in the brand settings, plus anything the user shared in this conversation. When a source is unavailable, say so in one line rather than silently skipping it. The user may be able to connect it or paste the material. With no internal sources at all, the article still works: Phase 3's interview becomes the main source of point of view, and the deliverable says so.

If a tool is not in the current tool list, run `tool_search` for it before concluding it is unavailable. Connectors are frequently deferred rather than absent.

## Call recordings (Gong, Modjo, Chorus, Fathom or similar)

The highest-value source, and the one most often skipped. Sales and customer calls give three things nothing else does: the objection that comes up every time, the vocabulary buyers actually use, and the question they ask right before they decide.

Search for: the target keyword, the competitor names in the keyword, the product area, and the pain phrasing from Phase 1.

Extract:
- **Recurring questions**: anything asked on three or more calls is an FAQ entry, phrased the way the customer phrased it.
- **Objections and the answers that worked.** An objection handled honestly in an article is worth more than any feature paragraph.
- **Verbatim customer language.** If buyers say "content ops" and the industry writes "editorial workflow orchestration", use theirs.
- **Failure stories.** What went wrong at a customer before they switched, with the shape of the story kept and identifying details removed.
- **What surprised the rep.** The gap between what the company thinks matters and what the buyer asks about is often the article's angle.

Anonymise. No company names, no individuals, no deal specifics unless the user confirms the account is a public reference.

## Knowledge base (Notion, Confluence, Coda or similar)

Start with the positioning and messaging sources named in the brand settings, then search for: "positioning", "messaging", "POV", "narrative", "competitive", "objection handling", "brand voice", "product principles", plus the topic keyword. Also check meeting notes for the topic. Strategy debates recorded in meeting notes are often more candid and more useful than the polished positioning doc.

Extract: the company's stated position on the topic, claims that have been approved for use, claims explicitly ruled out, defined terms and frameworks the company already uses, and any internal numbers with their provenance.

A named framework the company already owns is worth searching for specifically. Reusing it strengthens both the article and the framework; inventing a parallel one fragments the brand.

## File storage (Google Drive, SharePoint, Dropbox or similar)

Search for: strategy decks, competitive teardowns, customer research, win/loss analysis, launch briefs, and analyst material relating to the topic.

Extract the same categories as the knowledge base, plus any chart, benchmark, or dataset that could become an original visual in the article. Original data is the single most citable asset a page can carry.

Check the document date. A positioning doc from two product cycles ago can be actively wrong.

## The brand's website and CMS

Two jobs here.

1. **Duplication check.** Does a strong published page already target this keyword? If yes, stop and tell the user before writing a competitor to their own page. Updating usually beats publishing.
2. **Internal link inventory.** Collect candidate URLs with their titles and topics for Phase 6. Pull from the CMS connector if one is connected, and from the sitemap (`python scripts/sitemap_inventory.py <website> --match <topic terms>`, which follows sitemap indexes). Prefer pages at adjacent funnel stages, relevant docs and feature pages, and deeper education content on subtopics this article will only touch briefly.

## Reconciling internal evidence with public research

The interesting output of this phase is usually a contradiction. Three shapes worth carrying into the interview:

- **The SERP says X, internal evidence says the opposite.** This is the strongest possible article angle, if it can be supported.
- **Customers ask about something no ranking page addresses.** Straight to a section or an FAQ.
- **The positioning doc claims something no evidence supports.** Do not launder it into the article. Flag it as a claim needing a source.

## Attribution ledger

Record every extracted item as: claim or quote, source type, specific document or call reference, date, and whether it is publishable as-is. Anything that reaches the draft as a factual statement must be traceable back through this ledger, and anything that cannot be sourced gets hedged or cut in Phase 7.
