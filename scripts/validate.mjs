#!/usr/bin/env node
// Checks the marketplaces, plugins, skills, prompts, and library-context pages.
// Run with: npm run validate
import fs from 'node:fs';
import path from 'node:path';
import { pathToFileURL } from 'node:url';
import { parse as parseYaml } from 'yaml';
import {
  PATHS, abs, exists, readText, readJson, listDirs, walk, hasExactFile, parseFrontmatter,
  splitSections, relativeLinks, loadPlugins, loadPrompts, contextPath,
} from './lib/repo.mjs';

const NAME_RE = /^[a-z0-9]+(-[a-z0-9]+)*$/;
const SEMVER_RE = /^\d+\.\d+\.\d+(-[0-9A-Za-z.-]+)?(\+[0-9A-Za-z.-]+)?$/;
const MB = 1024 * 1024;

// Frontmatter keys from the Agent Skills specification (agentskills.io).
const SKILL_KEYS = new Set(['name', 'description', 'license', 'compatibility', 'metadata', 'allowed-tools']);

// Top-level entries a plugin package may contain. Website material belongs in library-context/.
const PLUGIN_ENTRIES = new Set(['.codex-plugin', 'skills', 'assets', 'agents', 'commands', 'hooks', '.mcp.json', '.app.json']);

// library-context page schema. Keep in sync with library-context/README.md.
const PAGE_KEYS = {
  title: { required: true },
  summary: { required: true },
  description: { required: true },
  categories: { required: true },
  tags: { required: true },
  featured: { required: false },
  draft: { required: false },
  image: { required: false },
  problem: { required: true },
  output: { required: false },
  requirements: { required: false },
  customize: { required: false, kinds: ['plugin'] },
  skills: { required: true, kinds: ['plugin'] },
  examples: { required: false },
};
// Each item in a plugin page's "skills" list: the skill's entry in the plugin's panel.
const SKILL_ENTRY_KEYS = ['name', 'title', 'summary', 'output', 'example'];
// Each "## " heading is a tab on the website.
const SECTIONS = ['How it works', 'Customize', 'How to use', "What it isn't", 'Mistakes to avoid'];
const REQUIRED_SECTIONS = ['How it works'];

// Placeholder marker used by docs/templates/. Nothing ships while one is left.
const PLACEHOLDER = '[[fill in';

