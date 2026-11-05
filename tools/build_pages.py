#!/usr/bin/env python3
"""Build the material, trade, about and 404 pages from one template.

Run from the repository root:  python3 tools/build_pages.py
Writes horn/index.html, bone-inlay/index.html, mother-of-pearl/index.html,
seashell/index.html, resin/index.html, trade/index.html, about/index.html,
404.html and sitemap.xml. Image sizes come from tools/images.json, written by
tools/make_images.py. Product names and captions are the ones already used on
the home page (index.html); nothing here should add products, codes or prices.
"""
import json, os, html
from urllib.parse import quote

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = 'https://chowringheearts.com'
EMAIL = 'info@chowringheearts.com'
WA = '919830922999'
LASTMOD = '2026-11-05'
IMG = json.load(open(os.path.join(ROOT, 'tools', 'images.json')))

def e(s):
    return html.escape(s, quote=True)

# ---------------------------------------------------------------- images
def srcset(i, ext):
    return ', '.join(f'/assets/img/p/{i}-{w}.{ext} {w}w' for w, h in IMG[i]['sizes'])

def pic(i, alt, sizes, eager=False):
    w, h = IMG[i]['sizes'][-1]
    mid = [s for s in IMG[i]['sizes'] if s[0] >= 480] or IMG[i]['sizes']
    fb = mid[0][0]
    load = 'loading="eager" fetchpriority="high"' if eager else 'loading="lazy"'
    return (f'<picture><source type="image/webp" srcset="{srcset(i, "webp")}" sizes="{sizes}">'
            f'<img src="/assets/img/p/{i}-{fb}.jpg" srcset="{srcset(i, "jpg")}" sizes="{sizes}" '
            f'width="{w}" height="{h}" alt="{e(alt)}" {load} decoding="async"></picture>')

# ---------------------------------------------------------------- icons
I_MAIL = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><rect x="3" y="5" width="18" height="14" rx="2.5"/><path d="m4 7 8 6 8-6"/></svg>'
I_WA = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><path d="M20 12a8 8 0 0 1-11.7 7.1L4 20l1-4.1A8 8 0 1 1 20 12Z"/><path d="M9 10.5h6M9 13.5h4"/></svg>'
I_MENU = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><path d="M4 7h16M4 12h16M4 17h16"/></svg>'

def mailto(subject, body):
    return f'mailto:{EMAIL}?subject={quote(subject)}&amp;body={quote(body)}'

def wa(text):
    return f'https://wa.me/{WA}?text={quote(text)}'

def ctas(p, cls='cta-row'):
    return (f'<div class="{cls}"><a class="btn btn-gold" href="{mailto(p["mail_subject"], MAIL_BODY)}">{I_MAIL}Email info@chowringheearts.com</a>'
            f'<a class="btn btn-line" href="{wa(p["wa_text"])}" target="_blank" rel="noopener">{I_WA}WhatsApp +91 98309 22999</a></div>')

MAIL_BODY = ('Hello Chowringhee Arts,\n\nPieces I am interested in:\n\nQuantity per design:\n\n'
             'Company and country:\n\nMy market (importer, wholesaler, retail chain, hotel supplier, buying agent):\n')

# ---------------------------------------------------------------- shared data
MATERIALS = [
    ('horn', 'Buffalo horn', 'Bowls, trays, spoons and servers', 'horn-bowl-two-tone', 'Two-tone horn bowl'),
    ('bone-inlay', 'Bone inlay', 'Boxes and trays', 'bone-inlay-box-floral', 'Floral bone inlay box'),
    ('mother-of-pearl', 'Mother-of-pearl', 'Carved dishes, trays and spoons', 'mop-flower-dish', 'Carved mother-of-pearl flower dish'),
    ('seashell', 'Seashell', 'Spoons, napkin rings, desk pieces', 'cat-napkin-ring', 'Shell napkin ring with a rope loop'),
    ('resin', 'Resin &amp; terrazzo', 'Boxes and tableware', 'cat-resin-box', 'Checkerboard resin and bone boxes'),
]
NAV = [('/horn/', 'Horn'), ('/bone-inlay/', 'Bone inlay'), ('/mother-of-pearl/', 'Mother-of-pearl'),
       ('/seashell/', 'Seashell'), ('/resin/', 'Resin'), ('/trade/', 'How we trade'), ('/about/', 'About')]

ORG = {
    '@type': 'Organization', '@id': SITE + '/#org', 'name': 'Chowringhee Arts', 'url': SITE + '/',
    'logo': SITE + '/assets/logo-ink.svg', 'image': SITE + '/assets/og-v3.jpg',
    'email': EMAIL, 'telephone': '+91-98309-22999',
    'address': {'@type': 'PostalAddress', 'streetAddress': '75C Park Street', 'addressLocality': 'Kolkata',
                'postalCode': '700016', 'addressRegion': 'West Bengal', 'addressCountry': 'IN'},
    'contactPoint': {'@type': 'ContactPoint', 'contactType': 'sales', 'email': EMAIL, 'telephone': '+91-98309-22999'},
    'memberOf': {'@type': 'Organization', 'name': 'Export Promotion Council for Handicrafts (EPCH)'},
    'description': ('Kolkata export house, in business for 10 years, making handmade homeware in buffalo horn, '
                    'bone inlay, mother-of-pearl, seashell and resin for trade buyers. Horn and bone are by-products '
                    'of cattle farming; no animal is harmed for its products.'),
}

