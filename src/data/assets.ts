import type { ImageMetadata } from "astro";

const images = import.meta.glob<{ default: ImageMetadata }>("/src/assets/**/*.{webp,jpg,jpeg,png,JPG}", { eager: true });

/** Resolve an image under src/assets/ by relative path, e.g. "optimized/recharge.webp". */
export function asset(path: string): ImageMetadata {
  const image = images[`/src/assets/${path}`];
  if (!image) throw new Error(`Missing image asset: src/assets/${path}`);
  return image.default;
}
