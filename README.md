# Stratedge Consultancy — Website

A four-page marketing site for Stratedge Consultancy (Dubai, UAE). Static HTML, CSS and
vanilla JavaScript — no build step, no framework, no dependencies. Upload the folder to any
host (or drag it into Netlify / Vercel / cPanel) and it runs.

```
website/
├── index.html          Home
├── about.html          About the firm
├── services.html       Six service lines + engagement models
├── contact.html        Enquiry form + FAQ
├── robots.txt
├── sitemap.xml
└── assets/
    ├── css/style.css   Design system + all components
    ├── js/main.js      Animation & interaction engine
    └── img/            Logo variants, favicons, social image
```

## Brand

Taken from the client's brand guidelines (`Stratedge consultants-3.pdf`) — from the
deck's own art direction, not only its spec pages. See **Brand guidelines** below for
where the two disagree.

| Token | Value | Use |
|---|---|---|
| White | `#ffffff` | Primary surface — the site is white-first throughout |
| Blue | `#518a9c` | **Lead colour.** Trust, stability, expertise; carries the **Research** pillar. Listed first and given the widest swatch in the deck, and the default logomark is blue |
| Red | `#d0423a` | Energy, bold action. Carries the **Growth** pillar |
| Orange | `#f5b02f` | Creativity, innovation. Carries the **Innovation** pillar |
| Ink | `#242525` | Warm charcoal — the deck's dark, sampled from its own spreads. Not a cold near-black |
| Paper | `#f5f4f2` | Alternating section background |

Every generic UI accent — buttons, links, eyebrow dots, focus rings, corner marks — reads
`--accent`, which points at blue. Re-pointing those four lines in `:root` re-themes the
site; red survives only where it means the Growth pillar.

The blue and orange are *graphic* colours: on white they measure 3.8:1 and 1.9:1, which is fine
for bars, rules and the triangle but unreadable as small type. Labels therefore use text-safe
variants — `--blue-ink #3e6c7b`, `--orange-ink #8a6208`, `--red-ink #b8372f` — all above 4.5:1.
Anywhere the colour sits on ink, the pure brand value is used instead.

Typography: **Jost** (display, Light/ExtraLight) and **Poppins** (body and labels), loaded
from Google Fonts with system fallbacks.

The guidelines name Anton under HEADING, and the site was built that way at first. That was
wrong. Every heading the deck itself sets — cover, contents, INTRODUCTIONS, CORE VALUE,
LOGO USAGE, COLOR PALETTE, TYPOGRAPHY, SERVICES, THANK YOU — is **Posterama 2001 Light**,
the thin wide geometric. Anton appears in none of its layouts. Page 8 gives it away twice:
the specimen labelled "HEADING 1" sits directly under the words *Title – posterama 2001
light* and is set in that face, and the two "AA" specimens beside it are *both* labelled
"ANTON – REGULAR" while only one of them is Anton. The rationale settles it — *"the
triangular 'A' nods to our signature symbol"* describes Posterama, whose A is a bare
triangle. Anton's A has a crossbar.

Posterama is a licensed Monotype face and cannot be served on the web without a purchased
licence, so **Jost** stands in — the closest free geometric with the same wide, even,
early-modern forms. The triangular A is restored separately by `.triA`; the real letter
stays in the DOM for screen readers and copy-paste, and only its rendering is replaced.
`splitText()` in `main.js` is word-aware so a `.triA` inside an animated heading stays
inside its word instead of being split out of it.

