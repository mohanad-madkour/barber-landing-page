"""Generate ar/index.html (the Arabic page) from index.html.

index.html stays the single source. Every element carrying data-en / data-ar
gets its Arabic text baked into the HTML, so search engines index real Arabic
content at https://barberegypt.com/ar/ instead of the JS-swapped English page.

Run after editing index.html:   python tools/build_ar.py
"""
import html
import io
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "index.html")
OUT = os.path.join(ROOT, "ar", "index.html")

AR_TITLE = "باربر مدينتي | BARBER — حلاق رجالي في مدينتي بـ 5 فروع"
AR_DESC = ("BARBER حلاق رجالي في مدينتي بـ 5 فروع (B8، B10، B12، B15، Craft Zone). "
           "قص شعر، فيد، تظبيط دقن، صبغة وتنظيف بشرة. مفتوح يوميًا لحد 1 بالليل — تواصل معانا على واتساب.")
AR_OG_TITLE = "BARBER مدينتي — حلاق رجالي بـ 5 فروع"


def replace_once(s, old, new):
    if s.count(old) != 1:
        raise SystemExit("expected exactly one match for: " + old[:80])
    return s.replace(old, new)


def main():
    s = io.open(SRC, encoding="utf-8", newline="").read()

    # 1) bake Arabic text into every data-en/data-ar element
    # (the page layout stays LTR like the English one; Arabic text gets dir="rtl"
    # so its punctuation lands on the correct side)
    tag_re = re.compile(r'(<(\w+)\b[^>]*\sdata-ar="([^"]*)"[^>]*>)(.*?)(</\2>)', re.S)
    arabic = re.compile("[؀-ۿ]")

    def bake(m):
        # attribute value -> innerHTML, same as main.js (so &lt;br&gt; becomes <br>)
        open_tag, text = m.group(1), html.unescape(m.group(3))
        if arabic.search(text) and " dir=" not in open_tag:
            open_tag = open_tag[:-1] + ' dir="rtl">'
        return open_tag + text + m.group(5)

    s, n = tag_re.subn(bake, s)

    # 2) document language + head metadata
    s = replace_once(s, '<html lang="en" dir="ltr">', '<html lang="ar" dir="ltr">')
    s = re.sub(r"<title>.*?</title>", "<title>" + AR_TITLE + "</title>", s, count=1)
    s = re.sub(r'(<meta name="description" content=")[^"]*', r"\g<1>" + AR_DESC, s, count=1)
    s = replace_once(s, '<link rel="canonical" href="https://barberegypt.com/" />',
                     '<link rel="canonical" href="https://barberegypt.com/ar/" />')
    s = replace_once(s, '<meta property="og:url" content="https://barberegypt.com/" />',
                     '<meta property="og:url" content="https://barberegypt.com/ar/" />')
    s = replace_once(s, '<meta property="og:locale" content="en_US" />',
                     '<meta property="og:locale" content="ar_EG" />')
    s = replace_once(s, '<meta property="og:locale:alternate" content="ar_EG" />',
                     '<meta property="og:locale:alternate" content="en_US" />')
    s = re.sub(r'(<meta (?:property="og:title"|name="twitter:title") content=")[^"]*',
               r"\g<1>" + AR_OG_TITLE, s)
    s = re.sub(r'(<meta (?:property="og:description"|name="twitter:description") content=")[^"]*',
               r"\g<1>" + AR_DESC, s)

    # 3) branch links: English pages live under /en/, Arabic ones at the root
    s = s.replace('href="/en/', 'href="/')
    # section pages: /services/ (English) -> /ar/services/ (Arabic)
    s = re.sub(r'href="/(about|services|branches|locations|reviews|contact)/"', r'href="/ar/\g<1>/"', s)

    # 4) the page lives in /ar/, so make local asset paths root-absolute
    s = re.sub(r'((?:src|href|poster)=")(?=(?:css|js|images|logo-layers|videos)/)', r"\g<1>/", s)

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    io.open(OUT, "w", encoding="utf-8", newline="").write(s)
    print("wrote %s (%d translated elements)" % (os.path.relpath(OUT, ROOT), n))


if __name__ == "__main__":
    main()
