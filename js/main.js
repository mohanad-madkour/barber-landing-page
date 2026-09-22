/* ============================================================
   BARBER — Landing Page JS
   ============================================================ */
(function () {
  "use strict";

  /* -------- Data -------- */
  const WA = "https://wa.me/201159125229";

  // UI strings for JS-rendered content
  const T = {
    en: { priceSoon: "Price soon", hoursLabel: "Hours", map: "Open in Maps", nowOpen: "Now Open", galleryAlt: "BARBER work" },
    ar: { priceSoon: "السعر قريبًا", hoursLabel: "المواعيد", map: "افتح على الخريطة", nowOpen: "Now Open", galleryAlt: "من أعمال BARBER" }
  };

  // Featured (important) services only — real prices in EGP. Full list is in-store.
  const services = [
    { name: "Haircut",           price: "180" },
    { name: "Haircut + Beard",   price: "300" },
    { name: "Beard",             price: "150" },
    { name: "Blow-dry",          price: "120" },
    { name: "Protein Treatment", price: "1000" },
    { name: "Hair Color",        price: "300" },
    { name: "Beard Color",       price: "150" },
    { name: "Facial Cleansing",  price: "350" }
  ];

  // Branch names + addresses stay Arabic in both languages (real place references).
  // pos = pin position on the map (% of the map box), ordered B10 → B12 → B15 → Craft → B8.
  // ll = [lat, lng]. B10 is exact; the others are estimates inside Madinaty (draggable → fine-tune).
  // map = real Google Maps link for each branch.
  const branches = [
    { name: "B10",        loc: "بجوار New Benny Market", ll: [30.0824197, 31.6588338], hours: "1 PM – 1 AM",  badge: null, map: "https://maps.app.goo.gl/CZsrdZdvszbi1Eo69" },
    { name: "B12",        loc: "بجوار بيت الجملة ماركت", ll: [30.0813061, 31.6741087], hours: "1 PM – 1 AM",  badge: null, map: "https://maps.app.goo.gl/RiEPsiAHepFNC2aQ6" },
    { name: "B15",        loc: "بجوار محمد الفار ماركت", ll: [30.0905698, 31.6779134], hours: "1 PM – 1 AM",  badge: null, map: "https://maps.app.goo.gl/6YmmWnykg3egYY6c7" },
    { name: "Craft Zone", loc: "بلوك 2",                 ll: [30.0727812, 31.6705481], hours: "11 AM – 2 AM", badge: null, map: "https://maps.app.goo.gl/fFCBS6Z8sCY5EHpq9" },
    { name: "B8",         loc: "خلف The Mart",           ll: [30.1004982, 31.6516985], hours: "1 PM – 1 AM",  badge: true, map: "https://maps.app.goo.gl/wWXc1byb1pg5qFpL7" }
  ];

  // Gallery placeholders (Unsplash, B/W barbershop). Replace with real images later.
  const gallery = [
    "https://images.unsplash.com/photo-1503951914875-452162b0f3f1?auto=format&fit=crop&w=800&q=80",
    "https://images.unsplash.com/photo-1585747860715-2ba37e788b70?auto=format&fit=crop&w=800&q=80",
    "https://images.unsplash.com/photo-1622286342621-4bd786c2447c?auto=format&fit=crop&w=800&q=80",
    "https://images.unsplash.com/photo-1599351431202-1e0f0137899a?auto=format&fit=crop&w=800&q=80",
    "https://images.unsplash.com/photo-1621605815971-fbc98d665033?auto=format&fit=crop&w=800&q=80",
    "https://images.unsplash.com/photo-1517832606299-7ae9b720a186?auto=format&fit=crop&w=800&q=80"
  ];

  const icons = {
    scissors: '<svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="6" cy="6" r="3"/><circle cx="6" cy="18" r="3"/><line x1="20" y1="4" x2="8.12" y2="15.88"/><line x1="14.47" y1="14.48" x2="20" y2="20"/><line x1="8.12" y1="8.12" x2="12" y2="12"/></svg>',
    razor: '<svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 4l7 7"/><rect x="10" y="10" width="10" height="6" rx="1" transform="rotate(45 15 13)"/></svg>',
    beard: '<svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 6c0 6 3 12 8 12s8-6 8-12"/><path d="M8 6v3M12 6v4M16 6v3"/></svg>',
    hand: '<svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 11V6a2 2 0 0 0-4 0v5M14 10V4a2 2 0 0 0-4 0v6M10 10.5V6a2 2 0 0 0-4 0v8"/><path d="M18 8a2 2 0 1 1 4 0v6a8 8 0 0 1-8 8h-2c-2.8 0-4.5-.86-5.99-2.34l-3.6-3.6a2 2 0 0 1 2.83-2.82L7 15"/></svg>',
    brush: '<svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9.06 11.9l8.07-8.06a2.85 2.85 0 1 1 4.03 4.03l-8.06 8.08"/><path d="M7.07 14.94c-1.66 0-3 1.35-3 3.02 0 1.33-2.5 1.52-2 2.02 1.08 1.1 2.49 2.02 4 2.02 2.2 0 4-1.8 4-4.04a3.01 3.01 0 0 0-3-3.02z"/></svg>',
    drop: '<svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2.69l5.66 5.66a8 8 0 1 1-11.31 0z"/></svg>',
    star: '<svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>'
  };

  /* -------- Render services as a price list (names stay Arabic) -------- */
  const servicesGrid = document.getElementById("servicesGrid");
  function renderServices() {
    if (!servicesGrid) return;
    servicesGrid.innerHTML = services.map(function (s) {
      return (
        '<div class="srv-row">' +
          '<span class="srv-name">' + s.name + '</span>' +
          '<span class="srv-dots" aria-hidden="true"></span>' +
          '<span class="srv-price">' + s.price + ' <em>EGP</em></span>' +
        '</div>'
      );
    }).join("");
  }

  /* -------- Marquee strip (repeating text ticker) -------- */
  (function marquee() {
    const el = document.getElementById("marquee");
    if (!el) return;
    const phrase = "THE ORIGINAL BARBER";
    const unit = '<span class="marquee-strip__item">' + phrase + '</span><span class="marquee-strip__sep">✦</span>';
    let group = "";
    for (let k = 0; k < 8; k++) group += unit;
    el.innerHTML =
      '<div class="marquee-strip__track">' +
        '<div class="marquee-strip__group">' + group + '</div>' +
        '<div class="marquee-strip__group">' + group + '</div>' +
      '</div>';
  })();

  /* -------- Render gallery -------- */
  const galleryGrid = document.getElementById("galleryGrid");
  function renderGallery(lang) {
    const alt = T[lang].galleryAlt;
    galleryGrid.innerHTML = gallery.map(function (src) {
      return (
        '<figure class="gallery__item reveal" data-full="' + src.replace('w=800', 'w=1400') + '">' +
          '<img src="' + src + '" alt="' + alt + '" loading="lazy" decoding="async" />' +
        '</figure>'
      );
    }).join("");
  }

  /* -------- Render branches on a real dark map (Leaflet + Esri) -------- */
  let activeBranch = 0;
  let lmap = null, lmarkers = [];

  function mapHrefFor(b) {
    return b.map || ("https://www.google.com/maps/search/" + encodeURIComponent("BARBER " + b.name + " " + b.loc));
  }

  function popupHtml(b, lang) {
    const t = T[lang];
    return (
      '<div class="branch-popup">' +
        (b.badge ? '<span class="branch-badge branch-popup__badge">' + t.nowOpen + '</span>' : '') +
        '<h3 class="branch-popup__name">' + b.name + '</h3>' +
        '<p class="branch-popup__loc" dir="rtl">' + b.loc + '</p>' +
        '<span class="branch-popup__meta">' + t.hoursLabel + ': ' + (b.hours || '') + '</span>' +
        '<a class="branch-popup__map" href="' + mapHrefFor(b) + '" target="_blank" rel="noopener">' +
          '<svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>' +
          ' ' + t.map +
        '</a>' +
      '</div>'
    );
  }

  function branchIcon(b, i, lang) {
    return L.divIcon({
      className: "",
      html:
        '<div class="branch-marker' + (b.badge ? " is-new" : "") + (i === activeBranch ? " is-active" : "") + '">' +
          '<span class="branch-marker__dot">' +
            '<img class="branch-marker__logo" src="logo-layers/logo-full-transparent.png" alt="BARBER" decoding="async" />' +
          '</span>' +
          '<span class="branch-marker__label">' + b.name + (b.badge ? ' · ' + T[lang].nowOpen : '') + '</span>' +
        '</div>',
      iconSize: [140, 74],
      iconAnchor: [70, 28]
    });
  }

  function refreshMarkerIcons(lang) {
    lmarkers.forEach(function (mk, i) { mk.setIcon(branchIcon(branches[i], i, lang)); });
  }

  function renderBranches(lang) {
    if (typeof L === "undefined") return; // Leaflet not loaded
    const mapEl = document.getElementById("branchMap");
    if (!mapEl) return;

    if (!lmap) {
      lmap = L.map(mapEl, { scrollWheelZoom: false, zoomControl: true, attributionControl: true });
      // Esri dark gray basemap — free, no API key
      L.tileLayer("https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Dark_Gray_Base/MapServer/tile/{z}/{y}/{x}", {
        maxZoom: 19, maxNativeZoom: 16, attribution: "&copy; Esri"
      }).addTo(lmap);
      // street/place labels overlay
      L.tileLayer("https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Dark_Gray_Reference/MapServer/tile/{z}/{y}/{x}", {
        maxZoom: 19, maxNativeZoom: 16, opacity: 0.9
      }).addTo(lmap);

      lmarkers = branches.map(function (b, i) {
        const mk = L.marker(b.ll, { icon: branchIcon(b, i, lang), draggable: false }).addTo(lmap);
        mk.bindPopup(popupHtml(b, currentLang), { className: "branch-popup-wrap", closeButton: true, offset: [0, -18], maxWidth: 260 });
        mk.on("click", function () {
          activeBranch = i;
          refreshMarkerIcons(currentLang);
        });
        return mk;
      });

      // move zoom buttons out of the top-left corner so they don't cover the B8 pin
      if (lmap.zoomControl) lmap.zoomControl.setPosition("bottomright");

      // fit all branches inside the view with padding so edge pins (e.g. B8) stay visible
      const bounds = L.latLngBounds(branches.map(function (b) { return b.ll; }));
      function fitAll() {
        // extra top padding on tall (mobile) maps so the northern pin + label clear the edge
        const tall = mapEl.clientHeight > mapEl.clientWidth;
        lmap.fitBounds(bounds, {
          paddingTopLeft: [40, tall ? 70 : 45],
          paddingBottomRight: [40, 55],
          maxZoom: 15
        });
      }
      fitAll();
      setTimeout(function () { lmap.invalidateSize(); fitAll(); }, 200);
      let rt;
      window.addEventListener("resize", function () {
        clearTimeout(rt);
        rt = setTimeout(function () { if (lmap) { lmap.invalidateSize(); fitAll(); } }, 250);
      });

      // On touch devices: one finger scrolls the PAGE, two fingers move the map.
      // (Leaflet grabs one-finger drags by default, which traps the page scroll.)
      const isTouch = window.matchMedia("(pointer: coarse)").matches ||
                      ("ontouchstart" in window);
      if (isTouch) {
        lmap.dragging.disable();
        const cont = lmap.getContainer();
        cont.addEventListener("touchstart", function (e) {
          if (e.touches.length >= 2) lmap.dragging.enable();
          else lmap.dragging.disable();
        }, { passive: true });
        cont.addEventListener("touchend", function (e) {
          if (e.touches.length < 2) lmap.dragging.disable();
        }, { passive: true });

        // subtle hint: fade in on touch, fade out shortly after
        const hint = document.createElement("div");
        hint.className = "map-hint";
        hint.setAttribute("data-en", "Use two fingers to move the map");
        hint.setAttribute("data-ar", "استخدم إصبعين لتحريك الخريطة");
        hint.textContent = currentLang === "ar" ? "استخدم إصبعين لتحريك الخريطة" : "Use two fingers to move the map";
        cont.appendChild(hint);
        let ht;
        cont.addEventListener("touchstart", function (e) {
          if (e.touches.length === 1) {
            hint.classList.add("is-visible");
            clearTimeout(ht);
            ht = setTimeout(function () { hint.classList.remove("is-visible"); }, 1400);
          } else {
            hint.classList.remove("is-visible");
          }
        }, { passive: true });
      }
    } else {
      refreshMarkerIcons(lang);
      lmarkers.forEach(function (mk, i) { mk.setPopupContent(popupHtml(branches[i], lang)); });
    }
  }

  /* -------- i18n engine + language toggle -------- */
  let currentLang = "en";
  try { const saved = localStorage.getItem("barber_lang"); if (saved === "ar" || saved === "en") currentLang = saved; } catch (e) {}

  const langToggle = document.getElementById("langToggle");
  const langToggleNav = document.getElementById("langToggleNav");

  function applyLang(lang, isInitial) {
    currentLang = lang;
    document.documentElement.setAttribute("lang", lang);
    // keep the layout direction fixed (LTR); only the text content changes
    document.documentElement.setAttribute("dir", "ltr");

    // static elements with data-en / data-ar
    document.querySelectorAll("[data-en]").forEach(function (el) {
      const val = el.getAttribute("data-" + lang);
      if (val != null) el.innerHTML = val;
    });
    document.querySelectorAll("[data-ph-en]").forEach(function (el) {
      const ph = el.getAttribute("data-ph-" + lang);
      if (ph != null) el.setAttribute("placeholder", ph);
    });

    // dynamic grids
    renderServices(lang);
    renderGallery(lang);
    renderBranches(lang);

    // toggle button shows the OTHER language, with its flag (standard style)
    const toggleHtml = (lang === "ar")
      ? '<span class="fi fi-gb"></span><span class="lang-toggle__txt">English</span>'
      : '<span class="fi fi-eg"></span><span class="lang-toggle__txt">العربية</span>';
    if (langToggle) langToggle.innerHTML = toggleHtml;
    if (langToggleNav) langToggleNav.innerHTML = toggleHtml;

    try { localStorage.setItem("barber_lang", lang); } catch (e) {}

    // grids were re-created after the scroll observer ran → reveal them
    if (!isInitial) {
      document.querySelectorAll("#servicesGrid .reveal, #galleryGrid .reveal, #branchesGrid .reveal")
        .forEach(function (el) { el.classList.add("is-visible"); });
    }
  }

  function toggleLang() {
    applyLang(currentLang === "ar" ? "en" : "ar", false);
  }
  if (langToggle) langToggle.addEventListener("click", toggleLang);
  if (langToggleNav) langToggleNav.addEventListener("click", function () {
    toggleLang();
    // close the mobile menu after switching
    const navEl = document.getElementById("nav");
    const navBtn = document.getElementById("navToggle");
    if (navEl) navEl.classList.remove("nav--open");
    if (navBtn) navBtn.setAttribute("aria-expanded", "false");
  });

  applyLang(currentLang, true);

  /* -------- Lightbox -------- */
  const lightbox = document.getElementById("lightbox");
  const lightboxImg = document.getElementById("lightboxImg");
  document.getElementById("lightboxClose").addEventListener("click", closeLightbox);
  lightbox.addEventListener("click", function (e) { if (e.target === lightbox) closeLightbox(); });
  document.addEventListener("keydown", function (e) { if (e.key === "Escape") closeLightbox(); });
  galleryGrid.addEventListener("click", function (e) {
    const item = e.target.closest(".gallery__item");
    if (!item) return;
    lightboxImg.src = item.getAttribute("data-full");
    lightbox.classList.add("lightbox--open");
    lightbox.setAttribute("aria-hidden", "false");
  });
  function closeLightbox() {
    lightbox.classList.remove("lightbox--open");
    lightbox.setAttribute("aria-hidden", "true");
  }

  /* -------- Gallery carousel arrows -------- */
  (function galleryArrows() {
    const prev = document.getElementById("galPrev");
    const next = document.getElementById("galNext");
    if (!galleryGrid || !prev || !next) return;
    function step() {
      const card = galleryGrid.querySelector(".gallery__item");
      const gap = 24;
      return card ? card.getBoundingClientRect().width + gap : 320;
    }
    prev.addEventListener("click", function () { galleryGrid.scrollBy({ left: -step(), behavior: "smooth" }); });
    next.addEventListener("click", function () { galleryGrid.scrollBy({ left: step(), behavior: "smooth" }); });
  })();

  /* -------- Contact form → WhatsApp -------- */
  (function contactForm() {
    const form = document.getElementById("contactForm");
    if (!form) return;
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      const name = (document.getElementById("cfName").value || "").trim();
      const branch = document.getElementById("cfBranch").value;
      const msg = (document.getElementById("cfMsg").value || "").trim();
      let text;
      if (currentLang === "ar") {
        text = "السلام عليكم BARBER 👋\n";
        if (name) text += "أنا " + name + ".\n";
        text += "الفرع: " + branch + ".\n";
        text += msg ? ("رسالتي: " + msg) : "حابب أستفسر عن خدمة/موعد.";
      } else {
        text = "Hello BARBER 👋\n";
        if (name) text += "I'm " + name + ".\n";
        text += "Branch: " + branch + ".\n";
        text += msg ? ("Message: " + msg) : "I have a quick question.";
      }
      window.open("https://wa.me/201159125229?text=" + encodeURIComponent(text), "_blank", "noopener");
    });
  })();

  /* -------- Header scroll state -------- */
  const header = document.getElementById("header");
  window.addEventListener("scroll", function () {
    header.classList.toggle("header--scrolled", window.scrollY > 40);
  });

  /* -------- Mobile nav -------- */
  const navToggle = document.getElementById("navToggle");
  const nav = document.getElementById("nav");
  navToggle.addEventListener("click", function () {
    const open = nav.classList.toggle("nav--open");
    navToggle.setAttribute("aria-expanded", open ? "true" : "false");
  });
  nav.addEventListener("click", function (e) {
    if (e.target.tagName === "A") {
      nav.classList.remove("nav--open");
      navToggle.setAttribute("aria-expanded", "false");
    }
  });

  /* -------- Hero video sequence (scissors → clipper, looping) -------- */
  (function heroVideos() {
    const v1 = document.getElementById("heroV1");
    const v2 = document.getElementById("heroV2");
    if (!v1 || !v2) return;
    const vids = [v1, v2];
    const MAX_MS = 6500;         // max time to show each scene before switching
    const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    let cur = 0, timer = null;

    function show(i) {
      vids.forEach(function (v, idx) { v.classList.toggle("is-active", idx === i); });
    }
    function playAll() {
      vids.forEach(function (v) {
        if (v.paused) { const p = v.play(); if (p && p.catch) p.catch(function () {}); }
      });
    }
    function next() {
      cur = (cur + 1) % vids.length;
      show(cur);                       // pure opacity crossfade — nothing pauses or seeks
      playAll();                       // resume anything a browser may have paused
      timer = setTimeout(next, MAX_MS);
    }

    // Both clips loop forever and never stop; we only fade which one is visible,
    // so there's no cut/freeze at the switch or when a clip repeats.
    vids.forEach(function (v) {
      v.loop = true;
      v.muted = true;
      const p = v.play();
      if (p && p.catch) p.catch(function () {});
    });

    if (reduceMotion) {
      show(0);
      vids.forEach(function (v) { v.pause(); });
      return;
    }
    show(0);
    timer = setTimeout(next, MAX_MS);
  })();

  /* -------- Falling hair particles -------- */
  const hairFall = document.getElementById("hairFall");
  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (hairFall && !reduceMotion) {
    let html = "";
    for (let i = 0; i < 16; i++) {
      const left = Math.random() * 100;
      const dur = 6 + Math.random() * 7;
      const delay = Math.random() * 8;
      const h = 10 + Math.random() * 14;
      html += '<i style="left:' + left + '%;animation-duration:' + dur + 's;animation-delay:-' + delay + 's;height:' + h + 'px"></i>';
    }
    hairFall.innerHTML = html;
  }

  /* -------- Scroll reveal -------- */
  if ("IntersectionObserver" in window && !reduceMotion) {
    const io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add("is-visible"); io.unobserve(en.target); }
      });
    }, { threshold: 0.12 });
    document.querySelectorAll(".reveal").forEach(function (el) { io.observe(el); });
  } else {
    document.querySelectorAll(".reveal").forEach(function (el) { el.classList.add("is-visible"); });
  }

  /* -------- Reviews marquee: duplicate cards for a seamless left-scroll loop -------- */
  (function reviewsMarquee() {
    const track = document.getElementById("reviewsTrack");
    if (!track) return;
    const originals = Array.prototype.slice.call(track.children);
    originals.forEach(function (card) { card.classList.add("is-visible"); });
    originals.forEach(function (card) {
      const clone = card.cloneNode(true);
      clone.classList.remove("reveal");
      clone.classList.add("is-visible");
      clone.setAttribute("aria-hidden", "true");
      track.appendChild(clone);
    });
  })();

})();
