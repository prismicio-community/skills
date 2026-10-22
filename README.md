# Prismic AI library

Free plugins, skills, and prompts from Prismic for Claude, ChatGPT, and other AI assistants. Browse them in the library on the Prismic website, or install them straight from this repository. <!-- TODO: link the library page once it is live. -->

- A **skill** is a folder of instructions and supporting files that teaches an assistant one workflow, such as writing meta descriptions.
- A **plugin** bundles one or more related skills so you can install them together.
- A **prompt** is a single message you copy and paste into a chat, such as one that builds a dashboard. There's nothing to install. Copy it from the library page or from [`prompts/`](prompts/).

> [!NOTE]
> **Building a Prismic project?** Use the official Prismic skill in [prismicio/skills](https://github.com/prismicio/skills) instead. The Prismic documentation recommends it, and it helps your assistant work with content models, slices, and content. The skills here are for general website and content work, such as SEO.
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

Every plugin and prompt is available as a file on the [library downloads release](https://github.com/prismicio-community/skills/releases/tag/library). The library page links to the same files.

| File | What to do with it |
| --- | --- |
| `<plugin>.zip` | **Claude:** go to **Customize → Plugins**, select **Add**, then **Upload plugin**. **ChatGPT:** upload it as a new plugin under **Plugins**. In a workspace, you need upload permission or an admin role. Don't unzip it first. |
| `<prompt>.md` | Open it, copy everything, and paste it into a new chat. |

## Update

| How you installed | How to update |
| --- | --- |
| Marketplace in Claude | Open the marketplace and select **Check for updates**, or turn on **Sync automatically**. |
| Marketplace in Claude Code | Run `/plugin marketplace update prismic-community`, or turn on auto-update for the marketplace in `/plugin` → **Marketplaces**. Run `/reload-plugins` to apply updates to a running session. |
| Marketplace in ChatGPT | Workspace marketplaces sync once a day. An admin can select **Sync now**. |
| Marketplace in Codex | Run `codex plugin marketplace upgrade prismic-community`. If a plugin doesn't change, run `codex plugin add <plugin>@prismic-community` again. |
| skills CLI | Run `npx skills update`. |
| Downloaded file | Download the file again and upload or unzip it in place of the old one. |
| Prompt | Copy the prompt again. Anything it already built keeps working as it is. |

Updates ship as soon as they are merged. There are no version numbers to track.

## Contribute

To suggest a change or add a skill or prompt, see [CONTRIBUTING.md](CONTRIBUTING.md).

## License

[MIT](LICENSE)
