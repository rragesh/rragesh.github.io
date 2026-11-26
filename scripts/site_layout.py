"""Shared, static navigation for the portfolio and its project pages."""

from html import escape

LINKEDIN = "https://www.linkedin.com/in/ragesh-ramachandran/"
NAVIGATION = (
    ("home", "index.html", "Home"),
    ("story", "about.html", "My story"),
    ("work", "work.html", "Work"),
    ("writing", "writing.html", "Writing"),
)


def header(active, prefix=""):
    links = []
    for key, route, label in NAVIGATION:
        current = f' aria-current="{"true" if prefix else "page"}"' if key == active else ""
        links.append(f'<a href="{prefix}{route}"{current}>{label}</a>')
    links.append(f'<a href="{LINKEDIN}" aria-label="Get in touch on LinkedIn">Get in touch <span class="arrow diagonal" aria-hidden="true"></span></a>')
    return f'''<header class="site-header container page-header">
      <a class="quiet-name" href="{prefix}index.html" aria-label="Ragesh Ramachandran, home">Ragesh Ramachandran</a>
      <nav class="header-nav" aria-label="Main navigation">{"".join(links)}</nav>
      <button class="theme-toggle" type="button" aria-label="Switch to evening theme" aria-pressed="false" hidden>
        <svg class="sun-icon" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><circle cx="12" cy="12" r="4" /><path d="M12 2v2m0 16v2M2 12h2m16 0h2M5 5l1.5 1.5m11 11L19 19M5 19l1.5-1.5m11-11L19 5" /></svg>
        <span class="theme-label">Evening</span>
      </button>
    </header>'''


def footer(prefix=""):
    links = "".join(f'<a href="{prefix}{route}">{label}</a>' for _, route, label in NAVIGATION)
    return f'''<footer class="site-footer container">
      <p>© <span id="year">2026</span> Ragesh Ramachandran</p>
      <nav aria-label="Footer navigation">{links}<a href="{LINKEDIN}">LinkedIn <span class="arrow diagonal" aria-hidden="true"></span></a></nav>
    </footer>'''


def continue_reading(heading, description, route, label):
    return f'''<section class="section continue-reading">
      <h2>{escape(heading)}</h2>
      <p>{escape(description)}</p>
      <div class="continue-actions"><a class="button primary-button" href="{LINKEDIN}">Get in touch on LinkedIn <span class="arrow diagonal" aria-hidden="true"></span></a>
      <a class="text-link" href="{escape(route, quote=True)}">{escape(label)} <span class="arrow" aria-hidden="true"></span></a></div>
    </section>'''
