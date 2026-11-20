# Personal website design system

## Direction

The user supplied `https://www.soorajchandran.com/` as a style reference during implementation. The finished site follows its personal-letter feel: a serif greeting, a narrow readable column, softly fading sky colors, simple inline navigation, and a day/evening switch. All biography, project photography, articles, and profile links belong to Ragesh. The earlier cobalt exhibition direction is superseded.

## Typography

- Georgia with Times New Roman/serif fallbacks for greeting, section headings, and the personal signoff. This follows the user’s reference-led direction.
- Self-hosted Manrope variable Latin for body and controls, `font-display: swap`.
- Desktop greeting: 58px maximum; mobile: 42px. Section headings: 34px desktop, 30px mobile. Introduction: 17px desktop, 16px mobile at a generous line height.
- Project and article headings use restrained sans-serif, with wrapping rather than truncation.

## Color tokens

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

## Layout and components

- Main column: 780px maximum; introduction prose: 660px. Side gutters: 32px, reduced to 20px below 600px.
- Header is not sticky. Navigation is always visible and wraps naturally.
- Sections are separated by quiet 1px rules and 56px vertical padding (42px mobile).
- Medium stories form an unboxed list with 150 × 112px thumbnails on desktop and 88px thumbnails on mobile. Text, dates, and outbound links are always present in HTML.
- The featured rover has a larger photo; supporting projects use a two-column desktop grid and small image/text rows on mobile.
- Native disclosure controls hold the project archive and original recommendations.
- Project detail pages share the same tokens, readable text measure, fluid images, and 16:9 video embeds.

## Interaction

- Day is the fallback without JavaScript. Theme preference persists in localStorage when available; storage failures do not disable controls.
- The theme button has a changing action label and pressed state. Its small sun rotation respects reduced motion.
- Article filters use pressed states; search and topic combine; results are announced by a live status. Empty results offer a reset.
- Content and navigation remain usable with JavaScript blocked. No third-party browser requests are needed by the homepage.
- Focus uses a 2px outline with 5px offset. Native keyboard behavior is preserved throughout.

## Assets and content

Use the existing photography and author-owned Medium covers. New raster assets carry source metadata; `data/assets.md` records provenance. Do not copy the reference site’s illustrations, biography, or signature. Do not reintroduce a résumé PDF; use LinkedIn.
