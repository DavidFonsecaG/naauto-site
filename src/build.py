"""Builds the N&A Auto Repairs static pages from shared partials.

Run:  python3 build.py   (writes ../dist/)
index.html is written without <!doctype>/<head> wrappers for the Artifact preview;
pass --standalone to wrap it like the other pages for real hosting.
"""
import html, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "dist")
STANDALONE = "--standalone" in sys.argv
EMBED_MAP = STANDALONE  # the Artifact preview cannot embed other sites, so the live map only goes into the hosted build

PHONE = "(847) 859-6191"
TEL = "tel:+18478596191"
MAPS = "https://www.google.com/maps/search/?api=1&amp;query=N%26A+Auto+Repairs+1701+W+Howard+St+Evanston+IL"
INSTA = "https://www.instagram.com/na_auto_repairs/"

FONTS = ("https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@100..125,400..900"
         "&family=Barlow:wght@400;500;600&family=Big+Shoulders+Display:wght@600;800;900"
         "&family=Chakra+Petch:wght@500;600;700&family=IBM+Plex+Mono:wght@400;500"
         "&family=Public+Sans:wght@400;500;600;700&display=swap")

PHONE_ICON = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/></svg>'

# ---------------------------------------------------------------- services
CATS = {"maint": "Maintenance", "repair": "Repair", "body": "Body & care"}
SERVICES = [
    ("oil", "maint", "Oil change", "Fresh oil and a new filter to keep the engine running smoothly.",
     ["Oil-life or maintenance light is on", "Dark, gritty oil on the dipstick", "Engine sounds louder than usual"]),
    ("battery", "maint", "Battery replacement", "Testing and replacement so you're never stuck with a dead start.",
     ["Slow crank on cold mornings", "Battery light on the dash", "Battery is 3 to 5 years old"]),
    ("filter", "maint", "Air filter replacement", "Engine and cabin filters for clean air and better mileage.",
     ["Lower gas mileage", "Musty smell from the vents", "Weak airflow from the vents"]),
    ("tire", "maint", "Tire replacement", "New tires mounted and balanced for a safer, smoother ride.",
     ["Tread worn down to the wear bars", "Bulges, cracks or a tire that keeps losing air", "Vibration at highway speed"]),
    ("align", "maint", "Wheel alignment", "Straight tracking, better handling and longer tire life.",
     ["Car pulls to one side", "Steering wheel sits off-center", "Uneven wear on the tires"]),
    ("brakes", "repair", "Brake repair", "Pads, rotors, calipers and lines, inspected and fixed right.",
     ["Squealing or grinding when you stop", "Soft or spongy brake pedal", "Car pulls to one side when braking"]),
    ("engine", "repair", "Engine repair", "Check-engine diagnostics through to major engine repairs.",
     ["Check engine light is on", "Rough idle or stalling", "Loss of power or a knocking sound"]),
    ("trans", "repair", "Transmission repair", "Service and repair so every gear shifts the way it should.",
     ["Slipping or delayed shifts", "Burning smell or a red fluid leak", "Clunk when shifting into gear"]),
    ("electric", "repair", "Electrical repair", "Wiring, starters, alternators and those hard-to-find faults.",
     ["Lights dim or flicker", "Windows or locks acting up", "Won't start, but the battery tests fine"]),
    ("susp", "repair", "Steering & suspension", "Shocks, struts and steering parts for a controlled ride.",
     ["Bouncy or floaty ride", "Clunks over bumps", "Nose dives when you brake"]),
    ("exhaust", "repair", "Exhaust", "Mufflers, pipes and catalytic converters repaired or replaced.",
     ["Engine sounds much louder", "Rattle from under the car", "Exhaust smell inside the cabin"]),
    ("ac", "repair", "A/C repair", "Recharge and repair so the cabin stays cool through July.",
     ["Air blows warm", "Weak airflow", "Odd smell or noise with the A/C on"]),
    ("glass", "body", "Glass repair", "Chips and cracks fixed for clear, safe visibility.",
     ["Chip or crack in the windshield", "A crack that keeps spreading", "Broken side or rear window"]),
    ("bodywork", "body", "Body repair & paint", "Dents, scrapes and panel work finished to match.",
     ["Dents and door dings", "Scratched or chipped paint", "Panel damage after a fender-bender"]),
    ("detail", "body", "Detailing", "Inside-and-out cleaning that leaves the car looking sharp.",
     ["Stains, crumbs and pet hair", "Dull, faded paint", "Getting ready to sell or trade in"]),
]
FEATURED = ["brakes", "engine", "oil", "ac", "tire", "electric"]

