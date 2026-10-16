// Shared helpers for reading the repository layout.
import fs from 'node:fs';
import path from 'node:path';
import { execFileSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { parse as parseYaml } from 'yaml';

export const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..', '..');

export const PATHS = {
  claudeMarketplace: '.claude-plugin/marketplace.json',
  codexMarketplace: '.agents/plugins/marketplace.json',
  plugins: 'plugins',
  prompts: 'prompts',
  context: 'library-context',
  taxonomy: 'library-context/taxonomy.yml',
  dist: 'dist',
};

// OS and tooling clutter. Never validated, never packaged.
const JUNK = new Set(['.DS_Store', 'Thumbs.db', 'desktop.ini', 'node_modules', '.git']);
export const isJunk = (name) => JUNK.has(name) || name.endsWith('.log');

export const abs = (rel) => path.join(ROOT, rel);
export const exists = (rel) => fs.existsSync(abs(rel));
export const readText = (rel) => fs.readFileSync(abs(rel), 'utf8').replace(/^﻿/, '');
export const readJson = (rel) => JSON.parse(readText(rel));

export function listDirs(rel) {
  if (!exists(rel)) return [];
  return fs
    .readdirSync(abs(rel), { withFileTypes: true })
    .filter((e) => e.isDirectory() && !isJunk(e.name))
    .map((e) => e.name)
    .sort();
}

// Exact-case lookup: macOS and Windows file systems ignore case, so
// fs.existsSync('SKILL.md') is true for 'skill.md' there but not on Linux.
export function hasExactFile(dirRel, name) {
  if (!exists(dirRel)) return false;
  return fs.readdirSync(abs(dirRel)).includes(name);
}

// Every entry under a directory, as sorted POSIX paths relative to it.
// type is 'file', 'dir', or 'symlink'. Junk is skipped.
export function walk(rel) {
  const out = [];
  const visit = (dirAbs, prefix) => {
    for (const e of fs.readdirSync(dirAbs, { withFileTypes: true })) {
      if (isJunk(e.name)) continue;
      const p = prefix ? `${prefix}/${e.name}` : e.name;
      if (e.isSymbolicLink()) out.push({ path: p, type: 'symlink' });
      else if (e.isDirectory()) {
        out.push({ path: p, type: 'dir' });
        visit(path.join(dirAbs, e.name), p);
      } else if (e.isFile()) out.push({ path: p, type: 'file' });
    }
  };
  if (exists(rel)) visit(abs(rel), '');
  return out.sort((a, b) => (a.path < b.path ? -1 : a.path > b.path ? 1 : 0));
}

export const walkFiles = (rel) => walk(rel).filter((e) => e.type === 'file').map((e) => e.path);

export function parseFrontmatter(text) {
  const m = text.replace(/^﻿/, '').match(/^---\r?\n([\s\S]*?)\r?\n---[ \t]*(?:\r?\n([\s\S]*))?$/);
  if (!m) return { data: null, body: text, error: 'the file must start with a frontmatter block between two "---" lines' };
  try {
    const data = parseYaml(m[1]) ?? {};
    if (typeof data !== 'object' || Array.isArray(data)) {
      return { data: null, body: m[2] ?? '', error: 'the frontmatter must be a list of "key: value" lines' };
    }
    return { data, body: m[2] ?? '' };
  } catch (e) {
    return { data: null, body: m[2] ?? '', error: `the frontmatter is not valid YAML (${e.message.split('\n')[0]})` };
  }
}

// Split a Markdown body into the text before the first "## " heading and one
// section per "## " heading. Headings inside fenced code blocks are ignored.
export function splitSections(body) {
  const lines = body.split(/\r?\n/);
  const intro = [];
  const sections = [];
  let fence = null;
  for (const line of lines) {
    const f = line.match(/^\s*(`{3,}|~{3,})/);
    if (f) fence = fence === null ? f[1][0] : fence === f[1][0] ? null : fence;
    const h = fence === null && line.match(/^##\s+(.+?)\s*#*\s*$/);
    if (h) sections.push({ heading: h[1], lines: [] });
    else (sections.length ? sections[sections.length - 1].lines : intro).push(line);
  }
  return {
    intro: intro.join('\n').trim(),
    sections: sections.map((s) => ({ id: slugify(s.heading), heading: s.heading, markdown: s.lines.join('\n').trim() })),
  };
}

export const slugify = (s) =>
  s.toLowerCase().normalize('NFKD').replace(/[^\w\s-]/g, '').trim().replace(/[\s_]+/g, '-').replace(/-+/g, '-');

// Relative link and image targets in Markdown: [text](target) and ![alt](target).
// External URLs, mailto: and in-page anchors are skipped.
export function relativeLinks(markdown) {
  const out = [];
  const withoutCode = markdown.replace(/```[\s\S]*?```/g, '').replace(/`[^`\n]*`/g, '');
  for (const m of withoutCode.matchAll(/!?\[[^\]]*\]\(\s*<?([^)\s>]+)>?(?:\s+"[^"]*")?\s*\)/g)) {
    const target = m[1];
    if (/^([a-z][a-z0-9+.-]*:|#|\/\/)/i.test(target)) continue;
    const bare = target.split('#')[0].split('?')[0];
    let clean = bare;
    try {
      clean = decodeURI(bare);
    } catch {}
    out.push({ target, clean, image: m[0].startsWith('!') });
  }
  return out;
}

export function loadConfig() {
  const pkg = readJson('package.json');
  return { ...pkg.library, license: pkg.license };
}

export function gitCommit() {
  if (process.env.GITHUB_SHA) return process.env.GITHUB_SHA;
  try {
    return execFileSync('git', ['rev-parse', 'HEAD'], { cwd: ROOT, stdio: ['ignore', 'pipe', 'ignore'] }).toString().trim();
  } catch {
    return null;
  }
}

export const contextPath = {
  plugin: (p) => `${PATHS.context}/plugins/${p}/index.md`,
  skill: (p, s) => `${PATHS.context}/plugins/${p}/skills/${s}/index.md`,
  prompt: (name) => `${PATHS.context}/prompts/${name}/index.md`,
};

// The plugin and skill folders on disk, with each skill's SKILL.md parsed.
export function loadPlugins() {
  return listDirs(PATHS.plugins).map((name) => {
    const dir = `${PATHS.plugins}/${name}`;
    const skills = listDirs(`${dir}/skills`).map((skill) => {
      const sdir = `${dir}/skills/${skill}`;
      const file = `${sdir}/SKILL.md`;
      const present = hasExactFile(sdir, 'SKILL.md');
      return { name: skill, plugin: name, dir: sdir, file, present, ...(present ? parseFrontmatter(readText(file)) : {}) };
    });
    return { name, dir, codexManifest: `${dir}/.codex-plugin/plugin.json`, skills };
  });
}

// The prompt files on disk: prompts/<name>.md, copied by visitors exactly as written.
// Anything else in prompts/ is returned with its entry type so validate can report it.
export function loadPrompts() {
  if (!exists(PATHS.prompts)) return [];
  return fs
    .readdirSync(abs(PATHS.prompts), { withFileTypes: true })
    .filter((e) => !isJunk(e.name))
    .map((e) => {
      const file = `${PATHS.prompts}/${e.name}`;
      const isPrompt = e.isFile() && e.name.endsWith('.md');
      return { name: isPrompt ? e.name.slice(0, -3) : e.name, file, entry: e.name, isPrompt };
    })
    .sort((a, b) => (a.entry < b.entry ? -1 : a.entry > b.entry ? 1 : 0));
}
