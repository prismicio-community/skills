# Website integration

The library page on the Prismic website reads one file: `library.json`. Every push to `main` rebuilds it, along with the downloads, and publishes them to a rolling GitHub release:

```
https://github.com/prismicio-community/skills/releases/download/library/library.json
https://github.com/prismicio-community/skills/releases/download/library/<plugin>.zip
https://github.com/prismicio-community/skills/releases/download/library/<prompt>.md
```

These URLs never change. Fetch `library.json` when the website builds, not from the browser. GitHub release downloads redirect and don't send CORS headers.

To build the same file locally, run `npm run build`. It writes to `dist/library.json`.

## library.json

```jsonc
{
  "schemaVersion": 2,
  "commit": "3f9c…",                         // the commit it was built from
  "repository": { "slug": "prismicio-community/skills", "url": "https://github.com/prismicio-community/skills", "branch": "main" },
  "marketplace": {
    "name": "prismic-community",
    "displayName": "Prismic Community",
    "url": "https://github.com/prismicio-community/skills",   // what users paste into Claude or ChatGPT
    "install": {
      "claudeCode": "/plugin marketplace add prismicio-community/skills",
      "codex": "codex plugin marketplace add prismicio-community/skills",
      "skillsCliList": "npx skills add prismicio-community/skills --list"
    }
  },
  "taxonomy": {
    "categories": [{ "id": "seo", "label": "SEO and AI search" }],
    "platforms": [{ "id": "claude", "label": "Claude apps" }]
  },
  "items": [ /* one per plugin, skill, and prompt, see below */ ]
}
```

### Items

Plugins, skills, and prompts share most fields:

| Field | Type | Notes |
| --- | --- | --- |
| `id` | string | `plugin:<name>`, `skill:<name>`, or `prompt:<name>`. Unique. |
| `type` | `"plugin"`, `"skill"`, or `"prompt"` | |
| `slug` | string | Plugin, skill, or prompt name. Unique within each type. Items of different types can share a slug. |
| `title`, `summary`, `description` | string | From the page fields |
| `categories`, `tags`, `platforms` | string[] | Category and platform ids are listed in `taxonomy` |
| `featured`, `draft` | boolean | **Don't list items where `draft` is `true`.** |
| `image` | string or null | Absolute URL, pinned to `commit` |
| `badge`, `output` | string or null | |
| `requirements` | `{ name, required, details }[]` | `details` may be null |
| `examples` | `{ prompt, note }[]` | `note` may be null |
| `intro` | string | Markdown before the first section, often empty |
| `sections` | `{ id, heading, markdown }[]` | One per `## ` heading, in page order. Always includes `how-it-works` and `setup`. Relative links and images are rewritten to absolute URLs. |
| `paths.source`, `paths.context` | string | Repository paths of the package and its page |
| `download` | object | Plugins and prompts only. `file`, `url`, `bytes`, and `sha256`. Plugins also have `contents` (paths inside the archive). One plugin zip uploads to both Claude and ChatGPT. |

Plugin-only fields:

| Field | Notes |
| --- | --- |
| `skills` | Skill slugs in the plugin |
| `displayName` | The name ChatGPT shows |
| `install.claudeCode`, `install.codex` | Commands to add the marketplace and install this plugin |
| `install.marketplaceUrl` | URL to paste into Claude or ChatGPT |

Skill-only fields:

| Field | Notes |
| --- | --- |
| `plugin` | Slug of the plugin that contains it. Skills have no `download`: link to this plugin's download instead. |
| `install.skillsCli` | `npx skills add prismicio-community/skills --skill <name>` |
| `install.viaPlugin` | The containing plugin's `install` object |

Prompt-only fields:

| Field | Notes |
| --- | --- |
| `prompt.file` | File name to show next to the Copy button, such as `content-intelligence-dashboard.md` |
| `prompt.markdown` | The full prompt, exactly as the Copy button should copy it |

Prompts have no `install` field. Visitors copy `prompt.markdown`, or download the same text from `download.url`.

`schemaVersion` changes only when a field is removed or changes meaning. Fields may be added at any time. Version 2 removed `download` from skills and changed plugin downloads from `.plugin` to `.zip`.

## Suggested page mapping

| Library page element | Source |
| --- | --- |
| Card title, text, badge | `title`, `summary`, `badge` |
| Card requirement chips | `requirements` where `required` is `true` |
| Card output line | `output` |
| Type filter | `type`. For prompts, `badge` says what the prompt makes, such as "Dashboard". |
| Category filter | `categories`, labels from `taxonomy.categories` |
| Search | `title`, `summary`, `tags`, `requirements[].name`, section text |
| Detail tabs | `sections` |
| Copyable prompts | `examples` |
| Prompt tab with a Copy button | `prompt.file`, `prompt.markdown` (prompts only) |
| Download button | `download.url` |
| Install tab | `install`, plus the generic steps in the repository README. Prompts have none. |
| Meta description | `description` |
