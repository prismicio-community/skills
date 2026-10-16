#!/usr/bin/env python3
"""Build the GEO Action Plan workbook from a run JSON.

Usage:
    python build_geo_workbook.py run.json output.xlsx
    python build_geo_workbook.py run.json output.xlsx --merge state.json
    python build_geo_workbook.py run.json --validate-only

Tabs produced (fixed order):
    Read Me | Coverage | SERP Pages | SERP Domains | Site Inventory |
    Content Plan | Off-site Targets | Threads | Method

The script fails loudly rather than shipping a broken plan. It validates that:
  * the run searched at least half of its merged intents, and searches_run
    matches the searches recorded
  * every content row's title traces to a phrasing in the evidence
  * every content row names at least one incumbent with a metric
  * every Action is legal
  * every cross-referenced row number resolves
  * priorities and off-site ownership classes are legal values

--merge accumulates across runs:
  * Searches and plan rows are tagged with the prompt IDs that produced them.
    Re-running a prompt already in the state removes that prompt's earlier
    searches and rows before the new run is added, so it never counts twice.
    The previous run stays in the Coverage tab as history.
  * Plan rows dedupe by target phrasing (title_evidence). A repeat phrasing adds
    the new prompt to the existing row instead of creating a duplicate.
  * New rows get the next free numbers, and their refs, the row numbers in their
    guardrail text, and their clusters' plan_row are remapped to match.
  * Clusters carry across runs. A new cluster joins an existing one when it
    names it in "same_as", has the same topic title, or points at a plan row
    that merged into an existing row; its members are added. Otherwise it is
    appended with a fresh ID.

run.json schema
---------------
{
  "project": {"id": "or_...", "name": "My Brand GEO", "site": "https://www.example.com"},
  "scope": {"kind": "prompt|topic|tag|project",
            "label": "What tools can help my company get mentioned...",
            "prompt_ids": ["pr_..."],
            "start_date": "2026-07-25", "end_date": "2026-08-24"},
  "run_date": "2026-08-24",
  "readme": {"summary": "...",
             "assumptions": ["..."],
             "untouched_pages": [{"url": "...", "why": "..."}],
             "cut_list": [{"intent": "fan-out intent or cluster",
                           "why": "why no row, and what would change the answer"}],
             "create_only_mode": false},
  "coverage": {"raw_queries": 68, "merged_intents": 22, "searches_run": 22},
  "clusters": [
      {"id": "C07", "topic": "...", "fit": "High", "action": "Create",
       "existing_url": "", "plan_row": 12, "same_as": "C03 (optional, on merge)",
       "members": [{"url": "...", "title": "...", "layer": "SERP", "metric": "..."}]}
  ],
  "serp_searches": [
      {"query": "best AEO tools (merged: 3 variants)", "weight": 9,
       "results": [{"url": "https://...", "title": "..."}]}
  ],
  "citation_sources": [
      {"url": "https://...", "domain": "techradar.com", "title": "...",
       "classification": "Listicle", "retrievals": 176, "citations": 558,
       "citation_rate": 3.17, "mentioned_brands": ["Brand A", "Brand B"]}
  ],
  "inventory": [
      {"url": "https://www.example.com/blog/x", "title": "...", "indexable": true,
       "matched_intent": "best GEO tools", "action": "Update",
       "notes": "600 words, no AI-search section, last updated 2024"}
  ],
  "content_plan": [
      {"num": 1, "priority": "P0", "action": "Fix", "page_type": "Technical",
       "title": "...", "title_evidence": "...", "title_evidence_source": "cited page title",
       "url": "https://...", "prompts": ["..."],
       "sources_to_beat": [{"url": "...", "metric": "18 retrievals", "layer": "citation"}],
       "why": "...", "brief": "...", "depends_on": "...",
       "guardrail": "Does not cover X - see row 3", "refs": [3]}
  ],
  "offsite_targets": [
      {"page_url": "...", "domain": "...", "ownership": "Independent",
       "evidence": "cited 22x", "ask": "...", "offer": "...", "contact": "...",
       "priority": "P0"}
  ],
  "threads": [
      {"url": "...", "platform": "Reddit", "community": "r/SEO",
       "question": "...", "evidence": "...", "angle": "...", "rules": "..."}
  ],
  "method": {"datasets": ["..."], "extra_notes": ["..."]}
}
"""

import argparse
import json
import re
import sys
from collections import defaultdict
from datetime import date

