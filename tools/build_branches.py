"""Generate one page per branch: /b8/, /b10/, /b12/, /b15/, /craft-zone/.

Each page targets searches for that branch ("حلاق B15 مدينتي"), carries its own
HairSalon schema, and is the link to put on that branch's Google Business Profile.

Branch data lives in BRANCHES below — edit it, then run:
    python tools/build_branches.py
"""
import html
import io
import json
import os
from urllib.parse import quote

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://barberegypt.com"
PHONE = "+201159125229"
PHONE_DISPLAY = "+20 11 5912 5229"
WA = "https://wa.me/201159125229"
INSTAGRAM = "https://www.instagram.com/barber._.eg"
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

HOURS_STD = {"opens": "13:00", "closes": "01:00", "ar": "يوميًا من 1 الظهر لحد 1 بالليل", "en": "1 PM – 1 AM"}
HOURS_CZ = {"opens": "11:00", "closes": "02:00", "ar": "يوميًا من 11 الصبح لحد 2 بالليل", "en": "11 AM – 2 AM"}

# geo only where the coordinates are exact (see main.js); others link to their Maps listing
BRANCHES = [
    {"slug": "b8", "name": "B8", "loc": "خلف The Mart", "hours": HOURS_STD, "new": True,
     "map": "https://maps.app.goo.gl/wWXc1byb1pg5qFpL7", "geo": None},
    {"slug": "b10", "name": "B10", "loc": "بجوار New Benny Market", "hours": HOURS_STD, "new": False,
     "map": "https://maps.app.goo.gl/CZsrdZdvszbi1Eo69", "geo": (30.0824197, 31.6588338)},
    {"slug": "b12", "name": "B12", "loc": "بجوار بيت الجملة ماركت", "hours": HOURS_STD, "new": False,
     "map": "https://maps.app.goo.gl/RiEPsiAHepFNC2aQ6", "geo": None},
    {"slug": "b15", "name": "B15", "loc": "بجوار محمود الفار ماركت", "hours": HOURS_STD, "new": False,
     "map": "https://maps.app.goo.gl/6YmmWnykg3egYY6c7", "geo": None},
    {"slug": "craft-zone", "name": "Craft Zone", "loc": "بلوك 2", "hours": HOURS_CZ, "new": False,
     "map": "https://maps.app.goo.gl/fFCBS6Z8sCY5EHpq9", "geo": None},
]

