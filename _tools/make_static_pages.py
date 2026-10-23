# -*- coding: utf-8 -*-
"""生成 4 个静态信任页（privacy/terms/refund-policy/faq），品牌风格自包含。"""
import json, pathlib, html

REPO = pathlib.Path(r"C:/Users/16554/WorkBuddy/2026-10-23-10-20-59/againpaws")

CSS = """
:root{--green:#6C8C5A;--green-dark:#557047;--ink:#2b2f33;--sub:#6b7280;--bg:#faf9f6;--card:#fff;--line:#e6e3dc}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:Georgia,'Times New Roman',serif;color:var(--ink);background:var(--bg);line-height:1.75;font-size:16px}
header{background:var(--card);border-bottom:1px solid var(--line);padding:14px 20px;display:flex;flex-wrap:wrap;gap:18px;align-items:center;justify-content:space-between}
header .brand{font-size:19px;font-weight:700;color:var(--green-dark);text-decoration:none;letter-spacing:.5px}
nav{display:flex;flex-wrap:wrap;gap:16px}
nav a{color:var(--ink);text-decoration:none;font-family:Helvetica,Arial,sans-serif;font-size:14px}
nav a:hover{color:var(--green-dark)}
main{max-width:760px;margin:0 auto;padding:48px 20px 80px}
h1{font-size:30px;margin-bottom:6px;color:var(--green-dark)}
h2{font-size:19px;margin:28px 0 10px}
.updated{color:var(--sub);font-size:13.5px;margin-bottom:28px;font-family:Helvetica,Arial,sans-serif}
p,li{margin:10px 0}
ul{padding-left:22px}
a{color:var(--green-dark)}
.foot-cta{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:18px 22px;margin-top:40px}
.foot-cta b{color:var(--green-dark)}
.btn{display:inline-block;background:var(--green);color:#fff;text-decoration:none;padding:10px 22px;border-radius:6px;font-family:Helvetica,Arial,sans-serif;font-size:14.5px;margin-top:10px}
.btn:hover{background:var(--green-dark)}
footer{border-top:1px solid var(--line);padding:24px 20px;text-align:center;color:var(--sub);font-size:13px;font-family:Helvetica,Arial,sans-serif}
footer nav{justify-content:center;margin-bottom:8px}
.faq-item{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:18px 22px;margin:14px 0}
.faq-item h2{margin:0 0 8px;font-size:17px}
"""

NAV = """<header>
  <a class="brand" href="/">Again Paws</a>
  <nav>
    <a href="/products/">Products</a>
    <a href="/pricing/">Pricing</a>
    <a href="/guides/">Guides</a>
    <a href="/faq/">FAQ</a>
    <a href="/contact/">Contact</a>
  </nav>
</header>"""

FOOTER = """<footer>
  <nav>
    <a href="/privacy/">Privacy</a>
    <a href="/terms/">Terms</a>
    <a href="/refund-policy/">Refunds</a>
    <a href="/faq/">FAQ</a>
  </nav>
  &copy; 2026 Again Paws · Handmade needle-felted pet keepsakes
</footer>"""

def page_html(route, title, desc, body, json_ld=None):
    ld = ""
    if json_ld:
        ld = f'    <script type="application/ld+json">\n{json.dumps(json_ld, ensure_ascii=False, indent=2)}\n    </script>\n'
    return f"""<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{html.escape(title)}</title>
    <link rel="icon" type="image/svg+xml" href="/favicon.svg" />
    <meta name="description" content="{html.escape(desc)}" />
    <meta name="robots" content="index, follow" />
    <link rel="canonical" href="https://againpaws.vip{route}" />
    <meta property="og:type" content="website" />
    <meta property="og:site_name" content="Again Paws" />
    <meta property="og:url" content="https://againpaws.vip{route}" />
    <meta property="og:title" content="{html.escape(title)}" />
    <meta property="og:description" content="{html.escape(desc)}" />
    <meta name="twitter:card" content="summary" />
    <style>{CSS}</style>
{ld}</head>
<body>
{NAV}
<main>
{body}
</main>
{FOOTER}
</body>
</html>
"""

EMAIL = "q8461994@gmail.com"