try:
    from openpyxl import Workbook
    from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
    from openpyxl.utils import get_column_letter
except ImportError:
    sys.exit("openpyxl is required: pip install openpyxl --break-system-packages")


LEGAL_ACTIONS = {"Create", "Update", "Retarget", "Consolidate", "Keep", "Fix"}
LEGAL_PRIORITIES = {"P0", "P1", "P2"}
LEGAL_OWNERSHIP = {
    "Independent",
    "Non-competing vendor",
    "Adjacent vendor",
    "Direct competitor",
    "Review platform",
    "UGC",
    "Verify",
}
LEGAL_TITLE_SOURCES = {
    "cited page title",
    "ranking page title",
    "fan-out query",
    "tracked prompt",
}

HEADER_FILL = PatternFill("solid", fgColor="1F3864")
HEADER_FONT = Font(color="FFFFFF", bold=True, size=11)
TITLE_FONT = Font(bold=True, size=14)
P0_FILL = PatternFill("solid", fgColor="FCE4E4")
P1_FILL = PatternFill("solid", fgColor="FFF4E0")
THIN = Side(style="thin", color="D9D9D9")
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)


# --------------------------------------------------------------------------
# validation
# --------------------------------------------------------------------------

def validate_coverage(run):
    """Check one run's own search coverage. Run this on a single run, before merging."""
    errors = []
    cov = run.get("coverage") or {}
    recorded = len(run.get("serp_searches") or [])
    searches_run = cov.get("searches_run")
    intents = cov.get("merged_intents")
    if searches_run is not None and searches_run != recorded:
        errors.append(
            f"coverage: searches_run is {searches_run} but {recorded} searches are recorded "
            f"in serp_searches; record every search that was run"
        )
    if intents:
        if recorded * 2 < intents:
            errors.append(
                f"coverage: only {recorded} of {intents} merged intents were searched; a run "
                f"must cover at least half. Search the rest, or narrow the scope"
            )
    return errors


def validate(run):
    """Return a list of human-readable errors. Empty list means the run is sound."""
    errors = []

    plan = run.get("content_plan", [])
    numbers = {row.get("num") for row in plan}

    for row in plan:
        n = row.get("num", "?")

        action = row.get("action")
        if action not in LEGAL_ACTIONS:
            errors.append(f"row {n}: action {action!r} is not one of {sorted(LEGAL_ACTIONS)}")

        priority = row.get("priority")
        if priority not in LEGAL_PRIORITIES:
            errors.append(f"row {n}: priority {priority!r} is not P0/P1/P2")

        # The core rule: titles trace to the evidence.
        if not (row.get("title_evidence") or "").strip():
            errors.append(
                f"row {n}: no title_evidence — every title must trace to a phrasing "
                f"present in the data (cited title, ranking title, fan-out query, or prompt)"
            )
        src = (row.get("title_evidence_source") or "").strip().lower()
        if src not in LEGAL_TITLE_SOURCES:
            errors.append(
                f"row {n}: title_evidence_source {row.get('title_evidence_source')!r} "
                f"is not one of {sorted(LEGAL_TITLE_SOURCES)}"
            )

        # Every row must name a real incumbent with a real metric.
        sources = row.get("sources_to_beat") or []
        if not sources and action not in {"Fix", "Keep"}:
            errors.append(
                f"row {n}: no sources_to_beat — every planned page must name at least one "
                f"real incumbent URL with its metric (Fix and Keep rows are exempt)"
            )
        for s in sources:
            if not s.get("url") or not s.get("metric"):
                errors.append(f"row {n}: a source_to_beat is missing its url or metric")
            if s.get("layer") not in {"citation", "SERP", "both"}:
                errors.append(
                    f"row {n}: source {s.get('url')} has layer {s.get('layer')!r}; "
                    f"expected 'citation', 'SERP', or 'both'"
                )

        # Non-Create actions act on an existing page.
        if action in {"Update", "Retarget", "Consolidate", "Keep", "Fix"}:
            if not (row.get("url") or "").strip():
                errors.append(f"row {n}: action {action} requires the existing page URL")

        # Cross-references must resolve.
        for ref in row.get("refs") or []:
            if ref not in numbers:
                errors.append(f"row {n}: guardrail references row {ref}, which does not exist")

    # No two rows may target the same phrasing.
    by_phrase = defaultdict(list)
    for row in plan:
        key = (row.get("title_evidence") or "").strip().lower()
        if key:
            by_phrase[key].append(row.get("num"))
    for phrase, nums in by_phrase.items():
        if len(nums) > 1:
            errors.append(
                f"rows {nums} all target the phrasing {phrase!r} — merge them, or give each "
                f"an explicit scope statement and distinct title_evidence"
            )

    for t in run.get("offsite_targets", []):
        if t.get("ownership") not in LEGAL_OWNERSHIP:
            errors.append(
                f"off-site target {t.get('page_url')}: ownership {t.get('ownership')!r} "
                f"is not one of {sorted(LEGAL_OWNERSHIP)}"
            )
        if t.get("ownership") == "Direct competitor" and t.get("priority") in LEGAL_PRIORITIES:
            errors.append(
                f"off-site target {t.get('page_url')}: competitor-owned pages belong on the "
                f"unlikely list and must not carry a priority"
            )

    return errors


