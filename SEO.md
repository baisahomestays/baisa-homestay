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

## What Google shows today (checked 24 Oct 2026, one day after going live)
* **Not indexed yet:** `site:baisahomestays.github.io` returns nothing (Google even suggests Search Console). Expected — step 1 fixes it.
* **"baisa party hall jaipur"**: your **Google Business Profile appears at the top** (4.98★, phone 082094 30330, "Open · Closes 9 pm") — but labelled **"Banquet hall"**. Below it rank *other people's pages about you*: **Justdial** ("Baisa Party Hall in Beelwa", 5.0★, 8 reviews, hours 9 am–5 pm, PIN **303905**), a **CareB4Cure** page (the link from the early chats — PIN 303905 too), and **EventsPlace** ("starting at just ₹5,000").
* **"baisa homestay"**: dominated by a **different business with almost the same name — "Baisa Homestay" in Vaishali Nagar** (Justdial, Facebook "Baisa Home stay" ~270 followers, Instagram `@baisa_homestay`, other phone numbers). Your site must therefore always say *where* you are: **Ring Road, Vatika, near Chokhi Dhani** (it does, in the title, H1, FAQ and structured data).
* **Generic searches** ("homestay jaipur", "bnb jaipur", "stays near chokhi dhani", "stays vatika road") are owned by **Booking.com, MakeMyTrip, Goibibo, Agoda, TripAdvisor, Airbnb** and Google's own hotel-price box. A new small site will not outrank them there; the realistic wins are the **Google Business Profile / map results** and long-tail searches such as *"homestay near Chokhi Dhani"*, *"party hall Vatika road"*, *"baisa party hall"*. For "stays vatika road", Google shows a neighbouring villa on Vatika Road **because its profile is categorised "Home stay"** — yours is "Banquet hall", so it is not eligible for those boxes.
* **Address inconsistency:** Google's profile says PIN **302029**; Justdial, CareB4Cure and a neighbouring business on the same road say **303905**. Pick the true postal PIN and use it everywhere (the website currently says 302029).

### Standing out from the other "Baisa Homestay" (Vaishali Nagar) — they are NOT related to you
**Done on the site:** "Vatika" added to the title/description; a visible FAQ ("Are you the Baisa Homestay in Vaishali Nagar? — No…"), a note under the distances table, a line on the party-hall page, `disambiguatingDescription` in the structured data (English + Hindi), and a line in `llms.txt`.

**What works (do these):**
1. **Get indexed** (step 1) — until then the site cannot compete at all.
2. **Switch the Google profile's primary category to Homestay** (step 2). Do **not** put place words into the business *name* field ("Baisa Home Stay Vatika") — that breaks Google's rules and can get the profile suspended.
3. **Reviews, steadily** (step 3): count and recency decide who Google shows first for an ambiguous name. Ask every guest.
4. **Make the entity unmistakable:** identical name / address / phone / PIN on every listing (fix Justdial hours + PIN; ask EventsPlace and the CareB4Cure page to add your website). Create **your own** Instagram + Facebook page with a distinctive handle (e.g. `baisa_homestay_partyhall` — the plain `baisa_homestay` is taken), put the website in the bio, and send me the links so they go into the structured data (`sameAs`).
5. **Win the searches that include a place or product** instead of the bare name: *baisa party hall*, *baisa home stay and party hall*, *baisa homestay vatika*, *baisa homestay ring road*, *homestay near chokhi dhani*. You already top the first one with your profile; the site now carries all of these phrases.
6. **Links and mentions:** a YouTube walkthrough titled with the location, local event planners / decorators / caterers who link to you, wedding-venue directories, a distinctive **domain** (step 6).
7. *(Optional, paid)* A small **Google Ads** campaign on location keywords ("party hall near Chokhi Dhani", "homestay Vatika Jaipur"). Don't bid on the other business's name.

**What not to do:** copy their name, handle, website or photos; buy or write fake reviews; stuff keywords into the profile name; report them without a real reason; "negative SEO". It backfires, and Google can penalise it.

