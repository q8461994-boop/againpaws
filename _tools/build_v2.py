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
.thumb-row{display:flex;gap:10px;margin-top:12px;flex-wrap:wrap}
.thumb{width:76px;height:76px;padding:0;border:1px solid var(--color-hairline);border-radius:var(--radius-md);
overflow:hidden;background:var(--color-surface);cursor:pointer}
.thumb img{width:100%;height:100%;object-fit:cover}
.thumb.is-active{border-color:var(--color-stone);box-shadow:0 0 0 1px var(--color-stone)}
.sku-group{margin:var(--space-5) 0 var(--space-4)}
.sku-label{font:600 14px/1.3 var(--font-sans);color:var(--color-stone);margin:0 0 10px}
.sku-row{display:flex;flex-direction:column;gap:10px}
.sku-chip{display:flex;align-items:center;gap:12px;text-align:left;background:var(--color-surface);
border:1px solid var(--color-hairline);border-radius:var(--radius-md);padding:8px 14px 8px 8px;cursor:pointer;width:100%;
font-family:var(--font-sans)}
.sku-chip img{width:52px;height:52px;object-fit:cover;border-radius:8px;flex:none}
.sku-chip span{display:flex;flex-direction:column;font-size:15px;color:var(--color-ink);line-height:1.35}
.sku-chip b{font-weight:600}
.sku-chip em{font-style:normal;color:var(--color-ash);font-size:13px}
.sku-chip i{font-style:normal;color:var(--color-clay);font-weight:600;font-size:14px;margin-top:2px}
.sku-chip:hover{border-color:var(--color-silver)}
.sku-chip.is-active{border-color:var(--color-stone);box-shadow:0 0 0 1px var(--color-stone)}
.pdp-price{font:300 34px/1.2 var(--font-serif);color:var(--color-ink);margin:var(--space-4) 0 var(--space-2)}
.pdp-price-note{font:400 14px/1.4 var(--font-sans);color:var(--color-ash)}
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

