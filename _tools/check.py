#!/usr/bin/env python3
"""QA checks for the Baisa site.  Run after `python3 _tools/build.py`:   python3 _tools/check.py
Standard library only.  Exits non-zero if anything is wrong."""
import html
import json
import os
import re
import sys
import xml.etree.ElementTree as ET
from html.parser import HTMLParser

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://baisahomestays.github.io/baisa-homestay"
PAGES = ["index.html", "party-hall/index.html", "hi/index.html", "hi/party-hall/index.html"]
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}
LATIN_OK = re.compile(r"^(Airbnb|WhatsApp|AC|Blinkit|ID|EN|km|PM|AM|Baisa|IN|Google|Maps|FAQ)$", re.I)

errors, notes = [], []


def err(page, msg):
    errors.append("%s: %s" % (page, msg))


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack, self.ids, self.links, self.imgs, self.metas, self.lds = [], [], [], [], {}, []
        self.titles, self.h1, self.canon, self.alts, self.text, self._cur = [], 0, None, [], [], None
        self.in_ld, self.ld_buf, self.skip_text = False, [], 0
        self.lang = None
        self.styles = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "html":
            self.lang = a.get("lang")
        if "id" in a:
            self.ids.append(a["id"])
        if tag == "h1":
            self.h1 += 1
        if tag == "a" and a.get("href") is not None:
            self.links.append(a["href"])
        if tag == "link":
            if a.get("rel") == "canonical":
                self.canon = a.get("href")
            if a.get("rel") == "alternate" and a.get("hreflang"):
                self.alts.append((a["hreflang"], a.get("href")))
            if a.get("rel") in ("icon", "apple-touch-icon", "stylesheet", "preload") and a.get("href"):
                self.links.append(a["href"])
        if tag == "script" and a.get("src"):
            self.links.append(a["src"])
        if tag == "script" and a.get("type") == "application/ld+json":
            self.in_ld, self.ld_buf = True, []
        if "style" in a:
            self.styles.append(a["style"])
        if tag == "img":
            self.imgs.append(a)
        if tag == "meta":
            key = a.get("name") or a.get("property")
            if key:
                self.metas.setdefault(key, []).append(a.get("content", ""))
        if tag in ("script", "style", "noscript", "title"):
            self.skip_text += 1
        if tag == "title":
            self.titles.append("")
        if tag not in VOID:
            self.stack.append((tag, self.getpos()[0]))

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID and self.stack and self.stack[-1][0] == tag:
            self.stack.pop()

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if tag in ("script", "style", "noscript", "title"):
            self.skip_text -= 1
        if tag == "script" and self.in_ld:
            self.in_ld = False
            self.lds.append("".join(self.ld_buf))
        if not self.stack or self.stack[-1][0] != tag:
            self.errs = getattr(self, "errs", [])
            self.errs.append("unexpected </%s> at line %d (open: %s)" % (tag, self.getpos()[0], self.stack[-1] if self.stack else None))
            # recover
            for i in range(len(self.stack) - 1, -1, -1):
                if self.stack[i][0] == tag:
                    del self.stack[i:]
                    break
        else:
            self.stack.pop()

    def handle_data(self, data):
        if self.in_ld:
            self.ld_buf.append(data)
        elif self.titles and self.skip_text and not self.in_ld and self.stack and self.stack[-1][0] == "title":
            self.titles[-1] += data
        elif not self.skip_text:
            self.text.append(data)


def resolve(page, href):
    """Return local file path for a relative href, or None if external/anchor-only."""
    if re.match(r"^([a-zA-Z][a-zA-Z0-9+.-]*:|//)", href):
        return None
    path = href.split("#")[0].split("?")[0]
    if path == "":
        return page
    base = os.path.dirname(page)
    full = os.path.normpath(os.path.join(base, path))
    if path.endswith("/") or os.path.isdir(os.path.join(ROOT, full)):
        full = os.path.join(full, "index.html")
    return full.replace(os.sep, "/")


