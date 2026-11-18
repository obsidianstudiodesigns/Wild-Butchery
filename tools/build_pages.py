"""Build privacy.html, terms.html, 404.html, robots.txt, sitemap.xml and site.webmanifest.

Run from the project root:  python -I tools/build_pages.py
"""
import json
import os
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = "Wild-Butchery"
BASE = f"https://obsidianstudiodesigns.github.io/{REPO}/"
NAME = "Wild Butchery"
UPDATED = "November 2026"
TODAY = date.today().isoformat()
WA = "https://wa.me/27640725121?text=Hi%20Wild%20Butchery%2C%20"


def page(slug, title, desc, body, robots="index, follow"):
    nf = slug == "404.html"
    pre = f"/{REPO}/" if nf else ""
    canon = "" if nf else f'<link rel="canonical" href="{BASE}{slug}">'
    base = f'<base href="/{REPO}/">' if nf else ""
    return f"""<!DOCTYPE html>
<html lang="en-ZA" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="{robots}">
{canon}
<meta name="color-scheme" content="dark">
<meta name="theme-color" content="#1a1512">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{NAME}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{BASE}assets/img/og-share.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<link rel="icon" href="{pre}favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="{pre}favicon-32.png">
<link rel="apple-touch-icon" href="{pre}apple-touch-icon.png">
<link rel="manifest" href="{pre}site.webmanifest">
{base}
<link rel="stylesheet" href="assets/css/style.css?v=1">
<script>document.documentElement.classList.replace('no-js','js')</script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site-header">
  <div class="wrap bar">
    <a class="brand" href="./" aria-label="Wild Butchery, home">
      <img src="assets/img/tree-64.png" srcset="assets/img/tree-64.png 1x, assets/img/tree-128.png 2x" alt="" width="44" height="31">
      <span class="brand__name">Wild Butchery</span>
    </a>
    <nav class="nav" id="nav" aria-label="Main">
      <a href="./#counter">The counter</a>
      <a href="./#planner">Braai planner</a>
      <a href="./#questions">Questions</a>
      <a href="./#visit">Visit</a>
      <a class="btn btn--ember nav__cta" href="{WA}" target="_blank" rel="noopener"><svg class="icon" aria-hidden="true"><use href="assets/icons.svg#i-whatsapp-logo"></use></svg>WhatsApp an order</a>
    </nav>
    <button class="menu-btn" type="button" aria-label="Open menu" aria-expanded="false" aria-controls="nav">
      <svg class="icon i-menu" aria-hidden="true"><use href="assets/icons.svg#i-list"></use></svg>
      <svg class="icon i-close" aria-hidden="true"><use href="assets/icons.svg#i-x"></use></svg>
    </button>
  </div>
</header>
<main id="main">
{body}
</main>
<footer class="footer">
  <div class="wrap footer__bottom" style="border-top:0">
    <span>&copy; <span id="yr">{date.today().year}</span> {NAME}. <a href="privacy.html">Privacy policy</a> <a href="terms.html">Terms of use</a></span>
    <span class="credit">Website designed by <a href="https://obsidianstudiodesigns.co.za/" target="_blank" rel="noopener">Obsidian Studio Designs</a></span>
  </div>
</footer>
<a class="fab" href="{WA}" target="_blank" rel="noopener" aria-label="WhatsApp Wild Butchery"><svg class="icon" aria-hidden="true"><use href="assets/icons.svg#i-whatsapp-logo"></use></svg></a>
<script src="assets/js/main.js?v=1" defer></script>
</body>
</html>
"""


CONTACT = ('<a href="https://wa.me/27640725121" target="_blank" rel="noopener">064 072 5121</a> (WhatsApp), '
           '<a href="tel:+27716583316">071 658 3316</a> or <a href="mailto:wildbutchery@gmail.com">wildbutchery@gmail.com</a>')

