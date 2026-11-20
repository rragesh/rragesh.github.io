---
title: Publish previews statically and send professional enquiries to LinkedIn
author: Ragesh
date: 2026-11-20
branch: master
id: l-19d369be
scope: repo
status: active
src: agent
touches:
  - about.html
  - index.html
  - projects/8_leg.html
  - projects/8_leg_dummy.html
  - projects/Saksha.html
  - projects/astra.html
  - projects/dhruv.html
  - projects/localization.html
  - projects/phoenix.html
  - projects/phoenix_dummy.html
---

## Decided
- Embed Medium RSS previews in index.html at refresh time using scripts/update_medium.py, rather than a browser-side feed proxy or an iframe. This makes links crawlable, avoids CORS dependence, and preserves the last good content when Medium is unavailable.
- The user explicitly requested removing resume/Ragesh_CV.pdf and replacing résumé links with https://www.linkedin.com/in/ragesh-ramachandran/. Keep project-publication PDFs; those are not the résumé.
- The configured origin is the writable fork ipa-rar/rragesh.github.io. The live site is hosted by rragesh/rragesh.github.io, which the available GitHub account cannot push to. Push the fork and use an upstream pull request for publication.
## In the code
- index.html, scripts/update_medium.py, .github/workflows/refresh-medium.yml, projects/*.html, about.html, PRODUCT.md.
