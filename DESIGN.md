# Personal website design system

## Direction

The owner’s latest direction is a hero-only homepage and a discovery-first funnel: Home → My story / Work / Writing / How I work → LinkedIn contact. Preserve the personal editorial identity: Source Serif 4 headings, Source Sans 3 reading text, soft sky colors, quiet rules, and the day/evening switch. The owner requested this font refinement after the page-based structure was established. The shared navigation names each destination and highlights the current page; project pages identify My story as their parent, with chapter-specific breadcrumbs and return links.

## Typography

- Self-hosted Source Serif 4 variable Latin for display headings, identity, quotations, and the featured offer; Georgia/Times New Roman/serif fallbacks. A genuine italic face serves the personal signoff.
- Self-hosted Source Sans 3 variable Latin for body, controls, navigation, and working subheadings; Arial/sans-serif fallbacks. A genuine italic face serves citations and emphasized prose.
- Both families support weights 200–900 and use `font-display: swap`. Only the two normal files are preloaded; italic files load when used. Font synthesis is disabled. Local WOFF2 assets and their OFL licenses are recorded in `data/assets.md`.
- Ordinary body: 17px / 1.75; story copy: 17px / 1.8 desktop and 16px mobile. Supporting reading text, blog excerpts, project descriptions, and assessment deliverables use at least 16px. Labels/metadata use 13px, with 14px navigation and a 16px search input. Reading width belongs to the enclosing block, so paragraphs, headings, and media share edges rather than using independent character-width caps.
- Homepage headline: up to 60px desktop, 38–52px mobile, 1.12 line height and -0.025em tracking. H2 tracking is -0.015em with 1.25 line height. Preserve serif/sans hierarchy and allow natural wrapping rather than shrinking long titles.
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

- Shared CSS layout tokens: `--site-width: 980px`, `--reading-width: 660px`, and `--page-gutter: 32px` (20px at 600px and below). Every page's header and footer use the site width. Home and Work use the wider layout for their multi-column compositions; My story, How I work, Writing, and all project detail pages use the centered reading width.
- Page introductions, section-heading groups, FAQs, and closing reading invitations share the 660px reading measure, bounded by the available column. Card headings, descriptions, and thumbnails align within their own grid columns. Project headings, paragraphs, photographs, and video embeds span one column with no nested inset. Story and project photographs retain their full aspect ratio; thumbnail and homepage portrait crops remain deliberate component treatments.
- Desktop reading paragraphs use justified alignment, restrained automatic hyphenation, and a start-aligned final line. This applies to the homepage introduction, page introductions, story chapters, working principles and fit descriptions, project narrative, FAQs, and closing invitations. At 600px and below, the shared prose tokens switch to left alignment, natural wrapping, and manual hyphenation. Short labels, cards, and compact multi-column summaries use natural left alignment at every width.
- Header is not sticky. Navigation is always visible and wraps naturally.
- Homepage sections use quiet 1px rules and 72px vertical padding (44px mobile). Editorial split sections and the assessment become one column below 800px. Supporting experience and follow-on options become one column below 600px.

## Components

