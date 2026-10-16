---
name: "geo-action-plan"
description: "Build a GEO/AI-search action plan from an AI visibility tool's tracked prompts: cluster every page AI assistants cite and every page ranking for their fan-out queries, check each topic against the brand's site, and deliver a ranked workbook of pages to create or update plus off-site targets. Use when asked for a GEO or AEO plan, what to publish to show up in ChatGPT or AI search, or to personalize this skill for a brand."
---

# GEO Action Plan

Turn what AI assistants and search engines already retrieve into an executable plan: which pages to create or update on the brand's site, and which third-party pages and threads to get mentioned in.

**The goal is to replicate what is cited and ranking.** Every page that gets cited or ranks for a prompt is evidence of content that engines want. The plan finds every distinct piece of content in that evidence, gives the brand its own version of each, and ranks them so a human can choose. It is a menu of opportunities, ranked. It is not a short list of the plan-maker's favourites.

The plan rests on three layers, all pulled live, never uploaded:

- **Citation layer.** The URLs AI assistants retrieve and cite for the tracked prompts, from the user's AI visibility tool (with Peec AI: `get_url_report` / `get_domain_report`).
- **SERP layer.** The pages that rank for the fan-out queries the engines issue while answering (with Peec AI: `list_search_queries`), then a live `web_search` per intent.
- **The brand's existing estate.** The sitemap and the brand's CMS (see Brand settings), used to decide whether each topic is a new page or an update to one that already exists.

## Brand settings

This skill holds no brand details. They live in a brand settings document the user owns, titled "GEO action plan brand settings", created by the personalization flow below from `assets/brand-settings-template.md`. Never write brand details into this skill's own files.

**At the start of every run, look for it.** Check the assistant's memory and project files for "GEO action plan brand settings", then search the connected document tools (Notion, Google Drive and similar) for a document with that title. If you find it, read it and say in one line which brand and settings you loaded. If you find more than one, ask which to use. If you find none, run without it: every step that needs a setting asks the user at that point, and at the end of the run suggest personalizing once ("Personalize the GEO action plan skill for my brand") so later runs skip those questions.

A setting marked `Not set`, or missing because there is no settings document, means: ask the user at run time, at the step that uses it. Wherever this file says "Brand settings", it means that document, and "the brand" means the brand it describes.

## Personalizing this skill

When the user asks to personalize, set up or customize this skill for their brand, follow `references/personalization.md` instead of running a plan. In short: list the details the skill needs and what each is for, take whatever the user has from wherever it lives (Notion, Google Drive, a PDF, a URL, pasted text), work out what can be read from their own sources, leave anything they don't have as `Not set`, and save the result as the brand settings document wherever the user chooses. The same flow updates an existing settings document.

## Data source: a connected AI visibility tool

The citation and fan-out data comes from the user's AI visibility tool, read through its connector (MCP). Any tool works if its connector provides tracked prompts and cited pages; fan-out queries make the plan much stronger. The skill does not accept CSV exports or pasted data.

**Before Step 0, read `references/data-sources.md`** and check the connected tool against the data it lists (D1–D6). If no connected tool provides tracked prompts and cited pages, stop and tell the user to connect one. If it lacks fan-out queries, say so and ask before running with the fallback described there.

The steps below name Peec AI's tools as the worked example. With another tool, use its equivalent tool for the same data (`references/data-sources.md` has the known mappings) and keep its metrics as reported.

**Where the reference files conflict with this SKILL.md, this file wins.** In particular, `references/plan-methodology.md` says to merge by default, cut weak intents, cap P0s tightly and treat section-level phrasings as H2s only. Those rules are superseded by the clustering method below. Use the reference files for brief templates, the evidence ladder, off-site classification and the technical audit.

## Phase map

| Phase | What happens | Gate |
| --- | --- | --- |
| 0 | Data source check, product docs, visibility-tool project, prompt / topic / tag, time window, sizing check | **Stop and wait** until scope and window are confirmed |
| 1 | Citation layer: cited pages and domains, brands, prompt text, read a few full AI answers | none |
| 2 | SERP layer: fan-out queries, merged into search intents, one live search each, results recorded verbatim | none |
| 3 | **Content clustering**: pool every cited and ranking page, group pages that say the same thing, write one topic title per cluster | none |
| 4 | Existing estate: sitemap, CMS reads, map every cluster to Update or Create, technical audit, reverse gap check | none |
| 5 | Content plan: one row per cluster, all listed, ranked by priority; briefs scaled to priority | none |
| 6 | Off-site targets: classify third-party domains by ownership, pitchable pages, threads | **Stop and wait** until the competitor list is confirmed |
| 7 | Deliver: build, add the Cited Sources and Topic Clusters tabs, validate, present | Script fails loudly on a broken plan |

