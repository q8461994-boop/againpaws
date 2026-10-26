# -*- coding: utf-8 -*-
"""Again Paws v2 site generator (warm-paper editorial design, tokens from Oura DESIGN.md).

Run from repo root:  python _tools/build_v2.py
Regenerates: assets/site-v2.css, all core pages, reskinned static pages, sitemap, llms.txt, 404.
Idempotent. Existing /images/* webp assets are reused; new-collection art is inline SVG
placeholders (real photos to be dropped in by the owner later).
"""
import os, re, html, json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

SITE = "https://againpaws.vip"

# ----------------------------------------------------------------------------
# 1. DESIGN SYSTEM CSS  (colors / type / radius / spacing taken from Oura DESIGN.md)
# ----------------------------------------------------------------------------
CSS = r""":root{
--color-primary:#2a72de;--color-on-primary:#ffffff;
--color-stone:#4a4741;--color-on-stone:#ffffff;
--color-clay:#6b443d;--color-espresso:#39221e;
--color-gold:#af751b;--color-ochre:#bc924c;--color-gold-pale:#ddbe78;--color-gold-deep:#684d07;
--color-forest:#224228;--color-olive:#5c6f5d;--color-sage:#849671;--color-sage-pale:#ced4b8;
--color-canvas:#f7f1e8;--color-surface:#ffffff;--color-surface-grey:#ececec;
--color-silver:#cccac7;--color-ink-band:#000000;--color-ink-band-soft:#19191c;
--color-ink:#1c1b1a;--color-ash:#838280;--color-mute:#a8a5a0;--color-on-dark:#ffffff;
--color-hairline:#e1dcd3;--color-error:#e33a22;
--font-serif:"Fraunces",Georgia,"Times New Roman",serif;
--font-sans:"Inter",-apple-system,BlinkMacSystemFont,"Segoe UI",Arial,sans-serif;
--radius-xs:4px;--radius-sm:8px;--radius-md:12px;--radius-lg:24px;--radius-xl:40px;--radius-full:9999px;
--space-1:4px;--space-2:8px;--space-3:12px;--space-4:16px;--space-5:24px;--space-6:32px;
--space-7:48px;--space-8:64px;--space-9:96px;--space-10:128px;
--shadow-1:0 6px 24px rgba(28,27,26,.06);
--shadow-2:0 12px 40px rgba(28,27,26,.10);
--maxw:1200px;
}
*,*::before,*::after{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;background:var(--color-canvas);color:var(--color-ink);
font-family:var(--font-sans);font-size:18px;line-height:1.5;-webkit-font-smoothing:antialiased}
img{max-width:100%;display:block}
a{color:var(--color-stone)}
h1,h2,h3{font-family:var(--font-serif);font-weight:300;line-height:1.12;margin:0 0 var(--space-4);letter-spacing:0}
.wrap{max-width:var(--maxw);margin:0 auto;padding:0 var(--space-5)}
.eyebrow{font:700 12px/1.2 var(--font-sans);letter-spacing:1px;text-transform:uppercase;
color:var(--color-ink);margin:0 0 var(--space-4)}
.eyebrow.on-dark{color:var(--color-mute)}
.display{font-family:var(--font-serif);font-weight:300;font-size:clamp(42px,6.4vw,88px);line-height:1.05}
.h1{font-family:var(--font-serif);font-weight:300;font-size:clamp(34px,4.6vw,60px);line-height:1.1}
.h2{font-family:var(--font-serif);font-weight:300;font-size:clamp(28px,3.6vw,44px);line-height:1.15}
.h3{font-family:var(--font-sans);font-weight:400;font-size:clamp(22px,2.4vw,30px);line-height:1.25}
.lead{font-family:var(--font-serif);font-weight:300;font-size:clamp(19px,2vw,24px);line-height:1.35;color:var(--color-stone)}
.muted{color:var(--color-ash)}.small{font-size:14px}.caption{font-size:13px;color:var(--color-ash)}
.section{padding:var(--space-9) 0}
.section-tight{padding:var(--space-8) 0}
.hairline-top{border-top:1px solid var(--color-hairline)}
.center{text-align:center}
.stack>*+*{margin-top:var(--space-4)}
.measure{max-width:680px}
.measure-c{max-width:680px;margin-left:auto;margin-right:auto}

/* ---------- buttons ---------- */
.btn{display:inline-flex;align-items:center;justify-content:center;gap:8px;
font:600 16px/1 var(--font-sans);border-radius:var(--radius-full);
padding:16px 28px;text-decoration:none;border:1px solid transparent;cursor:pointer;transition:filter .15s ease,background .15s ease}
.btn:hover{filter:brightness(.94)}
.btn-primary{background:var(--color-primary);color:var(--color-on-primary)}
.btn-stone{background:var(--color-stone);color:var(--color-on-stone)}
.btn-outline-stone{background:transparent;color:var(--color-stone);border-color:var(--color-stone)}
.btn-on-dark{background:var(--color-canvas);color:var(--color-stone)}
.btn-outline-dark{background:transparent;color:var(--color-on-dark);border-color:var(--color-on-dark)}
.btn-sm{padding:11px 20px;font-size:14px}
.btn-row{display:flex;flex-wrap:wrap;gap:var(--space-3);margin-top:var(--space-5)}

/* ---------- announcement + header ---------- */
.announce{background:var(--color-canvas);text-align:center;padding:10px 16px;
font:700 12px/1.2 var(--font-sans);letter-spacing:1px;text-transform:uppercase;color:var(--color-ink)}
.announce.band-clay{background:var(--color-clay);color:var(--color-gold-pale)}
.site-header{background:var(--color-canvas);position:sticky;top:0;z-index:50;
border-bottom:1px solid transparent;transition:border-color .2s ease}
.site-header.scrolled{border-bottom-color:var(--color-hairline)}
.header-inner{display:flex;align-items:center;justify-content:space-between;height:72px}
.brand{font:300 26px/1 var(--font-serif);color:var(--color-ink);text-decoration:none;letter-spacing:.2px}
.brand em{font-style:italic;color:var(--color-clay)}
.site-nav{display:flex;align-items:center;gap:var(--space-5)}
.site-nav a.nav-link{font:400 14px/1.4 var(--font-sans);color:var(--color-stone);text-decoration:none}
.site-nav a.nav-link:hover,.site-nav a.nav-link[aria-current="page"]{color:var(--color-ink);text-decoration:underline;text-underline-offset:6px}
.nav-toggle{display:none;background:none;border:0;padding:10px;cursor:pointer}
.nav-toggle span{display:block;width:22px;height:2px;background:var(--color-ink);margin:5px 0;border-radius:2px}
@media(max-width:900px){
 .site-nav{position:absolute;top:72px;left:0;right:0;background:var(--color-canvas);
  border-bottom:1px solid var(--color-hairline);flex-direction:column;align-items:flex-start;
  padding:var(--space-5);gap:var(--space-4);display:none}
 .site-nav.open{display:flex}
 .nav-toggle{display:block}
}

/* ---------- hero ---------- */
.hero{padding:var(--space-8) 0 var(--space-9)}
.hero-grid{display:grid;grid-template-columns:1.05fr .95fr;gap:var(--space-8);align-items:center}
@media(max-width:900px){.hero-grid{grid-template-columns:1fr}}
.hero-art{background:var(--color-surface-grey);border-radius:var(--radius-xl);overflow:hidden}
.hero-art img{width:100%;height:100%;object-fit:cover;aspect-ratio:4/4.4}
.stat-row{display:flex;flex-wrap:wrap;gap:var(--space-3);margin-top:var(--space-6)}
.stat-pill{background:var(--color-canvas);border:1px solid var(--color-hairline);border-radius:var(--radius-full);
padding:10px 18px;font:400 14px/1.4 var(--font-sans);color:var(--color-stone)}

/* ---------- bands ---------- */
.band{padding:var(--space-9) 0}
.band-white{background:var(--color-surface)}
.band-grey{background:var(--color-surface-grey)}
.band-clay{background:var(--color-clay);color:var(--color-on-dark)}
.band-clay .h2,.band-clay .h3{color:var(--color-on-dark)}
.band-clay .lead{color:var(--color-gold-pale)}
.band-clay .eyebrow{color:var(--color-gold-pale)}
.band-sage{background:var(--color-sage-pale)}
.band-ink{background:var(--color-ink-band-soft);color:var(--color-on-dark)}
.band-ink .h2{color:var(--color-on-dark)}
.band-ink .lead{color:var(--color-mute)}
.band-ink .eyebrow{color:var(--color-mute)}

/* ---------- cards & grids ---------- */
.grid{display:grid;gap:var(--space-5)}
.g2{grid-template-columns:repeat(2,1fr)}
.g3{grid-template-columns:repeat(3,1fr)}
.g4{grid-template-columns:repeat(4,1fr)}
@media(max-width:1024px){.g4{grid-template-columns:repeat(2,1fr)}.g3{grid-template-columns:repeat(2,1fr)}}
@media(max-width:640px){.g2,.g3,.g4{grid-template-columns:1fr}}
.card{background:var(--color-surface);border:1px solid var(--color-hairline);border-radius:var(--radius-lg);padding:var(--space-5)}
.card-elevated{background:var(--color-canvas);border-radius:var(--radius-lg);padding:var(--space-5);box-shadow:var(--shadow-1)}
.card h3{font:400 20px/1.3 var(--font-sans);margin:0 0 var(--space-2)}
.card p{margin:0;color:var(--color-stone);font-size:16px}

/* product card */
.pcard{display:flex;flex-direction:column;text-decoration:none;color:var(--color-ink)}
.band-clay .pcard{color:var(--color-canvas)}
.band-clay .pcard-title{color:var(--color-canvas)}
.band-clay .pcard-kicker{color:var(--color-gold-pale)}
.band-clay .pcard-desc{color:var(--color-gold-pale)}
.band-clay .pcard-price{color:var(--color-canvas)}
.band-clay .pcard-art{background:var(--color-canvas)}
.pcard .pcard-art{background:var(--color-surface-grey);border-radius:var(--radius-xl);overflow:hidden;
aspect-ratio:1/1;display:flex;align-items:center;justify-content:center;position:relative}
.pcard .pcard-art img{width:100%;height:100%;object-fit:cover;transition:transform .35s ease}
.pcard:hover .pcard-art img{transform:scale(1.03)}
.pcard .pcard-art svg{width:78%;height:auto}
.pcard-body{padding:var(--space-4) var(--space-1) 0}
.pcard-kicker{font:700 12px/1.2 var(--font-sans);letter-spacing:1px;text-transform:uppercase;color:var(--color-ash);margin:0 0 6px}
.pcard-title{font:300 24px/1.2 var(--font-serif);margin:0 0 6px}
.pcard-desc{font-size:15px;color:var(--color-stone);margin:0 0 var(--space-2)}
.pcard-price{font:600 15px/1.3 var(--font-sans);color:var(--color-clay)}
.pcard .tag{position:absolute;top:16px;left:16px;background:var(--color-canvas);color:var(--color-clay);
border-radius:var(--radius-full);padding:6px 14px;font:700 12px/1 var(--font-sans);letter-spacing:.5px;text-transform:uppercase}
.price-note{font-size:14px;color:var(--color-ash)}

/* steps */
.steps{counter-reset:step;display:grid;gap:var(--space-5);grid-template-columns:repeat(5,1fr)}
@media(max-width:1024px){.steps{grid-template-columns:repeat(2,1fr)}}
@media(max-width:640px){.steps{grid-template-columns:1fr}}
.step{background:var(--color-surface);border:1px solid var(--color-hairline);border-radius:var(--radius-lg);padding:var(--space-5)}
.step-num{font:300 44px/1 var(--font-serif);color:var(--color-ochre);display:block;margin-bottom:var(--space-3)}
.step h3{font:600 16px/1.3 var(--font-sans);margin:0 0 6px}
.step p{margin:0;font-size:15px;color:var(--color-stone)}

/* checks list */
.checks{list-style:none;padding:0;margin:var(--space-4) 0 0}
.checks li{padding-left:28px;position:relative;margin-bottom:10px;color:var(--color-stone)}
.checks li::before{content:"";position:absolute;left:0;top:5px;width:16px;height:16px;border-radius:50%;
background:var(--color-sage-pale)}
.checks li::after{content:"";position:absolute;left:5px;top:9px;width:6px;height:3px;border-left:2px solid var(--color-forest);
border-bottom:2px solid var(--color-forest);transform:rotate(-45deg)}

/* big stats */
.stats{display:grid;grid-template-columns:repeat(3,1fr);gap:var(--space-5);text-align:center}
@media(max-width:640px){.stats{grid-template-columns:1fr}}
.stat-circle{width:150px;height:150px;border-radius:50%;background:var(--color-canvas);border:1px solid var(--color-hairline);
display:flex;flex-direction:column;align-items:center;justify-content:center;margin:0 auto var(--space-3)}
.stat-circle b{font:300 34px/1 var(--font-serif);color:var(--color-stone)}
.stat-circle span{font-size:12px;color:var(--color-ash);text-transform:uppercase;letter-spacing:1px;margin-top:6px}

/* table */
.table{width:100%;border-collapse:collapse;background:var(--color-surface);border:1px solid var(--color-hairline);
border-radius:var(--radius-lg);overflow:hidden;font-size:16px}
.table th{font:700 12px/1.4 var(--font-sans);letter-spacing:1px;text-transform:uppercase;color:var(--color-ash);
text-align:left;padding:14px var(--space-4);border-bottom:1px solid var(--color-hairline);background:var(--color-surface)}
.table td{padding:16px var(--space-4);border-bottom:1px solid var(--color-hairline);vertical-align:top}
.table tr:last-child td{border-bottom:0}
.table .t-price{font:600 16px var(--font-sans);color:var(--color-clay);white-space:nowrap}

/* forms */
.field{display:flex;flex-direction:column;gap:6px;margin-bottom:var(--space-4)}
.field label{font:600 14px/1.3 var(--font-sans);color:var(--color-stone)}
.field input,.field select,.field textarea{background:var(--color-surface);border:1px solid var(--color-hairline);
border-radius:var(--radius-md);padding:14px 16px;font:400 16px var(--font-sans);color:var(--color-ink)}
.field input:focus,.field select:focus,.field textarea:focus{outline:2px solid var(--color-stone);outline-offset:1px}
.form-grid{display:grid;grid-template-columns:1fr 1fr;gap:0 var(--space-4)}
@media(max-width:640px){.form-grid{grid-template-columns:1fr}}

/* faq */
.faq-item{background:var(--color-surface);border:1px solid var(--color-hairline);border-radius:var(--radius-lg);
padding:var(--space-4) var(--space-5);margin-bottom:var(--space-3)}
.faq-item h2,.faq-item h3{font:600 17px/1.4 var(--font-sans);margin:0 0 8px}
.faq-item p{margin:0;color:var(--color-stone);font-size:16px}

/* detail page */
.breadcrumb{font-size:13px;color:var(--color-ash);margin-bottom:var(--space-5)}
.breadcrumb a{color:var(--color-ash)}
.detail-grid{display:grid;grid-template-columns:1fr 1fr;gap:var(--space-8);align-items:start}
@media(max-width:900px){.detail-grid{grid-template-columns:1fr}}
.detail-art{background:var(--color-surface-grey);border-radius:var(--radius-xl);overflow:hidden;
display:flex;align-items:center;justify-content:center;aspect-ratio:1/1}
.detail-art img{width:100%;height:100%;object-fit:cover}
.detail-art svg{width:80%;height:auto}
.spec-list{width:100%;border-collapse:collapse;font-size:16px}
.spec-list th{font:700 12px/1.4 var(--font-sans);letter-spacing:1px;text-transform:uppercase;color:var(--color-ash);
text-align:left;width:38%;padding:12px 0;border-bottom:1px solid var(--color-hairline);vertical-align:top}
.spec-list td{padding:12px 0;border-bottom:1px solid var(--color-hairline);color:var(--color-stone);vertical-align:top}

/* quote band */
.quote-band{text-align:center;padding:var(--space-9) 0}
.quote-band .h2{max-width:760px;margin:0 auto var(--space-3)}

/* ---------- prose (reskinned guides / legal / faq) ---------- */
.prose{max-width:720px;margin:0 auto}
.prose h1{font:300 clamp(32px,4.4vw,52px)/1.12 var(--font-serif);margin-bottom:var(--space-3)}
.prose h2{font:300 clamp(24px,3vw,34px)/1.2 var(--font-serif);margin:var(--space-7) 0 var(--space-3)}
.prose h3{font:600 18px/1.4 var(--font-sans);margin:var(--space-5) 0 var(--space-2)}
.prose p{margin:0 0 var(--space-4);color:var(--color-stone)}
.prose a{text-decoration:underline;text-underline-offset:3px}
.prose ul,.prose ol{margin:0 0 var(--space-4);padding-left:22px;color:var(--color-stone)}
.prose li{margin-bottom:8px}
.prose blockquote{border-left:3px solid var(--color-ochre);margin:var(--space-5) 0;padding:4px 0 4px var(--space-4);
font-family:var(--font-serif);font-weight:300;font-size:20px;color:var(--color-ink)}
.prose table{width:100%;border-collapse:collapse;font-size:15px;margin:var(--space-4) 0}
.prose th,.prose td{border:1px solid var(--color-hairline);padding:10px 12px;text-align:left}
.prose img{border-radius:var(--radius-lg);margin:var(--space-4) 0}
.prose .updated{font-size:13px;color:var(--color-ash);text-transform:uppercase;letter-spacing:1px;margin-bottom:var(--space-5)}
.prose strong{color:var(--color-ink)}

/* ---------- footer ---------- */
.site-footer{background:var(--color-ink-band-soft);color:var(--color-on-dark);padding:var(--space-8) 0 var(--space-6);margin-top:var(--space-9)}
.footer-grid{display:grid;grid-template-columns:1.4fr 1fr 1fr 1fr;gap:var(--space-6)}
@media(max-width:900px){.footer-grid{grid-template-columns:1fr 1fr}}
@media(max-width:560px){.footer-grid{grid-template-columns:1fr}}
.footer-brand{font:300 28px/1 var(--font-serif);color:var(--color-on-dark)}
.footer-brand em{font-style:italic;color:var(--color-gold-pale)}
.site-footer p,.site-footer a{color:var(--color-mute);font-size:15px;text-decoration:none}
.site-footer a:hover{color:var(--color-on-dark)}
.site-footer h4{font:700 12px/1.4 var(--font-sans);letter-spacing:1px;text-transform:uppercase;color:var(--color-on-dark);margin:0 0 var(--space-4)}
.site-footer ul{list-style:none;margin:0;padding:0}
.site-footer li{margin-bottom:10px}
.footer-bottom{border-top:1px solid #2c2c30;margin-top:var(--space-7);padding-top:var(--space-5);
display:flex;flex-wrap:wrap;gap:var(--space-3);justify-content:space-between;color:var(--color-mute);font-size:13px}

/* util */
.mt-0{margin-top:0}.mb-0{margin-bottom:0}.mt-2{margin-top:8px}.mt-3{margin-top:12px}.mt-4{margin-top:16px}
.mt-5{margin-top:24px}.mt-6{margin-top:32px}.mt-7{margin-top:48px}.mt-8{margin-top:64px}
.split{display:grid;grid-template-columns:1fr 1fr;gap:var(--space-8);align-items:center}
.split-top{align-items:start}
@media(max-width:900px){.split{grid-template-columns:1fr}}
.round-img{border-radius:var(--radius-xl);overflow:hidden}
.round-img img{width:100%;height:100%;object-fit:cover;aspect-ratio:4/3}
.pill-tab{display:inline-block;border:1px solid var(--color-silver);border-radius:var(--radius-full);
padding:8px 18px;font:400 14px var(--font-sans);color:var(--color-stone);text-decoration:none;margin:0 8px 8px 0}
.pill-tab:hover{border-color:var(--color-stone)}
.notice{background:var(--color-canvas);border:1px solid var(--color-hairline);border-radius:var(--radius-md);
padding:var(--space-4);font-size:15px;color:var(--color-stone)}
"""

