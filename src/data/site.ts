export const BASE = "https://rragesh.github.io/";
export const LINKEDIN = "https://www.linkedin.com/in/ragesh-ramachandran/";
export const PERSON_ID = `${BASE}#ragesh`;
export const GOOGLE_SITE_VERIFICATION = "K6vXoyADUXSxY4u8uVKJPiKUSXMnxKISFHwJyM7cCKU";

export type NavKey = "home" | "story" | "work" | "writing" | "approach";

export const NAVIGATION: ReadonlyArray<{ key: NavKey; href: string; label: string }> = [
  { key: "home", href: "/", label: "Home" },
  { key: "story", href: "/about.html", label: "My story" },
  { key: "work", href: "/work.html", label: "Work" },
  { key: "writing", href: "/writing.html", label: "Writing" },
  { key: "approach", href: "/how-i-work.html", label: "How I work" },
];

/** Absolute URL for a site path: "/" → BASE, "/about.html" → BASE + "about.html". */
export function absolute(path: string): string {
  return new URL(path, BASE).href;
}
