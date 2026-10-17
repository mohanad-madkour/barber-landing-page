"""Generate one page per branch, in Arabic and English:

    Arabic   /b8/      /b10/      /b12/      /b15/      /craft-zone/
    English  /en/b8/   /en/b10/   /en/b12/   /en/b15/   /en/craft-zone/

Each page targets searches for that branch ("حلاق B15 مدينتي"), carries its own
HairSalon schema, and is the link to put on that branch's Google Business Profile.
The header, footer and floating WhatsApp button are copied from the home pages
(index.html for English, ar/index.html for Arabic) so they stay identical.

Branch data lives in BRANCHES below — edit it (or the home pages), then run:
    python tools/build_ar.py          (if index.html changed)
    python tools/build_branches.py
"""
import html
import io
import json
import os
import re
from urllib.parse import quote

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://barberegypt.com"
PHONE = "+201159125229"
WA = "https://wa.me/201159125229"
INSTAGRAM = "https://www.instagram.com/barber._.eg"
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

HOURS_STD = {"opens": "13:00", "closes": "01:00",
             "ar": "يوميًا من 1 الظهر لحد 1 بالليل", "en": "Daily, 1 PM – 1 AM", "short": "1 PM – 1 AM"}
HOURS_CZ = {"opens": "11:00", "closes": "02:00",
            "ar": "يوميًا من 11 الصبح لحد 2 بالليل", "en": "Daily, 11 AM – 2 AM", "short": "11 AM – 2 AM"}

# geo only where the coordinates are exact (see main.js); others link to their Maps listing
BRANCHES = [
    {"slug": "b8", "name": "B8", "loc_ar": "خلف The Mart", "loc_en": "Behind The Mart",
     "hours": HOURS_STD, "new": True, "map": "https://maps.app.goo.gl/wWXc1byb1pg5qFpL7", "geo": None},
    {"slug": "b10", "name": "B10", "loc_ar": "بجوار New Benny Market", "loc_en": "Next to New Benny Market",
     "hours": HOURS_STD, "new": False, "map": "https://maps.app.goo.gl/CZsrdZdvszbi1Eo69", "geo": (30.0824197, 31.6588338)},
    {"slug": "b12", "name": "B12", "loc_ar": "بجوار بيت الجملة ماركت", "loc_en": "Next to Beit El Gomla Market",
     "hours": HOURS_STD, "new": False, "map": "https://maps.app.goo.gl/RiEPsiAHepFNC2aQ6", "geo": None},
    {"slug": "b15", "name": "B15", "loc_ar": "بجوار محمود الفار ماركت", "loc_en": "Next to Mahmoud El Far Market",
     "hours": HOURS_STD, "new": False, "map": "https://maps.app.goo.gl/6YmmWnykg3egYY6c7", "geo": None},
    {"slug": "craft-zone", "name": "Craft Zone", "loc_ar": "بلوك 2", "loc_en": "Block 2",
     "hours": HOURS_CZ, "new": False, "map": "https://maps.app.goo.gl/fFCBS6Z8sCY5EHpq9", "geo": None},
]

SERVICES = [  # same list and prices as main.js: (arabic, english, price)
    ("قص شعر", "Haircut", "180"), ("شعر + دقن", "Haircut + Beard", "300"), ("دقن", "Beard", "150"),
    ("سشوار", "Blow-dry", "120"), ("بروتين", "Protein Treatment", "1000"), ("صبغة شعر", "Hair Color", "300"),
    ("صبغة دقن", "Beard Color", "150"), ("تنظيف بشرة", "Facial Cleansing", "350"),
]

# real Google reviews already shown on the home page, by branch (verbatim)
REVIEWS = {
    "b15": [
        ("gamal fathy", "ممتازين ما شاء الله، ومحمد محترم وشاطر."),
        ("Eyad Mahmoud", "خدمة متميزة جدًا، قيمة مقابل سعر، والعمالة نضاف جدًا ومهندمين طول الوقت. أنصح بيه جدًا."),
        ("Seif Eldesouky", "كل اللي في المحل ناس محترمة ومتعاونة وأخلاقهم عالية أوي، من أنضف المحلات اللي في مدينتي، وإدارة ناجحة."),
    ],
    "craft-zone": [
        ("Soha Mohamed", "لديهم خبرة جيدة وأسعار مناسبة 👍"),
        ("D A", "Best for kids."),
    ],
}