Phases 1, 2 and 4 are cheap to run wide: batch visibility-tool calls, searches and sitemap or CMS reads in as few turns as possible without summarising between them.

## Step 0 — Set the scope

Ask four things, then work.

1. **Which product should be visible?** If the Brand settings name a positioning source, read it from there (through the connector it names, or ask the user to attach the file if it's a PDF that isn't in the conversation) and use it as the default unless the user gives something else. Otherwise ask for whatever describes it: product URLs, a positioning doc, a Notion page, a Google Drive doc, a PDF. If the settings already record what the product does and the categories it competes and does not compete in, state them back in one line and ask whether they still hold. Record in the Read Me what the product does, the categories it competes in and the categories it does not. Product fit is used for **ranking**, not for exclusion (see Step 5).
2. **Which project?** List the projects (or reports, categories, workspaces: whatever the tool calls them) in the AI visibility tool and match by name; with Peec AI, `list_projects`. Use the project in Brand settings by default.
3. **What scope?**
   - **One tracked prompt** (recommended default). List the tracked prompts (Peec AI: `list_prompts`) and let the user pick. If they ask for "the prompt with the least visibility", pull the own brand's visibility per prompt (Peec AI: `get_brand_report` by `prompt_id`), sorted ascending; on a tie, show the tied prompts and let the user choose. If the tool has no per-prompt visibility, say so and let the user pick.
   - **A topic or tag.** If the tool groups prompts this way, check the fan-out count first (sizing check).
   - **The whole project.** Run prompt by prompt against an accumulating workbook (see "Running across many prompts").
4. **What time window?** Ask; don't default silently. Recommend 30 days. 7–14 days is too thin for stable per-prompt metrics; 60–90 days widens the citation net but mixes engine versions. Flag any prompt created inside the window (partial denominator). Keep the window constant across runs.

State the scope back in one sentence: product, project, prompts, window.

**Coverage is validated, not self-reported.** The build script compares `searches_run` against the searches recorded and `merged_intents`. A run covering under half its merged intents is rejected; any intent without a search goes in the Read Me with a reason.

