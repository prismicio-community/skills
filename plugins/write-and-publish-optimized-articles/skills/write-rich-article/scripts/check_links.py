#!/usr/bin/env python3
"""Verify every link in a markdown article: status, redirects, anchor quality, counts.

Usage:
    python check_links.py article.md --internal-domain example.com
    python check_links.py article.md --internal-domain example.com --json

Reports per link: HTTP status, final URL after redirects, internal/external
classification, anchor warnings. Also checks the counts required by the
playbook (4 to 8 internal, 2 to 4 external) and flags duplicate destinations.

Exits 1 if any link is broken or any count is out of range.
Standard library only.
"""

import argparse
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")

WEAK_ANCHORS = {"click here", "read more", "here", "this", "this article",
                "learn more", "more", "link", "this page", "check it out",
                "this post", "see here", "find out more"}

STOPWORDS = {"the", "a", "an", "and", "or", "of", "to", "in", "for", "on",
             "with", "how", "what", "why", "is", "are", "your", "our", "it",
             "guide", "docs", "doc", "blog", "page", "www", "com", "io"}

INTERNAL_MIN, INTERNAL_MAX = 4, 8
EXTERNAL_MIN, EXTERNAL_MAX = 2, 4


class RecordingRedirectHandler(urllib.request.HTTPRedirectHandler):
    def __init__(self):
        self.chain = []

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        self.chain.append((code, newurl))
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def extract_links(path):
    """Return list of dicts for inline markdown links outside code fences."""
    links = []
    in_fence = False
    with open(path, encoding="utf-8") as fh:
        for no, raw in enumerate(fh.read().splitlines(), start=1):
            s = raw.strip()
            if s.startswith("```") or s.startswith("~~~"):
                in_fence = not in_fence
                continue
            if in_fence:
                continue
            for m in re.finditer(r"(!?)\[([^\]]*)\]\(\s*<?([^)\s>]+)>?[^)]*\)", raw):
                if m.group(1) == "!":
                    continue  # image
                links.append({"line": no, "anchor": m.group(2).strip(), "url": m.group(3).strip()})
    return links


def classify(url, internal_domain):
    if url.startswith("#"):
        return "anchor"
    if url.startswith(("mailto:", "tel:")):
        return "other"
    parsed = urllib.parse.urlparse(url)
    if not parsed.netloc:
        return "internal"
    host = parsed.netloc.lower().split(":")[0]
    if internal_domain and (host == internal_domain or host.endswith("." + internal_domain)):
        return "internal"
    return "external"


def fetch(url, timeout=20):
    """Return (status, final_url, redirect_chain, note)."""
    if not url.startswith("http"):
        return (None, url, [], "relative URL, not checked over the network")

    for method in ("HEAD", "GET"):
        handler = RecordingRedirectHandler()
        opener = urllib.request.build_opener(handler)
        req = urllib.request.Request(url, method=method,
                                     headers={"User-Agent": UA,
                                              "Accept": "text/html,application/xhtml+xml,*/*"})
        try:
            with opener.open(req, timeout=timeout) as resp:
                return (resp.status, resp.geturl(), handler.chain, "")
        except urllib.error.HTTPError as e:
            if method == "HEAD" and e.code in (403, 405, 501, 400):
                continue
            return (e.code, url, handler.chain, e.reason or "")
        except urllib.error.URLError as e:
            if method == "HEAD":
                continue
            return (None, url, handler.chain, f"network error: {e.reason}")
        except Exception as e:  # timeouts, malformed URLs, TLS problems
            if method == "HEAD":
                continue
            return (None, url, handler.chain, f"{type(e).__name__}: {e}")
    return (None, url, [], "unreachable")


def normalize(url):
    """Drop default ports and trailing slashes so equivalent URLs compare equal."""
    try:
        p = urllib.parse.urlparse(url)
    except ValueError:
        return url
    host = p.netloc
    if p.scheme == "https" and host.endswith(":443"):
        host = host[:-4]
    if p.scheme == "http" and host.endswith(":80"):
        host = host[:-3]
    return urllib.parse.urlunparse((p.scheme, host, p.path.rstrip("/") or "/",
                                    p.params, p.query, ""))


def tokens(text):
    return {t for t in re.split(r"[^a-z0-9]+", text.lower()) if t and t not in STOPWORDS and len(t) > 2}


