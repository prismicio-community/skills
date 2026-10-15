#!/usr/bin/env node
// Builds the downloads and the website index into dist/:
//   dist/skills/<skill>.zip       one skill folder, ready to upload to Claude
//   dist/plugins/<plugin>.plugin  one plugin folder with a generated .claude-plugin/plugin.json
//   dist/library.json             everything the library page needs
// Run with: npm run build
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { pathToFileURL } from 'node:url';
import { parse as parseYaml } from 'yaml';
import {
  PATHS, abs, readText, readJson, walkFiles, parseFrontmatter, splitSections, relativeLinks,
  loadConfig, gitCommit, contextPath,
} from './lib/repo.mjs';
import { createZip, fileEntry } from './lib/zip.mjs';
import { validate, report } from './validate.mjs';

export const SCHEMA_VERSION = 1;

export function build() {
  const result = validate();
  if (result.errors.length) {
    report(result);
    throw new Error('Fix the validation errors before building.');
  }

  const config = loadConfig();
  const commit = gitCommit();
  const claude = readJson(PATHS.claudeMarketplace);
  const marketplace = claude.name;
  const repoUrl = `https://github.com/${config.repository}`;
  const downloadBase = `${repoUrl}/releases/download/${config.releaseTag}`;
  const rawBase = `https://raw.githubusercontent.com/${config.repository}/${commit ?? config.branch}`;
  const taxonomy = parseYaml(readText(PATHS.taxonomy));

  fs.rmSync(abs(PATHS.dist), { recursive: true, force: true });
  fs.mkdirSync(abs(`${PATHS.dist}/skills`), { recursive: true });
  fs.mkdirSync(abs(`${PATHS.dist}/plugins`), { recursive: true });

  const pluginInstall = (p) => ({
    claudeCode: [`/plugin marketplace add ${config.repository}`, `/plugin install ${p}@${marketplace}`],
    codex: [`codex plugin marketplace add ${config.repository}`, `codex plugin add ${p}@${marketplace}`],
    marketplaceUrl: repoUrl,
  });

  const items = [];
  for (const plugin of result.plugins) {
    const p = plugin.name;
    const entry = claude.plugins.find((e) => e.name === p);
    const codexManifest = readJson(plugin.codexManifest);

    // Plugin download. Claude's "Upload plugin" needs .claude-plugin/plugin.json,
    // which the repo leaves out (the marketplace entry is the manifest there).
    const claudeManifest = {
      name: p,
      version: codexManifest.version,
      description: entry.description,
      author: entry.author,
      homepage: `${repoUrl}/tree/${config.branch}/plugins/${p}`,
      repository: repoUrl,
      license: config.license,
      keywords: codexManifest.keywords ?? [],
    };
    const pluginEntries = walkFiles(plugin.dir).map((f) => fileEntry(abs(`${plugin.dir}/${f}`), `${p}/${f}`));
    pluginEntries.push({
      path: `${p}/.claude-plugin/plugin.json`,
      data: Buffer.from(`${JSON.stringify(claudeManifest, null, 2)}\n`),
    });
    const pluginDownload = writeArchive(`plugins/${p}.plugin`, pluginEntries, downloadBase);

    items.push({
      ...page(contextPath.plugin(p), rawBase),
      id: `plugin:${p}`,
      type: 'plugin',
      slug: p,
      skills: plugin.skills.map((s) => s.name),
      displayName: codexManifest.interface?.displayName ?? p,
      paths: { source: plugin.dir, context: contextPath.plugin(p) },
      download: pluginDownload,
      install: pluginInstall(p),
    });

    for (const skill of plugin.skills) {
      const s = skill.name;
      const skillEntries = walkFiles(skill.dir).map((f) => fileEntry(abs(`${skill.dir}/${f}`), `${s}/${f}`));
      items.push({
        ...page(contextPath.skill(p, s), rawBase),
        id: `skill:${s}`,
        type: 'skill',
        slug: s,
        plugin: p,
        paths: { source: skill.dir, context: contextPath.skill(p, s) },
        download: writeArchive(`skills/${s}.zip`, skillEntries, downloadBase),
        install: {
          skillsCli: `npx skills add ${config.repository} --skill ${s}`,
          viaPlugin: pluginInstall(p),
        },
      });
    }
  }

  const library = {
    schemaVersion: SCHEMA_VERSION,
    commit,
    repository: { slug: config.repository, url: repoUrl, branch: config.branch },
    marketplace: {
      name: marketplace,
      displayName: readJson(PATHS.codexMarketplace).interface.displayName,
      url: repoUrl,
      install: {
        claudeCode: `/plugin marketplace add ${config.repository}`,
        codex: `codex plugin marketplace add ${config.repository}`,
        skillsCliList: `npx skills add ${config.repository} --list`,
      },
    },
    taxonomy,
    items,
  };
  fs.writeFileSync(abs(`${PATHS.dist}/library.json`), `${JSON.stringify(library, null, 2)}\n`);
  return library;
}

// Website fields from a library-context page. Relative images and links are
// rewritten to absolute URLs pinned to the built commit.
function page(file, rawBase) {
  const { data, body } = parseFrontmatter(readText(file));
  const dir = path.posix.dirname(file);
  const toUrl = (target) => `${rawBase}/${path.posix.normalize(path.posix.join(dir, target))}`;
  let markdown = body;
  for (const l of relativeLinks(body)) markdown = markdown.split(`](${l.target}`).join(`](${toUrl(l.target)}`);
  const { intro, sections } = splitSections(markdown);
  return {
    title: data.title,
    summary: data.summary,
    description: data.description,
    categories: data.categories,
    tags: data.tags,
    featured: data.featured ?? false,
    draft: data.draft ?? false,
    image: data.image ? toUrl(data.image) : null,
    badge: data.badge ?? null,
    output: data.output ?? null,
    platforms: data.platforms ?? [],
    requirements: (data.requirements ?? []).map((r) => ({ name: r.name, required: r.required, details: r.details ?? null })),
    examples: (data.examples ?? []).map((x) => ({ prompt: x.prompt, note: x.note ?? null })),
    intro,
    sections,
  };
}

function writeArchive(rel, entries, downloadBase) {
  const bytes = createZip(entries);
  fs.writeFileSync(abs(`${PATHS.dist}/${rel}`), bytes);
  const file = path.posix.basename(rel);
  return {
    file,
    url: `${downloadBase}/${file}`,
    bytes: bytes.length,
    sha256: crypto.createHash('sha256').update(bytes).digest('hex'),
    contents: entries.map((e) => e.path).sort(),
  };
}

if (import.meta.url === pathToFileURL(process.argv[1]).href) {
  try {
    const library = build();
    for (const item of library.items) console.log(`  ${item.type.padEnd(6)} ${item.download.file.padEnd(32)} ${item.download.bytes} bytes${item.draft ? '  (draft)' : ''}`);
    console.log(`\n✔ Built ${library.items.length} download(s) and ${PATHS.dist}/library.json`);
  } catch (e) {
    console.error(`\n✖ ${e.message}`);
    process.exit(1);
  }
}
