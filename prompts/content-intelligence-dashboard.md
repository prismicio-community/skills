Build me an interactive Content Intelligence dashboard for my website, published as a self-contained HTML artifact. It should query my Google Search Console connector live from the page, so that changing any control re-fetches the data. Use the connector's query_performance and compare_performance tools through the page's connector capability. Use the page's ability to ask Claude for the action-plan button. Hand-build the page rather than using a dashboard template, since a template can't call Claude.

BEFORE BUILDING, SET IT UP FOR MY SITE
1. List my Search Console properties. If there's more than one, ask me which to use.
2. Pull the top pages for the last 28 days and look at the URL structure. Then propose three things for me to confirm in one message:
   a. My main site host. Search Console domain properties often include subdomains (help centres, community forums, CDN or image hosts, app subdomains) that aren't marketing content and can fill the row limits.
   b. Paths to always exclude, such as login/app/dashboard pages, careers, legal, and search or filter pages.
   c. Page-type groups based on my real URL patterns (for example Blog, Docs/Help, Product/Features, Landing pages, Other), each defined by a URL regex.
   Also propose my brand terms and common misspellings for the branded-query toggle.
3. Run each query you'll use once yourself to confirm the response shape.

DATA RULES
- Restrict to my main host and remove the excluded paths inside the Search Console request itself (page filter regex), not after the data comes back. Add a toggle to show them.
- Merge "#section" URLs into their parent page: sum clicks and impressions, and use impression-weighted position.
- Page through results 1,000 rows at a time, up to 5,000 per period.
- Treat a page missing from one period as unobserved, not zero, unless the pull didn't hit the row cap.
- Use finalized data, with the end date defaulting to 3 days ago.

CONTROLS (top bar, apply to every tab)
- Date range: last 7 / 28 / 90 days, last 3 / 6 / 12 months, or custom.
- Comparison: previous period (default), same period last year, or custom.
- Page type: All, plus the groups we agreed.
- URL contains / excludes (free text).
- Query contains / excludes (free text), with a toggle to exclude branded queries.
- Country (populated from my data) and device.
- Minimum impressions (default 100), applied in the page without re-fetching.
- Remember each viewer's control settings in their browser.

HEADER
- Total clicks, impressions, average CTR and average position, each with its change vs the comparison period.
- A daily clicks chart, current vs comparison, aligned by day, with a tooltip.
- Counters: pages analysed, pages needing refresh, high-urgency pages, average click change on refresh pages, and estimated clicks per month across the top actions.
- A line stating the exact dates, comparison period and active filters.
- A notes line saying where data is partial: anonymized queries, row caps, and comparison periods older than Search Console's 16-month retention.

TABS
1. Overview: "Top actions" ranked by estimated clicks gained per month, mixing items from every tab. Tag each item Refresh / Striking distance / CTR fix, with a button that opens it in its tab.
2. Pages to refresh: pages losing ground.
   - Signal chips: All / Clicks declining (≥10% drop) / Rank dropping (position worse by ≥1.5) / CTR issues (CTR down ≥1.5 pts, or below 1% at position ≤10) / Lost visibility (impressions down ≥15%).
   - Columns: page, why refresh (signals with values), clicks, click change, position, position change, CTR and its change, impressions and their change, urgency, clicks at stake per month.
   - Urgency is H/M/L, based on signal count and severity, weighted by clicks at stake.
   - Default sort is by urgency, because a site-wide drop can make the impression signal fire on most pages.
3. Striking distance: pages averaging position 8–20, ranked by estimated extra clicks if they reached positions 3–5 (expected CTR ≈ 7.3%).
4. CTR fixes: top-10 pages whose CTR is at least 30% below expected for their position, ranked by lost clicks per month. Expected CTR by position: 1 ≈ 28%, 2 ≈ 15%, 3 ≈ 10%, 4 ≈ 7%, 5 ≈ 5%, 6 ≈ 4%, 7–10 ≈ 2.5%, 11–20 ≈ 1%.

EVERY ROW EXPANDS TO SHOW
- Keyword opportunities: the page's top 20 queries for the active range (position, clicks, impressions, CTR, change vs comparison). Tag each one:
  - Defend & expand: top 3.
  - Quick win: positions 4–10.
  - Title/meta fix: top 10 with CTR well below expected.
  - High potential: positions 11–30.
- The page's current title, meta description and H1.
- A "Generate action plan" button that asks Claude for a plan from that row's live data. The plan covers:
  - why the page needs work
  - priority keywords
  - a rewritten title tag (≤60 characters) and meta description (≤155 characters), with character counts
  - sections to add or restructure
  - schema to add
  - internal links, only to and from my own pages in the data
  - what to measure
  The plan must use only the data provided and never invent statistics, product features or backlink data. Stream it as it's written, with Stop and Copy buttons.

GROUNDING
When building, capture the live title, meta description, H1s and H2s of every page flagged in the default 28-day view. Embed them so the plan generator can use them, and show the capture date on the page.

TABLES
Every table is sortable and searchable, with a CSV export of the current view.

Show errors per section with the specific fix (reconnect the connector, add it, allow access), not one generic message. The page must work at phone width and in light and dark themes.
