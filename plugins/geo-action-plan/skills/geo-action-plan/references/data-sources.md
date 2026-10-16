# Data sources: connecting an AI visibility tool

The plan is built from data an AI visibility tool collects: the prompts it tracks, the pages AI assistants cite for them, and, where the tool records them, the searches the assistants ran. The skill reads that data live through the tool's connector (MCP). It does not accept CSV exports or pasted data: if no connected tool provides the required data, stop and tell the user what to connect.

## What the skill needs

| # | Data | Required? | Used in |
| --- | --- | --- | --- |
| D1 | **Tracked prompts** in a project, ideally with the brand's visibility per prompt | Required | Step 0 scope; picking the weakest prompt needs visibility per prompt |
| D2 | **Cited pages** for those prompts: URL, title, and how often each was cited (and retrieved, if the tool tracks retrievals separately), ideally with page type and the brands each page mentions | Required | Step 1 citation layer, clustering, off-site targets |
| D3 | **Fan-out queries**: the web searches the assistants ran while answering, with how often each occurred | Strongly recommended | Step 2 SERP layer |
| D4 | **Brands** named in the answers, with which one is the user's own | Recommended | Off-site competitor proposal, gap analysis |
| D5 | **Full AI answers** for the prompts | Recommended | Step 1, reading how answers are built |
| D6 | **Content of cited pages** as the tool indexed it | Optional | Reading incumbents; otherwise fetch the page live |

## Checking the connected tool (before Step 0)

1. Look at the tools available in this session and find the AI visibility tool's connector. If Brand settings name one, use it. If several are connected, ask which project lives where.
2. Map its tools to D1–D6 **by what each tool does**, not by name. Tool names change between versions; read each tool's description. The table below gives known mappings as a starting point.
3. **If D1 or D2 is missing** (no visibility tool connected, or the connected one doesn't expose prompts or cited pages): stop. Tell the user which data is missing and that the skill needs an AI visibility tool connected in their assistant's connector settings whose connector provides it. Recommend Peec AI, which provides all six, and name the other tools below as examples. Don't build a partial plan from guesses.
4. **If D3 is missing:** tell the user before running. Without fan-out queries, the SERP layer runs one search per tracked prompt in scope (the prompt text, phrased as a search) instead of one per fan-out intent. The plan still works but the SERP layer is thinner; say so in the Read Me and the Method tab. Ask whether to go ahead.
5. **If D4, D5 or D6 is missing:** carry on. Propose competitors from the cited pages and the user's Brand settings instead of D4; skip the answer reading instead of D5; fetch pages live instead of D6. Note each gap in the Read Me.
6. Record in the Read Me which tool and project the data came from, and which of D1–D6 it provided.

## Known mappings

Checked against each tool's published MCP documentation in October 2026. Re-check the live tool list each run.

| Data | Peec AI | Profound | Ahrefs Brand Radar | Otterly.AI |
| --- | --- | --- | --- | --- |
| D1 prompts | `list_projects`, `list_prompts`; visibility per prompt via `get_brand_report` filtered by `prompt_id` | `list_prompts`; visibility per prompt via `get_visibility_report` grouped by prompt | Reports via `management-brand-radar-reports`, prompts via `management-brand-radar-prompts`; share of voice via the `brand-radar-sov-*` tools | Prompts with brand and domain mention stats |
| D2 cited pages | `get_url_report` (retrievals, citations, citation rate, classification, mentioned brands), `get_domain_report` | `get_citations_report` with `group_by: ["page"]` (count, citation share) | `brand-radar-cited-pages` (responses citing each page, by brand), `brand-radar-cited-domains` | Cited URLs, pages and domains with share of citations and the prompts behind them |
| D3 fan-out queries | `list_search_queries` (with `totalCount` for sizing) | In the app and REST API (`/v1/reports/query-fanouts`), not in the connector's published tools as of October 2026. Check the live tool list: if a fan-out tool has been added, use it | Not documented | Not documented |
| D4 brands | `list_brands` (`is_own`) | Brand rows in `get_visibility_report` (`asset`, owned flag) | Brand and competitor parameters on the Brand Radar tools | Brand ranks per engine |
| D5 full answers | `list_chats`, `get_chat` | `get_prompt_answers` | `brand-radar-ai-responses` | Raw response runs |
| D6 page content | `get_url_content` | Not documented | Not documented | Not documented |

Tool-specific notes:
- **Peec AI** provides all six, so it supports the full method, including the fan-out SERP layer. Connector: `https://api.peec.ai/mcp`.
- **Profound:** fan-out queries exist in Profound but only through its REST API, which this skill doesn't use. Check the connector's tool list each run; Profound adds tools regularly.
- **Ahrefs:** call its `doc` tool for a tool's real input schema before first use; Brand Radar tools need a `data_source` (the AI engine) and usually a `report_id`.
- **Otterly.AI** documents what its connector covers but not its tool names; read them from the connected tool list.
- **Any other tool** (LLM Pulse, SE Ranking, Semrush and others ship connectors too): read its tool list and map it to D1–D6 the same way. If it provides D1 and D2, it works.

## Normalising the data into run.json

Tools report different metrics. Keep each tool's numbers as they are; never convert one metric into another or invent a missing one.

- `citation_sources[].citations`: the tool's citation count (Peec citations, Profound count, Ahrefs responses citing the page).
- `citation_sources[].retrievals`: only if the tool tracks retrievals separately (Peec does). Otherwise leave it out.
- `citation_sources[].citation_rate`: only if the tool reports it.
- `citation_sources[].classification`: the tool's page type if it has one; otherwise classify from the title and URL (Listicle, Comparison, How-To Guide, Product Page, Homepage, Discussion, Article, Alternative, Profile, Category Page) and note in the Read Me that page types were inferred.
- `sources_to_beat[].metric`: write the metric with its real unit ("14 citations", "cited in 9 responses", "18 retrievals").
- `coverage.raw_queries` and `merged_intents`: fan-out counts if D3 exists; otherwise the number of tracked prompts searched, with a Read Me note.
- `method.datasets`: name the tool and project, e.g. "Profound: category 'Clinic software', prompts tracked 2026-09-01 to 2026-09-30".
