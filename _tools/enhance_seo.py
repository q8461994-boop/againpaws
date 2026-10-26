# -*- coding: utf-8 -*-
"""P1 SEO 注入：全站 BreadcrumbList/Organization schema + 薄页面静态内容扩充。
内容区块插在 </body> 前、#root 之外，React 重挂载不会清除。幂等可重跑。
"""
import json, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
BASE = "https://againpaws.vip"
MARK = 'data-seo-injected'

def load(p):
    return (ROOT / p).read_text(encoding="utf-8")

def save(p, t):
    (ROOT / p).write_text(t, encoding="utf-8")

def ld_script(obj):
    return '<script type="application/ld+json">\n' + json.dumps(obj, indent=2, ensure_ascii=False) + '\n</script>\n'

def inject_ld(path, obj, slot_id):
    """按 slot_id 幂等注入 JSON-LD 到 </head> 前。"""
    t = load(path)
    if f"<!-- {slot_id} -->" in t:
        return False
    s = f'<!-- {slot_id} -->\n' + ld_script(obj)
    assert "</head>" in t, path
    t = t.replace("</head>", s + "  </head>", 1)
    save(path, t)
    return True

# ---------- 1. 首页 Organization + WebSite ----------
home_ld = {
    "@context": "https://schema.org",
    "@graph": [
        {"@type": "Organization", "@id": BASE + "/#organization",
         "name": "Again Paws", "url": BASE + "/",
         "logo": BASE + "/images/logo.svg",
         "description": "Handmade custom needle-felted pet replicas and keepsakes crafted from your photos."},
        {"@type": "WebSite", "@id": BASE + "/#website",
         "url": BASE + "/", "name": "Again Paws",
         "publisher": {"@id": BASE + "/#organization"},
         "inLanguage": "en"},
    ],
}
inject_ld("index.html", home_ld, "ld-org-website")

# ---------- 2. 内页 BreadcrumbList ----------
CRUMBS = {
    "about/index.html": ["About"],
    "contact/index.html": ["Contact"],
    "customization/index.html": ["Customization"],
    "pricing/index.html": ["Pricing"],
    "products/index.html": ["Products"],
    "process/index.html": ["How to Order"],
    "guides/index.html": ["Guides"],
    "guides/best-photos-for-felted-pet/index.html": ["Guides", "Best Photos for a Felted Pet Replica"],
    "guides/custom-needle-felted-pet-replica-from-photo/index.html": ["Guides", "Custom Needle-Felted Pet Replica From a Photo"],
    "guides/needle-felted-pet-cost/index.html": ["Guides", "How Much Does a Custom Needle-Felted Pet Cost?"],
    "custom-pet-keepsake-from-photo/index.html": ["Custom Pet Keepsake From a Photo"],
    "needle-felted-pet-memorial-gift/index.html": ["Pet Memorial Gift"],
    "personalized-pet-gift-from-photo/index.html": ["Personalized Pet Gift From a Photo"],
    "faq/index.html": ["FAQ"],
}
def breadcrumb(pages):
    items, url = [], BASE + "/"
    items.append({"@type": "ListItem", "position": 1, "name": "Home", "item": url})
    for i, name in enumerate(pages, start=2):
        if i == len(pages) + 1:
            url = None  # 最后一项可不带 item
        items.append({"@type": "ListItem", "position": i, "name": name})
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": items}

n_bc = 0
for path, pages in CRUMBS.items():
    if inject_ld(path, breadcrumb(pages), "ld-breadcrumb"):
        n_bc += 1

# ---------- 3. 薄页面内容扩充 ----------
STYLE = ('<style>.seo-block{max-width:860px;margin:0 auto;padding:48px 24px 64px;border-top:1px solid #e5e0d8;'
         'font-family:inherit;line-height:1.7;color:#3d3a34}.seo-block h2{font-size:1.5rem;margin:0 0 16px}'
         '.seo-block h3{font-size:1.1rem;margin:24px 0 6px}.seo-block p{margin:0 0 14px}'
         '.seo-block a{color:#8a6d3b;text-decoration:underline}.seo-block ul{padding-left:20px;margin:0 0 14px}</style>')

def block(title, paragraphs):
    """paragraphs: list of str 或 ('h3', str) 或 ('ul', [..])"""
    inner = f"<h2>{title}</h2>"
    for p in paragraphs:
        if isinstance(p, tuple) and p[0] == "h3":
            inner += f"<h3>{p[1]}</h3>"
        elif isinstance(p, tuple) and p[0] == "ul":
            inner += "<ul>" + "".join(f"<li>{x}</li>" for x in p[1]) + "</ul>"
        else:
            inner += f"<p>{p}</p>"
    return ('<section class="seo-block" ' + MARK + ' aria-label="More about our keepsakes">' + inner + "</section>")

