/* Baisa — small progressive-enhancement scripts.
   Nothing here is required for the content to work; it just adds polish. */
(function () {
  'use strict';

  /* ---- Current year in footer ---- */
  var yearEl = document.getElementById('year');
  if (yearEl) yearEl.textContent = new Date().getFullYear();

  /* ---- Mobile nav toggle ---- */
  var toggle = document.getElementById('nav-toggle');
  var nav = document.getElementById('main-nav');
  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      toggle.classList.toggle('open', open);
      toggle.setAttribute('aria-expanded', String(open));
    });
    // close the menu after tapping a link
    nav.addEventListener('click', function (e) {
      if (e.target.tagName === 'A') {
        nav.classList.remove('open');
        toggle.classList.remove('open');
        toggle.setAttribute('aria-expanded', 'false');
      }
    });
  }

  /* ---- Reveal-on-scroll ---- */
  var revealTargets = document.querySelectorAll(
    '.section-head, .about-grid, .room-card, .hall-grid, .amenities li, .g-tile, .review, .booking-wrap, .contact-grid'
  );
  revealTargets.forEach(function (el) { el.classList.add('reveal'); });

  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry, i) {
        if (entry.isIntersecting) {
          // gentle stagger for grouped items
          setTimeout(function () { entry.target.classList.add('in'); }, (i % 6) * 70);
          io.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
    revealTargets.forEach(function (el) { io.observe(el); });
  } else {
    revealTargets.forEach(function (el) { el.classList.add('in'); });
  }

  /* ---- Gallery lightbox ---- */
  var lb = document.getElementById('lightbox');
  var lbPhoto = document.getElementById('lb-photo');
  var lbCaption = document.getElementById('lb-caption');
  var lbClose = document.getElementById('lb-close');

  function openLightbox(tile) {
    if (!lb) return;
    var label = tile.getAttribute('data-label') || '';
    // Carry over a real <img> if the owner has added one; else copy the placeholder look.
    var img = tile.querySelector('img');
    lbPhoto.innerHTML = '';
    if (img) {
      var clone = img.cloneNode(true);
      lbPhoto.appendChild(clone);
      lbPhoto.removeAttribute('data-label');
    } else {
      lbPhoto.setAttribute('data-label', label);
    }
    lbCaption.textContent = label;
    lb.classList.add('open');
    lb.setAttribute('aria-hidden', 'false');
    document.body.style.overflow = 'hidden';
  }
  function closeLightbox() {
    if (!lb) return;
    lb.classList.remove('open');
    lb.setAttribute('aria-hidden', 'true');
    document.body.style.overflow = '';
  }

  document.querySelectorAll('.g-tile').forEach(function (tile) {
    tile.addEventListener('click', function () { openLightbox(tile); });
  });
  if (lbClose) lbClose.addEventListener('click', closeLightbox);
  if (lb) lb.addEventListener('click', function (e) { if (e.target === lb) closeLightbox(); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') closeLightbox(); });

  /* ---- Shrink header shadow on scroll ---- */
  var header = document.querySelector('.site-header');
  if (header) {
    var onScroll = function () {
      header.style.boxShadow = window.scrollY > 12 ? '0 10px 30px -20px rgba(60,20,20,.6)' : 'none';
    };
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
  }
})();

/* ---- Bilingual toggle (English / हिंदी) ---- */
(function () {
  'use strict';
  var KEY = 'baisa-lang';
  var toggle = document.getElementById('lang-toggle');
  var nodes = [].slice.call(document.querySelectorAll('[data-hi]'));
  // capture the original English markup once
  nodes.forEach(function (n) { if (!n.hasAttribute('data-en')) n.setAttribute('data-en', n.innerHTML); });

  function apply(l) {
    var hi = (l === 'hi');
    document.documentElement.lang = hi ? 'hi' : 'en';
    document.body.classList.toggle('lang-hi', hi);
    nodes.forEach(function (n) {
      n.innerHTML = hi ? n.getAttribute('data-hi') : n.getAttribute('data-en');
    });
    if (toggle) {
      toggle.textContent = hi ? 'EN' : 'हिंदी';
      toggle.setAttribute('aria-label', hi ? 'Switch to English' : 'हिंदी में देखें');
    }
  }

  var lang = 'en';
  try { lang = localStorage.getItem(KEY) || 'en'; } catch (e) {}
  if (toggle) {
    toggle.addEventListener('click', function () {
      lang = (lang === 'hi') ? 'en' : 'hi';
      try { localStorage.setItem(KEY, lang); } catch (e) {}
      apply(lang);
    });
  }
  apply(lang);
})();
