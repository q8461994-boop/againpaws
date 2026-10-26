# -*- coding: utf-8 -*-
"""Import product photos from the owner's desktop folder into /images/products/.

Sources live in:  Desktop/独立站素材/<品类>/
Outputs go to:    /images/products/<slug>/<name>.webp  (max 1400px, q85)

Run:  python _tools/import_assets.py
"""
import os, sys
from PIL import Image, ImageFilter

DESK = os.path.expanduser("~/Desktop/独立站素材")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "images", "products")

def src(folder, name):
    return os.path.join(DESK, folder, name)

def load(folder, name):
    p = src(folder, name)
    if not os.path.exists(p):
        print("MISSING", p)
        return None
    im = Image.open(p)
    return im.convert("RGB")

def detail_crop(im, fx0, fy0, fx1, fy1):
    """Crop a detail region (fractions) — used to avoid captions baked into the frame."""
    W, H = im.size
    return im.crop((int(fx0 * W), int(fy0 * H), int(fx1 * W), int(fy1 * H)))

def save(im, slug, name, max_side=1400, square=False):
    if im is None:
        return
    if square:
        s = min(im.size)
        w, h = im.size
        im = im.crop(((w - s) // 2, (h - s) // 2, (w - s) // 2 + s, (h - s) // 2 + s))
    im.thumbnail((max_side, max_side), Image.LANCZOS)
    d = os.path.join(OUT, slug)
    os.makedirs(d, exist_ok=True)
    p = os.path.join(d, name + ".webp")
    im.save(p, "WEBP", quality=85, method=6)
    print("  ->", os.path.relpath(p, ROOT), im.size, f"{os.path.getsize(p)//1024}KB")

# ---------------------------------------------------------------- wind chime
def wind_chime():
    s = "custom-pet-wind-chime"
    print(s)
    save(load("宠物风铃", "去除图片右下角水印 (1).png"), s, "natural-silver-photo", square=True)
    save(load("宠物风铃", "去除图片右下角水印.png"), s, "natural-silver-silhouette", square=True)
    im = load("宠物风铃", "去除图片右下角水印 (3).png")
    if im:
        save(detail_crop(im, 0.06, 0.04, 0.99, 0.60), s, "coffee-silver-detail", square=True)
    im = load("宠物风铃", "去除图片右下角水印 (4).png")
    if im:
        save(detail_crop(im, 0.06, 0.04, 0.99, 0.60), s, "coffee-black-detail", square=True)

# --------------------------------------------------------------- suncatcher
def suncatcher():
    s = "custom-pet-window-suncatcher"
    print(s)
    save(load("宠物窗饰", "主图-5.jpg"), s, "pet-portrait", square=True)
    save(load("宠物窗饰", "主图-4.jpg"), s, "custom-from-photo", square=True)
    save(load("宠物窗饰", "主图-3.jpg"), s, "in-window", square=True)

# -------------------------------------------------------------- garden stone
def stone():
    s = "pet-memorial-garden-stone"
    print(s)
    save(load("宠物墓碑", "主图-3.jpg"), s, "forever", square=True)
    save(load("宠物墓碑", "主图-4.jpg"), s, "companion", square=True)
    save(load("宠物墓碑", "主图-2.jpg"), s, "in-my-heart", square=True)
    save(load("宠物墓碑", "主图-1.jpg"), s, "angel-heart", square=True)
    save(load("宠物墓碑", "主图-5.jpg"), s, "angel-heart-front", square=True)

# ----------------------------------------------------------------------- urn
def urn():
    s = "pet-cremation-urn"
    print(s)
    save(load("宠物骨灰盒", "去除图片右下角水印 (5).png"), s, "pink", square=True)
    save(load("宠物骨灰盒", "去除图片右下角水印 (3).png"), s, "pink-lifestyle", square=True)
    save(load("宠物骨灰盒", "去除图片右下角水印 (6).png"), s, "white", square=True)
    save(load("宠物骨灰盒", "去除图片右下角水印 (7).png"), s, "black", square=True)
    save(load("宠物骨灰盒", "去除图片右下角水印 (4).png"), s, "black-lifestyle", square=True)
    save(load("宠物骨灰盒", "去除图片右下角水印 (8).png"), s, "grey", square=True)
    save(load("宠物骨灰盒", "去除图片右下角水印 (1).png"), s, "grey-lifestyle", square=True)

# ------------------------------------------------------------------ offering set
def offering():
    s = "pet-memorial-offering-set"
    print(s)
    save(load("宠物葬品", "主图-5.jpg"), s, "set-layout", square=True)
    save(load("宠物葬品", "去除图片右下角水印 (4).png"), s, "rainbow-bridge", square=True)

if __name__ == "__main__":
    for fn in (wind_chime, suncatcher, stone, urn, offering):
        fn()
    print("DONE")
