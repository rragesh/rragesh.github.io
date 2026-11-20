# Ragesh Ramachandran

Personal robotics portfolio and technical writing at [rragesh.github.io](https://rragesh.github.io/). The reading-first layout takes inspiration from [Sooraj Chandran’s personal site](https://www.soorajchandran.com/), with a conversational introduction, soft sky colors, and a persistent day/evening theme switch.

## Preview locally

```sh
python3 -m http.server 4173
```

Open `http://localhost:4173`. The committed HTML works directly on GitHub Pages; no browser framework or build service is required. Styles and the small progressive-enhancement script are `css/site.css` and `js/site.js`.

## Medium articles

The homepage embeds seven recent stories from [the Medium RSS feed](https://rragesh.medium.com/feed), with locally cached, optimized images, excerpts, publication dates, and links to the original articles. The links include UTM parameters to identify referrals from this website. Full stories stay on Medium.

Previews are real HTML, so they work without JavaScript and are available to search engines. JavaScript adds topic filtering and search. There is no client-side RSS proxy or API key.

Refresh manually:

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
python scripts/update_medium.py
```

The `Refresh Medium articles` GitHub Actions workflow runs daily at 07:23 UTC and can also be started manually. It commits changed previews and requests a rebuild of the original branch-based GitHub Pages site. Repository Actions must be enabled and permitted to write contents. GitHub may disable schedules in inactive public repositories after 60 days; re-enable the workflow if that happens. Forks may need their workflows enabled manually.

If the feed is unavailable, invalid, or empty, refresh fails without changing the homepage. Visitors continue seeing the last successful previews. Missing article images degrade to text-only previews. Thumbnail source URLs are recorded in `data/medium-posts.json` and embedded in image metadata.

## Project pages

Edit `data/projects.json`, then regenerate the nine static project pages:

```sh
python3 scripts/build_projects.py
```

Existing public project URLs and project-publication PDFs are retained. The résumé PDF has been removed; professional profile links point to [LinkedIn](https://www.linkedin.com/in/ragesh-ramachandran/). The old `about.html` route redirects to the homepage’s About section.

Destination-page links open in new tabs with `rel="noopener"`, including generated articles and project pages. Same-page navigation keeps its normal behavior. After adding handwritten links, run `python3 scripts/link_policy.py`. The owner has no Instagram account; do not add an Instagram profile.

## Search positioning

The homepage positions Ragesh as a **Robotics and Physical AI Deployment & Ops Specialist** helping VC-backed robotics startups scale reliable fleets. It includes owner-provided experience, service descriptions, sourced articles, and visible FAQs with matching structured data. See `SEO.md` for search goals, publication/indexing steps, and measurement; `data/profile-sources.md` records provenance and verification limits. Legacy template routes are marked `noindex, follow`.

## Checks

```sh
python -m unittest discover -s tests -v
python scripts/check_site.py
node --check js/site.js
```

The site checker covers local links, fragment targets, new-tab behavior, heading structure, image alt attributes, canonical URLs, sitemap coverage, structured entity references, visible FAQ parity, legacy noindex directives, and résumé/Instagram removal. Feed tests cover escaping, invalid URLs, empty/malformed feeds, tracking-pixel exclusion, and preserving content outside the generated region. Link-policy tests cover safe targets, same-page navigation, script preservation, and idempotence. CI runs these checks on pushes and pull requests.

## Publication

This checkout’s `origin` is `ipa-rar/rragesh.github.io`, a fork of `rragesh/rragesh.github.io`. The public website is published from the original repository. Pushing this fork does **not** update the live website: merge the upstream pull request into the original repository’s `master` branch to publish. Keep its existing branch-based Pages configuration. Development files are excluded through `_config.yml`.

## Assets and design

`PRODUCT.md`, `DESIGN.md`, and `.impeccable/surfaces/home.md` record the content constraints and design. Photography comes from the original portfolio; Medium covers come from the author’s RSS feed. See `data/assets.md` for sources. Manrope is self-hosted under the SIL Open Font License (`fonts/Manrope-OFL.txt`). Original template credit is retained for the historical portfolio content.