# --------------------------------------------------------------------------
# merge
# --------------------------------------------------------------------------

def norm_url(u):
    return (u or "").strip().rstrip("/").lower()


ROW_REF_RE = re.compile(r"\b(rows?\s+#?|#)(\d+(?:\s*(?:,|and|&)\s*#?\d+)*)", re.IGNORECASE)


def remap_text(text, mapping):
    """Rewrite row numbers in guardrail text ("row 3", "rows 3 and 5", "#3") in one pass."""
    if not text or not mapping:
        return text

    def fix(m):
        nums = re.sub(r"\d+", lambda d: str(mapping.get(int(d.group()), d.group())), m.group(2))
        return m.group(1) + nums

    return ROW_REF_RE.sub(fix, text)


def _ids(item):
    return set(item.get("prompt_ids") or [])


def merge_runs(state, run):
    """Fold a new run into accumulated state. Returns the merged run dict."""
    if not state:
        return run

    merged = json.loads(json.dumps(state))
    run = json.loads(json.dumps(run))
    new_prompts = set(run.get("scope", {}).get("prompt_ids") or [])
    prior_prompts = set(merged.get("scope", {}).get("prompt_ids") or [])

    # Tag anything untagged with the prompts that produced it, so a later re-run
    # of the same prompt can find and replace it.
    for s in merged.get("serp_searches") or []:
        s.setdefault("prompt_ids", sorted(prior_prompts))
    for row in merged.get("content_plan") or []:
        row.setdefault("prompt_ids", sorted(prior_prompts))
    for s in run.get("serp_searches") or []:
        s.setdefault("prompt_ids", sorted(new_prompts))
    for row in run.get("content_plan") or []:
        row.setdefault("prompt_ids", sorted(new_prompts))

    # Coverage history: a repeat prompt replaces its own contribution.
    history = merged.get("coverage_history")
    if history is None:
        # First merge into a single-run state: seed history from that run's own scope,
        # otherwise the original prompt silently disappears from the Coverage tab.
        prior_scope = merged.get("scope", {})
        prior_cov = merged.get("coverage", {})
        history = [
            {
                "prompt_id": pid,
                "label": prior_scope.get("label", ""),
                "run_date": merged.get("run_date", ""),
                "raw_queries": prior_cov.get("raw_queries"),
                "merged_intents": prior_cov.get("merged_intents"),
                "searches_run": prior_cov.get("searches_run"),
            }
            for pid in (prior_scope.get("prompt_ids") or [])
        ]
    history = [h for h in history if h.get("prompt_id") not in new_prompts]
    for pid in new_prompts:
        history.append(
            {
                "prompt_id": pid,
                "label": run.get("scope", {}).get("label", ""),
                "run_date": run.get("run_date") or date.today().isoformat(),
                "raw_queries": run.get("coverage", {}).get("raw_queries"),
                "merged_intents": run.get("coverage", {}).get("merged_intents"),
                "searches_run": run.get("coverage", {}).get("searches_run"),
            }
        )
    merged["coverage_history"] = history

    # SERP searches: drop the repeated prompts' earlier searches, then append.
    kept = []
    for s in merged.get("serp_searches") or []:
        ids = _ids(s)
        if ids and ids <= new_prompts:
            continue
        s["prompt_ids"] = sorted(ids - new_prompts)
        kept.append(s)
    merged["serp_searches"] = kept + (run.get("serp_searches") or [])

    # Plan rows: drop rows that only the repeated prompts produced.
    removed = {}  # old row number -> title_evidence key
    plan = []
    for row in merged.get("content_plan") or []:
        ids = _ids(row)
        if ids and ids <= new_prompts:
            removed[row.get("num")] = (row.get("title_evidence") or "").strip().lower()
            continue
        row["prompt_ids"] = sorted(ids - new_prompts)
        plan.append(row)

    # Clusters pointing at a removed row belong to the repeated run; drop them.
    clusters = [c for c in merged.get("clusters") or [] if c.get("plan_row") not in removed]

    # Add the new run's rows, deduping by phrasing and numbering new rows.
    by_phrase = {(r.get("title_evidence") or "").strip().lower(): r for r in plan}
    used = [r.get("num", 0) for r in plan] + list(removed)
    next_num = max([n for n in used if isinstance(n, int)], default=0) + 1
    num_map = {}  # new run's row number -> merged row number
    reuse = {k: n for n, k in removed.items() if k}
    fresh = []
    for row in run.get("content_plan") or []:
        key = (row.get("title_evidence") or "").strip().lower()
        old = row.get("num")
        if key and key in by_phrase:
            existing = by_phrase[key]
            num_map[old] = existing.get("num")
            for p in row.get("prompts", []):
                if p not in existing.setdefault("prompts", []):
                    existing["prompts"].append(p)
            existing["prompt_ids"] = sorted(_ids(existing) | _ids(row))
            have = {norm_url(x.get("url")) for x in existing.get("sources_to_beat", [])}
            for s in row.get("sources_to_beat", []):
                if norm_url(s.get("url")) not in have:
                    existing.setdefault("sources_to_beat", []).append(s)
        else:
            if key in reuse:
                row["num"] = reuse.pop(key)  # a re-run keeps its row's old number
            else:
                row["num"] = next_num
                next_num += 1
            num_map[old] = row["num"]
            plan.append(row)
            fresh.append(row)
            if key:
                by_phrase[key] = row

    # Remap the new rows' cross-references to the merged numbering. A ref that
    # does not resolve in the new run is kept as an unresolvable marker so that
    # validation fails loudly instead of pointing at the wrong row.
    for row in fresh:
        row["refs"] = [num_map.get(x, f"{x}?") for x in row.get("refs") or []]
        row["guardrail"] = remap_text(row.get("guardrail", ""), num_map)

    # Rows that survived but referred to a removed row: point them at the re-added
    # row with the same phrasing, or drop the ref and say so.
    readded = {(r.get("title_evidence") or "").strip().lower(): r.get("num") for r in fresh}
    removed_map = {old: readded[k] for old, k in removed.items() if k in readded}
    fresh_ids = {id(r) for r in fresh}
    for row in plan:
        if id(row) in fresh_ids:
            continue
        refs = []
        for x in row.get("refs") or []:
            if x in removed:
                if x in removed_map:
                    refs.append(removed_map[x])
                else:
                    row["guardrail"] = (row.get("guardrail", "") + f" (row {x} was removed when its prompt was re-run)").strip()
            else:
                refs.append(x)
        row["refs"] = refs
        row["guardrail"] = remap_text(row.get("guardrail", ""), removed_map)
    plan.sort(key=lambda r: r.get("num") if isinstance(r.get("num"), int) else 0)
    merged["content_plan"] = plan

    # Clusters carry across runs.
    by_id = {c.get("id"): c for c in clusters}
    by_topic = {(c.get("topic") or "").strip().lower(): c for c in clusters}
    by_row = {c.get("plan_row"): c for c in clusters}
    def next_id():
        nums = [int(m.group()) for c in clusters for m in [re.search(r"\d+", str(c.get("id", "")))] if m]
        return f"C{(max(nums, default=0) + 1):02d}"
    for c in run.get("clusters") or []:
        row = num_map.get(c.get("plan_row"), c.get("plan_row"))
        same = str(c.get("same_as") or "").split(" ")[0]
        target = (by_id.get(same) if same else None) \
            or by_topic.get((c.get("topic") or "").strip().lower()) \
            or (by_row.get(row) if row not in [r.get("num") for r in fresh] else None)
        if target:
            have = {norm_url(m.get("url")) for m in target.get("members", [])}
            for m in c.get("members", []):
                if norm_url(m.get("url")) not in have:
                    target.setdefault("members", []).append(m)
        else:
            c = dict(c)
            c.pop("same_as", None)
            c["id"] = next_id()
            c["plan_row"] = row
            clusters.append(c)
            by_id[c["id"]] = c
            by_topic[(c.get("topic") or "").strip().lower()] = c
            by_row[row] = c
    merged["clusters"] = clusters

    # Citation sources dedupe by URL, keeping the higher count.
    def strength(s):
        return ((s.get("retrievals") or 0), (s.get("citations") or 0))
    by_url = {norm_url(s["url"]): s for s in merged.get("citation_sources", [])}
    for s in run.get("citation_sources", []):
        k = norm_url(s["url"])
        if k not in by_url or strength(s) > strength(by_url[k]):
            by_url[k] = s
    merged["citation_sources"] = list(by_url.values())

    # Inventory dedupe by URL.
    inv = {norm_url(i["url"]): i for i in merged.get("inventory", [])}
    for i in run.get("inventory", []):
        inv[norm_url(i["url"])] = i
    merged["inventory"] = list(inv.values())

    # Off-site targets dedupe by page URL.
    off = {norm_url(t["page_url"]): t for t in merged.get("offsite_targets", [])}
    for t in run.get("offsite_targets", []):
        off.setdefault(norm_url(t["page_url"]), t)
    merged["offsite_targets"] = list(off.values())

    thr = {norm_url(t["url"]): t for t in merged.get("threads", [])}
    for t in run.get("threads", []):
        thr.setdefault(norm_url(t["url"]), t)
    merged["threads"] = list(thr.values())

    # Totals across every prompt run so far, for the Method tab.
    def total(k):
        vals = [h.get(k) for h in history if isinstance(h.get(k), int)]
        return sum(vals) if vals else None
    merged["coverage"] = {k: total(k) for k in ("raw_queries", "merged_intents", "searches_run")}

    merged["scope"] = {**run.get("scope", {}),
                       "prompt_ids": sorted({h.get("prompt_id") for h in history if h.get("prompt_id")})}
    merged["project"] = run.get("project") or merged.get("project") or {}
    merged["run_date"] = run.get("run_date") or date.today().isoformat()
    return merged


