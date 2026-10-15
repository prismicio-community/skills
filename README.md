# Prismic AI library

Free plugins and skills from Prismic for Claude, ChatGPT, and other AI assistants. Browse them in the library on the Prismic website, or install them straight from this repository. <!-- TODO: link the library page once it is live. -->

- A **skill** is a folder of instructions and supporting files that teaches an assistant one workflow, such as writing meta descriptions.
- A **plugin** bundles one or more related skills so you can install them together.

> [!NOTE]
> **Looking for the official Prismic skill?** It lives in [prismicio/skills](https://github.com/prismicio/skills), and it's the one the Prismic documentation recommends. It helps an assistant build and manage Prismic projects: content models, slices, and content, through the Prismic CLI and MCP server.
>
> This repository is separate. It holds skills from Prismic for general website and content work, such as SEO, and these are the skills Prismic's marketing content links to. Assistants working on a Prismic project's code, models, or content should use `prismicio/skills`.
>
> ```
> npx skills add --global prismicio/skills
> ```

## Install

Choose the option that matches how you work. Each one installs the same skills.

### Add the whole marketplace (Claude and ChatGPT)

Adding the marketplace shows you every plugin in this repository. You then choose which plugins to install. Adding it installs nothing by itself.

**Claude (web, desktop, and Cowork)**

1. Go to **Customize → Plugins**, select **Add**, then **Add marketplace**.
2. Enter `https://github.com/prismicio-community/skills`.
3. Open the marketplace and select **Install** on the plugins you want.

**Claude Code**

```
/plugin marketplace add prismicio-community/skills
/plugin install <plugin>@prismic-community
```

**ChatGPT and Codex**

In a ChatGPT workspace, an admin adds the marketplace under **Admin → Plugins → Import marketplace** with the repository URL `https://github.com/prismicio-community/skills`. Members then install the plugins they want.

With the Codex command line:

```
codex plugin marketplace add prismicio-community/skills
codex plugin add <plugin>@prismic-community
```

### Install one skill with the skills CLI

The [skills CLI](https://skills.sh) installs single skills into Claude Code, Codex, Cursor, and many other agents. It finds skills inside every plugin in this repository.

```
npx skills add prismicio-community/skills --list
npx skills add prismicio-community/skills --skill <skill>
```

Add `--global` to install for your user instead of the current project, and `--agent claude-code` (or `codex`, `cursor`, ...) to skip the agent picker.

### Download the files

Every skill and plugin is available as a file on the [library downloads release](https://github.com/prismicio-community/skills/releases/tag/library). The library page links to the same files.

| File | What to do with it |
| --- | --- |
| `<skill>.zip` | **Claude:** go to **Customize → Skills**, select **+**, then **Upload a skill**. Don't rename the zip or the folder inside it. **Claude Code:** unzip it into `~/.claude/skills/`. **Codex:** unzip it into `~/.agents/skills/`. |
| `<plugin>.plugin` | **Claude:** go to **Customize → Plugins**, select **Add**, then **Upload plugin**. |

## Update

| How you installed | How to update |
| --- | --- |
| Marketplace in Claude | Open the marketplace and select **Check for updates**, or turn on **Sync automatically**. |
| Marketplace in Claude Code | Run `/plugin marketplace update prismic-community`, or turn on auto-update for the marketplace in `/plugin` → **Marketplaces**. Run `/reload-plugins` to apply updates to a running session. |
| Marketplace in ChatGPT | Workspace marketplaces sync once a day. An admin can select **Sync now**. |
| Marketplace in Codex | Run `codex plugin marketplace upgrade prismic-community`. If a plugin doesn't change, run `codex plugin add <plugin>@prismic-community` again. |
| skills CLI | Run `npx skills update`. |
| Downloaded file | Download the file again and upload or unzip it in place of the old one. |

Every change merged into `main` is a new release. There are no version numbers to track.

## What's in this repository

```
.claude-plugin/marketplace.json     Marketplace for Claude, Claude Code, and the skills CLI
.agents/plugins/marketplace.json    Marketplace for ChatGPT and Codex
plugins/<plugin>/                   One installable plugin
  .codex-plugin/plugin.json         Plugin details for ChatGPT and Codex
  assets/                           The plugin icon
  skills/<skill>/                   One installable skill
    SKILL.md                        Instructions the assistant follows
    references/, assets/, scripts/  Files the skill uses while it works
library-context/                    Library page content (not installed)
  taxonomy.yml                      Allowed categories and platforms
  plugins/<plugin>/index.md         Plugin page
  plugins/<plugin>/skills/<skill>/index.md   Skill page
docs/                               Templates and the website data format
scripts/                            Validation and packaging
```

Plugins and skills contain only what an assistant needs. Text and images for the library page live in `library-context/`, which mirrors the `plugins/` folder and is never installed.

## Contribute

Anyone at Prismic can add or update a plugin, skill, or library page through a pull request, including from the GitHub website without installing anything. See [CONTRIBUTING.md](CONTRIBUTING.md).

Maintainers and coding agents: see [AGENTS.md](AGENTS.md) for the repository rules and [docs/website-integration.md](docs/website-integration.md) for the data the library page uses.

## License

[MIT](LICENSE)
