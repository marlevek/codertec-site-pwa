# Delivery verification — 2026-09-10

## Scope

Changed: `en/portfolio/index.html`.

Created:

- `en/portfolio/portfolio-en.css` (scoped CTA contrast and focus styles).
- `en/demos/hvac/index.html`, `hvac.css`, `hvac.js`, `mark.svg`.
- Eight WebP assets under `en/demos/hvac/images/` (four generated subjects, responsive variants, one actual site screenshot).
- `en/demos/hvac/README.md`, `image-prompts.json`, `VALIDATION.md`.
- `tests/hvac_browser.py`.

Portuguese/Spanish pages, shared header/footer, shared CSS/JS, other demos, contact backend, sitemap and service worker were not modified.

## Results

- Chrome headless: demo and English portfolio checked at 320, 375, 390, 430, 768, 1024 and 1440 CSS pixels; no horizontal overflow.
- Demo navigation: open, close on section link, Escape and aria-expanded checks passed. Navigation remains available without JavaScript.
- Portfolio: existing English header/footer loaded; Bootstrap mobile menu opened after its transition. CDN access was enabled for the final visual checks.
- Form: required-field validation, a valid sample submission, service preselection, field reset and confirmation passed; no network submission occurred. Submission is disabled without JavaScript.
- Phone: opens a dismissible native dialog; no real phone call or third-party destination.
- Assets: images decode successfully; alt text and dimensions present. Local file links and demo fragment identifiers resolve.
- SEO: one H1, canonical URL, description, Open Graph and `noindex, follow`; no fictional LocalBusiness/review schema.
- Footer: concept disclosure, CoderTec link, service and contact links present. Mobile bottom space reserves room for the fixed contact bar.
- JavaScript: syntax check passed; no uncaught JavaScript errors. Demo has no console errors or third-party dependencies.
- Existing portfolio chatbot: its external configuration endpoint rejects the localhost origin with CORS. This is an existing global integration and should be checked on the production domain. Analytics requests may be cancelled by test navigation.
- No Lighthouse score was collected. This was a local Chromium validation, not physical-device certification.

## Visual assessment and review

The layout reads as a local Canadian trade business: furnace-led service structure, residential heating equipment, seasonal cooling, small commercial equipment, Calgary-area copy, restrained navy/orange identity, a visible phone and quote path. Sample reviews and generated project imagery are explicitly labelled.

NorthPeak appears before Pet Grooming, Dental Clinic and Dermatology in a wide featured card with an actual demo screenshot. Climátis appears separately above the concepts as a real HVAC client project, retaining its real WhatsApp integration. The final portfolio CTA links to the existing English contact form.

Before external use, review AI-generated equipment for technical plausibility and approve the visual identity/copy. Check physical iOS/Android behaviour and the existing chatbot on the published domain. No deployment was performed by this task.