PRIVACY_BODY = """
<h1>Privacy Policy</h1>
<p class="updated">Last updated: October 23, 2026</p>

<h2>1. Who we are</h2>
<p>Again Paws ("we", "us") is a handmade studio creating custom needle-felted pet keepsakes from customer photos. This policy explains what information we collect at againpaws.vip and how we use it. Contact us any time at <b>q8461994@gmail.com</b>.</p>

<h2>2. Information we collect</h2>
<ul>
  <li><b>Contact details</b> you give us when requesting a quote or placing an order: name, email address, and shipping address.</li>
  <li><b>Pet photos</b> you send us so we can create your keepsake. Photos are used only to produce your order.</li>
  <li><b>Order details</b>: the items you order, prices, and communication history about your order.</li>
  <li><b>Basic analytics</b> (page views, approximate region, device type) collected through our analytics script to understand how the site is used. No advertising profiles are built from this data.</li>
</ul>

<h2>3. How we use your information</h2>
<ul>
  <li>To create your custom keepsake and deliver it to you.</li>
  <li>To communicate with you about your quote, order, or questions.</li>
  <li>To improve the website (which pages are useful, what visitors look for).</li>
  <li>We never sell your personal information or your photos.</li>
</ul>

<h2>4. Photos of your pet</h2>
<p>Your photos are used solely as reference material for your order. With your permission, we may share photos of the finished keepsake on our website or social media — we will always ask first, and we never publish your name or address alongside them. If you prefer we don't, just say so and we won't.</p>

<h2>5. Sharing</h2>
<p>We share information only with the services needed to run the studio: our email provider, payment processor, and shipping carriers. Each receives only what is necessary (for example, the shipping carrier receives your address and nothing else).</p>

<h2>6. Data retention</h2>
<p>Order records are kept for accounting and warranty purposes. Pet photos are kept only as long as needed to complete your order, unless you ask us to keep them for future orders. You can request deletion at any time via <b>q8461994@gmail.com</b>.</p>

<h2>7. Your rights</h2>
<p>You may ask us to access, correct, or delete your personal information, or withdraw consent for us to use your photos, at any time. Email us and we will respond within 7 days.</p>

<h2>8. Cookies</h2>
<p>We use a minimal analytics script that stores a small identifier to count visits. You can block it with any browser setting or extension without affecting how the site works.</p>

<h2>9. Changes</h2>
<p>If this policy changes we will update the date at the top. Material changes will also be announced on this page before they take effect.</p>
"""

TERMS_BODY = """
<h1>Terms of Service</h1>
<p class="updated">Last updated: October 23, 2026</p>

<h2>1. About these terms</h2>
<p>These terms apply to every order placed with Again Paws (againpaws.vip). By requesting a quote or placing an order you agree to them. Questions? Email <b>q8461994@gmail.com</b>.</p>

<h2>2. What we make</h2>
<p>Every keepsake is handmade to order from the photos you provide. Needle felting is a hand craft: your keepsake will capture your pet's likeness, character, and markings, but it is a wool artwork, not a factory-made replica. Minor variations are part of what makes each piece one of a kind.</p>

<h2>3. Quotes and orders</h2>
<ul>
  <li>Prices range from $87 to $477 USD depending on size and complexity; the final quote is confirmed before production starts.</li>
  <li>An order is confirmed when we receive your photos, your approval of the quote, and payment.</li>
  <li>Production typically takes 2–4 weeks, plus shipping time.</li>
</ul>

<h2>4. Your photos</h2>
<p>You confirm that you own the photos you send us (or have permission to use them). See our <a href="/guides/best-photos-for-felted-pet/">photo guide</a> for what works best; if a photo won't produce a good likeness we'll ask for alternatives before starting.</p>

<h2>5. Approval during production</h2>
<p>For larger pieces we send progress photos before final detailing. Changes requested at this stage are possible; significant changes may affect the price or timeline, and we'll always confirm with you first.</p>

<h2>6. Shipping</h2>
<p>We ship worldwide from our studio. Shipping cost and estimated delivery time are confirmed with your quote. Customs duties or taxes in your country, if any, are the buyer's responsibility.</p>

<h2>7. Cancellations, changes and problems</h2>
<p>Because each piece is custom-made, our refund rules follow the production stage — see the <a href="/refund-policy/">Refund &amp; Returns Policy</a> for the details.</p>

<h2>8. Liability</h2>
<p>Our liability for any order is limited to the amount you paid for it. We pack every keepsake carefully; if it arrives damaged, contact us with photos within 7 days and we will make it right (replacement or repair).</p>

<h2>9. Contact</h2>
<p>Again Paws · <b>q8461994@gmail.com</b> · or via the <a href="/contact/">contact page</a>.</p>
"""

REFUND_BODY = """
<h1>Refund &amp; Returns Policy</h1>
<p class="updated">Last updated: October 23, 2026</p>
<p>Every Again Paws keepsake is handmade to order, so returns work a little differently from off-the-shelf products. Here is exactly what happens at each stage — no small print games.</p>

<h2>Stage 1 — Before production starts</h2>
<p>You can cancel or change your order for a <b>full refund</b> at any time before we begin felting. We always confirm the design and quote with you first, so you have a clear "start" moment.</p>

<h2>Stage 2 — During production</h2>
<p>Once production starts, materials and hours are committed to your piece. If you need to cancel at this stage, we refund <b>50% of the order price</b>. For larger pieces you'll see progress photos along the way, and any concern you raise will be fixed before completion.</p>

<h2>Stage 3 — Finished piece</h2>
<p>Because each keepsake is a one-of-a-kind custom artwork made to your pet's photos, finished pieces are <b>not returnable for change of mind</b>. If the likeness doesn't capture your pet, tell us — we will keep adjusting the details (fur color, markings, expression) until it does. We'd rather spend another week than have you disappointed.</p>

<h2>If it arrives damaged</h2>
<p>Every keepsake ships in protective packaging. If yours arrives damaged, send photos within <b>7 days</b> of delivery and we will repair or remake the piece and reship it at our cost.</p>

<h2>If it goes missing</h2>
<p>If tracking shows delivery but the package never arrived, or it is lost in transit, contact us — after the carrier's investigation (usually 2–4 weeks) we will remake and reship your keepsake.</p>

<h2>How to reach us</h2>
<p>Email <b>q8461994@gmail.com</b> with your order number and photos. We reply within 24 hours, 7 days a week.</p>

<div class="foot-cta">
  <p>Ready to turn your pet's photo into a keepsake?</p>
  <a class="btn" href="/contact/">Request a Quote</a>
</div>
"""

