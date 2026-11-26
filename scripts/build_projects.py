#!/usr/bin/env python3
"""Build static project pages from data/projects.json, preserving their public URLs."""

import argparse
from html import escape
import json
from pathlib import Path
from link_policy import open_in_new_tabs
from site_layout import header, footer, continue_reading

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/projects.json"
LINKEDIN = "https://www.linkedin.com/in/ragesh-ramachandran/"


def render(project):
    title = escape(project["title"])
    seo_title = escape(project.get("seoTitle", project["title"] + " | Ragesh Ramachandran"))
    summary = project.get("summary") or project.get("intro") or " ".join(project.get("paragraphs", []))[:180]
    description = escape(summary, quote=True)
    image_alt = escape(project.get("imageAlt", project["title"]), quote=True)
    canonical = f"https://rragesh.github.io/projects/{project['slug']}.html"
    image = f"https://rragesh.github.io/img/{project['image']}"
    person = {"@type": "Person", "@id": "https://rragesh.github.io/#ragesh", "name": "Ragesh Ramachandran", "url": "https://rragesh.github.io/"}
    structured = json.dumps({"@context": "https://schema.org", "@graph": [
        {"@type": "WebPage", "@id": canonical + "#webpage", "url": canonical, "name": project["title"], "description": summary, "inLanguage": "en", "mainEntity": {"@id": canonical + "#project"}},
        {"@type": "CreativeWork", "@id": canonical + "#project", "name": project["title"], "description": summary, "url": canonical, "image": image, "author": {"@id": person["@id"]}},
        person
    ]}, ensure_ascii=False).replace("<", "\\u003c")
    intro = f'<p class="project-lead">{escape(project["intro"])}</p>' if project.get("intro") else ""
    sections = project.get("sections") or [{"heading": "About the project", "paragraphs": project.get("paragraphs", [])}]
    body = "\n".join(
        f'<section class="project-section"><h2>{escape(section["heading"])}</h2>'
        + "".join(f"<p>{escape(p)}</p>" for p in section["paragraphs"])
        + "</section>"
        for section in sections
    )
    links = "\n".join(f'<a class="button" href="{escape(link["url"], quote=True)}">{escape(link["label"])}</a>' for link in project["links"])
    videos = "\n".join(
        f'<iframe class="project-video" src="https://www.youtube-nocookie.com/embed/{video}" title="{title} — demonstration {i + 1}" loading="lazy" allow="fullscreen; picture-in-picture" allowfullscreen></iframe>'
        f'<a class="text-link" href="https://www.youtube.com/watch?v={video}">Watch demonstration {i + 1} on YouTube <span class="arrow diagonal" aria-hidden="true"></span></a>'
        for i, video in enumerate(project["videos"])
    )
    if videos:
        videos = f'<section class="project-section"><h2>Watch the project in motion</h2>{videos}</section>'
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{seo_title}</title>
  <meta name="description" content="{description}">
  <meta name="author" content="Ragesh Ramachandran">
  <meta name="robots" content="index, follow, max-image-preview:large">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Ragesh Ramachandran">
  <meta property="og:title" content="{seo_title}">
  <meta property="og:description" content="{description}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:image" content="{image}">
  <meta property="og:image:alt" content="{image_alt}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{seo_title}">
  <meta name="twitter:description" content="{description}">
  <meta name="twitter:image" content="{image}">
  <meta name="twitter:image:alt" content="{image_alt}">
  <meta name="theme-color" content="#dceef3">
  <link rel="canonical" href="{canonical}">
  <link rel="icon" href="../img/favicon.svg" type="image/svg+xml">
  <link rel="preload" href="../fonts/source-serif-4-latin-normal.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="../fonts/source-sans-3-latin-normal.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="../css/site.css">
  <script src="../js/site.js" defer></script>
  <script type="application/ld+json">{structured}</script>
</head>
<body>
  <a class="skip-link" href="#main">Skip to content</a>
  {header("work", "../")}
  <main id="main" class="project-page container">
    <nav class="breadcrumbs" aria-label="Breadcrumb"><a href="../index.html">Home</a><span aria-hidden="true">/</span><a href="../work.html#projects">Work</a></nav>
    <h1>{title}</h1>
    <p class="project-context">{escape(project['context'])}</p>
    {intro}
    <img class="project-hero-image" src="../img/{project['image']}" alt="{image_alt}" fetchpriority="high">
    <div class="project-body">{body}<div class="project-links">{links}</div>{videos}</div>
    {continue_reading("Working on something similar?", "If this project connects with a problem or idea you’re exploring, I’d enjoy comparing notes.", "../work.html#projects", "Explore more projects")}
  </main>
  {footer("../")}
</body>
</html>
'''


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Fail when generated project pages are stale")
    args = parser.parse_args()
    projects = json.loads(DATA.read_text())
    stale = []
    for project in projects:
        target = ROOT / f"projects/{project['slug']}.html"
        output = open_in_new_tabs(render(project))
        if args.check:
            if not target.exists() or target.read_text() != output:
                stale.append(project["slug"])
        else:
            target.write_text(output)
    if stale:
        raise SystemExit("Regenerate project pages with scripts/build_projects.py: " + ", ".join(stale))
    print(f"{'Checked' if args.check else 'Built'} {len(projects)} project pages.")