PRIVACY = f"""<div class="legal-head"><div class="wrap"><h1>Privacy policy</h1><p>Protection of Personal Information Act, 2013 (POPIA). Last updated {UPDATED}.</p></div></div>
<div class="wrap legal">
<p>{NAME} ("we", "us") is a butchery in the Bush Centre, Marloth Park. This policy explains what personal information we collect when you visit this website, message us or place an order, why we need it, and the rights you have under POPIA.</p>

<h2>1. Who is responsible</h2>
<p>The responsible party is {NAME}, Bush Centre, 3883 Olifant Road, Marloth Park, 1321, Mpumalanga. You can reach us on {CONTACT}.</p>

<h2>2. What we collect</h2>
<ul>
<li>Your name and phone or WhatsApp number when you message or call us.</li>
<li>Your email address if you email us.</li>
<li>Order details, such as the products and quantities you ask for and the day you want to collect.</li>
<li>Records of payments made in the shop, as required for our accounting.</li>
</ul>
<p>This website does not take payments and never asks for card or banking details.</p>

<h2>3. How the braai planner works</h2>
<p>The braai planner works out suggested amounts in your own browser and does not store anything on a server. When you press "Send list on WhatsApp", your browser opens WhatsApp with the list filled in, and nothing reaches us until you send it yourself. Messages sent on WhatsApp are also subject to WhatsApp's own privacy terms.</p>

<h2>4. Why we use it</h2>
<ul>
<li>To answer your questions and prepare and confirm your order.</li>
<li>To let you know when your order is ready or if something is out of stock.</li>
<li>To keep the accounting and tax records the law requires.</li>
</ul>
<p>We do not sell or rent your information, and we will not add you to marketing lists or broadcast groups without your consent.</p>

<h2>5. Who we share it with</h2>
<p>We share your information only where it is needed to run the business or where the law requires it, for example with our accountant, our payment and banking providers, and the messaging and email services we use to talk to you.</p>

<h2>6. How long we keep it</h2>
<p>Order messages are kept only as long as they are useful for your order and any follow-up questions. Financial records are kept for as long as tax law requires (currently five years).</p>

<h2>7. Keeping it safe</h2>
<p>We take reasonable steps to protect your information against loss, misuse and unauthorised access, including password-protected phones, accounts and backups.</p>

<h2>8. This website</h2>
<p>This website does not use advertising cookies or tracking analytics, and it does not ask you to log in. It is hosted on GitHub Pages, which may keep basic technical logs (such as IP addresses) to keep the service secure. The map on the home page is provided by Google Maps, which may set its own cookies when it loads. Links to WhatsApp, Facebook, Google Maps and email open services with their own privacy policies.</p>

<h2>9. Your rights</h2>
<p>Under POPIA you may ask what personal information we hold about you, ask us to correct or delete it, object to how we use it, and withdraw consent you have given. Contact us using the details above. If you are not happy with our response you may complain to the Information Regulator (South Africa) at <a href="https://inforegulator.org.za/" target="_blank" rel="noopener">inforegulator.org.za</a>.</p>

<h2>10. Changes</h2>
<p>We may update this policy from time to time. The latest version will always be on this page.</p>
</div>"""