# UI text per language
T = {
    "ar": {
        "home": "/ar/", "prefix": "/", "other_lang": "en", "locale": "ar_EG",
        "title": "BARBER {name} مدينتي — حلاق رجالي {loc}",
        "desc": "فرع BARBER {name} في مدينتي ({loc}): قص شعر، دقن، صبغة وتنظيف بشرة. {hours}. تواصل معانا على واتساب أو افتح موقع الفرع على الخريطة.",
        "kicker": 'فرع <span dir="ltr">{name}</span> · مدينتي',
        "h1": '<span dir="ltr">BARBER {name}</span> — حلاق رجالي في مدينتي',
        "addr": "{loc}، مدينتي — القاهرة الجديدة",
        "new": "فرع جديد",
        "wa_btn": "تواصل على واتساب", "wa_text": "السلام عليكم، عندي استفسار عن فرع {name}",
        "map_btn": "افتح الفرع على الخريطة",
        "img_alt": "واجهة فرع BARBER {name} في مدينتي",
        "services": "الخدمات والأسعار",
        "services_note": "* قائمة الأسعار الكاملة في الفرع — تواصل على واتساب للتأكيد.",
        "reviews": "آراء زباين فرع {name}", "no_reviews": "جربت فرع {name}؟",
        "no_reviews_p": "رأيك بيفرق معانا وبيساعد غيرك يختار.",
        "review_link": "اكتب تقييمك للفرع على Google ←",
        "others": "فروعنا التانية في مدينتي",
    },
    "en": {
        "home": "/", "prefix": "/en/", "other_lang": "ar", "locale": "en_US",
        "title": "BARBER {name} Madinaty — Men's Barbershop {loc}",
        "desc": "BARBER {name} in Madinaty, New Cairo ({loc}): haircuts, beard styling, color and facials. {hours}. Message us on WhatsApp or open the branch on the map.",
        "kicker": "{name} branch · Madinaty",
        "h1": "BARBER {name} — Men's Barbershop in Madinaty",
        "addr": "{loc}, Madinaty — New Cairo",
        "new": "New branch",
        "wa_btn": "Message us on WhatsApp", "wa_text": "Hi, I have a question about the {name} branch",
        "map_btn": "Open on the map",
        "img_alt": "BARBER {name} storefront in Madinaty",
        "services": "Services & prices",
        "services_note": "* Full price list available in-store — message us on WhatsApp to confirm.",
        "reviews": "What {name} clients say", "no_reviews": "Been to {name}?",
        "no_reviews_p": "Your review helps others choose — and helps us improve.",
        "review_link": "Write a review on Google →",
        "others": "Our other branches in Madinaty",
    },
}

ICON_PIN = '<svg class="bp-ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>'
ICON_CLOCK = '<svg class="bp-ico" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>'
ICON_WA = '<svg class="ico" aria-hidden="true"><use href="#i-whatsapp"/></svg>'
FLAG = {"en": '<span class="fi fi-gb"></span><span class="lang-toggle__txt">English</span>',
        "ar": '<span class="fi fi-eg"></span><span class="lang-toggle__txt">العربية</span>'}

e = html.escape


def is_arabic(text):
    return any("؀" <= c <= "ۿ" for c in text)


def read(path):
    return io.open(os.path.join(ROOT, path), encoding="utf-8", newline="").read()


def grab(s, pattern):
    m = re.search(pattern, s, re.S)
    if not m:
        raise SystemExit("could not find in home page: " + pattern)
    return m.group(0)


def shared_parts(lang, other_url):
    """Header, footer, icon sprite and WhatsApp button, lifted from the home page."""
    t = T[lang]
    s = read("index.html" if lang == "en" else os.path.join("ar", "index.html"))
    sprite = grab(s, r'<svg xmlns="http://www.w3.org/2000/svg" style="display:none">.*?</svg>')
    header = grab(s, r'<header class="header" id="header">.*?</header>')
    footer = grab(s, r'<footer class="footer">.*?</footer>')
    wa = grab(s, r'<a href="https://wa.me/[^"]*"[^>]*class="wa-float".*?</a>')

    def fix(part):
        part = part.replace('href="#hero"', 'href="%s"' % t["home"])
        # section anchors point back to the home page (icon refs like #i-instagram stay local)
        part = re.sub(r'<a ([^>]*)href="#([\w-]+)"', lambda m: '<a %shref="%s#%s"' % (m.group(1), t["home"], m.group(2)), part)
        part = re.sub(r'((?:src|href)=")(?=(?:css|js|images|logo-layers|videos)/)', r"\g<1>/", part)
        return part

    header = fix(header)
    # the home page's language buttons are filled by main.js; here they are plain links
    header = re.sub(r'<button class="lang-toggle( lang-toggle--nav)?" id="(langToggle(?:Nav)?)"[^>]*></button>',
                    lambda m: '<a class="lang-toggle%s" id="%s" href="%s" hreflang="%s">%s</a>'
                    % (m.group(1) or "", m.group(2), other_url, t["other_lang"], FLAG[t["other_lang"]]), header)
    # header stays in its solid "scrolled" look since there is no hero video behind it
    header = header.replace('class="header" id="header"', 'class="header header--scrolled" id="header"')
    return sprite, header, fix(footer), wa