# ----------------------------------------------------------------------------
# 2. LINE-ART SVG PLACEHOLDERS for the 5 new memorial products (stone on grey)
# ----------------------------------------------------------------------------
def _paw(x=0, y=0, s=1.0):
    return (f'<g transform="translate({x},{y}) scale({s})" fill="#4a4741" stroke="none">'
            f'<ellipse cx="0" cy="10" rx="11" ry="9"/>'
            f'<circle cx="-12" cy="-2" r="5"/><circle cx="-4" cy="-8" r="5"/>'
            f'<circle cx="4" cy="-8" r="5"/><circle cx="12" cy="-2" r="5"/></g>')

SVGS = {
"wind_chime": f'''<svg viewBox="0 0 240 200" fill="none" stroke="#4a4741" stroke-width="3" stroke-linecap="round" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Custom pet memorial wind chime illustration">
<path d="M120 12c-10 0-16 6-16 12" />
<ellipse cx="120" cy="44" rx="52" ry="12"/>
<line x1="80" y1="52" x2="80" y2="120"/><rect x="74" y="120" width="12" height="46" rx="6"/>
<line x1="100" y1="55" x2="100" y2="108"/><rect x="94" y="108" width="12" height="52" rx="6"/>
<line x1="140" y1="55" x2="140" y2="108"/><rect x="134" y="108" width="12" height="52" rx="6"/>
<line x1="160" y1="52" x2="160" y2="120"/><rect x="154" y="120" width="12" height="46" rx="6"/>
<line x1="120" y1="56" x2="120" y2="86"/>
<circle cx="120" cy="118" r="32" fill="#f7f1e8"/>
{_paw(120,114)}
</svg>''',

"suncatcher": f'''<svg viewBox="0 0 240 200" fill="none" stroke="#4a4741" stroke-width="3" stroke-linecap="round" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Custom pet window suncatcher illustration">
<rect x="34" y="22" width="120" height="156" rx="6"/>
<line x1="94" y1="22" x2="94" y2="178"/><line x1="34" y1="100" x2="154" y2="100"/>
<line x1="176" y1="30" x2="176" y2="66"/>
<circle cx="176" cy="92" r="30" fill="#f7f1e8"/>
<line x1="176" y1="62" x2="176" y2="66"/>
{_paw(176,88)}
<path d="M158 130c8 8 30 8 36 0" stroke-linejoin="round"/>
<path d="M166 138l4 10M186 138l-4 10"/>
</svg>''',

"plaque": f'''<svg viewBox="0 0 240 200" fill="none" stroke="#4a4741" stroke-width="3" stroke-linecap="round" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Custom pet memorial plaque illustration">
<path d="M60 178c10-18 30-26 60-26s50 8 60 26" stroke-width="2"/>
<rect x="52" y="52" width="136" height="92" rx="14" fill="#f7f1e8"/>
{_paw(120,78)}
<line x1="84" y1="108" x2="156" y2="108"/>
<line x1="98" y1="122" x2="142" y2="122"/>
</svg>''',

"urn": f'''<svg viewBox="0 0 240 200" fill="none" stroke="#4a4741" stroke-width="3" stroke-linecap="round" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Custom pet urn illustration">
<circle cx="120" cy="22" r="7"/>
<path d="M92 40h56"/>
<path d="M96 40c-2 14-14 22-14 44 0 30 17 46 38 46s38-16 38-46c0-22-12-30-14-44" fill="#f7f1e8" stroke-linejoin="round"/>
<path d="M84 130h72"/>
<path d="M90 130l-8 24h76l-8-24" stroke-linejoin="round"/>
{_paw(120,92)}
</svg>''',

"remembrance_set": f'''<svg viewBox="0 0 240 200" fill="none" stroke="#4a4741" stroke-width="3" stroke-linecap="round" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Pet farewell and remembrance set illustration">
<rect x="46" y="96" width="26" height="66" rx="8" fill="#f7f1e8"/>
<line x1="59" y1="96" x2="59" y2="84"/>
<path d="M59 66c8 10 8 16 0 20-8-4-8-10 0-20z" fill="#ddbe78" stroke="#684d07" stroke-width="2"/>
<rect x="92" y="78" width="72" height="84" rx="8" fill="#f7f1e8" transform="rotate(-4 128 120)"/>
<path d="M128 138c-12-10-18-18-10-26 6-6 12-2 12 4 0-6 8-9 12-4 7 8 0 16-14 26z" fill="none" stroke="#6b443d" stroke-width="2.5" transform="rotate(-4 128 120)"/>
<path d="M176 162c2-22 8-34 22-34s20 12 22 34z" fill="#f7f1e8"/>
<line x1="190" y1="128" x2="206" y2="128"/>
<line x1="176" y1="162" x2="220" y2="162"/>
</svg>''',
}

