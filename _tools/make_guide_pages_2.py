# -*- coding: utf-8 -*-
"""第二批 2 篇长尾指南：安慰语与送礼礼仪。复用 make_guide_pages 管线。幂等。"""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import make_static_pages as m

REPO = m.REPO
BASE = "https://againpaws.vip"
DATE = "2026-10-30"

PAGES = [
{
 "route": "/guides/what-to-say-when-someones-pet-dies/",
 "title": "What to Say When Someone's Pet Dies: 20 Messages That Help | Again Paws",
 "desc": "What to write when a friend's dog or cat dies: 20 ready-to-use condolence messages, what to never say, and when a small memorial gift says more than words.",
 "ld_types": ["Article", "BreadcrumbList", "FAQPage"],
 "body": """
<h1>What to Say When Someone's Pet Dies</h1>
<p class="updated">By the Again Paws studio · October 2026</p>
<p>When a friend loses a pet, most people freeze — is it "just a dog"? It is not, and the research is clear that pet grief is real grief. The right words are simple, specific and free of clichés. Here are twenty messages you can send today, plus what to avoid and when to send something more than words.</p>

<h2>Short messages for a text or card</h2>
<ul>
  <li>"I'm so sorry about [name]. He was such a good boy, and he was so loved."</li>
  <li>"[Name] was lucky to have you. Thinking of you both."</li>
  <li>"No one could have asked for a better cat mom. I'm here if you want to talk or sit quietly."</li>
  <li>"I remember when you first brought her home. What a lucky life she had."</li>
  <li>"Sending love. Losing a friend like that leaves a real hole."</li>
  <li>"[Name] had the best life a dog could have. That's because of you."</li>
</ul>

<h2>Messages that share a memory</h2>
<p>The most treasured messages mention the specific animal — an anecdote only you know:</p>
<ul>
  <li>"I still laugh about the time [name] stole an entire sandwich off the counter. He was a legend."</li>
  <li>"She always sat on my feet like she owned them. I'm going to miss her."</li>
  <li>"That dog greeted me like a returning soldier every single visit. I loved him too."</li>
</ul>

<h2>What NOT to say</h2>
<ul>
  <li>"It's just a cat/dog" — never, under any circumstances.</li>
  <li>"You can get another one." A pet is not a subscription.</li>
  <li>"At least he didn't suffer" / "At least she was old." Minimizing reads as dismissive.</li>
  <li>"I know exactly how you feel." You don't; make it about them, not you.</li>
</ul>

<h2>When words aren't enough: the memorial gift</h2>
<p>A message fades into the chat history; a physical keepsake stays. If you were close to the person or the pet, a small <a href="/guides/pet-memorial-gift-ideas/">memorial gift made from a photo</a> often lands harder than any sentence — a felted portrait of the actual animal, made from the photos they already have, works even when the loss is fresh. <a href="/needle-felted-pet-memorial-gift/">See how our memorial keepsakes are made</a> — mini portraits start at $87 and ship worldwide.</p>

<h2>Frequently asked</h2>
<div class="faq-item"><h2>How soon should I reach out after a pet dies?</h2><p>Within a day or two — pet grief is sharpest in the first week and most people receive nothing. A late message ("I just heard about [name]") is still welcome weeks later.</p></div>
<div class="faq-item"><h2>Should I mention the pet by name?</h2><p>Yes, always. Grieving owners consistently say hearing the pet's name matters more than any phrasing — it confirms the animal mattered to someone else too.</p></div>
<div class="faq-item"><h2>Is a memorial gift appropriate if I didn't know the pet well?</h2><p>A card is enough for acquaintances. For close friends, a small photo-based keepsake is one of the few gifts people keep for years — our <a href="/guides/pet-memorial-gift-ideas/">memorial gift guide</a> lists options at every budget.</p></div>

<p class="foot-cta">Sending comfort to a friend? <a class="btn" href="/contact/">Ask us about a memorial keepsake from their pet's photo</a> — we reply within 24 hours and never push.</p>
"""
},
{
 "route": "/guides/pet-sympathy-gift-etiquette/",
 "title": "Pet Sympathy Gift Etiquette: When, What, and Who Pays | Again Paws",
 "desc": "Is a pet sympathy gift appropriate? Etiquette for coworkers, friends and family: timing, budgets, religious considerations, and what to do if you never met the pet.",
 "ld_types": ["Article", "BreadcrumbList", "FAQPage"],
 "body": """
<h1>Pet Sympathy Gift Etiquette</h1>
<p class="updated">By the Again Paws studio · October 2026</p>
<p>Giving a gift when someone loses a pet is increasingly normal — but the rules are unwritten, and getting them wrong makes an awkward moment worse. This guide covers who should give, when, how much to spend, and the situations people actually worry about.</p>

<h2>Is a pet sympathy gift appropriate at all?</h2>
<p>Yes — for anyone you'd send flowers to after a human loss. Surveys consistently show a majority of grieving owners felt their pet's death was not taken seriously by people around them; a gift that acknowledges the loss stands out precisely because most people send nothing. The only real mistake is a joke gift ("happy the cat is gone" mugs have ended friendships).</p>

<h2>Timing: when to send it</h2>
<ul>
  <li><b>Within the first week</b>: a card or message. This is the "I see your loss" moment.</li>
  <li><b>2–6 weeks after</b>: the best window for a gift. Support floods in during week one, then evaporates — right when the quiet house starts hurting.</li>
  <li><b>The first anniversary or holiday</b>: a small token is deeply appreciated and almost nobody does it.</li>
</ul>

<h2>How much to spend, by relationship</h2>
<ul>
  <li><b>Coworker:</b> a card, $15–30 (flowers, donation, small keepsake).</li>
  <li><b>Friend:</b> $30–100. A <a href="/custom-pet-wind-chime/">wind chime</a>, engraved stone or framed photo.</li>
  <li><b>Close friend or family:</b> $80–200+. A handmade portrait of their actual pet is the heavyweight option — see <a href="/guides/pet-memorial-gift-ideas/">what's available at each budget</a>.</li>
</ul>

<h2>Tricky situations</h2>
<ul>
  <li><b>You never met the pet.</b> Fine — gifts made from photos don't require you to have known the animal. Order from photos your friend already posted.</li>
  <li><b>The pet is dying, not dead.</b> Wait. A gift arrives better after the loss; a message of support can go now.</li>
  <li><b>Religious or cultural concerns.</b> Photo-based keepsakes are safe across beliefs; skip anything with afterlife imagery unless you know their views.</li>
  <li><b>A group gift.</b> Pooling money for one quality keepsake beats five cheap items — one person collects and orders, everyone signs the card.</li>
</ul>

<h2>Frequently asked</h2>
<div class="faq-item"><h2>Is it weird to give a pet memorial gift to a coworker?</h2><p>A card with a personal line about their pet is perfect for most offices. If the team was close to the pet (office dog), a group gift is common and appreciated.</p></div>
<div class="faq-item"><h2>How long does a custom keepsake take to arrive?</h2><p>Handmade pieces typically need 2–4 weeks plus shipping — which is exactly why they land in the quiet weeks after the loss, when support has dried up. Our <a href="/guides/how-long-does-a-custom-pet-portrait-take/">timeline guide</a> explains the process.</p></div>
<div class="faq-item"><h2>Should the gift include a message?</h2><p>Always — and mention the pet by name. The card is often kept longer than everything else.</p></div>

<p class="foot-cta">Need something made from a friend's pet photos? <a class="btn" href="/contact/">Send us what you have</a> — we'll tell you honestly what's possible within your budget.</p>
"""
},
]

