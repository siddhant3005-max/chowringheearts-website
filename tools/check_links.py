#!/usr/bin/env python3
"""Check every internal link, anchor, image, srcset and stylesheet in the site's HTML.
External links (mailto, wa.me, maps) are listed, not fetched."""
import os, re, sys
from html.parser import HTMLParser
from urllib.parse import urlparse, unquote
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGES = ['index.html', '404.html'] + [f'{d}/index.html' for d in ['horn','bone-inlay','mother-of-pearl','seashell','resin','trade','about']]
class P(HTMLParser):
    def __init__(s): super().__init__(); s.refs=[]; s.ids=set()
    def handle_starttag(s, t, a):
        a = dict(a)
        if 'id' in a: s.ids.add(a['id'])
        for k in ('href', 'src'):
            if a.get(k) and not (t == 'img' and a[k].startswith('data:')): s.refs.append((t, a[k]))
        for k in ('srcset', 'imagesrcset'):
            if a.get(k):
                for part in a[k].split(','): s.refs.append((t, part.strip().split(' ')[0]))
parsed = {}
for p in PAGES:
    x = P(); x.feed(open(os.path.join(ROOT, p), encoding='utf-8').read()); parsed[p] = x
def resolve(page, ref):
    u = urlparse(ref)
    if u.scheme or ref.startswith('//'): return None, None
    path = unquote(u.path)
    if not path: target = page
    elif path.startswith('/'): target = path.lstrip('/')
    else: target = os.path.normpath(os.path.join(os.path.dirname(page), path))
    if target == '' or target.endswith('/') or os.path.isdir(os.path.join(ROOT, target)): target = os.path.join(target, 'index.html')
    return os.path.normpath(target), u.fragment
bad = 0; n = 0; ext = set()
for p, x in parsed.items():
    for t, ref in x.refs:
        target, frag = resolve(p, ref)
        if target is None: ext.add(ref.split('?')[0]); continue
        n += 1
        if not os.path.isfile(os.path.join(ROOT, target)):
            print(f'BROKEN {p}: {ref}'); bad += 1; continue
        if frag and target in parsed and frag not in parsed[target].ids:
            print(f'BAD ANCHOR {p}: {ref}'); bad += 1
print(f'{n} internal references checked across {len(PAGES)} pages, {bad} broken')
print('external (not fetched):', *sorted(ext), sep='\n  ')
sys.exit(1 if bad else 0)
