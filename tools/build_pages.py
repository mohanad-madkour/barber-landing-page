"""Generate a standalone page for each home-page section, in English and Arabic:

    English  /about/  /services/  /branches/  /locations/  /reviews/  /contact/
    Arabic   /ar/about/  /ar/services/  ...

Each page is cut from the home page itself (index.html / ar/index.html): same head,
header, footer and scripts, plus that one section — so content never drifts.
Run tools/build_ar.py first (tools/build.py runs everything in order).
"""
import io
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://barberegypt.com"
SECTIONS = ["about", "services", "branches", "locations", "reviews", "contact"]

SERVICES = [  # same list and prices as main.js: (english, arabic, price)
    ("Haircut", "قص شعر", "180"), ("Haircut + Beard", "شعر + دقن", "300"), ("Beard", "دقن", "150"),
    ("Blow-dry", "سشوار", "120"), ("Protein Treatment", "بروتين", "1000"), ("Hair Color", "صبغة شعر", "300"),
    ("Beard Color", "صبغة دقن", "150"), ("Facial Cleansing", "تنظيف بشرة", "350"),
]

META = {
    "about": {
        "en": ("About BARBER — Men's Barbershop in Madinaty",
               "BARBER is a men's barbershop with 5 branches across Madinaty, New Cairo: skilled barbers, sanitized tools and a clean, comfortable space."),
        "ar": ("عن BARBER — حلاق رجالي في مدينتي",
               "BARBER حلاق رجالي بـ 5 فروع في مدينتي: حلاقين محترفين، أدوات معقمة، ومكان نضيف ومريح في كل زيارة."),
    },
    "services": {
        "en": ("Services & Prices — BARBER Madinaty",
               "BARBER Madinaty prices: haircut 180 EGP, haircut + beard 300, beard 150, blow-dry 120, hair color 300, facial cleansing 350, protein treatment 1000."),
        "ar": ("الخدمات والأسعار — BARBER مدينتي",
               "أسعار BARBER مدينتي: قص شعر 180 جنيه، شعر + دقن 300، دقن 150، سشوار 120، صبغة شعر 300، تنظيف بشرة 350، بروتين 1000."),
    },
    "branches": {
        "en": ("Our 5 Branches in Madinaty — BARBER",
               "BARBER has 5 branches in Madinaty: B8, B10, B12, B15 and Craft Zone. Open a branch for its address, hours and directions."),
        "ar": ("فروع BARBER الخمسة في مدينتي",
               "فروع BARBER في مدينتي: B8، B10، B12، B15 وCraft Zone. افتح صفحة أي فرع عشان تشوف العنوان والمواعيد والاتجاهات."),
    },
    "locations": {
        "en": ("Locations & Map — BARBER Madinaty",
               "Find the nearest BARBER branch in Madinaty on the map — B8, B10, B12, B15 and Craft Zone, open daily."),
        "ar": ("مواقع فروع BARBER على الخريطة — مدينتي",
               "اعرف أقرب فرع BARBER ليك في مدينتي على الخريطة — B8، B10، B12، B15 وCraft Zone، مفتوحين يوميًا."),
    },
    "reviews": {
        "en": ("Client Reviews — BARBER Madinaty",
               "What clients say about BARBER Madinaty — verified Google reviews from our branches."),
        "ar": ("آراء العملاء — BARBER مدينتي",
               "آراء عملاء BARBER مدينتي — تقييمات حقيقية من جوجل لفروعنا."),
    },
    "contact": {
        "en": ("Contact & Working Hours — BARBER Madinaty",
               "Contact BARBER Madinaty on WhatsApp +20 11 5912 5229 or Instagram @barber._.eg. Open daily 1 PM – 1 AM (Craft Zone 11 AM – 2 AM)."),
        "ar": ("تواصل ومواعيد العمل — BARBER مدينتي",
               "تواصل مع BARBER مدينتي على واتساب ‎+20 11 5912 5229‎ أو إنستجرام @barber._.eg. مفتوحين يوميًا من 1 الظهر لـ 1 بالليل (Craft Zone من 11 الصبح لـ 2 بالليل)."),
    },
}


def url(section, lang):
    return SITE + ("/ar/" if lang == "ar" else "/") + section + "/"


def one(pattern, s, what):
    m = re.search(pattern, s, re.S)
    if not m:
        raise SystemExit("could not find " + what)
    return m


