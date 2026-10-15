# Website integration

The library page on the Prismic website reads one file: `library.json`. Every push to `main` rebuilds it, along with the downloads, and publishes them to a rolling GitHub release:

```
https://github.com/prismicio-community/skills/releases/download/library/library.json
https://github.com/prismicio-community/skills/releases/download/library/<skill>.zip
https://github.com/prismicio-community/skills/releases/download/library/<plugin>.plugin
```

These URLs never change. Fetch `library.json` when the website builds, not from the browser. GitHub release downloads redirect and don't send CORS headers.

To build the same file locally, run `npm run build`. It writes to `dist/library.json`.

## library.json

```jsonc
{
  "schemaVersion": 1,
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
  "items": [ /* one per plugin and one per skill, see below */ ]
}
```

### Items

Plugins and skills share most fields:

| Field | Type | Notes |
| --- | --- | --- |
| `id` | string | `plugin:<name>` or `skill:<name>`. Unique. |
| `type` | `"plugin"` or `"skill"` | |
| `slug` | string | Plugin or skill name. Unique within each type. A plugin and a skill can share a slug. |
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
| `download` | object | `file`, `url`, `bytes`, `sha256`, and `contents` (paths inside the archive) |

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
| `plugin` | Slug of the plugin that contains it |
| `install.skillsCli` | `npx skills add prismicio-community/skills --skill <name>` |
| `install.viaPlugin` | The containing plugin's `install` object |

`schemaVersion` changes only when a field is removed or changes meaning. Fields may be added at any time.

## Suggested page mapping

| Library page element | Source |
| --- | --- |
| Card title, text, badge | `title`, `summary`, `badge` |
| Card requirement chips | `requirements` where `required` is `true` |
| Card output line | `output` |
| Type filter | `type` |
| Category filter | `categories`, labels from `taxonomy.categories` |
| Search | `title`, `summary`, `tags`, `requirements[].name`, section text |
| Detail tabs | `sections` |
| Copyable prompts | `examples` |
| Download button | `download.url` |
| Install tab | `install`, plus the generic steps in the repository README |
| Meta description | `description` |
