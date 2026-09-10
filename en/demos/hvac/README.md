# NorthPeak HVAC concept

Demo route: `/en/demos/hvac/`. Portfolio: `/en/portfolio/`.

NorthPeak is fictional. The page has `noindex, follow`, no LocalBusiness or review structured data, and is intentionally absent from the sitemap. Do not remove the concept disclosures when sharing this demo.

## Behaviour

- The call controls open an accessible native dialog explaining the fictional number. They intentionally do not invoke a telephone handler. A real deployment would replace these controls with the verified business phone number and `tel:` links.
- The quote form validates required fields, email and Canadian postal-code format. Its submit handler prevents transmission, clears the sample entries and announces a demo confirmation. Fields have no `name` attributes, and the submit button remains disabled without JavaScript. No storage, analytics, API, email or backend is used by the demo.
- The mobile navigation supports expanded state, link dismissal, outside clicks and Escape. Without JavaScript, the navigation links remain visible.
- The mobile contact bar includes bottom safe-area spacing; footer padding reserves space to reach all final content.
- Reviews, emergency availability, service areas, maintenance features and equipment imagery are labelled as concept content. No licence, certification, real ratings or performance metrics are claimed.

## Assets

All four photographic source images were generated using the built-in ImageGen tool on 2026-09-10. They are illustrative, not stock photos, client work or technical installation references. No real company branding was requested. Exact prompts are recorded in `image-prompts.json`.

- `images/technician.webp`, `images/technician-small.webp`: technician and outdoor heat pump beside a Canadian-style home.
- `images/furnace.webp`, `images/furnace-small.webp`: forced-air furnace and residential mechanical room.
- `images/cooling.webp`, `images/cooling-small.webp`: residential central air conditioning condenser.
- `images/commercial-small.webp`: rooftop equipment for a small commercial property.
- `images/portfolio-preview.webp`: actual Chrome rendering of this demo at 1440 × 1000, not an AI website mockup.
- `mark.svg`: original simple vector mountain mark.

WebP derivatives use quality 82, explicit dimensions and lazy loading below the hero. The hero uses responsive sources and high fetch priority. No external fonts or frontend libraries are loaded by the demo.

## Verification

`tests/hvac_browser.py` starts an ephemeral loopback HTTP server and runs installed Chrome headlessly through Playwright. Install the Python `playwright` package in your development environment, then run `python tests/hvac_browser.py` from the repository root. Existing portfolio CDN dependencies require network access. No real contact form is submitted.

The test checks 320, 375, 390, 430, 768, 1024 and 1440 px; horizontal overflow; decoded images; menu actions; form validation and no transmission; call-dialog dismissal; noindex; local anchors; no-JavaScript form state; and the English portfolio. It also regenerates the portfolio screenshot. Screenshots and diagnostics are written under `.tmp/hvac-qa/`.

Human review before prospecting: review generated equipment imagery for technical plausibility, review the commercial copy and brand direction, and test on a physical iOS/Android device. Before converting this into a real contractor site, replace all fictional information and connect only a verified contact destination. No Lighthouse score is claimed.