# ---------------------------------------------------------------- service photos (Unsplash License; see img/services/credits.md)
SERVICE_PHOTOS = {  # key: (alt text, photographer, Unsplash photo id)
    "oil": ("Mechanic pouring fresh oil into a car engine", "Dextar Studio", "gW34cv-Ojjs"),
    "battery": ("Close-up of a car battery with its cables connected", "Wesley Tingey", "E4Oz0TZUDe8"),
    "filter": ("Air filter installed in a car engine bay", "Rahul Bhogal", "9mxviB2BBOE"),
    "tire": ("Mechanic mounting a wheel and tire in a garage", "Jimmy Nilsson Masth", "9uHal2Dd9aE"),
    "align": ("Truck on an alignment lift with wheel clamps attached", "Hanindito Prabandaru", "GGp8F_3EOpo"),
    "brakes": ("Brake rotor and caliper exposed with the wheel off", "Erik Mclean", "vS2shmNei2E"),
    "engine": ("Mechanic inspecting an engine under an open hood", "Kate Ibragimova", "bEGTsOCnHro"),
    "trans": ("Automatic transmission gear selector in a car", "Maxim Hopman", "FdAXItuGDnY"),
    "electric": ("Mechanic testing the fuse box under a car's hood", "Maxim Hopman", "s4d_ESS0ylA"),
    "susp": ("Car suspension and steering parts behind the wheel", "Wesley Tingey", "U4i2bZw4wms"),
    "exhaust": ("Dual exhaust tips at the back of a car", "Obi", "MmWN1yTatDg"),
    "ac": ("Car climate control panel with the A/C button", "Luca Freddi", "e_c6jDnvpRg"),
    "glass": ("Shattered car windshield", "Gohar Khachatryan", "oeA4k4u6AbI"),
    "bodywork": ("Technician sanding a car's rear panel in a body shop", "Zoshua Colah", "CNciVh_m1rU"),
    "detail": ("Detailer polishing a car's hood with an orbital buffer", "Luay Barani", "iXpjQNP__EQ"),
}

def art(key, label):
    alt, by, _ = SERVICE_PHOTOS[key]
    return (f'<figure class="art"><img src="img/services/{key}.webp" alt="{html.escape(alt)}" width="800" height="600" loading="eager" decoding="async">'
            f'</figure>')  # credits kept in img/services/credits.md (Unsplash License needs no on-page credit)

def svc_card(i, s, show_signs=True, cls=""):
    key, cat, name, desc, signs = s
    signs_html = ""
    if show_signs:
        signs_html = ('<div class="signs-label">Signs you need it</div><ul class="signs">'
                      + "".join(f"<li>{html.escape(x)}</li>" for x in signs) + "</ul>")
    tag = "article" if show_signs else "a"
    href = "" if show_signs else f' href="services.html#{key}"'
    return (f'<{tag} class="svc reveal {cls}" id="{key}" data-cat="{cat}"{href}>{art(key, name)}'
            f'<div class="body"><div class="meta"><span>{html.escape(CATS[cat])}</span><span>No. {i:02d}</span></div>'
            f'<h3>{html.escape(name)}</h3><p>{html.escape(desc)}</p>{signs_html}</div></{tag}>')

# ---------------------------------------------------------------- photo slots
GLYPHS = {
    "bay": '<path d="M14.7 6.3a4 4 0 0 0-5.4 5.4L3 18l3 3 6.3-6.3a4 4 0 0 0 5.4-5.4l-2.6 2.6-2.4-.6-.6-2.4z"/>',
    "people": '<circle cx="9" cy="8" r="3.2"/><circle cx="16.5" cy="9" r="2.6"/><path d="M3 20c0-3.3 2.7-6 6-6s6 2.7 6 6M14 14.4c.8-.3 1.6-.4 2.5-.4 2.8 0 4.5 2.2 4.5 5"/>',
    "store": '<path d="M3 21V9l9-6 9 6v12M7 21v-7h10v7M7 17h10"/>',
    "disc": '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="3"/>',
    "engine": '<rect x="3" y="7" width="18" height="11" rx="1"/><path d="M7 7V4h5v3M3 12H1M23 12h-2"/>',
    "car": '<path d="M5 17h14v-4l-2-5H7l-2 5zM3 17h18"/><circle cx="7.5" cy="17.5" r="1.5"/><circle cx="16.5" cy="17.5" r="1.5"/>',
    "spark": '<path d="M12 3l1.8 4.7L18 9l-4.2 1.3L12 15l-1.8-4.7L6 9l4.2-1.3zM18 15l.8 2 2 .8-2 .8-.8 2-.8-2-2-.8 2-.8z"/>',
}
def img_size(path):
    from PIL import Image
    with Image.open(os.path.join(HERE, path)) as im:
        return im.size

