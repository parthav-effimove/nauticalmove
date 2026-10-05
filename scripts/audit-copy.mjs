import fs from "node:fs";
import ts from "typescript";

const urls = ["https://public.axsmarine.com/axsdry", "https://public.axsmarine.com/axsdry/all-tools"];
const decode = (text) => text.replace(/&#(x[\da-f]+|\d+);/gi, (_, code) => String.fromCodePoint(code[0].toLowerCase() === "x" ? parseInt(code.slice(1), 16) : Number(code))).replace(/&(?:amp|nbsp|quot|apos|lt|gt);/g, (entity) => ({ "&amp;": "&", "&nbsp;": " ", "&quot;": '"', "&apos;": "'", "&lt;": "<", "&gt;": ">" }[entity]));
const normalize = (text) => decode(text).toLowerCase().replace(/[’‘]/g, "'").replace(/\s+/g, " ").trim();
const words = (text) => normalize(text).match(/[a-z]+(?:['-][a-z]+)*/g) ?? [];
const sources = await Promise.all(urls.map(async (url) => {
  const response = await fetch(url);
  if (!response.ok) throw new Error(`${url}: ${response.status}`);
  return normalize((await response.text()).replace(/<(script|style)\b[^>]*>[\s\S]*?<\/\1>/gi, " ").replace(/<[^>]+>/g, " "));
}));
const vocabulary = new Set(sources.flatMap(words));
const files = ["app/page.tsx", "app/solutions/page.tsx", "app/markets/page.tsx", "app/intelligence/page.tsx", "app/company/page.tsx", "app/layout.tsx", "components/SiteChrome.tsx", "components/PageHero.tsx"];
const missing = new Set();
const duplicates = [];
let checked = 0;
for (const file of files) {
  const ast = ts.createSourceFile(file, fs.readFileSync(file, "utf8"), ts.ScriptTarget.Latest, true, ts.ScriptKind.TSX);
  const copy = [];
  function visit(node) {
    if (ts.isJsxText(node)) copy.push(node.text);
    if (ts.isStringLiteral(node)) {
      const parent = node.parent;
      const excludedAttribute = ts.isJsxAttribute(parent) && !["aria-label", "alt", "title", "description", "eyebrow", "action"].includes(parent.name.text);
      const excludedProperty = ts.isPropertyAssignment(parent) && ["id", "code", "number", "type", "template"].includes(parent.name.getText(ast));
      if (!excludedAttribute && !excludedProperty && !ts.isImportDeclaration(parent) && !node.text.startsWith("/") && !node.text.startsWith("mailto:") && !["use client", "next/link", "next", "lucide-react", "en"].includes(node.text) && !/^(?:nav-links|solution-detail)/.test(node.text)) copy.push(node.text);
    }
    ts.forEachChild(node, visit);
  }
  visit(ast);
  for (const text of copy) {
    const clean = text.replace(/\b\S+@\S+\b/g, "").replace(/nauticalmove/gi, "");
    for (const word of words(clean)) {
      checked++;
      if (!vocabulary.has(word)) missing.add(word);
    }
    for (const sentence of normalize(clean).match(/[^.!?]+[.!?]/g) ?? []) {
      const candidate = sentence.trim();
      if (words(candidate).length >= 3 && sources.some((source) => source.includes(candidate))) duplicates.push({ file, sentence: candidate });
    }
  }
}
console.log(JSON.stringify({ checkedWords: checked, absentWords: [...missing].sort(), copiedSentences: duplicates }, null, 2));
if (missing.size || duplicates.length) process.exitCode = 1;
