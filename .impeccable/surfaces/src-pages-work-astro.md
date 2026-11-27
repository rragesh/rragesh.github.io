---
version: 1
slug: "src-pages-work-astro"
primary_target: "src/pages/work.astro"
related_targets: []
---

# Customer-facing Work page

Mode: Persuade. Surface: `src/pages/work.astro`. Audience: robotics founders, CTOs, and engineering teams in the EU and US moving from pilots to production fleets. Primary action: discuss a deployment on LinkedIn. The owner approved applying the positioning in `docs/value-proposition.md` and opening a PR.

## Direction contract

THESIS: Make robotics deployment expertise concrete through the customer's operational problem, the result of each engagement, and attributed production experience. The visitor should understand what their team receives before reading the detailed career history.

OWN-WORLD: Inherit the established Source Serif 4 / Source Sans 3 editorial identity, sky-to-paper day palette, deep-blue evening palette, blue actions, quiet rules, and 980px shell. A busy engineering leader can scan the page in daylight or evening; use the existing theme switch and readable contrast in both.

STORY: Recognize the difficulty of manual releases, unclear rollout health, recovery, and competing priorities. Compare assessment, implementation, and fractional leadership through concrete outcomes. See the existing attributed evidence, understand scope and handover, then describe a deployment on LinkedIn. Continue to How I work through the existing reading invitation.

FIRST VIEWPORT: Within the existing introduction, lead with “Robot deployments your team can depend on.” and the approved one-paragraph value proposition. A prominent “Discuss your deployment” action leads to the contact section; a quieter link leads to the engagement comparison. Place the attributed 1,500-robot NODE experience immediately below the actions. Keep the introduction at the existing reading measure and the local navigation visible. On phones, the headline, short explanation, and primary action precede proof and section navigation.

FORM: Code-led extension of the existing Work surface; seed: none (pinned), “Lets apply that to my website and open a new PR”. Add open problem-to-outcome definition-list rows, strengthen the existing three-column engagement comparison, and add a specific LinkedIn invitation. Retain the native technical disclosure, expanded FAQ, and story bridge. No new interaction beyond working anchors; keyboard, no-JavaScript, and theme behavior remain native to the site.

FINISH: unreviewed and undocumented is unfinished; this build ends with the finish review, the verdict, DESIGN.md, and every shipping raster carrying its provenance

## Content constraints

Use the already supplied historical results and their attribution. Describe deliverables and collaboration goals, not guaranteed improvements, new customer findings, fixed fees, turnaround promises, or certifications. Assessment is useful on its own; direct implementation is possible when the scope is already clear. Keep visible FAQ answers and JSON-LD synchronized. This is a local extension, so the existing global design system and approved personal homepage remain the visual authority. No new raster assets are required.

## Finish record

The independent rendered-page review returned **ship**, with no material fixes, on 2026-11-27. Desktop (1440px), phone (390px), and the actual Pane viewport (785px) were inspected, with day/evening, engagement, contact, and expanded-disclosure evidence. The extension follows the existing `DESIGN.md` fonts, tokens, reading measure, comparison treatment, and native interaction patterns; the global design system was preserved. Automated site checks, keyboard/no-JavaScript checks, and responsive overflow checks passed. No new raster assets were introduced.

## Reading alignment

In the owner's follow-up review, the mixture of justified and left-aligned paragraphs felt inconsistent. The approved refinement left-aligns all Work-page body text at every viewport, with natural word spacing, `pretty` wrapping, and manual hyphenation. Set this once through the `.work-page` prose tokens; the introduction, proof, FAQs, and closing invitation follow the same rule.

Verified the rendered alignment of all 56 paragraph, definition, and list blocks at 1440px, 751px, and 390px in both themes, with no horizontal overflow. The local review preview was refreshed and confirmed to contain no justified body-text blocks. The build, 14-page site validation, and typography detector passed.