# ----------------------------------------------------------------------------
# 3. DATA
# ----------------------------------------------------------------------------
FELT = [
 dict(img="/images/product-1.webp", kicker="Mini Portrait", name="Custom Needle-Felted Pet Mini",
      desc="A small handmade wool felt pet portrait, perfect as a personal keepsake or gift.",
      incl="Pocket-size wool felt portrait, made from your pet photos", price="$87"),
 dict(img="/images/product-2.webp", kicker="Headshot Frame", name="Custom Felted Pet Headshot in Frame",
      desc="A framed handmade felted headshot designed to preserve your pet's unique appearance.",
      incl="Felted headshot, wooden frame, protective packaging", price="$197"),
 dict(img="/images/product-3.webp", kicker="Half-Body Frame", name="Custom Needle-Felted Half-Body Portrait",
      desc="A detailed half-body needle-felted portrait in frame with customized features.",
      incl="Half-body portrait in frame, pose & expression customization", price="$297"),
 dict(img="/images/product-4.webp", kicker="Full-Body Portrait", name="Custom Needle-Felted Pet Replica",
      desc="A premium full-body handmade replica capturing your pet's appearance and personality.",
      incl="Full-body replica, coat pattern matching, size-dependent pricing", price="From $477"),
 dict(img="/images/product-5.webp", kicker="Leather Sculpted Portrait", name="Hand-Carved & Hand-Painted Leather Portrait",
      desc="A miniature pet portrait carved and painted by hand on genuine leather — durable, detailed and one of a kind.",
      incl="Hand-carved leather portrait, keychain or display option", price="$112"),
]

