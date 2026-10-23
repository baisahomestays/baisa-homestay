# SEO guide — Baisa Home Stay & Party Hall

Live site: https://baisahomestays.github.io/baisa-homestay/ · Hindi: `/hi/` · Party hall: `/party-hall/` · `/hi/party-hall/`

> Nobody can honestly promise a #1 ranking in Google, Gemini or ChatGPT. What this file does is (1) list what the
> site now does to be *findable and quotable*, and (2) list the handful of things **only the owner can do** that matter
> most (Google Business Profile, reviews, listings). Do the "Your to-do list" in order — step 1–3 are the big ones.

---

## What the website now does (already built)

| Area | What was added |
|---|---|
| **Pages** | Dedicated **Party Hall** page (its own search intent), plus a real **Hindi version of every page** (`/hi/…`) — before, Hindi was swapped in by JavaScript so Google could never read it. |
| **Titles & descriptions** | Keyword-led, length-checked titles/descriptions per page and language. |
| **Structured data (JSON-LD)** | `LodgingBusiness` (address, geo pin, phones, check-in/out, amenities, rooms), `EventVenue` (party hall), `WebSite`, `WebPage`, `BreadcrumbList`, `FAQPage`. Validated against the schema.org vocabulary (0 errors). Google, Gemini, Bing/ChatGPT and Perplexity all read this. |
| **FAQ + facts for AI answers** | 11 homestay FAQs, 6 party-hall FAQs, a "Baisa at a glance" fact card, and a distances table (airport, railway, Chokhi Dhani, city sights). Answer engines quote exactly this kind of plain, factual text. |
| **Language handling** | `hreflang` (en / hi / x-default), per-language canonical URLs, visitor's language choice remembered. |
| **Crawl files** | `sitemap.xml` (with images + hreflang), `robots.txt` (AI crawlers explicitly allowed), `llms.txt`, branded `404.html`. |
| **Sharing** | Open Graph + Twitter cards; 1200×630 share images (~100 KB, so WhatsApp previews work). |
| **Local signals** | Exact map coordinates, `geo.*` tags, visible address + phone in every footer, "Write a Google review" link. |
| **Speed / quality** | Hero image preloaded, fonts no longer block first paint, image sizes declared (no layout jump), descriptive alt text, `<main>`/skip-link/landmarks, favicons in the sizes Google wants (multiples of 48 px). |
| **Spelling** | Hindi brand spelling unified to **बाईसा** (matches your logo and Google listing). |

### Honest notes
* **`robots.txt` / `llms.txt` only take effect at the root of a domain.** On the free `github.io/baisa-homestay/` address
  they sit in a sub-folder, so crawlers ignore them (no robots.txt = "everything allowed", so nothing is blocked). They become
  active when you move to your own domain. Everything else above works today.
* **Star ratings are not marked up** in the structured data on purpose: Google does not allow a business to mark up its own
  third-party ratings, and doing so risks a penalty. The 4.9★ is shown as plain text.
* Distances are approximate **road** distances computed from the map pin; travel time depends on traffic.
* **Some things only fully work on your own domain, not on `github.io/baisa-homestay/`:** the small logo next to your result in Google (favicon), the "site name" shown in results, `robots.txt` and `llms.txt` are all read at the root of a domain. They are set up and will switch on once you move to a custom domain (step 6).
* **FAQ markup** is included for Bing, ChatGPT-style answer engines and voice assistants. Google no longer shows expandable FAQ snippets for most websites, so don't expect them in Google results.
* The hall **banner photo** (`images/party-hall.jpg`, shown on the home page and in the gallery) prints the phone number 95115 85857. I kept that photo out of the structured data and sitemap; once you tell me which numbers are public I can add it back (or swap the home-page photo for the clean hall photo).

---

## Your to-do list (highest impact first)

### 1. Google Search Console — get the site into Google (10 min)
1. Go to <https://search.google.com/search-console> → *Add property* → **URL prefix** → paste
   `https://baisahomestays.github.io/baisa-homestay/`
2. Verification: choose **HTML tag**, copy the `<meta name="google-site-verification" …>` line and **send it to me** — I add it to the site, you click *Verify*.
3. *Sitemaps* → add `sitemap.xml` → Submit.
4. *URL inspection* → paste the 4 page URLs → **Request indexing** on each.
Why: today a search for `site:baisahomestays.github.io` finds nothing — the site is invisible until Google is told about it.

### 2. Fix your Google Business Profile (the #1 lever for "homestay near me" and for Gemini's local answers)
Open the profile (search "Baisa home stay and party hall" while signed in as the owner) and:
* **Primary category:** Google's own listing data shows it as **"Banquet hall"** today, so Google treats Baisa as an event venue first. If rooms bring most of your business, change the primary category to **Homestay** (or *Bed & breakfast* / *Guest house*, whichever Google offers) and keep **Banquet hall** and **Event venue** as additional categories. (The primary category has the most weight — keep "Banquet hall" primary only if hall bookings matter more.)
* **Website:** keep `https://baisahomestays.github.io/baisa-homestay/` (already set).
* **Description (≤ 750 chars, paste-ready):**
  *Baisa Home Stay & Party Hall is a garden homestay on Jaipur Ring Road in Vatika–Beelwa, about 10 minutes from Chokhi Dhani. Six spacious rooms (three AC, three non-AC) with work desks, a shared balcony, garden and free parking — for short stays and long-term/monthly rental, with self check-in. Our indoor Baisa Party Hall hosts birthdays, engagements, kitty parties, anniversaries and family functions, with stage, banquet seating and parking. Book rooms on Airbnb, or message us on WhatsApp for rooms and the hall.*
