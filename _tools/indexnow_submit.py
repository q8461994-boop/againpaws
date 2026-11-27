#!/usr/bin/env python3
"""IndexNow push: submit URLs to Bing/Seznam/Yandex instantly.
Usage: python _tools/indexnow_submit.py url1 url2 ...
       (no args = submit all URLs in sitemap.xml)
"""
import json
import sys
import urllib.request

KEY = "71f11ad7ebbfd609ecdb41d2c35e0e4f"
KEY_LOCATION = f"https://againpaws.vip/{KEY}.txt"
HOST = "againpaws.vip"
ENDPOINT = "https://api.indexnow.org/indexnow"


def urls_from_sitemap(path="sitemap.xml"):
    with open(path, encoding="utf-8") as f:
        return [u.strip() for u in f.read().split("<loc>")[1:]]


def main():
    if len(sys.argv) > 1:
        urls = sys.argv[1:]
    else:
        urls = [s.split("</loc>")[0].strip() for s in urls_from_sitemap()]
    if not urls:
        print("no urls"); sys.exit(1)
    payload = {
        "host": HOST,
        "key": KEY,
        "keyLocation": KEY_LOCATION,
        "urlList": urls,
    }
    req = urllib.request.Request(
        ENDPOINT,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )
    with urllib.request.urlopen(req) as r:
        print("HTTP", r.status, "-", len(urls), "urls submitted")
        # 200/202 = ok, 429 = too many, 403 = key invalid


if __name__ == "__main__":
    main()