TERMS = f"""<div class="legal-head"><div class="wrap"><h1>Terms of use</h1><p>Last updated {UPDATED}.</p></div></div>
<div class="wrap legal">
<p>These terms apply to your use of this website and to orders placed with {NAME} ("we", "us"). By using the website you accept them.</p>

<h2>1. Products and prices</h2>
<ul>
<li>The products on this website are examples of what we usually stock. What is in the display changes with supply and the season.</li>
<li>Prices are not listed on this website. Prices and specials are confirmed in the shop, on WhatsApp or on our Facebook page.</li>
<li>Specials run for the dates stated, while stocks last.</li>
<li>Meat is sold by weight, so the final weight and price of an order can differ a little from what was asked for.</li>
</ul>

<h2>2. Orders</h2>
<ul>
<li>An order sent on WhatsApp or by phone is a request until we confirm it.</li>
<li>Please collect confirmed orders on the agreed day. If your plans change, let us know as early as you can.</li>
<li>Fresh meat must be kept cold. Once an order has been collected, storage and cooking are your responsibility.</li>
</ul>

<h2>3. The braai planner</h2>
<p>The braai planner gives a rough guide only, based on average portions. Appetites differ, so please use your own judgement and ask us at the counter if you are unsure.</p>

<h2>4. Photographs</h2>
<p>Photographs on this website are illustrative and do not show specific products from our counter.</p>

<h2>5. Use of this website</h2>
<p>You may use this website for personal, non-commercial purposes. Do not copy its content or images for commercial use without our written permission.</p>

<h2>6. Liability</h2>
<p>We take care to keep the information on this website correct, but it may contain errors or be out of date, for example trading hours over holidays. To the extent the law allows, we are not liable for loss arising from reliance on the website. Nothing in these terms limits your rights under the Consumer Protection Act, 2008.</p>

<h2>7. Links</h2>
<p>This website links to services run by others, such as WhatsApp, Facebook and Google Maps. We are not responsible for their content or how they handle your information.</p>

<h2>8. Governing law</h2>
<p>These terms are governed by the laws of South Africa.</p>

<h2>9. Contact</h2>
<p>Questions about these terms? Contact us on {CONTACT}.</p>
</div>"""

NOTFOUND = """<section class="wrap notfound">
<h1>Off the menu</h1>
<p>That page isn't here. The steaks, boerewors and braai planner are all on the home page.</p>
<div><a class="btn btn--ember btn--lg" href="./">Back to the home page</a></div>
</section>"""

PAGES = [
    ("privacy.html", f"Privacy policy | {NAME}", "How Wild Butchery in Marloth Park collects, uses and protects your personal information under POPIA.", PRIVACY, "index, follow"),
    ("terms.html", f"Terms of use | {NAME}", "Terms for using the Wild Butchery website and placing orders at the Bush Centre, Marloth Park.", TERMS, "index, follow"),
    ("404.html", f"Page not found | {NAME}", "This page could not be found.", NOTFOUND, "noindex"),
]

for slug, title, desc, body, robots in PAGES:
    with open(os.path.join(ROOT, slug), "w", encoding="utf-8", newline="\n") as fh:
        fh.write(page(slug, title, desc, body, robots))

with open(os.path.join(ROOT, "robots.txt"), "w", newline="\n") as fh:
    fh.write(f"User-agent: *\nAllow: /\nDisallow: /tools/\n\nSitemap: {BASE}sitemap.xml\n")

imgs = ["hero-wide-1536.webp", "steaks-1024.webp", "wors-1280.webp", "sosaties-1536.webp", "braai-1536.webp", "og-share.jpg"]
img_xml = "\n".join(f"    <image:image><image:loc>{BASE}assets/img/{i}</image:loc></image:image>" for i in imgs)
with open(os.path.join(ROOT, "sitemap.xml"), "w", newline="\n") as fh:
    fh.write(f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">
  <url>
    <loc>{BASE}</loc>
    <lastmod>{TODAY}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
{img_xml}
  </url>
  <url>
    <loc>{BASE}privacy.html</loc>
    <lastmod>{TODAY}</lastmod>
    <changefreq>yearly</changefreq>
    <priority>0.3</priority>
  </url>
  <url>
    <loc>{BASE}terms.html</loc>
    <lastmod>{TODAY}</lastmod>
    <changefreq>yearly</changefreq>
    <priority>0.3</priority>
  </url>
</urlset>
""")

manifest = {
    "name": NAME,
    "short_name": NAME,
    "description": "Butchery in the Bush Centre, Marloth Park. Steaks, boerewors, biltong and sosaties for your braai.",
    "start_url": "./",
    "scope": "./",
    "display": "standalone",
    "background_color": "#1a1512",
    "theme_color": "#1a1512",
    "icons": [
        {"src": "icon-192.png", "sizes": "192x192", "type": "image/png"},
        {"src": "icon-512.png", "sizes": "512x512", "type": "image/png"},
        {"src": "icon-maskable-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"},
    ],
}
with open(os.path.join(ROOT, "site.webmanifest"), "w", newline="\n") as fh:
    json.dump(manifest, fh, indent=2)
print("ok")