def schema(b, lang):
    url = SITE + T[lang]["prefix"] + b["slug"] + "/"
    data = {
        "@context": "https://schema.org",
        "@type": "HairSalon",
        "@id": SITE + "/" + b["slug"] + "/#branch",   # same entity for both languages
        "name": "BARBER Madinaty — " + b["name"],
        "alternateName": ["باربر " + b["name"] + " مدينتي", "BARBER " + b["name"]],
        "url": url,
        "image": SITE + "/images/branches/" + b["slug"] + ".jpg",
        "telephone": PHONE,
        "priceRange": "EGP 120–1000",
        "address": {
            "@type": "PostalAddress",
            "streetAddress": b["loc_ar"] + "، " + b["name"] + "، مدينتي",
            "addressLocality": "Madinaty",
            "addressRegion": "Cairo Governorate",
            "addressCountry": "EG",
        },
        "hasMap": b["map"],
        "openingHoursSpecification": [{
            "@type": "OpeningHoursSpecification", "dayOfWeek": DAYS,
            "opens": b["hours"]["opens"], "closes": b["hours"]["closes"],
        }],
        "parentOrganization": {"@id": SITE + "/#barber"},
        "sameAs": [INSTAGRAM],
    }
    if b["geo"]:
        data["geo"] = {"@type": "GeoCoordinates", "latitude": b["geo"][0], "longitude": b["geo"][1]}
    return json.dumps(data, ensure_ascii=False, indent=2)


