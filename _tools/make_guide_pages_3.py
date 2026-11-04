# -*- coding: utf-8 -*-
"""第三批：/guides/dog-memorial-ideas/（GSC 曝光词 dog memorial ideas 5次）。幂等。"""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import make_static_pages as m

REPO = m.REPO
BASE = "https://againpaws.vip"
DATE = "2026-11-04"

PAGE = {
 "route": "/guides/dog-memorial-ideas/",
 "title": "12 Dog Memorial Ideas to Honor a Good Dog | Again Paws",
 "desc": "Heartfelt dog memorial ideas for the yard, home and daily life — from engraved garden stones and custom wind chimes to felted portraits made from your dog's photos.",
 "ld_types": ["Article", "BreadcrumbList", "FAQPage"],
 "body": """
<h1>12 Dog Memorial Ideas</h1>
<p class="updated">By the Again Paws studio · November 2026</p>
<p>Losing a dog leaves a very specific silence — the tag that doesn't jingle, the spot on the couch. A memorial doesn't erase that; it gives the grief somewhere to go. Here are twelve ideas, from backyard tributes to keepsakes made from photos, at every budget.</p>

<h2>Yard and garden memorials</h2>
<ul>
  <li><b>A memorial garden stone with a photo.</b> Weather-safe <a href="/pet-memorial-garden-stone/">garden stones with a ceramic photo window</a> ($79+) mark a resting place or favorite spot in the yard and survive every season.</li>
  <li><b>Plant a tree over the resting place.</b> A hardy native species turns the grave into shade in a few years.</li>
  <li><b>A dedicated flower bed.</b> Plant their favorite "sniffing spot" flowers; add a small marker.</li>
</ul>

<h2>Keepsakes made from photos</h2>
<ul>
  <li><b>A needle-felted portrait of your actual dog.</b> A handmade wool sculpture matching every marking — the crooked ear, the white chest. Works from any clear photos, even for dogs who have passed. <a href="/needle-felted-pet-memorial-gift/">Our memorial keepsakes start at $87</a>.</li>
  <li><b>A custom wind chime with their photo.</b> A <a href="/custom-pet-wind-chime/">photo wind chime on the porch</a> means every breeze is a small hello.</li>
  <li><b>A suncatcher for the window.</b> A <a href="/custom-pet-window-suncatcher/">portrait suncatcher</a> throws their colors across the room every morning.</li>
  <li><b>A framed photo with their collar.</b> Free if you own a frame — the collar draped over the corner does a lot of quiet work.</li>
</ul>

<h2>For their ashes</h2>
<ul>
  <li><b>A custom cremation urn with their portrait.</b> A <a href="/pet-cremation-urn/">hand-painted urn in four colors</a> turns storage into tribute.</li>
  <li><b>A farewell remembrance set.</b> For families who follow the paper-offering tradition, a complete <a href="/pet-memorial-offering-set/">farewell set</a> honors the passing properly.</li>
  <li><b>Scatter in a meaningful place.</b> A favorite trail, beach or lake — check local rules for public land.</li>
</ul>

<h2>Living tributes</h2>
<ul>
  <li><b>Donate to a rescue in their name.</b> Especially powerful for a rescue dog — other dogs get the second chance you gave yours.</li>
  <li><b>A photo album printed of their best 50 photos.</b> $20–40; best made together as a family.</li>
  <li><b>Keep their tag on your keychain.</b> The jingle moves with you.</li>
</ul>

<h2>Choosing between them</h2>
<p>One question sorts it: <i>do you want a place to visit, or something to hold?</i> Garden stones and trees serve the first; <a href="/guides/pet-memorial-gift-ideas/">handheld keepsakes like felted portraits</a> serve the second. Many families end up with one of each — a stone for the yard, a portrait inside.</p>

<h2>Frequently asked</h2>
<div class="faq-item"><h2>What is a good memorial for a dog?</h2><p>Something made from the dog's actual photo — a felted portrait, garden stone or wind chime — because specificity is what makes a memorial feel real. Generic paw prints read as generic; your dog's own markings do not.</p></div>
<div class="faq-item"><h2>How much should a dog memorial cost?</h2><p>Meaningful options exist at every budget: framed photos are nearly free, wind chimes and garden stones run $40–100, and handmade portraits $87–477 depending on size.</p></div>
<div class="faq-item"><h2>Can a memorial be made if I only have old or blurry photos?</h2><p>Usually yes — experienced makers work from phone photos all the time. Send what you have and ask honestly what's possible before paying anything.</p></div>

<p class="foot-cta">Have photos of your good dog? <a class="btn" href="/contact/">Send them for a free quote</a> — honest advice within 24 hours, even if a portrait isn't the right fit.</p>
"""
}