parsed = {}
for page in PAGES:
    path = os.path.join(ROOT, page)
    if not os.path.exists(path):
        err(page, "file missing (run _tools/build.py)")
        continue
    p = Page()
    p.feed(open(path, encoding="utf-8").read())
    parsed[page] = p
    for e in getattr(p, "errs", []):
        err(page, e)
    if p.stack:
        err(page, "unclosed tags: %s" % p.stack[:5])
    dup = {i for i in p.ids if p.ids.count(i) > 1}
    if dup:
        err(page, "duplicate ids: %s" % sorted(dup))
    if p.h1 != 1:
        err(page, "expected exactly one <h1>, found %d" % p.h1)
    if len(p.titles) != 1 or not p.titles[0].strip():
        err(page, "needs exactly one non-empty <title>")
    for k in ("description", "og:title", "og:description", "og:image", "og:url", "twitter:card", "robots"):
        if k not in p.metas:
            err(page, "missing <meta %s>" % k)
    for im in p.imgs:
        if "alt" not in im:
            err(page, "img without alt: %s" % im.get("src"))
        if im.get("src", "").startswith(("images/", "../images/", "../../images/")) and not (im.get("width") and im.get("height")):
            err(page, "img without width/height: %s" % im.get("src"))
    # canonical + hreflang
    expect = SITE + "/" + ("hi/" if page.startswith("hi/") else "") + ("party-hall/" if "party-hall" in page else "")
    if p.canon != expect:
        err(page, "canonical %r != %r" % (p.canon, expect))
    if p.metas.get("og:url", [""])[0] != expect:
        err(page, "og:url %r != %r" % (p.metas.get("og:url", [""])[0], expect))
    want_lang = "hi" if page.startswith("hi/") else "en"
    if p.lang != want_lang:
        err(page, "<html lang=%r> expected %r" % (p.lang, want_lang))
    d = dict(p.alts)
    twin_en = SITE + "/" + ("party-hall/" if "party-hall" in page else "")
    twin_hi = SITE + "/hi/" + ("party-hall/" if "party-hall" in page else "")
    if d.get("en") != twin_en or d.get("hi") != twin_hi or d.get("x-default") != twin_en:
        err(page, "hreflang set wrong: %s" % d)
    img = p.metas.get("og:image", [""])[0]
    if img.startswith(SITE + "/") and not os.path.exists(os.path.join(ROOT, img[len(SITE) + 1:])):
        err(page, "og:image file missing: %s" % img)
    # links
    for href in p.links:
        tgt = resolve(page, href)
        if tgt is None:
            continue
        if not os.path.exists(os.path.join(ROOT, tgt)):
            err(page, "broken link/asset: %s -> %s" % (href, tgt))
            continue
        if "#" in href and href.split("#")[1] and tgt in parsed:
            if href.split("#")[1] not in parsed[tgt].ids:
                err(page, "missing anchor: %s (in %s)" % (href, tgt))
        elif "#" in href and href.split("#")[1] and tgt.endswith(".html"):
            q = Page(); q.feed(open(os.path.join(ROOT, tgt), encoding="utf-8").read())
            if href.split("#")[1] not in q.ids:
                err(page, "missing anchor: %s (in %s)" % (href, tgt))
    # images, srcset and inline CSS url() must exist too
    refs = []
    for im in p.imgs:
        if im.get("src"):
            refs.append(im["src"])
        refs += [c.strip().split()[0] for c in (im.get("srcset") or "").split(",") if c.strip()]
    for st in p.styles:
        refs += [m.group(2) for m in re.finditer(r"url\((['\"]?)([^)'\"]+)\1\)", st)]
    for r in refs:
        tgt = resolve(page, r)
        if tgt is not None and not os.path.exists(os.path.join(ROOT, tgt)):
            err(page, "missing image/asset: %s -> %s" % (r, tgt))
    # JSON-LD
    if not p.lds:
        err(page, "no JSON-LD")
    for raw in p.lds:
        try:
            data = json.loads(raw)
        except Exception as ex:
            err(page, "JSON-LD does not parse: %s" % ex)
            continue
        graph = data.get("@graph", [data])
        ids = {n.get("@id") for n in graph if isinstance(n, dict)}
        types = [n.get("@type") for n in graph]
        for t in ("WebSite", "LodgingBusiness", "EventVenue", "WebPage"):
            if t not in types:
                err(page, "JSON-LD missing %s" % t)
        biz = next(n for n in graph if n.get("@type") == "LodgingBusiness")
        for req in ("name", "address", "telephone", "geo", "image", "url", "checkinTime", "checkoutTime"):
            if req not in biz:
                err(page, "LodgingBusiness missing %s" % req)
        for n in graph:
            for key in ("isPartOf", "about", "publisher", "containedInPlace"):
                ref = n.get(key)
                if isinstance(ref, dict) and set(ref) == {"@id"} and ref["@id"] not in ids and not ref["@id"].startswith(SITE):
                    err(page, "dangling @id %s" % ref["@id"])
        if "FAQPage" in types:
            faq = next(n for n in graph if n.get("@type") == "FAQPage")
            visible = len(re.findall(r'class="faq-item"', open(os.path.join(ROOT, page), encoding="utf-8").read()))
            if len(faq["mainEntity"]) != visible:
                err(page, "FAQ JSON-LD has %d Q&A but page shows %d" % (len(faq["mainEntity"]), visible))
            # every question and answer in the markup must be word-for-word on the page, with no stray markup
            squash = lambda t: re.sub(r"\s+", "", t)
            on_page = squash(" ".join(p.text))
            for qa in faq["mainEntity"]:
                for label, t in (("question", qa["name"]), ("answer", qa["acceptedAnswer"]["text"])):
                    if re.search(r"[<>]|data-hi", t):
                        err(page, "FAQ %s contains markup: %r" % (label, t[:70]))
                    elif squash(t) not in on_page:
                        err(page, "FAQ %s is not on the visible page: %r" % (label, t[:70]))
                    if not page.startswith("hi/") and re.search(r"[\u0900-\u097F]", t):
                        err(page, "English FAQ %s contains Devanagari: %r" % (label, t[:70]))
        # every local file the JSON-LD points at must exist
        for u in re.findall(r'"(%s/[^"#?]+\.[A-Za-z0-9]+)"' % re.escape(SITE), raw):
            if not os.path.exists(os.path.join(ROOT, u[len(SITE) + 1:])):
                err(page, "JSON-LD references a missing file: %s" % u)
        notes.append("%s: JSON-LD ok (%s), %d images, %d links" % (page, ", ".join(sorted(set(str(t) for t in types))), len(p.imgs), len(p.links)))
    # Hindi pages: report leftover Latin text (review by eye; brand/tech words are fine)
    if page.startswith("hi/"):
        left = []
        for chunk in p.text:
            for w in re.findall(r"[A-Za-z][A-Za-z'’\-]+", chunk):
                if not LATIN_OK.match(w):
                    left.append(w)
        if left:
            notes.append("%s: Latin words still on Hindi page (check they are intended): %s" % (page, sorted(set(left))[:40]))

