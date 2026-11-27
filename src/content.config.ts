import { defineCollection } from "astro:content";
import { file } from "astro/loaders";
import { z } from "astro/zod";

const projects = defineCollection({
  // Entries keep their historical slugs (including "Saksha" and "8_leg_dummy") as ids,
  // so /projects/<id>.html URLs never change.
  loader: file("src/data/projects.json", {
    parser: (text) => (JSON.parse(text) as Array<Record<string, unknown>>).map((project) => ({ id: project.slug, ...project })),
  }),
  schema: z.object({
    slug: z.string(),
    storyChapter: z.enum(["origins", "control"]),
    seoTitle: z.string(),
    summary: z.string(),
    title: z.string(),
    intro: z.string(),
    context: z.string(),
    /** Path relative to src/assets/, e.g. "optimized/recharge.webp". */
    image: z.string(),
    imageAlt: z.string().min(1),
    sections: z.array(z.object({ heading: z.string(), paragraphs: z.array(z.string()).min(1) })).min(1),
    links: z.array(z.object({ url: z.string(), label: z.string() })),
    /** YouTube video ids. */
    videos: z.array(z.string()),
  }),
});

export const collections = { projects };
