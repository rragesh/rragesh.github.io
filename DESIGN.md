# Personal website design system

## Direction

The owner’s latest direction is a hero-only homepage and a guided reading path: Home → My story → Work → How I work → Writing → subscribe on Medium or connect on LinkedIn. Preserve the personal editorial identity: Source Serif 4 headings, Source Sans 3 reading text, soft sky colors, quiet rules, and the day/evening switch. The shared navigation follows the reading order and highlights the current page; project pages identify My story as their parent, with chapter-specific breadcrumbs and return links. Reading stays in the same tab, with new tabs reserved for LinkedIn and YouTube.

## Typography

- Self-hosted Source Serif 4 variable Latin for display headings, identity, quotations, and the featured offer; Georgia/Times New Roman/serif fallbacks. A genuine italic face serves the personal signoff.
- Self-hosted Source Sans 3 variable Latin for body, controls, navigation, and working subheadings; Arial/sans-serif fallbacks. A genuine italic face serves citations and emphasized prose.
- Both families support weights 200–900 and use `font-display: swap`. Only the two normal files are preloaded; italic files load when used. Font synthesis is disabled. Local WOFF2 assets and their OFL licenses are recorded in `docs/assets.md`.
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

- Shared CSS layout tokens: `--site-width: 980px`, `--reading-width: 660px`, and `--page-gutter: 32px` (20px at 600px and below). Every page's header and footer use the site width. Home uses the wider layout for its two-column hero; Work, My story, How I work, Writing, and all project detail pages use the centered reading width.
- Page introductions, section-heading groups, FAQs, and closing reading invitations share the 660px reading measure, bounded by the available column. Card headings, descriptions, and thumbnails align within their own grid columns. Project headings, paragraphs, photographs, and video embeds span one column with no nested inset. Story and project photographs retain their full aspect ratio; thumbnail and homepage portrait crops remain deliberate component treatments.
- Desktop reading paragraphs use justified alignment, restrained automatic hyphenation, and a start-aligned final line. This applies to the homepage introduction, page introductions, story chapters, working principles and fit descriptions, project narrative, FAQs, and closing invitations, with a Work-page exception: all Work body copy is left-aligned at every width, with natural wrapping and manual hyphenation. Work sets this once through its page-scoped prose tokens rather than separate paragraph overrides. At 600px and below, the shared prose tokens switch to left alignment, natural wrapping, and manual hyphenation. Short labels, cards, and compact multi-column summaries use natural left alignment at every width.
- Header is not sticky. Navigation is always visible and wraps naturally.
- Sections use quiet 1px rules and generous vertical separation. Work's four-part narrative uses the standard 56px section padding (42px mobile) and one reading column at every width. Its engagement rows use 24px vertical padding and quiet top rules.

## Components