# sitemap
sm = os.path.join(ROOT, "sitemap.xml")
if os.path.exists(sm):
    ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9", "x": "http://www.w3.org/1999/xhtml", "i": "http://www.google.com/schemas/sitemap-image/1.1"}
    tree = ET.parse(sm)
    locs = [u.find("s:loc", ns).text for u in tree.getroot().findall("s:url", ns)]
    for loc in locs:
        rel = loc[len(SITE) + 1:] if loc.startswith(SITE + "/") else None
        if rel is None:
            err("sitemap.xml", "url outside site: %s" % loc); continue
        if not os.path.exists(os.path.join(ROOT, rel, "index.html")):
            err("sitemap.xml", "url has no file: %s" % loc)
    for img in tree.getroot().iter("{%s}loc" % ns["i"]):
        rel = img.text[len(SITE) + 1:]
        if not os.path.exists(os.path.join(ROOT, rel)):
            err("sitemap.xml", "image missing: %s" % img.text)
    notes.append("sitemap.xml: %d URLs" % len(locs))
else:
    err("sitemap.xml", "missing")
for f in ("robots.txt", "llms.txt", "404.html"):
    if not os.path.exists(os.path.join(ROOT, f)):
        notes.append("(not yet created: %s)" % f)

print("\n".join(notes))
if errors:
    print("\nPROBLEMS (%d):" % len(errors))
    print("\n".join(" - " + e for e in errors))
    sys.exit(1)
print("\nALL CHECKS PASSED")