def real(src, alt, cls="", caption="", eager=False):
    # Only the brothers' portrait keeps a name caption; other photos stay clean.
    cap = f"<figcaption>{html.escape(caption)}</figcaption>" if caption and "why-photo" in cls else ""
    w, h = img_size(f"img/{src}.webp")
    return (f'<figure class="photo has-img {cls}"><img src="img/{src}.webp" alt="{html.escape(alt)}" width="{w}" height="{h}" loading="eager" decoding="async">{cap}</figure>')

PHOTOS = {
    "storefront": ("The N&A Service Station storefront on Howard Street, with signs over each bay", "The shop on Howard St"),
    "street-view": ("N&A Service Station seen from across Howard Street", "From across Howard St"),
    "red-car-lift": ("A red sedan on a lift with its front wheel off in the N&A service bay", "Brake and tire work"),
    "shop-bay": ("Inside the shop: blue lifts, cars in every bay and tool carts along the wall", "The service bays"),
    "bay-door": ("A mechanic working under the hood of an SUV at the open bay door", "Under the hood"),
    "brothers-oil-change": ("Nabeel and Aqeel Attiya doing an oil change on a BMW", "Oil change in progress"),
}
def strip_gallery(wide="storefront", a="shop-bay", b="bay-door"):
    return ('<div class="strip-gallery">'
            + real(wide, PHOTOS[wide][0], "wide reveal", PHOTOS[wide][1])
            + real(a, PHOTOS[a][0], "reveal", PHOTOS[a][1])
            + real(b, PHOTOS[b][0], "reveal", PHOTOS[b][1])
            + "</div>")

def photo(n, label, glyph, cls=""):
    return (f'<div class="photo {cls}" role="img" aria-label="Photo placeholder: {html.escape(label)}">'
            f'<svg class="glyph" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" aria-hidden="true">{GLYPHS[glyph]}</svg>'
            f'<div class="tag"><b>PHOTO {n}</b>{html.escape(label)}</div></div>')

# ---------------------------------------------------------------- shared partials
NAV = [("index.html", "Home"), ("services.html", "Services"), ("about.html", "About"), ("contact.html", "Hours & contact")]

def header(active):
    links = "".join(f'<a class="nav-link" href="{h}"{" aria-current=\"page\"" if h == active else ""}>{html.escape(t)}</a>' for h, t in NAV)
    mlinks = "".join(f'<li><a href="{h}"{" aria-current=\"page\"" if h == active else ""}>{html.escape(t)}</a></li>' for h, t in NAV)
    return f'''<div class="strip"><div class="wrap">
  <span class="status"><span class="dot" data-open-dot></span><span data-open-text>Mon–Sat 7am–6pm · Sun 8am–1pm</span></span>
  <span class="addr">1701 W Howard St<span class="addr-city">, Evanston, IL 60202</span></span>
</div></div>
<header class="site">
  <div class="wrap">
    <a class="brand brand-logo" href="index.html" aria-label="N&amp;A Auto Repair &amp; Towing Service, home">
      <span class="logo-set logo-blue"><img class="logo-light" src="img/logo/logo-light.svg" alt="N&amp;A Auto Repair &amp; Towing Service" width="763" height="164"><img class="logo-dark" src="img/logo/logo-dark.svg" alt="" width="763" height="164" aria-hidden="true"></span>
      <span class="logo-set logo-red"><img class="logo-light" src="img/logo/logo-red-light.svg" alt="N&amp;A Auto Repair &amp; Towing Service" width="763" height="164"><img class="logo-dark" src="img/logo/logo-red-dark.svg" alt="" width="763" height="164" aria-hidden="true"></span>
    </a>
    <nav class="primary" aria-label="Main">
      {links}
      <a class="btn btn-signal" href="{TEL}">{PHONE_ICON}<span class="num">{PHONE}</span></a>
      <button class="menu-btn" id="menu-btn" type="button" aria-expanded="false" aria-controls="mobile-nav"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg><span class="txt">Menu</span></button>
    </nav>
  </div>
  <nav class="mobile-nav" id="mobile-nav" aria-label="Main" hidden><div class="wrap"><ul>{mlinks}</ul></div></nav>
</header>'''

def cta(title="Car acting up? Call the shop."):
    return f'''<section class="cta"><div class="wrap">
  <h2>{title}</h2>
  <div class="actions" style="margin-top:0">
    <a class="btn btn-ink" href="{TEL}">{PHONE_ICON}Call {PHONE}</a>
    <a class="btn btn-ghost" href="{MAPS}" target="_blank" rel="noopener">Get directions</a>
  </div>
</div></section>'''

