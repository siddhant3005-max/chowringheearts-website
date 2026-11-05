#!/usr/bin/env python3
"""Make responsive WebP (q82) + JPEG fallback copies of the product photos used
by the material, trade and about pages. Originals in assets/img are untouched.
Source = largest existing variant; longest side capped at 1600 px (never upscaled).
Output: assets/img/p/<id>-<width>.webp and .jpg
"""
import os, json
from PIL import Image
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'assets', 'img')
OUT = os.path.join(SRC, 'p')
IDS = ['horn-bowls-trio','horn-bowl-two-tone','horn-bowl-amber','horn-bowl-brass-stripes','horn-bowl-dots',
       'horn-bowl-gold-swirl','horn-plate-rings','horn-tray-brass-swirl','horn-spoon-diag','cat-horn-bowl',
       'cat-servers','cat-comb','bone-inlay-tray-stars','bone-inlay-box-floral','bone-inlay-box-cubes',
       'cat-bone-box','cat-resin-box','mop-bird-platter','mop-bird-dish','mop-dish-jewels','mop-flower-dish',
       'mop-oval-dish','mop-plate-silver','mop-spoon-diag','cat-shell-sp','cat-stool','cat-napkin-ring',
       'cat-magnifier','stand-front','stand-shelves']
STEPS = [480, 960, 1600]
BG = (255, 252, 246)  # --card, for the JPEG fallback of cut-out photos
def largest(i):
    best = None
    for f in os.listdir(SRC):
        if f.startswith(i + '-') and f.endswith('.webp') and f[len(i)+1:-5].isdigit():
            im = Image.open(os.path.join(SRC, f))
            if best is None or im.size[0] * im.size[1] > best[1]:
                best = (f, im.size[0] * im.size[1])
    return best[0]
os.makedirs(OUT, exist_ok=True)
manifest = {}
for i in IDS:
    src = largest(i)
    im = Image.open(os.path.join(SRC, src)); im.load()
    w, h = im.size
    cap = min(1600, max(w, h))
    widths = sorted({s for s in STEPS if s < cap * w / max(w, h)} | {round(cap * w / max(w, h))})
    out = []
    for tw in widths:
        th = round(h * tw / w)
        r = im.resize((tw, th), Image.LANCZOS) if tw != w else im.copy()
        r.save(os.path.join(OUT, f'{i}-{tw}.webp'), 'WEBP', quality=82, method=6)
        if r.mode in ('RGBA', 'LA'):
            bg = Image.new('RGB', r.size, BG); bg.paste(r, mask=r.split()[-1]); r = bg
        r.convert('RGB').save(os.path.join(OUT, f'{i}-{tw}.jpg'), 'JPEG', quality=82, optimize=True, progressive=True)
        out.append([tw, th])
    manifest[i] = {'src': src, 'sizes': out}
    print(i, src, out)
json.dump(manifest, open(os.path.join(ROOT, 'tools', 'images.json'), 'w'), indent=1)