**Sizing check:** count the fan-out queries for the scope and window (Peec AI: `list_search_queries` with the scope's `prompt_id`, the window and `limit: 1`, then read `totalCount`). Without fan-out queries, count the tracked prompts in scope instead. Under about 120 raw queries, cover them all. Over that, report the number and let the user choose between narrowing the scope or covering by weight. Never silently truncate.

## Step 1 — Pull the citation layer

With the scope's filters applied:

- **Cited pages** (Peec AI: `get_url_report` with `limit` raised to 200, paging with `offset` if `rowCount == limit`). Keep every URL with title, classification, the citation metrics the tool reports (retrievals, citations, citation rate) and mentioned brands. Page through everything the tool returns. Large results are saved to a file; parse them with `jq` or Python rather than reading them into context.
- **Cited domains** (Peec AI: `get_domain_report`) for domain-level classification and the brand's own domain.
- **Brands** (Peec AI: `list_brands`) to resolve brand IDs and find the brand's own.
- **Read two or three full AI answers** (Peec AI: `list_chats` then `get_chat`) to see how engines actually build the answer: what shape it takes (a table by site type, a ranked list, a decision framework), which sources they cite at the top, and what caveats they repeat. This often explains why a brand is retrieved but not named.

Record the page-type distribution, top domains, UGC share and whether the own domain appears. See `references/evidence-analysis.md`.

## Step 2 — Build the SERP layer

Pull every fan-out query for the scope (Peec AI: `list_search_queries`, paging until `totalCount` is exhausted). If the tool has no fan-out queries and the user agreed to the fallback, use the tracked prompts in scope, phrased as searches, and record that in the Read Me and Method. Then:

1. **Merge queries into search intents.** Deduplicate exact and near-exact strings and merge queries that would clearly return the same results. An intent's weight is the sum of its members' occurrence counts. (This merge only decides how many searches to run. Content clustering happens later and works on pages, not queries.)
2. **Search.** One `web_search` per intent, using the query close to verbatim.
3. **Record verbatim.** Every returned result's URL and title, exactly as returned, into the run JSON. Don't filter by your opinion of quality.

Method caveats every time: the search tool returns roughly the top 10 per query, and it is not literally Google.

## Step 3 — Cluster the content (the core of the plan)

This step decides what goes in the plan. Do it before looking at the brand's site, so the existing estate doesn't bias which topics you see.

### 3a. Pool every page

Build one list of every page from both layers: all cited/retrieved URLs from Step 1 and all SERP results from Step 2, deduplicated by normalised URL. Keep for each page its title (use the URL slug when the title is missing), its layer(s) and its metrics: retrievals and citations for the citation layer, number of intents and weight for the SERP layer.

Set aside, but don't discard:
- **UGC** (Reddit, Quora, Facebook, LinkedIn posts, YouTube videos). These go to the Threads and Off-site tabs. A UGC page can also join a content cluster as a demand signal when it asks or answers the same thing, but a cluster made only of UGC is not a content topic.
- **Pages that aren't content**: homepages, pricing pages, login pages, vendor docs and help-centre articles, pure data trackers (W3Techs pages). Note them in the Read Me; they can still be off-site targets.

### 3b. Group pages by what they say

**A cluster is a set of pages that would tell a reader essentially the same thing.** Group by the substance of the page: the question it answers, the subject it covers, the information a reader would come away with. Do not group by format (listicle, guide, comparison) and do not group by surface keywords.

If Brand settings include category examples, use them alongside the examples below; they show the same rules in the brand's own category.

Examples of correct clusters:
- "Sanity vs Contentful 2026: Which Headless CMS Wins?" + "Contentful vs Sanity: Which Headless CMS is Best for You?" are one cluster (same two products, same decision).
- "Best Headless CMS for Enterprise" + "Top 7 Enterprise-Ready Headless CMSs" + "Best Headless CMS for Large Businesses" are one cluster (same audience, same question).
- "Why Your WordPress Site Keeps Breaking After Updates" + "Top 12 WordPress Plugin Vulnerabilities" + "Do Plugins Slow Your WordPress Site?" are one cluster: different formats, but they all explain the same underlying problem (plugins causing breakage, slowness and security risk).

Examples of what is **not** one cluster:
- "Sanity vs Contentful" and "Sanity vs Strapi vs Contentful vs Payload". Both are comparisons, but they compare different sets of products and answer different questions. Two clusters.
- "Best headless CMS for enterprise" and "Best headless CMS for agencies". Same format, different audience and criteria. Two clusters.
- "WordPress alternatives" and "Why people are leaving WordPress". Related, but one lists destinations and the other explains reasons. Two clusters.

The test: if the brand published one page that fully answered member A, would a reader of member B still need a different page? If not, A and B belong together. If yes, they're separate clusters.

Work through the pooled list in order of evidence strength, not alphabetically. A single page can form its own cluster if nothing else says the same thing; keep it.

### 3c. Write one topic title per cluster

Each cluster becomes one topic the brand can publish: the brand's own version of what all the members say. Not a copy of any one member.

The title must read like a real blog post or page title that a person would click: a complete, natural headline. Test it by asking whether it could sit as the H1 of a published article.

- Good: "Why WordPress Sites Keep Breaking: Plugins, Updates and Security Risks"
- Good: "Sanity vs Contentful: Which Headless CMS Should You Choose in 2026?"
- Good: "Best Headless CMS for Enterprise Teams in 2026"
- Bad: "WordPress security plugin" (a keyword fragment, not a title)
- Bad: "Headless CMS enterprise adoption official" (a fan-out query pasted as a title)
- Bad: "The Content Velocity Playbook" (invented; traces to nothing in the cluster)

Build the title from the members' own titles and the fan-out phrasing: keep the shared subject and the wording buyers and engines use, then phrase it as a headline. Record the member title it most closely follows as `title_evidence` (source "cited page title" or "ranking page title"), so the build script can trace it.

### 3d. Record the clusters

Each cluster goes into `run.json` under `clusters` with every member, so the user can see exactly which pages back each topic:

```json
{"id": "C07", "topic": "Sanity vs Contentful: Which Headless CMS Should You Choose in 2026?",
 "fit": "High", "action": "Create", "existing_url": "", "plan_row": 12,
 "members": [
   {"url": "https://pagepro.co/blog/sanity-vs-contentful/", "title": "Sanity vs Contentful 2026: Which Headless CMS Wins?", "layer": "SERP", "metric": "1 intent (w3)"},
   {"url": "https://www.trantorinc.com/blog/contentful-vs-sanity", "title": "Contentful vs Sanity: Which Headless CMS is Best for You?", "layer": "SERP", "metric": "1 intent (w3)"}]}
```

Expect many clusters. A single prompt with 200 cited URLs and about 120 SERP pages typically yields 30–60 content clusters. Fewer than 20 almost always means pages were grouped by format or by keyword instead of by substance; go back and split.

## Step 4 — Map every cluster to the brand's site

Read `references/site-inventory.md` for the method. In brief:

- **The sitemap is the spine.** Fetch the sitemap from Brand settings (default `<website>/sitemap.xml`), follow sitemap indexes, collect every `<loc>`. If the website isn't set, ask for it. A CMS connector's search returns relevance samples, so it is not an inventory.
- **For every cluster, look for an existing brand page that covers the same content**, by slug, by title and, where ambiguous, by fetching it. Look for families, not just exact matches: if the clusters include "best headless CMS for enterprise", check every `/blog/best-headless-cms-*` page, because the brand often already has the sibling. Use the page families in Brand settings, and spot others in the sitemap.
- **Assign an action per cluster:**
  - **Update**: the brand has a page on the same content. The `url` is that page. This is the default whenever a version exists, even if it's weak, old or framed differently.
  - **Create**: no brand page covers it.
  - **Retarget**: a strong brand page exists under the wrong title or framing; retitle it and edit sections rather than creating a new page.
  - **Consolidate**: two or more brand pages compete for the same cluster.
  - **Keep**: a brand page already appears in the evidence and serves the cluster well; record it so nobody duplicates it.
  - **Fix**: a technical blocker (noindex, blocked crawler).
- **Read Update candidates** through the CMS named in Brand settings (its connector's search, then a full document read) or a live fetch, so the brief is a diff: keep / change / add.
- **Technical audit**: meta robots, robots.txt for GPTBot / ClaudeBot / PerplexityBot / Google-Extended, llms.txt, and whether content is in the server-rendered HTML.
- **Reverse gap check**: topic-relevant brand pages that match no cluster get a line in the Read Me ("reviewed, intentionally untouched", with a reason).

## Step 5 — Build the content plan: every cluster, ranked

**One plan row per content cluster. List them all.** Don't cut topics because they seem off-category or low volume. A human reviews the list and decides what to commission; the plan's job is to make sure nothing in the evidence is missed and that the order is sensible.

### Ranking

Score each cluster on five things and assign a priority:

1. **Evidence strength**: number of member pages, total retrievals and citations, SERP weight.
2. **Prompt match**: does the topic answer a tracked prompt in scope directly, or only touch it?
3. **Product fit**: High (the brand's category and ICP), Medium (adjacent, a mention could still sell), Low (outside the category). Use the "competes in" and "does not compete in" lists from Brand settings and Step 0.
4. **Winnability**: incumbent strength, and whether the brand already has a page (Update rows are usually cheaper wins).
5. **Readiness**: whether the brand has the asset the angle needs (data, a customer story, testing).

- **P0**: strong evidence, direct prompt match, High fit, startable now. Usually 10–15% of rows.
- **P1**: strong on most of the five, or High fit with moderate evidence.
- **P2**: everything else, including all Low-fit topics. Low fit lowers priority; it never removes a topic.

Sort the Content Plan by priority, then by evidence strength. Put the fit rating at the start of the "Why this page" cell (`FIT: High`) so it can be filtered.

### What each row carries

- **Title**: the cluster's topic title from Step 3c.
- **Action and URL**: from Step 4. Update rows name the existing brand URL.
- **Title evidence**: the member title it follows, with source.
- **Sources to beat**: the strongest 3–6 cluster members with real metrics, labelled by layer. The full member list is in the Topic Clusters tab.
- **Why this page**: fit rating; cluster size and evidence; what the members agree on; what they miss (the angle). Note which members were actually read.
- **Brief**, scaled to priority:
  - **P0 and P1**: full brief per `references/brief-standards.md`. Read the top 2–3 members first (the tool's indexed page content where it has it, such as Peec AI's `get_url_content`, otherwise a fetch) so the angle rests on a gap you observed. Give the H2 structure, the differentiator, the honesty instruction (name competitors fairly, say when the brand isn't the right fit), and for Updates a keep / change / add diff against the live page.
  - **P2**: a short brief, with the angle in a sentence or two plus 3–5 starter H2s. Mark it "incumbents not read" if they weren't.
- **A P0 row may not rest on an unread incumbent.** Read it, which is free for anything in the citation layer, or drop the row to P1 and mark it unverified.
- **Depends on**: the asset the angle needs, flagged when the brand doesn't have it. If the strongest version needs an asset the brand lacks, also plan the version it can do now (see "The evidence ladder" in `references/plan-methodology.md`).
- **Guardrail**: which neighbouring rows this page must not overlap with, by row number.

### Overlap rules (kept, adapted)

Clustering already ensures each row is distinct content. Two final checks:
- **No two rows may have the same title evidence** (the script rejects it).
- **If two rows' H2 outlines share more than one section, the clusters were split too finely.** Merge them, or move the shared section to one row and link to it from the other.

### Never invent

URLs, titles, counts, classifications and page content come verbatim from the AI visibility tool, a search run in this session or a page fetched in this session. Briefs request numbers the brand must supply; they never supply them. Competitor claims come only from pages read or the positioning doc.

## Step 6 — Off-site targets

Read `references/offsite-targets.md`. The core insight: **a publisher's willingness to mention the brand depends on whether the publisher's company competes in the brand's category, not on the article's topic.** Classify every third-party domain in either layer by ownership, judged from the domain's own homepage: Independent, Non-competing vendor, Adjacent vendor, Direct competitor, Review platform, UGC, or Verify when unclear.

**Confirm the competitor list with the user before classifying.** Propose it from the tool's brand data and the brands dominating the prompts, and add the direct competitors and neighbouring groups from Brand settings, and ask which other neighbouring groups also count.

Pitchable targets get the page, the evidence metric, the ask, the offer, and a contact route only if found on the page. Also look for **data and directory sources** engines cite as adoption evidence (tech-detection sites, switching studies, "companies using X" profiles): if the brand is missing from them, that's often the highest-value off-site fix. Threads get a comment angle with disclosure, never a drafted comment. Competitor-owned pages go on the "unlikely" list.

## Step 7 — Deliver

Build the run JSON (schema at the top of `scripts/build_geo_workbook.py`, plus the `clusters` array from Step 3d), then:

```bash
python scripts/build_geo_workbook.py run.json output.xlsx
```

Then add the **Cited Sources** and **Topic Clusters** tabs, which the build script doesn't produce. Run `python scripts/add_tabs.py run.json output.xlsx` (the same code is below for reference):

```python
import json, sys
from openpyxl import load_workbook
from openpyxl.styles import Alignment, Font, PatternFill
run = json.load(open(sys.argv[1])); wb = load_workbook(sys.argv[2])
H = PatternFill("solid", fgColor="1F3864"); HF = Font(color="FFFFFF", bold=True)
def sheet(name, head, rows, widths, after):
    if name in wb.sheetnames: del wb[name]
    ws = wb.create_sheet(name, wb.sheetnames.index(after) + 1)
    ws.append(head)
    for r in rows: ws.append(r)
    for i, w in enumerate(widths): ws.column_dimensions[chr(65 + i)].width = w
    for c in ws[1]: c.fill, c.font = H, HF
    for row in ws.iter_rows(min_row=2):
        for c in row: c.alignment = Alignment(wrap_text=True, vertical="top")
    ws.freeze_panes = "A2"
cid = {}
for c in run.get("clusters", []):
    for m in c["members"]: cid.setdefault(m["url"].rstrip("/").lower(), c["id"])
src = sorted(run.get("citation_sources", []), key=lambda s: (-(s.get("retrievals") or 0), -(s.get("citations") or 0)))
sheet("Cited Sources", ["URL", "Title", "Domain", "Page type", "Retrievals", "Citations", "Citation rate", "Brands mentioned", "Cluster"],
      [[s["url"], s.get("title", ""), s.get("domain", ""), s.get("classification", ""), s.get("retrievals"), s.get("citations"),
        s.get("citation_rate"), ", ".join(s.get("mentioned_brands", [])), cid.get(s["url"].rstrip("/").lower(), "")] for s in src],
      [60, 50, 24, 14, 11, 11, 11, 50, 9], "Read Me")
rows = []
for c in run.get("clusters", []):
    for i, m in enumerate(c["members"]):
        rows.append([c["id"] if i == 0 else "", c["topic"] if i == 0 else "", c.get("fit", "") if i == 0 else "",
                     c.get("action", "") if i == 0 else "", c.get("existing_url", "") if i == 0 else "",
                     c.get("plan_row", "") if i == 0 else "", m["title"], m["url"], m["layer"], m["metric"]])
sheet("Topic Clusters", ["Cluster", "Topic (brand title)", "Fit", "Action", "Existing brand page", "Plan row",
                         "Member page title", "Member URL", "Layer", "Metric"], rows,
      [8, 46, 8, 10, 40, 8, 50, 55, 9, 26], "Cited Sources")
wb.save(sys.argv[2]); print("tabs:", wb.sheetnames)
```

Final tab order: Read Me · Cited Sources · Topic Clusters · Coverage · SERP Pages · SERP Domains · Site Inventory · Content Plan · Off-site Targets · Threads · Method.

**Google Sheet.** If a Google Drive connector is available, run `python scripts/upload_to_drive.py output.xlsx "<title>"`. Only pass the payload to the Google Drive connector's create-file tool if it's small enough to copy exactly (roughly under 20,000 base64 characters); a single wrong character corrupts the file. If it's larger, deliver the xlsx and tell the user it opens as a Sheet once uploaded to Drive.

**Always send the xlsx** to the user.

In chat, lead with the numbers (pages pooled, clusters found, Update vs Create split, P0 count), then the 2–4 findings that matter: why the brand is or isn't being named, which existing brand pages are the cheapest wins, and the biggest off-site gap. Keep it prose.

## Running across many prompts

State lives in the `_state.json` the build script writes. Store it where Brand settings say plans and state go (Google Drive by default), because the working filesystem resets between sessions. Each new run: fetch the state from there, run Steps 0–6 for the new prompt, then `python scripts/build_geo_workbook.py new_run.json output.xlsx --merge state.json`, and re-run `add_tabs.py` on the merged run.

**Clusters carry across runs.** Before creating a new cluster, check whether an existing cluster from an earlier prompt already covers the same content. If it does, add the new members to it and add the new prompt to that row's prompts; don't create a duplicate topic. The Coverage tab records which prompts have been run. Re-running a prompt already covered replaces that prompt's contribution by default and keeps the earlier run as history; ask first if the user wants to compare plans over time.

## Quality checklist before delivering

- Scope, window and product categories (in and out) are recorded in the Read Me.
- Every non-UGC, content-type page from both layers belongs to exactly one cluster, and the Topic Clusters tab lists every member.
- Clusters are grouped by what the pages say, not by format or keyword. Same products compared = one cluster; different products compared = different clusters.
- Every topic title reads like a real headline, and its title evidence traces to a member page.
- Every cluster was checked against the full sitemap; existing brand pages (including sibling families like `/blog/best-headless-cms-*`) are Update rows, not new Creates.
- Every cluster is a plan row. Low-fit topics are ranked P2, not removed.
- Competitor comparisons seen in the evidence (e.g. Sanity vs Contentful) are captured as rows.
- P0/P1 rows have full briefs based on incumbents actually read; P2 rows have short briefs marked accordingly.
- No brief contains a statistic the brand didn't supply.
- The Cited Sources tab lists every citation-layer URL with metrics and its cluster.
- Off-site competitor list was confirmed with the user; competitor pages are only on the "unlikely" list.
- The build script validated the plan, and `add_tabs.py` ran.

## Compatibility

- **An AI visibility tool connector is required.** It must provide tracked prompts and the pages AI assistants cite for them; fan-out queries are strongly recommended. See `references/data-sources.md`.
- **Web search is required** for the SERP layer and for reading ranking pages.
- **Code execution is required** to build and validate the workbook with the bundled scripts in `scripts/` (Python 3 with `openpyxl`).
- **Optional connectors:** the brand's CMS (to read existing pages), Google Drive (Google Sheet output and run state), and a document tool such as Notion or Google Drive (positioning material and the brand settings document).
