# Baisa — Homestay & Party Hall website

Bilingual (English / हिंदी) static site for **Baisa Home Stay & Party Hall, Jaipur** (Vatika, Ring Road,
10 min from Chokhi Dhani). No server, no monthly fees. Live on GitHub Pages:
**https://baisahomestays.github.io/baisa-homestay/**

```
Baisa website/
├── index.html            ← English home page  (SOURCE — edit this)
├── party-hall/index.html ← English Party Hall page (SOURCE — edit this)
├── hi/                   ← Hindi versions — GENERATED, don't edit by hand
├── styles.css            ← colours, fonts, layout (theme at the top)
├── script.js             ← menu, language link, lightbox, animations
├── images/               ← photos, logo, favicons, share images
├── _tools/               ← build.py (generator) + check.py (QA)  — not published
├── sitemap.xml · robots.txt · llms.txt · 404.html   ← search/AI crawler files
├── SEO.md                ← what's been done + owner to-do list for search/AI visibility
└── README.md             ← this guide
```

## Edit things
- **Text**: edit the English in `index.html` / `party-hall/index.html`. Every translatable element
  also has a `data-hi="…"` attribute holding its Hindi text (head tags use `data-hi` or `data-hi-<attribute>`).
- **After ANY edit, rebuild:**
  ```
  python3 _tools/build.py     # regenerates hi/ pages, JSON-LD structured data, sitemap.xml
  python3 _tools/check.py     # QA: links, anchors, JSON-LD, hreflang, FAQ markup parity
  ```
- **Phone/WhatsApp**: search `918209430330` (WhatsApp), `919460491850`, and the displayed
  `+91 82094 30330 / +91 94604 91850` in both English pages and in `_tools/build.py` (structured data).
- **Business facts for search engines** (name, address, hours, amenities, rooms): top of `_tools/build.py`.
- **Photos**: replace files in `images/` (keep names/sizes, or update `width`/`height` in the `<img>` tags).
- **Prices**: rooms say "Rates on request" — add numbers in the Rooms section (prices also help search).
- **Colours/fonts**: the `:root { … }` block at the top of `styles.css`.
- **Language switch**: English lives at `/`, Hindi at `/hi/` (real pages so Google can index both).

## Publish
`git add -A && git commit -m "…" && git push` — GitHub Pages republishes in about a minute.
The remote is `baisahomestays/baisa-homestay`; pushes authenticate as the `accakks` GitHub account.
Ignored (never published): `.claude/`, the form `.docx`, the raw logo files — see `.gitignore`.

## Search & AI visibility
Read **SEO.md** — it lists what the site already does and the owner steps that matter most
(Google Search Console, Google Business Profile category + reviews, Bing, listings, custom domain).

Preview locally: `python3 -m http.server 8123` in this folder, then open http://localhost:8123.