**Aligning it is the whole difficulty**, and it is why `.triA` is a sized box rather than a
mark positioned inside the letter. An inline-block's height is its *line* box, not its cap
height, so anchoring the triangle to `bottom:0` of the span put it below the baseline by the
half-leading plus the descender — which is exactly what made it sit low and read small.
`overflow:hidden` on an inline-block moves its baseline to the bottom margin edge, so a box
of cap height sits on the text baseline at any font size, in any heading, whatever the
line-height. The two numbers in that rule are measured from Jost, not guessed: cap height
`0.700em`, uppercase A advance `0.618em` (so the word's fit is unchanged), plus a hair of
overshoot because a pointed apex reads short against flat-topped caps. The responsive audit
asserts the rendered height stays at `0.722em` on every page and breakpoint.

Logo files were produced from the supplied PNG:
`logo-light@900.png` is the original white wordmark (used on dark surfaces);
`logo-dark@900.png` is an inverted version with the red triangle preserved (used on white).

## Page architecture

The design is built around a visible hairline grid, framed "dossier" panels and dense,
metadata-labelled blocks — the pattern used by firms like McKinsey, BCG and Oliver Wyman, where
structure carries the page rather than empty space.

**Home** (seven sections, deliberately tight) — hero (headline + animated capability orbit + Dubai
skyline horizon + four-credential bar) · capability ticker · positioning statement with the *firm at
a glance* fact ledger · interactive service explorer · dark band: *who we work with* + pull quote ·
method rail (five panels) · sector grid · CTA.

Nothing on the home page is repeated elsewhere: engagement models are summarised in the explorer
column and detailed on Services, and the FAQ lives on Contact. The four hero credentials state the
proof points; the dark band qualifies the audience rather than restating them.

**About** — page hero with firm panel · purpose statement + pull quote · story with animated
diagram · vision & mission · six principles · dark commitments band · leadership.

**Services** — page hero with a service index panel · sticky side navigation with six detailed
service sections, each opening with its own generated chart · engagement models · method summary.

**Contact** — page hero with a dark direct-line panel · three contact cards · enquiry form with a
*what happens next* panel · two-column FAQ.

### Imagery

The site uses no stock photography. Every visual is generated and ships as inline SVG, so there is
nothing to license, nothing to load and nothing to go blurry:

- a Dubai skyline drawn as hairline architecture along the hero base
- the hero capability orbit: a graduated bezel, counter-rotating rings and a hexagonal field with
  the six service lines set around the logo's triangle
- the fact ledger, set in large display type against a red rule rather than boxed
- six service charts (bar, scatter, flow, radial, line, funnel) that draw themselves on scroll
- five method diagrams inside the pinned phase panels
- the rotating triangle compositions built from the logo mark

## Animation

All motion is hand-written — no GSAP, no Lenis, no AOS.

- Preloader with a drawn triangle mark and progress bar
- Method rail: five panels on a horizontal scroll-snap track with arrow controls, drag-to-pan on
  desktop and a progress indicator. It is a plain block section whose height is simply its content —
  no sticky positioning and no JavaScript-set heights — so it cannot leave an empty band at any
  window size. (An earlier pinned-scroll version tied the section height to the viewport in
  JavaScript; that coupling was the source of a persistent black gap and was removed.)
- Interactive service explorer with cross-fading panels, chart redraw and gentle auto-advance
- Charts that draw on reveal (bars grow, lines trace, points fade in)
- The capability orbit assembles on entry — bezel fades up, hexagon scales in, spokes draw outward
  and each node fades in on its own delay; hovering a node lights its spoke
- Word-by-word split-text reveals on every heading
- Scroll reveals (`up`, `fade`, `scale`, `left`, `right`, `clip`, `mask`, `line`) with staggering
- Scroll-linked paragraph highlighting, parallax layers and a drawing timeline rule
- Interactive triangle-mesh canvas in the hero (pauses when off-screen or when the tab is hidden)
- Custom cursor with magnetic buttons and pointer-reactive card glow / tilt (desktop only)
- Animated counters, marquees, sticky auto-hiding navigation, scroll progress bar
- Full-screen mobile menu with staggered entries, accordion FAQ, service scrollspy

Everything respects `prefers-reduced-motion`, and all pointer effects are disabled on touch devices.

### Performance notes

The motion layer is deliberately cheap to run:

- No `filter: blur()` on the background glows and no full-screen blend-mode overlay — both force
  the browser to re-rasterise large areas on every frame. Soft radial gradients do the same job.
- The cursor's follow loop stops the moment the ring catches up, so `requestAnimationFrame` is
  idle whenever the pointer is still. Hover states use two delegated listeners rather than one
  per element.
- Magnetic buttons and card tilt measure their rectangle once per hover and write inside a single
  rAF, instead of forcing layout on every `mousemove`.
- Scroll effects read every measurement first, then write — no interleaved layout thrashing.
- The hero mesh runs at 40fps with batched `Path2D` strokes (8 draw calls per frame instead of
  ~200), a capped pixel ratio, and it stops entirely when scrolled past or when the tab is hidden.
- Marquees, rotating artwork and the spinning mark pause while off-screen.
- `backdrop-filter` is applied to the navigation only while it is stuck to the top.

### Mobile & tablet

The small-screen experience is built, not inherited:

- A fixed bottom action bar (Call · WhatsApp · Enquire) with safe-area padding for notched phones
- The full-screen menu carries its own prominent CTAs
- Hero highlights, sectors, engagement models and contact cards become swipeable, snapping
  carousels with a "swipe" affordance
- Tablets get a two-column service index and two-column deliverable lists rather than a squeezed
  desktop layout
- 16px form fields so iOS never zooms on focus, larger tap targets, and a dedicated layout for
  short landscape screens



## v3 redesign — bold & angular

Review feedback was that the logo read small, the page felt bland, the purpose was not
obvious, and the density read as mess. Measured before the change: logo 28px (37% of the nav
bar, second line ~6px), 38 micro-labels on the home page, 5 rail + 4 grid overlays, 101 words
above the fold and no plain statement of what the firm sells.

Applied across the whole site: home, about, services hub, contact, the six service pages
and the 404. Each top-level page carries its own Dubai photograph so they do not repeat.

What changed:

- **Logo 28px → 48px** in a taller nav bar, so the full lockup is legible
- **Plain-language H1** — "We help UAE businesses decide what to do next" — replacing an
  abstract line, plus a six-item service strip inside the first screen
- **Photography** from Unsplash (free for commercial use, no attribution required):
  a dusk skyline in the hero and a storm-lit skyline behind the dark section
- **Angular motif** — a cut corner on the hero image filled with the brand triangle, a
  wipe-to-black on service cards, a large triangle outline in the closing panel
- **Noise cut** — home page from 1,415 to 291 words and 38 micro-labels to 5; depth now
  lives on the six service pages, which is what they are for

### Photography licensing

Images are from Unsplash under the [Unsplash License](https://unsplash.com/license), which
permits commercial use without attribution.

**One caveat to decide on:** Emaar has historically asserted rights over commercial use of
Burj Khalifa imagery in the UAE. Wide skyline shots that include it are common practice and
low risk; a tight hero shot of the tower alone sits at the riskier end. The images used here
are wide cityscapes rather than isolated portraits of the tower. If the client wants zero
exposure, swap `hero-dubai.webp` and `band-storm.webp` for architecture that excludes it.


## Mobile

The desktop design carries much of its character in hover states, which a touch device never
shows. Rather than let the phone layout fall back to plain text blocks, it gets its own
expression of the same idea:

- **Service cards alternate filled and outlined** on small screens, so the stack has the same
  black-and-red rhythm the hover produces on desktop
- **Hero tightened** so the photograph and its red corner reach the first screen instead of
  sitting a scroll below it
- **Card heights sized to content** rather than to a desktop grid — the services section went
  from 1,625px to about 1,150px
- **Label/value rows stack** instead of squeezing long values into a narrow right column
- **Footer condensed**; the oversized wordmark is hidden below 620px
- Form fields stay at 16px so iOS never zooms on focus

Checked at 375px, 768px and 1440px on every page. No horizontal overflow anywhere.

### Photographic cards

Each service has its own photograph, used as a card background and shared across the home page
and the services hub. Six unrelated photos would have looked like a scrapbook, so each is
converted to a duotone in the brand ink with a faintly warm highlight — different images, one
visual family.

- **Desktop:** the card wipe reveals the photograph instead of flat black
- **Mobile:** alternating cards keep their photograph on permanently, since touch has no hover
- The closing panel carries a city photograph behind the ink on every page
- **Service pages** use the same photograph in full colour in their hero, so an image is muted
  in the grid and comes alive when you land on its page. Their hero now matches every other
  page — copy left, angular photo right — with the old boxed panel replaced by a four-item
  strip beneath

One trap worth recording: a relative `url()` inside a CSS custom property resolves against the
**stylesheet**, not the page that declares it. `--img:url(assets/img/x.webp)` in the HTML was
requesting `/assets/css/assets/img/x.webp`. The paths are written `../img/x.webp` for that
reason, which also makes them correct from every page depth.


## Brand guidelines — what they changed

The client supplied `Stratedge consultants-3.pdf` (brand guidelines, 12 pages) after the site
was built. It contradicted several things that had been assumed from the original brief.

**Services — corrected.** The site was advertising six service lines that were invented to fit
the brief's description. The guidelines define six different ones, and the site now matches:

| Guidelines | Previously on the site |
|---|---|
| Advertising Research & Consultancies | Business Strategy & Growth |
| Management Consultancies | Market Research & Intelligence |
| Marketing Research & Consultancies | Operational Excellence |
| Innovation & AI Research & Consultancies | Market Entry & Expansion |
| Sourcing & Procurement Consultancies | Financial & Commercial Advisory |
| Project Development Consultancies | Brand & Go-To-Market |

Deliverables on each service page are now the exact sub-services the guidelines list, not
invented ones. Old URLs under `/services/` were replaced, so any link to the previous six
will 404 — nothing had been indexed, so no redirects were added.

**Colour, typography and the three pillars — applied.**

*Colour.* The site now runs the guidelines' three values rather than the single red sampled
from the logo file. Colour is not decorative: each of the three carries one pillar, and that
mapping is the only reason a given element is blue rather than orange. See **Brand** above for
the text-safe variants and why they exist.

*Typography.* Anton, Jost and Poppins replaced Sora, Inter, JetBrains Mono and Instrument Serif
across all eleven pages. Anton is condensed and set uppercase for `.h-mega`, `.h-big`, service
card titles, the pillar names and the mobile menu, which is what gives the site its poster
feel. See **Brand** above for the Posterama substitution and the single-weight constraint.

*Brand pillars.* RESEARCH · INNOVATION · GROWTH — the three points of the triangle — are now a
structural device rather than a statement:

| Pillar | Colour | Meaning in the guidelines | Services |
|---|---|---|---|
| Research | Blue `#518a9c` | Trust, stability, expertise | Advertising Research, Marketing Research |
| Innovation | Orange `#f5b02f` | Creativity | Innovation & AI, Project Development |
| Growth | Red `#d0423a` | Energy, bold action | Management Consultancy, Sourcing & Procurement |

- A `#pillars` section on the home page states the three, with the triangle drawn in the three
  colours (`.pillars3`).
- Every service card carries a `bs--research` / `bs--innovation` / `bs--growth` modifier that
  sets `--pillar` and `--pillar-ink`, which drive its number, its corner label and the bar that
  wipes in on hover. On touch devices the bar is always shown — on *every* card, not an
  alternating subset, because a subset reads as a rendering fault rather than as a rhythm.
- The four method steps walk the pillars: Diagnose = research, Design = innovation, Deliver and
  Sustain = growth. The three commitments on the dark photo band use the three colours in
  order, as an echo of the triangle.

**Art direction — corrected after a full read of the deck.** The first pass at the
guidelines read only the spec pages (palette, font names, pillars) and produced a heavy
black Anton poster site. Rendering all twelve spreads showed the deck is the opposite:
thin wide display type, blue leading, warm charcoal darks, hairline rules, and a large
quiet triangle. What changed:

| | Before | Now |
|---|---|---|
| Display type | Anton, heavy condensed | Jost Light/ExtraLight, tracked out |
| Lead colour | Red | Blue |
| Dark surface | `#0a0e11` | `#242525` |
| Logomark | Red triangle | Blue triangle (PNG, WebP, favicons, OG image; originals kept in `assets/img/.red-originals/`) |
| Service names | Uppercase Anton | Poppins SemiBold in the pillar colour, as pp.9–10 set them |
| The A | Ordinary letter | `.triA` — the logomark triangle, on pillar names and headings that open on an A |
| Pillars | One tricolour triangle | Three coloured logomarks, as p6 shows them |

**Imagery — reprinted, not replaced.** The deck's images are not photographs. They are a
paper ground, a gritty high-contrast photographic plate, flat brand-colour geometry printed
slightly out of register, and visible grain. `tools/build_imagery.py` rebuilds the whole set
that way from the site's own Dubai photography, so a stock-photo grid becomes one press run:

- **Page and service heroes** print on the deck's bone (`#cecabe`) — the inset plate p3 uses.
- **Service cards** print on the charcoal, since they sit inside dark-filling cards, with the
  flat shape in the card's own pillar colour.
- **Full-bleed bands** carry white copy, so the shape sits far right at low strength rather
  than under the text.
- Composition varies across the set — scale, placement, and whether the mark is printed solid
  or as the **logomark's rounded outline** (contact, management consultancy, project
  development) — so ten plates read as a run rather than one template used ten times.
- Every plate is normalised with `autocontrast` before the curve, because night shots and
  daylight shots otherwise print at wildly different densities.
- Grain is blurred to 0.9px. Sharper than that roughly doubles every file — WebP cannot
  encode high-frequency noise — and it is not worth it on a `fetchpriority="high"` hero.

**Landmark substitutions.** Four plates were isolated portraits — two of the Burj Khalifa
(innovation & AI) and two of the Burj Al Arab (sourcing & procurement), the building filling
the frame as the subject. Emaar and Jumeirah both assert commercial-image rights over their
towers, and an isolated portrait is the exposed case; a tower appearing among dozens in a
cityscape is not. Those four are now printed from wide skylines instead — `band-dawn`, which
was carrying no references at all, and `band-dusk` — each from a different region of the
source via the `crop` argument, so the hero and the card of one service never repeat a
composition. The `SWAPS` table in `tools/build_imagery.py` holds the crops.

Re-run with `python3 tools/build_imagery.py`. It always works from the untouched originals in
`assets/img/.photo-originals/`, so the treatment never compounds on itself.

**Copy folded in from the deck** (it had been paraphrased or missing): the cover strapline,
the 360°/"from setup to growth" positioning claim, the "we don't just consult — we partner"
line, the full core-value statement, the triangle rationale (now the pillars section's own
copy), "guiding businesses through change with precision and foresight", and the belief line
in the footer of every page.

**Still outstanding — needs the client:**

- **The pillar colour mapping is ambiguous in the source.** Read positionally, p6 gives
  orange=Research, blue=Innovation, red=Growth. Read by the stated meanings on p7 — blue is
  trust/expertise, orange is creativity, red is energy — you get blue=Research,
  orange=Innovation, red=Growth. The site implements the second. Confirm with the client.
- **p9 lists only five distinct services**: "Innovation & Artificial Intelligence Research &
  Consultancies" appears as both №3 and №4, and Marketing Research is missing from that page
  (it is present on p10). The site carries all six correctly.
- **Service naming.** The deck pluralises — "Advertising Research & Consultanc**ies**". The
  site uses the singular throughout. Confirm which the client wants.
- **The business card on p5 is placeholder** — "John Smith, +971-58-234-2345, Dubai, Business
  bay, 1234" — but it implies a real Business Bay address the site does not have.

## Domain — stratedgeconsultancy.com

**It is registered and it expires 2026-09-10.** Checked 2026-09-08: GoDaddy, created
2025-09-10, nameservers `ns47/ns48.domaincontrol.com`, currently serving a GoDaddy
"Launching Soon" parking page. Renewing it is the most urgent item on this list — if it
lapses the firm loses the name the whole brand is built on, and the site's canonical URLs
all point at it.

**Why it matters beyond the renewal.** Every page declares
`<link rel="canonical" href="https://www.stratedgeconsultancy.com/...">` and the sitemap
lists the same URLs. That domain answers HTTP 200 — with the parking page. So a crawler
reading the GitHub Pages site is told the real version lives elsewhere, follows the pointer,
and finds a placeholder. Until DNS moves, the live site cannot rank on its own content.

**The switch, in order.** Do not reorder these — adding the CNAME file before DNS resolves
takes the github.io preview link down without putting anything in its place.

1. Renew the domain.
2. In GoDaddy DNS, for the apex `stratedgeconsultancy.com`, four A records:
   `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`.
   Optionally the AAAA set too: `2606:50c0:8000::153`, `2606:50c0:8001::153`,
   `2606:50c0:8002::153`, `2606:50c0:8003::153`.
3. A CNAME record for `www` pointing at `mohammadmarwanbalkis-sketch.github.io`.
4. Wait for propagation (`dig +short www.stratedgeconsultancy.com` should return the
   github.io host, not the GoDaddy address).
5. Add a file named `CNAME` at the repo root containing exactly
   `www.stratedgeconsultancy.com`, and push.
6. In the repo's Settings → Pages, confirm the custom domain and tick **Enforce HTTPS**
   once the certificate is issued (usually within the hour).

No content changes are needed at the switch — canonicals, `og:url` and the sitemap already
name the final domain. That was deliberate; it is only wrong for as long as DNS is not moved.

## Launch checklist — the five things only you can do

Everything else in Phase 0 and Phase 1 of the roadmap is done. These five need your
accounts or the client's confirmation.

### 1. Point the real domain (blocks everything else)

Search authority accumulates against a domain, so every week on the `github.io` address is
authority thrown away. Once the domain is registered:

```bash
# from the repo root — swap the placeholder for the real domain everywhere
grep -rl "www.stratedgeconsultancy.com" . --include="*.html" --include="*.xml" --include="*.txt" \
  | xargs sed -i '' 's|https://www\.stratedgeconsultancy\.com|https://YOURDOMAIN.com|g'

# tell GitHub Pages about it, then set the same domain in Settings → Pages
echo "YOURDOMAIN.com" > CNAME
git add -A && git commit -m "Point site at production domain" && git push
```

DNS at your registrar: four `A` records for the apex pointing at `185.199.108.153`,
`185.199.109.153`, `185.199.110.153`, `185.199.111.153`, plus a `CNAME` for `www`
pointing at `mohammadmarwanbalkis-sketch.github.io`. Then tick **Enforce HTTPS**.

### 2. Turn on analytics

Open `assets/js/main.js`, find `GA4_ID` near the top, paste your Measurement ID:

```js
var GA4_ID = 'G-XXXXXXXXXX';
```

Left empty, no analytics script loads and no cookies are set. One edit switches it on
across all five pages.

### 3. Verify in Search Console and Bing

Use the **DNS TXT** method in both — it survives redeploys, unlike the HTML-file method.
Submit `https://YOURDOMAIN.com/sitemap.xml` in each once verified. Bing matters more than
its market share suggests: it is a retrieval source for several AI assistants.

### 4. Give the form somewhere to post

Create an endpoint (Formspree, Web3Forms, Getform) and add it to the form tag in
`contact.html`:

```html
<form class="form" data-validate data-endpoint="https://formspree.io/f/XXXX">
```

Until then the form validates and hands off to the visitor's mail client, which loses
anyone without a mail client configured. Test end to end after wiring it.

### 5. Confirm the content the client owns

- **Email address** — `sayed.dahdah@stratededgeconcultancy.com` as given in the brief, and
  the spelling looks like it contains typos. It appears on the contact page, in the footer,
  and in the structured data.
- **Sayed's job title** — "Managing Partner" is an assumption, and it is now also asserted
  in `Person` schema.
- **His photograph** is live on the About page and referenced in `Person` schema. He should be
  happy with this specific frame and crop before the site goes public.
- **Business hours, response time, languages** — presented as commitments on the site.


## Service pages — drafts that need Sayed's pass

The six service lines are now separate pages under `/services/<slug>/`, and `services.html`
is a hub that links to them. Splitting them means each targets its own query cluster instead
of six competing for one URL.

**These are drafts, not finished copy.** They cover methodology and decision-framing, which
is stable professional knowledge. Everything that would need first-hand experience was left
out rather than invented:

- No client results, statistics, prices or durations stated as fact
- No regulatory or licensing specifics — the market entry page explicitly routes licensing
  and legal execution to a licensed corporate services provider or legal counsel
- No claims about Stratedge's track record

Each page runs 770–970 words. The roadmap target was 1,200–1,800, and the gap is deliberate:
the remaining depth should be Sayed's — worked examples, sector specifics, what he has seen
go wrong. That is also the part that will differentiate these pages from every competitor
running the same generic service copy.

**What to add per page, in priority order:**

1. One worked example per service, anonymised if necessary
2. Sector-specific detail where the approach genuinely differs
3. Anything he would say to a client that no competitor would put in writing

Structure per page: question-shaped H2s with self-contained answers (built for AI answer
engines), signals-it-is-time list, client questions, methodology, deliverables, FAQ, related
services. Each carries `Service`, `FAQPage`, `BreadcrumbList` and `WebPage` schema.

## Structured data: what still needs confirming

Every page now carries a JSON-LD `@graph`. Three fields were deliberately left out rather
than guessed, because inventing them would put false facts in machine-readable form:

| Field | Why it is missing | Add it when |
|---|---|---|
| `geo` coordinates + `streetAddress` | No office address in the brief | The Google Business Profile is verified — that becomes the authoritative source |
| `sameAs` | No social profiles supplied | LinkedIn and Instagram are live; add the URLs to the array in each page's `@graph` |
| `openingHours` | Hours never confirmed | The client confirms them |

Validate any changes at [Rich Results Test](https://search.google.com/test/rich-results) and
[Schema Markup Validator](https://validator.schema.org/).

## Original build notes — checklist

1. **Domain / canonical URLs.** Every page currently uses `https://www.stratedgeconsultancy.com`
   in its `<link rel="canonical">`, Open Graph tags, `robots.txt` and `sitemap.xml`.
   Find-and-replace this with the real domain once it is confirmed.
2. **Email address.** The brief lists `sayed.dahdah@stratededgeconcultancy.com`. That spelling
   ("stratededge…concultancy") is used verbatim across the site — please confirm it is correct
   before launch, then find-and-replace if it is not.
3. **Contact form delivery.** The form validates in the browser and then opens the visitor's
   mail client with the enquiry pre-filled, so nothing is lost. To receive submissions directly
   instead, create a form endpoint (Formspree, Web3Forms, Getform or your own script) and put the
   URL in `contact.html`:
   `<form class="form" data-validate data-endpoint="https://your-endpoint">`
4. **Leadership section.** The named leadership card was removed at his request; the section now
   describes the senior-led model without naming anyone. His email address remains as the firm's
   contact channel — confirm whether that should change too.
5. **Claims to confirm.** A few statements were written as reasonable positioning for a strategic
   advisory firm and should be approved (or edited) by the client: "response within one business
   day", "available during UAE business hours", the four-phase method names, the engagement models
   on `services.html`, and the FAQ answers on `contact.html`.
6. **Real proof points.** The stats band on the home page deliberately uses structural figures
   (service lines, sectors, phases) rather than invented performance numbers. Once real figures
   exist — clients advised, years in operation, value of projects supported — swap them into the
   `data-count` attributes in `index.html`.
7. **Social links.** The footer currently links WhatsApp, email and phone only. Add LinkedIn /
   Instagram once the profiles are live (markup is in the `.socials` block of each page).
8. **Analytics.** Add a Google Analytics or Tag Manager snippet before `</head>` on all four pages.

## Editing notes

- Breakpoints: 1180 / 1080 / 900 (tablet + burger menu + action bar) / 760 (swipe carousels) /
  560 (phone), plus a short-landscape rule. Add `class="snap"` to any grid to turn it into a
  swipeable row below 760px.
- CSS and JS are linked with `?v=14`. Bump that number whenever you edit them so browsers and CDNs
  pick up the change instead of serving a cached copy.
- The navigation and footer are duplicated in each HTML file; a change to one must be repeated in
  the other three.
- Section colours, spacing and radii all come from the CSS custom properties in `:root`
  (`assets/css/style.css`, section 1). Changing the brand red there updates the whole site.
- Service content lives in `services.html`; the summary rows on the home page link to the matching
  anchors (`services.html#strategy`, `#research`, `#operations`, `#expansion`, `#financial`, `#brand`).
