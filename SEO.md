# Search and answer-engine discoverability

## Objective

Help search systems and visitors identify **Ragesh Ramachandran** as a **Robotics and Physical AI Deployment & Ops Specialist** serving **VC-backed robotics startups**. The target problem is moving from fragile pilots to repeatable operations at 1,000+ robot scale.

## Implemented

- Name and specialty in the visible H1, title, description, social metadata, opening summary, and consistent Person entity.
- Specific service coverage: ROS/ROS 2 CI/CD, packaging, releases, OTA updates, fleet observability, incident response, and on-premise/hybrid/cloud infrastructure.
- Owner-supplied professional experience at NODE Robotics, Robotair, Fraunhofer IPA, and ROS-Industrial, with public links to organizations and relevant published articles.
- A visible, concise question-and-answer section; ProfilePage, Person, Service, WebSite, and FAQ structured data reflect page content.
- Stable entity identifiers and sameAs links connect the website, LinkedIn, Medium, and GitHub identities. Past roles are not mislabeled as current employment in worksFor.
- Static article previews, text-first HTML, crawlable links, canonical URLs, an XML sitemap, and unrestricted crawling in robots.txt.
- Legacy template/demo routes are lightweight redirects to the relevant homepage sections, with fallback links, the homepage canonical URL, and `noindex, follow`. They remain crawlable so search engines can see those instructions. Do not block those routes in robots.txt while expecting their noindex directives to be processed.
- Checks validate structured-data references, visible FAQ parity, canonical URLs, and sitemap targets.
- All nine project pages have unique search titles/descriptions, Open Graph and Twitter previews, and WebPage/CreativeWork data linked to the same Ragesh author identity as the homepage.
- Robotair's Organization entity identifies Ragesh as its founder, consistent with the visible biography. Search checks also verify access for Googlebot, bingbot, OAI-SearchBot, Claude-SearchBot, and PerplexityBot under the existing open robots policy.

## Readiness verification

```sh
python -m unittest discover -s tests -v
python scripts/check_site.py
```

After the original GitHub Pages site deploys, run:

```sh
python scripts/check_live.py
```

This verifies the actual HTTP responses, canonical metadata, published structured identities, sitemap, and crawler access across every sitemap page. It fails if the old homepage still returns HTTP 200 without the new profile. It also checks `X-Robots-Tag` and HTML indexing directives. Passing means publication is technically accessible; it does not mean Google or an answer engine has indexed or recommended the site.

For a local server, use `python scripts/check_live.py --base-url http://127.0.0.1:4173/`. Production canonicals are still expected in local HTML.

## Query themes

These are intent-based content targets, not measured keyword-volume or ranking claims:

| Intent | Themes |
| --- | --- |
| Find the person | Ragesh Ramachandran robotics; Ragesh Ramachandran Robotair; Ragesh Ramachandran robotics DevOps |
| Find specialist support | robotics DevOps specialist; Physical AI deployment specialist; robot fleet operations consultant; ROS 2 deployment support |
| Solve deployment problems | ROS 2 CI/CD pipelines; OTA updates for robot fleets; on-premise robot deployment; robotics release engineering |
| Improve operations | robot fleet observability; robotics incident response; scaling AMR fleets; robot rollout health |

## Publication and measurement

1. Merge the upstream PR into `rragesh/rragesh.github.io` and verify the resulting public HTML. A push to the fork alone does not publish this domain.
2. In Google Search Console, verify the existing property, submit `https://rragesh.github.io/sitemap.xml`, and inspect/request indexing for the homepage. Use Bing Webmaster Tools for Bing discovery. These account-side actions require the owner's access; they were not performed by this change.
3. Keep the website link, professional title, and core biography consistent on LinkedIn, Medium, GitHub, and Robotair. Where possible, obtain links from real conference speaker pages, professional biographies, and relevant project pages.
4. Add a public ROSCon talk/recording link and detailed, permission-cleared deployment case studies when available. Describe context, personal contribution, technical decisions, and measured outcomes; do not invent customer details or fleet reliability metrics.
5. Record a Search Console baseline and compare branded and non-branded impressions, queries, clicks, and click-through rate after recrawling. Review monthly. AI Overviews and AI Mode traffic are included in Google's overall Web search reporting; they are not a separate guaranteed acquisition channel.
6. Monitor inbound LinkedIn conversations and Medium referrals alongside search traffic. The Medium links already carry referral parameters; no new tracking service was added.

## Limits

Google's [AI-feature guidance](https://developers.google.com/search/docs/appearance/ai-features) says there are no special AI-search optimization requirements. Clear content, evidence, crawlability, and accurate structured data improve eligibility and understanding; they do not guarantee indexing, rankings, AI citations, or recommendations. FAQ structured data does not make this site eligible for Google's government/health-focused FAQ rich results. No keyword volume, ranking, or backlink measurements were available in this implementation.

Factual provenance and verification limitations are recorded in `data/profile-sources.md`.
