import type { APIRoute } from "astro";
import { getCollection } from "astro:content";
import pages from "../data/pages.json";
import projectData from "../data/projects.json";
import { absolute } from "../data/site";

// Canonical, indexable pages only: compatibility redirects and the search-console
// verification file in public/ are deliberately absent. No <lastmod>: the build has
// no trustworthy per-page modification date. scripts/check_site.py verifies this
// list matches the canonical URLs of the built pages exactly.
export const GET: APIRoute = async () => {
  // getCollection() sorts by id; keep the editorial order of src/data/projects.json.
  const order = projectData.map(({ slug }) => slug);
  const projects = (await getCollection("projects")).sort((a, b) => order.indexOf(a.id) - order.indexOf(b.id));
  const paths = [
    ...pages.map(({ file }) => (file === "index.html" ? "/" : `/${file}`)),
    ...projects.map(({ id }) => `/projects/${id}.html`),
  ];
  const urls = paths.map((path) => `  <url><loc>${absolute(path)}</loc></url>`).join("\n");
  const body = `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n${urls}\n</urlset>\n`;
  return new Response(body, { headers: { "Content-Type": "application/xml; charset=utf-8" } });
};