# price=None → "Price on request" until the owner supplies the final numbers (single edit here).
NEW = [
 dict(slug="custom-pet-wind-chime", price=None, art="wind_chime", kicker="Memorial Collection",
      name="Custom Pet Memorial Wind Chime",
      desc="A gentle wind chime personalized with your pet's portrait and name — a soft reminder every time the breeze passes.",
      short="Personalized chime with your pet's photo charm, engraved name and dates",
      long=("Some pets are felt in sound as much as in sight. Our custom memorial wind chime carries a hand-finished charm "
            "with your pet's portrait, their name and their dates, hung above a set of warm, low-toned chime tubes. "
            "Hang it on a porch, by a window, or near a favourite resting spot in the garden — every breeze becomes a quiet hello."),
      incl=["Photo charm customized from your pet's picture", "Engraved name and dates", "Weather-resistant coated tubes", "Ready to hang — no assembly"],
      spec=[("Material","Hardwood crown, coated aluminium tubes, printed photo charm"),
            ("Size","Approx. 45–60 cm total hang length"),
            ("Personalization","Pet photo, name, dates, short message (optional)"),
            ("Lead time","7–12 days production before shipping"),
            ("Shipping","Worldwide, tracked")],
      faq=[("Can the wind chime stay outdoors?","Yes. The tubes and crown are coated for outdoor use. As with any keepsake, a sheltered spot will keep the photo charm vivid for longer."),
           ("What photo works best?","A clear, well-lit photo where your pet's face fills the frame works best. We confirm the crop with you before production."),
           ("Can I choose the message on the charm?","Yes — most owners choose the pet's name and dates, but a short line such as “Best friend, always” fits beautifully.")] ),
 dict(slug="custom-pet-window-suncatcher", price=None, art="suncatcher", kicker="Memorial Collection",
      name="Custom Pet Portrait Window Suncatcher",
      desc="A light-catching window ornament made with your pet's portrait — their silhouette glows in the morning sun.",
      short="Photo suncatcher for windows, personalized with your pet's portrait",
      long=("Turn the light your pet loved to nap in into a small daily memorial. Our custom window suncatcher holds your pet's "
            "portrait in a light-catching pendant that glows when the sun passes through. It hangs from a fine chain with a "
            "suction hook, ready for any window, mirror or sunny corner."),
      incl=["Portrait pendant customized from your pet's photo", "Suction hook and hanging chain included", "Engraved name or short message (optional)", "Gift-ready packaging"],
      spec=[("Material","Light-catching acrylic or glass-style pendant, metal chain"),
            ("Size","Pendant approx. 8–12 cm diameter"),
            ("Personalization","Pet photo, name or short message"),
            ("Lead time","7–12 days production before shipping"),
            ("Shipping","Worldwide, tracked")],
      faq=[("Where should I hang it?","Any window that gets direct or strong indirect light. The portrait reads best against a bright background."),
           ("Is it heavy?","No — the pendant is lightweight acrylic or glass-style material, safe for standard suction hooks."),
           ("Can I order two with different pets?","Yes, and many customers do. Send both photos and we will match the style so they hang well together.")] ),
 dict(slug="custom-pet-memorial-plaque", price=None, art="plaque", kicker="Memorial Collection",
      name="Custom Pet Memorial Plaque & Grave Marker",
      desc="An engraved memorial plaque for a garden, grave or special place — weatherproof, dignified, made to last.",
      short="Engraved grave marker or garden plaque with name, dates and a paw emblem",
      long=("A place to visit, a mark that stays. Our custom memorial plaque is engraved with your pet's name, their dates and a "
            "paw emblem, finished to withstand the weather where they loved to be — the garden, the graveside, or beneath a "
            "favourite tree. Choose a stake for lawns and gardens, or a flat version for shelves and memorial walls."),
      incl=["Engraved plaque with name, dates and paw emblem", "Garden stake or flat display option", "All-weather protective finish", "Optional short memorial line"],
      spec=[("Material","Cast stone or hardwood composite with weatherproof finish"),
            ("Size","Approx. 20 × 14 cm (custom sizes on request)"),
            ("Personalization","Name, dates, short memorial line, paw emblem"),
            ("Lead time","7–14 days production before shipping"),
            ("Shipping","Worldwide, tracked")],
      faq=[("Will it survive rain and frost?","Yes. The plaque and engraving are finished for outdoor year-round use; colours are UV-stable."),
           ("Stake or flat — which should I choose?","The stake suits lawns, gardens and graveside soil. The flat version suits urn shelves, memorial walls and indoor display."),
           ("How much text fits?","Comfortably a name, two dates and one short line (about 30 characters). We confirm the layout before engraving.")] ),
 dict(slug="custom-pet-urn", price=None, art="urn", kicker="Memorial Collection",
      name="Custom Wooden Pet Urn",
      desc="A calm, beautifully made wooden urn with your pet's name and portrait — a dignified place to keep them close.",
      short="Handmade wooden urn with engraved name, dates and photo plaque",
      long=("A resting place that feels like furniture, not loss. Our custom wooden urn is made from warm hardwood with a soft "
            "matte finish, engraved with your pet's name and dates and finished with a portrait plaque made from your photo. "
            "Available in three sizes sized to your pet, with a secure threaded or magnetic closure."),
      incl=["Hardwood urn with soft matte finish", "Engraved name and dates", "Portrait plaque from your pet's photo", "Felt base to protect furniture"],
      spec=[("Material","Solid hardwood, matte protective finish"),
            ("Sizes","Small (pets up to 10 kg) · Medium (up to 25 kg) · Large (up to 45 kg)"),
            ("Personalization","Name, dates, portrait plaque, short line"),
            ("Lead time","10–15 days production before shipping"),
            ("Shipping","Worldwide, tracked")],
      faq=[("How do I choose the size?","As a rule of thumb, one cubic inch of interior space per pound of body weight. Tell us your pet's weight and we will recommend the right size."),
           ("Can it hold a collar or toy inside?","Yes — many families place a collar, tag or small toy inside alongside the ashes."),
           ("Is the closure secure?","Yes. Each urn closes with a threaded or magnetic panel sealed from underneath, and sits on a felt base.")] ),
 dict(slug="pet-farewell-remembrance-set", price=None, art="remembrance_set", kicker="Memorial Collection",
      name="Pet Farewell & Remembrance Set",
      desc="A gentle set for saying goodbye: memorial candle, remembrance card, scatter pouch and keepsake token.",
      short="Ceremony set — memorial candle, remembrance card, scatter pouch and token",
      long=("For the days when words are hard. The Farewell & Remembrance Set gathers the small rituals that help: a hand-poured "
            "memorial candle, a printed remembrance card with your pet's photo, a linen scatter pouch for a favourite spot, and a "
            "small keepsake token to keep in a pocket or a drawer. Together they make space for a calm, personal goodbye."),
      incl=["Hand-poured memorial candle", "Remembrance card printed with your pet's photo", "Linen scatter pouch", "Keepsake token with paw emblem", "Keepsake box to hold it all"],
      spec=[("Material","Soy candle, cotton linen pouch, letterpress card, brass token"),
            ("Personalization","Pet photo and name on the remembrance card"),
            ("Lead time","5–10 days production before shipping"),
            ("Shipping","Worldwide, tracked")],
      faq=[("Is this suitable as a sympathy gift?","Very much so — it is one of our most-gifted sets. We can ship directly to the recipient with a handwritten note."),
           ("Can I order the set without the candle?","Yes, tell us in your inquiry and we will adjust the quote."),
           ("How long does the candle burn?","Approximately 20–25 hours, sized for several evenings of remembrance.")] ),
]

ALL_PRODUCTS = FELT + NEW

# ----------------------------------------------------------------------------
# 4. SHELL
# ----------------------------------------------------------------------------
NAV = [
    ("/", "Home"), ("/products/", "Products"), ("/pricing/", "Pricing"),
    ("/process/", "Process"), ("/guides/", "Guides"), ("/about/", "About"), ("/contact/", "Contact"),
]

def shell(*, title, desc, canonical, active=None, body, extra_head="", og_image="/images/hero.webp", og_type="website"):
    nav_html = "".join(
        f'<a class="nav-link" href="{href}"{" aria-current=\"page\"" if href == active else ""}>{label}</a>'
        for href, label in NAV)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>{html.escape(title)}</title>
<link rel="icon" type="image/svg+xml" href="/favicon.svg"/>
<meta name="description" content="{html.escape(desc)}"/>
<meta name="robots" content="index, follow"/>
<link rel="canonical" href="{canonical}"/>
<meta property="og:type" content="{og_type}"/>
<meta property="og:site_name" content="Again Paws"/>
<meta property="og:url" content="{canonical}"/>
<meta property="og:title" content="{html.escape(title)}"/>
<meta property="og:description" content="{html.escape(desc)}"/>
<meta property="og:image" content="{SITE}{og_image}"/>
<meta name="twitter:card" content="summary_large_image"/>
<meta name="twitter:title" content="{html.escape(title)}"/>
<meta name="twitter:description" content="{html.escape(desc)}"/>
<meta name="twitter:image" content="{SITE}{og_image}"/>
<meta name="theme-color" content="#f7f1e8"/>
<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,300;9..144,400&family=Inter:wght@400;500;600;700&display=swap"/>
<link rel="stylesheet" href="/assets/site-v2.css"/>
{extra_head}
<script src="/analytics.js" defer></script>
</head>
<body>
<div class="announce band-clay">Handmade · Made to Order · Worldwide Delivery</div>
<header class="site-header" id="siteHeader">
  <div class="wrap header-inner">
    <a class="brand" href="/">Again <em>Paws</em></a>
    <button class="nav-toggle" id="navToggle" aria-label="Open menu" aria-expanded="false"><span></span><span></span><span></span></button>
    <nav class="site-nav" id="siteNav" aria-label="Main navigation">
      {nav_html}
      <a class="btn btn-primary btn-sm" href="/contact/">Request a Quote</a>
    </nav>
  </div>
</header>
{body}
<footer class="site-footer">
  <div class="wrap">
    <div class="footer-grid">
      <div>
        <div class="footer-brand">Again <em>Paws</em></div>
        <p class="mt-4">Handmade pet keepsakes and memorials, crafted from your photos and shipped worldwide.</p>
        <p class="mt-3"><a href="https://www.tiktok.com/@againpaws">TikTok · @againpaws</a></p>
      </div>
      <div>
        <h4>Collections</h4>
        <ul>
          <li><a href="/products/#felted">Felted Portraits</a></li>
          <li><a href="/products/#memorial">Memorial Collection</a></li>
          <li><a href="/pricing/">Pricing</a></li>
          <li><a href="/customization/">Customization</a></li>
        </ul>
      </div>
      <div>
        <h4>Company</h4>
        <ul>
          <li><a href="/about/">About</a></li>
          <li><a href="/process/">Our Process</a></li>
          <li><a href="/guides/">Guides</a></li>
          <li><a href="/faq/">FAQ</a></li>
        </ul>
      </div>
      <div>
        <h4>Get in touch</h4>
        <ul>
          <li><a href="mailto:q8461994@gmail.com">q8461994@gmail.com</a></li>
          <li><a href="https://wa.me/8613064191721">WhatsApp · +86 130 6419 1721</a></li>
          <li>Worldwide shipping</li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <span>© 2026 Again Paws. Handmade with love.</span>
      <span><a href="/privacy/">Privacy</a> · <a href="/terms/">Terms</a> · <a href="/refund-policy/">Refund Policy</a></span>
    </div>
  </div>