# --------------------------------------------------------------------------
# aggregation
# --------------------------------------------------------------------------

def aggregate_serp(searches):
    """Roll searches up into ranked pages and domains."""
    pages = {}
    for s in searches:
        weight = s.get("weight", 1) or 1
        seen = set()
        for r in s.get("results", []):
            k = norm_url(r.get("url"))
            if not k or k in seen:
                continue
            seen.add(k)
            p = pages.setdefault(
                k,
                {
                    "url": r.get("url"),
                    "title": r.get("title", ""),
                    "domain": domain_of(r.get("url")),
                    "queries": [],
                    "weight": 0,
                },
            )
            p["queries"].append(s.get("query", ""))
            p["weight"] += weight

    page_rows = sorted(
        pages.values(), key=lambda p: (len(p["queries"]), p["weight"]), reverse=True
    )

    domains = {}
    for p in page_rows:
        d = domains.setdefault(
            p["domain"], {"domain": p["domain"], "queries": set(), "weight": 0, "urls": set()}
        )
        d["queries"].update(p["queries"])
        d["weight"] += p["weight"]
        d["urls"].add(p["url"])
    domain_rows = sorted(
        domains.values(), key=lambda d: (len(d["queries"]), d["weight"]), reverse=True
    )
    return page_rows, domain_rows


