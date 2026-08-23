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

| Token | Value | Use |
|---|---|---|
| White | `#ffffff` | Primary surface — the site is white-first throughout |
| Brand red | `#d13a45` | Secondary colour, sampled from the logo triangle. Accents, CTAs, highlights |
| Ink | `#0b0d10` | Text and the dark contrast sections |
| Paper | `#f7f7f8` | Alternating section background |

Typography: **Sora** (headings), **Inter** (body), **JetBrains Mono** (labels and numbering),
loaded from Google Fonts with system fallbacks.

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

## Before launch — checklist

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
4. **Leadership section.** `about.html` lists Sayed Dahdah as *Managing Partner* with a short
   descriptive bio, and uses an "SD" monogram placeholder. Confirm the job title and replace the
   monogram with a photograph when one is available.
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
- CSS and JS are linked with `?v=6`. Bump that number whenever you edit them so browsers and CDNs
  pick up the change instead of serving a cached copy.
- The navigation and footer are duplicated in each HTML file; a change to one must be repeated in
  the other three.
- Section colours, spacing and radii all come from the CSS custom properties in `:root`
  (`assets/css/style.css`, section 1). Changing the brand red there updates the whole site.
- Service content lives in `services.html`; the summary rows on the home page link to the matching
  anchors (`services.html#strategy`, `#research`, `#operations`, `#expansion`, `#financial`, `#brand`).
