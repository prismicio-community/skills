#!/usr/bin/env node
// Checks what the build produced, independently of how it was produced:
// every plugin and prompt has exactly one download and skills have none, each
// plugin download contains exactly the package's files (no website content, no
// clutter), each prompt download is the prompt file byte for byte, and
// library.json matches the files on disk.
// Run with: npm run build && npm run verify
import fs from 'node:fs';
import crypto from 'node:crypto';
import { PATHS, abs, exists, readJson, walkFiles, loadPlugins, loadPrompts } from './lib/repo.mjs';
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
const prompts = loadPrompts().filter((p) => p.isPrompt);
const expectedFiles = new Set(['library.json']);

const sameSet = (label, actual, expected) => {
  const a = new Set(actual);
  const e = new Set(expected);
  for (const x of e) if (!a.has(x)) fail(`${label}: missing ${x}`);
  for (const x of a) if (!e.has(x)) fail(`${label}: unexpected ${x}`);
};

// The built file's bytes, after checking its size and checksum against library.json.
function checkFile(item, rel) {
  expectedFiles.add(rel);
  const file = `${PATHS.dist}/${rel}`;
  if (!exists(file)) return fail(`${item.id}: ${file} was not built`), null;
  const bytes = fs.readFileSync(abs(file));
  if (item.download.bytes !== bytes.length) fail(`${item.id}: library.json says ${item.download.bytes} bytes, file is ${bytes.length}`);
  const sha = crypto.createHash('sha256').update(bytes).digest('hex');
  if (item.download.sha256 !== sha) fail(`${item.id}: library.json checksum does not match ${file}`);
  return bytes;
}

function checkDownload(item, rel) {
  if (!checkFile(item, rel)) return null;
  const zip = readZip(abs(`${PATHS.dist}/${rel}`));
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
  const zip = checkDownload(item, `plugins/${p}.zip`);
  if (zip) {
    // Exactly the plugin folder's files, plus the generated Claude manifest, at the
    // archive root, where both Claude and ChatGPT look for their manifests.
    const expected = [...walkFiles(plugin.dir), '.claude-plugin/plugin.json'];
    sameSet(`${p}.zip`, Object.keys(zip), expected);
    for (const [path, bytes] of Object.entries(zip)) {
      if (path !== '.claude-plugin/plugin.json' && !Buffer.from(bytes).equals(fs.readFileSync(abs(`${plugin.dir}/${path}`)))) {
        fail(`${p}.zip: ${path} differs from the source file`);
      }
    }
    if (!zip['.codex-plugin/plugin.json']) fail(`${p}.zip: .codex-plugin/plugin.json is missing from the archive root`);
    const manifest = zip['.claude-plugin/plugin.json'];
    if (manifest) {
      const m = JSON.parse(decode(manifest));
      if (m.name !== p) fail(`${p}.zip: .claude-plugin/plugin.json has name "${m.name}"`);
      if ('skills' in m) fail(`${p}.zip: .claude-plugin/plugin.json must not list skills (they load from skills/)`);
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
    // Skills ship only inside their plugin.
    if ('download' in sitem) fail(`skill:${s}: skills must not have a download; they ship in ${p}.zip`);
  }
}

for (const prompt of prompts) {
  const n = prompt.name;
  const item = library.items.find((i) => i.id === `prompt:${n}`);
  if (!item) {
    fail(`prompt:${n}: missing from library.json`);
    continue;
  }
  // Visitors copy the text and download the file, so both must be the source exactly.
  const source = fs.readFileSync(abs(prompt.file));
  const bytes = checkFile(item, `prompts/${n}.md`);
  if (bytes && !bytes.equals(source)) fail(`prompt:${n}: ${n}.md differs from ${prompt.file}`);
  if (item.prompt?.markdown !== decode(source).replace(/^\uFEFF/, '')) fail(`prompt:${n}: library.json "prompt.markdown" differs from ${prompt.file}`);
  if (item.prompt?.file !== `${n}.md`) fail(`prompt:${n}: library.json "prompt.file" should be "${n}.md"`);
}

const knownIds = new Set([
  ...plugins.flatMap((p) => [`plugin:${p.name}`, ...p.skills.map((s) => `skill:${s.name}`)]),
  ...prompts.map((p) => `prompt:${p.name}`),
]);
for (const item of library.items) if (!knownIds.has(item.id)) fail(`${item.id}: in library.json but not in plugins/ or prompts/`);
const downloadFiles = library.items.filter((i) => i.download).map((i) => i.download.file);
if (new Set(downloadFiles).size !== downloadFiles.length) fail('two downloads share a file name');

const built = walkFiles(PATHS.dist);
sameSet('dist/', built, [...expectedFiles]);

if (failures.length) {
  console.error(`✖ Package check failed:\n${failures.map((f) => `  - ${f}`).join('\n')}`);
  process.exit(1);
}
console.log(`✔ Packages verified: ${downloadFiles.length} download(s) match the source folders and library.json.`);
