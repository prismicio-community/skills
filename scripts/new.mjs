#!/usr/bin/env node
// Scaffolds a plugin or skill from docs/templates/ and registers it in both marketplaces.
//   npm run new:plugin -- <plugin> <first-skill>
//   npm run new:skill -- <plugin> <skill>
// The new files contain "[[fill in: ...]]" placeholders, which "npm run validate"
// reports until they are replaced.
import fs from 'node:fs';
import path from 'node:path';
import { PATHS, abs, exists, readText, readJson, loadPlugins, loadConfig, contextPath } from './lib/repo.mjs';

const NAME_RE = /^[a-z0-9]+(-[a-z0-9]+)*$/;
const [kind, plugin, skill] = process.argv.slice(2);

const usage = () => {
  console.error('Usage:\n  npm run new:plugin -- <plugin> <first-skill>\n  npm run new:skill -- <plugin> <skill>');
  process.exit(1);
};
const die = (msg) => {
  console.error(`✖ ${msg}`);
  process.exit(1);
};

if (!['plugin', 'skill'].includes(kind) || !plugin || !skill) usage();
for (const n of [plugin, skill]) {
  if (!NAME_RE.test(n) || n.length > 64) die(`"${n}" must be lowercase letters, numbers, and hyphens, such as "meta-descriptions".`);
}

const plugins = loadPlugins();
const owner = plugins.flatMap((p) => p.skills).find((s) => s.name === skill);
if (owner) die(`A skill named "${skill}" already exists in plugins/${owner.plugin}. Skill names must be unique.`);

const title = (n) => n.split('-').map((w) => w[0].toUpperCase() + w.slice(1)).join(' ');
const fill = (template, vars) => readText(`docs/templates/${template}`).replace(/\{\{(\w+)\}\}/g, (_, k) => vars[k]);
const created = [];
const write = (rel, content) => {
  fs.mkdirSync(path.dirname(abs(rel)), { recursive: true });
  fs.writeFileSync(abs(rel), content);
  created.push(rel);
};
const writeJson = (rel, data) => fs.writeFileSync(abs(rel), `${JSON.stringify(data, null, 2)}\n`);

const claude = readJson(PATHS.claudeMarketplace);
const codex = readJson(PATHS.codexMarketplace);

if (kind === 'plugin') {
  if (exists(`${PATHS.plugins}/${plugin}`)) die(`plugins/${plugin} already exists. Use "npm run new:skill -- ${plugin} ${skill}" to add a skill to it.`);
  const { repository, license } = loadConfig();
  const author = { name: 'Prismic', url: 'https://prismic.io' };
  const description = '[[fill in: One sentence on what the plugin helps with.]]';

  write(`${PATHS.plugins}/${plugin}/.codex-plugin/plugin.json`, `${JSON.stringify({
    name: plugin,
    version: '0.1.0',
    description,
    author,
    repository: `https://github.com/${repository}`,
    license,
    keywords: [plugin],
    skills: './skills/',
    interface: {
      displayName: title(plugin),
      shortDescription: '[[fill in: Under 30 characters]]',
      longDescription: description,
      developerName: 'Prismic',
      category: 'Productivity',
      composerIcon: './assets/icon.svg',
      logo: './assets/icon.svg',
      logoDark: './assets/icon.svg',
      capabilities: ['Skills'],
      defaultPrompt: ['[[fill in: A prompt that shows what the plugin does.]]'],
    },
  }, null, 2)}\n`);
  write(`${PATHS.plugins}/${plugin}/assets/icon.svg`, readText('docs/templates/icon.template.svg'));

  claude.plugins.push({ name: plugin, source: `./plugins/${plugin}`, strict: false, description, author, skills: [] });
  codex.plugins.push({
    name: plugin,
    source: { source: 'local', path: `./plugins/${plugin}` },
    policy: { installation: 'AVAILABLE', authentication: 'ON_INSTALL' },
    category: 'Productivity',
  });
  write(contextPath.plugin(plugin), fill('plugin-page.template.md', { plugin, title: title(plugin) }));
} else if (!exists(`${PATHS.plugins}/${plugin}`)) {
  die(`plugins/${plugin} does not exist. Create it with "npm run new:plugin -- ${plugin} ${skill}".`);
}

// The skill, its page, and its marketplace listing.
write(`${PATHS.plugins}/${plugin}/skills/${skill}/SKILL.md`, fill('SKILL.template.md', { skill, title: title(skill) }));
write(contextPath.skill(plugin, skill), fill('skill-page.template.md', { skill, title: title(skill) }));
const entry = claude.plugins.find((e) => e.name === plugin);
if (!entry) die(`plugins/${plugin} has no entry in ${PATHS.claudeMarketplace}. Fix that first.`);
entry.skills = [...(entry.skills ?? []), `./skills/${skill}`];

writeJson(PATHS.claudeMarketplace, claude);
writeJson(PATHS.codexMarketplace, codex);

console.log(`Created:\n${created.map((f) => `  ${f}`).join('\n')}\nUpdated:\n  ${PATHS.claudeMarketplace}${kind === 'plugin' ? `\n  ${PATHS.codexMarketplace}` : ''}`);
console.log('\nNext: replace every "[[fill in: ...]]" placeholder, then run "npm run validate".');
