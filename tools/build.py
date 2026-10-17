"""Rebuild every generated page and the sitemap, in the right order.

    python tools/build.py

index.html is the source for everything:
  1. ar/index.html              (tools/build_ar.py)
  2. section pages              (tools/build_pages.py)   /services/, /ar/services/ …
  3. branch pages               (tools/build_branches.py) /b15/, /en/b15/ …
  4. sitemap.xml
"""
import datetime
import io
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_ar        # noqa: E402
import build_branches  # noqa: E402
import build_pages     # noqa: E402

ROOT = build_pages.ROOT
SITE = build_pages.SITE + "/"


def sitemap():
    # (english path, arabic path) pairs; each URL lists its language alternates
    pairs = [("", "ar/")]
    pairs += [(s + "/", "ar/" + s + "/") for s in build_pages.SECTIONS]
    pairs += [("en/%s/" % b["slug"], "%s/" % b["slug"]) for b in build_branches.BRANCHES]
    today = datetime.date.today().isoformat()
    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
           '        xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    for en, ar in pairs:
        alts = ("    <xhtml:link rel=\"alternate\" hreflang=\"en\" href=\"%s%s\" />\n"
                "    <xhtml:link rel=\"alternate\" hreflang=\"ar\" href=\"%s%s\" />\n"
                "    <xhtml:link rel=\"alternate\" hreflang=\"x-default\" href=\"%s%s\" />\n"
                % (SITE, en, SITE, ar, SITE, en))
        for loc in (en, ar):
            out.append("  <url>\n    <loc>%s%s</loc>\n    <lastmod>%s</lastmod>\n%s  </url>" % (SITE, loc, today, alts))
    out.append("</urlset>")
    io.open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8", newline="\n").write("\n".join(out) + "\n")
    print("wrote sitemap.xml (%d urls)" % (2 * len(pairs)))


if __name__ == "__main__":
    build_ar.main()
    build_pages.main()
    build_branches.main()
    sitemap()
