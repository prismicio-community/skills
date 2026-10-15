# Contributing

You can add or update plugins, skills, and library pages through a pull request. Everything on this page works in the GitHub website, so you don't need to install anything.

## Where things live

| You want to change | Edit this | Who sees it |
| --- | --- | --- |
| Text or images on the library page | `library-context/plugins/<plugin>/index.md` or `library-context/plugins/<plugin>/skills/<skill>/index.md` | Website visitors |
| What a skill tells the assistant to do | `plugins/<plugin>/skills/<skill>/SKILL.md` and the files next to it | Everyone who installs the skill |
| A plugin's name and description in Claude or ChatGPT | `.claude-plugin/marketplace.json` and `plugins/<plugin>/.codex-plugin/plugin.json` | Everyone who browses the marketplace |
| Which categories the website can filter by | `library-context/taxonomy.yml` | Website visitors |

The two halves never mix:
- `plugins/` holds only what an assistant needs to do the work.
- `library-context/` holds only what the website shows.

If a skill needs a template or a reference document while it works, that file goes inside the skill folder. If the website needs a screenshot, that image goes in `library-context/`.

## Edit a library page

1. On GitHub, open the page you want to change, such as `library-context/plugins/<plugin>/index.md`.
2. Select the pencil icon (**Edit this file**).
3. Make your changes. The fields between the two `---` lines control the card and filters. The text below them becomes the page. The fields are explained in [library-context/README.md](library-context/README.md).
4. Select **Commit changes…**. Choose **Create a new branch for this commit and start a pull request**, then select **Propose changes**.
5. On the next screen, describe your change and select **Create pull request**.
6. Wait for the **Validate** check, which takes a few minutes:
   - If it passes, a maintainer reviews it. Maintainers listed in [.github/CODEOWNERS](.github/CODEOWNERS) are asked to review automatically, and one of them must approve before the change can merge.
   - If it fails, see [When a check fails](#when-a-check-fails).

To change more than one file in the same pull request, open each file from your new branch and commit to that branch.

### Add an image

Images for a page go in an `assets` folder next to the page's `index.md`:

1. Open the folder that holds `index.md`, then select **Add file → Upload files**.
2. If there's no `assets` folder yet, drag a folder named `assets` that contains your image.
3. Refer to the image from the page. For the card image, set this field at the top:

   ```yaml
   image: ./assets/cover.png
   ```

   For an image in the page text, write:

   ```markdown
   ![What the image shows](./assets/screenshot.png)
   ```

Use PNG, JPG, SVG, or WebP, and keep each image under 2 MB. Always describe the image in the square brackets.

### Hide a page until it's ready

Set `draft: true`. The website skips drafts.

`draft` only affects the website. A skill or plugin can be installed from the marketplace as soon as it is merged. Don't merge skills that aren't ready to use.

## Update a skill

1. Open `plugins/<plugin>/skills/<skill>/SKILL.md`, or a file in its `references/` or `assets/` folder.
2. Edit, commit to a new branch, and open a pull request, as for a library page.
3. Before you ask for a review, try the changed skill at least once. Upload the skill folder in Claude, or ask a maintainer to install your branch.

If the change affects what visitors should know, update the skill's library page in the same pull request.

## Add a new skill

Each skill needs a folder, a website page, and a line in the Claude marketplace. A maintainer or a coding agent can create all three with one command:

```
npm run new:skill -- <plugin> <skill-name>
```

To do it in the GitHub website instead:

1. **Create the skill.**
   - Select **Add file → Create new file**.
   - For the name, type `plugins/<plugin>/skills/<skill-name>/SKILL.md`. Typing `/` creates the folders.
   - Copy the content of [docs/templates/SKILL.template.md](docs/templates/SKILL.template.md) into the file. Replace `{{skill}}` with the skill name and `{{title}}` with a readable title.
2. **Create the page.**
   - Create `library-context/plugins/<plugin>/skills/<skill-name>/index.md` the same way.
   - Fill it from [docs/templates/skill-page.template.md](docs/templates/skill-page.template.md).
3. **List the skill in the Claude marketplace.**
   - In `.claude-plugin/marketplace.json`, find your plugin.
   - Add `"./skills/<skill-name>"` to its `"skills"` list.
   - Put a comma between items in the list.
4. **Fill in the placeholders.** Replace every `[[fill in: ...]]` with real text. The check fails while any placeholder is left.
5. Commit everything to one branch and open a pull request.

Skill names use lowercase letters, numbers, and hyphens, such as `meta-descriptions`. The name must match the folder name, and no two skills may share a name, even in different plugins.

### Writing a good skill

- **Start with the description.** The `description` at the top of `SKILL.md` is how the assistant decides to use the skill. Say what the skill does and list the words people use when they need it. Keep it under 450 characters.
- **Keep SKILL.md short.** Write steps the assistant can follow. Move long rules, examples, and checklists into `references/` and tell the assistant when to read them.
- **Name connectors by what they are.** Write "a Google Search Console connector", not a tool id from one assistant.
- **Don't mention plugins inside a skill.** Plugins are how skills are distributed. To point to another skill, use its name.
- **Keep it public.** No customer names, internal links, credentials, or internal-only process.

## Add a new plugin

A plugin needs entries in both marketplace files, a ChatGPT manifest, an icon, a page, and at least one skill. Ask a maintainer or a coding agent to run:

```
npm run new:plugin -- <plugin> <first-skill>
```

Then fill in the placeholders as for a new skill. Name plugins after what they do, such as `seo-basics`, never after a team or audience.

## When a check fails

1. On the pull request, select **Details** next to the failed **Validate** check.
2. Open the step with the red cross. Each problem lists the file and what to change, for example:

```
✖ library-context/plugins/seo-basics/index.md
    "categories" uses "seo-tools", which is not in library-context/taxonomy.yml. Use one of: seo, content, research, design, development.
```

The same messages appear on the **Files changed** tab, next to the file.

Fix the file on your branch and commit. The check runs again on its own.

Warnings (`!`) don't block merging, but read them.

## After merging

On every merge into `main`:
- The marketplaces update. Users who sync or update get the change.
- The downloads and `library.json` are rebuilt and published on the [library downloads release](../../releases/tag/library).
- The website picks up the change the next time it rebuilds.

## Working locally

You need Node.js 20 or later.

```
npm ci
npm run check            # validate, build the downloads, and verify their contents
npm run check:discovery  # try the skills CLI, Claude Code, and Codex against this checkout
```

`check:discovery` uses the `claude` and `codex` commands when they are installed and reports them as skipped when they aren't. It never changes your own Claude or Codex setup.