</footer>
<script>
(function(){{
  var t=document.getElementById('navToggle'),n=document.getElementById('siteNav');
  if(t&&n){{t.addEventListener('click',function(){{var o=n.classList.toggle('open');t.setAttribute('aria-expanded',o?'true':'false');}});}}
  var h=document.getElementById('siteHeader');
  if(h){{window.addEventListener('scroll',function(){{h.classList.toggle('scrolled',window.scrollY>8);}},{{passive:true}});}}
}})();
</script>
</body>
</html>
"""

def page(path, s):
    p = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        f.write(s)
    print("wrote", path, len(s))

def price_html(price):
    return price if price else "Price on request"

# ----------------------------------------------------------------------------
# 5. SHARED PARTIALS
# ----------------------------------------------------------------------------
def felt_card(p, link="/contact/"):
    return f"""<a class="pcard" href="{link}">
  <div class="pcard-art"><img src="{p['img']}" alt="{html.escape(p['name'])}" loading="lazy"/></div>
  <div class="pcard-body">
    <p class="pcard-kicker">{html.escape(p['kicker'])}</p>
    <h3 class="pcard-title">{html.escape(p['name'])}</h3>
    <p class="pcard-desc">{html.escape(p['desc'])}</p>
    <p class="pcard-price">Reference price · {p['price']}</p>
  </div>
</a>"""

def new_card(p, tag=None):
    tag_html = f'<span class="tag">{tag}</span>' if tag else ""
    return f"""<a class="pcard" href="/{p['slug']}/">
  <div class="pcard-art">{tag_html}{SVGS[p['art']]}</div>
  <div class="pcard-body">
    <p class="pcard-kicker">{html.escape(p['kicker'])}</p>
    <h3 class="pcard-title">{html.escape(p['name'])}</h3>
    <p class="pcard-desc">{html.escape(p['short'])}</p>
    <p class="pcard-price">{price_html(p['price'])}</p>
  </div>
</a>"""

CTA_BAND = """<section class="band band-ink">
  <div class="wrap quote-band">
    <p class="eyebrow on-dark">Ready When You Are</p>
    <h2 class="h2">Ready To Create Your Pet's Keepsake?</h2>
    <p class="lead mb-0">Send a photo and we will craft a quote made for your pet.</p>
    <div class="btn-row" style="justify-content:center">
      <a class="btn btn-primary" href="/contact/">Get Custom Quote</a>
      <a class="btn btn-outline-dark" href="https://wa.me/8613064191721">Chat With Us</a>
    </div>
  </div>
</section>"""

STEPS = [
    ("Send Pet Photos", "Share a few clear photos of your pet — front, side and close-up of the face."),
    ("Confirm Design Details", "We agree on size, pose, colours, expression and the frame or base you prefer."),
    ("Handmade Crafting", "Our artisans shape wool, wood and print fibre by fibre until the likeness appears."),
    ("Quality Check", "Every detail is reviewed against your photos before the piece is approved."),
    ("Delivery Worldwide", "Carefully packed and shipped to your door with tracked delivery."),
]

def steps_html():
    rows = "".join(
        f'<div class="step"><span class="step-num">{i+1}</span><h3>{t}</h3><p>{d}</p></div>'
        for i, (t, d) in enumerate(STEPS))
    return f'<div class="steps">{rows}</div>'

# ----------------------------------------------------------------------------
# 6. PAGES
# ----------------------------------------------------------------------------
def build_home():
    featured = "".join(felt_card(p) for p in FELT[:4])
    memorial_cards = "".join(new_card(p, tag="New") for p in NEW)
    body = f"""
<main>
<section class="hero">
  <div class="wrap hero-grid">
    <div>
      <p class="eyebrow">Handmade Pet Memorials &amp; Keepsakes</p>
      <h1 class="display">Turn your beloved pet into a timeless handmade keepsake.</h1>
      <p class="lead mt-5">Handcrafted felted portraits and personalized memorial pieces, created from your pet's photo — made by hand, kept forever.</p>
      <div class="btn-row">
        <a class="btn btn-primary" href="/contact/">Request a Custom Quote</a>
        <a class="btn btn-outline-stone" href="/products/">Browse the Collection</a>
      </div>
      <div class="stat-row">
        <span class="stat-pill">100% handmade</span>
        <span class="stat-pill">Made from your photos</span>
        <span class="stat-pill">Shipped worldwide</span>
      </div>
    </div>
    <div class="hero-art"><img src="/images/hero.webp" alt="Handmade needle-felted pet portrait held beside the reference photo" fetchpriority="high" width="720" height="790"/></div>
  </div>
</section>

<section class="section band-white">
  <div class="wrap">
    <p class="eyebrow">Two Ways To Remember</p>
    <h2 class="h2" style="max-width:720px">A collection shaped by hand, for the pets who never leave us.</h2>
    <div class="grid g2 mt-7">
      <a class="card" href="/products/#felted" style="text-decoration:none">
        <div class="round-img"><img src="/images/product-3.webp" alt="Needle-felted pet portrait in frame" loading="lazy"/></div>
        <h3 class="mt-4" style="font:300 30px/1.2 var(--font-serif)">Felted Portraits</h3>
        <p>Needle-felted minis, framed headshots, half-body and full-body replicas — and hand-carved leather portraits. From $87.</p>
      </a>
      <a class="card" href="/products/#memorial" style="text-decoration:none">
        <div class="round-img" style="background:var(--color-surface-grey);display:flex;align-items:center;justify-content:center">{SVGS['urn']}</div>
        <h3 class="mt-4" style="font:300 30px/1.2 var(--font-serif)">The Memorial Collection <span class="pcard-price">· New</span></h3>
        <p>Wind chimes, window suncatchers, memorial plaques, wooden urns and farewell sets — gentle ways to keep them close.</p>
      </a>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <p class="eyebrow">Signature Collection</p>
    <h2 class="h2">Handmade pieces, made for your pet.</h2>
    <p class="lead" style="max-width:640px">Each creation begins with your pet's photo and ends as a one-of-a-kind keepsake.</p>
    <div class="grid g4 mt-7">{featured}</div>
    <p class="mt-6"><a class="btn btn-stone" href="/products/">View All Keepsakes</a></p>
  </div>
</section>

<section class="band band-clay" id="memorial">
  <div class="wrap">
    <p class="eyebrow">The Memorial Collection · New</p>
    <h2 class="h2">Gentle ways to say, and keep saying, goodbye.</h2>
    <p class="lead" style="max-width:680px">Five new handmade-to-order memorials — from a wind chime for the porch to a place to keep them close. Personalized from your photos.</p>
    <div class="grid g3 mt-7">{memorial_cards}</div>
  </div>
</section>

<section class="section band-sage">
  <div class="wrap split">
    <div>
      <p class="eyebrow">Why It Matters</p>
      <h2 class="h2">Your pet is more than a pet.</h2>
      <p class="lead">Many owners want to preserve the memory of a beloved companion. Photos stay on your phone — a handmade keepsake brings those memories into the real world.</p>
      <div class="btn-row"><a class="btn btn-stone" href="/about/">Learn More About Us</a></div>
    </div>
    <div class="stats">
      <div><div class="stat-circle"><b>100%</b><span>handmade</span></div></div>
      <div><div class="stat-circle"><b>1:1</b><span>photo likeness</span></div></div>
      <div><div class="stat-circle"><b>24h</b><span>quote reply</span></div></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <p class="eyebrow">How It Works</p>
    <h2 class="h2">From photo to finished keepsake.</h2>
    <p class="lead" style="max-width:640px">Five simple steps turn a favourite photo into a handmade treasure.</p>
    <div class="mt-7">{steps_html()}</div>
    <p class="mt-6"><a class="btn btn-outline-stone" href="/process/">See The Full Process</a></p>
  </div>
</section>

<section class="band band-grey">
  <div class="wrap split">
    <div class="round-img"><img src="/images/about-1.webp" alt="Artisan hand-felting a pet portrait" loading="lazy"/></div>
    <div>
      <p class="eyebrow">Partner With Again Paws</p>
      <h2 class="h2">Bring handmade pet keepsakes to your brand.</h2>
      <p class="lead">We work with pet shops, gift stores and pet brands on wholesale customization and private-label cooperation.</p>
      <ul class="checks">
        <li>Pet shops &amp; gift stores</li>
        <li>Wholesale &amp; private label</li>
        <li>Tailored pricing for your customers</li>
      </ul>
      <div class="btn-row"><a class="btn btn-stone" href="/contact/">Business Inquiry</a></div>
    </div>
  </div>
