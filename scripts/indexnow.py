"""Announce new and changed protologue.com pages to search engines through IndexNow.

IndexNow (https://www.indexnow.org/) is used by Bing, Yandex, Seznam, Naver and others; Bing's
index also feeds several AI assistants' web search. The key is public by design: it is served at
https://protologue.com/<key>.txt so search engines can confirm the site owns it.

Usage:
  python3 scripts/indexnow.py --all                      # every URL in site/sitemap.xml
  python3 scripts/indexnow.py --since old_sitemap.xml    # URLs that are new or have a newer lastmod
  python3 scripts/indexnow.py --all --dry-run            # print, do not submit

Run `python3 build.py` first so site/sitemap.xml exists.
"""
import argparse
import glob
import json
import os
import re
import sys
import urllib.request

HOST = "protologue.com"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENDPOINT = "https://api.indexnow.org/indexnow"
# Pages that change whenever any entry changes, so they go along with any other change.
ALWAYS_WITH_CHANGES = ["/", "/new/", "/terms/", "/llms.txt", "/llms-full.txt", "/feed.xml"]


def key():
    keys = [os.path.basename(p)[:-4] for p in glob.glob(os.path.join(ROOT, "static", "*.txt"))
            if re.fullmatch(r"[0-9a-f]{32}\.txt", os.path.basename(p))]
    if len(keys) != 1:
        sys.exit(f"expected exactly one IndexNow key file static/<32 hex>.txt, found {len(keys)}")
    return keys[0]


def sitemap(path):
    text = open(path, encoding="utf-8").read()
    out = {}
    for block in re.findall(r"<url>(.*?)</url>", text, re.S):
        loc = re.search(r"<loc>(.*?)</loc>", block).group(1)
        m = re.search(r"<lastmod>(.*?)</lastmod>", block)
        out[loc] = m.group(1) if m else ""
    return out


def main():
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--all", action="store_true")
    g.add_argument("--since", metavar="OLD_SITEMAP")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    new = sitemap(os.path.join(ROOT, "site", "sitemap.xml"))
    if a.all:
        urls = list(new)
    else:
        old = sitemap(a.since) if os.path.exists(a.since) else {}
        urls = [u for u, d in new.items() if u not in old or d > old[u]]
        if urls:
            urls += [f"https://{HOST}{p}" for p in ALWAYS_WITH_CHANGES if f"https://{HOST}{p}" not in urls]
    if not urls:
        print("No new or changed pages; nothing to submit.")
        return

    k = key()
    print(f"{len(urls)} URL(s):")
    for u in urls:
        print("  " + u)
    if a.dry_run:
        return
    for i in range(0, len(urls), 10000):
        body = json.dumps({"host": HOST, "key": k, "keyLocation": f"https://{HOST}/{k}.txt",
                           "urlList": urls[i:i + 10000]}).encode()
        req = urllib.request.Request(ENDPOINT, data=body, method="POST",
                                     headers={"Content-Type": "application/json; charset=utf-8"})
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                print(f"IndexNow responded {r.status}")
        except urllib.error.HTTPError as e:
            # 200/202 are success; 403 means the key file is not live yet; 422 means a URL is off-host.
            sys.exit(f"IndexNow responded {e.code}: {e.read().decode(errors='replace')[:300]}")


if __name__ == "__main__":
    main()
