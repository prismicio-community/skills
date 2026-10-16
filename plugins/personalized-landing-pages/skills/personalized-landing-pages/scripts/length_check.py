#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mechanical verification for a personalized page.

Usage:
    python3 length_check.py fields.json

Input shape:

{
  "company_name": "Northwind Freight",
  "h1_field": "hero.heading",
  "tolerance": 0.10,
  "ban_dashes": true,
  "banned_words": ["words from the seller's brand voice"],
  "fields": [
    {"name": "hero.heading", "base": "Ship every campaign page without a queue",
     "new": "Northwind Freight lost 6 points of margin"},
    {"name": "testi.quote", "base": "...", "new": "...", "exception": "approved customer quote"}
  ],
  "groups": [
    {"name": "problem.cards", "base_count": 9, "new_count": 9}
  ]
}

Fields marked with "exception" are reported separately and do not fail the run.
"ban_dashes" (default true) flags em and en dashes; set it to false if the
seller's style guide allows them. "banned_words" adds the seller's own list to
the defaults below, which are a floor, not a full list.
Exit code is 0 when everything passes, 1 when anything fails.
"""

import json
import re
import sys

DEFAULT_BANNED = [
    "seamless", "seamlessly", "powerful", "robust", "cutting-edge",
    "cutting edge", "innovative", "game-changing", "game changing",
    "game-changer", "revolutionary", "revolutionize", "best-in-class",
    "world-class", "effortless", "effortlessly", "supercharge", "unlock",
    "leverage", "synergy", "next-level", "unleash",
]


def load(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def check_lengths(fields, tol):
    rows, failures, exceptions = [], [], []
    for f in fields:
        name, base, new = f["name"], f["base"], f["new"]
        lb, ln = len(base), len(new)
        delta = ((ln - lb) / lb * 100) if lb else 0.0
        ok = lb == 0 or (lb * (1 - tol) <= ln <= lb * (1 + tol))
        if f.get("exception"):
            status = "EXCEPTION"
            if not ok:
                exceptions.append((name, delta, f["exception"]))
        elif ok:
            status = "PASS"
        else:
            status = "FAIL"
            failures.append((name, lb, ln, delta))
        rows.append((name, lb, ln, delta, status))
    return rows, failures, exceptions


def check_groups(groups):
    return [g for g in groups
            if g.get("base_count") != g.get("new_count")]


def check_lexicon(fields, banned, ban_dashes=True):
    hits = []
    for f in fields:
        text = f["new"]
        for word in banned:
            if re.search(r"(?<!\w)" + re.escape(word) + r"(?!\w)", text, re.I):
                hits.append((f["name"], word))
        if ban_dashes and ("\u2014" in text or "\u2013" in text):
            hits.append((f["name"], "em/en dash"))
    return hits


def check_h1(fields, h1_field, company, tol):
    if not h1_field or not company:
        return ["H1 check skipped: needs both h1_field and company_name"], []
    match = [f for f in fields if f["name"] == h1_field]
    if not match:
        return ["H1 check failed: field '%s' not found" % h1_field], []
    h1 = match[0]
    problems, warnings = [], []
    count = h1["new"].count(company)
    if count == 0:
        problems.append("company name '%s' missing from H1" % company)
    elif count > 1:
        problems.append("company name appears %d times in H1, expected once" % count)
    cap = int(len(h1["base"]) * (1 + tol))
    if len(h1["new"]) > cap:
        problems.append("H1 is %d chars, cap is %d" % (len(h1["new"]), cap))
    elsewhere = sum(f["new"].count(company) for f in fields if f["name"] != h1_field)
    if elsewhere:
        warnings.append("company name also appears %d time(s) outside the H1, "
                        "check this is intentional" % elsewhere)
    return problems, warnings


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        return 2

    data = load(sys.argv[1])
    fields = data.get("fields", [])
    groups = data.get("groups", [])
    tol = data.get("tolerance", 0.10)
    company = data.get("company_name")
    h1_field = data.get("h1_field")
    banned = DEFAULT_BANNED + data.get("banned_words", [])

    rows, failures, exceptions = check_lengths(fields, tol)
    bad_groups = check_groups(groups)
    lex = check_lexicon(fields, banned, data.get("ban_dashes", True))
    h1_problems, h1_warnings = check_h1(fields, h1_field, company, tol)

    print("%-28s %6s %6s %8s  %s" % ("FIELD", "BASE", "NEW", "DELTA", "STATUS"))
    print("-" * 64)
    for name, lb, ln, delta, status in rows:
        print("%-28s %6d %6d %+7.1f%%  %s" % (name[:28], lb, ln, delta, status))

    print("\nREPEATABLE GROUPS")
    if not groups:
        print("  none declared")
    for g in groups:
        flag = "FAIL" if g in bad_groups else "PASS"
        print("  %-26s base %-3s new %-3s  %s"
              % (g["name"], g.get("base_count"), g.get("new_count"), flag))

    print("\nLEXICAL SCAN")
    if lex:
        for name, word in lex:
            print("  HIT  %-26s %s" % (name[:26], word))
    else:
        print("  clean, no banned words or dashes")

    print("\nH1 CHECK")
    if h1_problems:
        for p in h1_problems:
            print("  " + p)
    else:
        print("  clean")
    for w in h1_warnings:
        print("  WARN " + w)

    if exceptions:
        print("\nAPPROVED EXCEPTIONS, report these rather than fixing them")
        for name, delta, why in exceptions:
            print("  %-26s %+.1f%%  %s" % (name[:26], delta, why))

    total_fail = len(failures) + len(bad_groups) + len(lex) + len(h1_problems)
    print("\n" + "=" * 64)
    if total_fail:
        print("FAILED: %d field(s), %d group(s), %d lexical hit(s), "
              "%d H1 problem(s)" % (len(failures), len(bad_groups),
                                    len(lex), len(h1_problems)))
        print("Fix these in the copy, do not report them as-is.")
        return 1

    print("PASSED: %d fields, %d groups, %d approved exception(s)"
          % (len(fields), len(groups), len(exceptions)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