FAQS = [
  ("What is a custom needle-felted pet replica?",
   "It is a one-of-a-kind sculpture of your pet, handmade by repeatedly shaping wool fiber with a special barbed needle. We work from your photos to match your pet's fur color, markings, pose and expression. Each piece takes many hours of handwork and is made to order — no two are ever alike."),
  ("How much does a custom felted pet cost?",
   "Again Paws keepsakes range from $87 for a Mini Portrait to $477 for a Full-Body piece. The final quote depends on size, pose complexity and fur detail. See the <a href='/pricing/'>pricing page</a> for what is included at each level."),
  ("How long does it take to make?",
   "Production typically takes 2–4 weeks depending on the size and complexity of your piece, plus shipping time to your country. We confirm the exact timeline with your quote before starting, and you can request updates at any time."),
  ("What photos work best?",
   "Clear, well-lit photos taken at your pet's eye level work best: one showing the whole body or head, plus close-ups of the face, and photos of any distinctive markings. Multiple angles help a lot. See our <a href='/guides/best-photos-for-felted-pet/'>photo guide</a> for examples."),
  ("Can you make a keepsake of a pet that has passed away?",
   "Yes — memorial keepsakes are one of the main reasons people order from us. Send us the best photos you have, even older ones. We will tell you honestly what we can capture before production starts, and we handle every memorial order with extra care."),
  ("What are the keepsakes made of?",
   "High-quality wool fiber, shaped entirely by hand using needle-felting techniques — no molds, no machines. Glass eyes are used for realism, and pieces can include a frame or base depending on the style you choose."),
  ("Do you ship worldwide?",
   "Yes, we ship worldwide from our studio with tracking. Shipping cost and estimated delivery time are confirmed with your quote. Every keepsake is packed in protective packaging designed for international transit."),
  ("Can I request changes while my keepsake is being made?",
   "Yes. For larger pieces we send progress photos before final detailing, and you can request adjustments then. We would always confirm with you before making any change that affects price or timeline."),
  ("What if I'm not happy with the result?",
   "Tell us — we will keep adjusting the details until the piece truly captures your pet. Our refund policy is stage-based: full refund before production starts, a partial refund during production, and free fixes for anything that arrives damaged. See the <a href='/refund-policy/'>refund policy</a>."),
  ("How do I order?",
   "Send us your photos through the <a href='/contact/'>contact page</a> and tell us which style you are interested in. We will reply with a quote, a production timeline, and photo advice if needed. Once you approve, production begins."),
]

FAQ_BODY = """
<h1>Frequently Asked Questions</h1>
<p class="updated">Everything people usually ask before ordering a custom needle-felted pet keepsake.</p>
""" + "".join(
    f'<div class="faq-item"><h2>{q}</h2><p>{a}</p></div>' for q, a in FAQS
) + """
<div class="foot-cta">
  <p>Something else on your mind? Ask us any time.</p>
  <a class="btn" href="/contact/">Contact Us</a>
</div>
"""

FAQ_LD = {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": [
        {"@type": "Question", "name": q,
         "acceptedAnswer": {"@type": "Answer", "text": a}}
        for q, a in FAQS
    ],
}

PAGES = [
    ("privacy/index.html", "/privacy/", "Privacy Policy | Again Paws",
     "How Again Paws collects, uses and protects your personal information, including the photos you share for your custom pet keepsake.",
     PRIVACY_BODY, None),
    ("terms/index.html", "/terms/", "Terms of Service | Again Paws",
     "The terms that apply when you order a custom needle-felted pet keepsake from Again Paws: quotes, production, shipping and what to expect.",
     TERMS_BODY, None),
    ("refund-policy/index.html", "/refund-policy/", "Refund & Returns Policy | Again Paws",
     "Clear, stage-based refund policy for Again Paws custom pet keepsakes: before, during and after production, plus our damage and loss guarantee.",
     REFUND_BODY, None),
    ("faq/index.html", "/faq/", "Custom Pet Keepsake FAQ | Again Paws",
     "Answers about custom needle-felted pet keepsakes: prices ($87-$477), production time, best photos, memorial orders, worldwide shipping and refunds.",
     FAQ_BODY, FAQ_LD),
]

for rel, route, title, desc, body, ld in PAGES:
    p = REPO / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(page_html(route, title, desc, body, ld), encoding="utf-8")
    print("written:", rel)
