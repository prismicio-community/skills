# Research Protocol (Phase 1)

The goal is not "learn about the topic". It is to answer three questions precisely enough to make outline decisions:

1. What does every ranking page already cover? (table stakes: must be present, must be brief)
2. What does no ranking page cover well? (gaps: the reason this article exists)
3. What does the reader already know, and what are they actually trying to decide?

## 1. SERP analysis

### Searches to run

- The exact target keyword.
- 2–4 variants: question form ("how do I…", "is X worth it"), the comparison form if relevant, and the year-qualified form if the topic is fast-moving.
- One "site:reddit.com" or "reddit" appended search for the same keyword.

Fetch the top 8–10 organic results. Skip results that are pure product pages unless the keyword is commercial. If a result is paywalled or fails to fetch, note it and move on rather than guessing at its contents.

### The coverage matrix

Build this as you read. Subtopics down the side, competing URLs across the top, a mark where a page covers a subtopic with real substance (not a passing mention).

| Subtopic | A | B | C | D | E | Coverage |
| --- | --- | --- | --- | --- | --- | --- |
| Pricing models | x | x | x | x | x | 5/5: table stakes |
| Migration timeline | | x | | | | 1/5: thin gap |
| Team workflow impact | | | | | | 0/5: open gap |

Read the matrix two ways:

- **6+ of 10 cover it** → table stakes. Include it, but cover it faster and more concretely than everyone else. Skipping table stakes reads as an incomplete article; over-explaining them wastes the reader's time.
- **0–2 of 10 cover it** → candidate gap. A gap is only worth taking if the brand can credibly fill it. A gap nobody can fill with evidence is just a topic nobody knows about.
- **Covered but badly** → the most winnable category. Everyone lists the options, nobody says which to pick and why. Everyone names the risk, nobody quantifies it.

### Also capture per result

- Approximate word count and heading structure (H2 list).
- Content formats present: tables, code blocks, screenshots, videos, calculators, original data.
- Publication and last-updated dates. A SERP where the top result is three years old is a freshness opportunity worth naming.
- Whether the page answers in the first paragraph or buries the answer.

### And from the SERP itself

- Featured snippet: what is being extracted, and from where. Matching that format in one section is the cheapest snippet play available.
- "People Also Ask" questions, verbatim. These go straight into FAQ candidates.
- Related searches at the bottom of the page.
- Whether AI Overviews appear, and which sources they cite.

### Structural conclusion

Note the median word count of the top 5 and the dominant structure. Then deliberately choose whether to match or break that structure. If 8 of 10 use the same H2 sequence, copying it guarantees the article reads as the eleventh version of the same page. Reorganize around gaps instead.

## 2. Audience and intent profiling

Answer each of these in one line:

- **Search intent**: informational, commercial investigation, transactional, navigational.
- **Audience level**: beginner, intermediate, expert. If expert, note it explicitly: zero explanatory scaffolding.
- **Decision stage**: awareness, consideration, decision. This determines how the brand appears and how hard the closing invitation works.
- **The job**: what the reader is trying to get done today, in their words.
- **Pain and consequence**: what goes wrong if they choose badly. Specificity here is what makes the intro land.

### Knowledge inference

The query itself reveals what the reader already knows. Use it to decide what NOT to write.

| Query pattern | Reader already knows | Exclude from the outline |
| --- | --- | --- |
| "X vs Y" | What X and Y are | Standalone definitions of either |
| "Best [X]" | What X is, why they need one | "What is X" sections |
| "How to [task]" | The task exists and why it matters | Motivation sections; start at step 1 |
| "X explained" | The term exists | Extended preamble; go to the core explanation |
| "Alternatives to X" | What X is, why they'd switch | Definition of X |
| "X for [audience]" | Their own segment | Generic audience framing |
| "[Task] not working" | The normal path | The happy path; start with causes |

Sections that explain what the reader already knows are the most common quality failure in this format. They are also the easiest to catch: if the section title restates the query's premise, cut it.