**Realistic expectation:** for an ambiguous name Google often shows *both* businesses. The goal is to appear beside them with a clearly different description and to win every search that includes your place or product. Expect weeks to months, not days.

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
* **Primary category:** Google's own listing data shows it as **"Banquet hall"** today, so Google treats Baisa as an event venue first. If rooms bring most of your business, change the primary category to **Homestay** (or *Bed & breakfast* / *Guest house*, whichever Google offers) and keep **Banquet hall** and **Event venue** as additional categories. (The primary category has the most weight — keep "Banquet hall" primary only if hall bookings matter more. It is also why Baisa is missing from Google's "stays" results today.)
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
Priority: **first fix the listings that already exist** (Justdial: hours, PIN, add the website; EventsPlace; the CareB4Cure page — add the website link, same phone/PIN), **then** add Booking.com · MakeMyTrip · Goibibo · Agoda · TripAdvisor (they own the generic "homestay jaipur" searches and feed Google's hotel price box) · Sulekha · Facebook page · Instagram profile (link in bio) · Apple Business Connect · WhatsApp Business profile (add website). Each is a "mention" AI assistants use to verify the business exists.
Also: a short **YouTube/Instagram Reel walkthrough** of the rooms and hall — video is heavily surfaced by Google and Gemini.

### 6. Get your own domain (strongly recommended, ~₹800/yr)
A domain makes the brand searchable, lets `robots.txt`/`llms.txt` work, and avoids the "github.io" look in results.
* **Do NOT use `baisahomestay.com` / `.in`**: the other "Baisa Homestay" (Vaishali Nagar) advertises *www.baisahomestay.com* on its Facebook page. Even if it is unregistered today, using it invites confusion and disputes.
* **Looked free on 24 Oct 2026** (check at the registrar before buying): `baisapartyhall.com` / `.in`, `baisahomestayjaipur.com`, `baisahomestayandpartyhall.com`, `baisavatika.com` / `.in`, `baisastays.com` / `.in`. Taken: `baisajaipur.com`, `baisajaipur.in`.
* A name that covers both businesses and the place works best, e.g. `baisavatika.in` or `baisahomestayjaipur.com`. Keep it short and easy to say on a phone call.
* Steps: buy domain (~₹800/yr) → add a `CNAME` file containing the domain → point DNS at GitHub Pages → *Settings → Pages → Custom domain* (GitHub then 301-redirects the old address). Tell me the domain and I will update every URL (one search-and-replace plus a rebuild) and re-submit the sitemap. Update the Google Business Profile website field too.

### 7. Facts I need from you to make the pages stronger (each one answers a real search)
* **Party hall:** seating capacity (seated / standing), starting price or package idea, whether outside catering/DJ is allowed, timings/curfew, AC or not, stage size, more **real hall photos** (the current one is a photo of a banner).
* **Rooms:** Wi-Fi? kitchen/laundry? meals included? per-night **price range** (even "from ₹…") — pages with a price rank and convert better.
* **Long stays:** monthly price range, minimum stay, what's included → I will add a dedicated *Long-term stay in Jaipur* page.
* **About you:** a short host story (who runs Baisa, since when) — answer engines love a human "About".
* **Social links** (Instagram/Facebook/YouTube) so they go into the structured data.
* **Phone numbers:** the hall banner and the old form list **95115 85857**, the site shows **94604 91850**. Tell me which numbers should be public, and whether 94604 91850 is call-only (the site's Contact row labels both "Phone / WhatsApp").
* **Wording on the site I did not change but you should confirm is true** (answer engines repeat it): "Arrive whenever suits you" (the FAQ says check-in is after 2:00 PM), "Book instantly on Airbnb" / "Instant booking" (is Instant Book switched on?), "one of the few places in the area with free parking", "ample parking" and "space for a big gathering" (no capacity is stated anywhere).
* **Photos:** two gallery tiles are the same picture (`room-2.jpg` = `room-longstay.jpg`) — send a different one.
* **Is the Vaishali Nagar "Baisa Homestay" (Facebook / Instagram / Justdial) related to you?** If not, I can add a gentle "find us on Ring Road, Vatika" disambiguation to the site and structured data; if it is a sister property, we should link the two properly.
* **Correct postal PIN** (302029 or 303905)? I will update the site and structured data to match.
* **Who runs the CareB4Cure page and the EventsPlace / Justdial listings?** Ask them to add the website and use the same phone, hours and PIN. EventsPlace shows a hall price "from ₹5,000" — is that accurate?

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
