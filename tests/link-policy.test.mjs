import { test } from "node:test";
import assert from "node:assert/strict";
import { openInNewTabs } from "../src/integrations/link-policy-core.mjs";

test("external and site links open safely in a new tab", () => {
  for (const href of ["https://robotair.io/", "projects/recharge.html", "/projects/recharge.html", "//example.com/"]) {
    const result = openInNewTabs(`<a href="${href}" target="_self" rel="opener nofollow">Read</a>`);
    assert.equal(result, `<a href="${href}" target="_blank" rel="nofollow noopener">Read</a>`);
  }
});

test("links without rel gain noopener", () => {
  assert.equal(openInNewTabs('<a class="x" href="/about.html#origins">Story</a>'), '<a class="x" href="/about.html#origins" target="_blank" rel="noopener">Story</a>');
});

test("section navigation, script/style text, comments and non-web schemes are unchanged", () => {
  const source = [
    '<a href="#writing">Writing</a>',
    `<script>const text = '<a href="https://example.com">';</script>`,
    '<style>a[href="https://example.com"]::after{content:"<a href=x>"}</style>',
    '<!-- <a href="https://example.com">old</a> -->',
    '<a href="mailto:me@example.com">Mail</a>',
    '<a href="tel:+351000000">Call</a>',
    '<a href="javascript:void(0)">Run</a>',
    "<a>No destination</a>",
    '<a href="">Empty</a>',
  ].join("");
  assert.equal(openInNewTabs(source), source);
});

test("is idempotent and preserves surrounding HTML", () => {
  const source = '<p>A &amp; B</p>\r\n<a\n href="https://robotair.io/" >Robotair</a><img src="x.png" alt="">';
  const once = openInNewTabs(source);
  assert.equal(openInNewTabs(once), once);
  assert.ok(once.startsWith("<p>A &amp; B</p>\r\n"));
  assert.ok(once.endsWith('>Robotair</a><img src="x.png" alt="">'));
  assert.match(once, /target="_blank" rel="noopener">Robotair/);
});

test("legacy redirect fallback links are already compliant", () => {
  const source = '<p><a href="work.html" target="_blank" rel="noopener">Get in touch with Ragesh.</a></p>';
  assert.equal(openInNewTabs(source), source);
});

test("attribute values containing tag-like text do not confuse the rewrite", () => {
  const source = `<a title="a > b rel=x" href='https://example.com/?a=1&amp;b=2' TARGET=_top>Go</a>`;
  assert.equal(openInNewTabs(source), `<a title="a > b rel=x" href='https://example.com/?a=1&amp;b=2' target="_blank" rel="noopener">Go</a>`);
});