FOOTER = f'''<footer class="site">
  <div class="wrap cols">
    <div>
      <div class="big-name">N&amp;A Auto Repairs</div>
      <p>Family-owned auto repair on Howard Street, Evanston.</p>
    </div>
    <div><h2 class="ftitle">Visit</h2><ul><li>1701 W Howard St</li><li>Evanston, IL 60202</li><li><a href="{MAPS}" target="_blank" rel="noopener">Directions</a></li></ul></div>
    <div><h2 class="ftitle">Hours</h2><ul><li>Mon–Sat 7am–6pm</li><li>Sun 8am–1pm</li><li><a href="{TEL}">{PHONE}</a></li></ul></div>
    <div><h2 class="ftitle">Pages</h2><ul>{"".join(f'<li><a href="{h}">{html.escape(t)}</a></li>' for h, t in NAV)}<li><a href="{INSTA}" target="_blank" rel="noopener">Instagram</a></li></ul></div>
  </div>
  <div class="wrap legal"><span>© <span data-year>2026</span> N&amp;A Auto Repairs Inc.</span><span>Evanston, Illinois</span></div>
</footer>
<div class="callbar">
  <a class="btn btn-signal" href="{TEL}">Call now</a>
  <a class="btn btn-ghost" href="{MAPS}" target="_blank" rel="noopener">Directions</a>
</div>
<div class="switcher" role="group" aria-label="Design direction (preview only)">
  <span class="lbl">Design</span>
  <button type="button" data-style="d" aria-pressed="true">Shop Blue</button>
  <button type="button" data-style="a" aria-pressed="false">Shop Ticket</button>
  <button type="button" data-style="b" aria-pressed="false">Showroom</button>
  <button type="button" data-style="c" aria-pressed="false">Blueprint</button>
</div>
<script src="site.js"></script>'''

EARLY = '<script>(function(){var s="d";try{s=localStorage.getItem("na-style-v3")||"d"}catch(e){}var h=location.hash.match(/^#style-([abcd])$/);if(h)s=h[1];document.documentElement.setAttribute("data-style",s)})()</script>'

# --staging builds the review copy on David's subdomain: hidden from search engines so it never competes with the real domain.
STAGING = "--staging" in sys.argv
SITE = "https://naauto.davidfonseca.io" if STAGING else "https://naautorepair.com"
SCHEMA = {
    "@context": "https://schema.org", "@type": "AutoRepair", "@id": SITE + "/#shop",
    "name": "N&A Auto Repairs", "url": SITE + "/", "telephone": "+1-847-859-6191",
    "image": SITE + "/img/storefront.webp",
    "logo": SITE + "/android-chrome-512x512.png",
    "address": {"@type": "PostalAddress", "streetAddress": "1701 W Howard St", "addressLocality": "Evanston",
                "addressRegion": "IL", "postalCode": "60202", "addressCountry": "US"},
    "openingHoursSpecification": [
        {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"], "opens": "07:00", "closes": "18:00"},
        {"@type": "OpeningHoursSpecification", "dayOfWeek": "Sunday", "opens": "08:00", "closes": "13:00"}],
    "founder": [{"@type": "Person", "name": "Nabeel Attiya"}, {"@type": "Person", "name": "Aqeel Attiya"}],
    "foundingDate": "2020",
    "sameAs": ["https://www.instagram.com/na_auto_repairs/"],
}

def head(title, desc, name="index.html"):
    import json
    path = "/" if name == "index.html" else "/" + name
    seo = ""
    if STANDALONE or name != "index.html":
        seo = f'''<link rel="canonical" href="{SITE}{path}">
<link rel="icon" href="favicon.ico" sizes="48x48">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<link rel="manifest" href="site.webmanifest">
<meta name="theme-color" content="#1F4FA3">
<meta property="og:type" content="website">
<meta property="og:site_name" content="N&amp;A Auto Repairs">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{SITE}{path}">
<meta property="og:image" content="{SITE}/img/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="N&amp;A Auto Repair &amp; Towing Service logo">
<meta name="twitter:card" content="summary_large_image">'''
    if name == "index.html":
        seo += "\n<script type=\"application/ld+json\">" + json.dumps(SCHEMA) + "</script>"
    if STAGING:
        seo = '<meta name="robots" content="noindex, nofollow">\n' + seo
    return f'''<title>{title}</title>
<meta name="claude:viewport-fit-sides" content="cover">
<meta name="description" content="{html.escape(desc)}">
{seo}
{EARLY}
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONTS}">
<link rel="stylesheet" href="styles.css">'''

def page(name, title, desc, body, wrap):
    inner = head(title, desc, name) + "\n" + body + "\n" + FOOTER + "\n"
    if wrap:
        inner = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
                 '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
                 + inner.replace("<link rel=\"stylesheet\" href=\"styles.css\">", "<link rel=\"stylesheet\" href=\"styles.css\">\n</head>\n<body>", 1)
                 + "</body>\n</html>\n")
    with open(os.path.join(OUT, name), "w") as f:
        f.write(inner)

