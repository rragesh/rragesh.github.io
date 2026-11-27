import { readdir, readFile, writeFile } from "node:fs/promises";
import { fileURLToPath } from "node:url";
import path from "node:path";
import { openInNewTabs } from "./link-policy-core.mjs";

async function* htmlFiles(directory) {
  for (const entry of await readdir(directory, { withFileTypes: true })) {
    const target = path.join(directory, entry.name);
    if (entry.isDirectory()) yield* htmlFiles(target);
    else if (entry.isFile() && entry.name.endsWith(".html")) yield target;
  }
}

/**
 * Rewrites built HTML after `astro build` so destination links open in new tabs with
 * rel="noopener" (owner preference). See ./link-policy-core.mjs for the exact rules.
 * @returns {import("astro").AstroIntegration}
 */
export default function linkPolicy() {
  return {
    name: "link-policy",
    hooks: {
      "astro:build:done": async ({ dir, logger }) => {
        const root = fileURLToPath(dir);
        let checked = 0;
        let updated = 0;
        for await (const file of htmlFiles(root)) {
          checked++;
          const source = await readFile(file, "utf8");
          const result = openInNewTabs(source);
          if (result !== source) {
            await writeFile(file, result);
            updated++;
          }
        }
        logger.info(`Applied new-tab link policy to ${updated} of ${checked} HTML files.`);
      },
    },
  };
}
