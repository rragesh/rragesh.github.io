import pages from "./pages.json";
import type { NavKey } from "./site";

export interface PageMeta {
  key: NavKey;
  /** Historical output file, e.g. "about.html". */
  file: string;
  title: string;
  description: string;
  bodyClass: string;
  /** Social image path relative to the site root, e.g. "img/optimized/…". */
  image: string;
  imageAlt: string;
  /** JSON-LD @graph nodes. */
  graph: unknown[];
}

/** Metadata (title, description, social image, JSON-LD) for a main page. */
export function pageMeta(key: NavKey): PageMeta & { path: string } {
  const page = (pages as PageMeta[]).find((entry) => entry.key === key);
  if (!page) throw new Error(`Missing page metadata for ${key}`);
  return { ...page, path: page.file === "index.html" ? "/" : `/${page.file}`, image: `/${page.image}` };
}