# ---------------------------------------------------------------- pages
QUOTES = [
    ("They are very friendly and really make you feel like your vehicle is being taken care of.", "Aug 2023"),
    ("Both of the brothers that work here are extremely helpful when something happens to my car.", "Feb 2024"),
    ("Great customer service and really a life-saver when I was in a tough situation!", "Nov 2023"),
]
def reviews_band(link=True):
    q = "".join(f'<figure class="quote reveal"><blockquote>“{html.escape(t)}”</blockquote><cite>GOOGLE REVIEW · {d.upper()}</cite></figure>' for t, d in QUOTES)
    more = f'<a class="btn btn-ghost more" href="{MAPS}" target="_blank" rel="noopener">Read all reviews on Google</a>' if link else ""
    return f'''<section class="section reviews" id="reviews"><div class="wrap">
  <div class="section-head"><span class="eyebrow">What customers say</span><h2>Evanston's most reliable auto shop</h2></div>
  <div class="score"><span class="big" data-count="4.8">4.8</span><span class="stars" aria-label="4.8 out of 5 stars">★★★★★</span><span class="src">AVERAGE RATING ON GOOGLE</span></div>
  <div class="quotes">{q}</div>
  {more}
</div></section>'''

REASONS = f'''<div class="reasons">
  <div class="reason reveal"><span class="ic"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="12" cy="13" r="8"/><path d="M12 9v4l2.5 2.5M9 2h6"/></svg></span>
    <div><h3>Quick service</h3><p>Most repairs are finished the same day, so you're back on the road instead of waiting on a callback.</p></div></div>
  <div class="reason reveal"><span class="ic"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M20.6 13.4 13.4 20.6a2 2 0 0 1-2.8 0L3 13V3h10l7.6 7.6a2 2 0 0 1 0 2.8z"/><circle cx="7.5" cy="7.5" r="1.5"/></svg></span>
    <div><h3>Fair prices</h3><p>Competitive rates and a clear quote up front. You approve the work before we pick up a wrench.</p></div></div>
  <div class="reason reveal"><span class="ic"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M14.7 6.3a4 4 0 0 0-5.4 5.4L3 18l3 3 6.3-6.3a4 4 0 0 0 5.4-5.4l-2.6 2.6-2.4-.6-.6-2.4z"/></svg></span>
    <div><h3>Expert mechanics</h3><p>Experienced technicians who find the real problem and walk you through what they found.</p></div></div>
</div>'''

HOURS_TABLE = '''<table class="hours"><caption class="eyebrow">Shop hours</caption><tbody>
<tr data-day="1"><td>Monday</td><td>7:00 am – 6:00 pm</td></tr>
<tr data-day="2"><td>Tuesday</td><td>7:00 am – 6:00 pm</td></tr>
<tr data-day="3"><td>Wednesday</td><td>7:00 am – 6:00 pm</td></tr>
<tr data-day="4"><td>Thursday</td><td>7:00 am – 6:00 pm</td></tr>
<tr data-day="5"><td>Friday</td><td>7:00 am – 6:00 pm</td></tr>
<tr data-day="6"><td>Saturday</td><td>7:00 am – 6:00 pm</td></tr>
<tr data-day="0"><td>Sunday</td><td>8:00 am – 1:00 pm</td></tr>
</tbody></table>
<div class="now"><span class="dot" data-open-dot></span><span data-open-text>Mon–Sat 7am–6pm · Sun 8am–1pm</span></div>'''

def ticker():
    items = "".join(f"<li>{html.escape(s[2])}</li>" for s in SERVICES)
    return f'<div class="ticker" aria-hidden="true"><div class="ticker-track"><ul>{items}</ul><ul>{items}</ul></div></div>'

