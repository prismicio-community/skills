#!/usr/bin/env node
// Summarizes what a pull request changes about what installed skills can do:
// bundled scripts, plugin capabilities, tool permissions, network hosts,
// install commands, and the repository's own checks.
// The "Capability summary" workflow posts the result on the pull request.
// It reads the diff as data and never runs code from the pull request.
// Uses only Node built-ins, so it runs without "npm ci".
// Run with: node scripts/pr-summary.mjs <base> <head>   (default: origin/main HEAD)
import fs from 'node:fs';
import { execFileSync } from 'node:child_process';

export const MARKER = '<!-- capability-summary -->';
const MAX_ITEMS = 20;

const SCRIPT_RE = /\.(py|mjs|cjs|js|ts|sh)$/i;
const CAPABILITY_PATH_RE = /^plugins\/[^/]+\/(hooks|agents|commands)\/|^plugins\/[^/]+\/\.(mcp|app)\.json$/;
const MANIFEST_RE = /^(\.claude-plugin\/marketplace\.json|\.agents\/plugins\/marketplace\.json|plugins\/[^/]+\/\.codex-plugin\/plugin\.json)$/;
const CAPABILITY_KEY_RE = /"(hooks|mcpServers|lspServers|agents|commands|apps)"\s*:/;
const CHECKS_RE = /^(\.github\/|scripts\/|package(-lock)?\.json$)/;
const IGNORED_HOST_RE = /^((.+\.)?example\.(com|org|net)|localhost|127\.0\.0\.1|www\.w3\.org)$/;
const INSTALL_RE = /\b(pip3?\s+install|uv\s+(add|pip\s+install|tool\s+install)|uvx|pipx|npm\s+(i|install|exec)|npx|pnpm\s+(add|dlx)|yarn\s+(add|dlx)|bunx|brew\s+install|apt(-get)?\s+install|go\s+install|cargo\s+install|gem\s+install|docker\s+run|git\s+clone|curl|wget|playwright\s+install)\b/i;

const git = (...args) => execFileSync('git', ['-c', 'core.quotePath=false', ...args], { encoding: 'utf8', maxBuffer: 64 * 1024 * 1024, stdio: ['ignore', 'pipe', 'pipe'] });

