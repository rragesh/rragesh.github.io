/**
 * Owner preference: every destination link opens in a new tab with rel="noopener".
 * Same-page fragments ("#..."), non-web schemes (mailto:, tel:, javascript:, …) and
 * markup inside <script>/<style>/comments are left untouched. The transform only
 * rewrites matching <a> start tags, so the rest of the document is preserved byte for byte,
 * and running it twice gives the same result.
 */

const RAW_TEXT = new Set(["script", "style"]);
const NAME = /[^\s/>"'=]/;

const ENTITIES = { amp: "&", lt: "<", gt: ">", quot: '"', apos: "'" };

/** Minimal HTML attribute unescaping (enough to read href/rel the way a browser would). */
function unescape(value) {
  return value.replace(/&(#x[0-9a-f]+|#\d+|[a-z]+);/gi, (entity, body) => {
    if (body[0] === "#") {
      const code = body[1] === "x" || body[1] === "X" ? parseInt(body.slice(2), 16) : parseInt(body.slice(1), 10);
      return Number.isFinite(code) && code <= 0x10ffff ? String.fromCodePoint(code) : entity;
    }
    return ENTITIES[body.toLowerCase()] ?? entity;
  });
}

/**
 * Parse one start tag beginning at `start` (source[start] === "<").
 * @returns {{ name: string, end: number, close: number, attrs: Array<{ name: string, value: string | null, start: number, end: number }> } | null}
 *   `end` is the index just past ">", `close` the index of the "/>" or ">" terminator.
 */
function parseStartTag(source, start) {
  let i = start + 1;
  const nameMatch = /^[a-zA-Z][^\s/>]*/.exec(source.slice(i, i + 64));
  if (!nameMatch) return null;
  const name = nameMatch[0].toLowerCase();
  i += nameMatch[0].length;
  const attrs = [];
  while (i < source.length) {
    const attrStart = i;
    while (i < source.length && /\s/.test(source[i])) i++;
    if (i >= source.length) return null;
    if (source[i] === ">") return { name, attrs, close: i, end: i + 1 };
    if (source[i] === "/" && source[i + 1] === ">") return { name, attrs, close: i, end: i + 2 };
    if (source[i] === "/") {
      i++;
      continue;
    }
    let nameEnd = i + 1;
    while (nameEnd < source.length && NAME.test(source[nameEnd])) nameEnd++;
    const attrName = source.slice(i, nameEnd).toLowerCase();
    i = nameEnd;
    let j = i;
    while (j < source.length && /\s/.test(source[j])) j++;
    let value = null;
    if (source[j] === "=") {
      j++;
      while (j < source.length && /\s/.test(source[j])) j++;
      const quote = source[j];
      if (quote === '"' || quote === "'") {
        const closing = source.indexOf(quote, j + 1);
        if (closing === -1) return null;
        value = source.slice(j + 1, closing);
        i = closing + 1;
      } else {
        let k = j;
        while (k < source.length && !/[\s>]/.test(source[k])) k++;
        value = source.slice(j, k);
        i = k;
      }
      value = unescape(value);
    }
    attrs.push({ name: attrName, value, start: attrStart, end: i });
  }
  return null;
}

/** Scheme as Python's urlsplit reports it ("" for relative and protocol-relative URLs). */
function scheme(href) {
  const match = /^([a-zA-Z][a-zA-Z0-9+.-]*):/.exec(href.replace(/^[\x00-\x20]+/, ""));
  return match ? match[1].toLowerCase() : "";
}

function rewriteAnchor(source, tag) {
  const attr = (name) => tag.attrs.find((entry) => entry.name === name);
  const href = attr("href")?.value;
  if (!href || href.startsWith("#") || !["", "http", "https"].includes(scheme(href))) return null;
  const rel = new Set((attr("rel")?.value ?? "").split(/\s+/).filter(Boolean));
  rel.delete("opener");
  rel.add("noopener");
  let raw = "";
  let cursor = tag.start;
  for (const entry of tag.attrs) {
    if (entry.name !== "target" && entry.name !== "rel") continue;
    raw += source.slice(cursor, entry.start);
    cursor = entry.end;
  }
  raw += source.slice(cursor, tag.close).replace(/\s+$/, "");
  const close = source.slice(tag.close, tag.end) === "/>" ? ">" : source.slice(tag.close, tag.end);
  return `${raw} target="_blank" rel="${[...rel].sort().join(" ")}"${close}`;
}

/**
 * Give every destination link target="_blank" and a rel containing "noopener".
 * @param {string} source HTML document or fragment
 * @returns {string}
 */
export function openInNewTabs(source) {
  const lower = source.toLowerCase();
  let output = "";
  let copied = 0;
  let i = 0;
  while ((i = source.indexOf("<", i)) !== -1) {
    if (source.startsWith("<!--", i)) {
      const end = source.indexOf("-->", i + 4);
      if (end === -1) break;
      i = end + 3;
      continue;
    }
    if (source[i + 1] === "!" || source[i + 1] === "?" || source[i + 1] === "/") {
      const end = source.indexOf(">", i + 2);
      if (end === -1) break;
      i = end + 1;
      continue;
    }
    const tag = parseStartTag(source, i);
    if (!tag) {
      i++;
      continue;
    }
    tag.start = i;
    if (tag.name === "a") {
      const replacement = rewriteAnchor(source, tag);
      if (replacement !== null) {
        output += source.slice(copied, i) + replacement;
        copied = tag.end;
      }
    }
    i = tag.end;
    if (RAW_TEXT.has(tag.name) && source.slice(tag.close, tag.end) !== "/>") {
      const end = lower.indexOf(`</${tag.name}`, i);
      if (end === -1) break;
      i = end;
    }
  }
  return output + source.slice(copied);
}
