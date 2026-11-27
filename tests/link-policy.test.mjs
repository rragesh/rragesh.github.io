import { test } from "node:test";
import assert from "node:assert/strict";
import { applyLinkPolicy } from "../src/integrations/link-policy-core.mjs";

test("only LinkedIn and YouTube hosts open safely in a new tab", () => {
  for (const href of ["https://www.linkedin.com/in/ragesh-ramachandran/", "https://linkedin.com/pulse/story", "https://www.youtube.com/watch?v=abc", "https://youtu.be/abc", "//m.youtube.com/watch?v=abc", "https://www.youtube-nocookie.com/embed/abc", "HTTPS://WWW.LINKEDIN.COM/in/example/"]) {
    const result = applyLinkPolicy(`<a href="${href}" target="_self" rel="opener nofollow">Read</a>`);
    assert.equal(result, `<a href="${href}" target="_blank" rel="nofollow noopener">Read</a>`);
  }
});

test("site, Medium, other external links and fragments keep the reader in the same tab", () => {
  for (const href of ["/", "projects/recharge.html", "/about.html#origins", "#main", "https://rragesh.github.io/work.html", "https://rragesh.medium.com/", "https://robotair.io/", "//example.com/"]) {
    const source = `<a href="${href}">Read</a>`;
    assert.equal(applyLinkPolicy(source), source);
    assert.equal(applyLinkPolicy(`<a href="${href}" target="_blank">Read</a>`), source);
  }
});

test("host lookalikes, URL paths and user information cannot opt a link into new tabs", () => {
  for (const href of ["https://linkedin.com.example.org/", "https://notyoutube.com/", "https://linkedin.com@example.org/", "https://example.org/youtube.com", "/youtube.com/watch", "https://example.org/?next=https://linkedin.com", "https://["]) {
    const source = `<a href="${href}">Read</a>`;
    assert.equal(applyLinkPolicy(source), source);
  }
});

test("allowlisted links without rel gain noopener", () => {
  assert.equal(applyLinkPolicy('<a class="x" href="https://youtu.be/abc">Talk</a>'), '<a class="x" href="https://youtu.be/abc" target="_blank" rel="noopener">Talk</a>');
});

test("section navigation, script/style text, comments and non-web schemes are unchanged", () => {
  const source = [
    '<a href="#writing">Writing</a>',
    `<script>const text = '<a href="https://www.youtube.com/watch?v=abc">';</script>`,
    '<style>a::after{content:"<a href=https://linkedin.com>"}</style>',
    '<!-- <a href="https://youtu.be/abc">old</a> -->',
    '<a href="mailto:me@example.com">Mail</a>',
    '<a href="tel:+351000000">Call</a>',
    '<a href="javascript:void(0)">Run</a>',
    "<a>No destination</a>",
    '<a href="">Empty</a>',
  ].join("");
  assert.equal(applyLinkPolicy(source), source);
});

test("is idempotent and preserves surrounding HTML", () => {
  const source = '<p>A &amp; B</p>\r\n<a\n href="https://www.youtube.com/watch?v=abc" >Talk</a><a href="/about.html" target="_blank">Story</a><img src="x.png" alt="">';
  const once = applyLinkPolicy(source);
  assert.equal(applyLinkPolicy(once), once);
  assert.ok(once.startsWith("<p>A &amp; B</p>\r\n"));
  assert.ok(once.endsWith('<a href="/about.html">Story</a><img src="x.png" alt="">'));
  assert.match(once, /target="_blank" rel="noopener">Talk/);
});

test("stale new-tab targets are removed without dropping relationship metadata", () => {
  const source = '<p><a href="work.html" target="_blank" rel="noopener">Get in touch with Ragesh.</a></p>';
  assert.equal(applyLinkPolicy(source), '<p><a href="work.html" rel="noopener">Get in touch with Ragesh.</a></p>');
  assert.equal(applyLinkPolicy('<a href="/" target="named" rel="nofollow">Home</a>'), '<a href="/" rel="nofollow">Home</a>');
});

test("attribute values containing tag-like text do not confuse the rewrite", () => {
  const source = `<a title="a > b rel=x" href='https://example.com/?a=1&amp;b=2' TARGET=_top>Go</a>`;
  assert.equal(applyLinkPolicy(source), `<a title="a > b rel=x" href='https://example.com/?a=1&amp;b=2'>Go</a>`);
});
