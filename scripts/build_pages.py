#!/usr/bin/env python3
"""Build the main pages with shared navigation and page-specific content."""

import argparse
from html import escape
import json
from pathlib import Path
import re

from link_policy import open_in_new_tabs
from site_layout import header, footer, continue_reading

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "data" / "pages"
MANIFEST = ROOT / "data" / "pages.json"
BASE = "https://rragesh.github.io/"


def element(source, tag, attribute, value):
    """Extract a known balanced element for the one-time landing-page migration."""
    start = re.search(rf'<{tag}\b[^>]*\b{attribute}="{re.escape(value)}"[^>]*>', source)
    if not start:
        raise ValueError(f"Missing {tag}[{attribute}={value}]")
    depth = 0
    for token in re.finditer(rf'</?{tag}\b[^>]*>', source[start.start():]):
        depth += -1 if token.group().startswith("</") else 1
        if depth == 0:
            return source[start.start():start.start() + token.end()]
    raise ValueError(f"Unclosed {tag}")


def inner(source):
    return source[source.index(">") + 1:source.rfind("</")].strip()


def import_landing():
    """Move existing content once; never overwrite authored page sources."""
    if MANIFEST.exists() or CONTENT.exists():
        raise SystemExit("Page sources already exist. Edit data/pages/ instead.")
    landing = (ROOT / "index.html").read_text()
    story = (ROOT / "about.html").read_text()
    graph = json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>', landing, re.S)[1])["@graph"]
    person = next(node for node in graph if node.get("@type") == "Person")
    website = next(node for node in graph if node.get("@type") == "WebSite")
    organization = next(node for node in graph if node.get("@type") == "Organization")
    service = next(node for node in graph if node.get("@type") == "Service")
    service["url"] = BASE + "work.html#expertise"
    faq = next(node for node in graph if node.get("@type") == "FAQPage")
    faq["@id"] = faq["url"] = BASE + "work.html#faq"
    articles = [node for node in graph if node.get("@type") == "Article"]
    story_graph = json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>', story, re.S)[1])["@graph"]
    home_graph = [website, {
        "@type": "ProfilePage", "@id": BASE + "#profile", "url": BASE,
        "name": "Ragesh Ramachandran — Robotics engineer and founder",
        "mainEntity": {"@id": BASE + "#ragesh"}, "inLanguage": "en"
    }, person, organization]
    work_graph = [{"@type": "CollectionPage", "@id": BASE + "work.html#page", "url": BASE + "work.html", "name": "Work — Ragesh Ramachandran", "about": {"@id": BASE + "#ragesh"}, "hasPart": {"@id": BASE + "work.html#faq"}}, person, organization, service, faq]
    writing_graph = [{"@type": "CollectionPage", "@id": BASE + "writing.html#page", "url": BASE + "writing.html", "name": "Writing and learning — Ragesh Ramachandran", "about": {"@id": BASE + "#ragesh"}}, person, *articles]
    photo = "img/optimized/ragesh-roscon-2023-social.jpg"
    photo_alt = "Ragesh Ramachandran speaking at ROSCon India 2023"
    pages = [
        {"key": "home", "file": "index.html", "title": "Ragesh Ramachandran | Robotics Engineer & Founder", "description": "Explore the work, writing, and story of Ragesh Ramachandran: robotics engineering, reliable deployment, and the systems behind real-world robot fleets.", "bodyClass": "consulting-page entry-page", "image": photo, "imageAlt": photo_alt, "graph": home_graph},
        {"key": "story", "file": "about.html", "title": "My Story | Ragesh Ramachandran", "description": "From a rover team in Kerala to software infrastructure for defense robotics. Ragesh Ramachandran’s story of engineering, company-building, and deployment at scale.", "bodyClass": "journey-page", "image": "img/optimized/roveruk.webp", "imageAlt": "Phoenix II, the planetary rover built for the 2016 United Kingdom Rover Challenge", "graph": story_graph},
        {"key": "work", "file": "work.html", "title": "Work & Robotics Projects | Ragesh Ramachandran", "description": "Explore Ragesh Ramachandran’s robotics work: production fleet infrastructure, Robotair, industrial integration, and nine hands-on robotics projects.", "bodyClass": "content-page", "image": photo, "imageAlt": photo_alt, "graph": work_graph},
        {"key": "writing", "file": "writing.html", "title": "Writing & Learning | Ragesh Ramachandran", "description": "Read Ragesh Ramachandran’s Medium articles, engineering notes, and ROSCon talk on ROS 2, deployment, containers, and operating robot fleets.", "bodyClass": "content-page", "image": photo, "imageAlt": photo_alt, "graph": writing_graph},
    ]
    home = '''<section class="intro consulting-hero" aria-labelledby="intro-title">
      <div class="hero-content">
        <h1 id="intro-title">I build the systems that make <span>robots dependable.</span></h1>
        <p class="hero-copy">I’m Ragesh, a robotics engineer and founder. My work connects robot software, reliable deployment, and real-world operations—from planetary rovers to industrial and defense robotics.</p>
        <p class="hero-discovery">Explore what I’ve built, how I think, and what I’m learning along the way.</p>
        <div class="hero-actions">
          <a class="button primary-button" href="work.html">Explore my work <span class="arrow" aria-hidden="true"></span></a>
          <a class="text-link" href="about.html">Read my story <span class="arrow" aria-hidden="true"></span></a>
          <a class="text-link" href="writing.html">Read my writing <span class="arrow" aria-hidden="true"></span></a>
        </div>
      </div>
      <figure class="hero-speaker">
        <img src="img/optimized/ragesh-roscon-2023.webp" width="800" height="1000" fetchpriority="high" alt="Ragesh Ramachandran speaking at ROSCon India 2023" />
        <figcaption><strong>Ragesh Ramachandran</strong><span>Robotics engineer · Founder of Robotair</span>
          <a href="https://www.youtube.com/watch?v=p302LwKIhQg">Watch my ROSCon India 2023 talk <span class="arrow diagonal" aria-hidden="true"></span></a>
        </figcaption>
      </figure>
    </section>'''
    work_intro = '''<section class="page-intro" aria-labelledby="work-page-title">
      <h1 id="work-page-title">Work, from prototypes to production.</h1>
      <p>Robot applications, industrial integration, and the infrastructure behind reliable fleets. Explore the work itself, then the ways I help teams move it forward.</p>
      <nav class="chapter-nav" aria-label="Work sections"><a href="#exp">Professional experience</a><a href="#projects">Robotics projects</a><a href="#expertise">Working together</a></nav>
    </section>'''
    projects = '''<section class="section" id="projects" aria-labelledby="projects-title"><div class="section-heading"><div><h2 id="projects-title">Robotics projects, explained.</h2><p>From a robot finding its charger to a rover finding its way across rough ground. Every project starts with the idea, then explains the engineering.</p></div></div><div class="project-grid">\n<!-- PROJECTS:START -->\n<!-- PROJECTS:END -->\n</div></section>'''
    work = work_intro + "\n" + element(landing, "section", "id", "exp") + "\n" + projects
    for section in ("expertise", "process", "faq"):
        work += "\n" + element(landing, "section", "id", section)
    work = work.replace('href="#contact">Discuss an assessment', 'href="https://www.linkedin.com/in/ragesh-ramachandran/">Discuss an assessment on LinkedIn')
    work += "\n" + continue_reading("Let’s talk about what you’re building.", "Whether you’re developing a robotics product, working through a deployment problem, or exploring a collaboration, I’d like to hear from you.", "writing.html", "Explore my engineering notes")
    writing = element(landing, "section", "id", "writing")
    writing = writing.replace('class="section" id="writing"', 'class="writing-page-content" id="writing"')
    writing = writing.replace('<h2 id="writing-title">Latest writing on Medium.</h2>', '<h1 id="writing-title">Writing &amp; learning.</h1>')
    writing = writing.replace('Practical notes on ROS 2, deployment, and the work of keeping robot fleets running.', 'My latest Medium articles on ROS 2, deployment, and the lessons learned from building and operating robots.')
    writing += "\n" + continue_reading("See the work behind the writing.", "Explore the projects and production experience behind these notes—or get in touch if something here connects with what you’re building.", "work.html", "Explore my work")
    story_content = inner(element(story, "main", "id", "main")).replace('href="index.html#expertise"', 'href="work.html#expertise"')
    CONTENT.mkdir(parents=True)
    for key, content in (("home", home), ("story", story_content), ("work", work), ("writing", writing)):
        (CONTENT / f"{key}.html").write_text(content.strip() + "\n")
    MANIFEST.write_text(json.dumps(pages, ensure_ascii=False, indent=2) + "\n")