## 3. Community mining

Where to look, in rough order of value:

- **Reddit**: append "reddit" to the keyword and the results will mostly be vendor blogs that mention Reddit, not threads. Use `site:reddit.com` plus the keyword, or name the subreddit directly (r/webdev, r/nextjs, r/marketing, r/ExperiencedDevs, r/ContentManagement). Then read two or three threads in full, replies included. Subreddit choice matters more than thread score.
- **Quora**: good for the naive and adjacent framings of the question that practitioners forget people have.
- **Stack Overflow / GitHub issues**: for technical topics, the failure modes people actually hit.
- **Hacker News**: for opinionated counterpoints worth engaging with honestly.
- **LinkedIn / X / niche Slack and Discord recaps**: for how practitioners talk about the topic now.
- **Review sites as a fallback**: G2, Capterra, TrustRadius and the AWS Marketplace review lists. When forum searches come back thin, the "what do you dislike" fields are the closest public equivalent to a customer interview, and they are specific in a way marketing pages never are ("asset management lacks advanced DAM features", "steeper learning curve for the content team than expected"). Treat them as UGC, quote them as opinion rather than fact, and check the review date.

For each useful item, capture:
- The question in the asker's own words, unedited. Marketing rephrasing destroys the value.
- Thread URL and rough date.
- The frustration underneath it. "Why does X keep failing" is usually really "I cannot tell whether X or my config is at fault."
- Any answer that got strong agreement, and any consensus that looks wrong.

These feed four places: FAQ questions, section angles, the intro's tension, and the "common mistakes" section if one is warranted.

## Audience research: find the real buying criteria

For any comparison or listicle, the comparison columns must come from what buyers actually weigh, not from what is easy to tabulate. Feature counts and integration lists are easy to fill in and almost never decide a purchase.

The best source is recorded sales calls, because evaluation criteria are stated out loud in them. Ask a call: what did the customer use to judge the options, what did they ask before deciding, what worried them. Two or three evaluation calls produce a better column set than any amount of desk research.

Look for the questions that repeat across calls. In practice they cluster into five shapes:

- **Evidence** — can it show me the specific thing, not a score?
- **Next action** — what do I do once it tells me something?
- **Provenance** — where does the output come from, and can a competitor get the same?
- **Effort** — how much of this lands on my developers or my team?
- **Disruption** — do I have to change how we already work?

Turn each into a table column and answer it honestly for every tool. If a criterion cannot be answered for most of the list, it is a feature, not a criterion.

Where sales calls are unavailable, use review-site "what do you dislike" fields and buyer threads, and say in the appendix which source the criteria came from.

## Inventory the brand's own site through the CMS

Before planning internal links, list what the brand has already published, from the website in the brand settings:

1. **If the brand's CMS has a connector connected**, search its published content across the topic and its subtopics. Work only in the live repository or space; staging and sandbox content is not live and must never be linked. Semantic search returns a relevance sample rather than a complete list, so run several phrasings.
2. **Otherwise, use the sitemap.** `python scripts/sitemap_inventory.py <website> --match <topic terms>` lists every published URL whose path matches. If the script cannot reach the site, fetch the sitemap with the web fetch tool and filter it the same way.
3. **Only published pages qualify.** Drafts and release-staged documents are not live.
4. **Check indexability before linking.** A landing page can return 200 and still be `noindex, nofollow`, which means it passes no value and cannot itself be cited. Fetch each candidate and read the robots meta tag.

Report both sets: pages worth linking, and pages carrying good material that are currently unindexable. The second list is usually more valuable than the first, because it points at assets the brand already owns but cannot get credit for.

## Output of Phase 1

A research brief containing:
- Coverage matrix with table stakes and gaps labelled.
- Median top-5 word count and dominant structure.
- Audience profile including the knowledge-inference exclusions.
- 8–15 real questions with source URLs.
- A first hypothesis of the differentiating angle, to be tested in the interview.

Keep the chat summary to 4–6 sentences. The full brief goes in the research appendix file.
