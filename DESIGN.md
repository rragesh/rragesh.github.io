# Personal website design system

## Direction

The owner’s latest direction is a hero-only homepage and a discovery-first funnel: Home → My story / Work / Writing → LinkedIn contact. Preserve the established personal editorial identity: Georgia, Manrope, soft sky colors, quiet rules, and the day/evening switch. The shared navigation names each destination and highlights the current page; project pages identify Work as their parent and include breadcrumbs. Ragesh’s full name, actual photography, and documented experience establish the identity throughout.

## Typography

- Georgia with Times New Roman/serif fallbacks for the outcome headline, section headings, identity, and featured offer.
- Self-hosted Manrope variable Latin for body and controls, `font-display: swap`.
- Homepage headline: up to 60px desktop, 38–52px mobile, 1.08 line height. The dependability phrase uses the link color in roman type. Content-page section headings: 30–40px. Hero copy: 17px desktop and 16px mobile; supporting prose: 15–17px. Keep readable line lengths.
- Project and article headings use restrained sans-serif, with wrapping rather than truncation.

## Colors

| Token | Day | Evening |
| --- | --- | --- |
| Paper | `#fafbf9` | `#15212b` |
| Ink | `#263b45` | `#e7eef0` |
| Secondary text | `#4e626e` | `#b1c2cc` |
| Links | `#245c86` | `#9acdec` |
| Rules | `#cfdddd` | `#3b505e` |
| Soft controls | `#eaf2f3` | `#243746` |
| Sky | `#c6e6ef` | `#294d60` |
| Focus | `#8d4300` | `#f5cd8c` |

The sky fades into paper over the first 900px. Text contrast is checked against both gradient endpoints and the soft control background. Inline prose links retain an underline. Selection, caret, scrollbars, and focus colors use the same token system.

## Layout

- Homepage column: 980px maximum, with narrower prose measures. Project pages retain the 780px column. Side gutters: 32px, reduced to 20px below 600px.
- Header is not sticky. Navigation is always visible and wraps naturally.
- Homepage sections use quiet 1px rules and 72px vertical padding (44px mobile). Editorial split sections and the assessment become one column below 800px. Supporting experience and follow-on options become one column below 600px.

## Components

- Primary buttons use link-color fill, paper-color text, a 52px minimum height, and an ink-color hover. The homepage primary action is “Explore my work”, followed by Story and Writing links. “Get in touch” consistently opens LinkedIn; it is available in every header and at the end of reading paths. Collaboration options live on Work.
- The hero is an editorial two-column composition: personal positioning, value, and discovery links on the left; a 4:5 crop of the owner-supplied ROSCon India 2023 photo, professional identity, and talk link on the right. The home figure is capped at 360px wide. Below 800px, the action comes before the photo. A concise line attributes fleet-scale experience to NODE Robotics. Home has no subsequent content sections.
- NODE Robotics experience and an exact attributed recommendation lead the detailed proof section; Robotair and Fraunhofer support it. Do not fabricate case-study outcomes.
- The assessment on Work uses a soft-color surface with 12px corners. Content pages end with a prominent LinkedIn action and a secondary further-reading link. Deliverables are ordinary HTML lists; there is no inquiry form or booking widget.
- Seven automatically refreshed Medium previews are directly visible on Writing, with search and topic filters. Do not hide the feed inside a disclosure. Additional LinkedIn articles and the ROSCon talk use disclosures below the feed. Thumbnails remain 150 × 112px desktop and 88px mobile.
- Work places professional experience before a visible nine-project grid. All project titles, introductions, and links come from `data/projects.json`. Do not hide projects in an archive disclosure. The rover remains historical work, distinct from current professional experience.
- Project detail pages share the same tokens, readable text measure, fluid images, and 16:9 video embeds.
- Project copy begins with a plain-language introduction above the image, followed by short, project-specific narrative sections in the existing reading column. Technical terms are explained where introduced. Separate design ideas from simulated or measured results. Image descriptions and external resource labels describe what readers will find; each embedded demonstration also has a direct YouTube link.
- Detailed technical scope uses definition-list rows inside a disclosure. Buying FAQs stay expanded in ordinary HTML and exactly match the structured data.
- My story at `about.html` retains its 740px reading column, 40–64px headline, Phoenix II photograph, quiet chapter links, and approved first-person narrative. Dates and results remain woven into the story. Its global navigation matches the rest of the site; current-work details remain at capability level.

## Interaction

- Day is the fallback without JavaScript. Theme preference persists in localStorage when available; storage failures do not disable controls.
- The theme button has a changing action label and pressed state. Its small sun rotation respects reduced motion.
- Article filters use pressed states; search and topic combine; results are announced by a live status. Empty results offer a reset.
- Content and navigation remain usable with JavaScript blocked. No third-party browser requests are needed by the homepage.
- Focus uses a 2px outline with 5px offset. Native keyboard behavior is preserved throughout.
- Per the owner's request, article, project, and profile links open in new tabs with `noopener`; section navigation stays within the page. Do not add Instagram links.

## Assets and content

Use the existing photography and author-owned Medium covers. New raster assets carry source metadata; `data/assets.md` records provenance. Do not copy the reference site’s illustrations, biography, or signature. Do not reintroduce a résumé PDF; use LinkedIn.
