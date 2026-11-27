# Asset sources

Project photographs were already present at repository revision `e60b4e5`. The owner subsequently supplied the ROSCon India 2023 speaking photograph to replace the old portrait. No generated imagery or stock photography was added.

| Shipping asset | Source | Treatment |
| --- | --- | --- |
| `img/optimized/roveruk.webp` | `img/work/roveruk.jpg` | WebP conversion |
| `img/optimized/recharge.webp` | `img/work/recharge.jpeg` | Resized, WebP conversion |
| `img/optimized/localize.webp` | `img/work/localize.png` | Resized, WebP conversion |
| `img/optimized/saksha.webp` | `img/work/saksha.jpg` | Resized, WebP conversion |
| `img/optimized/astra.webp` | `img/work/astra.jpg` | Resized, WebP conversion |
| `img/optimized/ragesh-roscon-2023.webp` | Owner-supplied 2000 × 1333 photograph of Ragesh speaking at ROSCon India 2023; related recording: `https://www.youtube.com/watch?v=p302LwKIhQg` | Speaker-centered crop, 800 × 1000 WebP; no generative edits |
| `img/optimized/ragesh-roscon-2023-social.jpg` | Same owner-supplied ROSCon India 2023 photograph | 1200 × 630 social crop, JPEG; no generative edits |
| `src/assets/medium/*.webp` | Individual `image` URLs in `src/data/medium-posts.json` | Bounded to 800 × 600, WebP conversion |
| `fonts/source-serif-4-latin-{normal,italic}.woff2` | `@fontsource-variable/source-serif-4@5.3.1`, files `source-serif-4-latin-wght-{normal,italic}.woff2`, via `https://cdn.jsdelivr.net/npm/` | Self-hosted Latin variable faces, weights 200–900; `fonts/SourceSerif4-OFL.txt` |
| `fonts/source-sans-3-latin-{normal,italic}.woff2` | `@fontsource-variable/source-sans-3@5.3.1`, files `source-sans-3-latin-wght-{normal,italic}.woff2`, via `https://cdn.jsdelivr.net/npm/` | Self-hosted Latin variable faces, weights 200–900; `fonts/SourceSans3-OFL.txt` |
| `img/favicon.svg` | Authored monogram | SVG |

New photographic files include source information in their EXIF image-description metadata. After the Astro migration, images optimized at build time live in `src/assets/` (`img/work/*` → `src/assets/work/`, `img/optimized/*` → `src/assets/optimized/`) and are served as responsive AVIF/WebP; files that must keep stable public URLs (favicon, social previews, the ROSCon portrait, PDFs, fonts) live in `public/`. Source photographs listed above are intentionally retained for future crops and conversions; unreferenced template artwork, skill icons, recommendation portraits, and unused project images have been removed.