out = REPO / PAGE["route"].strip("/") / "index.html"
if out.exists():
    print("skip existing:", PAGE["route"])
else:
    import re
    out.parent.mkdir(parents=True, exist_ok=True)
    lds = []
    name = "Dog Memorial Ideas"
    lds.append({"@context": "https://schema.org", "@type": "Article",
        "headline": PAGE["title"].split("|")[0].strip(),
        "author": {"@type": "Organization", "name": "Again Paws"},
        "publisher": {"@type": "Organization", "name": "Again Paws", "url": BASE + "/"},
        "datePublished": DATE, "dateModified": DATE,
        "mainEntityOfPage": BASE + PAGE["route"]})
    lds.append({"@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": BASE + "/"},
            {"@type": "ListItem", "position": 2, "name": "Guides", "item": BASE + "/guides/"},
            {"@type": "ListItem", "position": 3, "name": name}]})
    faqs = re.findall(r'<h2>([^<]+)</h2>\s*<p>(.*?)</p>', PAGE["body"])
    lds.append({"@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": re.sub(r"<[^>]+>", "", q).strip(),
            "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"<[^>]+>", "", a).strip()}}
            for q, a in faqs]})
    html_text = m.page_html(PAGE["route"], PAGE["title"], PAGE["desc"], PAGE["body"], lds)
    out.write_text(html_text, encoding="utf-8")
    print("created:", PAGE["route"], len(html_text), "bytes")

# ---- sitemap ----
NS = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
import xml.etree.ElementTree as ET
ET.register_namespace("", "http://www.sitemaps.org/schemas/sitemap/0.9")
sm = REPO / "sitemap.xml"
tree = ET.parse(sm); root = tree.getroot()
locs = {e.text for e in root.iter(NS + "loc")}
if BASE + PAGE["route"] not in locs:
    u = ET.SubElement(root, NS + "url")
    ET.SubElement(u, NS + "loc").text = BASE + PAGE["route"]
    ET.SubElement(u, NS + "lastmod").text = DATE
    tree.write(sm, encoding="utf-8", xml_declaration=True)
print("sitemap total:", len(list(root.iter(NS + "url"))))

# ---- llms.txt ----
llms = REPO / "llms.txt"
t = llms.read_text(encoding="utf-8")
if PAGE["route"] not in t:
    t += f"- [{PAGE['title'].split('|')[0].strip()}]({BASE}{PAGE['route']}): {PAGE['desc']}\n"
    llms.write_text(t, encoding="utf-8")
    print("llms.txt: +1")

# ---- guides 枢纽 ----
hub = REPO / "guides/index.html"
t = hub.read_text(encoding="utf-8")
if PAGE["route"] not in t:
    name = PAGE["title"].split("|")[0].strip()
    idx = t.rfind("</ul>")
    t = t[:idx] + f'<li><a href="{PAGE["route"]}">{name}</a> \u2014 backyard, home and keepsake tributes.</li>' + t[idx:]
    hub.write_text(t, encoding="utf-8")
    print("hub: +1")
