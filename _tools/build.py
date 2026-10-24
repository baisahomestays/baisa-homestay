#!/usr/bin/env python3
"""Baisa site builder (SEO + Hindi pages).  Standard library only.

Run after ANY edit to index.html or party-hall/index.html:

    python3 _tools/build.py

What it does
  1. Writes the JSON-LD structured data (business, rooms, party hall, FAQ, breadcrumbs)
     between the <!-- JSON-LD:START --> / <!-- JSON-LD:END --> markers of each English page.
     The FAQPage markup is built FROM the visible FAQ on the page, so the two can never drift.
  2. Builds the Hindi pages (hi/...) from the English pages: every element that carries a
     data-hi="..." attribute is swapped to its Hindi text; head tags use data-hi / data-hi-<attr>.
  3. Writes sitemap.xml (with hreflang alternates, image entries and real lastmod dates).

All business facts (name, address, phones, hours, amenities ...) live in the BUSINESS block below.
The folder is served from a sub-path on GitHub Pages; if you move to a custom domain, change SITE
(and search-replace the old base URL in index.html / party-hall/index.html / robots.txt / llms.txt).
"""
import hashlib
import html
import json
import os
import re
import sys
from datetime import date
from html.parser import HTMLParser

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATE_FILE = os.path.join(ROOT, "_tools", "lastmod.json")

SITE = "https://baisahomestays.github.io/baisa-homestay"          # no trailing slash
PAGES = ["index.html", "party-hall/index.html"]                    # English sources (hi/ mirrors are generated)

# ----------------------------------------------------------------------------------------------
# BUSINESS FACTS  (single source of truth for the structured data)
# ----------------------------------------------------------------------------------------------
NAME = "Baisa Home Stay & Party Hall"
ALT_NAMES = ["Baisa Homestay", "Baisa Home Stay and Party Hall",
             "बाईसा होम स्टे एंड पार्टी हॉल", "बायसा होम स्टे"]
