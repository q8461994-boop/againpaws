# -*- coding: utf-8 -*-
"""新增 3 篇长尾关键词指南页（复用信任页模板）+ 更新 sitemap/llms.txt/导览页内链 + 落地页 LCP 预加载。幂等。"""
import json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import make_static_pages as m

REPO = m.REPO
BASE = "https://againpaws.vip"

# ---------------- 1. 三篇指南 ----------------
PAGES = [
{
 "route": "/guides/pet-memorial-gift-ideas/",
 "title": "10 Pet Memorial Gift Ideas for Someone Who Lost a Dog or Cat | Again Paws",
 "desc": "Thoughtful pet memorial gift ideas, from handmade keepsakes to living tributes — what to give when someone loses a dog or cat, and what each option costs.",
 "ld_types": ["Article", "BreadcrumbList"],
 "body": """
<h1>10 Pet Memorial Gift Ideas</h1>
<p class="updated">By the Again Paws studio · October 2026</p>
<p>When someone loses a dog or a cat, ordinary sympathy gifts don't quite fit. The best pet memorial gifts do one thing: they turn a memory you can't hold into something you can. Here are ten ideas, from handmade keepsakes to living tributes, with honest notes on cost and timing.</p>

<h2>1. A custom needle-felted portrait from a photo</h2>
<p>A small wool sculpture of the actual pet — same markings, same tilted ear — is the closest thing to holding them again. Made from photos, it works even when the only pictures are old phone snapshots. <a href="/needle-felted-pet-memorial-gift/">See how our memorial keepsakes are made</a>; prices start at $87 for a mini portrait.</p>
<h2>2. A framed photo with a custom engraved mat</h2>
<p>Simple and fast (days, not weeks). Print the best photo, add a mat engraved with the pet's name and dates. Cost: $30–60 at any print shop.</p>
<h2>3. A paw-print cast or ink print kit</h2>
<p>Ink kits ($15–25) work if the pet has passed but prints were taken; clay castings need to be made while the pet is still alive or from an existing print. If no print exists, a felted portrait from photos is the alternative.</p>
<h2>4. A memorial stone or garden marker</h2>
<p>Engraved stone for a garden or burial spot. $40–100, weatherproof, zero upkeep.</p>
<h2>5. A living tribute plant or tree</h2>
<p>A hardy indoor plant or a tree planted in the pet's name. Growth becomes an ongoing, quiet memorial. $25–150.</p>
<h2>6. A donation in the pet's name</h2>
<p>To a rescue or the vet school that treated them. Costs whatever you choose, and for many grieving owners it is the most meaningful gesture of all.</p>
<h2>7. Custom jewelry with fur or ashes</h2>
<p>Glass pendants or resin rings containing a lock of fur. $60–200. Beautiful, but order early — most makers need 4–8 weeks.</p>
<h2>8. A portrait painted from photos</h2>
<p>Watercolor or oil portraits from photos, $80–500 depending on the artist. Ask to see photos of finished work before paying a deposit.</p>
<h2>9. A star or flower naming</h2>
<p>Novelty registries will "name a star" ($30–60). Sentimental value varies — know your person before choosing this one.</p>
<h2>10. A handmade memorial ornament</h2>
<p>Felted or ceramic ornaments ($25–90) are especially appreciated around the first holiday without the pet — the hardest one of all.</p>

<h2>How to choose</h2>
<p>Ask one question: <i>does this person want to see their pet every day, or hold something when it hurts?</i> Wall pieces serve the first; <a href="/needle-felted-pet-memorial-gift/">handheld keepsakes like our felted portraits</a> serve the second. Whatever you choose, include a handwritten note mentioning the pet by name — it costs nothing and matters more than the gift itself.</p>
"""
},
{
 "route": "/guides/are-custom-pet-portraits-worth-it/",
 "title": "Are Custom Pet Portraits Worth It? An Honest Answer | Again Paws",
 "desc": "What a custom pet portrait actually costs, what decides quality, and how to tell a keepsake worth ordering from a printed photo with a filter. Honest guide, no sales pitch.",
 "ld_types": ["Article", "BreadcrumbList", "FAQPage"],
 "body": """
<h1>Are Custom Pet Portraits Worth It?</h1>
<p class="updated">By the Again Paws studio · October 2026</p>
<p>Straight answer: yes, if you want a one-of-a-kind object made from your pet's actual photos and you pick the right maker. No, if you expect it to be cheap, fast, or identical to the photo. Here is the honest breakdown.</p>

<h2>What you are really paying for</h2>
<p>A custom portrait is not "a photo with a style on it." A handmade felted portrait takes 15–40 hours of handwork: building form layer by layer, matching the white sock on the left paw, getting the half-ear to stand the way it always did. You are paying for hours of skilled labor on a single object that exists for exactly one purpose — your pet.</p>

<h2>What it costs (and why the range is so wide)</h2>
<p>Printed digital portraits: $15–50, same-day, and honestly worth about that. Painted portraits: $80–500. <a href="/guides/needle-felted-pet-cost/">Handmade needle-felted keepsakes run $87–477</a> depending on size and detail. The wider the range, the more you should ask what is included: revisions, progress photos, frame, shipping.</p>

<h2>The three signs of a maker worth ordering from</h2>
<ul>
  <li><b>They ask for specific photos</b> — eye-level, good light, clear markings. A maker who explains <a href="/guides/best-photos-for-felted-pet/">what photos work best</a> is a maker who plans to match your pet, not a generic dog.</li>
  <li><b>They confirm the design before starting</b> — quote, pose, timeline, all in writing.</li>
  <li><b>They have a real refund policy</b> — custom work should still protect you before production starts, and repair guarantees after delivery.</li>
</ul>

<h2>When it is not worth it</h2>
<p>Skip the custom order if you need it this week (a framed print will do), if the pet's photos are all blurry and the maker never mentions it, or if the price is far below everyone else — handmade work has a floor, and prices below it mean molds or outsourcing.</p>

<h2>Frequently asked</h2>
<div class="faq-item"><h2>Will it actually look like my pet?</h2><p>A good maker will tell you honestly what they can capture from your photos — and will keep adjusting the details until it does. Ask before ordering what happens if the likeness misses.</p></div>
<div class="faq-item"><h2>What if my pet has passed away and I only have old photos?</h2><p>That is most of our memorial orders. Older, slightly blurry photos usually contain enough detail. A good maker tells you what is possible before you pay — see our <a href="/needle-felted-pet-memorial-gift/">memorial keepsake page</a>.</p></div>
<div class="faq-item"><h2>Is handmade really better than a digital print?</h2><p>Different things. A print decorates; a felted sculpture commemorates. If you want an object with weight, texture and hours of human attention in it, handmade wins. If you want a quick gift, print.</p></div>

<p class="foot-cta">Curious what your photos could become? <a class="btn" href="/contact/">Request a free quote</a> — we reply within 24 hours with honest advice, even if the answer is "a felted portrait isn't right for these photos."</p>
"""
},
{
 "route": "/guides/how-long-does-a-custom-pet-portrait-take/",
 "title": "How Long Does a Custom Pet Portrait Take? Realistic Timelines | Again Paws",
 "desc": "Realistic production times for custom pet portraits: digital prints, paintings and handmade felted keepsakes, plus what actually causes delays and how to get it faster.",
 "ld_types": ["Article", "BreadcrumbList", "FAQPage"],
 "body": """
<h1>How Long Does a Custom Pet Portrait Take?</h1>
<p class="updated">By the Again Paws studio · October 2026</p>
<p>Short answer: a printed portrait takes days, a painting takes 2–6 weeks, and a handmade felted keepsake takes 2–4 weeks of production plus shipping. Here is what happens inside those weeks, and what actually causes delays.</p>

<h2>By portrait type</h2>
<ul>
  <li><b>Printed / digital:</b> 1–5 days. The artist edits a photo; nothing is made by hand.</li>
  <li><b>Painted:</b> 2–6 weeks. Oil dries slowly; watercolor is faster.</li>
  <li><b>Needle-felted (our craft):</b> 2–4 weeks. Each piece is built by hand, one layer at a time — a mini portrait needs around 15 hours of felting, a full-body piece considerably more.</li>
</ul>

<h2>The five steps that make up those weeks</h2>
<ol>
  <li><b>Photo review &amp; quote</b> (1–2 days): you send photos, we confirm what we can capture, style and price.</li>
  <li><b>Design confirmation</b> (1–2 days): pose, size and timeline agreed in writing.</li>
  <li><b>Felting</b> (2–4 weeks): the core work. Larger pieces include <a href="/custom-pet-keepsake-from-photo/">progress photos</a> before final detailing.</li>
  <li><b>Your review</b> (1–3 days): final-detail photos sent to you; small adjustments made.</li>
  <li><b>Shipping</b> (3–10 days worldwide, tracked): protective packaging designed for international transit.</li>
</ol>

<h2>What actually causes delays</h2>
<ul>
  <li><b>Vague photos.</b> Blurry or dark photos mean a round of "can you send another?" — the single most common delay. Ten seconds spent on <a href="/guides/best-photos-for-felted-pet/">our photo guide</a> saves a week.</li>
  <li><b>Slow replies during design confirmation.</b> The felting clock starts when you approve the quote, not when you first message.</li>
  <li><b>Holiday season.</b> Orders placed in November queue behind earlier ones. Order early for Christmas; most studios, including ours, say this every year and every year someone is surprised.</li>
</ul>

<h2>Can it be faster?</h2>
<p>Ask before ordering — some studios offer rush slots for a fee. What we don't recommend is skipping the design confirmation: it is the cheapest insurance that the finished piece matches your pet.</p>

<h2>Frequently asked</h2>
<div class="faq-item"><h2>How long does shipping take after production?</h2><p>3–10 days worldwide with tracking, depending on your country. The tracking number is sent the day it ships.</p></div>
<div class="faq-item"><h2>Can I request changes while it is being made?</h2><p>Yes — that is exactly what the progress-photo stage is for. Changes that affect price or timeline are always confirmed with you first.</p></div>
<div class="faq-item"><h2>What if I need it for a specific date?</h2><p>Tell us the date in your first message. We will tell you honestly whether it fits the queue before you pay anything.</p></div>

<p class="foot-cta">Planning ahead? <a class="btn" href="/contact/">Send your photos today</a> and get a written timeline with your quote — production time is confirmed before felting begins.</p>
"""
},
]