def project_cards():
    cards = []
    for project in json.loads((ROOT / "data/projects.json").read_text()):
        cards.append(f'''<a class="project-card" href="projects/{escape(project['slug'])}.html">
          <img src="img/{escape(project['image'])}" width="800" height="500" loading="lazy" alt="{escape(project['imageAlt'], quote=True)}" />
          <div><h3>{escape(project['title'])}</h3><p>{escape(project['intro'])}</p><span class="project-meta">{escape(project['context'])}</span></div></a>''')
    return "\n".join(cards)


def render(page, content):
    canonical = BASE if page["file"] == "index.html" else BASE + page["file"]
    graph = json.dumps({"@context": "https://schema.org", "@graph": page["graph"]}, ensure_ascii=False).replace("<", "\\u003c")
    title = escape(page["title"])
    description = escape(page["description"], quote=True)
    image = BASE + page["image"]
    alt = escape(page["imageAlt"], quote=True)
    if page["key"] == "work":
        content = re.sub(r'(?<=<!-- PROJECTS:START -->).*?(?=<!-- PROJECTS:END -->)', "\n" + project_cards() + "\n", content, flags=re.S)
    return open_in_new_tabs(f'''<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>{title}</title>
    <meta name="description" content="{description}" />
    <meta name="author" content="Ragesh Ramachandran" />
    <meta name="robots" content="index, follow, max-image-preview:large" />
    <meta name="google-site-verification" content="K6vXoyADUXSxY4u8uVKJPiKUSXMnxKISFHwJyM7cCKU" />
    <meta name="theme-color" content="#dceef3" />
    <link rel="canonical" href="{canonical}" />
    <link rel="icon" href="img/favicon.svg" type="image/svg+xml" />
    <link rel="preload" href="fonts/source-serif-4-latin-normal.woff2" as="font" type="font/woff2" crossorigin />
    <link rel="preload" href="fonts/source-sans-3-latin-normal.woff2" as="font" type="font/woff2" crossorigin />
    <link rel="stylesheet" href="css/site.css" />
    <link rel="alternate" type="application/rss+xml" title="Ragesh on Medium" href="https://rragesh.medium.com/feed" />
    <meta property="og:type" content="website" />
    <meta property="og:site_name" content="Ragesh Ramachandran" />
    <meta property="og:title" content="{title}" />
    <meta property="og:description" content="{description}" />
    <meta property="og:url" content="{canonical}" />
    <meta property="og:image" content="{image}" />
    <meta property="og:image:alt" content="{alt}" />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:title" content="{title}" />
    <meta name="twitter:description" content="{description}" />
    <meta name="twitter:image" content="{image}" />
    <meta name="twitter:image:alt" content="{alt}" />
    <script type="application/ld+json">{graph}</script>
    <script src="js/site.js" defer></script>
  </head>
  <body class="{page['bodyClass']}">
    <a class="skip-link" href="#main">Skip to content</a>
    {header(page['key'])}
    <main id="main" class="container">
      {content}
    </main>
    {footer()}
  </body>
</html>
''')


def build(only=None, check=False):
    pages = json.loads(MANIFEST.read_text())
    stale = []
    for page in pages:
        if only and page["key"] != only:
            continue
        content = (CONTENT / f"{page['key']}.html").read_text()
        output = render(page, content)
        target = ROOT / page["file"]
        if check:
            if not target.exists() or target.read_text() != output:
                stale.append(page["file"])
        else:
            target.write_text(output)
    if stale:
        raise SystemExit("Regenerate main pages with scripts/build_pages.py: " + ", ".join(stale))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--import-landing", action="store_true")
    parser.add_argument("--only", choices=("home", "story", "work", "writing", "approach"))
    parser.add_argument("--check", action="store_true", help="Fail when generated pages differ from their sources")
    args = parser.parse_args()
    if args.import_landing:
        import_landing()
    build(args.only, args.check)
    print("Checked main pages." if args.check else "Built main pages with shared navigation.")