</section>
{CTA_BAND}
</main>"""
    page("index.html", shell(
        title="Custom Pet Keepsakes & Memorials Made From Photos | Again Paws",
        desc="Handmade needle-felted pet replicas and personalized pet memorials — wind chimes, suncatchers, plaques, urns and farewell sets — crafted from your photos. Request a quote today.",
        canonical=f"{SITE}/", active="/", body=body,
        extra_head="""<script type="application/ld+json">{
  "@context":"https://schema.org","@graph":[
    {"@type":"WebSite","@id":"https://againpaws.vip/#website","url":"https://againpaws.vip/","name":"Again Paws","inLanguage":"en-US","publisher":{"@id":"https://againpaws.vip/#organization"}},
    {"@type":"Organization","@id":"https://againpaws.vip/#organization","name":"Again Paws","url":"https://againpaws.vip/","logo":"https://againpaws.vip/favicon.svg","email":"q8461994@gmail.com",
     "contactPoint":{"@type":"ContactPoint","telephone":"+86-130-6419-1721","contactType":"customer service","availableLanguage":"English","areaServed":"US"},"sameAs":["https://www.tiktok.com/@againpaws"]},
    {"@type":"WebPage","@id":"https://againpaws.vip/#webpage","url":"https://againpaws.vip/","name":"Custom Pet Keepsakes & Memorials Made From Photos","isPartOf":{"@id":"https://againpaws.vip/#website"},"inLanguage":"en-US"}
  ]}</script>"""))

def build_products():
    felt = "".join(felt_card(p) for p in FELT)
    memorial = "".join(new_card(p) for p in NEW)
    body = f"""
<main>
<section class="section-tight">
  <div class="wrap">
    <p class="eyebrow">Signature Keepsakes</p>
    <h1 class="h1">A handmade tribute to your pet.</h1>
    <p class="lead" style="max-width:680px">Choose a style below. Every piece is customized from your pet's photos and made to order. Reference prices — final quotation depends on pet size, design complexity and custom requirements.</p>
  </div>
</section>

<section class="section-tight" id="felted">
  <div class="wrap">
    <h2 class="h2">Felted Portraits</h2>
    <div class="grid g3 mt-6">{felt}</div>
  </div>
</section>

<section class="band band-clay" id="memorial">
  <div class="wrap">
    <p class="eyebrow">The Memorial Collection · New</p>
    <h2 class="h2">Memorial &amp; remembrance pieces.</h2>
    <div class="grid g3 mt-6">{memorial}</div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <p class="eyebrow">How Your Quote Is Calculated</p>
    <h2 class="h2">What shapes the final price.</h2>
    <div class="grid g4 mt-6">
      <div class="card"><h3>01 · Pet size</h3><p>Larger breeds and full-body pieces need more material and time.</p></div>
      <div class="card"><h3>02 · Design complexity</h3><p>Coat patterns, markings and special poses add handwork hours.</p></div>
      <div class="card"><h3>03 · Custom requirements</h3><p>Frames, engraving, accessories and display bases.</p></div>
      <div class="card"><h3>04 · Quantity</h3><p>Wholesale and bulk orders receive tailored pricing.</p></div>
    </div>
  </div>
</section>
{CTA_BAND}
</main>"""
    page("products/index.html", shell(
        title="Custom Pet Keepsakes & Memorial Products | Again Paws",
        desc="Browse handmade felted pet portraits ($87–$477) and the new Memorial Collection: custom wind chimes, window suncatchers, plaques, urns and farewell sets — all made from your photos.",
        canonical=f"{SITE}/products/", active="/products/", body=body,
        extra_head=_products_schema()))

def _products_schema():
    items = []
    for i, p in enumerate(ALL_PRODUCTS, 1):
        d = {"@type": "Product", "position": i, "name": p["name"], "description": p["desc"],
             "brand": {"@type": "Brand", "name": "Again Paws"},
             "url": f"{SITE}/{p['slug']}/" if p.get("slug") else f"{SITE}/products/"}
        if p.get("img"):
            d["image"] = SITE + p["img"]
        items.append(d)
    return ('<script type="application/ld+json">'
            + json.dumps({"@context": "https://schema.org", "@type": "ItemList",
                          "name": "Again Paws Keepsake Collection", "itemListElement": items}, ensure_ascii=False)
            + '</script>')

def build_product_page(p):
    faq_json = json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in p["faq"]]}, ensure_ascii=False)
    incl = "".join(f"<li>{x}</li>" for x in p["incl"])
    spec = "".join(f"<tr><th>{k}</th><td>{v}</td></tr>" for k, v in p["spec"])
    faq_html = "".join(f'<div class="faq-item"><h3>{q}</h3><p>{a}</p></div>' for q, a in p["faq"])
    related = "".join(new_card(r) for r in NEW if r["slug"] != p["slug"])
    prod_json = json.dumps({"@context": "https://schema.org", "@type": "Product",
        "name": p["name"], "description": p["desc"], "brand": {"@type": "Brand", "name": "Again Paws"},
        "material": p["spec"][0][1], "url": f"{SITE}/{p['slug']}/"}, ensure_ascii=False)
    price_line = (f'<p class="pcard-price" style="font-size:20px">Reference price · {p["price"]}</p>'
                  if p["price"] else '<p class="pcard-price" style="font-size:20px">Price on request — personalized quote for every order.</p>')
    body = f"""
<main>
<section class="section-tight">
  <div class="wrap">
    <p class="breadcrumb"><a href="/">Home</a> · <a href="/products/">Products</a> · {html.escape(p['name'])}</p>
    <div class="detail-grid">
      <div class="detail-art">{SVGS[p['art']]}</div>
      <div>
        <p class="eyebrow">{html.escape(p['kicker'])}</p>
        <h1 class="h1">{html.escape(p['name'])}</h1>
        <p class="lead">{html.escape(p['short'])}</p>
        {price_line}
        <div class="btn-row">
          <a class="btn btn-primary" href="/contact/">Request a Quote</a>
          <a class="btn btn-outline-stone" href="https://wa.me/8613064191721">Chat With Us</a>
        </div>
        <ul class="checks">{incl}</ul>
      </div>
    </div>
  </div>
</section>

<section class="band band-white">
  <div class="wrap split">
    <div>
      <p class="eyebrow">About This Piece</p>
      <h2 class="h2">Made from your photos, one at a time.</h2>
      <p>{html.escape(p['long'])}</p>
      <p class="muted">Every order starts with a conversation: send your photos, tell us about your pet, and we confirm every detail — size, personalization and finish — before production begins.</p>
      <div class="btn-row"><a class="btn btn-stone" href="/customization/">How Customization Works</a></div>
    </div>
    <div class="card">
      <h3 style="font:300 28px/1.2 var(--font-serif)">Specifications</h3>
      <table class="spec-list mt-4">{spec}</table>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap measure-c">
    <p class="eyebrow center">Good To Know</p>
    <h2 class="h2 center">Common questions.</h2>
    <div class="mt-6">{faq_html}</div>
  </div>
</section>

<section class="band band-grey">
  <div class="wrap">
    <p class="eyebrow">More From The Memorial Collection</p>
    <h2 class="h2">You may also like.</h2>
    <div class="grid g4 mt-6">{related}</div>
  </div>
</section>
{CTA_BAND}
</main>"""
    page(f"{p['slug']}/index.html", shell(
        title=f"{p['name']} Made From Photos | Again Paws",
        desc=p["short"], canonical=f"{SITE}/{p['slug']}/", active="/products/",
        body=body, extra_head=f'<script type="application/ld+json">{prod_json}</script>'
                              f'<script type="application/ld+json">{faq_json}</script>'))

def build_pricing():
    rows = "".join(
        f'<tr><td><strong>{p["kicker"]}</strong><br/><span class="muted small">{html.escape(p["name"])}</span></td>'
        f'<td class="t-price">{p["price"]}</td><td>{html.escape(p["incl"])}</td></tr>' for p in FELT)
    mrows = "".join(
        f'<tr><td><strong>{html.escape(p["name"])}</strong></td>'
        f'<td class="t-price">{price_html(p["price"])}</td><td>{html.escape(p["short"])}</td></tr>' for p in NEW)
    body = f"""
<main>
<section class="section-tight">
  <div class="wrap">
    <p class="eyebrow">Pricing</p>
    <h1 class="h1">Custom pet keepsake pricing.</h1>
    <p class="lead" style="max-width:680px">Each piece is handmade and customized. Contact us for your personalized quote.</p>
  </div>
</section>
<section class="section-tight">
  <div class="wrap">
    <h2 class="h2">Felted Portraits</h2>
    <div class="mt-5" style="overflow-x:auto"><table class="table">
      <thead><tr><th>Keepsake</th><th>Starting from</th><th>What's included</th></tr></thead>
      <tbody>{rows}</tbody></table></div>
  </div>
</section>
<section class="section-tight">
  <div class="wrap">
    <h2 class="h2">The Memorial Collection</h2>
    <div class="mt-5" style="overflow-x:auto"><table class="table">
      <thead><tr><th>Memorial piece</th><th>Price</th><th>What's included</th></tr></thead>
      <tbody>{mrows}</tbody></table></div>
    <p class="price-note mt-4">Memorial pieces are quoted individually — send us your pet's photo and personalization request and we reply within 24 hours.</p>
  </div>