def domain_of(url):
    u = (url or "").split("//")[-1]
    return u.split("/")[0].replace("www.", "").lower()


# --------------------------------------------------------------------------
# writing
# --------------------------------------------------------------------------

def style_header(ws, widths):
    for i, w in enumerate(widths, start=1):
        ws.column_dimensions[get_column_letter(i)].width = w
    for cell in ws[1]:
        cell.fill = HEADER_FILL
        cell.font = HEADER_FONT
        cell.alignment = Alignment(vertical="center", wrap_text=True)
    ws.freeze_panes = "A2"
    ws.row_dimensions[1].height = 28


def wrap_body(ws, start=2):
    for row in ws.iter_rows(min_row=start):
        for cell in row:
            cell.alignment = Alignment(vertical="top", wrap_text=True)
            cell.border = BORDER


def sheet_readme(wb, run):
    ws = wb.create_sheet("Read Me")
    scope = run.get("scope", {})
    project = run.get("project") or {}
    rows = [
        ("GEO Action Plan", ""),
        ("Project", project.get("name", "")),
        ("Site", project.get("site", "")),
        ("Scope", f"{scope.get('kind', '')}: {scope.get('label', '')}"),
        ("Date range", f"{scope.get('start_date', '')} to {scope.get('end_date', '')}"),
        ("Run date", run.get("run_date", "")),
        ("", ""),
        ("Summary", run.get("readme", {}).get("summary", "")),
    ]
    for label, value in rows:
        ws.append([label, value])
    ws["A1"].font = TITLE_FONT

    assumptions = run.get("readme", {}).get("assumptions") or []
    if assumptions:
        ws.append(["", ""])
        ws.append(["Assumptions and gaps", ""])
        ws.cell(ws.max_row, 1).font = Font(bold=True)
        for a in assumptions:
            ws.append(["", a])

    untouched = run.get("readme", {}).get("untouched_pages") or []
    if untouched:
        ws.append(["", ""])
        ws.append(["Reviewed, intentionally untouched", ""])
        ws.cell(ws.max_row, 1).font = Font(bold=True)
        for u in untouched:
            ws.append([u.get("url", ""), u.get("why", "")])

    # Intents that are present in the evidence but deliberately got no row. Without
    # this, a defensible cut and an oversight are indistinguishable from outside.
    cut_list = run.get("readme", {}).get("cut_list") or []
    if cut_list:
        ws.append(["", ""])
        ws.append(["Considered and cut", ""])
        ws.cell(ws.max_row, 1).font = Font(bold=True)
        ws.append(["Intent / cluster", "Why no row, and what would change the answer"])
        ws.cell(ws.max_row, 1).font = Font(italic=True)
        ws.cell(ws.max_row, 2).font = Font(italic=True)
        for c in cut_list:
            ws.append([c.get("intent", ""), c.get("why", "")])

    if run.get("readme", {}).get("create_only_mode"):
        ws.append(["", ""])
        ws.append(
            [
                "Create-only mode",
                "No relevant existing pages were found in the inventory; every row is Create or Fix.",
            ]
        )
        ws.cell(ws.max_row, 1).font = Font(bold=True)

    ws.column_dimensions["A"].width = 32
    ws.column_dimensions["B"].width = 110
    for row in ws.iter_rows():
        for cell in row:
            cell.alignment = Alignment(vertical="top", wrap_text=True)


