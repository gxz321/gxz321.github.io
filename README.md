# GXZ — Intelligence, in motion.

An English-language portfolio exploring crowd intelligence, spatial research and embodied AI. Featured work includes CrowdFlow AI, GR00T × Isaac Sim and Sunken Plaza. A medical-robotics project remains a reserved entry until its source code, package and supporting material are supplied.

The site uses pre-rendered HTML, CSS and native JavaScript, with no runtime framework or package-install step. Project content remains readable without JavaScript. `assets/js/motion.js` adds navigation, restrained reveals and a canvas-based motion study. Manrope and Instrument Serif are self-hosted, with their SIL Open Font License files included in `assets/fonts/`.

## Edit, build and preview

1. Edit project content in `content/projects.json` and the profile in `content/profile.json`. The contact destination is GitHub.
2. Add project media to `assets/portfolio/` and update the relevant image paths, alternative text and captions.
3. Generate the static pages:

   ```sh
   python scripts/build.py
   ```

4. Check internal links, media, metadata and page structure:

   ```sh
   python scripts/check_site.py
   ```

5. Start a local preview:

   ```sh
   python -m http.server 8080 --bind 127.0.0.1
   ```

   Open [the local preview](http://127.0.0.1:8080/).

For a separate deployment directory, run `python scripts/build.py --output dist`. The generated `dist/` directory does not need to be committed.

## Publish to GitHub Pages

The existing repository publishes from `master / (root)`. Keep `.nojekyll` in place so GitHub Pages serves the generated files directly. Commit the generated HTML together with its content and source changes to avoid publishing an older build.

The original Jekyll theme sources remain in the repository for reference; the current portfolio uses the generated static pages. The original theme's MIT license is retained.

## Design and interaction

The visual system combines editorial typography, project-led imagery and native motion. Motion is progressive enhancement: navigation and project reading work independently of animation. The site respects `prefers-reduced-motion`; reduced motion, keyboard navigation, touch layouts and the JavaScript-disabled experience should be included in release checks.

The canvas is an illustrative motion study, not a calibrated crowd simulator. Project figures and schematics are identified separately from measured results. See `docs/design-v2.md` for the current design direction and `docs/design.md` for the earlier version.

Release validation and measured local Lighthouse results are recorded in `docs/quality-review.md`.

## Content maintenance

- Keep all public-facing text in English, including metadata, alternative text, video labels and navigation.
- Describe only documented work. Do not infer education, employment, individual team responsibilities or project outcomes.
- Keep the medical-robotics entry pending until reviewable material is available; do not generate technical or clinical claims for it.
- Preserve each project's status and limitations. GR00T has 12 passing CPU protocol and validation tests; real-model inference, GPU training and Isaac Sim closed-loop task evaluation remain unverified.
- Use the source and attribution record in `docs/content-sources.md` when adding or replacing media.
- Keep GitHub as the contact channel. No email address has been introduced.