export function validate() {
  const errors = [];
  const warnings = [];
  const error = (file, msg) => errors.push({ file, msg });
  const warn = (file, msg) => warnings.push({ file, msg });

  const plugins = loadPlugins();
  const pluginNames = new Set(plugins.map((p) => p.name));

  // ---------------------------------------------------------------- marketplaces
  const claude = loadJson(PATHS.claudeMarketplace, error);
  const codex = loadJson(PATHS.codexMarketplace, error);

  if (claude) {
    const f = PATHS.claudeMarketplace;
    if (!NAME_RE.test(claude.name ?? '')) error(f, '"name" must be lowercase letters, numbers, and hyphens.');
    if (!claude.owner?.name) error(f, '"owner.name" is required.');
    if (!claude.description) warn(f, '"description" is missing.');
    if ('version' in claude) error(f, 'Remove "version". Without it, every commit to main is a new release (see AGENTS.md).');
    if (!Array.isArray(claude.plugins)) error(f, '"plugins" must be a list.');
  }
  if (codex) {
    const f = PATHS.codexMarketplace;
    if (!NAME_RE.test(codex.name ?? '')) error(f, '"name" must be lowercase letters, numbers, and hyphens.');
    if (!codex.interface?.displayName) error(f, '"interface.displayName" is required.');
    if (!Array.isArray(codex.plugins)) error(f, '"plugins" must be a list.');
  }
  if (claude && codex && claude.name !== codex.name) {
    error(PATHS.codexMarketplace, `"name" is "${codex.name}" but ${PATHS.claudeMarketplace} uses "${claude.name}". They must match.`);
  }

  for (const f of [PATHS.claudeMarketplace, PATHS.codexMarketplace, ...plugins.map((p) => p.codexManifest)]) {
    if (exists(f) && readText(f).includes(PLACEHOLDER)) error(f, `Replace every "${PLACEHOLDER}: ...]]" placeholder with real text.`);
  }

  const claudeEntries = indexEntries(claude?.plugins, PATHS.claudeMarketplace, error);
  const codexEntries = indexEntries(codex?.plugins, PATHS.codexMarketplace, error);

  for (const [name] of claudeEntries) {
    if (!pluginNames.has(name)) error(PATHS.claudeMarketplace, `Plugin "${name}" is listed but plugins/${name}/ does not exist.`);
  }
  for (const [name] of codexEntries) {
    if (!pluginNames.has(name)) error(PATHS.codexMarketplace, `Plugin "${name}" is listed but plugins/${name}/ does not exist.`);
  }

  // ---------------------------------------------------------------- plugins and skills
  const skillOwners = new Map();

  for (const plugin of plugins) {
    const p = plugin.name;
    const dir = plugin.dir;
    const expectedSource = `./plugins/${p}`;

    if (!NAME_RE.test(p) || p.length > 64) error(dir, `Folder name "${p}" must be lowercase letters, numbers, and hyphens (max 64).`);

    // Claude marketplace entry
    const ce = claudeEntries.get(p);
    if (!ce) {
      if (claude) error(PATHS.claudeMarketplace, `Add an entry for plugin "${p}" (copy an existing entry and change the names).`);
    } else {
      const f = PATHS.claudeMarketplace;
      if (ce.source !== expectedSource) error(f, `"${p}": "source" must be "${expectedSource}".`);
      if (ce.strict !== false) error(f, `"${p}": "strict" must be false.`);
      if ('version' in ce) error(f, `"${p}": remove "version" (see AGENTS.md).`);
      if (!ce.description) error(f, `"${p}": "description" is required.`);
      if (!ce.author?.name) error(f, `"${p}": "author.name" is required.`);
      const listed = Array.isArray(ce.skills) ? ce.skills : [];
      const expected = plugin.skills.map((s) => `./skills/${s.name}`);
      for (const s of expected) if (!listed.includes(s)) error(f, `"${p}": add "${s}" to "skills".`);
      for (const s of listed) if (!expected.includes(s)) error(f, `"${p}": "skills" lists "${s}", which does not exist in ${dir}/skills/.`);
      if (new Set(listed).size !== listed.length) error(f, `"${p}": "skills" lists the same skill twice.`);
    }

    // Codex / ChatGPT marketplace entry
    const xe = codexEntries.get(p);
    if (!xe) {
      if (codex) error(PATHS.codexMarketplace, `Add an entry for plugin "${p}" (copy an existing entry and change the names).`);
    } else {
      const f = PATHS.codexMarketplace;
      if (xe.source?.source !== 'local' || xe.source?.path !== expectedSource) {
        error(f, `"${p}": "source" must be { "source": "local", "path": "${expectedSource}" }.`);
      }
      if (!['AVAILABLE', 'INSTALLED_BY_DEFAULT', 'NOT_AVAILABLE'].includes(xe.policy?.installation)) {
        error(f, `"${p}": "policy.installation" must be AVAILABLE, INSTALLED_BY_DEFAULT, or NOT_AVAILABLE.`);
      }
      if (!xe.policy?.authentication) error(f, `"${p}": "policy.authentication" is required (use "ON_INSTALL").`);
      if (!xe.category) error(f, `"${p}": "category" is required.`);
    }

    // Codex / ChatGPT plugin manifest
    const mf = plugin.codexManifest;
    const m = exists(mf) ? loadJson(mf, error) : (error(mf, 'Missing. Copy it from another plugin and change the values.'), null);
    if (m) {
      if (m.name !== p) error(mf, `"name" must be "${p}" (the folder name).`);
      if (!SEMVER_RE.test(m.version ?? '')) error(mf, '"version" must be a version number such as "0.1.0".');
      if (!m.description) error(mf, '"description" is required.');
      if (!m.author?.name) error(mf, '"author.name" is required.');
      if (m.skills !== './skills/') error(mf, '"skills" must be "./skills/".');
      const i = m.interface ?? {};
      for (const k of ['displayName', 'shortDescription', 'longDescription', 'developerName', 'category']) {
        if (!i[k]) error(mf, `"interface.${k}" is required.`);
      }
      if (!Array.isArray(i.capabilities) || !i.capabilities.length) error(mf, '"interface.capabilities" must be a list, for example ["Skills"].');
      // ChatGPT rejects an uploaded plugin that breaks these limits.
      if (m.name?.length > 64) error(mf, '"name" must be 64 characters or fewer.');
      if (i.displayName?.length > 30) error(mf, '"interface.displayName" must be 30 characters or fewer for ChatGPT.');
      if (i.shortDescription?.length > 30) error(mf, '"interface.shortDescription" must be 30 characters or fewer for ChatGPT.');
      if (i.longDescription?.length > 4000) error(mf, '"interface.longDescription" must be 4000 characters or fewer for ChatGPT.');
      for (const k of ['composerIcon', 'logo']) if (!i[k]) error(mf, `"interface.${k}" is required, for example "./assets/icon.svg".`);
      if (i.brandColor && !/^#[0-9A-Fa-f]{6}$/.test(i.brandColor)) error(mf, '"interface.brandColor" must look like "#6E56CF".');
      if (i.defaultPrompt !== undefined) {
        if (!Array.isArray(i.defaultPrompt) || i.defaultPrompt.length > 3) error(mf, '"interface.defaultPrompt" must be a list of up to 3 prompts.');
        else i.defaultPrompt.forEach((d, n) => d.length > 128 && error(mf, `"interface.defaultPrompt" item ${n + 1} is over 128 characters.`));
      }
      for (const k of ['composerIcon', 'logo', 'logoDark']) {
        if (i[k] && !insideAndExists(dir, i[k])) error(mf, `"interface.${k}" points to "${i[k]}", which does not exist in ${dir}/.`);
      }
    }

    // Package contents
    if (exists(`${dir}/.claude-plugin`)) {
      error(`${dir}/.claude-plugin`, 'Remove this folder. Claude reads the plugin from the marketplace entry, and a plugin.json here conflicts with "strict": false. Downloads get a generated one.');
    }
    if (exists(`${dir}/bin`)) error(`${dir}/bin`, 'A top-level bin/ folder is rejected by Claude organization sync. Move scripts into the skill that uses them.');
    for (const e of fs.readdirSync(abs(dir))) {
      if (e.startsWith('.') && !PLUGIN_ENTRIES.has(e) && e !== '.DS_Store') warn(`${dir}/${e}`, 'Unexpected hidden file in a plugin package.');
      else if (!e.startsWith('.') && !PLUGIN_ENTRIES.has(e)) {
        warn(`${dir}/${e}`, 'Unexpected item in a plugin package. Website text and images belong in library-context/.');
      }
    }
    for (const e of walk(dir)) {
      const f = `${dir}/${e.path}`;
      if (e.type === 'symlink') error(f, 'Symbolic links are not allowed. Copy the file instead.');
      if (e.type === 'file' && fs.statSync(abs(f)).size > 5 * MB) warn(f, 'File is over 5 MB. Large files slow down installs.');
    }
    if (!plugin.skills.length) error(`${dir}/skills`, 'A plugin needs at least one skill.');

    for (const skill of plugin.skills) {
      validateSkill(skill, { error, warn });
      if (skillOwners.has(skill.name)) {
        error(skill.dir, `Another skill is already named "${skill.name}" (in plugins/${skillOwners.get(skill.name)}). Skill names must be unique across all plugins, or the skills CLI installs only one of them.`);
      } else skillOwners.set(skill.name, p);
    }
  }

  // ---------------------------------------------------------------- prompts
  const entries = loadPrompts();
  for (const prompt of entries) validatePrompt(prompt, { error, warn });
  const prompts = entries.filter((p) => p.isPrompt);

  // ---------------------------------------------------------------- library-context
  validateContext(plugins, prompts, { error, warn });

  return { errors, warnings, plugins, prompts };
}

function validateSkill(skill, { error, warn }) {
  const f = skill.file;
  if (!skill.present) {
    error(f, hasExactFile(skill.dir, 'skill.md') || fs.readdirSync(abs(skill.dir)).some((x) => x.toLowerCase() === 'skill.md')
      ? 'Rename the file to SKILL.md (all capitals).'
      : 'Missing. Every skill folder needs a SKILL.md.');
    return;
  }
  if (skill.error) return error(f, `Frontmatter problem: ${skill.error}.`);
  const fm = skill.data;
  if (fm.name !== skill.name) error(f, `"name" must be "${skill.name}" (the folder name).`);
  if (!NAME_RE.test(skill.name) || skill.name.length > 64) error(f, 'The skill name must be lowercase letters, numbers, and hyphens (max 64).');
  if (typeof fm.description !== 'string' || !fm.description.trim()) error(f, '"description" is required.');
  else if (fm.description.length > 1024) error(f, `"description" is ${fm.description.length} characters. The limit is 1024.`);
  else if (fm.description.length > 450) warn(f, `"description" is ${fm.description.length} characters. Aim for 450 or fewer: it is for routing, not instructions.`);
  for (const k of Object.keys(fm)) if (!SKILL_KEYS.has(k)) warn(f, `"${k}" is not an Agent Skills frontmatter field. Some assistants may reject or ignore it.`);
  if (fm.metadata?.internal === true || fm.metadata?.internal === 'true') warn(f, '"metadata.internal" hides this skill from the skills CLI.');

  const body = skill.body ?? '';
  const lineCount = body.split('\n').length;
  if (lineCount > 500) warn(f, `SKILL.md is ${lineCount} lines. Move detail into references/ to stay under 500.`);
  if (/mcp__/.test(body)) warn(f, 'Name connector capabilities ("a Notion connector"), not tool ids like mcp__...');
  if (/\bplugins?\b/i.test(body)) warn(f, 'Skills should not mention plugins. Refer to sibling skills by name instead.');

  // Files the skill tells the agent to read must ship with it.
  const refs = new Set(relativeLinks(body).map((l) => l.clean));
  for (const m of body.matchAll(/`((?:references|assets|scripts|templates)\/[^`\s]+)`/g)) refs.add(m[1]);
  for (const r of refs) {
    if (!insideAndExists(skill.dir, r)) error(f, `Refers to "${r}", which does not exist in ${skill.dir}/.`);
  }
  for (const e of walk(skill.dir)) {
    if (e.type === 'file' && /\.(md|txt)$/i.test(e.path) && readText(`${skill.dir}/${e.path}`).includes(PLACEHOLDER)) {
      error(`${skill.dir}/${e.path}`, `Replace every "${PLACEHOLDER}: ...]]" placeholder with real text.`);
    }
  }
  if (exists(`${skill.dir}/README.md`)) warn(`${skill.dir}/README.md`, 'Skills do not need a README. Put agent instructions in SKILL.md and website text in library-context/.');
}

// A prompt is one Markdown file that visitors copy and paste exactly as written.
function validatePrompt(prompt, { error, warn }) {
  const f = prompt.file;
  if (!prompt.isPrompt) {
    return error(f, 'Unexpected item. Each prompt is one Markdown file, prompts/<prompt>.md. Images for its page go in library-context/prompts/<prompt>/assets/.');
  }
  if (!NAME_RE.test(prompt.name) || prompt.name.length > 64) {
    error(f, `"${prompt.entry}" must be lowercase letters, numbers, and hyphens, followed by .md, such as "content-dashboard.md" (max 64 before .md).`);
  }
  const text = readText(f);
  if (!text.trim()) return error(f, 'The prompt is empty.');
  if (/^---\r?\n/.test(text)) {
    error(f, `Remove the frontmatter. Visitors copy this file exactly as written, so it holds only the prompt. Card and page fields go in ${contextPath.prompt(prompt.name)}.`);
  }
  if (text.includes(PLACEHOLDER)) error(f, `Replace every "${PLACEHOLDER}: ...]]" placeholder with real text.`);
  if (/mcp__/.test(text)) warn(f, 'Name connector capabilities ("a Notion connector"), not tool ids like mcp__...');
}

function validateContext(plugins, prompts, { error, warn }) {
  const ctx = PATHS.context;
  let taxonomy = null;
  if (!exists(PATHS.taxonomy)) error(PATHS.taxonomy, 'Missing.');
  else {
    try {
      taxonomy = parseYaml(readText(PATHS.taxonomy));
      const list = taxonomy?.categories;
      if (!Array.isArray(list) || list.some((c) => !c?.id || !c?.label)) error(PATHS.taxonomy, '"categories" must be a list of { id, label }.');
      else if (new Set(list.map((c) => c.id)).size !== list.length) error(PATHS.taxonomy, '"categories" has a duplicate id.');
    } catch (e) {
      error(PATHS.taxonomy, `Not valid YAML (${e.message.split('\n')[0]}).`);
    }
  }
  const categoryIds = (taxonomy?.categories ?? []).map((c) => c.id);

  // Every plugin and prompt has a page. The value is the kind of page.
  // Skills have no page: their plugin page lists them under "skills".
  const expectedPages = new Map();
  const pluginSkills = new Map();
  for (const p of plugins) {
    expectedPages.set(contextPath.plugin(p.name), 'plugin');
    pluginSkills.set(contextPath.plugin(p.name), p.skills.map((s) => s.name));
  }
  for (const p of prompts) expectedPages.set(contextPath.prompt(p.name), 'prompt');

  // Only pages and their assets live here, in the same shape as plugins/ and prompts/.
  const allowed = [
    /^README\.md$/,
    /^taxonomy\.yml$/,
    /^plugins\/[^/]+\/index\.md$/,
    /^plugins\/[^/]+\/assets\/.+$/,
    /^prompts\/[^/]+\/index\.md$/,
    /^prompts\/[^/]+\/assets\/.+$/,
  ];
  for (const e of walk(ctx)) {
    const f = `${ctx}/${e.path}`;
    if (e.type === 'symlink') error(f, 'Symbolic links are not allowed.');
    if (e.type !== 'file') continue;
    if (path.basename(e.path).toLowerCase() === 'skill.md') {
      error(f, 'Website pages are named index.md. A SKILL.md here would be picked up as an installable skill.');
      continue;
    }
    if (/^plugins\/[^/]+\/skills\//.test(e.path)) {
      error(f, 'Skills have no page of their own. Describe the skill in the "skills" list of its plugin page, plugins/<plugin>/index.md.');
      continue;
    }
    if (!allowed.some((re) => re.test(e.path))) {
      error(f, 'Unexpected file. Pages are plugins/<plugin>/index.md or prompts/<prompt>/index.md, and images go in an assets/ folder next to the page.');
      continue;
    }
    if (e.path.endsWith('/index.md') && !expectedPages.has(f)) {
      error(f, e.path.startsWith('prompts/')
        ? 'This page has no matching prompt. Add prompts/<prompt>.md with the same name as the folder, or remove the page.'
        : 'This page has no matching plugin in plugins/. Check the folder name, or remove the page.');
    }
    if (e.path.includes('/assets/') && fs.statSync(abs(f)).size > 2 * MB) warn(f, 'Image is over 2 MB. Compress it before adding it.');
  }

  const titles = new Map();
  for (const [page, kind] of expectedPages) {
    if (!exists(page)) {
      error(page, 'Missing website page. Copy one from docs/templates/ and fill it in.');
      continue;
    }
    const text = readText(page);
    if (text.includes(PLACEHOLDER)) error(page, `Replace every "${PLACEHOLDER}: ...]]" placeholder with real text.`);
    const { data, body, error: fmError } = parseFrontmatter(text);
    if (fmError) {
      error(page, `Frontmatter problem: ${fmError}.`);
      continue;
    }
    validatePage(page, kind, data, body, { categoryIds, skillNames: pluginSkills.get(page), error, warn });
    if (typeof data.title === 'string') {
      if (titles.has(data.title)) warn(page, `The title "${data.title}" is also used by ${titles.get(data.title)}.`);
      titles.set(data.title, page);
    }
  }
}

function validatePage(page, kind, d, body, { categoryIds, skillNames, error, warn }) {
  const dir = path.posix.dirname(page);
  const keys = Object.keys(PAGE_KEYS).filter((k) => !PAGE_KEYS[k].kinds || PAGE_KEYS[k].kinds.includes(kind));
  for (const k of Object.keys(d)) {
    if (k in PAGE_KEYS && !keys.includes(k)) error(page, `"${k}" is only for ${PAGE_KEYS[k].kinds.join(' and ')} pages.`);
    else if (!(k in PAGE_KEYS)) error(page, `Unknown field "${k}". Check the spelling. Allowed fields: ${keys.join(', ')}.`);
  }
  for (const k of keys) {
    if (PAGE_KEYS[k].required && (d[k] === undefined || d[k] === null || d[k] === '')) error(page, `"${k}" is required.`);
  }
  // The card shows the reader's problem in place of the first example.
  if (typeof d.problem === 'string' && d.problem.length > 70) error(page, `"problem" is ${d.problem.length} characters. The limit is 70.`);
  const str = (k, max) => {
    if (d[k] === undefined || d[k] === null) return;
    if (typeof d[k] !== 'string') return error(page, `"${k}" must be text.`);
    if (max && d[k].length > max) warn(page, `"${k}" is ${d[k].length} characters. Keep it under ${max}.`);
  };
  str('title', 60);
  str('problem');
  str('summary', 160);
  str('description', 160);
  str('output', 80);

  const list = (k, allowedIds, label) => {
    if (d[k] === undefined) return;
    if (!Array.isArray(d[k]) || d[k].some((v) => typeof v !== 'string')) return error(page, `"${k}" must be a list, for example [${allowedIds?.[0] ?? 'one'}, ${allowedIds?.[1] ?? 'two'}].`);
    if (allowedIds) {
      for (const v of d[k]) {
        if (!allowedIds.includes(v)) error(page, `"${k}" uses "${v}", which is not in ${PATHS.taxonomy}. Use one of: ${allowedIds.join(', ')}. To add a new ${label}, add it to that file.`);
      }
    }
  };
  list('categories', categoryIds, 'category');
  if (Array.isArray(d.categories) && !d.categories.length) error(page, '"categories" needs at least one category.');
  list('tags');
  if (Array.isArray(d.tags)) {
    for (const t of d.tags) if (typeof t === 'string' && !NAME_RE.test(t)) error(page, `Tag "${t}" must be lowercase words joined by hyphens, such as "ai-search".`);
    if (d.tags.length > 8) warn(page, `${d.tags.length} tags. Keep it to 8 or fewer.`);
  }
  for (const k of ['featured', 'draft']) {
    if (d[k] !== undefined && typeof d[k] !== 'boolean') error(page, `"${k}" must be true or false.`);
  }

  if (d.requirements !== undefined) {
    if (!Array.isArray(d.requirements)) error(page, '"requirements" must be a list.');
    else d.requirements.forEach((r, n) => {
      if (typeof r?.name !== 'string') error(page, `"requirements" item ${n + 1} needs a "name".`);
      if (typeof r?.required !== 'boolean') error(page, `"requirements" item ${n + 1} needs "required: true" or "required: false".`);
      for (const k of Object.keys(r ?? {})) if (!['name', 'required', 'details'].includes(k)) error(page, `"requirements" item ${n + 1} has an unknown field "${k}".`);
    });
  }
  if (d.examples !== undefined) {
    if (!Array.isArray(d.examples)) error(page, '"examples" must be a list.');
    else d.examples.forEach((x, n) => {
      if (typeof x?.prompt !== 'string') error(page, `"examples" item ${n + 1} needs a "prompt".`);
      for (const k of Object.keys(x ?? {})) if (!['prompt', 'note'].includes(k)) error(page, `"examples" item ${n + 1} has an unknown field "${k}".`);
    });
  }
  if (!d.examples?.length) warn(page, 'Add at least one item to "examples". The website shows them as prompts visitors can copy.');

  if (d.customize !== undefined && kind === 'plugin') {
    const c = d.customize;
    if (typeof c !== 'object' || c === null || Array.isArray(c)) error(page, '"customize" must have a "note" and an optional "prompt".');
    else {
      if (typeof c.note !== 'string' || !c.note.trim()) error(page, '"customize" needs a "note".');
      if (c.prompt !== undefined && typeof c.prompt !== 'string') error(page, '"customize.prompt" must be text.');
      for (const k of Object.keys(c)) if (!['prompt', 'note'].includes(k)) error(page, `"customize" has an unknown field "${k}".`);
    }
  }

  if (kind === 'plugin' && !d.requirements?.length) warn(page, 'Add "requirements". The website shows them on the Install tab and as chips on the card.');

  // One entry per skill, in the order the website lists them in the plugin's panel.
  if (kind === 'plugin' && d.skills != null) {
    const listed = d.skills;
    if (!Array.isArray(listed) || listed.some((x) => typeof x !== 'object' || x === null || Array.isArray(x))) {
      error(page, `"skills" must be a list with one item per skill (${skillNames.join(', ')}), each with "name", "title", "summary", "output" and "example".`);
    } else {
      const names = listed.map((x) => x.name);
      for (const s of skillNames) if (!names.includes(s)) error(page, `"skills": add an item for "${s}".`);
      listed.forEach((x, n) => {
        const at = `"skills" item ${n + 1}${typeof x.name === 'string' ? ` (${x.name})` : ''}`;
        if (typeof x.name !== 'string') error(page, `${at} needs a "name", the skill's folder name.`);
        else if (!skillNames.includes(x.name)) error(page, `${at}: "${x.name}" is not a skill in this plugin.`);
        for (const k of ['title', 'summary']) if (typeof x[k] !== 'string' || !x[k].trim()) error(page, `${at} needs a "${k}".`);
        for (const k of ['output', 'example']) {
          if (x[k] === undefined) warn(page, `${at} has no "${k}". The website's hero demo only plays skills with an example and an output.`);
          else if (typeof x[k] !== 'string') error(page, `${at}: "${k}" must be text.`);
        }
        if (x.title?.length > 60) warn(page, `${at}: "title" is ${x.title.length} characters. Keep it under 60.`);
        if (x.summary?.length > 160) warn(page, `${at}: "summary" is ${x.summary.length} characters. Keep it under 160.`);
        if (x.output?.length > 80) warn(page, `${at}: "output" is ${x.output.length} characters. Keep it under 80.`);
        for (const k of Object.keys(x)) if (!SKILL_ENTRY_KEYS.includes(k)) error(page, `${at} has an unknown field "${k}". Allowed: ${SKILL_ENTRY_KEYS.join(', ')}.`);
      });
      if (new Set(names).size !== names.length) error(page, '"skills" lists the same skill twice.');
    }
  }

  if (d.image !== undefined && (typeof d.image !== 'string' || !insideAndExists(dir, d.image, PATHS.context))) {
    error(page, `"image" points to "${d.image}", which does not exist inside library-context/.`);
  }
  for (const l of relativeLinks(body)) {
    if (!insideAndExists(dir, l.clean, PATHS.context)) error(page, `Link or image "${l.target}" does not exist inside library-context/.`);
  }

  const { sections } = splitSections(body);
  const norm = (h) => h.toLowerCase().replace(/’/g, "'");
  const headings = sections.map((s) => norm(s.heading));
  for (const h of REQUIRED_SECTIONS) if (!headings.includes(norm(h))) error(page, `Add a "## ${h}" section.`);
  for (const s of sections) {
    if (!SECTIONS.map(norm).includes(norm(s.heading))) error(page, `"## ${s.heading}" isn't a section the website shows. Use ${SECTIONS.map((h) => `"## ${h}"`).join(', ')}, or make it a "### " heading inside one.`);
  }
  for (const s of sections) if (!s.markdown) warn(page, `The "## ${s.heading}" section is empty.`);
  if (/^#\s/m.test(body.replace(/```[\s\S]*?```/g, ''))) warn(page, 'Use "## " for section headings. The page title comes from "title".');
}

