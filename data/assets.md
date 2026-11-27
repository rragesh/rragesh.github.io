# Asset sources

Project photographs were already present at repository revision `e60b4e5`. The owner subsequently supplied the ROSCon India 2023 speaking photograph to replace the old portrait. No generated imagery or stock photography was added.

| Asset | Source | Treatment |
| --- | --- | --- |
| `src/assets/work/*` | Original project photographs (see `data/project-copy-sources.md`) | Unmodified sources; Astro generates responsive AVIF/WebP and 1200px social JPEGs at build time |
| `src/assets/ragesh-roscon-2023.webp` | Owner-supplied 2000 × 1333 photograph of Ragesh speaking at ROSCon India 2023; related recording: `https://www.youtube.com/watch?v=p302LwKIhQg` | Speaker-centered crop, 800 × 1000 WebP; no generative edits. Homepage portrait, resized responsively by Astro |
| `public/img/optimized/ragesh-roscon-2023.webp` | Same crop | Stable public URL used as the Person `image` in structured data |
| `public/img/optimized/ragesh-roscon-2023-social.jpg` | Same owner-supplied ROSCon India 2023 photograph | 1200 × 630 social crop, JPEG; no generative edits |
| `public/img/optimized/roveruk.webp` | `src/assets/work/roveruk.jpg` | WebP conversion; stable social-preview URL for My story |
| `src/assets/medium/*.webp` | Individual `image` URLs in `src/data/medium-posts.json` | Bounded to 800 × 600, WebP conversion, by `scripts/update-medium.mjs` |
| `public/img/exp/*.pdf` | Project publications | Unmodified |
| `public/fonts/source-serif-4-latin-{normal,italic}.woff2` | `@fontsource-variable/source-serif-4@5.3.1`, files `source-serif-4-latin-wght-{normal,italic}.woff2`, via `https://cdn.jsdelivr.net/npm/` | Self-hosted Latin variable faces, weights 200–900; `public/fonts/SourceSerif4-OFL.txt` |
| `public/fonts/source-sans-3-latin-{normal,italic}.woff2` | `@fontsource-variable/source-sans-3@5.3.1`, files `source-sans-3-latin-wght-{normal,italic}.woff2`, via `https://cdn.jsdelivr.net/npm/` | Self-hosted Latin variable faces, weights 200–900; `public/fonts/SourceSans3-OFL.txt` |
| `public/img/favicon.svg` | Authored monogram | SVG |

New photographic files include source information in their EXIF image-description metadata. Unreferenced template artwork, skill icons, recommendation portraits, and unused project images have been removed.