SERVICES = [  # same list and prices as main.js
    ("قص شعر", "180"), ("شعر + دقن", "300"), ("دقن", "150"), ("سشوار", "120"),
    ("بروتين", "1000"), ("صبغة شعر", "300"), ("صبغة دقن", "150"), ("تنظيف بشرة", "350"),
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

ICON_PIN = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>'
ICON_CLOCK = '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>'
ICON_WA = ('<svg viewBox="0 0 448 512" class="fill" aria-hidden="true"><path d="M380.9 97.1C339 55.1 283.2 32 223.9 32c-122.4 0-222 99.6-222 222 '
           '0 39.1 10.2 77.3 29.6 111L0 480l117.7-30.9c32.4 17.7 68.9 27 106.1 27h.1c122.3 0 224.1-99.6 224.1-222 0-59.3-25.2-115-67.1-157zm-157 '
           '341.6c-33.2 0-65.7-8.9-94-25.7l-6.7-4-69.8 18.3L72 359.2l-4.4-7c-18.5-29.4-28.2-63.3-28.2-98.2 0-101.7 82.8-184.5 184.6-184.5 49.3 0 '
           '95.6 19.2 130.4 54.1 34.8 34.9 56.2 81.2 56.1 130.5 0 101.8-84.9 184.6-186.6 184.6zm101.2-138.2c-5.5-2.8-32.8-16.2-37.9-18-5.1-1.9-8.8-2.8-12.5 '
           '2.8-3.7 5.6-14.3 18-17.6 21.8-3.2 3.7-6.5 4.2-12 1.4-32.6-16.3-54-29.1-75.5-66-5.7-9.8 5.7-9.1 16.3-30.3 1.8-3.7.9-6.9-.5-9.7-1.4-2.8-12.5-30.1-17.1-41.2-4.5-10.8-9.1-9.3-12.5-9.5-3.2-.2-6.9-.2-10.6-.2-3.7 '
           '0-9.7 1.4-14.8 6.9-5.1 5.6-19.4 19-19.4 46.3 0 27.3 19.9 53.7 22.6 57.4 2.8 3.7 39.1 59.7 94.8 83.8 35.2 15.2 49 16.5 66.6 13.9 10.7-1.6 '
           '32.8-13.4 37.4-26.4 4.6-13 4.6-24.1 3.2-26.4-1.3-2.5-5-3.9-10.5-6.6z"/></svg>')

e = html.escape


def schema(b):
    data = {
        "@context": "https://schema.org",
        "@type": "HairSalon",
        "@id": SITE + "/" + b["slug"] + "/#branch",
        "name": "BARBER Madinaty — " + b["name"],
        "alternateName": ["باربر " + b["name"] + " مدينتي", "BARBER " + b["name"]],
        "url": SITE + "/" + b["slug"] + "/",
        "image": SITE + "/images/branches/" + b["slug"] + ".jpg",
        "telephone": PHONE,
        "priceRange": "EGP 120–1000",
        "address": {
            "@type": "PostalAddress",
            "streetAddress": b["loc"] + "، " + b["name"] + "، مدينتي",
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


def page(b):
    name, loc, h = b["name"], b["loc"], b["hours"]
    title = "BARBER %s مدينتي — حلاق رجالي %s" % (name, loc)
    desc = ("فرع BARBER %s في مدينتي (%s): قص شعر، دقن، صبغة وتنظيف بشرة. %s. احجز على واتساب أو افتح موقع الفرع على الخريطة."
            % (name, loc, h["ar"]))
    wa_link = WA + "?text=" + quote("السلام عليكم، عايز أحجز في فرع %s" % name)
    url = SITE + "/" + b["slug"] + "/"

    services = "\n".join(
        '        <li><span>%s</span><span class="dots" aria-hidden="true"></span><b>%s <small>EGP</small></b></li>' % (e(n), p)
        for n, p in SERVICES)

    reviews = ""
    if b["slug"] in REVIEWS:
        cards = "\n".join(
            '        <figure class="review"><span class="stars" aria-label="5 من 5">★★★★★</span>'
            '<blockquote%s>%s</blockquote><figcaption dir="ltr">%s · Google</figcaption></figure>'
            % ("" if any("؀" <= c <= "ۿ" for c in t) else ' dir="ltr"', e(t), e(a))
            for a, t in REVIEWS[b["slug"]])
        reviews = """
    <section class="section">
      <h2>آراء زباين فرع %s</h2>
      <div class="reviews">
%s
      </div>
      <a class="link" href="%s" target="_blank" rel="noopener">اكتب تقييمك للفرع على Google ←</a>
    </section>
""" % (e(name), cards, e(b["map"]))
    else:
        reviews = """
    <section class="section">
      <h2>جربت فرع %s؟</h2>
      <p class="muted">رأيك بيفرق معانا وبيساعد غيرك يختار.</p>
      <a class="link" href="%s" target="_blank" rel="noopener">اكتب تقييمك للفرع على Google ←</a>
    </section>
""" % (e(name), e(b["map"]))

    others = "\n".join(
        '        <a class="branch-card" href="/%s/"><b dir="ltr">%s</b><span>%s</span></a>' % (o["slug"], e(o["name"]), e(o["loc"]))
        for o in BRANCHES if o is not b)

    badge = '<span class="badge">فرع جديد</span>' if b["new"] else ""

    return """<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title}</title>
  <meta name="description" content="{desc}" />
  <meta name="theme-color" content="#141412" />
  <link rel="canonical" href="{url}" />

  <meta property="og:type" content="website" />
  <meta property="og:url" content="{url}" />
  <meta property="og:site_name" content="BARBER Madinaty" />
  <meta property="og:title" content="{title}" />
  <meta property="og:description" content="{desc}" />
  <meta property="og:image" content="{site}/images/branches/{slug}.jpg" />
  <meta property="og:image:width" content="512" />
  <meta property="og:image:height" content="640" />
  <meta property="og:locale" content="ar_EG" />
  <meta name="twitter:card" content="summary_large_image" />

  <link rel="icon" href="/favicon.ico" sizes="48x48" />
  <link rel="icon" type="image/png" sizes="32x32" href="/images/icons/icon-32.png" />
  <link rel="apple-touch-icon" href="/images/icons/icon-180.png" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&family=Poppins:wght@600;700&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="/css/branch.css?v=1" />

  <!-- Generated by tools/build_branches.py — edit the script, not this file. -->
  <script type="application/ld+json">
{schema}
  </script>
</head>
<body>
  <header class="top">
    <a href="/ar/" class="top__logo" aria-label="BARBER — الصفحة الرئيسية">
      <img src="/logo-layers/logo-full-transparent.png" alt="BARBER" width="40" height="60" />
    </a>
    <nav class="top__nav">
      <a href="/ar/#branches">كل الفروع</a>
      <a href="/" lang="en" dir="ltr">English</a>
    </nav>
  </header>

  <main class="wrap">
    <section class="hero">
      <img class="hero__img" src="/images/branches/{slug}.jpg" alt="واجهة فرع BARBER {name_e} في مدينتي" width="512" height="640" fetchpriority="high" />
      <div class="hero__body">
        <span class="kicker">فرع <span dir="ltr">{name_e}</span> · مدينتي {badge}</span>
        <h1><span dir="ltr">BARBER {name_e}</span> — حلاق رجالي في مدينتي</h1>
        <ul class="facts">
          <li>{icon_pin}<span>{loc_e}، مدينتي — القاهرة الجديدة</span></li>
          <li>{icon_clock}<span>{hours_ar} <span class="muted" dir="ltr">({hours_en})</span></span></li>
        </ul>
        <div class="cta">
          <a class="btn btn--primary" href="{wa}" target="_blank" rel="noopener">{icon_wa} احجز على واتساب</a>
          <a class="btn btn--ghost" href="{map}" target="_blank" rel="noopener">{icon_pin} افتح الفرع على الخريطة</a>
        </div>
        <p class="en" lang="en" dir="ltr">BARBER {name_e} — men's barbershop in Madinaty, New Cairo. Open daily {hours_en}.</p>
      </div>
    </section>

    <section class="section">
      <h2>الخدمات والأسعار</h2>
      <ul class="services">
{services}
      </ul>
      <p class="muted small">* قائمة الأسعار الكاملة في الفرع — تواصل على واتساب للتأكيد.</p>
    </section>
{reviews}
    <section class="section">
      <h2>فروعنا التانية في مدينتي</h2>
      <div class="branches">
{others}
      </div>
    </section>
  </main>

  <footer class="foot">
    <a href="{wa_plain}" target="_blank" rel="noopener" dir="ltr">{phone}</a>
    <a href="{insta}" target="_blank" rel="noopener" dir="ltr">@barber._.eg</a>
    <span>© 2026 BARBER — جميع الحقوق محفوظة</span>
  </footer>
</body>
</html>
""".format(
        title=e(title), desc=e(desc), url=url, site=SITE, slug=b["slug"], schema=schema(b),
        name_e=e(name), loc_e=e(loc), badge=badge, hours_ar=e(h["ar"]), hours_en=e(h["en"]),
        wa=e(wa_link), map=e(b["map"]), services=services, reviews=reviews, others=others,
        wa_plain=WA, phone=PHONE_DISPLAY, insta=INSTAGRAM,
        icon_pin=ICON_PIN, icon_clock=ICON_CLOCK, icon_wa=ICON_WA,
    )


def main():
    for b in BRANCHES:
        out = os.path.join(ROOT, b["slug"], "index.html")
        os.makedirs(os.path.dirname(out), exist_ok=True)
        io.open(out, "w", encoding="utf-8", newline="").write(page(b))
        print("wrote", os.path.relpath(out, ROOT))


if __name__ == "__main__":
    main()
