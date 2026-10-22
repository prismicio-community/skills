#!/usr/bin/env node
// Checks the repo with the real tools users install from:
//   1. skills CLI: lists every skill and no prompt, and installs one skill with its exact files.
//   2. Claude Code: validates the marketplace and each plugin download,
//      then adds the marketplace and installs every plugin.
//   3. Codex: adds the marketplace and installs every plugin.
// Every tool runs with a throwaway home directory, so your own setup is untouched.
// Tools that aren't installed are reported as SKIPPED, never as passed.
// Needs network access for npx. Run "npm run build" first.
// Run with: npm run check:discovery
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import { ROOT, PATHS, abs, exists, readJson, walkFiles, loadPlugins, loadPrompts } from './lib/repo.mjs';
import { readZip } from './lib/zip.mjs';

const SKILLS_CLI = 'skills@1.7.2';

const results = [];
const record = (status, name, detail = '') => results.push({ status, name, detail });
const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'library-discovery-'));
const plugins = loadPlugins();
const skills = plugins.flatMap((p) => p.skills);
const prompts = loadPrompts().filter((p) => p.isPrompt);
const marketplace = readJson(PATHS.claudeMarketplace).name;

function run(cmd, args, { env = {}, cwd = tmp } = {}) {
  const r = spawnSync(cmd, args, {
    cwd,
    env: { ...process.env, DISABLE_TELEMETRY: '1', DO_NOT_TRACK: '1', ...env },
    input: '',
    encoding: 'utf8',
    timeout: 180_000,
  });
  const out = `${r.stdout ?? ''}${r.stderr ?? ''}`.replace(/\x1b\[[0-9;]*[A-Za-z]/g, '');
  return { ok: r.status === 0, out, missing: r.error?.code === 'ENOENT' };
}
const has = (cmd) => !run(cmd, ['--version']).missing;
const tail = (s) => s.trim().split('\n').slice(-8).join('\n');

// ---------------------------------------------------------------- skills CLI
if (!skills.length) record('SKIPPED', 'skills CLI', 'the repository has no skills yet');
else {
  const home = fs.mkdtempSync(path.join(tmp, 'skills-home-'));
  const list = run('npx', ['-y', SKILLS_CLI, 'add', ROOT, '--list'], { env: { HOME: home } });
  if (!list.ok) record('FAIL', 'skills CLI --list', tail(list.out));
  else {
    const listed = (name) => new RegExp(`^[\\s│]*${name}\\s*$`, 'm').test(list.out);
    const missing = skills.filter((s) => !listed(s.name));
    // Prompts are copied, not installed, so the skills CLI must not offer them.
    const leaked = prompts.filter((p) => listed(p.name) && !skills.some((s) => s.name === p.name));
    const count = Number(list.out.match(/Found (\d+) skill/)?.[1]);
    if (missing.length) record('FAIL', 'skills CLI --list', `not listed: ${missing.map((s) => s.name).join(', ')}`);
    else if (leaked.length) record('FAIL', 'skills CLI --list', `prompts listed as skills: ${leaked.map((p) => p.name).join(', ')}`);
    else if (count !== skills.length) record('FAIL', 'skills CLI --list', `found ${count}, expected ${skills.length}`);
    else record('PASS', 'skills CLI --list', `${count} skill(s) found`);
  }

  // Install the first skill into an empty project and compare files.
  const skill = skills[0];
  const proj = fs.mkdtempSync(path.join(tmp, 'skills-proj-'));
  const add = run('npx', ['-y', SKILLS_CLI, 'add', ROOT, '--skill', skill.name, '--agent', 'claude-code', '-y'], { cwd: proj, env: { HOME: home } });
  const installed = path.join(proj, '.claude/skills', skill.name);
  if (!add.ok || !fs.existsSync(installed)) record('FAIL', `skills CLI install ${skill.name}`, tail(add.out));
  else {
    const got = listFiles(installed);
    const want = walkFiles(skill.dir);
    const same = got.length === want.length && want.every((f, i) => got[i] === f
      && fs.readFileSync(path.join(installed, f)).equals(fs.readFileSync(abs(`${skill.dir}/${f}`))));
    record(same ? 'PASS' : 'FAIL', `skills CLI install ${skill.name}`, same ? `${got.length} file(s), identical to source` : `got ${got.join(', ')}`);
  }
}

// ---------------------------------------------------------------- Claude Code
if (!has('claude')) record('SKIPPED', 'Claude Code', '"claude" is not installed');
else {
  const env = { CLAUDE_CONFIG_DIR: fs.mkdtempSync(path.join(tmp, 'claude-')) };
  // An empty marketplace is only a warning, which --strict would turn into a failure.
  const v = run('claude', ['plugin', 'validate', ROOT, ...(plugins.length ? ['--strict'] : [])], { env });
  record(v.ok ? 'PASS' : 'FAIL', 'claude plugin validate (marketplace)', v.ok ? '' : tail(v.out));

  for (const p of plugins) {
    const file = `${PATHS.dist}/plugins/${p.name}.zip`;
    if (!exists(file)) {
      record('FAIL', `claude plugin validate ${p.name}.zip`, 'not built; run "npm run build" first');
      continue;
    }
    const dir = fs.mkdtempSync(path.join(tmp, 'unpacked-'));
    for (const [name, bytes] of Object.entries(readZip(abs(file)))) {
      fs.mkdirSync(path.join(dir, path.dirname(name)), { recursive: true });
      fs.writeFileSync(path.join(dir, name), bytes);
    }
    // The archive holds the plugin's files at its root.
    const pv = run('claude', ['plugin', 'validate', dir, '--strict'], { env });
    record(pv.ok ? 'PASS' : 'FAIL', `claude plugin validate ${p.name}.zip`, pv.ok ? '' : tail(pv.out));
  }

  const add = run('claude', ['plugin', 'marketplace', 'add', ROOT], { env });
  record(add.ok ? 'PASS' : 'FAIL', 'claude plugin marketplace add', add.ok ? '' : tail(add.out));
  for (const p of plugins) {
    const inst = run('claude', ['plugin', 'install', `${p.name}@${marketplace}`], { env });
    const details = run('claude', ['plugin', 'details', `${p.name}@${marketplace}`], { env });
    const missing = p.skills.filter((s) => !details.out.includes(s.name));
    const ok = inst.ok && details.ok && !missing.length;
    record(ok ? 'PASS' : 'FAIL', `claude plugin install ${p.name}@${marketplace}`,
      ok ? `skills: ${p.skills.map((s) => s.name).join(', ')}` : tail(`${inst.out}\n${details.out}`));
  }
}

// ---------------------------------------------------------------- Codex
if (!has('codex')) record('SKIPPED', 'Codex', '"codex" is not installed');
else {
  const home = fs.mkdtempSync(path.join(tmp, 'codex-'));
  const env = { CODEX_HOME: home };
  const add = run('codex', ['plugin', 'marketplace', 'add', ROOT], { env });
  record(add.ok ? 'PASS' : 'FAIL', 'codex plugin marketplace add', add.ok ? '' : tail(add.out));
  for (const p of plugins) {
    const inst = run('codex', ['plugin', 'add', `${p.name}@${marketplace}`], { env });
    const root = inst.out.match(/Installed plugin root: (.+)/)?.[1]?.trim();
    const missing = root ? p.skills.filter((s) => !fs.existsSync(path.join(root, 'skills', s.name, 'SKILL.md'))) : p.skills;
    const ok = inst.ok && !missing.length;
    record(ok ? 'PASS' : 'FAIL', `codex plugin add ${p.name}@${marketplace}`,
      ok ? `skills: ${p.skills.map((s) => s.name).join(', ')}` : tail(inst.out));
  }
}

fs.rmSync(tmp, { recursive: true, force: true });

for (const r of results) console.log(`${r.status.padEnd(7)} ${r.name}${r.detail ? `\n        ${r.detail.replace(/\n/g, '\n        ')}` : ''}`);
const failed = results.filter((r) => r.status === 'FAIL').length;
const skipped = results.filter((r) => r.status === 'SKIPPED').length;
console.log(`\n${failed ? '✖' : '✔'} ${results.length - failed - skipped} passed, ${failed} failed, ${skipped} skipped.`);
if (failed) process.exit(1);

function listFiles(dir, prefix = '') {
  return fs.readdirSync(dir, { withFileTypes: true }).flatMap((e) => {
    const p = prefix ? `${prefix}/${e.name}` : e.name;
    return e.isDirectory() ? listFiles(path.join(dir, e.name), p) : [p];
  }).sort();
}