created = []
for p in PAGES:
    out = REPO / p["route"].strip("/") / "index.html"
    if out.exists():
        print("skip existing:", p["route"]); continue
    out.parent.mkdir(parents=True, exist_ok=True)
    lds = []
    name = p["route"].strip("/").split("/")[-1].replace("-", " ").title()
    for t in p["ld_types"]:
        if t == "Article":
            lds.append({"@context": "https://schema.org", "@type": "Article",
                "headline": p["title"].split("|")[0].strip(),
                "author": {"@type": "Organization", "name": "Again Paws"},
                "publisher": {"@type": "Organization", "name": "Again Paws", "url": BASE + "/"},
                "datePublished": "2026-10-26", "dateModified": "2026-10-26",
                "mainEntityOfPage": BASE + p["route"]})
        elif t == "BreadcrumbList":
            lds.append({"@context": "https://schema.org", "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Home", "item": BASE + "/"},
                    {"@type": "ListItem", "position": 2, "name": "Guides", "item": BASE + "/guides/"},
                    {"@type": "ListItem", "position": 3, "name": name}]})
        elif t == "FAQPage":
            # 从 body 提取可见 FAQ
            import re
            faqs = re.findall(r'<h2>([^<]+)</h2>\s*<p>(.*?)</p>', p["body"])
            lds.append({"@context": "https://schema.org", "@type": "FAQPage",
                "mainEntity": [{"@type": "Question", "name": re.sub(r"<[^>]+>", "", q).strip(),
                    "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"<[^>]+>", "", a).strip()}}
                    for q, a in faqs]})
    body_with_cta = p["body"]
    html_text = m.page_html(p["route"], p["title"], p["desc"], body_with_cta, lds if len(lds) > 1 else lds[0])
    out.write_text(html_text, encoding="utf-8")
    created.append(p["route"])
    print("created:", p["route"], len(html_text), "bytes")

# ---------------- 2. sitemap 追加 ----------------
NS = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
sm_path = REPO / "sitemap.xml"
import xml.etree.ElementTree as ET
ET.register_namespace("", "http://www.sitemaps.org/schemas/sitemap/0.9")
tree = ET.parse(sm_path)
root = tree.getroot()
locs = {e.text for e in root.iter(NS + "loc")}
added = 0
for p in PAGES:
    url = BASE + p["route"]
    if url in locs: continue
    u = ET.SubElement(root, NS + "url")
    ET.SubElement(u, NS + "loc").text = url
    ET.SubElement(u, NS + "lastmod").text = "2026-10-26"
    added += 1
if added:
    tree.write(sm_path, encoding="utf-8", xml_declaration=True)
print(f"sitemap: +{added} urls ->", len(list(root.iter(NS + 'url'))))

# ---------------- 3. llms.txt 追加 ----------------
llms = REPO / "llms.txt"
t = llms.read_text(encoding="utf-8")
n = 0
for p in PAGES:
    name = p["title"].split("|")[0].strip()
    if p["route"] not in t:
        t += f"- [{name}]({BASE}{p['route']}): {p['desc']}\n"
        n += 1
if n: llms.write_text(t, encoding="utf-8")
print(f"llms.txt: +{n} entries")

# ---------------- 4. guides 枢纽 seo-block 加内链 ----------------
hub = REPO / "guides/index.html"
t = hub.read_text(encoding="utf-8")
extra = ""
for p in PAGES:
    name = p["title"].split("|")[0].strip()
    if p["route"] not in t:
        extra += f'<li><a href="{p["route"]}">{name}</a> \u2014 {p["desc"].split(",")[0].split(" \u2014 ")[0].lower()}.</li>'
if extra:
    marker = "</ul>"
    # 只替换 seo-block 内第一个 ul 的收尾（seo-block 在 </body> 前）
    idx = t.rfind(marker)
    t = t[:idx] + extra + t[idx:]
    hub.write_text(t, encoding="utf-8")
print("guides hub links added:", bool(extra))

# ---------------- 5. 落地页 LCP 预加载 ----------------
PRELOADS = {
    "custom-pet-keepsake-from-photo/index.html": "/images/product-2.webp",
    "needle-felted-pet-memorial-gift/index.html": "/images/product-4.webp",
    "personalized-pet-gift-from-photo/index.html": "/images/product-5.webp",
}
for f, img in PRELOADS.items():
    p = REPO / f
    t = p.read_text(encoding="utf-8")
    tag = f'<link rel="preload" as="image" href="{img}" fetchpriority="high" />'
    if "preload" not in t:
        t = t.replace("</head>", f"    {tag}\n  </head>", 1)
        p.write_text(t, encoding="utf-8")
        print("preload added:", f)
    else:
        print("preload exists:", f)