def build(section, lang):
    s = io.open(os.path.join(ROOT, "index.html" if lang == "en" else os.path.join("ar", "index.html")),
                encoding="utf-8", newline="").read()
    title, desc = META[section][lang]
    page_url = url(section, lang)
    home = "/ar/" if lang == "ar" else "/"
    prefix = "/ar/" if lang == "ar" else "/"

    # ---- head ----
    head_end = s.index("</head>")
    head, rest = s[:head_end], s[head_end:]
    head = re.sub(r"<title>.*?</title>", lambda m: "<title>%s</title>" % title, head, count=1)
    head = re.sub(r'(<meta name="description" content=")[^"]*', lambda m: m.group(1) + desc, head, count=1)
    head = re.sub(r'(<meta (?:property="og:title"|name="twitter:title") content=")[^"]*', lambda m: m.group(1) + title, head)
    head = re.sub(r'(<meta (?:property="og:description"|name="twitter:description") content=")[^"]*', lambda m: m.group(1) + desc, head)
    head = re.sub(r'(<link rel="canonical" href=")[^"]*', lambda m: m.group(1) + page_url, head, count=1)
    head = re.sub(r'(<meta property="og:url" content=")[^"]*', lambda m: m.group(1) + page_url, head, count=1)
    head = re.sub(r'(<link rel="alternate" hreflang="(en|x-default)" href=")[^"]*', lambda m: m.group(1) + url(section, "en"), head)
    head = re.sub(r'(<link rel="alternate" hreflang="ar" href=")[^"]*', lambda m: m.group(1) + url(section, "ar"), head)
    # the WebSite (site name) schema belongs on the home page only
    head = re.sub(r'\s*<!-- schema.org WebSite.*?</script>', "", head, flags=re.S)
    if section != "locations":   # the map library is only needed on the map page
        head = re.sub(r'\s*<link rel="stylesheet" href="[^"]*leaflet[^"]*" />', "", head)
        rest = re.sub(r'\s*<script defer src="[^"]*leaflet[^"]*"></script>', "", rest)

    # ---- body: sprite + header, the one section, footer + scripts ----
    body_top = one(r"<body>.*?</header>", rest, "header").group(0)
    sec = one(r'<section class="[^"]*" id="%s">.*?</section>' % section, rest, "section " + section).group(0)
    body_end = one(r"\s*<!-- ============ FOOTER ============ -->.*", rest, "footer").group(0)

    body_top = body_top.replace("<body>", '<body class="subpage">', 1)
    # the section heading becomes the page's h1
    sec = re.sub(r'<h2 class="section__title"(.*?)</h2>', r'<h1 class="section__title"\1</h1>', sec, count=1, flags=re.S)
    if section == "services":   # bake the price list into the HTML (main.js re-renders the same rows)
        rows = "".join(
            '<div class="srv-row"><span class="srv-name">%s</span><span class="srv-dots" aria-hidden="true"></span>'
            '<span class="srv-price">%s <em>EGP</em></span></div>' % (ar if lang == "ar" else en, price)
            for en, ar, price in SERVICES)
        sec = sec.replace('<div class="services__rows" id="servicesGrid"></div>',
                          '<div class="services__rows" id="servicesGrid">%s</div>' % rows)

    out = head + body_top + '\n\n  <main class="subpage__main">\n  ' + sec + "\n  </main>\n" + body_end
    # in-page anchors now point at the matching page; the logo goes home
    out = out.replace('href="#hero"', 'href="%s"' % home)
    out = re.sub(r'<a ([^>]*)href="#(%s)"' % "|".join(SECTIONS),
                 lambda m: '<a %shref="%s%s/"' % (m.group(1), prefix, m.group(2)), out)
    # pages live one folder down: make local asset paths root-absolute
    out = re.sub(r'((?:src|href|poster)=")(?=(?:css|js|images|logo-layers|videos)/)', r"\g<1>/", out)

    folder = os.path.join(ROOT, "ar", section) if lang == "ar" else os.path.join(ROOT, section)
    os.makedirs(folder, exist_ok=True)
    io.open(os.path.join(folder, "index.html"), "w", encoding="utf-8", newline="").write(out)
    print("wrote", os.path.relpath(os.path.join(folder, "index.html"), ROOT))


def main():
    for section in SECTIONS:
        for lang in ("en", "ar"):
            build(section, lang)


if __name__ == "__main__":
    main()
