#!/usr/bin/env python3
"""Inject GA4 gtag snippet into every index.html (idempotent)."""
import pathlib, re

GA_ID = "G-KKE2MPQSCL"
SNIPPET = (
    "<!-- Google tag (gtag.js) -->\n"
    f'<script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>\n'
    "<script>\n"
    "  window.dataLayer = window.dataLayer || [];\n"
    "  function gtag(){dataLayer.push(arguments);}\n"
    f"  gtag('js', new Date());\n"
    f"  gtag('config', '{GA_ID}');\n"
    "</script>\n"
)

root = pathlib.Path(__file__).resolve().parent.parent
files = sorted(root.glob("**/index.html"))
injected = skipped = 0
for f in files:
    if "_tools" in str(f):
        continue
    t = f.read_text(encoding="utf-8")
    if GA_ID in t:
        skipped += 1
        continue
    if "</head>" not in t:
        print("NO </head>:", f)
        continue
    t = t.replace("</head>", SNIPPET + "</head>", 1)
    f.write_text(t, encoding="utf-8")
    injected += 1
print(f"injected: {injected}, already had: {skipped}, total: {injected + skipped}")
