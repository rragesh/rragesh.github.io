# Personal website design system

## Direction

The user supplied `https://www.soorajchandran.com/` as the original style reference, then approved a consulting-conversion direction. Keep the personal editorial identity: Georgia, Manrope, softly fading sky colors, quiet rules, and a day/evening switch. The homepage now leads with the buyer outcome, followed by deployment problems, relevant experience, an assessment offer, process, biography, selected writing, archives, buying FAQs, and a specific LinkedIn invitation. Ragesh’s full name remains in the header, hero identity, metadata, and Person entity; his specialty is explicit in the biography. All professional claims, photography, articles, and profile links belong to Ragesh.

## Typography

- Georgia with Times New Roman/serif fallbacks for the outcome headline, section headings, identity, and featured offer.
- Self-hosted Manrope variable Latin for body and controls, `font-display: swap`.
- Homepage headline: up to 76px desktop, 40–58px mobile, 1.08 line height. The italic closing phrase uses the link color. Homepage section headings: 30–40px. Hero copy: 18px desktop and 16px mobile; supporting prose: 15–17px. Keep readable line lengths.
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

- Primary buttons use link-color fill, paper-color text, a 52px minimum height, and an ink-color hover. Destination labels explicitly identify LinkedIn. Assessment CTAs navigate to the contact brief.
- A portrait and concise professional identity follow the hero actions. NODE Robotics experience and an exact attributed recommendation lead the proof section; Robotair and Fraunhofer support it. Do not fabricate case-study outcomes.
- The assessment and final contact invitation use soft-color surfaces with 12px corners. Deliverables and first-message guidance are ordinary HTML lists; there is no nonfunctional inquiry form or booking widget.
- Three curated articles stay visible. Seven automatically refreshed Medium previews, search, and topic filters live inside a native disclosure. Existing thumbnails remain 150 × 112px desktop and 88px mobile.
- Earlier project imagery and the original career history/recommendations live inside native disclosures. The rover is historical work, not the primary commercial proof. Project URLs remain available.
- Project detail pages share the same tokens, readable text measure, fluid images, and 16:9 video embeds.
- Detailed technical scope uses definition-list rows inside a disclosure. Buying FAQs stay expanded in ordinary HTML and exactly match the structured data.
- The additional story at `about.html` inherits these tokens with a 740px reading column, a 40–64px headline, the existing Phoenix II photograph, quiet chapter anchors, and continuous 16–17px first-person prose. Dates and results are woven into the narrative. It explains how the experience shaped Ragesh without timeline columns, repeated takeaway blocks, or a duplicate service pitch. Current-work content stays at capability level. The homepage keeps its approved conversion copy and structure; the biography and footer link to the story.

## Interaction

- Day is the fallback without JavaScript. Theme preference persists in localStorage when available; storage failures do not disable controls.
- The theme button has a changing action label and pressed state. Its small sun rotation respects reduced motion.
- Article filters use pressed states; search and topic combine; results are announced by a live status. Empty results offer a reset.
- Content and navigation remain usable with JavaScript blocked. No third-party browser requests are needed by the homepage.
- Focus uses a 2px outline with 5px offset. Native keyboard behavior is preserved throughout.
- Per the owner's request, article, project, and profile links open in new tabs with `noopener`; section navigation stays within the page. Do not add Instagram links.

## Assets and content

Use the existing photography and author-owned Medium covers. New raster assets carry source metadata; `data/assets.md` records provenance. Do not copy the reference site’s illustrations, biography, or signature. Do not reintroduce a résumé PDF; use LinkedIn.