* Add **photos** (rooms, garden, balcony, hall, exterior, signage) — more real photos mean more views and clicks (aim for 20+); add the **WhatsApp/phone** and **booking link** (Airbnb).
* Turn on **messaging**, add **hours** (24 h / by appointment), **attributes** (free parking, etc.), and post an update every week or two (new photos, offers).

### 3. Get more Google reviews (8 today — this moves rankings more than any code change)
Send this link to every guest/host after their stay (WhatsApp works well):
`https://search.google.com/local/writereview?placeid=ChIJ4W4lahvPbTkRKpPZqh83qf8`
Reply to every review (thanks + a keyword naturally, e.g. "…glad you enjoyed your stay near Chokhi Dhani"). Also ask Airbnb guests to review on Airbnb.

### 4. Bing Webmaster Tools + Bing Places (this is what feeds ChatGPT search & Copilot)
* <https://www.bing.com/webmasters> → *Import from Google Search Console* (one click after step 1).
* <https://www.bingplaces.com> → add the business with the **same name/address/phone** as Google.
* After the site is live I can also ping **IndexNow** (the key file is already in the repo; because it lives in a sub-folder the ping names its location) so Bing learns about changes within hours.

### 5. List Baisa where travellers and AI look (keep name/address/phone **identical** everywhere)
Use exactly: **Baisa Home Stay & Party Hall**, *ID/130, 14 Ring Road, near Vatika Road, Beelwa, Sukhdeopura Nohara, Jaipur, Rajasthan 302029*, **+91 82094 30330**, website URL.
Priority: Justdial · Sulekha · TripAdvisor · MakeMyTrip/Goibibo/Booking.com (if you want OTA bookings) · Facebook page · Instagram profile (link in bio) · Apple Business Connect · WhatsApp Business profile (add website). Each is a "mention" AI assistants use to verify the business exists.
Also: a short **YouTube/Instagram Reel walkthrough** of the rooms and hall — video is heavily surfaced by Google and Gemini.

### 6. Get your own domain (strongly recommended, ~₹800/yr)
`baisahomestay.in` (or `.com`) makes the brand searchable, lets `robots.txt`/`llms.txt` work, and avoids the "github.io" look in search results. Steps: buy domain → add a `CNAME` file containing the domain → point DNS at GitHub Pages → *Settings → Pages → Custom domain* (GitHub then 301-redirects the old address). Tell me the domain and I will update every URL (it is one search-and-replace plus a rebuild) and re-submit the sitemap. Update the Google Business Profile website field too.

### 7. Facts I need from you to make the pages stronger (each one answers a real search)
* **Party hall:** seating capacity (seated / standing), starting price or package idea, whether outside catering/DJ is allowed, timings/curfew, AC or not, stage size, more **real hall photos** (the current one is a photo of a banner).
* **Rooms:** Wi-Fi? kitchen/laundry? meals included? per-night **price range** (even "from ₹…") — pages with a price rank and convert better.
* **Long stays:** monthly price range, minimum stay, what's included → I will add a dedicated *Long-term stay in Jaipur* page.
* **About you:** a short host story (who runs Baisa, since when) — answer engines love a human "About".
* **Social links** (Instagram/Facebook/YouTube) so they go into the structured data.
* **Phone numbers:** the hall banner and the old form list **95115 85857**, the site shows **94604 91850**. Tell me which numbers should be public, and whether 94604 91850 is call-only (the site's Contact row labels both "Phone / WhatsApp").
* **Wording on the site I did not change but you should confirm is true** (answer engines repeat it): "Arrive whenever suits you" (the FAQ says check-in is after 2:00 PM), "Book instantly on Airbnb" / "Instant booking" (is Instant Book switched on?), "one of the few places in the area with free parking", "ample parking" and "space for a big gathering" (no capacity is stated anywhere).
* **Photos:** two gallery tiles are the same picture (`room-2.jpg` = `room-longstay.jpg`) — send a different one.

---

## Updating the site (for whoever edits it)
1. Edit `index.html` and/or `party-hall/index.html` (English is the source; every translatable element has a `data-hi="…"` Hindi version; head tags use `data-hi` / `data-hi-<attribute>`).
2. Rebuild + check:
   ```
   python3 _tools/build.py     # regenerates Hindi pages, JSON-LD, sitemap
   python3 _tools/check.py     # links, anchors, JSON-LD, hreflang, FAQ ↔ markup parity
   ```
3. `git add -A && git commit -m "…" && git push` → GitHub Pages republishes in ~1 minute.
Never hand-edit `hi/…` or the JSON-LD block — they are regenerated. Business facts (name, phones, address, amenities, hours) live at the top of `_tools/build.py`.

## How to tell if it's working
* **Search Console → Performance:** impressions/clicks per query (appears within days of indexing; expect real ranking movement over weeks to months — new sites take time).
* **Search Console → Pages:** all 4 URLs should read "Indexed".
* **Rich Results Test** (<https://search.google.com/test/rich-results>) → paste a page URL → it should read the breadcrumb and FAQ markup without errors (that confirms the markup is valid; Google won't show FAQ snippets, see above).
* **AI check:** once indexed, ask ChatGPT, Gemini and Perplexity: *"homestay near Chokhi Dhani Jaipur"*, *"party hall near Chokhi Dhani Jaipur"*, *"Baisa Home Stay Jaipur"*, *"monthly stay Jaipur Ring Road"* — and note whether Baisa appears. Repeat monthly.