def sheet_coverage(wb, run):
    ws = wb.create_sheet("Coverage")
    ws.append(["Prompt", "Prompt ID", "Run date", "Raw queries", "Merged intents", "Searches run"])
    history = run.get("coverage_history")
    if not history:
        scope = run.get("scope", {})
        cov = run.get("coverage", {})
        for pid in scope.get("prompt_ids") or [scope.get("label", "")]:
            ws.append(
                [
                    scope.get("label", ""),
                    pid,
                    run.get("run_date", ""),
                    cov.get("raw_queries"),
                    cov.get("merged_intents"),
                    cov.get("searches_run"),
                ]
            )
    else:
        for h in history:
            ws.append(
                [
                    h.get("label", ""),
                    h.get("prompt_id", ""),
                    h.get("run_date", ""),
                    h.get("raw_queries"),
                    h.get("merged_intents"),
                    h.get("searches_run"),
                ]
            )
    style_header(ws, [60, 40, 14, 14, 16, 14])
    wrap_body(ws)


def sheet_serp_pages(wb, page_rows):
    ws = wb.create_sheet("SERP Pages")
    ws.append(["# queries", "Weighted score", "Domain", "Title", "URL", "Queries it appeared for"])
    for p in page_rows:
        ws.append(
            [
                len(p["queries"]),
                p["weight"],
                p["domain"],
                p["title"],
                p["url"],
                " | ".join(p["queries"]),
            ]
        )
    style_header(ws, [11, 15, 26, 60, 60, 80])
    wrap_body(ws)


def sheet_serp_domains(wb, domain_rows):
    ws = wb.create_sheet("SERP Domains")
    ws.append(["# queries", "Weighted score", "# unique URLs", "Domain", "Queries"])
    for d in domain_rows:
        ws.append(
            [len(d["queries"]), d["weight"], len(d["urls"]), d["domain"], " | ".join(sorted(d["queries"]))]
        )
    style_header(ws, [11, 15, 14, 30, 90])
    wrap_body(ws)


