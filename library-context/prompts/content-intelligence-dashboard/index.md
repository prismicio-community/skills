---
title: Content Intelligence Dashboard
summary: One prompt that builds a live Search Console dashboard ranking the pages worth refreshing this week, with a plan for each.
description: A free Claude prompt that builds a live Search Console dashboard of the pages worth refreshing, with an action plan for each page.
categories: [seo]
tags: [search-console, content-refresh, content-decay, striking-distance, ctr, dashboard]
featured: false
draft: false
badge: Dashboard
output: Live dashboard with page plans
platforms: [claude]
requirements:
  - name: Google Search Console connector
    required: true
    details: Add it in Claude under Settings → Connectors and sign in with a Google account that can see your property. Everyone who opens the dashboard needs it too, because data loads with each viewer's own access.
  - name: Artifacts
    required: true
    details: The dashboard is published as an artifact, a private page in your Claude account that you can share from its Share menu. Usually on by default.
  - name: Web access while building
    required: true
    details: Claude reads the title, meta description and headings of the pages it flags, so your pages need to be public.
  - name: Claude usage for plans
    required: false
    details: Each "Generate action plan" click uses the viewer's own Claude usage, after a one-time permission prompt. Without it, the dashboard works but doesn't write plans.
examples:
  - prompt: Make the default date range 90 days and the minimum impressions 50.
    note: Change any default.
  - prompt: Recapture the page content for the pages flagged in the current 28-day view.
    note: Refreshes what the plans are grounded in after you've edited pages or new ones get flagged.
  - prompt: Exclude /careers and /partners from every tab.
    note: Add exclusions you missed during setup.
  - prompt: "Change the expected CTR curve to: position 1 = 32%, 2 = 18%, 3 = 11%."
    note: If you have your own click-through benchmarks, use them.
---

## How it works

Paste one prompt into Claude and get a live dashboard over your Search Console data. It ranks the pages worth working on this week: the ones losing ground, the ones sitting just off page one, and the ones that rank but don't get clicked. Open any row and Claude writes a plan for that page, grounded in its real queries and its current title, meta and headings.

### What you get

One dashboard with a filter bar, a header of totals with a daily clicks chart, and four tabs:

- **Overview:** the top actions from every tab, ranked by estimated extra clicks a month.
- **Pages to refresh:** pages losing clicks, rank, CTR or visibility, with the reasons and an urgency score.
- **Striking distance:** pages at positions 8–20 and the clicks they'd gain at 3–5.
- **CTR fixes:** page-one pages that rank but don't get clicked, usually a title or meta problem.

Every table is sortable, searchable and exportable to CSV. Here is the shape of one row once it's opened, with example data:

| | |
| --- | --- |
| Page | `/blog/best-project-management-tools` |
| Tag | Refresh · Urgency H · 3 signals |
| Why refresh | Clicks −34% · Position worse by 2.8 · Impressions −22% |
| At stake | ≈ 410 clicks a month |
| Top queries | "project management tools for agencies" · position 6.2 · Quick win<br>"best pm software" · position 2.4 · CTR 3% · Title/meta fix |
| Action plan | Why it needs work, priority keywords, a new title tag and meta description with character counts, sections to add, schema, internal links, and what to measure. |

The dashboard reads Search Console and nothing else. It never changes anything in Search Console, your CMS or your site.

## Setup

Add the Google Search Console connector in Claude under **Settings → Connectors**, and sign in with a Google account that can see your property. To check it works, ask Claude to list your Search Console properties.

Make sure artifacts are turned on. They usually are by default.

## Customize

The prompt has no placeholders. Before it builds anything, Claude reads your Search Console data and comes back with one message of proposed settings. You confirm them or correct them.

| Claude proposes | Why it matters |
| --- | --- |
| Which property (required) | Asked only if your Google account can see more than one. |
| Your main host (required) | Domain properties include every subdomain. Forums, help centres and file hosts can take most of the rows Search Console returns and push your real pages out. |
| Paths to exclude (required) | Logged-in app pages, careers and legal pages get impressions but aren't content you'd refresh. Leaving them in clutters every list. |
| Page types (optional) | Built from your own URL patterns, so the page-type filter matches how your site is organised. |
| Brand terms (optional) | Lets you switch off branded searches, which inflate CTR and hide how content performs. |

You don't need to supply competitors, keywords or a page list. Everything else comes from your Search Console data.

To change the dashboard afterwards, ask in the same chat. The examples on this page show a few common changes.

## How to use

1. Copy the prompt and paste it into a new Claude chat.
2. Confirm or correct the settings Claude proposes for your site.
3. Open the dashboard Claude publishes. Allow Search Console access when asked, and Claude access the first time you generate a plan.
4. To share it, use the dashboard's Share menu. Each person sees data through their own Search Console access.

### What the build looks like

1. Claude lists your Search Console properties and pulls a month of page data.
2. **It pauses for you.** It proposes your main host, paths to exclude, page types and brand terms, and waits for your answer.
3. It runs every query once to check the shape of the data, then works out which pages get flagged in the default 28-day view.
4. It reads the live title, meta description and headings of those pages, so the plans start from your real copy.
5. **It publishes the dashboard:** a private page in your Claude account that loads fresh data each time it opens.

## Pitfalls

### What it is not

- **Not keyword research.** Search Console only reports searches your site already appears for. It can't show demand where you don't rank at all. For new topics, use a keyword tool.
- **Not a rank tracker.** Positions are Search Console averages across every search and device, not a daily check of one keyword.
- **Not a traffic or conversion report.** It shows clicks from Google search. Sessions, sign-ups and revenue live in your analytics tool.
- **Not an editor.** It never changes your pages. The action plans are recommendations for you to apply.
- **Not a backlink audit.** Search Console has no backlink data in this connector, and the plans are told not to guess.

### Mistakes to avoid

- **Skipping the host and exclusion step.** On a domain property, forums and file hosts can take almost all of the rows Search Console returns, and your real pages fall off the end of the list without any error. Confirm your main host and exclusions when Claude proposes them.
- **Working through the refresh list top to bottom.** When impressions drop across the whole site, the "lost visibility" signal fires on most pages and the list gets long. Sort by urgency and clicks at stake, and use the signal chips to narrow it.
- **Treating a missing page as zero.** Search Console only returns its top rows, so a page missing from one period may just be below the cut. Read the notes line. It says when the row limit was hit.
- **Comparing a year that Search Console no longer has.** Data older than 16 months is gone, so a long range compared with the same period last year is partly empty. Use previous-period comparisons for ranges longer than four months.
- **Applying a plan without reading it.** Plans are only as good as the data and page content they were given, and page content is captured once at build time. Recapture page content after big edits, and check every suggested title and fact before it goes live.
- **Sharing it with someone who has no access.** The dashboard loads data with each viewer's own Search Console access. Give teammates access to the property and ask them to add the connector before you send the link.
