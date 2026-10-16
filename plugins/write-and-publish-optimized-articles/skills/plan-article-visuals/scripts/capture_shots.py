#!/usr/bin/env python3
"""Capture the public-page screenshots in a shot list.

Setup, once:
    pip install playwright
    python -m playwright install chromium

Usage:
    python capture_shots.py shots.json --out ./images
    python capture_shots.py shots.json --out ./images --only 3,5

Shot list is a JSON array. Only `id`, `name` and `url` are required:

[
  {
    "id": 3,
    "name": "seomatic-pricing",
    "url": "https://seomatic.ai/pricing",
    "wait_for": "text=Launch",        optional CSS or text selector
    "clip_to": ".pricing-table",      optional: crop to this element
    "hide": [".cookie-banner", "#intercom"],   optional: remove before shooting
    "click": ["text=Decline All"],    optional: dismiss consent properly first
    "full_page": false,
    "wait_until": "domcontentloaded",   optional: for sites that never idle
    "supports": "the claim that SEOmatic starts at $149"
  }
]

Writes a PNG per shot plus `manifest.json` recording the capture date, final
URL and viewport, which is what makes a screenshot auditable six months later.

Only works on pages reachable without a login. Anything behind authentication
should be captured in a real browser session instead: see the skill's notes on
Claude for Chrome.
"""

import argparse
import json
import sys
from datetime import date, datetime, timezone
from pathlib import Path

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("Playwright is not installed. Run:\n"
          "  pip install playwright\n"
          "  python -m playwright install chromium", file=sys.stderr)
    sys.exit(1)

# Cookie banners and chat widgets ruin more screenshots than anything else.
COMMON_JUNK = [
    "#onetrust-consent-sdk", "#onetrust-banner-sdk", ".ot-sdk-container",
    "#cookie-banner", ".cookie-banner", ".cookie-consent", "#cookiescript_injected",
    "#hubspot-messages-iframe-container", ".intercom-lightweight-app",
    "#intercom-container", ".drift-frame-controller", "#drift-frame-controller",
    "[id*='cookie'][class*='banner']", ".cky-consent-container",
    "#usercentrics-root", "#usercentrics-cmp-ui", "[id^='usercentrics']",
    "#uc-center-container", ".uc-overlay", "#CybotCookiebotDialog",
    "#truste-consent-track", ".qc-cmp2-container", "#didomi-popup",
]

HIDE_JS = """(sels) => {
  for (const s of sels) {
    document.querySelectorAll(s).forEach(el => el.style.setProperty('display','none','important'));
  }
}"""


def capture(page, shot, out_dir, viewport):
    url = shot["url"]
    # Some sites poll continuously and never reach networkidle. Fall back to
    # domcontentloaded plus a settle delay rather than failing the shot.
    try:
        page.goto(url, wait_until=shot.get("wait_until", "networkidle"), timeout=45000)
    except Exception:
        print("    note: networkidle not reached, falling back to domcontentloaded")
        page.goto(url, wait_until="domcontentloaded", timeout=45000)
        page.wait_for_timeout(3500)

    if shot.get("wait_for"):
        try:
            page.wait_for_selector(shot["wait_for"], timeout=15000)
        except Exception:
            print(f"    note: wait_for {shot['wait_for']!r} never appeared")

    # Clicking a real consent choice is better than hiding the modal, because
    # hiding it can leave the page scroll-locked behind an invisible overlay.
    for sel in shot.get("click", []):
        try:
            page.click(sel, timeout=6000)
            page.wait_for_timeout(500)
        except Exception:
            print(f"    note: click target {sel!r} not found")

    page.evaluate(HIDE_JS, COMMON_JUNK + shot.get("hide", []))
    page.evaluate("() => { document.documentElement.style.overflow = 'auto';"
                  " document.body.style.overflow = 'auto'; }")
    # Anchors and lazy loading can leave the page scrolled mid-document, which
    # produces a valid screenshot of the wrong section.
    page.evaluate("() => window.scrollTo(0, 0)")
    page.wait_for_timeout(600)          # let layout settle after hiding

    path = out_dir / f"{shot['id']:02d}-{shot['name']}.png"
    target, clipped = page, False
    if shot.get("clip_to"):
        el = page.query_selector(shot["clip_to"])
        if el:
            target, clipped = el, True
        else:
            print(f"    note: clip_to {shot['clip_to']!r} not found, full viewport used")

    target.screenshot(path=str(path), **({} if clipped
                                         else {"full_page": shot.get("full_page", False)}))
    return {
        "id": shot["id"],
        "name": shot["name"],
        "file": path.name,
        "requested_url": url,
        "final_url": page.url,
        "title": page.title(),
        "viewport": f"{viewport[0]}x{viewport[1]}",
        "clipped_to": shot.get("clip_to"),
        "supports": shot.get("supports", ""),
        "captured": date.today().isoformat(),
        "captured_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("shots")
    ap.add_argument("--out", default="./images")
    ap.add_argument("--width", type=int, default=1440)
    ap.add_argument("--height", type=int, default=900)
    ap.add_argument("--scale", type=int, default=2, help="2 for retina-quality")
    ap.add_argument("--only", help="comma-separated shot ids")
    ap.add_argument("--dark", action="store_true")
    ap.add_argument("--insecure", action="store_true",
                    help="skip TLS verification. Only for sandboxes behind a "
                         "TLS-intercepting proxy, where Chromium does not trust "
                         "the proxy CA. Never use against untrusted networks.")
    args = ap.parse_args()

    shots = json.load(open(args.shots, encoding="utf-8"))
    if args.only:
        keep = {int(x) for x in args.only.split(",")}
        shots = [s for s in shots if s["id"] in keep]

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    viewport = (args.width, args.height)

    manifest, failures = [], []
    with sync_playwright() as p:
        browser = p.chromium.launch()
        ctx = browser.new_context(
            viewport={"width": args.width, "height": args.height},
            device_scale_factor=args.scale,
            color_scheme="dark" if args.dark else "light",
            ignore_https_errors=args.insecure,
            user_agent=("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                        "AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Chrome/124.0 Safari/537.36"),
        )
        page = ctx.new_page()
        for shot in shots:
            print(f"[{shot['id']:02d}] {shot['name']}: {shot['url']}")
            try:
                manifest.append(capture(page, shot, out_dir, viewport))
                print(f"    saved {manifest[-1]['file']}")
            except Exception as e:
                print(f"    FAILED: {type(e).__name__}: {e}")
                failures.append({"id": shot["id"], "name": shot["name"],
                                 "error": f"{type(e).__name__}: {e}"})
        browser.close()

    (out_dir / "manifest.json").write_text(
        json.dumps({"captured": date.today().isoformat(),
                    "viewport": f"{args.width}x{args.height}@{args.scale}x",
                    "shots": manifest, "failures": failures}, indent=2))

    print(f"\n{len(manifest)} captured, {len(failures)} failed. "
          f"Manifest: {out_dir / 'manifest.json'}")
    print("Copy the capture dates into the article appendix.")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