def sheet_inventory(wb, run):
    ws = wb.create_sheet("Site Inventory")
    ws.append(["URL", "Title", "Indexable", "Matched intent", "Action", "Notes"])
    for i in run.get("inventory", []):
        ws.append(
            [
                i.get("url", ""),
                i.get("title", ""),
                "yes" if i.get("indexable", True) else "NO — fix",
                i.get("matched_intent", ""),
                i.get("action", ""),
                i.get("notes", ""),
            ]
        )
    style_header(ws, [58, 46, 12, 34, 14, 60])
    wrap_body(ws)
    for row in ws.iter_rows(min_row=2, min_col=3, max_col=3):
        for cell in row:
            if isinstance(cell.value, str) and cell.value.startswith("NO"):
                cell.fill = P0_FILL
                cell.font = Font(bold=True, color="9C0006")


def sheet_content_plan(wb, run):
    ws = wb.create_sheet("Content Plan")
    ws.append(
        [
            "#",
            "Priority",
            "Action",
            "Page type",
            "Working title",
            "Title evidence (phrasing found in data)",
            "Evidence source",
            "URL (existing, or suggested)",
            "Prompts this targets",
            "Sources to beat",
            "Why this page",
            "Brief",
            "Depends on",
            "Cannibalization guardrail",
        ]
    )
    for r in sorted(run.get("content_plan", []), key=lambda x: x.get("num", 0)):
        sources = "\n".join(
            f"{s.get('url')} — {s.get('metric')} ({s.get('layer')} layer)"
            for s in r.get("sources_to_beat", [])
        )
        ws.append(
            [
                r.get("num"),
                r.get("priority"),
                r.get("action"),
                r.get("page_type", ""),
                r.get("title", ""),
                r.get("title_evidence", ""),
                r.get("title_evidence_source", ""),
                r.get("url", ""),
                "\n".join(r.get("prompts", [])),
                sources,
                r.get("why", ""),
                r.get("brief", ""),
                r.get("depends_on", ""),
                r.get("guardrail", ""),
            ]
        )
    style_header(ws, [5, 9, 12, 14, 42, 42, 18, 44, 44, 56, 50, 78, 40, 44])
    wrap_body(ws)
    for row in ws.iter_rows(min_row=2):
        pri = row[1].value
        if pri == "P0":
            for cell in row:
                cell.fill = P0_FILL
        elif pri == "P1":
            for cell in row:
                cell.fill = P1_FILL


def sheet_offsite(wb, run):
    ws = wb.create_sheet("Off-site Targets")
    ws.append(
        [
            "Priority",
            "Page",
            "Domain",
            "Ownership class",
            "Evidence",
            "The ask",
            "The offer",
            "Contact route",
        ]
    )
    pitchable = [t for t in run.get("offsite_targets", []) if t.get("ownership") != "Direct competitor"]
    unlikely = [t for t in run.get("offsite_targets", []) if t.get("ownership") == "Direct competitor"]
    order = {"P0": 0, "P1": 1, "P2": 2}
    for t in sorted(pitchable, key=lambda x: order.get(x.get("priority"), 9)):
        ws.append(
            [
                t.get("priority", ""),
                t.get("page_url", ""),
                t.get("domain", ""),
                t.get("ownership", ""),
                t.get("evidence", ""),
                t.get("ask", ""),
                t.get("offer", ""),
                t.get("contact", ""),
            ]
        )
    if unlikely:
        ws.append([])
        ws.append(["UNLIKELY — competitor-owned, do not pitch", "", "", "", "", "", "", ""])
        ws.cell(ws.max_row, 1).font = Font(bold=True, color="9C0006")
        for t in unlikely:
            ws.append(
                [
                    "",
                    t.get("page_url", ""),
                    t.get("domain", ""),
                    t.get("ownership", ""),
                    t.get("evidence", ""),
                    t.get("ask", ""),
                    "",
                    "",
                ]
            )
    style_header(ws, [9, 58, 26, 22, 34, 52, 52, 34])
    wrap_body(ws)


def sheet_threads(wb, run):
    ws = wb.create_sheet("Threads")
    ws.append(["URL", "Platform", "Community", "Question asked", "Evidence", "Comment angle", "Community rules"])
    for t in run.get("threads", []):
        ws.append(
            [
                t.get("url", ""),
                t.get("platform", ""),
                t.get("community", ""),
                t.get("question", ""),
                t.get("evidence", ""),
                t.get("angle", ""),
                t.get("rules", ""),
            ]
        )
    style_header(ws, [58, 14, 22, 50, 26, 72, 36])
    wrap_body(ws)