- Primary buttons use link-color fill, paper-color text, a 52px minimum height, and an ink-color hover. The homepage primary action is “Explore my work”, followed by Story and Writing links. “Get in touch” consistently opens LinkedIn; it is available in every header and at the end of reading paths. Work's engagement comparison provides three individually named LinkedIn actions.
- The hero is an editorial two-column composition: personal positioning, value, and discovery links on the left; a 4:5 crop of the owner-supplied ROSCon India 2023 photo, professional identity, and talk link on the right. The desktop figure is capped at 360px wide. Below 800px, the photo becomes an 88–104px-wide portrait beside the name, role, and talk link, between the introduction and discovery links. Source order follows this mobile reading sequence, with one shared photo and caption. The hero ends with discovery links; experience metrics belong on Work, rather than in a separate homepage proof line. Home has no subsequent content sections.
- NODE Robotics experience and an exact attributed recommendation lead the detailed proof section; Robotair and Fraunhofer support it. Do not fabricate case-study outcomes.
- Work presents three premium engagement options in one 12px-cornered, thin-bordered comparison: Deployment Readiness Assessment, Production deployment engineering, and Fractional Robotics DevOps leadership. Three equal desktop columns use subgrid to align serif titles, descriptions, scope lists, and 52px LinkedIn actions. The engineering column has a subtle soft-color background; no popularity claim or invented price is shown. At 1000px and below, the options stack in reading order with horizontal separators; mobile copy stays naturally left-aligned. Verified NODE Robotics experience and individually agreed commercial terms follow the comparison. Content pages end with a prominent LinkedIn action and a secondary further-reading link. Deliverables are ordinary HTML lists; there is no inquiry form or booking widget.
- Seven automatically refreshed Medium previews are directly visible on Writing, with search and topic filters. Do not hide the feed inside a disclosure. Additional LinkedIn articles and the ROSCon talk use disclosures below the feed. Thumbnails remain 150 × 112px desktop and 88px mobile.
- Work flows from engagement options to professional experience, a short engineering-story invitation, the engagement process, FAQs, and a closing invitation. Its introduction explains that path, and local navigation follows engagement options, experience, process, and questions. DOM and visual reading order match at every width. Experience uses four consistent editorial rows: a 264px organization/role column, a 56px gap, and a content column that reaches the shared 660px reading width at desktop. Rows stack below 800px. Current-work capabilities form a two-column definition list inside the content column, stacking at 600px. NODE results are a concise list, followed by its attributed recommendation within the same entry; founder and research entries use the same alignment. Quiet horizontal rules separate roles. The former gallery's `#projects` anchor contains the story invitation, with heading and prose aligned to the 660px reading measure. All nine earlier projects are linked within My story; their detail content and story-chapter assignments live in `data/projects.json`. FAQs use two readable columns above 800px, then one, with natural left alignment.
- Project detail pages share the same tokens, readable text measure, fluid images, and 16:9 video embeds. Their closing primary action returns to the corresponding story chapter; LinkedIn remains a secondary action alongside it.
- Project copy begins with a plain-language introduction above the image, followed by short, project-specific narrative sections in the existing reading column. Technical terms are explained where introduced. Separate design ideas from simulated or measured results. Image descriptions and external resource labels describe what readers will find; each embedded demonstration also has a direct YouTube link.
- Detailed technical scope uses definition-list rows inside a disclosure. Buying FAQs stay expanded in ordinary HTML and exactly match the structured data.
- The technical-capabilities disclosure previews its purpose with “From code to fleet operations.” Its full-width native summary has visible View/Hide details text and a plus/minus state indicator. Expanded scope uses four concise definition-list entries in a two-column grid with quiet separators, stacking at 600px and below. Body copy is 16px, capability headings 18px, and the summary title 20px; keyboard and no-JavaScript behavior remain native.
- My story at `about.html` uses one shared 660px reading column. The introduction leads into the essay; the Phoenix II photograph follows the rover-team paragraph, and the localization image follows the France/calibration paragraph. Both images retain their aspect ratio, with 32px vertical spacing, 16px contribution-focused captions, and a project link beneath. Autonomous docking is linked within the prose. Earlier rover work and the SAKSHA/ASTRA/DHRUV explorations use small, visible chapter link groups with quiet rules and 44px link targets. All nine projects appear exactly once, with no gallery interrupting the narrative. Preserve the 40–64px headline and first-person story; current-work details remain at capability level.
- My story paragraphs use justified alignment on desktop, with restrained automatic hyphenation and a start-aligned final line. At 600px and below, paragraphs are left-aligned without automatic hyphenation to avoid stretched word spacing. Headings, captions, chapter links, and the personal signoff are left-aligned within the shared column.
- How I work uses the shared 660px reading column, with ten plainly titled principles, a concise definition-list fit summary, and a LinkedIn invitation. It opens with the people-first DevOps philosophy and its connection to becoming a founder. The owner removed the public influences section to keep the page focused on working together; source references remain in development notes. Main navigation includes this destination and wraps below 1000px so the labels stay readable.
- Work's experience section leads with a current-work entry for the stealth defense robotics startup. Capability-level delivery and quality-process contributions come before earlier organizations; current employer and actual position are never named.

## Interaction

- Day is the fallback without JavaScript. Theme preference persists in localStorage when available; storage failures do not disable controls.
- The theme button has a changing action label and pressed state. Its small sun rotation respects reduced motion.
- Article filters use pressed states; search and topic combine; results are announced by a live status. Empty results offer a reset.
- Content and navigation remain usable with JavaScript blocked. No third-party browser requests are needed by the homepage.
- Focus uses a 2px outline with 5px offset. Native keyboard behavior is preserved throughout.
- Per the owner's request, article, project, and profile links open in new tabs with `noopener`; section navigation stays within the page. Do not add Instagram links.

## Assets and content

Use the existing photography and author-owned Medium covers. New raster assets carry source metadata; `data/assets.md` records provenance. Do not copy the reference site’s illustrations, biography, or signature. Do not reintroduce a résumé PDF; use LinkedIn.
