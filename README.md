# DM Electricals

Website for DM Electricals (Mwihoko Road, Nairobi).

**Live site:** [dmelectricals.com](https://dmelectricals.com/) (GitHub Pages + custom domain; apex `CNAME` in repo)

The published page is the static site at the repo root (`index.html`).

**SEO & discovery:** `robots.txt`, `sitemap.xml` (homepage + all `services/`, `products/`, `areas/` landing pages), `llms.txt`, `index.html.md`, `humans.txt`, `.well-known/security.txt`, `manifest.webmanifest`. Submit the sitemap URL (`https://dmelectricals.com/sitemap.xml`) in [Google Search Console](https://search.google.com/search-console) and add the HTML verification meta tag where indicated in `index.html`.

**Regenerate SEO pages** after editing `scripts/generate_seo_pages.py`: `py -3 scripts/generate_seo_pages.py`