def page(b, lang):
    t = T[lang]
    name, h = b["name"], b["hours"]
    loc = b["loc_" + lang]
    fill = dict(name=name, loc=loc, hours=h[lang])
    url_ar = SITE + "/" + b["slug"] + "/"
    url_en = SITE + "/en/" + b["slug"] + "/"
    url = url_ar if lang == "ar" else url_en
    other_url = ("/en/" if lang == "ar" else "/") + b["slug"] + "/"
    sprite, header, footer, wa_float = shared_parts(lang, other_url)
    wa_link = WA + "?text=" + quote(t["wa_text"].format(**fill))
    rtl = ' dir="rtl"' if lang == "ar" else ""

    services = "\n".join(
        '          <li><span>%s</span><span class="bp-dots" aria-hidden="true"></span><b>%s <small>EGP</small></b></li>'
        % (e(ar if lang == "ar" else en), p) for ar, en, p in SERVICES)

    if b["slug"] in REVIEWS:
        cards = "\n".join(
            '          <figure class="bp-review"><span class="bp-stars" aria-label="5/5">★★★★★</span>'
            '<blockquote dir="%s">%s</blockquote><figcaption dir="ltr">%s · Google</figcaption></figure>'
            % ("rtl" if is_arabic(text) else "ltr", e(text), e(author))
            for author, text in REVIEWS[b["slug"]])
        reviews = ('        <h2>%s</h2>\n        <div class="bp-reviews">\n%s\n        </div>\n'
                   % (e(t["reviews"].format(**fill)), cards))
    else:
        reviews = ('        <h2>%s</h2>\n        <p class="bp-muted">%s</p>\n'
                   % (e(t["no_reviews"].format(**fill)), e(t["no_reviews_p"])))

    others = "\n".join(
        '          <a class="bp-branch" href="%s%s/"><b dir="ltr">%s</b><span>%s</span></a>'
        % (t["prefix"], o["slug"], e(o["name"]), e(o["loc_" + lang])) for o in BRANCHES if o is not b)

    badge = ' <span class="bp-badge">%s</span>' % t["new"] if b["new"] else ""

    return """<!DOCTYPE html>
<html lang="{lang}" dir="ltr">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title}</title>
  <meta name="description" content="{desc}" />
  <meta name="theme-color" content="#141412" />
  <link rel="canonical" href="{url}" />
  <link rel="alternate" hreflang="ar" href="{url_ar}" />
  <link rel="alternate" hreflang="en" href="{url_en}" />
  <link rel="alternate" hreflang="x-default" href="{url_en}" />

  <meta property="og:type" content="website" />
  <meta property="og:url" content="{url}" />
  <meta property="og:site_name" content="BARBER Madinaty" />
  <meta property="og:title" content="{title}" />
  <meta property="og:description" content="{desc}" />
  <meta property="og:image" content="{site}/images/branches/{slug}.jpg" />
  <meta property="og:image:width" content="512" />
  <meta property="og:image:height" content="640" />
  <meta property="og:locale" content="{locale}" />
  <meta name="twitter:card" content="summary_large_image" />

  <link rel="icon" href="/favicon.ico" sizes="48x48" />
  <link rel="icon" type="image/png" sizes="32x32" href="/images/icons/icon-32.png" />
  <link rel="apple-touch-icon" href="/images/icons/icon-180.png" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&family=Poppins:wght@500;600;700;800&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="/css/styles.css?v=64" />
  <link rel="stylesheet" href="/css/branch.css?v=2" />

  <!-- Generated by tools/build_branches.py — edit the script, not this file. -->
  <script type="application/ld+json">
{schema}
  </script>
</head>
<body class="bp">
{sprite}

  {header}

  <main class="container bp-main"{rtl}>
    <section class="bp-hero">
      <img class="bp-hero__img" src="/images/branches/{slug}.jpg" alt="{img_alt}" width="512" height="640" fetchpriority="high" />
      <div class="bp-hero__body">
        <span class="bp-kicker">{kicker}{badge}</span>
        <h1>{h1}</h1>
        <ul class="bp-facts">
          <li>{icon_pin}<span>{addr}</span></li>
          <li>{icon_clock}<span>{hours} <span class="bp-muted" dir="ltr">({hours_short})</span></span></li>
        </ul>
        <div class="bp-cta">
          <a class="btn btn--primary" href="{wa}" target="_blank" rel="noopener">{icon_wa} {wa_btn}</a>
          <a class="btn btn--ghost" href="{map}" target="_blank" rel="noopener">{icon_pin} {map_btn}</a>
        </div>
      </div>
    </section>

    <section class="bp-section">
      <h2>{services_h}</h2>
      <ul class="bp-services">
{services}
      </ul>
      <p class="bp-muted bp-small">{services_note}</p>
    </section>

    <section class="bp-section">
{reviews}        <a class="bp-link" href="{map}" target="_blank" rel="noopener">{review_link}</a>
    </section>

    <section class="bp-section">
      <h2>{others_h}</h2>
      <div class="bp-branches">
{others}
      </div>
    </section>
  </main>

  {footer}

  {wa_float}

  <script>
    // mobile menu (the home page does this in main.js)
    (function () {{
      var btn = document.getElementById("navToggle"), nav = document.getElementById("nav");
      if (!btn || !nav) return;
      btn.addEventListener("click", function () {{
        var open = nav.classList.toggle("nav--open");
        btn.setAttribute("aria-expanded", open ? "true" : "false");
      }});
      document.querySelectorAll(".lang-toggle").forEach(function (a) {{
        a.addEventListener("click", function () {{
          try {{ localStorage.setItem("barber_lang", a.getAttribute("hreflang")); }} catch (e) {{}}
        }});
      }});
    }})();
  </script>
</body>
</html>
""".format(
        lang=lang, title=e(t["title"].format(**fill)), desc=e(t["desc"].format(**fill)),
        url=url, url_ar=url_ar, url_en=url_en, site=SITE, slug=b["slug"], locale=t["locale"],
        schema=schema(b, lang), sprite=sprite, header=header, footer=footer, wa_float=wa_float, rtl=rtl,
        img_alt=e(t["img_alt"].format(**fill)), kicker=t["kicker"].format(name=e(name)), badge=badge,
        h1=t["h1"].format(name=e(name)), addr=e(t["addr"].format(**fill)),
        hours=e(h[lang]), hours_short=e(h["short"]),
        wa=e(wa_link), wa_btn=e(t["wa_btn"]), map=e(b["map"]), map_btn=e(t["map_btn"]),
        services_h=e(t["services"]), services=services, services_note=e(t["services_note"]),
        reviews=reviews, review_link=e(t["review_link"]), others_h=e(t["others"]), others=others,
        icon_pin=ICON_PIN, icon_clock=ICON_CLOCK, icon_wa=ICON_WA,
    )


def main():
    for b in BRANCHES:
        for lang, folder in (("ar", b["slug"]), ("en", os.path.join("en", b["slug"]))):
            out = os.path.join(ROOT, folder, "index.html")
            os.makedirs(os.path.dirname(out), exist_ok=True)
            io.open(out, "w", encoding="utf-8", newline="").write(page(b, lang))
            print("wrote", os.path.relpath(out, ROOT))


if __name__ == "__main__":
    main()