def jsonld(p):
    graph = [ORG]
    crumbs = [{'@type': 'ListItem', 'position': 1, 'name': 'Home', 'item': SITE + '/'}]
    if p['path'] != '/':
        crumbs.append({'@type': 'ListItem', 'position': 2, 'name': p['crumb'], 'item': SITE + p['path']})
    graph.append({'@type': 'BreadcrumbList', 'itemListElement': crumbs})
    if p.get('faq'):
        graph.append({'@type': 'FAQPage', 'mainEntity': [
            {'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a_plain}}
            for q, a, a_plain in p['faq']]})
    return json.dumps({'@context': 'https://schema.org', '@graph': graph}, ensure_ascii=False, indent=1)

# ---------------------------------------------------------------- chrome
def head(p):
    canon = SITE + p['path']
    og = p.get('og', 'og-v3.jpg')
    robots = '<meta name="robots" content="noindex">\n' if p.get('noindex') else ''
    canon_tag = '' if p.get('noindex') else f'<link rel="canonical" href="{canon}">\n'
    preload = ''
    if p.get('hero_img'):
        i = p['hero_img']
        preload = (f'<link rel="preload" as="image" type="image/webp" imagesrcset="{srcset(i, "webp")}" '
                   f'imagesizes="{p.get("hero_sizes", HERO_SIZES)}" fetchpriority="high">\n')
    ld = '' if p.get('noindex') else f'<script type="application/ld+json">\n{jsonld(p)}\n</script>\n'
    return f'''<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{p["title"]}</title>
<meta name="description" content="{e(p["desc"])}">
{robots}{canon_tag}<meta name="theme-color" content="#14183F">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/assets/favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Chowringhee Arts">
<meta property="og:locale" content="en_GB">
<meta property="og:title" content="{p["og_title"]}">
<meta property="og:description" content="{e(p["desc"])}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{SITE}/assets/og/{og}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{e(p["og_alt"])}">
<meta name="twitter:card" content="summary_large_image">
<link rel="stylesheet" href="/assets/site.css">
{preload}<link rel="preload" href="/assets/fonts/cormorant-garamond-latin-500-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/poppins-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>
<script>document.documentElement.className+=' js';</script>
{ld}</head>'''

def header(p):
    cur = lambda href: ' aria-current="page"' if href == p['path'] else ''
    lnks = '\n      '.join(f'<a class="lnk" href="{h}"{cur(h)}>{t}</a>' for h, t in NAV)
    mats = '\n      '.join(f'<a href="/{slug}/"{cur("/" + slug + "/")}>{name}</a>' for slug, name, *_ in MATERIALS)
    return f'''<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site-head" id="top">
  <div class="wrap">
    <a class="brand" href="/" aria-label="Chowringhee Arts home"><img src="/assets/logo-gold.svg" alt="Chowringhee Arts" width="112" height="50"></a>
    <nav class="nav" aria-label="Main">
      {lnks}
      <a class="btn btn-gold btn-sm" href="#enquire">Enquire</a>
      <button class="menu-btn" type="button" aria-expanded="false" aria-controls="menu">{I_MENU}<span class="sr">Menu</span></button>
    </nav>
  </div>
  <div class="menu" id="menu" hidden>
    <div class="wrap">
      <a href="/">Home</a>
      <p class="menu-k">Materials</p>
      {mats}
      <p class="menu-k">Working with us</p>
      <a href="/trade/"{cur("/trade/")}>How we trade</a>
      <a href="/about/"{cur("/about/")}>About us</a>
      <a href="#enquire">Contact</a>
    </div>
  </div>
</header>
'''

FOOTER = f'''<footer class="site-foot on-navy">
  <div class="wrap foot-top">
    <div class="foot-brand">
      <img src="/assets/logo-gold.svg" alt="Chowringhee Arts" width="300" height="134" loading="lazy">
      <p>Handmade homeware in buffalo horn, bone inlay, mother-of-pearl, seashell and resin, for the trade. No animal is harmed for our products. 75C Park Street, Kolkata.</p>
      <div class="foot-ctas">
        <a class="btn btn-gold btn-sm" href="mailto:{EMAIL}?subject=Enquiry%20from%20chowringheearts.com">{I_MAIL}Email us</a>
        <a class="btn btn-ghost btn-sm" href="{wa('Hello Chowringhee Arts, I found you on your website.')}" target="_blank" rel="noopener">{I_WA}WhatsApp</a>
      </div>
    </div>
    <div class="foot-cols">
      <div>
        <h2 class="foot-h">Contact</h2>
        <ul>
          <li><b>Email</b><a href="mailto:{EMAIL}?subject=Enquiry%20from%20chowringheearts.com">{EMAIL}</a></li>
          <li><b>WhatsApp · Phone</b><a href="{wa('Hello Chowringhee Arts, I found you on your website.')}" target="_blank" rel="noopener">+91 98309 22999</a></li>
          <li><b>Office</b>75C Park Street, Kolkata 700016, India</li>
        </ul>
      </div>
      <div>
        <h2 class="foot-h">Materials</h2>
        <ul>
          <li><a href="/horn/">Buffalo horn</a></li>
          <li><a href="/bone-inlay/">Bone inlay</a></li>
          <li><a href="/mother-of-pearl/">Mother-of-pearl</a></li>
          <li><a href="/seashell/">Seashell</a></li>
          <li><a href="/resin/">Resin &amp; terrazzo</a></li>
        </ul>
      </div>
      <div>
        <h2 class="foot-h">Company</h2>
        <ul>
          <li><a href="/">Home</a></li>
          <li><a href="/trade/">How we trade</a></li>
          <li><a href="/about/">About us</a></li>
          <li><b>Next fair</b>IHGF Delhi Fair Spring 2027, 15–19 March</li>
        </ul>
      </div>
    </div>
  </div>
  <div class="foot-bar">
    <div class="wrap">
      <span>© 2026 Chowringhee Arts · Kolkata, India · Member of EPCH</span>
      <a href="#top">Back to top ↑</a>
    </div>
  </div>
</footer>
<script>
(function(){{var b=document.querySelector('.menu-btn'),m=document.getElementById('menu'),h=document.querySelector('.site-head');
if(!b||!m)return;function s(o){{m.hidden=!o;b.setAttribute('aria-expanded',String(o));h.classList.toggle('menu-open',o);}}
b.addEventListener('click',function(){{s(m.hidden);}});m.addEventListener('click',function(e){{if(e.target.closest('a'))s(false);}});
document.addEventListener('keydown',function(e){{if(e.key==='Escape'&&!m.hidden){{s(false);b.focus();}}}});}})();
</script>
</body>
</html>
'''

HERO_SIZES = '(max-width:900px) 84vw, 520px'
TILE_SIZES = '(max-width:640px) 40vw, (max-width:980px) 30vw, 300px'

def crumbs(p):
    return (f'<nav class="crumbs" aria-label="Breadcrumb"><ol><li><a href="/">Home</a></li>'
            f'<li aria-current="page">{p["crumb"]}</li></ol></nav>')

def sub_hero(p, photo=False):
    facts = ''.join(f'<li>{f}</li>' for f in p['hero_facts'])
    cls = 'sub-stage photo' if photo else 'sub-stage'
    return f'''  <section class="sub-hero on-navy" aria-labelledby="page-title">
    <div class="wrap sub-grid">
      <div>
        {crumbs(p)}
        <p class="eyebrow">{p["eyebrow"]}</p>
        <h1 id="page-title">{p["h1"]}</h1>
        <p class="lede">{p["lede"]}</p>
        {ctas(p)}
        <ul class="hero-facts">{facts}</ul>
      </div>
      <figure class="{cls}">{pic(p["hero_img"], p["hero_alt"], p.get("hero_sizes", HERO_SIZES), eager=True)}<figcaption>{p["hero_cap"]}</figcaption></figure>
    </div>
  </section>
'''

def make_list(items):
    return '<ul class="make">' + ''.join(f'<li><b>{t}</b><span>{d}</span></li>' for t, d in items) + '</ul>'

def spec(rows):
    return '<dl class="spec">' + ''.join(f'<div><dt>{k}</dt><dd>{v}</dd></div>' for k, v in rows) + '</dl>'

def gallery(tiles):
    out = []
    for i, title, sub in tiles:
        alt = f'{title} — {sub}' if sub else title
        out.append(f'<figure class="tile"><div class="ph">{pic(i, alt, TILE_SIZES)}</div>'
                   f'<figcaption><span class="t">{e(title)}' + (f'<small>{e(sub)}</small>' if sub else '') + '</span></figcaption></figure>')
    return '<div class="gallery g3">' + ''.join(out) + '</div>'

def faq_html(items):
    return '<div class="faq">' + ''.join(f'<details><summary>{e(q)}</summary><p>{a}</p></details>' for q, a, _ in items) + '</div>'

def next_step(p):
    return f'''  <section id="enquire" class="band" aria-labelledby="next-title">
    <div class="wrap">
      <div class="next on-navy">
        <p class="eyebrow">Next step</p>
        <h2 id="next-title">{p["next_h"]}</h2>
        <p>{p["next_p"]}</p>
        {ctas(p)}
        <p>Office: 75C Park Street, Kolkata 700016, India. We reply with photos, sizes and ex-works prices for the pieces you ask about.</p>
      </div>
    </div>
  </section>
'''

def other_links(p):
    lis = []
    for slug, name, sub, img, alt in MATERIALS:
        if '/' + slug + '/' == p['path']:
            continue
        lis.append(f'<li><a href="/{slug}/"><span class="th">{pic(img, alt, "64px")}</span><span><b>{name}</b><small>{sub}</small></span></a></li>')
    if p['path'] != '/trade/':
        lis.append('<li><a href="/trade/"><span class="th">' + pic('stand-front', 'The Chowringhee Arts stand at IHGF Delhi Fair, Autumn 2025', '64px') + '</span><span><b>How we trade</b><small>Terms, samples and lead times</small></span></a></li>')
    if p['path'] != '/about/':
        lis.append('<li><a href="/about/"><span class="th">' + pic('stand-shelves', 'Shelves of bone inlay, horn and shell pieces on the Chowringhee Arts stand', '64px') + '</span><span><b>About us</b><small>10 years, 4,000+ designs, Kolkata</small></span></a></li>')
    return f'''  <section class="band alt" aria-labelledby="more-title">
    <div class="wrap">
      <div class="sec-head"><div><p class="eyebrow">Also from Chowringhee Arts</p><h2 id="more-title">More to <em>look at.</em></h2></div></div>
      <ul class="mat-links">{''.join(lis)}</ul>
    </div>
  </section>
'''

# ---------------------------------------------------------------- common FAQ answers
def faq_common(material_q, material_a, custom_a):
    raw = [
        ('What is the lead time?',
         'Orders are ready 30 to 45 days after we receive the 50% advance. The balance is due before dispatch.'),
        ('Is there a minimum order quantity?',
         'Prices get better from 100 pieces and again from 300 pieces per design. Tell us the quantities you have in mind and we will quote for those.'),
        ('Can I order samples?',
         'Yes. Samples are made on request and charged at the piece price.'),
        ('Can you make custom sizes, colours or finishes?', custom_a),
        ('How are the pieces packed?',
         'Tell us how your market needs goods packed and labelled when you enquire, and we will confirm it with the quote.'),
        (material_q, material_a),
        ('Do you send a price list or catalogue?',
         'No. We sell to the trade only and do not publish prices or send full catalogues. Tell us the pieces you are interested in and we send photos, sizes and ex-works Kolkata prices for those.'),
    ]
    return [(q, e(a), a) for q, a in raw]

TERMS = [
    ('Prices', 'Quoted ex-works Kolkata, in US dollars, for the pieces you ask about'),
    ('Volume', 'Better prices from 100 and from 300 pieces per design'),
    ('Samples', 'On request, charged at piece price'),
    ('Payment', '50% advance, balance before dispatch'),
    ('Lead time', 'Ready 30 to 45 days after the advance'),
]

# ---------------------------------------------------------------- pages
PAGES = []

PAGES.append(dict(
    slug='horn', path='/horn/', crumb='Buffalo horn',
    title='Buffalo Horn Serveware &amp; Cutlery Exporter, India | Chowringhee Arts',
    og_title='Buffalo horn serveware and cutlery — Chowringhee Arts, Kolkata',
    desc='Kolkata maker and exporter of real buffalo horn bowls, trays, plates, spoons and salad servers, many finished with brass. Trade only, ex-works Kolkata.',
    og='horn.jpg', og_alt='Three buffalo horn bowls: natural, dotted and brass-striped',
    targets=['buffalo horn serveware manufacturer India', 'horn and brass cutlery exporter', 'horn bowls wholesale', 'handicraft exporter Kolkata'],
    eyebrow='Buffalo horn · for the trade',
    h1='Buffalo horn serveware and cutlery, <em>made by hand in Kolkata</em>',
    lede='Bowls, trays, plates, spoons and salad servers in real buffalo horn, never faux, many of them finished with brass. We make them for importers, wholesalers, retail chains and hotel suppliers, and sell to the trade only.',
    hero_img='horn-bowls-trio', hero_alt='Horn bowls — three finishes — Natural, dotted and brass-striped',
    hero_cap='Horn bowls — natural, dotted and brass-striped',
    hero_facts=['Real buffalo horn', 'Handmade', 'Ex-works Kolkata', 'Ready 30–45 days'],
    mail_subject='Buffalo horn enquiry', wa_text='Hello Chowringhee Arts, I am interested in your buffalo horn pieces.',
    make_lede='Horn is our largest range. These are the kinds of piece we make; we send photos and sizes of current designs when you tell us what you need.',
    make=[('Bowls', 'Natural, two-tone, dotted, striped and amber horn; some inlaid with shell dots, many finished with brass.'),
          ('Trays and plates', 'Horn trays and plates, including a swirl-pattern tray and a plate with a ring pattern.'),
          ('Spoons and servers', 'Long-handled horn spoons and salad servers, including servers with bone inlay handles.'),
          ('Cutlery', 'Spoons, forks and knives in horn, with handles in plain horn or combined with other materials to your specification.'),
          ('Combs', 'Horn combs, including a heart-shaped comb, and other hair accessories in horn, bone and brass.'),
          ('Desk and table pieces', 'Magnifiers and other desk pieces with horn handles, and horn napkin rings.')],
    made_h='How horn is <em>made and finished</em>',
    made=['<p>We use <strong>real buffalo horn</strong>, a by-product of cattle farming. It is real horn, never faux, and no animal is harmed for our products.</p>',
          '<p>Each piece is cut, shaped and polished by hand by our karigars until the natural grain shows. Some pieces are then inlaid, for example with shell dots, and many are finished with brass.</p>',
          '<p>Natural horn has its own grain and colour, from dark to amber to two-tone, so no two pieces are exactly the same. Expect the grain and pattern to vary a little across an order.</p>'],
    sizes_rows=[('Sizes', 'We send sizes with photos and prices for the pieces you ask about. Custom sizes are made to your specification.'),
                ('Finishes', 'Natural, two-tone, dotted, striped or brass-finished, or a finish you specify.')] + TERMS,
    gallery=[('horn-bowls-trio', 'Horn bowls — three finishes', 'Natural, dotted and brass-striped'),
             ('horn-bowl-brass-stripes', 'Horn bowl', 'Striped pattern'),
             ('horn-bowl-dots', 'Horn bowl', 'Dotted pattern'),
             ('horn-tray-brass-swirl', 'Horn tray', 'Swirl pattern'),
             ('horn-plate-rings', 'Horn plate', 'Ring pattern'),
             ('horn-spoon-diag', 'Horn spoon', 'Long handle'),
             ('cat-servers', 'Horn salad servers', 'With bone inlay handles'),
             ('horn-bowl-two-tone', 'Horn bowl', 'Natural two-tone horn'),
             ('horn-bowl-amber', 'Amber horn bowl', ''),
             ('cat-horn-bowl', 'Horn bowl', 'With inlaid shell dots'),
             ('horn-bowl-gold-swirl', 'Patterned horn bowl', ''),
             ('cat-comb', 'Heart-shaped horn comb', '')],
    faq=faq_common('Where does the horn come from?',
                   'It is real buffalo horn, never faux. The horn is a by-product of cattle farming and no animal is harmed for our products.',
                   'Yes. We make sizes, colours and finishes to your specification, including brass finishes. Send a drawing, photo or reference piece with the quantity.'),
    next_h='Tell us which horn pieces <em>you need.</em>',
    next_p='Write to us or send a WhatsApp message with the pieces you are interested in (a photo or a description is enough), the quantity per design and your market. We reply with photos, sizes and ex-works prices for those pieces.',
))

PAGES.append(dict(
    slug='bone-inlay', path='/bone-inlay/', crumb='Bone inlay',
    title='Bone Inlay Boxes &amp; Trays Wholesale, India | Chowringhee Arts',
    og_title='Bone inlay boxes and trays, wholesale — Chowringhee Arts, Kolkata',
    desc='Handmade bone inlay boxes and trays from Kolkata for importers, wholesalers and retail chains. Floral, geometric and striped patterns; custom sizes and colours.',
    og='bone-inlay.jpg', og_alt='A black and white bone inlay tray with a pattern of stars and moons',
    targets=['bone inlay boxes wholesale India', 'bone inlay tray manufacturer', 'bone inlay exporter Kolkata', 'IHGF exhibitor horn bone shell'],
    eyebrow='Bone inlay · for the trade',
    h1='Bone inlay boxes and trays, <em>wholesale from Kolkata</em>',
    lede='Boxes and trays inlaid by hand with small pieces of bone, in floral, geometric and striped patterns. Made for importers, wholesalers, retail chains and buying agents.',
    hero_img='bone-inlay-tray-stars', hero_alt='Close-up of a bone inlay tray: small pieces of bone set by hand into a pattern of stars and moons',
    hero_cap='Bone inlay, set by hand',
    hero_facts=['Set by hand', 'Bone from cattle farming', 'Custom colours', 'Ready 30–45 days'],
    mail_subject='Bone inlay enquiry', wa_text='Hello Chowringhee Arts, I am interested in your bone inlay pieces.',
    make_lede='Bone inlay suits boxes, trays and anything with a flat surface to decorate. These are the kinds of piece we make.',
    make=[('Boxes', 'Bone inlay boxes in floral, geometric and striped patterns, including checkerboard boxes in resin and bone.'),
          ('Trays', 'Bone inlay trays, such as a black and white tray with a pattern of stars and moons.'),
          ('Inlaid handles', 'Bone inlay used on the handles of horn salad servers and other serveware.'),
          ('Stools and small furniture', 'Stools and small furniture with bone tops, made to order.'),
          ('Table accessories', 'Napkin rings, key rings and small boxes in bone, horn and shell.'),
          ('Combs', 'Combs and hair accessories in horn, bone and brass.')],
    made_h='How bone inlay is <em>made</em>',
    made=['<p>The bone we use is a <strong>by-product of cattle farming</strong>: material that would otherwise go to waste. No animal is harmed for our products.</p>',
          '<p>Our karigars cut the bone into small pieces and set them by hand, one piece at a time, into the pattern.</p>',
          '<p>Because every piece is set by hand, small differences in the pattern from one box or tray to the next are normal.</p>'],
    sizes_rows=[('Sizes', 'We send sizes with photos and prices for the pieces you ask about. Custom sizes are made to your specification.'),
                ('Colours and patterns', 'Black and white, floral, geometric and striped patterns shown here; other colours and patterns to your specification.')] + TERMS,
    gallery=[('bone-inlay-tray-stars', 'Bone inlay tray', 'Black and white pattern'),
             ('bone-inlay-box-floral', 'Bone inlay box', 'Floral pattern'),
             ('bone-inlay-box-cubes', 'Bone inlay box', 'Geometric pattern'),
             ('cat-bone-box', 'Striped bone inlay box', ''),
             ('cat-resin-box', 'Checkerboard resin and bone boxes', ''),
             ('cat-servers', 'Horn salad servers', 'With bone inlay handles')],
    faq=faq_common('Where does the bone come from?',
                   'The bone is a by-product of cattle farming, material that would otherwise go to waste. No animal is harmed for our products.',
                   'Yes. Sizes, colours and patterns are made to your specification. Send a drawing, photo or reference piece with the quantity.'),
    next_h='Tell us which bone inlay pieces <em>you need.</em>',
    next_p='Write to us or send a WhatsApp message with the boxes or trays you are interested in, the sizes and colours you want, the quantity per design and your market. We reply with photos and ex-works prices.',
))

PAGES.append(dict(
    slug='mother-of-pearl', path='/mother-of-pearl/', crumb='Mother-of-pearl',
    title='Mother of Pearl Tray &amp; Dish Manufacturer, India | Chowringhee Arts',
    og_title='Mother-of-pearl trays and dishes — Chowringhee Arts, Kolkata',
    desc='Carved mother-of-pearl dishes, trays, spoons and salt and pepper sets, handmade in Kolkata for the trade. Birds, flowers, stones and metal trim; custom finishes.',
    og='mother-of-pearl.jpg', og_alt='A mother-of-pearl dish carved as a bird',
    targets=['mother of pearl tray manufacturer', 'mother of pearl dish wholesale India', 'mother of pearl serveware exporter'],
    eyebrow='Mother-of-pearl · for the trade',
    h1='Mother-of-pearl trays and dishes, <em>carved by hand</em>',
    lede='Dishes and trays carved from shell into birds, flowers and fish, some set with stones or trimmed with metal. Made in Kolkata for importers, wholesalers, retail chains and hotel suppliers.',
    hero_img='mop-bird-platter', hero_alt='Mother-of-pearl dish carved as a bird',
    hero_cap='Mother-of-pearl dish carved as a bird',
    hero_facts=['Carved by hand', 'Each shell different', 'Custom finishes', 'Ready 30–45 days'],
    mail_subject='Mother-of-pearl enquiry', wa_text='Hello Chowringhee Arts, I am interested in your mother-of-pearl pieces.',
    make_lede='Mother-of-pearl works for serving dishes, trays and small table pieces. These are the kinds of piece we make.',
    make=[('Dishes', 'Carved as birds and flowers, engraved with fish, set with stones or trimmed with metal.'),
          ('Trays', 'Mother-of-pearl trays for serving and display.'),
          ('Spoons', 'Mother-of-pearl spoons, such as a spoon with an embossed metal handle. See also our <a href="/seashell/">seashell spoons</a>.'),
          ('Salt and pepper sets', 'Including a heart-shaped mother-of-pearl salt and pepper set.'),
          ('Pill boxes and small boxes', 'Small boxes and pill boxes in shell.'),
          ('Stools and small furniture', 'Round stools with a mother-of-pearl top, made to order.')],
    made_h='How mother-of-pearl is <em>made and finished</em>',
    made=['<p>Mother-of-pearl is the shimmering inner layer of the shell. Our karigars cut it, carve it into birds and flowers, and inlay it into dishes and serveware.</p>',
          '<p>Some dishes are engraved, some are set with stones and some are trimmed with metal. Every piece is finished by hand.</p>',
          '<p>Every shell has its own shimmer and colour, so no two pieces are exactly alike. Expect small differences across an order.</p>'],
    sizes_rows=[('Sizes', 'We send sizes with photos and prices for the pieces you ask about. Custom sizes are made to your specification.'),
                ('Finishes', 'Carved, engraved, set with stones or metal-trimmed, or a finish you specify.')] + TERMS,
    gallery=[('mop-bird-platter', 'Mother-of-pearl dish', 'Carved as a bird'),
             ('mop-flower-dish', 'Mother-of-pearl dish', 'Carved flower'),
             ('mop-dish-jewels', 'Mother-of-pearl dish', 'Set with stones'),
             ('mop-oval-dish', 'Mother-of-pearl dish', 'Engraved fish'),
             ('mop-bird-dish', 'Mother-of-pearl dish', 'Carved bird'),
             ('mop-plate-silver', 'Mother-of-pearl dish', 'Metal trim'),
             ('mop-spoon-diag', 'Mother-of-pearl spoon', 'Embossed metal handle'),
             ('cat-shell-sp', 'Mother-of-pearl salt and pepper set', 'Heart-shaped'),
             ('cat-stool', 'Round stool', 'With a mother-of-pearl top')],
    faq=faq_common('Where does the shell come from?',
                   'Ask us about the shell used in the pieces you are interested in and we will tell you for those pieces.',
                   'Yes. Sizes, finishes and trims are made to your specification. Send a drawing, photo or reference piece with the quantity.'),
    next_h='Tell us which mother-of-pearl pieces <em>you need.</em>',
    next_p='Write to us or send a WhatsApp message with the dishes, trays or spoons you are interested in, the quantity per design and your market. We reply with photos, sizes and ex-works prices.',
))

PAGES.append(dict(
    slug='seashell', path='/seashell/', crumb='Seashell',
    title='Seashell Caviar Spoons &amp; Shell Tableware Supplier | Chowringhee Arts',
    og_title='Seashell spoons and table pieces — Chowringhee Arts, Kolkata',
    desc='Shell spoons, caviar and serving spoons, napkin rings, salt and pepper sets and desk pieces, handmade in Kolkata. Trade only; custom sizes and finishes.',
    og='seashell.jpg', og_alt='A mother-of-pearl spoon with an embossed metal handle',
    targets=['seashell caviar spoons supplier', 'shell napkin rings wholesale', 'shell tableware supplier India'],
    eyebrow='Seashell · for the trade',
    h1='Seashell spoons and table pieces, <em>made by hand</em>',
    lede='Spoons, napkin rings, salt and pepper sets and desk pieces made with shell. Made in Kolkata for importers, wholesalers, retail chains, hotel suppliers and buying agents.',
    hero_img='mop-spoon-diag', hero_alt='Mother-of-pearl spoon — Embossed metal handle',
    hero_cap='Shell spoon with an embossed metal handle',
    hero_facts=['Handmade', 'Custom sizes', 'Samples on request', 'Ready 30–45 days'],
    mail_subject='Seashell enquiry', wa_text='Hello Chowringhee Arts, I am interested in your seashell pieces.',
    make_lede='Shell is cut, carved or inlaid. These are the kinds of piece we make with it.',
    make=[('Spoons', 'Shell spoons for serving, and small spoons for caviar, made to the size you need. The spoon shown has an embossed metal handle.'),
          ('Napkin rings', 'Shell napkin rings, such as a ring with a rope loop.'),
          ('Salt and pepper sets', 'Including a heart-shaped mother-of-pearl salt and pepper set.'),
          ('Dishes', 'Shell dishes, engraved or set with stones. See our <a href="/mother-of-pearl/">mother-of-pearl dishes and trays</a>.'),
          ('Desk pieces', 'Magnifying glasses with a shell and filigree handle, pen holders and paperweights.'),
          ('Table accessories', 'Key rings and small boxes in shell, horn and bone.')],
    made_h='How shell pieces are <em>made</em>',
    made=['<p>Shell is cut and carved by hand by our karigars, and inlaid into dishes and serveware. Some pieces are combined with metal, rope or filigree, as in the spoon, napkin ring and magnifier shown here.</p>',
          '<p>Every shell has its own shimmer and colour, so no two pieces are exactly alike. Expect small differences across an order.</p>',
          '<p>For spoons, tell us the length and bowl size you need. We make sizes to your specification.</p>'],
    sizes_rows=[('Sizes', 'We send sizes with photos and prices for the pieces you ask about. Custom sizes, including spoon lengths, are made to your specification.'),
                ('Finishes', 'Plain shell, metal handles, rope or filigree details, or a finish you specify.')] + TERMS,
    gallery=[('mop-spoon-diag', 'Mother-of-pearl spoon', 'Embossed metal handle'),
             ('cat-napkin-ring', 'Shell napkin ring', 'With a rope loop'),
             ('cat-magnifier', 'Magnifying glass', 'Shell and filigree handle'),
             ('cat-shell-sp', 'Mother-of-pearl salt and pepper set', 'Heart-shaped'),
             ('mop-oval-dish', 'Mother-of-pearl dish', 'Engraved fish'),
             ('mop-dish-jewels', 'Mother-of-pearl dish', 'Set with stones')],
    faq=faq_common('Where does the shell come from?',
                   'Ask us about the shell used in the pieces you are interested in and we will tell you for those pieces.',
                   'Yes. Sizes, including spoon lengths, colours and finishes are made to your specification. Send a drawing, photo or reference piece with the quantity.'),
    next_h='Tell us which shell pieces <em>you need.</em>',
    next_p='Write to us or send a WhatsApp message with the spoons, napkin rings or other pieces you are interested in, the sizes, the quantity per design and your market. We reply with photos and ex-works prices.',
))

PAGES.append(dict(
    slug='resin', path='/resin/', crumb='Resin &amp; terrazzo',
    title='Resin &amp; Terrazzo Tableware Manufacturer, Kolkata | Chowringhee Arts',
    og_title='Resin and terrazzo tableware — Chowringhee Arts, Kolkata',
    desc='Resin and terrazzo boxes and tableware, handmade in Kolkata, some combined with bone. Coloured resin to your specification. Trade only, ex-works Kolkata.',
    og='resin.jpg', og_alt='Checkerboard resin and bone boxes',
    targets=['resin tableware manufacturer Kolkata', 'terrazzo homeware supplier India', 'resin boxes wholesale'],
    eyebrow='Resin &amp; terrazzo · for the trade',
    h1='Resin and terrazzo tableware, <em>handmade in Kolkata</em>',
    lede='Boxes and tableware in coloured resin and terrazzo, some combined with bone. Made by our karigars for importers, wholesalers and retail chains.',
    hero_img='cat-resin-box', hero_alt='Checkerboard resin and bone boxes',
    hero_cap='Checkerboard resin and bone boxes',
    hero_facts=['Handmade', 'Colours to order', 'Samples on request', 'Ready 30–45 days'],
    mail_subject='Resin and terrazzo enquiry', wa_text='Hello Chowringhee Arts, I am interested in your resin and terrazzo pieces.',
    make_lede='There is only one resin piece on this website so far. Ask us and we will send photos of the resin and terrazzo pieces that suit your range.',
    make=[('Boxes', 'Resin boxes, including checkerboard boxes in resin and bone.'),
          ('Tableware', 'Resin and terrazzo tableware and serveware. Tell us the pieces you need and we send photos of what we make.'),
          ('Coloured resin', 'Resin in the colours you specify.'),
          ('Terrazzo', 'Terrazzo pieces; ask us for photos of current designs.')],
    made_h='How resin pieces are <em>made</em>',
    made=['<p>Like the rest of our range, our resin and terrazzo pieces are made and finished by hand by our karigars in Kolkata.</p>',
          '<p>Resin can be combined with other materials: the checkerboard boxes shown here combine resin and bone.</p>',
          '<p>Colours are made to your specification. Send us a colour reference with your enquiry.</p>'],
    sizes_rows=[('Sizes', 'We send sizes with photos and prices for the pieces you ask about. Custom sizes are made to your specification.'),
                ('Colours', 'Coloured resin and terrazzo in the colours you specify.')] + TERMS,
    gallery=[('cat-resin-box', 'Checkerboard resin and bone boxes', '')],
    faq=faq_common('What is the resin made from?',
                   'Ask us about the materials in the pieces you are interested in and we will tell you for those pieces.',
                   'Yes. Sizes and colours are made to your specification. Send a colour reference, drawing or photo with the quantity.'),
    next_h='Tell us which resin pieces <em>you need.</em>',
    next_p='Write to us or send a WhatsApp message with the kind of resin or terrazzo piece you are looking for, the colours, the quantity per design and your market. We reply with photos, sizes and ex-works prices.',
))

# ---------------------------------------------------------------- material page body
def material_page(p):
    body = [head(p), header(p), '<main id="main">\n', sub_hero(p)]
    body.append(f'''  <section class="band" aria-labelledby="make-title">
    <div class="wrap">
      <div class="sec-head"><div><p class="eyebrow">What we make</p><h2 id="make-title">What we make in <em>{p["crumb"].lower() if p["slug"] != "mother-of-pearl" else "mother-of-pearl"}.</em></h2></div><p class="lede">{p["make_lede"]}</p></div>
      {make_list(p["make"])}
    </div>
  </section>
  <section class="band card" aria-labelledby="made-title">
    <div class="wrap split">
      <div class="prose"><p class="eyebrow">The craft</p><h2 id="made-title">{p["made_h"]}</h2>{''.join(p["made"])}</div>
      <div class="prose"><p class="eyebrow">Sizes and customisation</p><h2 id="size-title">Sizes, finishes <em>and terms.</em></h2>{spec(p["sizes_rows"])}</div>
    </div>
  </section>
  <section class="band" aria-labelledby="gal-title">
    <div class="wrap">
      <div class="sec-head"><div><p class="eyebrow">Gallery</p><h2 id="gal-title">From our <em>{p["crumb"].lower() if p["slug"] != "mother-of-pearl" else "mother-of-pearl"} range.</em></h2></div><p class="lede">Real pieces, photographed by us. Ask for sizes and ex-works prices on anything you see.</p></div>
      {gallery(p["gallery"])}
      {f'<p class="note">{p["gallery_note"]}</p>' if p.get("gallery_note") else ''}
    </div>
  </section>
  <section class="band alt" aria-labelledby="faq-title">
    <div class="wrap">
      <div class="sec-head"><div><p class="eyebrow">Questions buyers ask</p><h2 id="faq-title">FAQ</h2></div><p class="lede">More detail on payment, samples and fairs is on <a href="/trade/">how we trade</a>.</p></div>
      {faq_html(p["faq"])}
    </div>
  </section>
''')
    body.append(next_step(p))
    body.append(other_links(p))
    body.append('</main>\n')
    body.append(FOOTER)
    return ''.join(body)

# ---------------------------------------------------------------- trade
TRADE = dict(
    slug='trade', path='/trade/', crumb='How we trade',
    title='Handicraft Exporter Kolkata: Wholesale Terms | Chowringhee Arts',
    og_title='How to buy from Chowringhee Arts — trade terms',
    desc='How to buy from Chowringhee Arts, a Kolkata handicraft exporter: trade only, ex-works Kolkata, 50% advance, ready 30–45 days, samples on request.',
    og='trade.jpg', og_alt='The Chowringhee Arts stand at IHGF Delhi Fair',
    targets=['handicraft exporter Kolkata', 'wholesale handicrafts India terms', 'IHGF exhibitor horn bone shell'],
    eyebrow='Working with us',
    h1='How to buy from us: <em>terms, samples and lead times</em>',
    lede='We sell to the trade only: importers, wholesalers, retail chains, hotel suppliers and buying agents. Here is how an order works, from first message to dispatch.',
    hero_img='stand-front', hero_alt='The Chowringhee Arts stand at IHGF Delhi Fair, Autumn 2025',
    hero_cap='Our stand at IHGF Delhi Fair, Autumn 2025', hero_sizes='(max-width:900px) 92vw, 560px',
    hero_facts=['Trade only', 'Ex-works Kolkata', '50% advance', 'Ready 30–45 days'],
    mail_subject='Trade enquiry', wa_text='Hello Chowringhee Arts, I would like to discuss a trade order.',
    faq=[(q, e(a), a) for q, a in [
        ('Do you sell to consumers?', 'No. We sell to the trade only: importers, wholesalers, retail chains, hotel suppliers and buying agents.'),
        ('Do you send a price list or catalogue?', 'No. We do not publish prices or send full catalogues. Tell us the pieces you are interested in and we send photos, sizes and ex-works Kolkata prices for those.'),
        ('Is there a minimum order quantity?', 'Prices get better from 100 pieces and again from 300 pieces per design. Tell us the quantities you have in mind and we will quote for those.'),
        ('Can I order samples?', 'Yes. Samples are made on request and charged at the piece price.'),
        ('What are the payment terms?', '50% advance with the order, and the balance before dispatch.'),
        ('How long does an order take?', 'Orders are ready 30 to 45 days after we receive the advance.'),
        ('Where are prices quoted?', 'Ex-works Kolkata, in US dollars.'),
        ('Can I see your pieces in person?', 'Yes. We exhibit at IHGF Delhi Fair. The next edition is IHGF Spring 2027, 15 to 19 March 2027, at India Expo Centre and Mart, Greater Noida. Write to us for our stand number before the fair.'),
    ]],
    next_h='Start with the pieces <em>you are interested in.</em>',
    next_p='Write to us or send a WhatsApp message with the pieces you are interested in (photos from this site, your own references or a description), the quantity per design and your market. We reply with photos, sizes and ex-works prices.',
)

def trade_page(p):
    steps = [('Tell us what you need', 'The pieces you are interested in, rough quantities per design and your market. Photos from this site or your own references are fine.'),
             ('Photos, sizes and prices', 'We reply with photos, sizes and ex-works Kolkata prices in US dollars for those pieces. We do not send full catalogues or price lists.'),
             ('Samples', 'If you want to see a piece first, we make samples on request, charged at the piece price.'),
             ('Order and advance', 'Confirm the pieces, quantities and any custom sizes, colours or finishes. We start on receipt of a 50% advance.'),
             ('Production', 'Everything is made by hand by our karigars. Orders are ready 30 to 45 days after the advance.'),
             ('Balance and dispatch', 'The balance is paid before dispatch. Goods are sold ex-works Kolkata.')]
    st = ''.join(f'<li class="step"><span class="n">{n}</span><h3>{t}</h3><p>{d}</p></li>' for n, (t, d) in enumerate(steps, 1))
    rows = [('Who we sell to', 'Importers, wholesalers, retail chains, hotel suppliers and buying agents. Trade only.'),
            ('Prices', 'Quoted ex-works Kolkata, in US dollars, for the pieces you ask about'),
            ('Volume', 'Better prices from 100 and from 300 pieces per design'),
            ('Samples', 'On request, charged at piece price'),
            ('Custom work', 'Sizes, colours and finishes to your specification'),
            ('Payment', '50% advance, balance before dispatch'),
            ('Lead time', 'Ready 30 to 45 days after the advance'),
            ('Membership', 'Member of EPCH, the Export Promotion Council for Handicrafts')]
    body = [head(p), header(p), '<main id="main">\n', sub_hero(p, photo=True)]
    body.append(f'''  <section class="buyers on-navy" aria-labelledby="steps-title">
    <div class="wrap">
      <div class="sec-head"><div><p class="eyebrow">Step by step</p><h2 id="steps-title">How an order <em>works.</em></h2></div><p class="lede">We start from your requirement, so you only see the pieces that fit.</p></div>
      <ol class="steps s3">{st}</ol>
    </div>
  </section>
  <section class="band card" aria-labelledby="terms-title">
    <div class="wrap split">
      <div class="prose"><p class="eyebrow">Terms</p><h2 id="terms-title">Trade terms <em>at a glance.</em></h2>{spec(rows)}</div>
      <div class="prose"><p class="eyebrow">Trade fairs</p><h2 id="fair-title">Meet us at <em>IHGF Delhi Fair.</em></h2>
        <p>We exhibit at IHGF Delhi Fair, organised by EPCH, at India Expo Centre and Mart, Greater Noida.</p>
        <ul class="past-list" aria-label="IHGF Delhi Fair editions">
          <li class="next"><b>Spring 2027 · 15–19 March 2027</b>India Expo Centre and Mart, Greater Noida. Write to us for our stand.</li>
          <li><b>Autumn 2026</b>Hall 3, Stand E-06/05</li>
          <li><b>Spring 2026</b>Hall 11, G10/29</li>
          <li><b>Autumn 2025</b>Hall 16, J-01/11</li>
        </ul>
        <p class="note">You do not need to come to Delhi: you can start by email or WhatsApp with photos of the pieces you want.</p>
      </div>
    </div>
  </section>
  <section class="band" aria-labelledby="what-title">
    <div class="wrap">
      <div class="sec-head"><div><p class="eyebrow">What we make</p><h2 id="what-title">4,000+ designs in <em>five materials.</em></h2></div><p class="lede">Each material has its own page with photos, how it is made and the questions buyers ask about it.</p></div>
      <ul class="mat-links">{''.join(f'<li><a href="/{s}/"><span class="th">{pic(img, alt, "64px")}</span><span><b>{n}</b><small>{sub}</small></span></a></li>' for s, n, sub, img, alt in MATERIALS)}</ul>
    </div>
  </section>
  <section class="band alt" aria-labelledby="faq-title">
    <div class="wrap">
      <div class="sec-head"><div><p class="eyebrow">Questions buyers ask</p><h2 id="faq-title">FAQ</h2></div></div>
      {faq_html(p["faq"])}
    </div>
  </section>
''')
    body.append(next_step(p))
    body.append('</main>\n')
    body.append(FOOTER)
    return ''.join(body)

# ---------------------------------------------------------------- about
ABOUT = dict(
    slug='about', path='/about/', crumb='About us',
    title='About Us: Horn, Bone &amp; Shell Makers in Kolkata | Chowringhee Arts',
    og_title='About Chowringhee Arts — handmade in Kolkata for 10 years',
    desc='Chowringhee Arts: 10 years making handmade horn, bone inlay, mother-of-pearl, shell and resin homeware in Kolkata. EPCH member and IHGF Delhi Fair exhibitor.',
    og='about.jpg', og_alt='Shelves of bone inlay, horn and shell pieces on the Chowringhee Arts stand',
    targets=['IHGF exhibitor horn bone shell', 'handicraft exporter Kolkata', 'horn and bone handicrafts manufacturer India'],
    eyebrow='About Chowringhee Arts',
    h1='Horn, bone and shell, <em>made by hand in Kolkata</em>',
    lede='We are an export house on Park Street, Kolkata. For 10 years our karigars have made homeware in buffalo horn, bone inlay, mother-of-pearl, seashell and resin for buyers abroad.',
    hero_img='stand-shelves', hero_alt='Shelves of bone inlay trays, horn and shell pieces on the Chowringhee Arts stand at IHGF Delhi Fair',
    hero_cap='On our stand at IHGF Delhi Fair', hero_sizes='(max-width:900px) 92vw, 560px',
    hero_facts=['10 years in business', '4,000+ designs', 'Member of EPCH', 'IHGF exhibitor'],
    mail_subject='Enquiry from chowringheearts.com', wa_text='Hello Chowringhee Arts, I found you on your website.',
    next_h='Tell us what <em>you are looking for.</em>',
    next_p='Write to us or send a WhatsApp message with the pieces you are interested in, the quantity per design and your market. We reply with photos, sizes and ex-works prices.',
)

def about_page(p):
    body = [head(p), header(p), '<main id="main">\n', sub_hero(p, photo=True)]
    body.append(f'''  <section class="band" aria-labelledby="story-title">
    <div class="wrap split">
      <div class="prose"><p class="eyebrow">Our story</p><h2 id="story-title">Real materials, <em>real hands.</em></h2>
        <p>Chowringhee Arts has been in business for 10 years. From our office at 75C Park Street, in the heart of Kolkata, we make and export handmade homeware for importers, wholesalers, retail chains, hotel suppliers and buying agents.</p>
        <p>The range has grown to <strong>more than 4,000 designs</strong>: bowls, trays, dishes, boxes, cutlery and serveware, table accessories, desk pieces, combs and small furniture.</p>
        <p>We do not sell retail. Buyers tell us what they need, and we send photos, sizes and ex-works prices for the pieces that fit.</p>
      </div>
      <div class="prose"><p class="eyebrow">Our people</p><h2 id="people-title">Made by <em>our karigars.</em></h2>
        <p>Everything we sell is made by hand. Our pieces are made by many karigars, skilled artisans, and <strong>women are a big part of our team</strong>.</p>
        <p>Horn is cut, shaped and polished by hand until its natural grain shows. Bone inlay is set one small piece at a time. Mother-of-pearl is carved into dishes, birds and flowers. It is patient work, and no two pieces are exactly alike.</p>
      </div>
    </div>
  </section>
  <section class="band card" aria-labelledby="mat-title">
    <div class="wrap split">
      <div class="prose"><p class="eyebrow">Our materials</p><h2 id="mat-title">Horn and bone that would <em>otherwise go to waste.</em></h2>
        <p>Our buffalo horn and bone are <strong>by-products of cattle farming</strong>. No animal is harmed for our products.</p>
        <p>We use real buffalo horn, never faux. Every horn piece has its own grain, and every shell its own shimmer.</p>
        <p>We also work in mother-of-pearl, seashell and resin, and finish many pieces with brass details.</p>
      </div>
      <div class="prose"><p class="eyebrow">Membership and fairs</p><h2 id="fair-title">EPCH member, <em>IHGF exhibitor.</em></h2>
        <p>We are a member of EPCH, the Export Promotion Council for Handicrafts, and exhibit at IHGF Delhi Fair.</p>
        <ul class="past-list" aria-label="IHGF Delhi Fair editions">
          <li class="next"><b>Spring 2027 · 15–19 March 2027</b>India Expo Centre and Mart, Greater Noida</li>
          <li><b>Autumn 2026</b>Hall 3, Stand E-06/05</li>
          <li><b>Spring 2026</b>Hall 11, G10/29</li>
          <li><b>Autumn 2025</b>Hall 16, J-01/11</li>
        </ul>
      </div>
    </div>
  </section>
  <section class="band" aria-labelledby="range-title">
    <div class="wrap">
      <div class="sec-head"><div><p class="eyebrow">What we make</p><h2 id="range-title">Five materials, <em>all handmade.</em></h2></div><p class="lede">See photos, finishes and buyer FAQs for each material.</p></div>
      <ul class="mat-links">{''.join(f'<li><a href="/{s}/"><span class="th">{pic(img, alt, "64px")}</span><span><b>{n}</b><small>{sub}</small></span></a></li>' for s, n, sub, img, alt in MATERIALS)}<li><a href="/trade/"><span class="th">{pic('stand-front', 'The Chowringhee Arts stand at IHGF Delhi Fair, Autumn 2025', '64px')}</span><span><b>How we trade</b><small>Terms, samples and lead times</small></span></a></li></ul>
      <figure class="sub-stage photo" style="margin-top:22px;aspect-ratio:16/9">{pic('stand-front', 'The Chowringhee Arts stand at IHGF Delhi Fair, Autumn 2025', '(max-width:1200px) 92vw, 1100px')}<figcaption>Our stand at IHGF Delhi Fair, Autumn 2025</figcaption></figure>
    </div>
  </section>
''')
    body.append(next_step(p))
    body.append('</main>\n')
    body.append(FOOTER)
    return ''.join(body)

# ---------------------------------------------------------------- 404
NOTFOUND = dict(
    slug='404', path='/404.html', crumb='Page not found', noindex=True,
    title='Page not found | Chowringhee Arts',
    og_title='Chowringhee Arts — Handmade in India, for trade',
    desc='This page does not exist. Chowringhee Arts makes handmade homeware in buffalo horn, bone inlay, mother-of-pearl, seashell and resin for the trade.',
    og_alt='Chowringhee Arts',
)

def notfound_page(p):
    p = dict(p)
    p['og'] = 'about.jpg'
    body = [head(p), header(p), '<main id="main">\n']
    body.append(f'''  <section class="sub-hero on-navy" aria-labelledby="page-title">
    <div class="wrap">
      <p class="eyebrow">Error 404</p>
      <h1 id="page-title">We can't find <em>that page.</em></h1>
      <p class="lede">The link may be old or mistyped. Try one of these pages, or go back to the <a href="/" style="color:var(--gold-hi)">home page</a>.</p>
      <div class="cta-row"><a class="btn btn-gold" href="/">Go to the home page</a><a class="btn btn-ghost" href="mailto:{EMAIL}?subject=Enquiry%20from%20chowringheearts.com">{I_MAIL}Email us</a></div>
    </div>
  </section>
  <section class="band" aria-labelledby="more-title">
    <div class="wrap">
      <div class="sec-head"><div><p class="eyebrow">Our pages</p><h2 id="more-title">Where to <em>next.</em></h2></div></div>
      <ul class="mat-links">{''.join(f'<li><a href="/{s}/"><span class="th">{pic(img, alt, "64px")}</span><span><b>{n}</b><small>{sub}</small></span></a></li>' for s, n, sub, img, alt in MATERIALS)}<li><a href="/trade/"><span class="th">{pic('stand-front', 'The Chowringhee Arts stand at IHGF Delhi Fair, Autumn 2025', '64px')}</span><span><b>How we trade</b><small>Terms, samples and lead times</small></span></a></li><li><a href="/about/"><span class="th">{pic('stand-shelves', 'Shelves of bone inlay, horn and shell pieces on the Chowringhee Arts stand', '64px')}</span><span><b>About us</b><small>10 years, 4,000+ designs, Kolkata</small></span></a></li></ul>
    </div>
  </section>
  <section id="enquire" class="band alt" aria-label="Contact">
    <div class="wrap"><p class="note" style="margin:0">Looking for something specific? Email <a href="mailto:{EMAIL}">{EMAIL}</a> or WhatsApp <a href="{wa('Hello Chowringhee Arts, I found you on your website.')}" target="_blank" rel="noopener">+91 98309 22999</a> with the pieces you are interested in.</p></div>
  </section>
''')
    body.append('</main>\n')
    body.append(FOOTER)
    return ''.join(body)

# ---------------------------------------------------------------- write
def write(rel, text):
    path = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)
    print('wrote', rel, len(text.encode()), 'bytes')

if __name__ == '__main__':
    for p in PAGES:
        write(f'{p["slug"]}/index.html', material_page(p))
    write('trade/index.html', trade_page(TRADE))
    write('about/index.html', about_page(ABOUT))
    write('404.html', notfound_page(NOTFOUND))
    urls = ['/'] + [p['path'] for p in PAGES] + ['/trade/', '/about/']
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    sm += [f'  <url><loc>{SITE}{u}</loc><lastmod>{LASTMOD}</lastmod></url>' for u in urls]
    sm.append('</urlset>')
    write('sitemap.xml', '\n'.join(sm) + '\n')
    # summary for the pull request
    with open(os.path.join(ROOT, 'tools', 'pages.json'), 'w') as f:
        json.dump([{'path': p['path'], 'title': html.unescape(p['title']), 'desc': p['desc'], 'targets': p['targets']}
                   for p in PAGES + [TRADE, ABOUT]], f, indent=1, ensure_ascii=False)
