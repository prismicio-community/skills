#!/usr/bin/env node
// Scaffolds a plugin, skill, or prompt from docs/templates/. Plugins and skills
// are also registered in both marketplaces.
//   npm run new:plugin -- <plugin> <first-skill>
//   npm run new:skill -- <plugin> <skill>
//   npm run new:prompt -- <prompt>
// The new files contain "[[fill in: ...]]" placeholders, which "npm run validate"
// reports until they are replaced.
import fs from 'node:fs';
import path from 'node:path';
import { PATHS, abs, exists, readText, readJson, loadPlugins, loadConfig, contextPath } from './lib/repo.mjs';

const NAME_RE = /^[a-z0-9]+(-[a-z0-9]+)*$/;
const [kind, ...names] = process.argv.slice(2);
const [plugin, skill] = names;

const usage = () => {
  console.error('Usage:\n  npm run new:plugin -- <plugin> <first-skill>\n  npm run new:skill -- <plugin> <skill>\n  npm run new:prompt -- <prompt>');
  process.exit(1);
};
const die = (msg) => {
  console.error(`✖ ${msg}`);
  process.exit(1);
};

if (names.length !== { plugin: 2, skill: 2, prompt: 1 }[kind]) usage();
for (const n of names) {
  if (!NAME_RE.test(n) || n.length > 64) die(`"${n}" must be lowercase letters, numbers, and hyphens, such as "meta-descriptions".`);
}

const title = (n) => n.split('-').map((w) => w[0].toUpperCase() + w.slice(1)).join(' ');
const fill = (template, vars) => readText(`docs/templates/${template}`).replace(/\{\{(\w+)\}\}/g, (_, k) => vars[k]);
const created = [];
const updated = [PATHS.claudeMarketplace];
const write = (rel, content) => {
  fs.mkdirSync(path.dirname(abs(rel)), { recursive: true });
  fs.writeFileSync(abs(rel), content);
  created.push(rel);
};
const writeJson = (rel, data) => fs.writeFileSync(abs(rel), `${JSON.stringify(data, null, 2)}\n`);
const next = () => console.log('\nNext: replace every "[[fill in: ...]]" placeholder, then run "npm run validate".');
// A skill's entry in its plugin page's "skills" list. Skills have no page of their own.
const skillEntry = (s) => [
  `  - name: ${s}`,
  `    title: ${title(s)}`,
  '    summary: "[[fill in: One sentence on what the skill does, under 160 characters.]]"',
  '    output: "[[fill in: What the user gets, in a few words.]]"',
  '    example: "[[fill in: A prompt that runs the skill.]]"',
].join('\n');

// A prompt is one Markdown file and its page. It isn't listed in a marketplace.
if (kind === 'prompt') {
  const [prompt] = names;
  if (exists(`${PATHS.prompts}/${prompt}.md`)) die(`${PATHS.prompts}/${prompt}.md already exists. Prompt names must be unique.`);
  write(`${PATHS.prompts}/${prompt}.md`, readText('docs/templates/prompt.template.md'));
  write(contextPath.prompt(prompt), fill('prompt-page.template.md', { prompt, title: title(prompt) }));
  console.log(`Created:\n${created.map((f) => `  ${f}`).join('\n')}`);
  next();
  process.exit(0);
}

const owner = loadPlugins().flatMap((p) => p.skills).find((s) => s.name === skill);
if (owner) die(`A skill named "${skill}" already exists in plugins/${owner.plugin}. Skill names must be unique.`);

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
  write(contextPath.plugin(plugin), fill('plugin-page.template.md', { plugin, skillEntry: skillEntry(skill), title: title(plugin) }));
} else if (!exists(`${PATHS.plugins}/${plugin}`)) {
  die(`plugins/${plugin} does not exist. Create it with "npm run new:plugin -- ${plugin} ${skill}".`);
} else {
  // Add the skill to the end of the plugin page's "skills" list.
  const page = contextPath.plugin(plugin);
  const lines = readText(page).split('\n');
  const start = lines.findIndex((l) => /^skills:\s*$/.test(l));
  if (start === -1) console.log(`Add an item for "${skill}" to "skills" in ${page}.`);
  else {
    let end = start + 1;
    while (end < lines.length && /^\s+\S/.test(lines[end])) end++;
    lines.splice(end, 0, skillEntry(skill));
    fs.writeFileSync(abs(page), lines.join('\n'));
    updated.push(page);
  }
}

// The skill and its marketplace listing.
write(`${PATHS.plugins}/${plugin}/skills/${skill}/SKILL.md`, fill('SKILL.template.md', { skill, title: title(skill) }));
const entry = claude.plugins.find((e) => e.name === plugin);
if (!entry) die(`plugins/${plugin} has no entry in ${PATHS.claudeMarketplace}. Fix that first.`);
entry.skills = [...(entry.skills ?? []), `./skills/${skill}`];

writeJson(PATHS.claudeMarketplace, claude);
writeJson(PATHS.codexMarketplace, codex);

if (kind === 'plugin') updated.push(PATHS.codexMarketplace);
console.log(`Created:\n${created.map((f) => `  ${f}`).join('\n')}\nUpdated:\n${updated.map((f) => `  ${f}`).join('\n')}`);
next();
