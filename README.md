# Ragesh Ramachandran

The personal site of [Ragesh Ramachandran](https://rragesh.github.io/), organized around discovery → reading and exploration → a LinkedIn conversation. The homepage contains only the positioning hero, ROSCon photograph, and clear paths into the site. Its editorial identity retains the serif typography, soft sky colors, and day/evening theme inspired by [Sooraj Chandran’s personal site](https://www.soorajchandran.com/).

## Pages and navigation

- `index.html` — Home: who Ragesh is and where to explore next.
- `about.html` — My story: the personal robotics journey, with all nine earlier projects linked within their relevant chapters.
- `work.html` — Work: professional experience, collaboration options, and a short bridge to the engineering story.
- `writing.html` — Writing: visible Medium previews, learning notes, and talks.
- `how-i-work.html` — How I work: working principles, communication preferences, team fit, and a direct LinkedIn invitation. Supporting source references live in development notes.
- `projects/*.html` — individual projects, with My story active in navigation and breadcrumbs/return links to their story chapter.

Every page offers Home, My story, Work, Writing, How I work, and **Get in touch**, which links directly to LinkedIn. End-of-page links connect the reading paths. Work introduces the engagement options, supports them with professional experience and an engineering-story invitation, then answers questions before contact. The FAQ covers scope, collaboration, and handover; the old `work.html#process` bookmark lands at its heading. The current employer and position remain private. Old homepage fragment links such as `/#writing` and `/#work` forward to their new pages when JavaScript is available; navigation still works without JavaScript.

The site is built with [Astro](https://astro.build/) as fully static HTML. Pages ship no framework JavaScript; only the small progressive-enhancement script runs in the browser.

| What | Where |
| --- | --- |
| Main page content | `src/pages/{index,about,work,writing,how-i-work}.astro` |
| Titles, descriptions, social images, JSON-LD | `src/data/pages.json` (read through `src/data/pages.ts`) |
| Project content | `src/data/projects.json`, validated by `src/content.config.ts` |
| Project page template | `src/pages/projects/[slug].astro` |
| Shared `<head>`, header, footer | `src/layouts/BaseLayout.astro`, `src/components/` |
| Styles and browser script | `src/styles/site.css`, `src/scripts/site.js` (bundled and fingerprinted) |
| Images to optimize | `src/assets/` (served as responsive AVIF/WebP) |
| Files served as-is | `public/` (fonts, favicon, PDFs, redirects, robots.txt) |

`build.format: "file"` keeps every historical URL (`about.html`, `projects/Saksha.html`, …). Write internal links as root-absolute paths such as `/work.html` and `/about.html#origins`. In `.astro` markup, keep inline elements on the same line as neighbouring text: Astro's HTML compression removes whitespace that contains a line break next to a tag, which would run words together.

## Develop locally

```sh
npm ci
npm run dev       # live-reloading dev server
npm run build     # static site in dist/
npm run preview   # serve dist/
```

Requires Node.js 22 or later (CI uses 24).

## Medium articles

The dedicated Writing page displays seven recent stories from [the Medium RSS feed](https://rragesh.medium.com/feed) directly, without opening a disclosure. Each preview has a locally cached image, excerpt, publication date, and link to the original article. Search and topic filters enhance the visible feed. Additional LinkedIn writing and the ROSCon talk are available in disclosures below it. Refresh updates only the cached post data; it does not add articles back to Home. Article links include UTM parameters. Full stories stay on Medium.

Previews are rendered into static HTML at build time from `src/data/medium-posts.json` (`src/components/writing/ArticleCard.astro`), so they work without JavaScript and are available to search engines. JavaScript adds topic filtering and search. There is no client-side RSS proxy or API key.

Refresh manually:

```sh
npm run medium:refresh
```

This updates `src/data/medium-posts.json` and caches new thumbnails as WebP in `src/assets/medium/`. Use `node scripts/update-medium.mjs --feed-file feed.xml` to test against a saved feed.

The `Deploy website` workflow refreshes the previews daily at 07:23 UTC (and on manual runs), builds and checks the site, commits changed previews to `master`, and deploys. Repository Actions must be enabled and permitted to write contents. GitHub may disable schedules in inactive public repositories after 60 days; re-enable the workflow if that happens.

If the feed is unavailable, invalid, or empty, refresh exits with an error without changing any files, and the site is built with the last successful previews. Missing article images degrade to text-only previews. Thumbnail source URLs are recorded in `src/data/medium-posts.json` and embedded in image metadata.

## Project pages

Each project has a plain-language `intro`, descriptive `imageAlt`, search `summary`, and `sections` containing a `heading` and `paragraphs`. Its `storyChapter` (`origins` or `control`) determines the breadcrumb and return destination; link the project from that chapter in `src/pages/about.astro`. Explain the problem before introducing the engineering, define technical terms in context, and distinguish prototypes, simulations, and measured results. Publications, repositories, and demonstration links remain available for deeper reading.

Edit `src/data/projects.json`; the build regenerates the nine project pages. The schema in `src/content.config.ts` fails the build on a missing image, an unknown story chapter, empty text, or unexpected fields. `image` paths are relative to the JSON file (for example `../assets/work/pro1.JPG`); the page serves responsive AVIF/WebP versions and a 1200px social preview instead of the original photo.

Existing public project URLs and project-publication PDFs are retained. My story links every project exactly once through two captioned visual examples, an inline docking link, and small contextual link groups. Work's former `#projects` anchor remains as a visible invitation to the story, including without JavaScript. The résumé PDF remains private; professional profile links point to [LinkedIn](https://www.linkedin.com/in/ragesh-ramachandran/). `about.html` connects planetary rovers, control and recovery, industrial robotics, Robotair, production fleets, and current software-factory work through first-person narrative. The current employer, position, internal product names, operational metrics, and personal details from the private CV are not published.

## Legacy cleanup

The old Colorlib demo pages are lightweight, JavaScript-free redirects in `public/`, copied to the build unchanged:

| Old route | Destination |
| --- | --- |
| `blog-home.html`, `blog-single.html` | `writing.html` |
| `contact.html` | `work.html` (collaboration and LinkedIn contact) |
| `portfolio.html`, `portfolio-details.html` | `about.html#origins` |
| `services.html` | `work.html#expertise` |
| `elements.html` | `index.html` |

Bootstrap, jQuery and its plugins, template Sass/CSS, icon fonts, the PHP mail handler, bundled template documentation, and unreferenced images have been removed. The site uses `src/styles/site.css`, `src/scripts/site.js`, and self-hosted Source Serif 4 and Source Sans 3 fonts. Project data is maintained directly in `src/data/projects.json`. `about.html` now serves the personal story.

Source photography is documented in `data/assets.md`. Project-publication PDFs are retained; the original template credit was removed from public footers at the owner's request.

## Link policy

Destination-page links open in new tabs with `rel="noopener"`, including generated articles and project pages. Same-page navigation keeps its normal behavior. The `link-policy` integration (`src/integrations/`) applies this to every built page after `astro build`, so do not write `target`/`rel` by hand. The owner has no Instagram account; do not add an Instagram profile.

## Search positioning

Home introduces Ragesh as a robotics engineer and founder. Story provides the personal context; Work holds professional evidence, services, and matching FAQs; Writing holds article references and previews. Each page has its own canonical URL, metadata, and appropriate structured data connected to the same Person identity. Pricing and availability are not invented. See `SEO.md` for publication/indexing steps and `data/profile-sources.md` for provenance. Legacy template routes remain marked `noindex, follow`.

## Checks

```sh
npm test                                   # Medium refresh and link-policy tests
npx astro check                            # types and content schema
npm run build
python3 scripts/check_site.py              # checks dist/ (or --dist PATH)
python3 -m unittest discover -s tests -v   # live-publication checker tests
```

`sitemap.xml` is generated from the page metadata and the projects collection (`src/pages/sitemap.xml.ts`). The site checker validates the built output and covers consistent navigation/current-page state, a hero-only Home, visible Medium previews, all nine projects linked from their declared story chapters, project breadcrumbs/return paths, the Work story bridge, local targets, stylesheet assets, link behavior, headings, image alt text, canonical URLs, sitemap coverage, entity references, FAQ parity, compatibility redirect destinations/fallback links/noindex directives, and résumé/Instagram removal. It also checks bundled CSS/JS, font URLs inside the built CSS, responsive image sources, and that social images exist in the build. Feed tests cover entity decoding, invalid URLs, empty/malformed feeds, tracking pixels, and leaving files untouched when a refresh fails. Link-policy tests cover safe targets, navigation, script preservation, and idempotence. The `Check website` workflow runs these checks on pull requests; `Deploy website` runs them before every deployment.

It also verifies unique page titles/descriptions, social-preview images, project authorship, the Robotair founder relationship, and crawler access. After deployment, run `python scripts/check_live.py` to verify the **public** site rather than just the working copy. Publication tests ensure this check rejects stale pages, incorrect canonicals, and indexing restrictions.

## Publication

This checkout’s `origin` is `rragesh/rragesh.github.io`. Publish by merging the feature pull request into `master`; the `Deploy website` workflow builds `dist/`, runs the checks, and deploys it with GitHub Pages Actions. Pushing a feature branch does not update the live website.

GitHub Pages must use **Settings → Pages → Build and deployment → Source: GitHub Actions**. When migrating from the old branch-based site, switch the source *before* merging: the currently published site stays live until the first Actions deployment, whereas a branch build of the new repository layout would publish a broken site.

## Assets and design

`PRODUCT.md`, `DESIGN.md`, and `.impeccable/surfaces/home.md` record the content constraints and design. Photography comes from the original portfolio and the owner-supplied ROSCon photo; Medium covers come from the author’s RSS feed. Source Serif 4 and Source Sans 3 are self-hosted variable Latin fonts, with normal/italic faces and OFL licenses in `public/fonts/`. Only normal faces are preloaded. See `data/assets.md` for pinned sources and `DESIGN.md` for type roles.