def build():
    os.makedirs(OUT, exist_ok=True)
    by_key = {s[0]: (i + 1, s) for i, s in enumerate(SERVICES)}

    # Home
    featured = "".join(svc_card(by_key[k][0], by_key[k][1], show_signs=False) for k in FEATURED)
    home = header("index.html") + f'''
<main>
<section class="hero"><div class="wrap hero-grid">
  <div>
    <span class="eyebrow rise">Family-owned auto repair · Howard Street, Evanston</span>
    <h1><span class="line rise d1">Auto repair</span> <span class="line rise d2">you can trust</span> <span class="line rise d3">in <span class="hl">Evanston.</span></span></h1>
    <p class="lede rise d3">Honest work, fair prices, and repairs explained in plain English. From brakes to engines, we’ve got you covered.</p>
    <div class="actions rise d4">
      <a class="btn btn-signal" href="{TEL}">{PHONE_ICON}Call {PHONE}</a>
      <a class="btn btn-ghost" href="services.html">See all services</a>
    </div>
    <div class="facts rise d5">
      <div><b>4.8★</b><span>Google rating</span></div>
      <div><b>7 days</b><span>Open every day of the week</span></div>
      <div><b>15</b><span>Services under one roof</span></div>
    </div>
  </div>
  <div class="hero-photo-wrap rise d2">
    {real("brothers-oil-change", "Nabeel and Aqeel Attiya doing an oil change on a BMW", "hero-photo", eager=True)}
    <aside class="ticket" aria-label="Featured review">
      <div class="t-head"><span>Google review</span><span>Feb 2024</span></div>
      <div class="stars" aria-label="5 out of 5 stars">★★★★★</div>
      <p>“Both of the brothers that work here are extremely helpful when something happens to my car.”</p>
    </aside>
  </div>
</div></section>
{ticker()}
<section class="section" id="services"><div class="wrap">
  <div class="section-row">
    <div class="section-head"><span class="eyebrow">What we fix</span><h2>Popular services</h2><p>From routine maintenance to major repairs, here's what drivers bring us most.</p></div>
    <a class="arrow-link" href="services.html">All 15 services <span aria-hidden="true">→</span></a>
  </div>
  <div class="svc-grid">{featured}</div>
</div></section>
<section class="section tight-top" id="why"><div class="wrap why-grid">
  <div class="reveal">{real("brothers", "Nabeel and Aqeel Attiya standing arms crossed in their shop", "why-photo", "Nabeel & Aqeel Attiya")}</div>
  <div>
    <div class="section-head"><span class="eyebrow">Why drivers come back</span><h2>Run by brothers, not a chain</h2></div>
    {REASONS}
    <p style="margin-top:28px"><a class="arrow-link" href="about.html">Our story <span aria-hidden="true">→</span></a></p>
  </div>
</div></section>
<section class="section tight-top" id="shop"><div class="wrap">
  <div class="section-head"><span class="eyebrow">Inside the shop</span><h2>Where the work happens</h2></div>
  {strip_gallery()}
</div></section>
{reviews_band()}
<section class="section" id="visit"><div class="wrap">
  <div class="section-row">
    <div class="section-head"><span class="eyebrow">Hours &amp; location</span><h2>Stop by the shop</h2><p>On Howard Street, steps from the Howard CTA station. Walk-ins welcome; call ahead for bigger jobs.</p></div>
    <a class="arrow-link" href="contact.html">Contact details <span aria-hidden="true">→</span></a>
  </div>
  <div class="visit-grid">
    <div class="card reveal">{HOURS_TABLE}</div>
    {map_card()}
  </div>
</div></section>
</main>
{cta()}'''
    page("index.html", "N&amp;A Auto Repairs | Auto Repair Shop in Evanston, IL" if STANDALONE else "N&amp;A Auto Repairs", "Family-owned auto repair shop at 1701 W Howard St, Evanston, IL. Brakes, engine, A/C, oil changes and more. Open 7 days. Call (847) 859-6191.", home, STANDALONE)

    # Services
    counts = {c: sum(1 for s in SERVICES if s[1] == c) for c in CATS}
    chips = f'<button class="chip" type="button" data-filter="all" aria-pressed="true">All<span class="n">{len(SERVICES)}</span></button>' + "".join(
        f'<button class="chip" type="button" data-filter="{c}" aria-pressed="false">{html.escape(n)}<span class="n">{counts[c]}</span></button>' for c, n in CATS.items())
    cards = "".join(svc_card(i + 1, s) for i, s in enumerate(SERVICES))
    services = header("services.html") + f'''
<main>
<section class="page-hero"><div class="wrap">
  <div class="crumbs rise"><a href="index.html">Home</a> / Services</div>
  <h1 class="rise d1">Auto repair services</h1>
  <p class="rise d2">Fifteen services under one roof, from a quick oil change to transmission work. Not sure what's wrong? Describe what the car is doing and we'll diagnose it.</p>
</div></section>
<section class="section" style="padding-top:40px"><div class="wrap">
  <h2 class="sr-only">All services</h2>
  <div class="filters" role="group" aria-label="Filter services">{chips}</div>
  <div class="svc-grid">{cards}</div>
</div></section>
<section class="section tight-top"><div class="wrap">
  <div class="section-head"><span class="eyebrow">In the shop</span><h2>Recent work</h2></div>
  {strip_gallery("red-car-lift", "brothers-oil-change", "bay-door")}
</div></section>
<section class="section tight-top"><div class="wrap">
  <div class="section-head"><span class="eyebrow">How a repair works</span><h2>Three steps, no surprises</h2></div>
  <div class="steps">
    <div class="step reveal"><span class="n">Step 1</span><h3>Call or drop in</h3><p>Tell us what the car is doing. Walk-ins are welcome seven days a week.</p></div>
    <div class="step reveal"><span class="n">Step 2</span><h3>We diagnose &amp; quote</h3><p>We find the actual problem and give you a clear price before any work starts.</p></div>
    <div class="step reveal"><span class="n">Step 3</span><h3>Back on the road</h3><p>Most jobs are done the same day. We walk you through what we fixed.</p></div>
  </div>
</div></section>
</main>
{cta("Don't see your problem listed? Call and ask.")}'''
    page("services.html", "Auto Repair Services in Evanston, IL | N&amp;A Auto Repairs", "Brake repair, engine and transmission work, A/C, electrical, tires, alignment, oil changes, glass, body work and detailing in Evanston, IL.", services, True)

    # About
    gallery = strip_gallery("street-view", "brothers-oil-change", "shop-bay")
    about = header("about.html") + f'''
<main>
<section class="page-hero"><div class="wrap">
  <div class="crumbs rise"><a href="index.html">Home</a> / About</div>
  <h1 class="rise d1">Two brothers, one shop</h1>
  <p class="rise d2">N&amp;A Auto Repairs is a family business on Howard Street, right where Evanston meets Chicago.</p>
</div></section>
<section class="section"><div class="wrap story">
  <div class="prose reveal">
    <p>N&amp;A is run by brothers Nabeel and Aqeel Attiya, who work on the cars themselves.</p>
    <p>They opened at 1701 W Howard St in 2020. The goal is simple: find the real problem, quote a fair price and get people back on the road quickly.</p>
    <p>Customers mention the same thing again and again in reviews: the brothers are friendly, they explain what's going on, and they help out when you're in a tough spot.</p>
  </div>
  <div class="reveal">{real("brothers", "Nabeel and Aqeel Attiya standing arms crossed in their shop", "why-photo", "Nabeel & Aqeel Attiya")}</div>
</div></section>
<section class="section tight-top"><div class="wrap why-grid">
  <div>
    <div class="section-head"><span class="eyebrow">At a glance</span><h2>The shop</h2></div>
    <ul class="timeline">
      <li class="reveal"><span class="when">2020</span><b>N&amp;A Auto Repairs Inc. opens on Howard Street</b></li>
      <li class="reveal"><span class="when">Today</span><b>15 services, open 7 days a week</b></li>
      <li class="reveal"><span class="when">Google</span><b>4.8★ average rating from local drivers</b></li>
    </ul>
  </div>
  <div>
    <div class="section-head"><span class="eyebrow">What we promise</span><h2>Why drivers come back</h2></div>
    {REASONS}
  </div>
</div></section>
{reviews_band()}
<section class="section" id="gallery"><div class="wrap">
  <div class="section-head"><span class="eyebrow">Inside the shop</span><h2>Photos</h2></div>
  {gallery}
</div></section>
</main>
{cta()}'''
    page("about.html", "About Us | N&amp;A Auto Repairs, Evanston IL", "N&A Auto Repairs is a family-owned shop run by brothers Nabeel and Aqeel Attiya on Howard Street in Evanston since 2020.", about, True)

    # Contact
    contact = header("contact.html") + f'''
<main>
<section class="page-hero"><div class="wrap">
  <div class="crumbs rise"><a href="index.html">Home</a> / Hours &amp; contact</div>
  <h1 class="rise d1">Hours &amp; contact</h1>
  <p class="rise d2">Call, or just pull in. We're open seven days a week on Howard Street, steps from the Howard CTA station.</p>
</div></section>
<section class="section" style="padding-top:40px"><div class="wrap">
  <div class="visit-grid">
    <div class="card contact-list reveal">
      <div class="contact-row">
        <div class="eyebrow">Phone</div>
        <div class="phone-row"><span class="val" id="phone">{PHONE}</span><button class="copy" type="button" data-copy="phone">Copy number</button></div>
      </div>
      <div class="contact-row">
        <div class="eyebrow">Address</div>
        <div class="val">1701 W Howard St<br>Evanston, IL 60202</div>
        <div class="links">
          <a class="btn btn-signal" href="{MAPS}" target="_blank" rel="noopener">Open in Google Maps</a>
          <a class="btn btn-ghost" href="{INSTA}" target="_blank" rel="noopener">Instagram</a>
        </div>
      </div>
    </div>
    <div class="card reveal">{HOURS_TABLE}</div>
  </div>
</div></section>
<section class="section tight-top" id="map"><div class="wrap">
  <div class="section-head"><span class="eyebrow">Find us</span><h2>Look for the red N&amp;A sign</h2><p>Five service bays facing Howard Street, a short walk from the Howard CTA station.</p></div>
  <div class="map-grid">
    {map_card()}
    {real("storefront", PHOTOS["storefront"][0], "reveal map-photo", "1701 W Howard St")}
  </div>
</div></section>
<section class="section tight-top" id="request"><div class="wrap visit-grid">
  <div class="card reveal">
    <div class="section-head" style="margin-bottom:24px"><span class="eyebrow">Request an appointment</span><h2>We'll call you back</h2><p>Send the details and the shop will call to confirm a time and a price.</p></div>
    {request_form()}
  </div>
  <div>
    <div class="section-head"><span class="eyebrow">Before you call</span><h2>Have this ready</h2><p>It helps us give you a faster, more accurate answer over the phone.</p></div>
    <ul class="checklist">
      <li class="reveal"><span class="tick">✓</span><div><b>Year, make and model</b><span class="sub">Mileage too, if you know it.</span></div></li>
      <li class="reveal"><span class="tick">✓</span><div><b>What the car is doing</b><span class="sub">Noises, smells, warning lights, and when it happens.</span></div></li>
      <li class="reveal"><span class="tick">✓</span><div><b>When you need it back</b><span class="sub">Most jobs are done the same day.</span></div></li>
    </ul>
  </div>
</div></section>
</main>
{cta("See you on Howard Street.")}'''
    page("contact.html", "Hours, Directions & Contact | N&amp;A Auto Repairs Evanston", "Hours, phone and directions for N&A Auto Repairs, 1701 W Howard St, Evanston, IL 60202. Open 7 days. Request an appointment online.", contact, True)

