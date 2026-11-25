#!/usr/bin/env python3
"""Build static project pages from data/projects.json, preserving their public URLs."""

import argparse
from html import escape
import json
from pathlib import Path
from link_policy import open_in_new_tabs

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/projects.json"
LINKEDIN = "https://www.linkedin.com/in/ragesh-ramachandran/"


def render(project):
    title = escape(project["title"])
    seo_title = escape(project.get("seoTitle", project["title"] + " | Ragesh Ramachandran"))
    summary = project.get("summary", project["paragraphs"][0][:180])
    description = escape(summary, quote=True)
    canonical = f"https://rragesh.github.io/projects/{project['slug']}.html"
    image = f"https://rragesh.github.io/img/{project['image']}"
    person = {"@type": "Person", "@id": "https://rragesh.github.io/#ragesh", "name": "Ragesh Ramachandran", "url": "https://rragesh.github.io/"}
    structured = json.dumps({"@context": "https://schema.org", "@graph": [
        {"@type": "WebPage", "@id": canonical + "#webpage", "url": canonical, "name": project["title"], "description": summary, "inLanguage": "en", "mainEntity": {"@id": canonical + "#project"}},
        {"@type": "CreativeWork", "@id": canonical + "#project", "name": project["title"], "description": summary, "url": canonical, "image": image, "author": {"@id": person["@id"]}},
        person
    ]}, ensure_ascii=False).replace("<", "\\u003c")
    paragraphs = "\n".join(f"<p>{escape(p)}</p>" for p in project["paragraphs"])
    links = "\n".join(f'<a class="button" href="{escape(link["url"], quote=True)}">{escape(link["label"])}</a>' for link in project["links"])
    videos = "\n".join(f'<iframe class="project-video" src="https://www.youtube-nocookie.com/embed/{video}" title="{title} — demonstration {i + 1}" loading="lazy" allow="fullscreen; picture-in-picture" allowfullscreen></iframe>' for i, video in enumerate(project["videos"]))
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
  <meta property="og:image:alt" content="{title}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{seo_title}">
  <meta name="twitter:description" content="{description}">
  <meta name="twitter:image" content="{image}">
  <meta name="twitter:image:alt" content="{title}">
  <meta name="theme-color" content="#dceef3">
  <link rel="canonical" href="{canonical}">
  <link rel="icon" href="../img/favicon.svg" type="image/svg+xml">
  <link rel="stylesheet" href="../css/site.css">
  <script src="../js/site.js" defer></script>
  <script type="application/ld+json">{structured}</script>
</head>
<body>
  <a class="skip-link" href="#main">Skip to content</a>
  <header class="site-header container"><a class="wordmark" href="../index.html" aria-label="Ragesh Ramachandran, home">ragesh<span>.</span></a><div class="project-header-links"><a class="text-link" href="../index.html#work">All projects <span class="arrow" aria-hidden="true"></span></a><button class="theme-toggle" type="button" aria-label="Switch to evening theme" aria-pressed="false" hidden><span class="theme-label">Evening</span></button></div></header>
  <main id="main" class="project-page container">
    <h1>{title}</h1>
    <p class="project-context">{escape(project['context'])}</p>
    <img class="project-hero-image" src="../img/{project['image']}" alt="{title}" fetchpriority="high">
    <div class="project-body"><h2>About the project</h2>{paragraphs}<div class="project-links">{links}<a class="text-link" href="{LINKEDIN}">Connect on LinkedIn <span class="arrow diagonal" aria-hidden="true"></span></a></div>{videos}</div>
    <div class="project-return"><a class="text-link" href="../index.html#work">Explore more projects <span class="arrow" aria-hidden="true"></span></a><a class="text-link" href="../index.html#writing">Read my engineering notes <span class="arrow" aria-hidden="true"></span></a></div>
  </main>
  <footer class="site-footer container"><p>© <span id="year">2026</span> Ragesh Ramachandran</p><nav aria-label="Social links"><a href="{LINKEDIN}">LinkedIn</a><a href="https://rragesh.medium.com/">Medium</a><a href="https://github.com/EnigmaRagesh">GitHub</a></nav><p class="template-credit">Original portfolio template by <a href="https://colorlib.com">Colorlib</a>.</p></footer>
</body>
</html>
'''


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    projects = json.loads(DATA.read_text())
    for project in projects:
        (ROOT / f"projects/{project['slug']}.html").write_text(open_in_new_tabs(render(project)))
    print(f"Built {len(projects)} project pages.")