PHONES = ["+918209430330", "+919460491850"]
GEO = (26.7347246, 75.821976)                       # Google Maps pin of the listing
CID_URL = "https://maps.google.com/?cid=18422316359885624106"
PLACE_ID = "ChIJ4W4lahvPbTkRKpPZqh83qf8"
AIRBNB = "https://www.airbnb.co.in/rooms/1735537768779780218"
ADDRESS = {
    "@type": "PostalAddress",
    "streetAddress": "ID/130, 14, Ring Road, near Vatika Road, Beelwa, Sukhdeopura Nohara",
    "addressLocality": "Jaipur",
    "addressRegion": "Rajasthan",
    "postalCode": "302029",
    "addressCountry": "IN",
}
DISAMBIG = {
    "en": ("Located on Jaipur Ring Road at Vatika-Beelwa in south Jaipur, near Chokhi Dhani (not in Vaishali Nagar). "
           "Not affiliated with other homestays that have a similar name."),
    "hi": ("जयपुर रिंग रोड पर वाटिका–बीलवा (दक्षिण जयपुर) में, चोखी ढाणी के पास स्थित (वैशाली नगर में नहीं)। "
           "मिलते-जुलते नाम वाले अन्य होमस्टे से कोई संबंध नहीं।"),
}
BIZ_DESC = {
    "en": ("Baisa Home Stay & Party Hall is a garden homestay on Jaipur Ring Road in the Vatika-Beelwa area, "
           "about 10 minutes from Chokhi Dhani. It has six rooms (three air-conditioned, three non-AC) with work "
           "desks, a shared balcony, a garden and free parking, for short stays and long-term rental, plus an "
           "indoor party hall for birthdays, engagements, kitty parties and other celebrations."),
    "hi": ("बाईसा होम स्टे और पार्टी हॉल जयपुर रिंग रोड पर वाटिका–बीलवा इलाके में एक गार्डन होमस्टे है, चोखी ढाणी से लगभग 10 मिनट "
           "की दूरी पर। यहाँ वर्क डेस्क, साझा बालकनी, बगीचे और मुफ़्त पार्किंग वाले छह कमरे (तीन AC, तीन बिना-AC) हैं — छोटे और "
           "लंबी अवधि के ठहराव के लिए — और जन्मदिन, सगाई, किटी पार्टी व अन्य समारोहों के लिए एक इनडोर पार्टी हॉल।"),
}
VENUE_DESC = {
    "en": ("Baisa Party Hall is a private, spacious, well-ventilated indoor hall on the lower level of Baisa Home Stay, "
           "Jaipur, with an elegant stage and décor, comfortable banquet seating and parking, for birthdays, engagements "
           "and ring ceremonies, kitty parties, anniversaries, family get-togethers and small functions."),
    "hi": ("बाईसा पार्टी हॉल जयपुर में बाईसा होम स्टे के निचले तल पर एक निजी, विशाल और हवादार इनडोर हॉल है — भव्य मंच व सजावट, "
           "आरामदायक बैंक्वेट सीटिंग और पार्किंग के साथ — जन्मदिन, सगाई और रिंग सेरेमनी, किटी पार्टी, सालगिरह, पारिवारिक समारोह "
           "और छोटे आयोजनों के लिए।"),
}
# (English, Hindi)
AMENITIES = [
    ("Free parking", "मुफ़्त पार्किंग"),
    ("Dedicated work desks", "वर्क डेस्क"),
    ("Garden", "बगीचा"),
    ("Shared balcony", "साझा बालकनी"),
    ("Self check-in", "सेल्फ़ चेक-इन"),
    ("Air-conditioned rooms (3 of 6)", "एयर-कंडीशन्ड कमरे (6 में से 3)"),
    ("Breakfast on request", "अनुरोध पर नाश्ता"),
    ("Security cameras", "सुरक्षा कैमरे"),
    ("Long-term and monthly stays", "लंबी अवधि और मासिक ठहराव"),
]
VENUE_AMENITIES = [
    ("Indoor hall", "इनडोर हॉल"),
    ("Stage and banquet seating", "मंच और बैंक्वेट सीटिंग"),
    ("Parking on the premises", "परिसर में पार्किंग"),
    ("Catering on request", "अनुरोध पर कैटरिंग"),
    ("Décor assistance", "सजावट में मदद"),
]
ROOMS = [
    {"en": ("Air-conditioned room", "Air-conditioned room with a double bed, a work desk and access to the shared balcony and garden. Three of Baisa's six rooms are air-conditioned."),
     "hi": ("एयर-कंडीशन्ड कमरा", "डबल बेड, वर्क डेस्क और साझा बालकनी व बगीचे तक पहुँच वाला एयर-कंडीशन्ड कमरा। बाईसा के छह में से तीन कमरे एयर-कंडीशन्ड हैं।"),
     "bed": {"@type": "BedDetails", "typeOfBed": "Double bed", "numberOfBeds": 1},
     "features": [("Air conditioning", "एयर कंडीशनिंग"), ("Work desk", "वर्क डेस्क"), ("Balcony access", "बालकनी")],
     "image": "images/room-ac.jpg"},
    {"en": ("Non-AC room", "Non-AC room with a bed, a fan, a work desk and access to the shared balcony and garden. Three of Baisa's six rooms are non-AC."),
     "hi": ("बिना-AC कमरा", "बेड, पंखा, वर्क डेस्क और साझा बालकनी व बगीचे तक पहुँच वाला बिना-AC कमरा। बाईसा के छह में से तीन कमरे बिना-AC हैं।"),
     "features": [("Ceiling fan", "पंखा"), ("Work desk", "वर्क डेस्क"), ("Balcony access", "बालकनी")],
     "image": "images/room-nonac.jpg"},
]
# Only real photos that are shown on the pages. images/party-hall.jpg is deliberately NOT listed anywhere in
# structured data or sitemaps: it is a photo of the owner's banner, which prints a phone number (95115 85857)
# that is not the one on the site - add it back once the owner confirms which numbers are public.
BIZ_IMAGES = ["images/room-hero.jpg", "images/room-ac.jpg", "images/room-nonac.jpg",
              "images/room-desk.jpg", "images/garden.jpg", "images/balcony.jpg"]
VENUE_IMAGES = ["images/hall-interior.jpg"]
LOGO = "images/logo-mark.png"
SAME_AS = [AIRBNB, CID_URL]

# Image lists for the sitemap (per English page)
SITEMAP_IMAGES = {
    "index.html": ["images/room-hero.jpg", "images/room-ac.jpg", "images/room-nonac.jpg", "images/room-desk.jpg",
                   "images/room-longstay.jpg", "images/garden.jpg", "images/balcony.jpg", "images/corridor.jpg",
                   "images/bathroom.jpg", "images/room-corner.jpg"],
    "party-hall/index.html": ["images/hall-interior.jpg"],
}
BREADCRUMB = {"party-hall/index.html": {"en": ("Home", "Party Hall"), "hi": ("होम", "पार्टी हॉल")}}
PAGE_ABOUT = {"index.html": "#business", "party-hall/index.html": "party-hall/#venue"}