CONTENT = {
    "guides/index.html": block("Learn before you order: guides from the studio", [
        "Every custom pet keepsake starts with a photo and a question: \u201cCan this really be made?\u201d "
        "The answer is almost always yes \u2014 but the quality of the result depends on the photos you send, "
        "the size you choose and how the sculpture will be built up layer by layer. These guides walk you "
        "through each decision before you spend a dollar.",
        ("h3", "Start with these three"),
        ("ul", [
            '<a href="/guides/best-photos-for-felted-pet/">Best photos for a custom felted pet replica</a> \u2014 which angles, lighting and close-ups let us match fur color, markings and expression accurately.',
            '<a href="/guides/needle-felted-pet-cost/">How much does a custom needle-felted pet cost?</a> \u2014 what changes the price between $87 and $477, and what is included at every level.',
            '<a href="/guides/custom-needle-felted-pet-replica-from-photo/">Custom needle-felted pet replica from a photo</a> \u2014 the full journey from your photos to the finished sculpture.',
        ]),
        ("h3", "Then choose your piece"),
        'Once you know what is possible, browse the <a href="/products/">full range of keepsakes</a>, check '
        '<a href="/pricing/">current pricing from $87</a>, or read the <a href="/faq/">frequently asked questions</a> '
        'covering production time (2\u20134 weeks), worldwide shipping and our stage-based refund policy. '
        'Still unsure? <a href="/contact/">Send us your photos</a> and we will tell you honestly what we can capture \u2014 '
        'before you order.',
    ]),
    "custom-pet-keepsake-from-photo/index.html": block("How a photo becomes a felted keepsake", [
        "A custom pet keepsake made from a photo is not printed or molded \u2014 it is built by hand, one poke at a time, "
        "with a barbed needle that tangles wool fiber into firm sculpture. Your photos are the blueprint: we match the "
        "fur color, the white socks, the crooked ear, the exact way your pet tilts its head.",
        ("h3", "The four steps"),
        ("ul", [
            "You send 2\u20135 clear photos (see our <a href=\"/guides/best-photos-for-felted-pet/\">photo guide</a>) and tell us the pose you want.",
            "We reply within 24 hours with a quote, a timeline and honest advice on what we can capture.",
            "A studio artist needle-felts your piece over 2\u20134 weeks, sending progress photos on larger works.",
            "Your keepsake ships worldwide in protective packaging, with tracking.",
        ]),
        ("h3", "What it costs and what is guaranteed"),
        'Pieces range from <a href="/pricing/">$87 for a Mini Portrait to $477 for a Full-Body portrait</a>. Every order '
        'is covered by our stage-based refund policy and a damage-in-transit guarantee \u2014 details on the '
        '<a href="/products/">products page</a> and in the <a href="/faq/">FAQ</a>. Memorial orders are handled with '
        'extra care; you can read more about <a href="/needle-felted-pet-memorial-gift/">pet memorial gifts here</a>.',
    ]),
    "needle-felted-pet-memorial-gift/index.html": block("A gentle way to keep them close", [
        "When a pet passes away, the photos that remain often say more than words. A custom needle-felted memorial gift "
        "turns one of those photos into something you can hold: the curled-up sleeping pose, the grey around the muzzle, "
        "the way one ear never stood up quite straight.",
        ("h3", "Made for older photos too"),
        "You do not need perfect studio shots. Blurry phone pictures, photos from years ago, even a favorite snapshot "
        "where only the face is sharp \u2014 send what you have. Before production starts we will tell you honestly what "
        "we can capture from your photos, so there are no surprises.",
        ("h3", "Timing, care and next steps"),
        'Production takes 2\u20134 weeks plus shipping, and larger memorial pieces include progress photos so you can '
        'follow along. Many families order two: one to keep, one for a parent or child. To begin, '
        '<a href="/contact/">send us your photos</a> and mention it is a memorial order \u2014 we will handle it with '
        'the extra care it deserves. You can also read the full '
        '<a href="/guides/custom-needle-felted-pet-replica-from-photo/">process guide</a> or the '
        '<a href="/faq/">FAQ</a> first.',
    ]),
    "personalized-pet-gift-from-photo/index.html": block("Why a personalized pet gift beats anything store-bought", [
        "A mug with a paw print is nice. A sculpture of \u201cthe actual dog\u201d \u2014 same ears, same markings, same "
        "goofy grin \u2014 makes people cry happy tears when they unwrap it. That is what a personalized pet gift made "
        "from a photo does that nothing off the shelf can.",
        ("h3", "Perfect for every occasion"),
        ("ul", [
            "Birthdays and holidays \u2014 for the person whose phone gallery is 90% pet photos.",
            "New-puppy and adopt-a-versary gifts \u2014 celebrate the newest family member.",
            "Memorial keepsakes \u2014 a gentle way to honor a pet who has passed.",
            "\u201cJust because\u201d \u2014 honestly, most of our orders are this one.",
        ]),
        ("h3", "Ordering is simple"),
        'Pick a style on the <a href="/products/">products page</a> (from <a href="/pricing/">$87</a>), '
        '<a href="/contact/">send us the photos</a>, and we reply within 24 hours with a quote and timeline. '
        'Production takes 2\u20134 weeks, ships worldwide with tracking, and every detail is confirmed with you '
        'before felting begins \u2014 see the <a href="/faq/">FAQ</a> for the full picture.',
    ]),
}

n_ct = 0
for path, html in CONTENT.items():
    t = load(path)
    if MARK in t:
        continue
    assert "</body>" in t, path
    t = t.replace("</body>", STYLE + html + "\n</body>", 1)
    save(path, t)
    n_ct += 1

print(f"breadcrumbs injected: {n_bc}/{len(CRUMBS)}")
print(f"content blocks injected: {n_ct}/{len(CONTENT)}")