def sheet_method(wb, run, page_rows, domain_rows):
    ws = wb.create_sheet("Method")
    cov = run.get("coverage", {})
    lines = [
        ("How this plan was built", ""),
        ("", ""),
        ("Evidence layers", "Citation layer from the AI visibility tool named under Datasets (cited URLs "
                            "with the citation metrics that tool reports). SERP layer from live searches run "
                            "against the fan-out queries the engines issued for the prompts in scope, or "
                            "against the tracked prompts where the tool provides no fan-out queries."),
        ("Site inventory", "Sitemap as the complete URL list; candidate pages read through the "
                           "CMS connector or fetched live; robots meta and robots.txt checked on the live site."),
        ("Fan-out coverage", f"{cov.get('raw_queries', '?')} raw fan-out queries merged to "
                             f"{cov.get('merged_intents', '?')} distinct intents; "
                             f"{cov.get('searches_run', '?')} searches run."),
        ("Unique pages found", str(len(page_rows))),
        ("Unique domains found", str(len(domain_rows))),
        ("", ""),
        ("Title rule", "Every working title is derived from a phrasing that appears in the evidence "
                       "(a cited page title, a ranking page title, a fan-out query, or a tracked "
                       "prompt). The phrasing and its source are recorded per row."),
        ("Angle rule", "Differentiators were checked against incumbent page content actually read, "
                       "not assumed. Where an angle depends on a brand asset that does not yet exist, "
                       "the row says so."),
        ("No invented data", "Every URL, title, metric and quoted page detail comes from the AI "
                             "visibility tool, a search run for this report, or a page fetched for it. Briefs "
                             "request numbers from the brand; they never supply them."),
        ("", ""),
        ("Search depth caveat", "The search tool returns roughly the top 10 results per query, not "
                                "positions 11-50. The report's depth comes from breadth across many "
                                "queries rather than depth within one."),
        ("Search engine caveat", "The search tool is a search engine but not literally Google; result "
                                 "ordering is approximate."),
    ]
    for label, value in lines:
        ws.append([label, value])
    ws["A1"].font = TITLE_FONT

    for d in run.get("method", {}).get("datasets", []):
        ws.append(["Dataset", d])
    for n in run.get("method", {}).get("extra_notes", []):
        ws.append(["Note", n])

    ws.column_dimensions["A"].width = 26
    ws.column_dimensions["B"].width = 110
    for row in ws.iter_rows():
        for cell in row:
            cell.alignment = Alignment(vertical="top", wrap_text=True)


def build(run, out_path):
    page_rows, domain_rows = aggregate_serp(run.get("serp_searches", []))
    wb = Workbook()
    wb.remove(wb.active)
    sheet_readme(wb, run)
    sheet_coverage(wb, run)
    sheet_serp_pages(wb, page_rows)
    sheet_serp_domains(wb, domain_rows)
    sheet_inventory(wb, run)
    sheet_content_plan(wb, run)
    sheet_offsite(wb, run)
    sheet_threads(wb, run)
    sheet_method(wb, run, page_rows, domain_rows)
    wb.save(out_path)
    return page_rows, domain_rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("run_json")
    ap.add_argument("output", nargs="?")
    ap.add_argument("--merge", help="existing state JSON to accumulate into")
    ap.add_argument("--validate-only", action="store_true")
    ap.add_argument("--state-out", help="where to write the merged state JSON (default: alongside output)")
    args = ap.parse_args()

    with open(args.run_json) as f:
        run = json.load(f)

    errors = validate_coverage(run)

    if args.merge:
        with open(args.merge) as f:
            state = json.load(f)
        run = merge_runs(state, run)

    errors += validate(run)
    if errors:
        print("VALIDATION FAILED — the plan was not written:\n", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        sys.exit(1)

    if args.validate_only:
        print(f"Validation passed: {len(run.get('content_plan', []))} plan rows, all references resolve.")
        return

    if not args.output:
        sys.exit("An output path is required unless --validate-only is set.")

    page_rows, domain_rows = build(run, args.output)

    state_out = args.state_out or (args.output.rsplit(".", 1)[0] + "_state.json")
    with open(state_out, "w") as f:
        json.dump(run, f, indent=2)

    plan = run.get("content_plan", [])
    p0 = sum(1 for r in plan if r.get("priority") == "P0")
    print(f"Wrote {args.output}")
    print(f"  {len(plan)} plan rows ({p0} P0) | {len(page_rows)} SERP pages | "
          f"{len(domain_rows)} domains | {len(run.get('offsite_targets', []))} off-site targets")
    print(f"  State for future runs: {state_out}")


if __name__ == "__main__":
    main()
