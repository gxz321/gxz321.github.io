# English portfolio release review

Reviewed on 20 October 2026. This release uses an editorial design system, real project evidence, native interaction, and fully English public copy. Four generated concept screens preceded implementation. Actual desktop and mobile captures were compared with those references, followed by two independent review rounds and corrections.

## Corrections made during review

- Removed a large-title collision with the flow field and aligned the two secondary studies to equal media widths and text baselines.
- Replaced generic preview text with concrete project descriptions. Increased mobile method text and corrected spaces around responsive line breaks.
- Added full-size evidence links that follow the selected artifact. Views switch image, description, caption, and pressed state together, including when clicked rapidly.
- Rebuilt the crowd figures from the named raw recording with equal coordinate scales and reproducible sampling. Relative observation frequency is explicitly distinguished from physical density and safety claims.
- Removed accessible-name mismatches, made main content programmatically focusable, and checked menu focus restoration.
- Set the enhancement class before first paint to prevent mobile navigation layout shift. Switched to WOFF2 fonts and lossless WebP images, retaining licenses and source artifacts.
- Added a 1200 × 630 social preview and checked its local target alongside ordinary routes and evidence paths.

## Functional and visual coverage

Chrome 155 with Playwright exercised five routes at widths 320, 390, 620, 768, 1024, and 1440 pixels. All 30 route/width combinations passed horizontal-overflow and English-content checks. Browser logs and local resource responses showed no errors. Desktop and mobile captures cover the complete homepage, project previews, approach, about, case headers, evidence controls, and expanded workflow details.

Verified behavior: native flow animation, pause/resume, offscreen suspension, project navigation, mobile menu, Escape and focus return, evidence switches and full-size links, workflow disclosures, valid ZIP download, and the 30.07-second plaza video. Reduced-motion mode starts with a static field and visible content. Navigation and research evidence remain accessible with JavaScript disabled.

The in-app browser was attempted first; its tab handles became unavailable during viewport changes. Regular Playwright with the installed Chrome provided stable, reproducible viewport tests instead.

The Python site checker passes for all five generated pages, including route and anchor targets, assets, social image, evidence paths, metadata, language, heading count, alternative text, and external-link relationships. Generated pages are checked again by GitHub Actions.

## Accessibility

axe-core 4.14.0 reported zero violations across five routes at both 1440 and 390 pixels (10 states). Manual checks passed for skip-link focus, mobile-menu keyboard use, Escape, reduced motion, and the JavaScript-disabled experience. The source film is silent; its text description and separate download link were manually reviewed. A card separator caused an automated background-color uncertainty; direct verification confirmed that it does not underlie the text and the ink/paper contrast is 15.78:1.

## Local Lighthouse results

Lighthouse 13.5.0, Node 24, Chrome 155, against the local production build. Mobile used the standard simulated mobile/4G/CPU slowdown profile. These are laboratory results, not live-site field measurements.

| Mode | Performance | Accessibility | Best practices | SEO | LCP | CLS | TBT |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Mobile | 99 | 100 | 100 | 100 | 2.106 s | 0.000355 | 41 ms |
| Desktop | 100 | 100 | 100 | 100 | 444 ms | 0.000797 | 0 ms |

Mobile performance improved from 91 to 99 during review; LCP improved from 3.397 to 2.106 seconds. Neither final run reported a warning. Raw reports and screenshot evidence are retained with the local handoff materials.

## Content limits

No education, employment, individual team responsibility, award, or measured project success is invented. Medical robotics remains a forthcoming entry. GR00T has seven passing CPU protocol tests; actual learned-policy inference, GPU training, and Isaac Sim closed-loop task evaluation still require demonstrations, a checkpoint, and a compatible environment. The hero flow field and robot schematic are labeled illustrations.

This review uses design, usability, creativity, and content as separate quality concerns, consistent with [Awwwards' published evaluation criteria](https://www.awwwards.com/about-evaluation/). Award selection belongs to its jury; the portfolio does not claim an award or guarantee one.
