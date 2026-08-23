# Baisa — Homestay & Party Hall website

Bilingual (English / हिंदी) single-page site for **Baisa Home Stay & Party Hall,
Jaipur** (Vatika, on Ring Road, 10 min from Chokhi Dhani). Static — no server, no
monthly fees. Personalised from your Airbnb listing, with your logo & photos.

```
Baisa website/
├── index.html   ← all page content (text, numbers, photos)
├── styles.css   ← colours, fonts, layout (theme at the top)
├── script.js    ← menu, language toggle, gallery lightbox, animations
├── images/      ← your photos + logo (logo-mark, favicon, apple-touch-icon)
└── README.md    ← this guide
```

**Preview:** double-click `index.html`, or serve the folder and open http://localhost:8123.

## What's on the site
- **English ⇄ हिंदी toggle** (top-right). Remembers the visitor's choice.
- **Logo**: the central *baisa* emblem is your favicon + header mark.
- Sections: hero, about, rooms (3 AC + 3 non-AC, short & long-term), party hall,
  amenities, gallery (12 photos), guest highlights, booking, contact + live map.
- **Bookings** (no online form): **Airbnb** = homestay rooms; **WhatsApp** = rooms
  *and* the party hall; **Call** = +91 82094 30330 / +91 94604 91850.

## Edit things
- **Phone/WhatsApp**: search `918209430330` (WhatsApp chat), `919460491850`, and the
  displayed `+91 82094 30330 / +91 94604 91850` in `index.html`.
- **Hindi text**: each translatable element has a `data-hi="…"` attribute (English is
  the visible default). Edit the Hindi there; the toggle swaps between them.
- **Photos**: replace files in `images/` (keep the same names), or edit the `<img src>`.
- **Prices**: rooms currently say "Rates on request" — add numbers in the Rooms section.
- **Colours/fonts**: the `:root { … }` block at the top of `styles.css`.

## Put it online + free analytics (your next target)
1. **Host free**: **Cloudflare Pages** (recommended) or **Netlify** — drag this folder
   in, get HTTPS + a custom domain (e.g. `baisahomestay.in`).
2. **Analytics free**: **Cloudflare Web Analytics** — privacy-first, no cookie banner
   (automatic on Cloudflare Pages). Tracks visits, pages, referrers, devices.
   Ask Claude to add **click-tracking** on the Airbnb/WhatsApp/Call buttons so you can
   see how many enquiries the site drives.

## ⚠️ Before you deploy — remove these source files (don't put them on the live site)
- `BAISA HOMESTAY form.docx` (your internal form draft)
- `logo-full.jpg` and `WhatsApp Image ….jpeg` (raw logo — the cropped versions in
  `images/` are what the site uses)
