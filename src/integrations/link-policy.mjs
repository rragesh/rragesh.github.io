/**
 * Placeholder. Will rewrite built HTML after `astro build` so destination links
 * open in new tabs with rel="noopener" (owner preference), matching the old
 * scripts/link_policy.py behavior.
 * @returns {import("astro").AstroIntegration}
 */
export default function linkPolicy() {
  return { name: "link-policy", hooks: {} };
}
