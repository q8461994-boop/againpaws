# -*- coding: utf-8 -*-
"""Again Paws 静态预渲染：渲染线上每个路由，把 DOM 固化进仓库对应 index.html。
head 保留原文件内容（修 canonical 尾斜杠、删 keywords、首页加 hero 预加载）。"""
import json, re, pathlib, sys
from urllib.parse import urljoin

REPO = pathlib.Path(r"C:/Users/16554/WorkBuddy/2026-10-23-10-20-59/againpaws")
BASE = "https://againpaws.vip"

ROUTES = {
    "/": "index.html",
    "/products/": "products/index.html",
    "/pricing/": "pricing/index.html",
    "/customization/": "customization/index.html",
    "/process/": "process/index.html",
    "/about/": "about/index.html",
    "/contact/": "contact/index.html",
    "/guides/": "guides/index.html",
    "/guides/custom-needle-felted-pet-replica-from-photo/": "guides/custom-needle-felted-pet-replica-from-photo/index.html",
    "/guides/needle-felted-pet-cost/": "guides/needle-felted-pet-cost/index.html",
    "/guides/best-photos-for-felted-pet/": "guides/best-photos-for-felted-pet/index.html",
    "/custom-pet-keepsake-from-photo/": "custom-pet-keepsake-from-photo/index.html",
    "/needle-felted-pet-memorial-gift/": "needle-felted-pet-memorial-gift/index.html",
    "/personalized-pet-gift-from-photo/": "personalized-pet-gift-from-photo/index.html",
}

SLASH_URLS = ("products", "pricing", "customization", "process", "about", "contact")

def patch_head(head: str, route: str) -> str:
    # 1) canonical/og:url 统一尾斜杠（根路径除外）
    canon = BASE + ("/" if route == "/" else route)
    head = re.sub(r'<link rel="canonical" href="[^"]*"\s*/?>',
                  f'<link rel="canonical" href="{canon}" />', head, count=1)
    head = head.replace(f'property="og:url" content="https://againpaws.vip/"',
                        f'property="og:url" content="{canon}"') if route == "/" else head
    for s in SLASH_URLS:
        head = head.replace(f'content="https://againpaws.vip/{s}"',
                            f'content="https://againpaws.vip/{s}/"')
        head = head.replace(f'"url": "https://againpaws.vip/{s}"',
                            f'"url": "https://againpaws.vip/{s}/"')
        head = head.replace(f'"url": "https://againpaws.vip/{s}\\n"', f'"url": "https://againpaws.vip/{s}/"')
        # JSON-LD 中不带空格的写法
        head = head.replace(f'"url":"https://againpaws.vip/{s}"',
                            f'"url":"https://againpaws.vip/{s}/"')
    # 2) 删除 meta keywords
    head = re.sub(r'\s*<meta\s+name="keywords"[^>]*>\s*', "\n    ", head)
    # 3) 首页 hero 预加载
    if route == "/" and "hero.webp" in head and "rel=\"preload\"" not in head:
        head = head.replace("</head>",
            '    <link rel="preload" as="image" href="/images/hero.webp" fetchpriority="high" />\n  </head>')
    return head

def main():
    from playwright.sync_api import sync_playwright
    results = []
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        for route, rel in ROUTES.items():
            f = REPO / rel
            original = f.read_text(encoding="utf-8")
            head_m = re.search(r"<head>.*?</head>", original, re.S)
            if not head_m:
                results.append((route, "NO_HEAD")); continue
            url = BASE + route
            page.goto(url, wait_until="networkidle", timeout=60000)
            page.wait_for_timeout(2500)
            dom = page.content()
            body_m = re.search(r"(<body[^>]*>.*</body>)", dom, re.S)
            if not body_m:
                results.append((route, "NO_BODY")); continue
            body = body_m.group(1)
            head = patch_head(head_m.group(0), route)
            out = ("<!doctype html>\n<html lang=\"en\">\n"
                   "<!-- prerendered by Again Paws SEO kit 2026-10-23; JS bundle kept for interactivity -->\n"
                   + head + "\n" + body + "\n</html>\n")
            f.write_text(out, encoding="utf-8")
            results.append((route, f"OK {len(out)}B"))
        browser.close()
    for r in results:
        print(*r)
    bad = [r for r in results if r[1] not in ("OK",) and not r[1].startswith("OK ")]
    sys.exit(1 if bad else 0)

if __name__ == "__main__":
    main()