/* ---------- cart, drawer & checkout ---------- */
.is-locked{overflow:hidden}
.header-actions{display:flex;align-items:center;gap:10px;margin-left:var(--space-5)}
.cart-link{display:inline-flex;align-items:center;gap:7px;text-decoration:none;color:var(--color-stone);
font:500 14px/1 var(--font-sans);border:1px solid var(--color-hairline);border-radius:var(--radius-full);
padding:9px 15px;background:var(--color-surface)}
.cart-link:hover{border-color:var(--color-stone);color:var(--color-ink)}
.cart-count{display:inline-flex;align-items:center;justify-content:center;min-width:19px;height:19px;padding:0 5px;
border-radius:var(--radius-full);background:var(--color-clay);color:#fff;font:600 11px/1 var(--font-sans)}
.cart-count[hidden]{display:none}
.drawer{position:fixed;inset:0;z-index:120;display:flex;justify-content:flex-end}
.drawer[hidden]{display:none}
.drawer-backdrop{position:absolute;inset:0;background:rgba(28,27,26,.42);opacity:0;transition:opacity .22s ease}
.drawer.is-open .drawer-backdrop{opacity:1}
.drawer-panel{position:relative;width:min(430px,100%);height:100%;background:var(--color-canvas);
display:flex;flex-direction:column;transform:translateX(101%);transition:transform .24s ease;box-shadow:var(--shadow-2)}
.drawer.is-open .drawer-panel{transform:none}
.drawer-head{display:flex;align-items:center;justify-content:space-between;padding:var(--space-5);
border-bottom:1px solid var(--color-hairline)}
.drawer-head h2{font:300 24px/1.1 var(--font-serif);margin:0}
.drawer-close{background:none;border:0;font-size:26px;line-height:1;cursor:pointer;color:var(--color-stone);padding:2px 8px}
.drawer-body{flex:1;overflow-y:auto;padding:var(--space-2) var(--space-5)}
.drawer-foot{border-top:1px solid var(--color-hairline);padding:var(--space-5);background:var(--color-surface)}
.cart-line{display:grid;grid-template-columns:84px 1fr auto;gap:var(--space-4);align-items:start;
padding:var(--space-4) 0;border-bottom:1px solid var(--color-hairline)}
.cart-line:first-child{padding-top:var(--space-3)}
.cart-line:last-child{border-bottom:0}
.cart-line.is-compact{grid-template-columns:62px 1fr auto;gap:12px;padding:12px 0}
.cart-thumb{background:var(--color-surface-grey);border-radius:var(--radius-md);overflow:hidden;aspect-ratio:1}
.cart-thumb img{width:100%;height:100%;object-fit:cover}
.cart-line-name{font:500 16px/1.35 var(--font-sans);margin:0 0 2px}
.cart-line-variant{font-size:13px;color:var(--color-ash);margin:0 0 8px}
.cart-line-actions{display:flex;align-items:center;gap:14px;flex-wrap:wrap}
.cart-line-price{font:600 15px/1.3 var(--font-sans);color:var(--color-clay);white-space:nowrap}
.link-quiet{background:none;border:0;padding:0;font:400 13px/1.4 var(--font-sans);color:var(--color-ash);
text-decoration:underline;text-underline-offset:3px;cursor:pointer}
.link-quiet:hover{color:var(--color-ink)}
.qty{display:inline-flex;align-items:center;border:1px solid var(--color-hairline);border-radius:var(--radius-full);
background:var(--color-surface);overflow:hidden}
.qty button{width:36px;height:38px;background:none;border:0;font-size:16px;cursor:pointer;color:var(--color-stone)}
.qty button:hover{background:var(--color-surface-grey)}
.qty span{min-width:24px;text-align:center;font:500 14px/1 var(--font-sans)}
.qty-sm button{width:28px;height:28px;font-size:14px}
.qty-sm span{min-width:18px;font-size:13px}
.qty input{width:52px;height:40px;border:0;text-align:center;font:500 15px/1 var(--font-sans);background:none}
.cart-layout{display:grid;grid-template-columns:1.55fr .9fr;gap:var(--space-7);align-items:start;margin-top:var(--space-6)}
@media(max-width:900px){.cart-layout{grid-template-columns:1fr;gap:var(--space-6)}}
.cart-side{position:sticky;top:96px}
@media(max-width:900px){.cart-side{position:static}}
.cart-summary h3{font:300 26px/1.2 var(--font-serif);margin:0 0 var(--space-4)}
.sum-list{margin:0 0 var(--space-4)}
.sum-row{display:flex;justify-content:space-between;align-items:baseline;gap:12px;
font-size:15px;color:var(--color-stone);margin:0 0 10px}
.sum-row dt,.sum-row dd{margin:0}
.sum-row.is-total{border-top:1px solid var(--color-hairline);padding-top:var(--space-3);margin-top:var(--space-3);
font:600 17px/1.3 var(--font-sans);color:var(--color-ink)}
.sum-row.is-total dd{font:300 26px/1.2 var(--font-serif)}
.cart-mini{font-size:13px;color:var(--color-ash);margin:0 0 var(--space-4);line-height:1.5}
.paypal-area{margin:0 0 var(--space-4);min-height:52px}
.paypal-area .btn{margin-bottom:10px}
.pay-loading{font-size:14px;color:var(--color-ash)}
.pay-error{color:var(--color-error);font-size:14px;margin:10px 0 0}
.pay-fallback{font-size:14px;color:var(--color-stone);margin:0 0 12px}
.pay-fallback-note{font-size:13px;color:var(--color-ash);margin:0 0 8px}
.pay-notes{border-top:1px solid var(--color-hairline);padding-top:var(--space-4);margin-top:var(--space-4)}
.pay-notes p{font-size:13px;color:var(--color-ash);margin:0 0 8px;line-height:1.5}
.pay-notes p:last-child{margin-bottom:0}
.cart-wide{width:100%;margin-bottom:10px;text-align:center;justify-content:center}
.cart-help{background:var(--color-surface);border:1px solid var(--color-hairline);border-radius:var(--radius-lg);
padding:var(--space-5);margin-top:var(--space-4)}
.cart-help h3{font:400 17px/1.3 var(--font-sans);margin:0 0 6px}
.cart-help p{font-size:14px;color:var(--color-stone);margin:0}
.cart-empty{background:var(--color-surface);border:1px solid var(--color-hairline);border-radius:var(--radius-lg);
padding:var(--space-6);text-align:center}
.cart-empty .lead{margin-bottom:var(--space-4)}
.cart-empty .btn-row{justify-content:center}
.buy-block{margin-top:var(--space-4)}
.qty-row{display:flex;align-items:center;gap:14px;margin-bottom:var(--space-3)}
.qty-row label{font:600 14px/1 var(--font-sans);color:var(--color-stone)}
.pay-line{font-size:13px;color:var(--color-ash);margin:var(--space-3) 0 0;line-height:1.5}
.note-block{background:var(--color-surface);border:1px solid var(--color-hairline);border-radius:var(--radius-lg);
padding:var(--space-6)}
.note-block p{color:var(--color-stone);margin:0 0 var(--space-4)}
.note-block p:last-child{margin-bottom:0}
.cart-mini+.pay-fallback{margin-top:6px}
.buybar{display:none}
@media(max-width:900px){
 .buybar{display:flex;position:fixed;left:0;right:0;bottom:0;z-index:90;align-items:center;
  justify-content:space-between;gap:12px;padding:10px 16px;background:var(--color-canvas);
  border-top:1px solid var(--color-hairline);box-shadow:0 -6px 20px rgba(28,27,26,.07)}
 body:has(.buybar){padding-bottom:78px}
 .buybar .btn{padding:13px 24px;font-size:15px}
 .buybar-price{display:flex;flex-direction:column;line-height:1.15;min-width:0}
 .buybar-price b{font:600 18px/1.2 var(--font-sans);color:var(--color-ink)}
 .buybar-price span{font-size:12px;color:var(--color-ash);white-space:nowrap;overflow:hidden;
  text-overflow:ellipsis;max-width:170px}
}
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
def money(v):
    """$39 · $23.50 · $28.50 — drop trailing zeros only when the cents are .00"""
    return ("$%d" % v) if abs(v - int(v)) < 1e-9 else ("$%.2f" % v)


def sku(sid, name, price, img, note=""):
    return dict(id=sid, name=name, price=price, img=img, note=note)


IMG = "/images/products"

NEW = [
 dict(slug="custom-pet-wind-chime", kicker="Memorial Collection",
      name="Custom Pet Memorial Wind Chime",
      price_from=39.0,
      desc="A wooden wind chime with an engraved tag carrying your pet's photo, name and dates.",
      short="Engraved photo tag, wooden crown and warm-sounding tubes — personalise it with a photo, name and dates.",
      long=("Some pets are remembered in sound as much as in sight. This memorial wind chime hangs a wooden tag engraved with "
            "your pet's photo, name and dates, above a ring of metal tubes tuned to a soft, low tone. Hang it on a porch, by a "
            "window or near a favourite spot in the garden — every breeze becomes a quiet hello."),
      incl=["Wooden tag engraved with your pet's photo, name and dates",
            "Solid wood crown with metal tubes",
            "Ready to hang — no assembly",
            "Gift-ready packaging"],
      spec=[("Total length","Approx. 68 cm"),
            ("Wooden crown","Ø 8.8 cm"),
            ("Hanging tag","9.5 × 5 cm"),
            ("Materials","Solid wood, aluminium tubes"),
            ("Personalization","Photo, name and dates engraved on the tag"),
            ("Lead time","5–10 days production before shipping"),
            ("Shipping","Worldwide, tracked")],
      faq=[("Can I put any photo on the tag?","Yes. Send a clear, well-lit photo where your pet's face fills the frame. We confirm the crop with you before engraving."),
           ("Can it hang outdoors?","The wood and tubes are finished for outdoor use. Under a porch or eaves the engraved tag will stay crisp for years."),
           ("What text fits on the tag?","A name and dates sit comfortably alongside the photo. A short line such as “Always with me” can be added on request.")],
      images=[(f"{IMG}/custom-pet-wind-chime/natural-silver-photo.webp","Custom pet memorial wind chime in natural wood with silver tubes and an engraved photo tag"),
              (f"{IMG}/custom-pet-wind-chime/natural-silver-silhouette.webp","Wind chime with engraved silhouette tag showing a pet name"),
              (f"{IMG}/custom-pet-wind-chime/coffee-silver-detail.webp","Coffee-coloured wooden crown with silver chime tubes"),
              (f"{IMG}/custom-pet-wind-chime/coffee-black-detail.webp","Coffee-coloured wooden crown with black chime tubes")],
      skus=[sku("natural-silver","Natural Wood · Silver Tubes",39.0,f"{IMG}/custom-pet-wind-chime/natural-silver-photo.webp","Light natural wood"),
            sku("coffee-silver","Coffee Wood · Silver Tubes",39.0,f"{IMG}/custom-pet-wind-chime/coffee-silver-detail.webp","Warm coffee wood"),
            sku("coffee-black","Coffee Wood · Black Tubes",39.0,f"{IMG}/custom-pet-wind-chime/coffee-black-detail.webp","Matte black tubes")],
      sku_label="Choose a finish",
      schema_desc="Wooden memorial wind chime engraved with your pet's photo, name and dates."),

 dict(slug="custom-pet-window-suncatcher", kicker="Memorial Collection",
      name="Custom Pet Portrait Window Suncatcher",
      price_from=31.0,
      desc="A stained-glass style pet portrait made from your photo — it glows in the window light.",
      short="Made to order from your photo in three sizes, with a chain ready to hang.",
      long=("Turn the light your pet loved to nap in into a small daily ritual. Your photo is developed into a stained-glass "
            "style portrait panel, finished with a metal chain — hang it in any window, on a mirror or across a sunny corner, "
            "and the colours come alive when the light passes through."),
      incl=["Portrait panel made from your pet's photo",
            "Metal hanging chain and ring",
            "Name or short message on request",
            "Protective gift packaging"],
      spec=[("Sizes","15 × 15 cm · 20 × 20 cm · 25 × 25 cm"),
            ("Material","Stained-glass style panel with metal chain"),
            ("Personalization","Your pet's photo; name or short message optional"),
            ("Lead time","5–10 days production before shipping"),
            ("Shipping","Worldwide, tracked")],
      faq=[("Which size should I choose?","15 cm suits a small kitchen window, 20 cm is the most popular for living-room windows, and 25 cm makes the portrait the focal point of a larger window."),
           ("Will the colours fade in direct sun?","The panel is made to hang in daylight. As with any printed keepsake, a spot that avoids hours of harsh afternoon sun will keep the colours truest."),
           ("Can I choose what the pet is doing?","Send several photos — sitting, lying down, head tilt — and we will recommend the pose that converts best into a round portrait.")],
      images=[(f"{IMG}/custom-pet-window-suncatcher/pet-portrait.webp","Custom pet portrait suncatcher with a dog portrait and engraved name"),
              (f"{IMG}/custom-pet-window-suncatcher/custom-from-photo.webp","Suncatcher hanging in a window beside the original reference photo"),
              (f"{IMG}/custom-pet-window-suncatcher/in-window.webp","Stained-glass style portrait panel held in the hand")],
      skus=[sku("15cm","15 × 15 cm",31.0,f"{IMG}/custom-pet-window-suncatcher/pet-portrait.webp"),
            sku("20cm","20 × 20 cm",33.0,f"{IMG}/custom-pet-window-suncatcher/pet-portrait.webp"),
            sku("25cm","25 × 25 cm",37.0,f"{IMG}/custom-pet-window-suncatcher/pet-portrait.webp")],
      sku_label="Choose a size",
      schema_desc="Stained-glass style custom pet portrait suncatcher made from your photo."),

 dict(slug="pet-memorial-garden-stone", kicker="Memorial Collection",
      name="Pet Memorial Garden Stone",
      price_from=23.5,
      desc="A weather-resistant memorial stone with a photo window and a flower planter top.",
      short="Four ready-designed stones with a built-in photo window — place it in the garden, on a patio or at the graveside.",
      long=("A place to visit. Each memorial stone is cast with a built-in photo window and a small planter top, so you can set "
            "your pet's picture and a few fresh flowers into the same spot. Four inscriptions are available, each finished by "
            "hand and sealed for outdoor weather. No engraving or design work is needed — insert your photo and place it."),
      incl=["Cast memorial stone with a built-in photo window",
            "Planter top for fresh or dried flowers",
            "Weather-resistant sealed finish",
            "Ready to display — no assembly"],
      spec=[("Designs","Four fixed inscriptions — Forever · Companion · In My Heart · Angel Heart"),
            ("Material","Weather-resistant cast stone"),
            ("Photo window","Insert your own photo (approx. 6 × 4 cm)"),
            ("Placement","Garden bed, graveside, patio or indoor shelf"),
            ("Lead time","3–7 days before shipping"),
            ("Shipping","Worldwide, tracked")],
      faq=[("Is the stone personalised?","No — these are ready-designed stones with four fixed inscriptions. You add your own photo to the built-in window, and we ship straight away."),
           ("Can it stay outside all year?","Yes. The stone is cast and sealed for outdoor use. In hard frost, bring it under cover to protect the photo print."),
           ("What size photo fits?","A standard small print trimmed to roughly 6 × 4 cm sits behind the window.")],
      images=[(f"{IMG}/pet-memorial-garden-stone/forever.webp","Pet memorial garden stone inscribed Forever in our hearts"),
              (f"{IMG}/pet-memorial-garden-stone/companion.webp","Pet memorial stone inscribed Thank you for your company"),
              (f"{IMG}/pet-memorial-garden-stone/in-my-heart.webp","Pet memorial stone inscribed You are in my heart forever"),
              (f"{IMG}/pet-memorial-garden-stone/angel-heart.webp","Heart-shaped pet memorial stone inscribed You are my angel"),
              (f"{IMG}/pet-memorial-garden-stone/angel-heart-front.webp","Heart-shaped memorial stone photographed on white")],
      skus=[sku("forever","Forever",23.5,f"{IMG}/pet-memorial-garden-stone/forever.webp","“Forever in our hearts”"),
            sku("companion","Companion",23.5,f"{IMG}/pet-memorial-garden-stone/companion.webp","“Thank you for your company”"),
            sku("in-my-heart","In My Heart",23.5,f"{IMG}/pet-memorial-garden-stone/in-my-heart.webp","“You are in my heart forever”"),
            sku("angel-heart","Angel Heart",23.5,f"{IMG}/pet-memorial-garden-stone/angel-heart.webp","“You are my angel”")],
      sku_label="Choose an inscription",
      schema_desc="Weather-resistant pet memorial garden stone with photo window and planter top."),

 dict(slug="pet-cremation-urn", kicker="Memorial Collection",
      name="Classic Square Pet Cremation Urn",
      price_from=28.5,
      desc="A heavyweight urn box with a photo window and paw details, in four colours.",
      short="18.5 × 14 × 11.5 cm · 1100 ml capacity · photo window on the front.",
      long=("A quiet, solid resting place. The Classic Square Urn is cast in a heavyweight stone-grey material with brushed gold "
            "paw prints and the words “we love you forever” along the base. A window on the front holds your pet's photo, so the "
            "urn reads as a framed picture rather than a box. Available in pink, white, black and grey."),
      incl=["Cast urn with photo window",
            "Brushed gold paw and corner detailing",
            "Fits a standard trimmed photo behind the window",
            "Protective packaging for transit"],
      spec=[("Dimensions","18.5 × 14 × 11.5 cm"),
            ("Capacity","1100 ml"),
            ("Weight","1964 g"),
            ("Material","Portland cement composite"),
            ("Colours","Pink · White · Black · Grey"),
            ("Lead time","3–7 days before shipping"),
            ("Shipping","Worldwide, tracked")],
      faq=[("What size pet does it suit?","With 1100 ml of interior space it suits most cats and small to medium dogs. For larger pets, message us and we will advise."),
           ("Is the urn personalised?","No — the urn ships as designed, with a photo window you fill yourself."),
           ("How do I insert the photo?","Trim a print to the window size, slide it behind the front frame and press the frame back into place.")],
      images=[(f"{IMG}/pet-cremation-urn/pink.webp","Pink classic square pet cremation urn with dimensions"),
              (f"{IMG}/pet-cremation-urn/white.webp","White classic square pet cremation urn"),
              (f"{IMG}/pet-cremation-urn/black.webp","Black classic square pet cremation urn"),
              (f"{IMG}/pet-cremation-urn/grey.webp","Grey classic square pet cremation urn"),
              (f"{IMG}/pet-cremation-urn/grey-lifestyle.webp","Grey urn with a photo of a cat in the front window")],
      skus=[sku("pink","Pink",28.5,f"{IMG}/pet-cremation-urn/pink.webp"),
            sku("white","White",28.5,f"{IMG}/pet-cremation-urn/white.webp"),
            sku("black","Black",28.5,f"{IMG}/pet-cremation-urn/black.webp"),
            sku("grey","Grey",28.5,f"{IMG}/pet-cremation-urn/grey.webp")],
      sku_label="Choose a colour",
      schema_desc="Classic square pet cremation urn, 1100 ml, with photo window in four colours."),

 dict(slug="pet-memorial-offering-set", kicker="Memorial Collection",
      name="Pet Memorial Offering Set · 55 Pieces",
      price_from=24.8,
      desc="A complete 55-piece farewell offering set — favourite treats, grooming items and traditional paper offerings.",
      short="55 pieces in one box: treats, milk and biscuits, grooming items, paper offerings and a memorial letter.",
      long=("A complete farewell, gathered in one box. The 55-piece set brings together the things many families place at a "
            "pet's resting place: premium treats, milk and biscuits, grooming items, and a set of traditional paper offerings — "
            "joss paper, folded ingots and a memorial letter — with an incense burner and keepsake card. Everything arrives "
            "arranged and ready to lay out."),
      incl=["55 pieces, arranged in one gift box",
            "Treats, milk, biscuits and freeze-dried snacks",
            "Grooming items: comb, toothbrush, shampoo, nail clippers",
            "Traditional paper offerings, folded ingots and memorial letter",
            "Incense burner and keepsake card"],
      spec=[("Pieces","55"),
            ("Style","3D (dimensional) offering set"),
            ("Includes","Treats · grooming · paper offerings · incense burner"),
            ("Lead time","3–7 days before shipping"),
            ("Shipping","Worldwide, tracked")],
      faq=[("What exactly is in the box?","Treats (tuna, salmon, wagyu beef and M9 steak), pet milk, biscuits, freeze-dried snacks, grooming items, a full set of traditional paper offerings with folded ingots, a memorial letter, an incense burner and a keepsake card — 55 pieces in total."),
           ("Is this a religious set?","It comes from a traditional East Asian farewell custom rather than from a single religion — the paper is a way of sending a pet off with the things it loved. Nothing in the box has to be used, and many families keep only the treats and keepsakes. There is a fuller explanation further up this page."),
           ("Can it be shipped as a gift?","Yes. Tell us when you order and we will leave the price out of the parcel and add a gift card.")],
      note=dict(
        eyebrow="A Note On The Paper Offerings",
        title="What the 55 pieces are for.",
        paras=[
          "The folded paper in this set comes from an East Asian farewell custom. Families gather the things a pet loved in life — a favourite treat, a bowl of milk, a comb — and add paper gifts: folded ingots, paper clothing and a written letter. At the graveside or at a small memorial service the paper is burned, so that the pet takes it along. It is a way of saying: this was yours, keep it.",
          "Nothing here is required, and nothing is permanent. Plenty of families use the treats, the grooming items and the keepsake card, and leave the paper folded in the box as a memento. Others use the set exactly as intended. If you would rather not receive the paper items at all, say so when you order and we will take them out before shipping.",
          "Buying it for someone else? The box arrives fully arranged, with a small card that explains each item in plain English — so nothing has to be explained out loud at a difficult moment."]),
      images=[(f"{IMG}/pet-memorial-offering-set/set-layout.webp","55-piece pet memorial offering set laid out with treats, paper offerings and incense burner"),
              (f"{IMG}/pet-memorial-offering-set/rainbow-bridge.webp","A dog and a cat asleep together in the sun")],
      skus=[sku("default","55-Piece Set · 3D Style",24.8,f"{IMG}/pet-memorial-offering-set/set-layout.webp")],
      sku_label="",
      schema_desc="55-piece pet memorial offering set with treats, grooming items and traditional paper offerings."),
]

ALL_PRODUCTS = FELT + NEW

# ----------------------------------------------------------------------------
# 4. SHELL
# ----------------------------------------------------------------------------
NAV = [
    ("/", "Home"), ("/products/", "Products"), ("/pricing/", "Pricing"),
    ("/process/", "Process"), ("/guides/", "Guides"), ("/about/", "About"), ("/contact/", "Contact"),
]

def shell(*, title, desc, canonical, active=None, body, extra_head="", og_image="/images/hero.webp", og_type="website", robots="index, follow"):
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
<meta name="robots" content="{robots}"/>
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
<script src="/assets/store-config.js"></script>
<script src="/analytics.js" defer></script>
</head>
<body>
<div class="announce band-clay">Handmade · Made to Order · Worldwide Delivery</div>
<header class="site-header" id="siteHeader">
  <div class="wrap header-inner">
    <a class="brand" href="/">Again <em>Paws</em></a>
    <nav class="site-nav" id="siteNav" aria-label="Main navigation">
      {nav_html}
      <a class="btn btn-primary btn-sm" href="/contact/">Request a Quote</a>
    </nav>
    <div class="header-actions">
      <a class="cart-link" href="/cart/" aria-label="Shopping bag"><span>Bag</span><span class="cart-count" data-cart-count hidden>0</span></a>
      <button class="nav-toggle" id="navToggle" aria-label="Open menu" aria-expanded="false"><span></span><span></span><span></span></button>
    </div>
  </div>
</header>
{body}
<div class="drawer" id="cartDrawer" hidden aria-hidden="true">
  <div class="drawer-backdrop" data-cart-close></div>
  <aside class="drawer-panel" role="dialog" aria-modal="true" aria-label="Shopping bag">
    <header class="drawer-head"><h2>Your bag</h2><button class="drawer-close" type="button" data-cart-close aria-label="Close bag">×</button></header>
    <div class="drawer-body" id="cartDrawerList"></div>
    <footer class="drawer-foot" id="cartDrawerFoot" hidden></footer>
  </aside>
</div>
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
          <li><a href="/cart/">Bag &amp; Checkout</a></li>
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
<script src="/assets/store.js" defer></script>
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
    prices = sorted({k["price"] for k in p["skus"]})
    if len(prices) == 1:
        price_line = money(prices[0])
    else:
        price_line = "From " + money(prices[0])
    cover = p["images"][0][0]
    return f"""<a class="pcard" href="/{p['slug']}/">
  <div class="pcard-art">{tag_html}<img src="{cover}" alt="{html.escape(p['name'])}" loading="lazy"/></div>
  <div class="pcard-body">
    <p class="pcard-kicker">{html.escape(p['kicker'])}</p>
    <h3 class="pcard-title">{html.escape(p['name'])}</h3>
    <p class="pcard-desc">{html.escape(p['desc'])}</p>
    <p class="pcard-price">{price_line}</p>
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
        <div class="round-img"><img src="/images/products/pet-cremation-urn/pink-lifestyle.webp" alt="Classic square pet cremation urn with a photo in the front window" loading="lazy"/></div>
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
    <p class="lead" style="max-width:680px">Five memorial pieces at fixed prices: wind chime $39 · portrait suncatcher from $31 · garden stone $23.50 · cremation urn $28.50 · 55-piece offering set $24.80.</p>
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
    <p class="lead" style="max-width:640px">Fixed prices, ready to ship — personalised from your photos where the piece is custom.</p>
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
        img = p.get("img") or (p.get("images") or [("", "")])[0][0]
        if img:
            d["image"] = SITE + img
        items.append(d)
    return ('<script type="application/ld+json">'
            + json.dumps({"@context": "https://schema.org", "@type": "ItemList",
                          "name": "Again Paws Keepsake Collection", "itemListElement": items}, ensure_ascii=False)
            + '</script>')

def build_product_page(p):
    personalised = p["name"].startswith("Custom")
    faq_json = json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in p["faq"]]}, ensure_ascii=False)
    incl = "".join(f"<li>{x}</li>" for x in p["incl"])
    spec = "".join(f"<tr><th>{k}</th><td>{v}</td></tr>" for k, v in p["spec"])
    faq_html = "".join(f'<div class="faq-item"><h3>{q}</h3><p>{a}</p></div>' for q, a in p["faq"])
    related = "".join(new_card(r) for r in NEW if r["slug"] != p["slug"])

    # ---- gallery + sku selector -------------------------------------------------
    cover_src, cover_alt = p["images"][0]
    thumbs = "".join(
        f'<button class="thumb{" is-active" if i == 0 else ""}" type="button" data-img="{src}" data-alt="{html.escape(alt)}">'
        f'<img src="{src}" alt="{html.escape(alt)}" loading="lazy"/></button>'
        for i, (src, alt) in enumerate(p["images"]))

    prices = sorted({k["price"] for k in p["skus"]})
    price_text = money(prices[0]) if len(prices) == 1 else "From " + money(prices[0])
    if len(p["skus"]) > 1:
        chips = "".join(
            f'<button class="sku-chip{" is-active" if i == 0 else ""}" type="button" aria-pressed="{"true" if i == 0 else "false"}" '
            f'data-img="{k["img"]}" data-price="{money(k["price"])}" data-name="{html.escape(k["name"])}" '
            f'data-sku="{k["id"]}" data-pricec="{int(round(k["price"] * 100))}">'
            f'<img src="{k["img"]}" alt="" loading="lazy"/>'
            f'<span><b>{html.escape(k["name"])}</b>'
            f'{f"<em>{html.escape(k["note"])}</em>" if k["note"] else ""}'
            f'<i>{money(k["price"])}</i></span></button>'
            for i, k in enumerate(p["skus"]))
        sku_block = f'''<div class="sku-group">
        <p class="sku-label">{html.escape(p["sku_label"])}</p>
        <div class="sku-row">{chips}</div>
      </div>'''
    else:
        sku_block = ""

    offers = [{"@type": "Offer", "name": k["name"], "price": f"{k['price']:.2f}",
               "priceCurrency": "USD", "availability": "https://schema.org/InStock",
               "url": f"{SITE}/{p['slug']}/"} for k in p["skus"]]
    prod_json = json.dumps({"@context": "https://schema.org", "@type": "Product",
        "name": p["name"], "description": p["schema_desc"], "image": [SITE + src for src, _ in p["images"]],
        "brand": {"@type": "Brand", "name": "Again Paws"}, "url": f"{SITE}/{p['slug']}/",
        "offers": offers}, ensure_ascii=False)

    about_block = (
        ('<p class="eyebrow">About This Piece</p>'
         '<h2 class="h2">Made from your photos, one at a time.</h2>'
         f'<p>{html.escape(p["long"])}</p>'
         '<p class="muted">Every order starts with a conversation: send your photos, tell us about your pet, and we confirm every '
         'detail — size, personalisation and finish — before production begins.</p>'
         '<div class="btn-row"><a class="btn btn-stone" href="/customization/">How Customization Works</a>'
         '<a class="btn btn-outline-stone" href="/process/">See The Process</a></div>')
        if personalised else
        ('<p class="eyebrow">About This Piece</p>'
         '<h2 class="h2">Ready to send, made to last.</h2>'
         f'<p>{html.escape(p["long"])}</p>'
         '<p class="muted">These pieces are ready-designed, so there is no artwork or proofing step — we pack and ship within a '
         'few working days. If you would like a photo print trimmed to fit, say so when you order.</p>'
         '<div class="btn-row"><a class="btn btn-stone" href="/process/">Shipping & Delivery</a>'
         '<a class="btn btn-outline-stone" href="/faq/">Read The FAQ</a></div>'))

    first_sku = p["skus"][0]
    add_attrs = (f'data-id="{p["slug"]}::{first_sku["id"]}" data-slug="{p["slug"]}" '
                 f'data-name="{html.escape(p["name"])}" data-variant="{html.escape(first_sku["name"])}" '
                 f'data-price="{int(round(first_sku["price"] * 100))}" data-img="{first_sku["img"]}"')

    note_html = ""
    if p.get("note"):
        n = p["note"]
        paras = "".join(f"<p>{x}</p>" for x in n["paras"])
        note_html = f"""<section class="section band-grey">
  <div class="wrap measure-c">
    <p class="eyebrow">{n['eyebrow']}</p>
    <h2 class="h2">{n['title']}</h2>
    <div class="note-block mt-5">{paras}</div>
  </div>
</section>"""

    body = f"""
<main>
<section class="section-tight">
  <div class="wrap">
    <p class="breadcrumb"><a href="/">Home</a> · <a href="/products/#memorial">Memorial Collection</a> · {html.escape(p['name'])}</p>
    <div class="detail-grid">
      <div>
        <div class="detail-art"><img id="heroImg" src="{cover_src}" alt="{html.escape(cover_alt)}"/></div>
        <div class="thumb-row">{thumbs}</div>
      </div>
      <div>
        <p class="eyebrow">{html.escape(p['kicker'])}</p>
        <h1 class="h1">{html.escape(p['name'])}</h1>
        <p class="lead">{html.escape(p['short'])}</p>
        <p class="pdp-price" id="pdpPrice">{price_text}<span class="pdp-price-note"> · {("made to order" if personalised else "ready to ship")}</span></p>
        {sku_block}
        <div class="buy-block">
          <div class="qty-row">
            <label for="qtyInput">Quantity</label>
            <div class="qty">
              <button type="button" data-qty="-1" aria-label="Decrease quantity">−</button>
              <input id="qtyInput" type="number" min="1" max="99" value="1" inputmode="numeric"/>
              <button type="button" data-qty="1" aria-label="Increase quantity">+</button>
            </div>
          </div>
          <div class="btn-row">
            <button class="btn btn-primary" type="button" data-add {add_attrs}>Add to Bag</button>
            <a class="btn btn-outline-stone" href="/contact/">Ask us first</a>
          </div>
          <p class="pay-line" data-ship-note></p>
        </div>
        <ul class="checks">{incl}</ul>
      </div>
    </div>
  </div>
</section>

<section class="band band-white">
  <div class="wrap split split-top">
    <div>{about_block}</div>
    <div class="card">
      <h3 style="font:300 28px/1.2 var(--font-serif)">Specifications</h3>
      <table class="spec-list mt-4">{spec}</table>
    </div>
  </div>
</section>

{note_html}
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
</main>
<div class="buybar">
  <div class="buybar-price"><b id="buyBarPrice">{money(first_sku['price'])}</b><span id="buyBarName">{html.escape(first_sku['name'])}</span></div>
  <button class="btn btn-primary" type="button" data-add {add_attrs}>Add to bag</button>
</div>
<script>
(function(){{
  var hero=document.getElementById('heroImg'), priceEl=document.getElementById('pdpPrice');
  document.querySelectorAll('.thumb').forEach(function(b){{
    b.addEventListener('click',function(){{
      hero.src=b.dataset.img; hero.alt=b.dataset.alt;
      document.querySelectorAll('.thumb').forEach(function(x){{x.classList.remove('is-active');}});
      b.classList.add('is-active');
    }});
  }});
  document.querySelectorAll('.sku-chip').forEach(function(c){{
    c.addEventListener('click',function(){{
      document.querySelectorAll('.sku-chip').forEach(function(x){{x.classList.remove('is-active');x.setAttribute('aria-pressed','false');}});
      c.classList.add('is-active'); c.setAttribute('aria-pressed','true');
      hero.src=c.dataset.img;
      priceEl.innerHTML=c.dataset.price+'<span class="pdp-price-note"> · '+c.dataset.name+'</span>';
      var addBtn=document.querySelector('[data-add]');
      if(addBtn){{
        document.querySelectorAll('[data-add]').forEach(function(b){{
          b.dataset.id='{p['slug']}::'+c.dataset.sku;
          b.dataset.variant=c.dataset.name;
          b.dataset.price=c.dataset.pricec;
          b.dataset.img=c.dataset.img;
        }});
      }}
      var bp=document.getElementById('buyBarPrice'), bn=document.getElementById('buyBarName');
      if(bp){{bp.textContent=c.dataset.price; bn.textContent=c.dataset.name;}}
      var firstThumb=document.querySelector('.thumb');
      if(firstThumb){{document.querySelectorAll('.thumb').forEach(function(t){{t.classList.remove('is-active');}});}}
    }});
  }});
}})();
</script>"""
    page(f"{p['slug']}/index.html", shell(
        title=f"{p['name']} | Again Paws",
        desc=p["desc"], canonical=f"{SITE}/{p['slug']}/", active="/products/",
        og_image=p["images"][0][0], og_type="product",
        body=body, extra_head=f'<script type="application/ld+json">{prod_json}</script>'
                              f'<script type="application/ld+json">{faq_json}</script>'))

def build_pricing():
    rows = "".join(
        f'<tr><td><strong>{p["kicker"]}</strong><br/><span class="muted small">{html.escape(p["name"])}</span></td>'
        f'<td class="t-price">{p["price"]}</td><td>{html.escape(p["incl"])}</td></tr>' for p in FELT)

    mrows = ""
    for prod in NEW:
        first = True
        for k in prod["skus"]:
            name_cell = (f'<strong>{html.escape(prod["name"])}</strong><br/>'
                         f'<span class="muted small"><a href="/{prod["slug"]}/">View product</a></span>') if first else ""
            opt = html.escape(k["name"])
            if k["note"]:
                opt += f'<br/><span class="muted small">{html.escape(k["note"])}</span>'
            mrows += f'<tr><td>{name_cell}</td><td>{opt}</td><td class="t-price">{money(k["price"])}</td></tr>'
            first = False

    body = f"""
<main>
<section class="section-tight">
  <div class="wrap">
    <p class="eyebrow">Pricing</p>
    <h1 class="h1">Pricing, in plain numbers.</h1>
    <p class="lead" style="max-width:680px">Felted portraits are quoted per pet — reference prices below. The Memorial Collection is fixed-price by size, colour or inscription.</p>
  </div>
</section>
<section class="section-tight">
  <div class="wrap">
    <h2 class="h2">The Memorial Collection</h2>
    <p class="muted" style="max-width:620px">Fixed prices. Choose the size, colour or inscription on the product page.</p>
    <div class="mt-5" style="overflow-x:auto"><table class="table">
      <thead><tr><th>Memorial piece</th><th>Option</th><th>Price</th></tr></thead>
      <tbody>{mrows}</tbody></table></div>
  </div>
</section>
<section class="section-tight">
  <div class="wrap">
    <h2 class="h2">Felted Portraits</h2>
    <p class="muted" style="max-width:620px">Handmade to order from your photos — the final quotation depends on pet size and design complexity.</p>
    <div class="mt-5" style="overflow-x:auto"><table class="table">
      <thead><tr><th>Keepsake</th><th>Starting from</th><th>What's included</th></tr></thead>
      <tbody>{rows}</tbody></table></div>
  </div>
</section>
<section class="section band-grey">
  <div class="wrap split">
    <div>
      <p class="eyebrow">Every Order Includes</p>
      <ul class="checks">
        <li>Design review of your pet photos (custom pieces)</li>
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
        title="Pricing: Pet Memorial Wind Chime, Suncatcher, Urn & Felted Portraits | Again Paws",
        desc="Fixed prices for the Memorial Collection — wind chime $39, pet portrait suncatcher $31–$37, memorial garden stone $23.50, cremation urn $28.50, 55-piece offering set $24.80 — plus felted portrait reference prices.",
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
                    'Custom Pet Memorial Wind Chime ($39)', 'Custom Pet Portrait Window Suncatcher ($31–$37)',
                    'Pet Memorial Garden Stone ($23.50)', 'Classic Square Pet Cremation Urn ($28.50)',
                    'Pet Memorial Offering Set — 55 pieces ($24.80)', 'Business & Wholesale Cooperation',
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

def build_cart():
    body = f"""
<main>
<section class="section-tight">
  <div class="wrap">
    <p class="eyebrow">Bag &amp; Checkout</p>
    <h1 class="h1">Your bag.</h1>
    <p class="lead" style="max-width:620px">Fixed-price pieces go straight from the workshop to you. Felted portraits and engraving are still quoted by hand.</p>
    <div class="cart-layout">
      <div id="cartApp" aria-live="polite">
        <div class="cart-empty"><p class="lead">Loading your bag…</p></div>
      </div>
      <aside id="cartSide" class="cart-side" hidden></aside>
    </div>
    <noscript><div class="notice mt-6">Checkout needs JavaScript. Email
      <a href="mailto:q8461994@gmail.com">q8461994@gmail.com</a> or message us on
      <a href="https://wa.me/8613064191721">WhatsApp</a> and we will take the order by hand.</div></noscript>
  </div>
</section>
</main>"""
    page("cart/index.html", shell(
        title="Your Bag | Again Paws",
        desc="Review your bag and pay securely with PayPal — card or PayPal balance.",
        canonical=f"{SITE}/cart/", active=None, body=body, robots="noindex, follow"))

def build_thank_you():
    body = f"""
<main>
<section class="section-tight">
  <div class="wrap measure-c">
    <p class="eyebrow">Order Confirmed</p>
    <h1 class="h1">Thank you. It is in good hands.</h1>
    <p class="lead">Your payment went through and the order is with us.</p>
    <div class="card mt-5">
      <div class="sum-row"><span>Order number</span><b id="okOrder">—</b></div>
      <div class="sum-row"><span>Paid</span><b id="okTotal">—</b></div>
      <div id="okItems"></div>
      <p class="cart-mini mb-0">A PayPal receipt is on its way to the email on your PayPal account.</p>
    </div>
    <h2 class="h2 mt-7">What happens next</h2>
    <ul class="checks">
      <li>We check the order and confirm any personalisation by email within one working day.</li>
      <li>Your piece is made or packed, then shipped with tracking.</li>
      <li>Memorial Collection: 3–10 working days before dispatch. Felted portraits: 2–4 weeks.</li>
      <li>You get a tracking number by email as soon as it leaves us.</li>
    </ul>
    <p class="mt-5">Need to add a name, a date, a photo or a gift note? Reply to your PayPal receipt or
      <a href="/contact/">message us</a> with the order number above — it attaches to the same order.</p>
    <div class="btn-row">
      <a class="btn btn-stone" href="/products/#memorial">Back to the collection</a>
      <a class="btn btn-outline-stone" href="/guides/">Read the guides</a>
    </div>
  </div>
</section>
</main>
<script>
(function(){{
  var q = new URLSearchParams(location.search);
  var id = q.get('order'), tot = q.get('total');
  if (id) document.getElementById('okOrder').textContent = id;
  if (tot) document.getElementById('okTotal').textContent = '$' + Number(tot).toFixed(2);
  try {{
    var last = JSON.parse(localStorage.getItem('ap_last_order_v1') || 'null');
    if (!last || !last.items || !last.items.length) return;
    if (!tot && last.total) document.getElementById('okTotal').textContent = '$' + Number(last.total).toFixed(2);
    document.getElementById('okItems').innerHTML = '<div class="sum-list mt-4">' + last.items.map(function (i) {{
      return '<div class="sum-row"><span>' + i.qty + ' × ' + i.name + (i.variant ? ' · ' + i.variant : '') + '</span><span>$' + ((i.price * i.qty) / 100).toFixed(2) + '</span></div>';
    }}).join('') + '</div>';
  }} catch (e) {{}}
}})();
</script>"""
    page("thank-you/index.html", shell(
        title="Order Confirmed | Again Paws",
        desc="Your Again Paws order is confirmed. Here is what happens next.",
        canonical=f"{SITE}/thank-you/", active=None, body=body, robots="noindex, nofollow"))

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
    # peel off any wrappers added by previous runs (they nest one level per build,
    # and each .wrap adds 24px of padding — eight levels destroys mobile layout)
    main_html = main_html.strip()
    peel = re.compile(
        r'^<section class="section-tight">\s*<div class="wrap">\s*<div class="prose">(.*)</div>\s*</div>\s*</section>$',
        re.S)
    while True:
        m2 = peel.match(main_html)
        if not m2:
            break
        main_html = m2.group(1).strip()
    # wrap in exactly one prose container
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
    "/custom-pet-wind-chime/", "/custom-pet-window-suncatcher/", "/pet-memorial-garden-stone/",
    "/pet-cremation-urn/", "/pet-memorial-offering-set/",
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

> Handmade pet keepsakes and memorials: needle-felted portraits, plus the Memorial Collection — custom photo wind chimes, custom window suncatchers, memorial garden stones, cremation urns and a 55-piece memorial offering set. Made to order, shipped worldwide.

Fixed prices: wind chime $39 · suncatcher $31–$37 by size · memorial garden stone $23.50 · cremation urn $28.50 · 55-piece offering set $24.80. Felted portraits: reference prices $87–$477.

- [Home](https://againpaws.vip/): custom pet keepsakes and memorials
- [Products](https://againpaws.vip/products/): full collection
- [Custom Pet Memorial Wind Chime ($39)](https://againpaws.vip/custom-pet-wind-chime/): engraved photo tag, natural or coffee wood, silver or black tubes
- [Custom Pet Portrait Window Suncatcher ($31–$37)](https://againpaws.vip/custom-pet-window-suncatcher/): stained-glass style portrait from your photo, 15/20/25 cm
- [Pet Memorial Garden Stone ($23.50)](https://againpaws.vip/pet-memorial-garden-stone/): four inscriptions, built-in photo window and planter top
- [Classic Square Pet Cremation Urn ($28.50)](https://againpaws.vip/pet-cremation-urn/): 18.5 × 14 × 11.5 cm, 1100 ml, four colours
- [Pet Memorial Offering Set — 55 pieces ($24.80)](https://againpaws.vip/pet-memorial-offering-set/): treats, grooming items and traditional paper offerings
- [Pricing](https://againpaws.vip/pricing/): all prices in one table
- [Customization](https://againpaws.vip/customization/): what can be customized from your pet photos
- [Process](https://againpaws.vip/process/): how an order goes from photo to finished piece
- [Guides](https://againpaws.vip/guides/): buying guides for custom pet memorials
- [FAQ](https://againpaws.vip/faq/): ordering, production and shipping answers
- [Contact](https://againpaws.vip/contact/): request a quote (email or WhatsApp)
"""

REDIRECTS = {
    "custom-pet-memorial-plaque": "pet-memorial-garden-stone",
    "custom-pet-urn": "pet-cremation-urn",
    "pet-farewell-remembrance-set": "pet-memorial-offering-set",
}

def build_redirects():
    for old, new in REDIRECTS.items():
        html_s = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<title>Redirecting | Again Paws</title>
<meta name="robots" content="noindex, follow"/>
<link rel="canonical" href="{SITE}/{new}/"/>
<meta http-equiv="refresh" content="0; url=/{new}/"/>
</head>
<body><p>This product has moved to <a href="/{new}/">/{new}/</a>.</p></body>
</html>
"""
        page(f"{old}/index.html", html_s)

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
    build_cart(); build_thank_you()
    for rel in RESKIN:
        reskin(rel)
    build_redirects(); build_sitemap(); build_llms()
    print("DONE")