export function summarize(base, head) {
  const range = `${base}...${head}`;

  // Changed files, with renames as their new path.
  const parts = git('diff', '--name-status', '-z', '--find-renames', range).split('\0').filter(Boolean);
  const files = [];
  for (let i = 0; i < parts.length; ) {
    const status = parts[i++];
    if (status.startsWith('R') || status.startsWith('C')) {
      i++;
      files.push({ status: 'renamed', path: parts[i++] });
    } else files.push({ status: { A: 'added', M: 'changed', D: 'deleted', T: 'changed' }[status[0]] ?? 'changed', path: parts[i++] });
  }

  // Added and removed lines per file, for shipped content and manifests.
  const added = new Map();
  const removed = new Map();
  let current = null;
  for (const line of git('diff', '-U0', '--no-color', '--no-ext-diff', range).split('\n')) {
    if (line.startsWith('+++ ')) current = line === '+++ /dev/null' ? null : line.slice(6);
    else if (line.startsWith('--- ')) continue;
    else if (current && line.startsWith('+')) push(added, current, line.slice(1));
    else if (current && line.startsWith('-')) push(removed, current, line.slice(1));
  }

  const sections = [];
  const section = (title, why, items) => items.length && sections.push({ title, why, items });

  section('Bundled scripts', 'Code that agents run on the user\'s machine. Read it in full.',
    files.filter((f) => f.path.startsWith('plugins/') && (SCRIPT_RE.test(f.path) || f.path.includes('/scripts/')))
      .map((f) => `${f.status} ${code(f.path)}`));

  const capabilities = files.filter((f) => CAPABILITY_PATH_RE.test(f.path)).map((f) => `${f.status} ${code(f.path)}`);
  for (const [f, lines] of [...added, ...removed]) {
    if (!MANIFEST_RE.test(f)) continue;
    for (const l of lines) if (CAPABILITY_KEY_RE.test(l)) capabilities.push(`${code(f)}: ${code(l.trim())}`);
  }
  section('Plugin capabilities', 'Hooks, MCP servers, agents, and commands run or load without a skill asking.', unique(capabilities));

  const tools = [];
  for (const [f, lines] of [...added, ...removed]) {
    if (!f.endsWith('/SKILL.md')) continue;
    for (const l of lines) if (/^\s*allowed-tools\s*:/.test(l)) tools.push(`${code(f)}: ${code(l.trim())}`);
  }
  section('Tool permissions', 'allowed-tools lets a skill use tools without asking the user.', unique(tools));

  // Skill and prompt text only. Manifest links (websiteURL and so on) are for people.
  const hosts = new Map();
  for (const [f, lines] of added) {
    if (!/^(plugins\/[^/]+\/skills|prompts)\//.test(f)) continue;
    let before = '';
    try {
      before = git('show', `${base}:${f}`).toLowerCase();
    } catch {}
    for (const l of lines) {
      for (const [, host] of l.matchAll(/\bhttps?:\/\/([A-Za-z0-9.-]+\.[A-Za-z]{2,})/g)) {
        const h = host.toLowerCase();
        if (IGNORED_HOST_RE.test(h) || before.includes(`//${h}`)) continue;
        if (!hosts.has(h)) hosts.set(h, new Set());
        hosts.get(h).add(f);
      }
    }
  }
  section('New hosts', 'Sites that skills or scripts now point the agent at. Check each one is expected.',
    [...hosts].map(([h, fs]) => `${code(h)} in ${[...fs].map(code).join(', ')}`));

  const installs = [];
  for (const [f, lines] of added) {
    if (!/^(plugins\/[^/]+\/skills|prompts)\//.test(f)) continue;
    for (const l of lines) if (INSTALL_RE.test(l)) installs.push(`${code(f)}: ${code(l.trim())}`);
  }
  section('Install and download commands', 'New packages or downloads an agent may fetch.', unique(installs));

  section('Repository checks and CI', 'Changes to the workflows, validation rules, or dependencies that guard everything above.',
    files.filter((f) => CHECKS_RE.test(f.path)).map((f) => `${f.status} ${code(f.path)}`));

  return { notable: sections.length > 0, markdown: render(sections) };
}

function render(sections) {
  const out = [MARKER, '### Capability summary', ''];
  if (!sections.length) {
    out.push('Nothing in this pull request changes bundled scripts, plugin capabilities, tool permissions, network hosts, install commands, or the repository\'s checks.');
    return out.join('\n') + '\n';
  }
  out.push('This pull request changes what installed skills can do. Everything below ships to auto-updating installs as soon as it merges, so review it before approving.', '');
  for (const s of sections) {
    out.push(`**${s.title}.** ${s.why}`, '');
    for (const item of s.items.slice(0, MAX_ITEMS)) out.push(`- ${item}`);
    if (s.items.length > MAX_ITEMS) out.push(`- …and ${s.items.length - MAX_ITEMS} more`);
    out.push('');
  }
  out.push('The **Validate** check enforces the hard rules. This summary only points out what needs a human look.');
  return out.join('\n') + '\n';
}

function push(map, key, value) {
  if (!map.has(key)) map.set(key, []);
  map.get(key).push(value);
}

const unique = (items) => [...new Set(items)];

// Text from the pull request goes in code spans, so it can't add links, mentions, or formatting.
function code(text) {
  const t = text.length > 160 ? `${text.slice(0, 157)}...` : text;
  return `\`${t.replace(/`/g, "'").replace(/[\r\n]/g, ' ')}\``;
}

if (process.argv[1] && import.meta.url === new URL(`file://${process.argv[1]}`).href) {
  const [base = 'origin/main', head = 'HEAD'] = process.argv.slice(2);
  const { notable, markdown } = summarize(base, head);
  process.stdout.write(markdown);
  if (process.env.GITHUB_OUTPUT) fs.appendFileSync(process.env.GITHUB_OUTPUT, `notable=${notable}\n`);
}