- Primary buttons use link-color fill, paper-color text, a 52px minimum height, and an ink-color hover. The homepage primary action is “Start with my story”, with a quieter Writing shortcut. Reading pages recommend the next page. Work instead shares one contact goal between its introduction and closing: discuss a deployment on LinkedIn, with How I work as the quieter closing continuation. The shared header’s “Stay in touch” points to `writing.html#stay-in-touch`.
- The hero is an editorial two-column composition: personal positioning, value, and discovery links on the left; a 4:5 crop of the owner-supplied ROSCon India 2023 photo, professional identity, and talk link on the right. The desktop figure is capped at 360px wide. Below 800px, the photo becomes an 88–104px-wide portrait beside the name, role, and talk link, between the introduction and discovery links. Source order follows this mobile reading sequence, with one shared photo and caption. The hero ends with discovery links; experience metrics belong on Work, rather than in a separate homepage proof line. Home has no subsequent content sections.
- Work uses one compact NODE Robotics story: the deployment context, the engineering contribution, and the owner-supplied 1,500-robot and 50% cost-reduction results. A brief Robotair lesson and links to My story supply the wider background. The introductory 100,000+ software-delivery statement is broader and keeps its owner-approved wording; do not attribute it exclusively to NODE or invent case-study outcomes.
- Work's three engagement paths are open editorial rows in the reading column. Each starts with a customer need in a 20px sans-serif heading, followed by the formal engagement name and a concise explanation of what the team receives in 16px text. A shared scope note explains the standalone assessment and separately scoped follow-on work. Contact actions belong to the introduction and closing, rather than each option. There is no inquiry form or booking widget.
- Writing ends with two open editorial columns: subscribe on Medium and connect on LinkedIn. Quiet top rules, 16px supporting text, and 52px actions inherit the page’s reading measure; columns stack at 600px. Medium copy explains Follow and email notifications. The footer offers “Start with my story” and both relationship destinations, rather than repeating every page link.
- Seven automatically refreshed Medium previews are directly visible on Writing, with search and topic filters. Do not hide the feed inside a disclosure. Additional LinkedIn articles and the ROSCon talk use disclosures below the feed. Thumbnails remain 150 × 112px desktop and 88px mobile.
- Work has four linear sections: a pilot-to-fleet opening, one real production example, three need-led engagement paths, and an invitation to discuss the next rollout. The main copy targets roughly 450–600 visible words with practical details collapsed. The 660px reading column, left alignment, and serif/sans hierarchy carry the story; DOM and visual order match. Direct hero links replace the former section-navigation row. The former gallery's `#projects` anchor points into My story, where all nine earlier projects remain linked. The wider professional history is reached through those story links.
- Project detail pages share the same tokens, readable text measure, fluid images, and 16:9 video embeds. Their closing primary action returns to the corresponding story chapter; LinkedIn remains a secondary action alongside it.
- Project copy begins with a plain-language introduction above the image, followed by short, project-specific narrative sections in the existing reading column. Technical terms are explained where introduced. Separate design ideas from simulated or measured results. Image descriptions and external resource labels describe what readers will find; each embedded demonstration also has a direct YouTube link.
- One native Practical details disclosure contains the technical scope and three short FAQs. The answers remain in static HTML, available by keyboard and without JavaScript, and exactly match the FAQ structured data.
- The Work FAQ covers scope/fees, taking the work forward, and the Robotair distinction. Each is a labeled article with an 18px question heading, 16px answer text, and a quiet separator in one column. Engagement choice and customer fit belong in the main narrative, rather than being repeated here.
- The disclosure previews its purpose with “Technical scope and working together.” Its full-width native summary has visible View/Hide details text and a plus/minus state indicator. Expanded scope uses four short list items followed by the FAQs. The summary title is 20px; keyboard and no-JavaScript behavior remain native.
- My story at `about.html` uses one shared 660px reading column. The introduction leads into the essay; the Phoenix II photograph follows the rover-team paragraph, and the localization image follows the France/calibration paragraph. Both images retain their aspect ratio, with 32px vertical spacing, 16px contribution-focused captions, and a project link beneath. Autonomous docking is linked within the prose. Earlier rover work and the SAKSHA/ASTRA/DHRUV explorations use small, visible chapter link groups with quiet rules and 44px link targets. All nine projects appear exactly once, with no gallery interrupting the narrative. Preserve the 40–64px headline and first-person story; current-work details remain at capability level.
- My story paragraphs use justified alignment on desktop, with restrained automatic hyphenation and a start-aligned final line. At 600px and below, paragraphs are left-aligned without automatic hyphenation to avoid stretched word spacing. Headings, captions, chapter links, and the personal signoff are left-aligned within the shared column.
- How I work uses the shared 660px reading column, with ten plainly titled principles, a concise definition-list fit summary, and a next step into Writing. It opens with the people-first DevOps philosophy and its connection to becoming a founder. The owner removed the public influences section to keep the page focused on working together; source references remain in development notes. Main navigation includes this destination and wraps below 1000px so the labels stay readable.
- Work links to the current-work chapter in My story for software-factory background. Current employer and actual position are never named; the public story remains at the approved capability level.

## Interaction

- Day is the fallback without JavaScript. Theme preference persists in localStorage when available; storage failures do not disable controls.
- The theme button has a changing action label and pressed state. Its small sun rotation respects reduced motion.
- Article filters use pressed states; search and topic combine; results are announced by a live status. Empty results offer a reset.
- Content and navigation remain usable with JavaScript blocked. No third-party browser requests are needed by the homepage.
- Focus uses a 2px outline with 5px offset. Native keyboard behavior is preserved throughout.
- Only LinkedIn and YouTube destinations open in new tabs with `noopener`. All other web links use the current tab, including Medium, projects, other external sites, and section navigation. The build integration enforces this policy by parsed hostname, never URL substring matching. Do not add Instagram links.

## Assets and content

Use the existing photography and author-owned Medium covers. New raster assets carry source metadata; `docs/assets.md` records provenance. Do not copy the reference site’s illustrations, biography, or signature. Do not reintroduce a résumé PDF; use LinkedIn.
