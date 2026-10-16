#!/usr/bin/env python3
"""List a site's published pages from its sitemap, for internal-link candidates.

Usage:
    python sitemap_inventory.py https://example.com
    python sitemap_inventory.py https://example.com/sitemap.xml --match pricing,migration
    python sitemap_inventory.py https://example.com --match "content model" --titles 40

Finds the sitemap (robots.txt Sitemap: lines, then /sitemap.xml, then
/sitemap_index.xml), follows sitemap indexes, and prints every page URL with its
lastmod date. --match keeps URLs whose path contains any of the comma-separated
terms (spaces and hyphens are treated alike). --titles N fetches the first N
matches and adds the page title and robots meta, so noindex pages are caught
before they are proposed.

Used when the site's CMS has no connector. Standard library only. If this
environment cannot reach the site, fetch the sitemap URL with the web fetch tool
instead and apply the same filtering by hand.
"""

import argparse
import gzip
import re
import sys
import urllib.parse
import urllib.request

UA = {"User-Agent": "Mozilla/5.0 (sitemap inventory)"}


def get(url, limit=5_000_000):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=30) as r:
        data = r.read(limit)
    if url.endswith(".gz") or data[:2] == b"\x1f\x8b":
        data = gzip.decompress(data)
    return data.decode("utf-8", "replace")


def find_sitemaps(start):
    if re.search(r"\.xml(\.gz)?$", start):
        return [start]
    root = "{0.scheme}://{0.netloc}".format(urllib.parse.urlparse(start if "://" in start else "https://" + start))
    found = []
    try:
        found = re.findall(r"(?im)^sitemap:\s*(\S+)", get(root + "/robots.txt", 200_000))
    except Exception:
        pass
    return found or [root + "/sitemap.xml", root + "/sitemap_index.xml"]


def crawl(sitemaps, max_maps=200):
    pages, seen, queue = {}, set(), list(sitemaps)
    while queue and len(seen) < max_maps:
        sm = queue.pop(0)
        if sm in seen:
            continue
        seen.add(sm)
        try:
            xml = get(sm)
        except Exception as e:
            print(f"# could not read {sm}: {type(e).__name__}", file=sys.stderr)
            continue
        if "<sitemapindex" in xml:
            queue += re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", xml)
            continue
        for block in re.findall(r"<url>(.*?)</url>", xml, re.S):
            loc = re.search(r"<loc>\s*([^<\s]+)\s*</loc>", block)
            if loc:
                mod = re.search(r"<lastmod>\s*([^<\s]+)", block)
                pages[loc.group(1)] = mod.group(1)[:10] if mod else ""
    return pages


def page_meta(url):
    try:
        body = get(url, 150_000)
    except Exception as e:
        return f"FETCH FAILED ({type(e).__name__})", ""
    t = re.search(r"<title[^>]*>([^<]*)", body, re.I)
    m = re.search(r'<meta[^>]+name=["\']robots["\'][^>]*content=["\']([^"\']+)', body, re.I)
    return (t.group(1).strip()[:90] if t else ""), (m.group(1) if m else "")


def norm(s):
    return re.sub(r"[\s_-]+", " ", s.lower())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("site", help="homepage or sitemap URL")
    ap.add_argument("--match", default="", help="comma-separated path terms to keep")
    ap.add_argument("--titles", type=int, default=0, help="fetch title and robots for the first N")
    args = ap.parse_args()

    pages = crawl(find_sitemaps(args.site))
    if not pages:
        print("No pages found. Check the sitemap URL, or fetch it with the web fetch tool.")
        return 1
    terms = [norm(t) for t in args.match.split(",") if t.strip()]
    rows = sorted(pages.items())
    if terms:
        rows = [(u, d) for u, d in rows if any(t in norm(urllib.parse.urlparse(u).path) for t in terms)]
    print(f"# {len(pages)} pages in sitemap, {len(rows)} listed")
    for i, (u, d) in enumerate(rows):
        line = f"{d or '----------'}  {u}"
        if i < args.titles:
            title, robots = page_meta(u)
            flag = "  NOINDEX" if "noindex" in robots.lower() else ""
            line += f"\n            {title}{flag}"
        print(line)
    return 0


if __name__ == "__main__":
    sys.exit(main())
