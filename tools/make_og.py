#!/usr/bin/env python3
"""1200x630 Open Graph images for the new pages, made from existing photos."""
import os
from PIL import Image, ImageDraw, ImageFilter
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(ROOT, 'assets', 'img'); OUT = os.path.join(ROOT, 'assets', 'og')
os.makedirs(OUT, exist_ok=True)
NAVY = (20, 24, 63)
def stage(name, files):
    W, H = 1200, 630
    bg = Image.new('RGB', (W, H), NAVY)
    glow = Image.new('L', (W, H), 0); ImageDraw.Draw(glow).ellipse((200, 40, 1000, 640), fill=110)
    glow = glow.filter(ImageFilter.GaussianBlur(120))
    bg = Image.composite(Image.new('RGB', (W, H), (211, 162, 78)), bg, glow.point(lambda v: v * 0.45))
    n = len(files); slot = W // n
    for k, f in enumerate(files):
        im = Image.open(os.path.join(IMG, f)).convert('RGBA')
        im.thumbnail((int(slot * 0.86), 470), Image.LANCZOS)
        x = k * slot + (slot - im.width) // 2; y = 330 - im.height // 2 + 20
        sh = Image.new('RGBA', im.size, (0, 0, 0, 0)); sh.putalpha(im.split()[-1].point(lambda v: v * 0.55))
        sh = sh.filter(ImageFilter.GaussianBlur(14))
        bg.paste((0, 0, 0), (x, y + 22), sh); bg.paste(im, (x, y), im)
    bg.save(os.path.join(OUT, name), 'JPEG', quality=84, optimize=True, progressive=True)
def photo(name, f):
    im = Image.open(os.path.join(IMG, f)).convert('RGB')
    w, h = im.size; th = int(w * 630 / 1200); top = int((h - th) * 0.12)
    im.crop((0, top, w, top + th)).resize((1200, 630), Image.LANCZOS).save(os.path.join(OUT, name), 'JPEG', quality=84, optimize=True, progressive=True)
stage('horn.jpg', ['horn-bowls-trio-1200.webp'])
stage('bone-inlay.jpg', ['bone-inlay-tray-stars-1200.webp'])
stage('mother-of-pearl.jpg', ['mop-bird-platter-1200.webp'])
stage('seashell.jpg', ['mop-spoon-diag-1200.webp', 'cat-napkin-ring-600.webp', 'cat-shell-sp-600.webp'])
stage('resin.jpg', ['cat-resin-box-600.webp'])
photo('trade.jpg', 'stand-front-1024.webp')
photo('about.jpg', 'stand-shelves-1440.webp')
