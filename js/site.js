"use strict";

// Keep existing homepage bookmarks useful after moving content to dedicated pages.
if (document.body.classList.contains("entry-page")) {
  const legacyRoutes = {
    "#about": "about.html",
    "#background": "about.html",
    "#exp": "work.html#exp",
    "#work": "about.html#origins",
    "#expertise": "work.html#expertise",
    "#process": "work.html#process",
    "#faq": "work.html#faq",
    "#writing": "writing.html",
    "#articles": "writing.html#articles",
    "#talks": "writing.html#talks",
    "#contact": "https://www.linkedin.com/in/ragesh-ramachandran/",
  };
  function followLegacyLink() {
    const destination = legacyRoutes[window.location.hash];
    if (destination) window.location.replace(new URL(destination, document.baseURI).href);
  }
  followLegacyLink();
  window.addEventListener("hashchange", followLegacyLink);
}

const themeToggle = document.querySelector(".theme-toggle");
let theme = "day";
try {
  if (localStorage.getItem("ragesh-theme") === "evening") theme = "evening";
} catch {
  // Storage may be disabled; theme switching still works for this page.
}
function applyTheme() {
  document.documentElement.dataset.theme = theme;
  const evening = theme === "evening";
  document
    .querySelector('meta[name="theme-color"]')
    ?.setAttribute("content", evening ? "#294d60" : "#dceef3");
  if (themeToggle) {
    themeToggle.setAttribute("aria-pressed", String(evening));
    themeToggle.setAttribute(
      "aria-label",
      evening ? "Switch to daytime theme" : "Switch to evening theme",
    );
    themeToggle.querySelector(".theme-label").textContent = evening
      ? "Daytime"
      : "Evening";
  }
}
applyTheme();
if (themeToggle) {
  themeToggle.hidden = false;
  themeToggle.addEventListener("click", () => {
    theme = theme === "evening" ? "day" : "evening";
    applyTheme();
    try {
      localStorage.setItem("ragesh-theme", theme);
    } catch {
      /* Optional persistence. */
    }
  });
}

const articles = [...document.querySelectorAll(".article-card")];
const search = document.querySelector("#article-search");
const filters = document.querySelector(".topic-filters");
if (articles.length && search && filters) {
  let topic = "All";
  const topicCounts = new Map();
  articles.forEach((article) => {
    JSON.parse(article.dataset.topics).forEach((tag) => {
      topicCounts.set(tag, (topicCounts.get(tag) || 0) + 1);
    });
  });
  const topics = [
    "All",
    ...[...topicCounts]
      .sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]))
      .slice(0, 4)
      .map(([tag]) => tag),
  ];
  function updateArticles() {
    const query = search.value.trim().toLocaleLowerCase();
    let visible = 0;
    articles.forEach((article) => {
      const matchesTopic =
        topic === "All" || JSON.parse(article.dataset.topics).includes(topic);
      article.hidden = !(
        matchesTopic && article.textContent.toLocaleLowerCase().includes(query)
      );
      if (!article.hidden) visible += 1;
    });
    filters.querySelectorAll("button").forEach((button) => {
      button.setAttribute(
        "aria-pressed",
        String(button.dataset.topic === topic),
      );
    });
    document.querySelector("#no-articles").hidden = visible !== 0;
    document.querySelector("#article-count").textContent =
      `${visible} ${visible === 1 ? "story" : "stories"}${topic === "All" ? "" : ` about ${topic}`}`;
  }
  topics.forEach((name) => {
    const button = document.createElement("button");
    button.type = "button";
    button.className = "filter";
    button.dataset.topic = name;
    button.textContent = name === "All" ? "All stories" : name;
    button.addEventListener("click", () => {
      topic = name;
      updateArticles();
    });
    filters.append(button);
  });
  search.addEventListener("input", updateArticles);
  document.querySelector("#reset-articles").addEventListener("click", () => {
    topic = "All";
    search.value = "";
    updateArticles();
    search.focus();
  });
  document.querySelector(".writing-tools").hidden = false;
  document.querySelector("#article-count").hidden = false;
  updateArticles();
}

const year = document.querySelector("#year");
if (year) year.textContent = new Date().getFullYear();