created = []
for p in PAGES:
    out = REPO / p["route"].strip("/") / "index.html"
    if out.exists():
        print("skip existing:", p["route"]); continue
    out.parent.mkdir(parents=True, exist_ok=True)
    import re
    lds = []
    name = p["route"].strip("/").split("/")[-1].replace("-", " ").title()
    for t in p["ld_types"]:
        if t == "Article":
            lds.append({"@context": "https://schema.org", "@type": "Article",
                "headline": p["title"].split("|")[0].strip(),
                "author": {"@type": "Organization", "name": "Again Paws"},
                "publisher": {"@type": "Organization", "name": "Again Paws", "url": BASE + "/"},
                "datePublished": DATE, "dateModified": DATE,
                "mainEntityOfPage": BASE + p["route"]})
        elif t == "BreadcrumbList":
            lds.append({"@context": "https://schema.org", "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Home", "item": BASE + "/"},
                    {"@type": "ListItem", "position": 2, "name": "Guides", "item": BASE + "/guides/"},
                    {"@type": "ListItem", "position": 3, "name": name}]})
        elif t == "FAQPage":
            faqs = re.findall(r'<h2>([^<]+)</h2>\s*<p>(.*?)</p>', p["body"])
            lds.append({"@context": "https://schema.org", "@type": "FAQPage",
                "mainEntity": [{"@type": "Question", "name": re.sub(r"<[^>]+>", "", q).strip(),
                    "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"<[^>]+>", "", a).strip()}}
                    for q, a in faqs]})
    html_text = m.page_html(p["route"], p["title"], p["desc"], p["body"], lds if len(lds) > 1 else lds[0])
    out.write_text(html_text, encoding="utf-8")
    created.append(p["route"])
    print("created:", p["route"], len(html_text), "bytes")

# ---- sitemap ----
NS = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
import xml.etree.ElementTree as ET
ET.register_namespace("", "http://www.sitemaps.org/schemas/sitemap/0.9")
sm = REPO / "sitemap.xml"
tree = ET.parse(sm); root = tree.getroot()
locs = {e.text for e in root.iter(NS + "loc")}
added = 0
for p in PAGES:
    url = BASE + p["route"]
    if url in locs: continue
    u = ET.SubElement(root, NS + "url")
    ET.SubElement(u, NS + "loc").text = url
    ET.SubElement(u, NS + "lastmod").text = DATE
    added += 1
if added:
    tree.write(sm, encoding="utf-8", xml_declaration=True)
print(f"sitemap: +{added} -> total {len(list(root.iter(NS + 'url')))}")

# ---- llms.txt ----
llms = REPO / "llms.txt"
t = llms.read_text(encoding="utf-8")
n = 0
for p in PAGES:
    if p["route"] not in t:
        t += f"- [{p['title'].split('|')[0].strip()}]({BASE}{p['route']}): {p['desc']}\n"
        n += 1
if n: llms.write_text(t, encoding="utf-8")
print(f"llms.txt: +{n}")

# ---- guides 枢纽内链 ----
hub = REPO / "guides/index.html"
t = hub.read_text(encoding="utf-8")
extra = ""
for p in PAGES:
    name = p["title"].split("|")[0].strip()
    if p["route"] not in t:
        extra += f'<li><a href="{p["route"]}">{name}</a> \u2014 {p["desc"].split(":")[0].lower()}.</li>'
if extra:
    idx = t.rfind("</ul>")
    t = t[:idx] + extra + t[idx:]
    hub.write_text(t, encoding="utf-8")
print("hub links:", bool(extra))