MAP_EMBED = "https://www.google.com/maps?q=N%26A+Auto+Repairs,+1701+W+Howard+St,+Evanston,+IL+60202&amp;output=embed"

def map_card():
    if EMBED_MAP:
        return (f'<div class="card map-live reveal"><iframe title="Map showing N&amp;A Auto Repairs at 1701 W Howard St, Evanston" '
                f'src="{MAP_EMBED}" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe></div>')
    return f'''<div class="card map-card reveal">
  <div class="map-top"><div class="eyebrow">Find us</div><div class="contact-row"><div class="val">1701 W Howard St<br>Evanston, IL 60202</div></div></div>
  <div class="road" aria-hidden="true"><span>W HOWARD ST</span></div>
  <div class="pin" aria-hidden="true"></div>
  <div class="map-foot"><span class="eyebrow">Live Google map shows here on the published site</span><a class="btn btn-signal" href="{MAPS}" target="_blank" rel="noopener">Directions</a></div>
</div>'''

SERVICE_OPTIONS = ["Not sure / diagnosis"] + [s[2] for s in SERVICES]

def request_form():
    opts = "".join(f"<option>{html.escape(o)}</option>" for o in SERVICE_OPTIONS)
    return f'''<form class="req-form" id="request-form" name="appointment" method="post" novalidate>
  <div class="field"><label for="rf-name">Name</label><input id="rf-name" name="name" autocomplete="name" required placeholder="Jordan Smith"></div>
  <div class="field"><label for="rf-phone">Phone</label><input id="rf-phone" name="phone" type="tel" autocomplete="tel" required placeholder="(847) 555-0134"></div>
  <div class="field"><label for="rf-car">Year, make and model</label><input id="rf-car" name="vehicle" placeholder="2016 Honda Accord"></div>
  <div class="field"><label for="rf-svc">Service</label><select id="rf-svc" name="service">{opts}</select></div>
  <div class="field"><label for="rf-day">Preferred day</label><input id="rf-day" name="day" type="date"></div>
  <div class="field full"><label for="rf-msg">What's the car doing?</label><textarea id="rf-msg" name="message" rows="4" placeholder="Grinding noise when I brake, mostly at low speed."></textarea></div>
  <div class="full form-foot"><button class="btn btn-signal" type="submit">Send request</button><span class="form-note" id="rf-status" role="status">Prefer to talk? Call {PHONE}.</span></div>
</form>'''