// ---------------------------------------------------------------- helpers

function loadJson(rel, error) {
  if (!exists(rel)) return error(rel, 'Missing.'), null;
  try {
    return readJson(rel);
  } catch (e) {
    return error(rel, `Not valid JSON (${e.message}). Check for a missing comma or quote.`), null;
  }
}

function indexEntries(list, file, error) {
  const map = new Map();
  for (const e of Array.isArray(list) ? list : []) {
    if (!e?.name) error(file, 'Every plugin entry needs a "name".');
    else if (map.has(e.name)) error(file, `Plugin "${e.name}" is listed twice.`);
    else map.set(e.name, e);
  }
  return map;
}

// True when `target`, relative to `fromDir`, exists and stays inside `root` (default: fromDir).
function insideAndExists(fromDir, target, root = fromDir) {
  const resolved = path.posix.normalize(path.posix.join(fromDir, target.replace(/^\.\//, '')));
  const base = path.posix.normalize(root);
  if (resolved !== base && !resolved.startsWith(`${base}/`)) return false;
  return exists(resolved);
}

export function report({ errors, warnings }) {
  // In GitHub Actions, also annotate the files so problems show on the pull request.
  if (process.env.GITHUB_ACTIONS) {
    const esc = (v) => v.replace(/%/g, '%25').replace(/\r/g, '%0D').replace(/\n/g, '%0A');
    for (const { file, msg } of warnings) console.log(`::warning file=${file},title=Library check::${esc(msg)}`);
    for (const { file, msg } of errors) console.log(`::error file=${file},title=Library check::${esc(msg)}`);
  }
  const fmt = (items, mark) => items.map(({ file, msg }) => `  ${mark} ${file}\n      ${msg}`).join('\n');
  if (warnings.length) console.log(`\nWarnings (${warnings.length}). These don't block merging, but please check them:\n${fmt(warnings, '!')}`);
  if (errors.length) console.log(`\nErrors (${errors.length}). These must be fixed before merging:\n${fmt(errors, '✖')}`);
}

if (import.meta.url === pathToFileURL(process.argv[1]).href) {
  const result = validate();
  report(result);
  const skillCount = result.plugins.reduce((n, p) => n + p.skills.length, 0);
  if (result.errors.length) {
    console.log(`\nValidation failed: ${result.errors.length} error(s).`);
    process.exit(1);
  }
  console.log(`\n✔ Valid: ${result.plugins.length} plugin(s), ${skillCount} skill(s), ${result.prompts.length} prompt(s), ${result.warnings.length} warning(s).`);
}