def anchor_warnings(link, status_url):
    warns = []
    anchor = link["anchor"]
    low = anchor.strip().lower()
    if not anchor:
        warns.append("empty anchor text")
        return warns
    if low in WEAK_ANCHORS:
        warns.append(f"weak anchor text: '{anchor}'")
    if re.match(r"^https?://", low):
        warns.append("naked URL used as anchor text")
    words = len(anchor.split())
    if words > 8:
        warns.append(f"anchor is {words} words, hard to scan")
    dest = urllib.parse.urlparse(status_url or link["url"])
    dest_tokens = tokens(dest.path + " " + dest.netloc)
    if dest_tokens and not (tokens(anchor) & dest_tokens):
        warns.append("anchor text shares no meaningful word with the destination URL, "
                     "check that it describes where it goes")
    return warns


def main():
    ap = argparse.ArgumentParser(description="Check links in a markdown article.")
    ap.add_argument("path")
    ap.add_argument("--internal-domain", default="", help="e.g. example.com")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--skip-network", action="store_true", help="anchor checks only")
    args = ap.parse_args()

    links = extract_links(args.path)
    if not links:
        print("No links found.")
        return 1

    for l in links:
        l["kind"] = classify(l["url"], args.internal_domain.lower().strip())

    checkable = [l for l in links if l["kind"] in ("internal", "external")]

    if args.skip_network:
        for l in links:
            l.update(status=None, final_url=l["url"], chain=[], note="skipped")
    else:
        with ThreadPoolExecutor(max_workers=args.workers) as pool:
            results = list(pool.map(lambda l: fetch(l["url"]), links))
        for l, (status, final, chain, note) in zip(links, results):
            l.update(status=status, final_url=normalize(final), chain=chain, note=note)

    problems = []
    for l in links:
        l["warnings"] = anchor_warnings(l, l.get("final_url"))
        if l["kind"] == "anchor":
            continue
        if l["status"] is None and not args.skip_network and l["url"].startswith("http"):
            problems.append((l, f"could not be reached ({l['note']})"))
        elif l["status"] and l["status"] >= 400:
            problems.append((l, f"HTTP {l['status']}"))
        elif l["chain"] and normalize(l["url"]) != l["final_url"]:
            problems.append((l, f"redirects to {l['final_url']}, update the link"))

    seen = {}
    dupes = []
    for l in checkable:
        key = normalize(l["final_url"] or l["url"])
        if key in seen:
            dupes.append((l, seen[key]))
        else:
            seen[key] = l["line"]

    n_int = sum(1 for l in links if l["kind"] == "internal")
    n_ext = sum(1 for l in links if l["kind"] == "external")
    count_issues = []
    if not INTERNAL_MIN <= n_int <= INTERNAL_MAX:
        count_issues.append(f"internal links: {n_int} (required {INTERNAL_MIN} to {INTERNAL_MAX})")
    if not EXTERNAL_MIN <= n_ext <= EXTERNAL_MAX:
        count_issues.append(f"external links: {n_ext} (required {EXTERNAL_MIN} to {EXTERNAL_MAX})")

    if args.json:
        print(json.dumps({"links": links, "problems": [p[1] for p in problems],
                          "duplicates": [d[0]["url"] for d in dupes],
                          "counts": {"internal": n_int, "external": n_ext},
                          "count_issues": count_issues}, indent=2, default=str))
        return 1 if (problems or count_issues) else 0

    print(f"Article: {args.path}")
    print(f"Links found: {len(links)}  (internal {n_int}, external {n_ext})\n")

    for l in links:
        status = l["status"] if l["status"] is not None else "ERR"
        flag = "ok "
        if l["kind"] == "anchor":
            flag, status = "   ", "frag"
        elif l["status"] is None or (l["status"] and l["status"] >= 400):
            flag = "FAIL"
        elif l["chain"]:
            flag = "REDIR"
        print(f"{flag:5} {str(status):5} [{l['kind']:8}] L{l['line']}: {l['anchor']!r} -> {l['url']}")
        if l["chain"]:
            print(f"      final: {l['final_url']}")
        if l["note"] and l["note"] != "skipped":
            print(f"      note: {l['note']}")
        for w in l["warnings"]:
            print(f"      warn: {w}")

    print()
    if problems:
        print(f"--- BROKEN OR REDIRECTING ({len(problems)}) ---")
        for l, why in problems:
            print(f"L{l['line']}: {l['url']} -> {why}")
        print()
    if dupes:
        print("--- DUPLICATE DESTINATIONS ---")
        for l, first in dupes:
            print(f"L{l['line']}: {l['url']} already linked at L{first}")
        print()
    if count_issues:
        print("--- COUNT ISSUES ---")
        for c in count_issues:
            print(c)
        print()

    if not problems and not count_issues:
        print("All links resolve and counts are within range.")

    return 1 if (problems or count_issues) else 0


if __name__ == "__main__":
    sys.exit(main())