if __name__ == "__main__":
    build()
    import shutil
    for f in ("styles.css", "site.js"):
        shutil.copy(os.path.join(HERE, f), os.path.join(OUT, f))
    shutil.copytree(os.path.join(HERE, "img"), os.path.join(OUT, "img"), dirs_exist_ok=True)
    # Favicons from the brand kit live at the site root; the share image goes with the other images.
    fav = os.path.join(HERE, "brand-kit", "03-favicons")
    for f in os.listdir(fav):
        shutil.copy(os.path.join(fav, f), os.path.join(OUT, f))
    shutil.copy(os.path.join(HERE, "brand-kit", "png", "04-social", "og-image-1200x630.png"), os.path.join(OUT, "img", "og-image.png"))
    with open(os.path.join(OUT, "robots.txt"), "w") as f:
        f.write("User-agent: *\nDisallow: /\n" if STAGING else f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n")
    # Staging stays out of search engines, so it gets no sitemap.
    if not STAGING:
        urls = "".join(f"  <url><loc>{SITE}{'/' if h == 'index.html' else '/' + h}</loc></url>\n" for h, _ in NAV)
        with open(os.path.join(OUT, "sitemap.xml"), "w") as f:
            f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + urls + "</urlset>\n")
    print("built", sorted(os.listdir(OUT)))
