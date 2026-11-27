import { defineCollection } from "astro:content";
import { file } from "astro/loaders";
import { z } from "astro/zod";

const text = z.string().trim().min(1);

const projects = defineCollection({
  // The file loader uses each entry's `slug` as its id, so historical slugs (including
  // "Saksha" and "8_leg_dummy") keep their /projects/<id>.html URLs.
  loader: file("src/data/projects.json"),
  schema: ({ image }) =>
    z.strictObject({
      slug: z.string().regex(/^[\w-]+$/),
      storyChapter: z.enum(["origins", "control"]),
      seoTitle: text.optional(),
      summary: text,
      title: text,
      intro: text,
      context: text,
      /** Path relative to src/data/projects.json, e.g. "../assets/optimized/recharge.webp". A missing file fails the build. */
      image: image(),
      imageAlt: text,
      sections: z.array(z.strictObject({ heading: text, paragraphs: z.array(text).min(1) })).min(1),
      /** External URLs, or root-absolute site paths such as "/about.html#origins". */
      links: z.array(z.strictObject({ url: z.string().regex(/^(https?:\/\/|\/)\S/), label: text })),
      /** YouTube video ids. */
      videos: z.array(z.string().regex(/^[\w-]{11}$/)),
    }),
});

export const collections = { projects };
