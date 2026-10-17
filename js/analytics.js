/* ============================================================
   BARBER — Google Analytics 4 + click tracking (loaded on every page)
   Events sent to GA4:
     whatsapp_click   any link to wa.me       (the main "lead" signal)
     map_click        any Google Maps link
     instagram_click  any Instagram link
   Each carries click_location (floating_button / header / footer / <section id>)
   and branch (when the page or link belongs to one branch).
   ============================================================ */
(function () {
  "use strict";
  var GA_ID = "G-K58YYDP5PG";

  window.dataLayer = window.dataLayer || [];
  function gtag() { window.dataLayer.push(arguments); }
  window.gtag = gtag;
  gtag("js", new Date());
  gtag("config", GA_ID);

  function eventFor(href) {
    if (/^https?:\/\/(wa\.me|api\.whatsapp\.com)\//.test(href)) return "whatsapp_click";
    if (/^https?:\/\/(maps\.app\.goo\.gl|(www\.)?google\.[a-z.]+\/maps)/.test(href)) return "map_click";
    if (/^https?:\/\/(www\.)?instagram\.com\//.test(href)) return "instagram_click";
    return null;
  }

  function locationOf(el) {
    if (el.closest(".wa-float")) return "floating_button";
    if (el.closest("header.header, .header")) return "header";
    if (el.closest("footer")) return "footer";
    if (el.closest(".leaflet-container")) return "map_popup";
    var sec = el.closest("section[id]");
    if (sec) return sec.id;
    if (el.closest(".bp-hero")) return "branch_hero";
    return "page";
  }

  // branch pages say which branch they are in their URL (/b15/, /en/craft-zone/)
  var pageBranch = (location.pathname.match(/^\/(?:en\/)?(b8|b10|b12|b15|craft-zone)\//) || [])[1] || "";

  document.addEventListener("click", function (e) {
    var a = e.target.closest && e.target.closest("a[href]");
    if (!a) return;
    var name = eventFor(a.href);
    if (!name) return;
    var params = { click_location: locationOf(a), link_url: a.href };
    var branch = pageBranch;
    var popup = a.closest(".branch-popup");
    if (popup) {
      var n = popup.querySelector(".branch-popup__name");
      if (n) branch = n.textContent.trim().toLowerCase().replace(/\s+/g, "-");
    }
    if (branch) params.branch = branch;
    gtag("event", name, params);
  }, true);
})();
