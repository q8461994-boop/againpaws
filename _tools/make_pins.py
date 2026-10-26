# -*- coding: utf-8 -*-
"""生成 Pinterest Pin 图 1000x1500（2:3）：产品图 cover 裁切 + 顶部标题 + 底部品牌条。"""
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import pathlib, sys

SRC = pathlib.Path(r"C:/Users/16554/WorkBuddy/2026-10-23-10-20-59/againpaws/images")
OUT = pathlib.Path(r"C:/Users/16554/WorkBuddy/2026-10-23-10-20-59/deliverables/pinterest-pins")
OUT.mkdir(parents=True, exist_ok=True)

W, H = 1000, 1500
BAND = 250          # 顶部标题区
FOOT = 120          # 底部品牌条
PHOTO_H = H - BAND - FOOT

FONT_BOLD = r"C:/Windows/Fonts/arialbd.ttf"
FONT = r"C:/Windows/Fonts/arial.ttf"
f_title = ImageFont.truetype(FONT_BOLD, 62)
f_sub = ImageFont.truetype(FONT, 36)
f_foot = ImageFont.truetype(FONT_BOLD, 40)

CREAM = (247, 243, 235)
INK = (61, 58, 52)
ACCENT = (138, 109, 59)

def cover(img, w, h):
    r = max(w / img.width, h / img.height)
    im = img.resize((round(img.width * r), round(img.height * r)), Image.LANCZOS)
    x = (im.width - w) // 2
    y = (im.height - h) // 2
    return im.crop((x, y, x + w, y + h))

def wrap(draw, text, font, max_w):
    lines, line = [], ""
    for word in text.split():
        t = (line + " " + word).strip()
        if draw.textlength(t, font=font) <= max_w:
            line = t
        else:
            if line: lines.append(line)
            line = word
    if line: lines.append(line)
    return lines

def make_pin(name, img_file, title, subtitle):
    canvas = Image.new("RGB", (W, H), CREAM)
    photo = cover(Image.open(SRC / img_file).convert("RGB"), W, PHOTO_H)
    canvas.paste(photo, (0, BAND))

    d = ImageDraw.Draw(canvas)
    # 顶部标题
    y = 52
    for line in wrap(d, title, f_title, W - 80):
        d.text((40, y), line, font=f_title, fill=INK)
        y += 72
    y += 4
    for line in wrap(d, subtitle, f_sub, W - 80)[:2]:
        d.text((40, y), line, font=f_sub, fill=ACCENT)
        y += 44

    # 底部品牌条
    d.rectangle([0, H - FOOT, W, H], fill=INK)
    ft = "AGAIN PAWS"
    d.text((40, H - FOOT + (FOOT - 52) // 2), ft, font=f_foot, fill=CREAM)
    sub = "againpaws.vip"
    d.text((W - 40 - d.textlength(sub, font=f_sub), H - FOOT + (FOOT - 40) // 2), sub, font=f_sub, fill=(200, 192, 178))

    out = OUT / f"{name}.jpg"
    canvas.save(out, quality=90)
    print("saved", out.name)

PINS = [
    ("pin-1-mini-portrait", "product-1.webp",
     "Mini Portrait Custom Pet Keepsake",
     "Hand-felted from your photos \u00b7 from $87"),
    ("pin-2-headshot-frame", "product-2.webp",
     "Custom Felted Pet Portrait, Framed",
     "Your pet, sculpted in wool by hand"),
    ("pin-3-half-body", "product-3.webp",
     "Half-Body Needle-Felted Pet Replica",
     "Every marking matched from your photo"),
    ("pin-4-full-body", "product-4.webp",
     "Full-Body Custom Pet Portrait",
     "From $477 \u00b7 progress photos included"),
    ("pin-5-leather-style", "product-5.webp",
     "Leather-Style Pet Portrait Keepsake",
     "A one-of-a-kind tribute to your best friend"),
    ("pin-6-hero", "hero.webp",
     "Custom Pet Keepsakes From Photos",
     "Handmade needle-felted \u00b7 ships worldwide"),
]

for p in PINS:
    make_pin(*p)
print("done:", len(PINS), "pins ->", OUT)