def abs_url(path):
    return SITE + "/" + path


def page_url(page, lang):
    d = os.path.dirname(page)                       # '' or 'party-hall'
    parts = ([ "hi" ] if lang == "hi" else []) + ([d] if d else [])
    return SITE + "/" + "".join(p + "/" for p in parts)


# ----------------------------------------------------------------------------------------------
# JSON-LD
# ----------------------------------------------------------------------------------------------
def norm(s):
    return re.sub(r"\s+", " ", s).strip()


class _Head(HTMLParser):
    """Reads <title>, the meta description and og:image - independent of attribute order or quoting."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title, self.desc, self.img, self._in_title = "", "", "", False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "title":
            self._in_title = True
        elif tag == "meta":
            if a.get("name") == "description":
                self.desc = a.get("content") or ""
            elif a.get("property") == "og:image":
                self.img = a.get("content") or ""

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False

    def handle_data(self, data):
        if self._in_title:
            self.title += data


class _Faq(HTMLParser):
    """Collects the VISIBLE FAQ: <details class="faq-item"> -> <summary> = question, everything inside
    <div class="faq-a"> (paragraphs, lists, <br>) = answer. The JSON-LD is built from this, so it always matches the page."""
    BLOCK = {"p", "li", "br", "div", "ul", "ol"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.items, self._q, self._a, self.mode, self._depth, self._in = [], [], [], None, 0, False

    def handle_starttag(self, tag, attrs):
        cls = (dict(attrs).get("class") or "").split()
        if tag == "details" and "faq-item" in cls:
            self._in, self._q, self._a, self.mode = True, [], [], None
        elif self._in:
            if tag == "summary":
                self.mode = "q"
            elif tag == "div" and "faq-a" in cls:
                self.mode, self._depth = "a", 1
            elif self.mode == "a":
                if tag == "div":
                    self._depth += 1
                if tag in self.BLOCK:
                    self._a.append(" ")
            elif self.mode == "q" and tag == "br":
                self._q.append(" ")

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)

    def handle_endtag(self, tag):
        if not self._in:
            return
        if tag == "summary":
            self.mode = None
        elif tag == "div" and self.mode == "a":
            self._depth -= 1
            if self._depth == 0:
                self.mode = None
        elif tag == "details":
            self.items.append((norm("".join(self._q)), norm("".join(self._a))))
            self._in = False
        elif self.mode == "a" and tag in self.BLOCK:
            self._a.append(" ")

    def handle_data(self, data):
        if self.mode == "q":
            self._q.append(data)
        elif self.mode == "a":
            self._a.append(data)


def extract_faq(text):
    f = _Faq()
    f.feed(text)
    return [(q, a) for q, a in f.items if q and a]


def extract_meta(text):
    h = _Head()
    h.feed(text)
    return norm(h.title), h.desc, h.img


def feature(name, value=True):
    return {"@type": "LocationFeatureSpecification", "name": name, "value": value}


def build_jsonld(page, lang, text, dmod):
    i = 0 if lang == "en" else 1
    url = page_url(page, lang)
    title, desc, ogimg = extract_meta(text)
    loc = "en-IN" if lang == "en" else "hi-IN"
    biz_id, venue_id, site_id = SITE + "/#business", SITE + "/party-hall/#venue", SITE + "/#website"

    business = {
        "@type": "LodgingBusiness", "@id": biz_id, "name": NAME, "alternateName": ALT_NAMES,
        "description": BIZ_DESC[lang], "disambiguatingDescription": DISAMBIG[lang], "url": SITE + "/",
        "logo": {"@type": "ImageObject", "url": abs_url(LOGO), "width": 250, "height": 250},
        "image": [abs_url(p) for p in BIZ_IMAGES],
        "telephone": PHONES[0],
        "contactPoint": [{"@type": "ContactPoint", "telephone": p, "contactType": "reservations",
                          "availableLanguage": ["English", "Hindi"], "areaServed": "IN"} for p in PHONES],
        "address": ADDRESS,
        "geo": {"@type": "GeoCoordinates", "latitude": GEO[0], "longitude": GEO[1]},
        "hasMap": CID_URL, "sameAs": SAME_AS,
        "areaServed": {"@type": "City", "name": "Jaipur"},
        "knowsLanguage": ["en", "hi"],
        "checkinTime": "14:00", "checkoutTime": "10:00", "numberOfRooms": 6,
        "amenityFeature": [feature(a[i]) for a in AMENITIES],
        "containsPlace": [],
    }
    for r in ROOMS:
        room = {"@type": "HotelRoom", "name": r[lang][0], "description": r[lang][1],
                "amenityFeature": [feature(f[i]) for f in r["features"]], "image": abs_url(r["image"])}
        if "bed" in r:
            room["bed"] = r["bed"]
        business["containsPlace"].append(room)
    business["containsPlace"].append({"@id": venue_id})

    venue = {
        "@type": "EventVenue", "@id": venue_id, "name": "Baisa Party Hall" if lang == "en" else "बाईसा पार्टी हॉल",
        "alternateName": ["Baisa Party Hall", "बाईसा पार्टी हॉल"], "description": VENUE_DESC[lang], "disambiguatingDescription": DISAMBIG[lang],
        "url": SITE + "/party-hall/", "telephone": PHONES[0], "address": ADDRESS,
        "geo": {"@type": "GeoCoordinates", "latitude": GEO[0], "longitude": GEO[1]},
        "hasMap": CID_URL, "containedInPlace": {"@id": biz_id},
        "image": [abs_url(p) for p in VENUE_IMAGES],
        "amenityFeature": [feature(a[i]) for a in VENUE_AMENITIES],
    }
    website = {"@type": "WebSite", "@id": site_id, "url": SITE + "/", "name": NAME,
               "alternateName": ["Baisa Homestay", "Baisa Home Stay Jaipur"], "inLanguage": ["en-IN", "hi-IN"],
               "publisher": {"@id": biz_id}}
    about_id = SITE + "/" + PAGE_ABOUT[page]
    webpage = {"@type": "WebPage", "@id": url + "#webpage", "url": url, "name": title, "description": desc,
               "inLanguage": loc, "isPartOf": {"@id": site_id}, "about": {"@id": about_id},
               "primaryImageOfPage": {"@type": "ImageObject", "url": ogimg, "width": 1200, "height": 630},
               "dateModified": dmod}
    graph = [website, business, venue, webpage]

    if page in BREADCRUMB:
        names = BREADCRUMB[page][lang]
        webpage["breadcrumb"] = {"@id": url + "#breadcrumb"}
        graph.append({"@type": "BreadcrumbList", "@id": url + "#breadcrumb", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": names[0], "item": page_url("index.html", lang)},
            {"@type": "ListItem", "position": 2, "name": names[1], "item": url}]})

    faqs = extract_faq(text)
    if faqs:
        graph.append({"@type": "FAQPage", "@id": url + "#faq", "inLanguage": loc, "isPartOf": {"@id": url + "#webpage"},
                      "mainEntity": [{"@type": "Question", "name": q,
                                      "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]})
    return {"@context": "https://schema.org", "@graph": graph}, len(faqs)


JSONLD_RE = re.compile(r"<!-- JSON-LD:START.*?<!-- JSON-LD:END -->", re.S)


def jsonld_block(data):
    body = json.dumps(data, ensure_ascii=False, indent=2).replace("</", "<\\/")
    return ("<!-- JSON-LD:START (generated by _tools/build.py - edit the facts there, not here) -->\n"
            '  <script type="application/ld+json">\n' + body + "\n  </script>\n  <!-- JSON-LD:END -->")


def put_jsonld(text, data):
    if not JSONLD_RE.search(text):
        raise SystemExit("missing JSON-LD markers")
    return JSONLD_RE.sub(lambda m: jsonld_block(data), text, count=1)


# ----------------------------------------------------------------------------------------------
# Hindi mirror
# ----------------------------------------------------------------------------------------------
ATTR_RE = re.compile(r'''([^\s"'<>/=]+)(?:\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s"'=<>`]+)))?''')
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}


def parse_tag(raw):
    m = re.match(r"<\s*([A-Za-z][^\s/>]*)(.*?)(/?)>$", raw, re.S)
    name, rest, selfclose = m.group(1), m.group(2), m.group(3) == "/"
    attrs = []
    for am in ATTR_RE.finditer(rest):
        v = am.group(2) if am.group(2) is not None else am.group(3) if am.group(3) is not None else am.group(4)
        attrs.append([am.group(1), v])
    return name, attrs, selfclose


def build_tag(name, attrs, selfclose):
    out = ["<" + name]
    for n, v in attrs:
        out.append(" " + n if v is None else ' %s="%s"' % (n, v.replace('"', "&quot;")))
    out.append(" />" if selfclose else ">")
    return "".join(out)


def fix_url(v):
    """Relative URL one directory deeper (hi/): assets get '../'; page links already mirror the tree."""
    if re.match(r"^(#|/|[A-Za-z][A-Za-z0-9+.-]*:)", v):
        return v
    path = re.split(r"[?#]", v, 1)[0]
    last = path.rstrip("/").rsplit("/", 1)[-1]
    if path in ("", ".", "..") or path.endswith("/") or path.endswith(".html") or "." not in last:
        return v                                        # a page link: the hi/ tree mirrors the English tree
    return "../" + v


def fix_srcset(v):
    out = []
    for cand in v.split(","):
        bits = cand.strip().split(None, 1)
        if bits:
            out.append(" ".join([fix_url(bits[0])] + bits[1:]))
    return ", ".join(out)


def fix_style(v):
    return re.sub(r"url\((['\"]?)([^)'\"]+)\1\)", lambda m: "url(%s%s%s)" % (m.group(1), fix_url(m.group(2)), m.group(1)), v)


def escape_amp(s):
    return re.sub(r"&(?!#?\w+;)", "&amp;", s)


class Mirror(HTMLParser):
    def __init__(self, page):
        super().__init__(convert_charrefs=False)
        self.page = page
        self.out = []
        self.skip_tag = None
        self.skip_depth = 0
        d = os.path.dirname(page)
        # relative link from the Hindi page back to its English twin: hi/ -> "../", hi/party-hall/ -> "../../party-hall/"
        rel = os.path.relpath(d or ".", start=os.path.join("hi", d)).replace(os.sep, "/")
        self.en_href = rel.rstrip("/") + "/"

    # -- start tags ----------------------------------------------------------------------
    def _start(self, tag, selfclose):
        raw = self.get_starttag_text()
        if self.skip_tag:
            if tag == self.skip_tag and tag not in VOID and not selfclose:
                self.skip_depth += 1
            return
        name, attrs, sc = parse_tag(raw)
        d = {n: v for n, v in attrs}
        changed = False
        inner = None

        def setattr_(n, v):
            for a in attrs:
                if a[0] == n:
                    a[1] = v
                    return
            attrs.append([n, v])

        if name == "html":
            setattr_("lang", "hi"); changed = True
        elif name == "body":
            setattr_("class", ((d.get("class") or "") + " lang-hi").strip()); changed = True
        if d.get("id") == "lang-toggle":
            setattr_("href", self.en_href); setattr_("hreflang", "en"); setattr_("lang", "en")
            setattr_("aria-label", "Switch to English")
            inner = "EN"; changed = True
        for n, v in list(attrs):
            if n.startswith("data-hi-") and v is not None:      # data-hi-<attr>="..." -> sets <attr> on the Hindi page
                setattr_(n[len("data-hi-"):], v)
            elif n == "data-hi" and v is not None:              # data-hi="..." -> inner HTML (or content="" on <meta>)
                if name == "meta":
                    setattr_("content", v)
                elif name not in VOID:
                    inner = escape_amp(html.unescape(v))
        if any(n.startswith("data-hi") for n, _ in attrs):
            attrs = [a for a in attrs if not a[0].startswith("data-hi")]
            changed = True
        for a in attrs:
            if a[1] is None:
                continue
            if a[0] in ("href", "src", "poster") and name != "meta":
                nv = fix_url(a[1])
                if nv != a[1]:
                    a[1] = nv; changed = True
            elif a[0] in ("srcset", "imagesrcset"):
                nv = fix_srcset(a[1])
                if nv != a[1]:
                    a[1] = nv; changed = True
            elif a[0] == "style" and "url(" in a[1]:
                nv = fix_style(a[1])
                if nv != a[1]:
                    a[1] = nv; changed = True
        self.out.append(build_tag(name, attrs, sc) if changed else raw)
        if inner is not None and name not in VOID:
            self.out.append(inner)
            self.skip_tag, self.skip_depth = name, 1

    def handle_starttag(self, tag, attrs):
        self._start(tag, False)

    def handle_startendtag(self, tag, attrs):
        self._start(tag, True)

    def handle_endtag(self, tag):
        if self.skip_tag:
            if tag == self.skip_tag:
                self.skip_depth -= 1
                if self.skip_depth == 0:
                    self.out.append("</%s>" % tag)
                    self.skip_tag = None
            return
        self.out.append("</%s>" % tag)

    # -- everything else is passed through untouched -----------------------------------------
    def _pass(self, s):
        if not self.skip_tag:
            self.out.append(s)

    def handle_data(self, data): self._pass(data)
    def handle_entityref(self, name): self._pass("&%s;" % name)
    def handle_charref(self, name): self._pass("&#%s;" % name)
    def handle_comment(self, data): self._pass("<!--%s-->" % data)
    def handle_decl(self, decl): self._pass("<!%s>" % decl)
    def handle_pi(self, data): self._pass("<?%s>" % data)
    def unknown_decl(self, data): self._pass("<![%s]>" % data)


def make_hindi(page, text):
    m = Mirror(page)
    m.feed(text)
    m.close()
    if m.skip_tag is not None:
        raise SystemExit("%s: <%s data-hi=...> was never closed - add its closing tag (HTML allows omitting it, this builder does not)" % (page, m.skip_tag))
    return "".join(m.out)


# ----------------------------------------------------------------------------------------------
# sitemap
# ----------------------------------------------------------------------------------------------
def build_sitemap(rows):
    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
           'xmlns:xhtml="http://www.w3.org/1999/xhtml" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">']
    for page, lastmod in rows:
        en, hi = page_url(page, "en"), page_url(page, "hi")
        for lang, loc in (("en", en), ("hi", hi)):
            out.append("  <url>")
            out.append("    <loc>%s</loc>" % loc)
            out.append("    <lastmod>%s</lastmod>" % lastmod)
            out.append('    <xhtml:link rel="alternate" hreflang="en" href="%s"/>' % en)
            out.append('    <xhtml:link rel="alternate" hreflang="hi" href="%s"/>' % hi)
            out.append('    <xhtml:link rel="alternate" hreflang="x-default" href="%s"/>' % en)
            for img in SITEMAP_IMAGES.get(page, []):
                out.append("    <image:image><image:loc>%s</image:loc></image:image>" % abs_url(img))
            out.append("  </url>")
    out.append("</urlset>")
    return "\n".join(out) + "\n"


# ----------------------------------------------------------------------------------------------
def write_if_changed(path, text):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    old = open(full, encoding="utf-8").read() if os.path.exists(full) else None
    if old == text:
        return False
    with open(full, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    return True


def main():
    state = json.load(open(STATE_FILE)) if os.path.exists(STATE_FILE) else {}
    today = date.today().isoformat()
    rows, report = [], []
    for page in PAGES:
        src = open(os.path.join(ROOT, page), encoding="utf-8").read()
        # lastmod = the day the hand-written content last changed (generated JSON-LD excluded)
        facts = json.dumps(build_jsonld(page, "en", src, "")[0], sort_keys=True, ensure_ascii=False)
        digest = hashlib.sha256((JSONLD_RE.sub("", src) + facts).encode("utf-8")).hexdigest()
        if state.get(page, {}).get("hash") != digest:
            state[page] = {"hash": digest, "date": today}
        dmod = state[page]["date"]
        rows.append((page, dmod))

        data_en, n_faq = build_jsonld(page, "en", src, dmod)
        en_text = put_jsonld(src, data_en)
        hi_text = make_hindi(page, en_text)
        data_hi, _ = build_jsonld(page, "hi", hi_text, dmod)
        hi_text = put_jsonld(hi_text, data_hi)

        changed = [write_if_changed(page, en_text), write_if_changed("hi/" + page, hi_text)]
        t_en, d_en, _ = extract_meta(en_text)
        t_hi, d_hi, _ = extract_meta(hi_text)
        report.append((page, changed, len(t_en), len(d_en), len(t_hi), len(d_hi), n_faq, src.count("data-hi=")))

    write_if_changed("sitemap.xml", build_sitemap(rows))
    json.dump(state, open(STATE_FILE, "w"), indent=2, sort_keys=True)

    print("%-24s %-14s %-9s %-9s %-9s %-9s %-4s %s" % ("page", "files changed", "title(en)", "desc(en)", "title(hi)", "desc(hi)", "FAQ", "data-hi"))
    for page, ch, te, de, th, dh, nf, nh in report:
        print("%-24s %-14s %-9d %-9d %-9d %-9d %-4d %d" % (page, "/".join("Y" if c else "-" for c in ch), te, de, th, dh, nf, nh))
    warn = [r for r in report if r[2] > 62 or r[3] > 165]
    if warn:
        print("WARNING: long English title/description (Google truncates ~60 / ~160 chars):", [w[0] for w in warn])


if __name__ == "__main__":
    sys.exit(main())
