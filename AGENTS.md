# Working on this repo

Public, agent-agnostic plugins and skills, plus copy-and-paste prompts, distributed five ways:

- **Claude and Claude Code:** the marketplace in `.claude-plugin/marketplace.json`.
- **ChatGPT and Codex:** the marketplace in `.agents/plugins/marketplace.json`.
- **skills CLI (skills.sh):** reads `.claude-plugin/marketplace.json` to find the skills nested in each plugin.
- **Downloads:** `npm run build` packages each skill as `<skill>.zip`, each plugin as `<plugin>.plugin`, and copies each prompt as `<prompt>.md`. CI publishes them with `library.json` to the rolling GitHub release named in `package.json` (`library.releaseTag`).
- **Copy and paste:** the website shows each prompt in `prompts/` with a Copy button. Nothing is installed.

This repository is `prismicio-community/skills`. It's separate from the official `prismicio/skills`, which the Prismic docs reference for building with Prismic. Don't add skills here that overlap with it, or reuse its skill names (such as `prismic`).

All canonical skills live under `plugins/<plugin>/skills/<skill>/`. Both marketplaces point each plugin at the same package directory, `./plugins/<plugin>`. Prompts live in `prompts/<prompt>.md`. Website content lives in `library-context/`, which mirrors `plugins/` and `prompts/`.

Run `npm run check` before you finish any change. It validates, builds, and verifies the packages. Run `npm run check:discovery` after you change marketplace files, package layout, or scripts.

## Rules

1. **Never set `version` in Claude marketplace entries.** With no version, the git commit SHA is the version: every push to `main` is a new release that auto-updating clients pick up. Users enable auto-update per marketplace and apply updates in a running session with `/reload-plugins`. The `.codex-plugin/plugin.json` manifests are a different contract and require a strict semver `version`. Keep them at `0.1.0` unless a package versioning policy is introduced. The generated `.claude-plugin/plugin.json` in downloads copies that version.

2. **No `.claude-plugin/plugin.json` inside `plugins/<plugin>/`.**
   - Marketplace entries use `"strict": false` with a `skills` list, so the entry is the manifest.
   - Adding a plugin.json makes Claude Code fail with conflicting manifests.
   - The build generates one inside each `.plugin` download, because Claude's plugin upload requires it.

3. **Skill names are unique across all plugins.** The skills CLI keeps only the first skill with a given name, and installs land in `.claude/skills/<name>/`.

4. **Skills are agent-agnostic.** Name capabilities, never client-specific tool ids (no `mcp__*`), and no harness-specific features ("Edit tool"). Platform syntax (Slack filters, `gh`/`git` CLIs) is fine.

5. **Skills never mention plugins.** Plugins are the distribution layer. Skills reference sibling skills by bare skill name. "Install X alongside Y" guidance belongs in library pages and marketplace descriptions only.

6. **Plugins are named after the capability**, such as `seo-basics`, never after an audience or team.

7. **Frontmatter descriptions are routing-only.** Say what the skill does, give trigger phrases, and disambiguate from sibling skills. Target 450 characters or fewer. Process detail goes in the body.

8. **Skills must not assume filesystem access for user data.** The agent may be connector-only, with no shell or local repo. User content lives behind connectors, and skills read and write it there. A skill's own bundled scripts are the exception: running them requires a shell-capable client, so say so in the skill's Compatibility section.

9. **Packages contain only what an agent needs.**
   - `plugins/<plugin>/` holds `.codex-plugin/`, `assets/` (the plugin icon), and `skills/`.
   - A skill holds `SKILL.md` plus the `references/`, `assets/` (templates the agent fills in), and `scripts/` it uses.
   - Card copy, screenshots, cover images, and install instructions belong in `library-context/`.
   - No README files inside skills.

10. **Every plugin, skill, and prompt has a library page** at `library-context/plugins/<plugin>/index.md`, `library-context/plugins/<plugin>/skills/<skill>/index.md`, or `library-context/prompts/<prompt>/index.md`. Its frontmatter schema is in `library-context/README.md` and enforced by `scripts/validate.mjs`. Keep the two in sync. New pages start as `draft: true`. `draft` hides a page from the website only; merged skills are installable immediately.

11. **Public content only.** This repository is public. No customer names without approval, no internal URLs, credentials, tokens, or internal-only process. Don't copy content from internal repositories without checking it is meant to be public.

12. **Plugin-local skills are canonical.** Edit skills only under `plugins/<plugin>/skills/<skill>/`. Don't create a top-level `skills/` directory or a root `SKILL.md`. Either would change what the skills CLI discovers.

13. **A prompt is one Markdown file that visitors copy exactly as written.**
    - It lives at `prompts/<prompt>.md`. There are no folders, no frontmatter, and no other files in `prompts/`. Card fields and page text go in its library page.
    - Use a prompt when the user pastes the work into a chat once, such as a prompt that builds a dashboard. Use a skill when an assistant should pick the work up again and again.
    - A prompt may rely on one assistant's features, such as Claude artifacts. Its page must list where it works in `platforms`. Rules 4 and 8 still apply where they can: name connectors by what they are, and read user data through connectors.
    - Prompts aren't in either marketplace, and the skills CLI must not find them. Never add a `SKILL.md` to `prompts/`.

## Changing the repository name or marketplace name

- The repository slug lives in `package.json` (`library.repository`), the `repository` field of each `.codex-plugin/plugin.json`, and the install commands in `README.md` and `docs/website-integration.md`.
- The marketplace name lives in `name` in both marketplace files.
- Update every place together.