</section>
<section class="section band-grey">
  <div class="wrap split">
    <div>
      <p class="eyebrow">Every Order Includes</p>
      <ul class="checks">
        <li>Design review of your pet photos</li>
        <li>Progress check-in before finishing</li>
        <li>Secure, gift-ready packaging</li>
        <li>Worldwide tracked delivery</li>
      </ul>
    </div>
    <div>
      <p class="eyebrow">Want A Price For Your Pet?</p>
      <h2 class="h2">Tell us the breed, size and style.</h2>
      <p class="lead">We will prepare a tailored quote within 24 hours.</p>
      <div class="btn-row">
        <a class="btn btn-primary" href="/contact/">Get Custom Quote</a>
        <a class="btn btn-outline-stone" href="https://wa.me/8613064191721">Chat With Us</a>
      </div>
    </div>
  </div>
</section>
</main>"""
    page("pricing/index.html", shell(
        title="Custom Pet Keepsake & Memorial Pricing | Again Paws",
        desc="Reference pricing for handmade felted pet portraits ($87–$477) and the Memorial Collection: wind chimes, suncatchers, plaques, urns and farewell sets. Personalized quotes within 24 hours.",
        canonical=f"{SITE}/pricing/", active="/pricing/", body=body))

def build_about():
    body = f"""
<main>
<section class="section-tight">
  <div class="wrap">
    <p class="eyebrow">About Again Paws</p>
    <h1 class="h1">The hands &amp; heart behind every keepsake.</h1>
    <p class="lead" style="max-width:680px">We believe a pet is family — and that love deserves more than a photo left on a phone. A handmade keepsake brings their memory into the real world, where you can see it and hold it.</p>
  </div>
</section>
<section class="band band-white">
  <div class="wrap split">
    <div class="round-img"><img src="/images/about-1.webp" alt="Artisan hand-felting a pet portrait" loading="lazy"/></div>
    <div>
      <p class="eyebrow">Crafted From Your Pet's Own Photos</p>
      <h2 class="h2">Slow, deliberate, entirely by hand.</h2>
      <p>Again Paws specializes in handcrafted pet keepsakes and memorials. Every piece is carefully handmade based on your pet's photos, capturing unique details, personality and emotions.</p>
      <p>Each order is a quiet collaboration: you send photos, we shape the wool and wood, and together we bring a beloved companion back into view. From a pocket-size mini to a full-body replica, from a garden plaque to a wooden urn — the work is slow, deliberate and made entirely by hand.</p>
      <ul class="checks">
        <li>Custom pet replicas</li><li>Personalized pet gifts</li>
        <li>Memorial &amp; remembrance pieces</li><li>Wholesale customization</li>
      </ul>
    </div>
  </div>
</section>
<section class="section">
  <div class="wrap">
    <p class="eyebrow">What We Stand For</p>
    <h2 class="h2">Emotion, memory &amp; handmade craft.</h2>
    <div class="grid g4 mt-6">
      <div class="card"><h3>Handmade Artistry</h3><p>Every piece is shaped by hand, never mass-produced.</p></div>
      <div class="card"><h3>Emotional Memory</h3><p>We capture the personality that made your pet yours.</p></div>
      <div class="card"><h3>Premium Materials</h3><p>Soft wool felt, warm hardwood and lasting finishes.</p></div>
      <div class="card"><h3>Made For You</h3><p>Customized from your pet's photos, one piece at a time.</p></div>
    </div>
  </div>
</section>
{CTA_BAND}
</main>"""
    page("about/index.html", shell(
        title="About Again Paws | Handmade Custom Pet Keepsakes",
        desc="Again Paws handcrafts pet keepsakes and memorials from your photos — felted portraits, wind chimes, plaques, urns and farewell sets. Meet the hands behind every piece.",
        canonical=f"{SITE}/about/", active="/about/", body=body))

def build_process():
    mats = "".join(f"<li>{x}</li>" for x in [
        "Premium natural wool felt, soft to the touch",
        "Warm hardwood and weatherproof finishes for memorial pieces",
        "Hypoallergenic filling for safe display at home",
        "Optional name engraving and memorial card",
        "Secure, gift-ready packaging",
    ])
    care = "".join(f"<li>{x}</li>" for x in [
        "Dust gently with a soft brush or cool air",
        "Keep away from direct sunlight and humidity",
        "Store in the included box when not on display",
        "Outdoor memorial pieces are finished for year-round weather",
    ])
    body = f"""
<main>
<section class="section-tight">
  <div class="wrap">
    <p class="eyebrow">Our Process</p>
    <h1 class="h1">From a single photo to a finished keepsake.</h1>
    <p class="lead" style="max-width:680px">Every Again Paws piece is shaped slowly by hand. Here is what happens between your photo and the moment it arrives at your door.</p>
  </div>
</section>
<section class="section-tight">
  <div class="wrap"><h2 class="h2">A calm, hands-on journey.</h2><div class="mt-6">{steps_html()}</div></div>
</section>
<section class="band band-sage">
  <div class="wrap split">
    <div>
      <p class="eyebrow">Materials</p>
      <h2 class="h2">Soft, natural &amp; made to last.</h2>
      <ul class="checks">{mats}</ul>
    </div>
    <div>
      <p class="eyebrow">Care</p>
      <h2 class="h2">Keep the memory beautiful.</h2>
      <ul class="checks">{care}</ul>
    </div>
  </div>
</section>
{CTA_BAND}
</main>"""
    page("process/index.html", shell(
        title="How to Order a Custom Pet Keepsake | Again Paws",
        desc="The five-step Again Paws process: send pet photos, confirm design details, handmade crafting, quality check and worldwide delivery. Materials and care explained.",
        canonical=f"{SITE}/process/", active="/process/", body=body))

def build_customization():
    opts = "".join(f"<li>{x}</li>" for x in [
        "Breed, coat colour &amp; markings",
        "Eye colour &amp; expression",
        "Pose, size &amp; scale",
        "Frame, wooden base or display case",
        "Name engraving &amp; memorial card",
        "Collar, bandana or favourite accessory",
        "Personalization for memorial pieces — plaques, urns, chimes and suncatchers",
    ])
    body = f"""
<main>
<section class="section-tight">
  <div class="wrap">
    <p class="eyebrow">Customization</p>
    <h1 class="h1">How your pet becomes a handmade keepsake.</h1>
    <p class="lead" style="max-width:680px">Five simple steps take your favourite photo from the screen to a keepsake you can hold.</p>
  </div>
</section>
<section class="section-tight">
  <div class="wrap">{steps_html()}
    <p class="mt-6"><a class="btn btn-primary" href="/contact/">Upload Pet Photo</a></p>
  </div>
</section>
<section class="band band-white">
  <div class="wrap split">
    <div>
      <p class="eyebrow">Made For Your Pet</p>
      <h2 class="h2">What you can customize.</h2>
      <p>Every keepsake is shaped around the details that made your pet unique.</p>
    </div>
    <div><ul class="checks">{opts}</ul></div>
  </div>
</section>
{CTA_BAND}
</main>"""
    page("customization/index.html", shell(
        title="Custom Pet Felted From Your Photos | Again Paws",
        desc="Customize every detail of your handmade pet keepsake — breed, coat, pose, expression, frames, engraving — plus personalization for memorial plaques, urns and wind chimes.",
        canonical=f"{SITE}/customization/", active="/customization/", body=body))

WA_PREFILL = "Hello%20Again%20Paws!%20I%20would%20love%20to%20know%20more%20about%20a%20custom%20pet%20keepsake."

def build_contact():
    prod_options = ['Mini Portrait ($87)', 'Headshot Frame ($197)', 'Half-Body Frame ($297)',
                    'Full-Body Portrait (from $477)', 'Leather Sculpted Pet Portrait ($112)',
                    'Custom Pet Memorial Wind Chime', 'Custom Pet Portrait Window Suncatcher',
                    'Custom Pet Memorial Plaque & Grave Marker', 'Custom Wooden Pet Urn',
                    'Pet Farewell & Remembrance Set', 'Business & Wholesale Cooperation',
                    'Not sure yet — need advice']
    opts_html = "".join(f'<option>{o}</option>' for o in prod_options)
    body = f"""
<main>
<section class="section-tight">
  <div class="wrap">
    <p class="eyebrow">Contact</p>
    <h1 class="h1">Create your custom pet keepsake.</h1>
    <p class="lead" style="max-width:680px">Tell us about your pet and we will prepare a personalized quote within 24 hours, Monday to Saturday. Prefer chatting? Reach us on WhatsApp any time.</p>
  </div>
