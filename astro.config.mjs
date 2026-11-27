// @ts-check
import { defineConfig } from "astro/config";
import linkPolicy from "./src/integrations/link-policy.mjs";

export default defineConfig({
  site: "https://rragesh.github.io",
  // Emit about.html, projects/astra.html, … so every published URL stays unchanged.
  build: { format: "file" },
  trailingSlash: "never",
  integrations: [linkPolicy()],
});
