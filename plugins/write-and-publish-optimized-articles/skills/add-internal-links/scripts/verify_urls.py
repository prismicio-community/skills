#!/usr/bin/env python3
"""Verify candidate links before they enter a draft.

Usage:
    python verify_urls.py urls.txt            # one URL per line
    echo "https://example.com" | python verify_urls.py -

Checks, per URL:
  - final HTTP status after redirects (must be 200)
  - the final URL, so redirects are caught and the canonical target used
  - the robots meta tag, so noindex pages are never linked as architecture
  - the page title, so the anchor can be checked against what the page says

Exit code 1 if any URL fails. Standard library only.
"""

import re
import sys
import urllib.request


def check(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (link check)"})
    try:
        with urllib.request.urlopen(req, timeout=25) as r:
            body = r.read(120000).decode("utf-8", "replace")
            status, final = r.status, r.url
    except Exception as e:
        return {"url": url, "ok": False, "status": f"{type(e).__name__}", "final": "",
                "robots": "", "title": ""}
    m = re.search(r'<meta[^>]+name=["\']robots["\'][^>]*content=["\']([^"\']+)', body, re.I)
    robots = m.group(1) if m else ""
    t = re.search(r"<title[^>]*>([^<]*)", body, re.I)
    title = (t.group(1).strip() if t else "")[:80]
    return {"url": url, "ok": status == 200, "status": status, "final": final,
            "robots": robots, "title": title}


def main():
    src = sys.stdin if sys.argv[1:] == ["-"] else open(sys.argv[1])
    urls = [l.strip() for l in src if l.strip() and not l.startswith("#")]
    bad = 0
    for u in urls:
        r = check(u)
        flag = "ok " if r["ok"] else "FAIL"
        noidx = "  NOINDEX" if "noindex" in r["robots"].lower() else ""
        redir = f"  -> {r['final']}" if r["final"] and r["final"].rstrip("/") != u.rstrip("/") else ""
        print(f"{flag} {r['status']:>4}  {u}{redir}{noidx}")
        if r["title"]:
            print(f"          {r['title']}")
        if not r["ok"] or noidx:
            bad += 1
    print(f"\n{len(urls)} checked, {bad} problem(s).")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