</section>
<section class="section-tight">
  <div class="wrap split split-top">
    <form id="inquiryForm" class="card">
      <div class="form-grid">
        <div class="field"><label for="f-name">Name *</label><input id="f-name" required/></div>
        <div class="field"><label for="f-email">Email *</label><input id="f-email" type="email" required/></div>
        <div class="field"><label for="f-country">Country</label><input id="f-country"/></div>
        <div class="field"><label for="f-pet">Pet type</label><select id="f-pet"><option>Dog</option><option>Cat</option><option>Rabbit</option><option>Bird</option><option>Horse</option><option>Other</option></select></div>
        <div class="field" style="grid-column:1/-1"><label for="f-product">Product interested</label><select id="f-product">{opts_html}</select></div>
        <div class="field" style="grid-column:1/-1"><label for="f-msg">Message</label><textarea id="f-msg" rows="4" placeholder="Breed, size, the style you like, and any personalization ideas…"></textarea></div>
      </div>
      <div class="btn-row"><button class="btn btn-primary" type="submit">Send via WhatsApp</button>
      <a class="btn btn-outline-stone" href="mailto:q8461994@gmail.com?subject=Custom%20pet%20keepsake%20inquiry">Or Email Us</a></div>
      <p class="caption mt-4">Sending opens WhatsApp with your message prefilled — no account needed. Please also send 3–5 clear photos of your pet (front, side and face close-up) by WhatsApp or email so we can start.</p>
    </form>
    <div>
      <div class="card">
        <h3 style="font:300 28px/1.2 var(--font-serif)">Reach us directly</h3>
        <p class="mt-3"><strong>Email</strong><br/><a href="mailto:q8461994@gmail.com">q8461994@gmail.com</a></p>
        <p><strong>WhatsApp</strong><br/><a href="https://wa.me/8613064191721">+86 130 6419 1721</a></p>
        <p><strong>Delivery</strong><br/>Worldwide shipping available</p>
        <p class="caption">We usually reply within 24 hours, Monday to Saturday.</p>
      </div>
      <div class="card mt-5">
        <h3 style="font:300 24px/1.2 var(--font-serif)">Prefer to browse first?</h3>
        <p class="mt-2">See styles and reference prices before you reach out.</p>
        <div class="btn-row"><a class="btn btn-stone btn-sm" href="/products/">View Products</a>
        <a class="btn btn-outline-stone btn-sm" href="/pricing/">View Pricing</a></div>
      </div>
    </div>
  </div>
</section>
<script>
(function(){{
  var f=document.getElementById('inquiryForm');
  if(!f)return;
  f.addEventListener('submit',function(e){{
    e.preventDefault();
    var v=function(id){{return (document.getElementById(id).value||'').trim();}};
    var msg='Hello Again Paws! I would love a custom pet keepsake quote.%0A%0AName: '+encodeURIComponent(v('f-name'))+
      '%0AEmail: '+encodeURIComponent(v('f-email'))+
      '%0ACountry: '+encodeURIComponent(v('f-country'))+
      '%0APet type: '+encodeURIComponent(v('f-pet'))+
      '%0AProduct: '+encodeURIComponent(v('f-product'))+
      '%0AMessage: '+encodeURIComponent(v('f-msg'));
    window.open('https://wa.me/8613064191721?text='+msg,'_blank','noopener');
  }});
}})();
</script>
</main>"""
    page("contact/index.html", shell(
        title="Request a Custom Pet Keepsake Quote | Again Paws",
        desc="Request a personalized quote for a handmade pet keepsake or memorial — felted portraits, wind chimes, suncatchers, plaques, urns and farewell sets. Reply within 24 hours.",
        canonical=f"{SITE}/contact/", active="/contact/", body=body))

def build_404():
    body = f"""
<main>
<section class="section">
  <div class="wrap center measure-c">
    <p class="eyebrow">404</p>
    <h1 class="h1">This page wandered off.</h1>
    <p class="lead">Even the best-trained pages sometimes don't come back when called. Let's get you home.</p>
    <div class="btn-row" style="justify-content:center">
      <a class="btn btn-primary" href="/">Back to Home</a>
      <a class="btn btn-outline-stone" href="/products/">Browse the Collection</a>
    </div>
  </div>
</section>
</main>"""
    page("404.html", shell(title="Page Not Found | Again Paws",
        desc="The page you are looking for does not exist.", canonical=f"{SITE}/404.html", body=body))

# ----------------------------------------------------------------------------
# 7. RESKIN STATIC PAGES (keep head meta + <main> content, replace chrome)
# ----------------------------------------------------------------------------
RESKIN = [
    "custom-pet-keepsake-from-photo/index.html",
    "needle-felted-pet-memorial-gift/index.html",
    "personalized-pet-gift-from-photo/index.html",
    "faq/index.html",
    "privacy/index.html", "terms/index.html", "refund-policy/index.html",
    "guides/index.html",
    "guides/are-custom-pet-portraits-worth-it/index.html",
    "guides/best-photos-for-felted-pet/index.html",
    "guides/custom-needle-felted-pet-replica-from-photo/index.html",
    "guides/how-long-does-a-custom-pet-portrait-take/index.html",
    "guides/needle-felted-pet-cost/index.html",
    "guides/pet-memorial-gift-ideas/index.html",
]

ACTIVE_BY_PATH = {"/guides/": "/guides/", "/faq/": "/contact/"}

def reskin(rel):
    path = os.path.join(ROOT, rel)
    h = open(path, encoding="utf-8").read()
    m = re.search(r"<main[^>]*>(.*)</main>", h, re.S)
    if not m:
        print("SKIP (no main):", rel); return
    main_html = m.group(1)
    tm = re.search(r"<title>(.*?)</title>", h, re.S)
    dm = re.search(r'<meta name="description" content="(.*?)"', h, re.S)
    cm = re.search(r'<link rel="canonical" href="(.*?)"', h)
    title = tm.group(1).strip() if tm else "Again Paws"
    desc = dm.group(1).strip() if dm else "Handmade pet keepsakes and memorials from your photos."
    canonical = cm.group(1).strip() if cm else SITE + "/" + rel
    # strip legacy inline styles from kept content if any
    main_html = re.sub(r"<style.*?</style>", "", main_html, flags=re.S)
    # wrap in prose container
    if "prose-wrap" not in main_html:
        main_html = f'<section class="section-tight"><div class="wrap"><div class="prose">{main_html}</div></div></section>'
    route = "/" + os.path.dirname(rel).replace("\\", "/").strip("/") + "/"
    active = "/guides/" if route.startswith("/guides") else None
    # move any JSON-LD from original head into new head
    ld = "".join(re.findall(r"<script type=\"application/ld\+json\">.*?</script>", h, re.S))
    page(rel, shell(title=title, desc=desc, canonical=canonical, active=active,
                    body=f"<main>{main_html}</main>",
                    extra_head=ld))

# ----------------------------------------------------------------------------
# 8. SITEMAP + LLMS
# ----------------------------------------------------------------------------
SITEMAP_URLS = [
    "/", "/products/", "/pricing/", "/about/", "/process/", "/customization/", "/contact/", "/faq/",
    "/custom-pet-wind-chime/", "/custom-pet-window-suncatcher/", "/custom-pet-memorial-plaque/",
    "/custom-pet-urn/", "/pet-farewell-remembrance-set/",
    "/custom-pet-keepsake-from-photo/", "/needle-felted-pet-memorial-gift/", "/personalized-pet-gift-from-photo/",
    "/guides/", "/guides/are-custom-pet-portraits-worth-it/", "/guides/best-photos-for-felted-pet/",
    "/guides/custom-needle-felted-pet-replica-from-photo/", "/guides/how-long-does-a-custom-pet-portrait-take/",
    "/guides/needle-felted-pet-cost/", "/guides/pet-memorial-gift-ideas/",
    "/privacy/", "/terms/", "/refund-policy/",
]

def build_sitemap():
    today = "2026-10-26"
    urls = "".join(f"<url><loc>{SITE}{u}</loc><lastmod>{today}</lastmod><changefreq>weekly</changefreq></url>" for u in SITEMAP_URLS)
    page("sitemap.xml", f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>')

LLMS = """# Again Paws

> Handmade pet keepsakes and memorials made from your photos: needle-felted portraits and the Memorial Collection (wind chimes, window suncatchers, memorial plaques, wooden urns, farewell sets). Made to order, shipped worldwide from the Again Paws studio.

Reference prices: felted portraits $87-$477. Memorial collection: personalized quotes within 24 hours.

- [Home](https://againpaws.vip/): custom pet keepsakes made from photos
- [Products](https://againpaws.vip/products/): full collection of felted portraits and memorial pieces
- [Custom Pet Memorial Wind Chime](https://againpaws.vip/custom-pet-wind-chime/): personalized chime with photo charm and engraved name
- [Custom Pet Portrait Window Suncatcher](https://againpaws.vip/custom-pet-window-suncatcher/): light-catching portrait pendant for windows
- [Custom Pet Memorial Plaque & Grave Marker](https://againpaws.vip/custom-pet-memorial-plaque/): engraved weatherproof garden or graveside plaque
- [Custom Wooden Pet Urn](https://againpaws.vip/custom-pet-urn/): handmade wooden urn with engraved name and portrait plaque
- [Pet Farewell & Remembrance Set](https://againpaws.vip/pet-farewell-remembrance-set/): memorial candle, remembrance card, scatter pouch and keepsake token
- [Pricing](https://againpaws.vip/pricing/): reference prices for every keepsake
- [Customization](https://againpaws.vip/customization/): what can be customized from your pet photos
- [Process](https://againpaws.vip/process/): how an order goes from photo to finished piece
- [Guides](https://againpaws.vip/guides/): buying guides for custom pet memorials
- [FAQ](https://againpaws.vip/faq/): ordering, production and shipping answers
- [Contact](https://againpaws.vip/contact/): request a quote (email or WhatsApp)
"""

def build_llms():
    page("llms.txt", LLMS)

# ----------------------------------------------------------------------------
if __name__ == "__main__":
    os.makedirs("assets", exist_ok=True)
    with open("assets/site-v2.css", "w", encoding="utf-8", newline="\n") as f:
        f.write(CSS)
    print("wrote assets/site-v2.css", len(CSS))
    build_home()
    build_products()
    for p in NEW:
        build_product_page(p)
    build_pricing(); build_about(); build_process(); build_customization(); build_contact(); build_404()
    for rel in RESKIN:
        reskin(rel)
    build_sitemap(); build_llms()
    print("DONE")
