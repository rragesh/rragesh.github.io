# Ragesh Ramachandran

The personal site of [Ragesh Ramachandran](https://rragesh.github.io/), organized around discovery → reading and exploration → a LinkedIn conversation. The homepage contains only the positioning hero, ROSCon photograph, and clear paths into the site. Its editorial identity retains the serif typography, soft sky colors, and day/evening theme inspired by [Sooraj Chandran’s personal site](https://www.soorajchandran.com/).

## Pages and navigation

- `index.html` — Home: who Ragesh is and where to explore next.
- `about.html` — My story: the personal robotics journey, with all nine earlier projects linked within their relevant chapters.
- `work.html` — Work: professional experience, collaboration options, and a short bridge to the engineering story.
- `writing.html` — Writing: visible Medium previews, learning notes, and talks.
- `how-i-work.html` — How I work: working principles, communication preferences, team fit, and a direct LinkedIn invitation. Supporting source references live in development notes.
- `projects/*.html` — individual projects, with My story active in navigation and breadcrumbs/return links to their story chapter.

Every page offers Home, My story, Work, Writing, How I work, and **Get in touch**, which links directly to LinkedIn. End-of-page links connect the reading paths. Work leads with the current confidential software-factory experience; the employer and position remain private. Old homepage fragment links such as `/#writing` and `/#work` forward to their new pages when JavaScript is available; navigation still works without JavaScript.

Edit the main content in `data/pages/*.html` and metadata in `data/pages.json`, then run `python3 scripts/build_pages.py`. The shared header/footer live in `scripts/site_layout.py`. Commit both sources and generated pages. CI checks that generated output matches its sources.

## Preview locally

```sh
python3 -m http.server 4173
```

Open `http://localhost:4173`. The committed HTML works directly on GitHub Pages; no browser framework or build service is required. Styles and the small progressive-enhancement script are `css/site.css` and `js/site.js`.

## Medium articles

The dedicated Writing page displays seven recent stories from [the Medium RSS feed](https://rragesh.medium.com/feed) directly, without opening a disclosure. Each preview has a locally cached image, excerpt, publication date, and link to the original article. Search and topic filters enhance the visible feed. Additional LinkedIn writing and the ROSCon talk are available in disclosures below it. Refresh updates `data/pages/writing.html`, `writing.html`, and the cached post data; it does not add articles back to Home. Article links include UTM parameters. Full stories stay on Medium.

Previews are real HTML, so they work without JavaScript and are available to search engines. JavaScript adds topic filtering and search. There is no client-side RSS proxy or API key.

Refresh manually:

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
python scripts/update_medium.py
```

The `Refresh Medium articles` GitHub Actions workflow runs daily at 07:23 UTC and can also be started manually. It commits changed previews and requests a rebuild of the original branch-based GitHub Pages site. Repository Actions must be enabled and permitted to write contents. GitHub may disable schedules in inactive public repositories after 60 days; re-enable the workflow if that happens. Forks may need their workflows enabled manually.

If the feed is unavailable, invalid, or empty, refresh fails without changing the Writing page. Visitors continue seeing the last successful previews. Missing article images degrade to text-only previews. Thumbnail source URLs are recorded in `data/medium-posts.json` and embedded in image metadata.

## Project pages

Each project has a plain-language `intro`, descriptive `imageAlt`, search `summary`, and `sections` containing a `heading` and `paragraphs`. Its `storyChapter` (`origins` or `control`) determines the breadcrumb and return destination; link the project from that chapter in `data/pages/story.html`. Explain the problem before introducing the engineering, define technical terms in context, and distinguish prototypes, simulations, and measured results. The builder still accepts the original flat `paragraphs` format for legacy imports. Publications, repositories, and demonstration links remain available for deeper reading.

Edit `data/projects.json`, then regenerate the nine static project pages:

```sh
python3 scripts/build_projects.py
python3 scripts/build_pages.py
```

Existing public project URLs and project-publication PDFs are retained. My story links every project exactly once through two captioned visual examples, an inline docking link, and small contextual link groups. Work's former `#projects` anchor remains as a visible invitation to the story, including without JavaScript. The résumé PDF remains private; professional profile links point to [LinkedIn](https://www.linkedin.com/in/ragesh-ramachandran/). `about.html` connects planetary rovers, control and recovery, industrial robotics, Robotair, production fleets, and current software-factory work through first-person narrative. The current employer, position, internal product names, operational metrics, and personal details from the private CV are not published.

## Legacy cleanup

The old Colorlib demo pages are lightweight, JavaScript-free redirects to the current pages:

| Old route | Destination |
| --- | --- |
| `blog-home.html`, `blog-single.html` | `writing.html` |
| `contact.html` | `work.html` (collaboration and LinkedIn contact) |
| `portfolio.html`, `portfolio-details.html` | `about.html#origins` |
| `services.html` | `work.html#expertise` |
| `elements.html` | `index.html` |

Bootstrap, jQuery and its plugins, template Sass/CSS, icon fonts, the PHP mail handler, bundled template documentation, and unreferenced images have been removed. The site uses `css/site.css`, `js/site.js`, and self-hosted Source Serif 4 and Source Sans 3 fonts. Project data is maintained directly in `data/projects.json`; the completed one-time legacy importer has been removed. `about.html` now serves the personal story.

Source photography is documented in `data/assets.md`. Project-publication PDFs are retained; the original template credit was removed from public footers at the owner's request.

## Link policy

Destination-page links open in new tabs with `rel="noopener"`, including generated articles and project pages. Same-page navigation keeps its normal behavior. After adding handwritten links, run `python3 scripts/link_policy.py`. The owner has no Instagram account; do not add an Instagram profile.

## Search positioning

Home introduces Ragesh as a robotics engineer and founder. Story provides the personal context; Work holds professional evidence, services, and matching FAQs; Writing holds article references and previews. Each page has its own canonical URL, metadata, and appropriate structured data connected to the same Person identity. Pricing and availability are not invented. See `SEO.md` for publication/indexing steps and `data/profile-sources.md` for provenance. Legacy template routes remain marked `noindex, follow`.

## Checks

```sh
python -m unittest discover -s tests -v
python scripts/build_pages.py --check
python scripts/build_projects.py --check
python scripts/check_site.py
node --check js/site.js
```

The site checker covers consistent navigation/current-page state, a hero-only Home, visible Medium previews, all nine projects linked from their declared story chapters, project breadcrumbs/return paths, the Work story bridge, local targets, stylesheet assets, link behavior, headings, image alt text, canonical URLs, sitemap coverage, entity references, FAQ parity, compatibility redirect destinations/fallback links/noindex directives, and résumé/Instagram removal. Feed tests cover escaping, invalid URLs, empty/malformed feeds, tracking pixels, and preserving content outside the generated region. Link-policy tests cover safe targets, navigation, script preservation, and idempotence. CI runs these checks on pushes and pull requests.

It also verifies unique page titles/descriptions, social-preview images, project authorship, the Robotair founder relationship, and crawler access. After deployment, run `python scripts/check_live.py` to verify the **public** site rather than just the working copy. Publication tests ensure this check rejects stale pages, incorrect canonicals, and indexing restrictions.

## Publication

This checkout’s `origin` is `rragesh/rragesh.github.io`. Publish by merging the feature pull request into `master`; pushing a feature branch does not update the live website. Keep the existing branch-based Pages configuration. Development files are excluded through `_config.yml`.

## Assets and design

`PRODUCT.md`, `DESIGN.md`, and `.impeccable/surfaces/home.md` record the content constraints and design. Photography comes from the original portfolio and the owner-supplied ROSCon photo; Medium covers come from the author’s RSS feed. Source Serif 4 and Source Sans 3 are self-hosted variable Latin fonts, with normal/italic faces and OFL licenses in `fonts/`. Only normal faces are preloaded. See `data/assets.md` for pinned sources and `DESIGN.md` for type roles.
