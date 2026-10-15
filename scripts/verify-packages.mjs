#!/usr/bin/env node
// Checks what the build produced, independently of how it was produced:
// every plugin and skill has exactly one download, each download contains
// exactly the package's files (no website content, no clutter), and
// library.json matches the files on disk.
// Run with: npm run build && npm run verify
import fs from 'node:fs';
import crypto from 'node:crypto';
import { PATHS, abs, exists, readJson, walkFiles, parseFrontmatter, loadPlugins } from './lib/repo.mjs';
import { readZip } from './lib/zip.mjs';

const failures = [];
const fail = (msg) => failures.push(msg);
const decode = (bytes) => new TextDecoder().decode(bytes);

if (!exists(`${PATHS.dist}/library.json`)) {
  console.error('✖ dist/library.json not found. Run "npm run build" first.');
  process.exit(1);
}
const library = readJson(`${PATHS.dist}/library.json`);
const plugins = loadPlugins();
const expectedFiles = new Set(['library.json']);

const sameSet = (label, actual, expected) => {
  const a = new Set(actual);
  const e = new Set(expected);
  for (const x of e) if (!a.has(x)) fail(`${label}: missing ${x}`);
  for (const x of a) if (!e.has(x)) fail(`${label}: unexpected ${x}`);
};

function checkDownload(item, rel) {
  expectedFiles.add(rel);
  const file = `${PATHS.dist}/${rel}`;
  if (!exists(file)) return fail(`${item.id}: ${file} was not built`), null;
  const bytes = fs.readFileSync(abs(file));
  if (item.download.bytes !== bytes.length) fail(`${item.id}: library.json says ${item.download.bytes} bytes, file is ${bytes.length}`);
  const sha = crypto.createHash('sha256').update(bytes).digest('hex');
  if (item.download.sha256 !== sha) fail(`${item.id}: library.json checksum does not match ${file}`);
  const zip = readZip(abs(file));
  sameSet(`${item.id} library.json contents`, item.download.contents, Object.keys(zip));
  for (const p of Object.keys(zip)) {
    if (/(^|\/)(library-context|\.DS_Store|Thumbs\.db|node_modules|\.git)(\/|$)/.test(p)) fail(`${item.id}: ${p} must not be packaged`);
  }
  return zip;
}

for (const plugin of plugins) {
  const p = plugin.name;
  const item = library.items.find((i) => i.id === `plugin:${p}`);
  if (!item) {
    fail(`plugin:${p}: missing from library.json`);
    continue;
  }
  const zip = checkDownload(item, `plugins/${p}.plugin`);
  if (zip) {
    // Exactly the plugin folder, plus the generated Claude manifest, under one top-level folder.
    const expected = [...walkFiles(plugin.dir).map((f) => `${p}/${f}`), `${p}/.claude-plugin/plugin.json`];
    sameSet(`${p}.plugin`, Object.keys(zip), expected);
    for (const [path, bytes] of Object.entries(zip)) {
      const src = path.slice(p.length + 1);
      if (src !== '.claude-plugin/plugin.json' && !Buffer.from(bytes).equals(fs.readFileSync(abs(`${plugin.dir}/${src}`)))) {
        fail(`${p}.plugin: ${path} differs from the source file`);
      }
    }
    const manifest = zip[`${p}/.claude-plugin/plugin.json`];
    if (manifest) {
      const m = JSON.parse(decode(manifest));
      if (m.name !== p) fail(`${p}.plugin: .claude-plugin/plugin.json has name "${m.name}"`);
      if ('skills' in m) fail(`${p}.plugin: .claude-plugin/plugin.json must not list skills (they load from skills/)`);
    }
  }
  sameSet(`plugin:${p} skills`, item.skills, plugin.skills.map((s) => s.name));

  for (const skill of plugin.skills) {
    const s = skill.name;
    const sitem = library.items.find((i) => i.id === `skill:${s}`);
    if (!sitem) {
      fail(`skill:${s}: missing from library.json`);
      continue;
    }
    if (sitem.plugin !== p) fail(`skill:${s}: library.json says plugin "${sitem.plugin}", expected "${p}"`);
    const szip = checkDownload(sitem, `skills/${s}.zip`);
    if (!szip) continue;
    // Claude's skill upload wants the skill folder at the top of the zip, named like the skill.
    sameSet(`${s}.zip`, Object.keys(szip), walkFiles(skill.dir).map((f) => `${s}/${f}`));
    const md = szip[`${s}/SKILL.md`];
    if (!md) fail(`${s}.zip: ${s}/SKILL.md is missing`);
    else if (parseFrontmatter(decode(md)).data?.name !== s) fail(`${s}.zip: SKILL.md name does not match the folder`);
  }
}

const knownIds = new Set(plugins.flatMap((p) => [`plugin:${p.name}`, ...p.skills.map((s) => `skill:${s.name}`)]));
for (const item of library.items) if (!knownIds.has(item.id)) fail(`${item.id}: in library.json but not in plugins/`);
if (new Set(library.items.map((i) => i.download.file)).size !== library.items.length) fail('two downloads share a file name');

const built = walkFiles(PATHS.dist);
sameSet('dist/', built, [...expectedFiles]);

if (failures.length) {
  console.error(`✖ Package check failed:\n${failures.map((f) => `  - ${f}`).join('\n')}`);
  process.exit(1);
}
console.log(`✔ Packages verified: ${library.items.length} download(s) match the source folders and library.json.`);
