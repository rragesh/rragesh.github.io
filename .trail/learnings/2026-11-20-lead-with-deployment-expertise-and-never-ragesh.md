---
title: Lead with deployment expertise and never add Instagram
author: Ragesh
date: 2026-11-20
branch: master
id: l-d7846451
scope: repo
status: active
src: agent
touches:
  - ".impeccable/surfaces/home.md"
  - DESIGN.md
  - PRODUCT.md
  - README.md
  - "_config.yml"
  - about.html
  - blog-home.html
  - blog-single.html
  - contact.html
  - css/site.css
---

## Decided
- Position index.html around Ragesh Ramachandran as a Robotics and Physical AI Deployment & Ops Specialist for VC-backed robotics startups because the user clarified that personal SEO and answer-engine discovery, rather than a general portfolio, is the main goal.
- Use the user's supplied 10+ years, NODE Robotics deployment scope of 1,200–1,500+ robots, Robotair founder role, and Fraunhofer IPA/ROS-Industrial experience. data/profile-sources.md distinguishes these owner-provided claims from public evidence because LinkedIn hides full employment records behind sign-in. Do not inflate these into company-wide figures or invent dates.
- Remove all Instagram links because the user explicitly said they have no Instagram account. This corrects the inherited social links in the original site.
- Article, project, and other destination-page links open in new tabs because the user requested it; preserve same-page navigation. scripts/link_policy.py and the generators keep this consistent after rebuilding.
- Structured data must match visible content, and SEO.md records the account-side publishing/indexing steps because no markup guarantees search or AI recommendations.
## In the code
- index.html, css/site.css, scripts/check_site.py, scripts/link_policy.py, scripts/update_medium.py, scripts/build_projects.py, PRODUCT.md, SEO.md, data/profile-sources.md.
