# Personalizing the skill

Run this when the user asks to personalize, set up or customize the GEO action plan skill for their brand, or to update their brand settings. The output is a brand settings document, built from `assets/brand-settings-template.md` and saved where the user chooses. Every later run reads it. The user never edits a file; they answer questions and share sources. Never change this skill's own files.

If a settings document already exists (look for it as `SKILL.md` describes), this is an update: read it, change only what the user mentions, show the change, and save it back (see "Re-personalizing" below).

## 1. Ask for what the skill needs, in one message

Before writing the message, check which connectors are already available in this session (Notion, Google Drive, Confluence, SharePoint, OneDrive, Dropbox, Slack, the brand's CMS, and any AI visibility tool such as Peec AI, Profound, Ahrefs or Otterly). That tells you which sources you can search yourself.

Open by saying what personalizing does: the skill will know the brand, site, positioning and competitors, so future plans skip those questions and rank topics for this business. Then list the details below, grouped, with one line on what each is used for. Make it easy to answer:

- **Any form works.** A link, a Notion page, a Google Drive doc, an uploaded PDF or deck, pasted text, or "don't have it". Anything they don't have stays unset, and the skill asks for it only when a run needs it.
- **Any positioning material works.** Not just a formal positioning doc: messaging frameworks, ICP or persona docs, brand guidelines, sales decks, product one-pagers, competitor battlecards, the "about" or product pages on the site. The more of these, the better the ranking.
- **Offer to look for it.** If a document tool is connected, say so and offer to search it yourself ("Your Google Drive is connected. Want me to search it for positioning, messaging and competitor docs?"). If none is connected, suggest connecting the one their documents live in: "If your docs are in Notion or Google Drive, connect it in your assistant's connector settings and I can find and read them myself, and re-read them on later runs so the plan stays current." Where the environment can suggest connectors directly, do that.
- **Check the AI visibility tool.** The skill can't build a plan without one connected. If one is connected, check it against `references/data-sources.md` and say what it provides (and whether it has fan-out queries). If none is, say the skill needs one and name examples (Peec AI, Profound, Ahrefs Brand Radar, Otterly.AI).
- **Suggest the CMS connector too.** A connected CMS lets the skill read existing pages directly.

**I need from you**
- **Your AI visibility tool, and which project to use.** Required: the plan is built from its data. Connect it if it isn't already. Peec AI is recommended: its connector provides everything the plan uses, including fan-out queries.
- **Website.** Used to find every page you already have, so the plan updates them instead of creating duplicates.
- **Positioning and messaging material**, wherever it lives (see above). Used to judge which topics fit your product. Telling me where it lives lets me read it again on later runs.
- **Your direct competitors.** Their pages go on the "unlikely to mention you" list instead of the pitch list. A battlecard or competitor doc works too.
- **Neighbouring vendor groups that should also count as competitors** (optional). For example, a CMS might count website builders.
- **Your CMS** (optional). If its connector is set up, I read your pages through it.
- **Where you want plans and run state kept** (optional). Google Drive by default.
- **Where to save your brand settings.** One short document that every run reads first. Offer the places that work in this session: a Notion page or Google Doc (if that connector is connected and can create documents), the assistant's memory (if it has memory), or the project's files or instructions (if the user works in a project). Default to the tool their positioning material already lives in.

**I'll work out myself, then ask you to check**
- What the product does, and the categories you compete in and don't (from your positioning material and site).
- Your sitemap (from the website).
- Page families on your site worth checking for siblings, such as `/blog/best-*` or `/compare/*` (from the sitemap).
- Competitors from your AI visibility tool's brand data, if it's connected.

Keep it to one message. Don't ask for anything else.

## 2. Get each detail from wherever it lives

Work out the route from what the user sends:

| They send | How to read it |
| --- | --- |
| A URL | Fetch it. |
| A Notion page or link | Use the Notion connector (search by title, then fetch the page). |
| A Google Drive link or file name | Use the Google Drive connector (search, then read the file). |
| An uploaded PDF, deck or doc | Read the file in the conversation. |
| Pasted text | Use it as given. |
| A name or description only ("our positioning doc in Confluence") | Search the matching connector if one is connected; if not, suggest connecting it, or ask them to paste or upload it instead. |
| "Search my Drive / Notion for it" | Search the connector for positioning, messaging, ICP, persona, brand guidelines, battlecard and competitor docs. Show the titles you found and confirm which to use before reading them in full. |

If a connector the source needs isn't connected, say so in one line, suggest connecting it, and offer the alternatives (paste, upload, a link). Don't stop the whole setup for one missing source. When several documents disagree (an old deck and a newer positioning doc), prefer the most recent and say which you used.

Read the website's homepage and the sitemap (`<website>/sitemap.xml`, following sitemap indexes) yourself.

## 3. Draft the settings and confirm them

From what you read, fill in every field of `assets/brand-settings-template.md`. Fill a field only from what the user gave you or a source you read in this conversation; never guess. Specifically:

- **What the product does, Competes in, Does not compete in:** from the positioning source. Use the source's own words where you can. "Does not compete in" matters most for ranking: list categories that sound close to the brand but aren't it.
- **Direct competitors:** what the user named, plus brands from their AI visibility tool if connected, marked as suggested.
- **AI visibility tool:** the tool, the default project, and which of D1–D6 its connector provides.
- **Positioning source:** record where it lives and how to read it (e.g. `Notion page "Positioning & Messaging" via the Notion connector`, `Google Drive doc "Brand positioning 2026" via the Google Drive connector`, a URL). If there are several sources, record each. If it's a PDF or file that can't be re-read later, record `Uploaded PDF "<name>", attach again for full detail`; the fields above already hold what the skill uses from it.
- **Page families:** URL patterns from the sitemap where the site keeps many pages of one kind.
- Anything the user didn't have: `Not set`.

Show the draft as a short list and ask the user to correct it. Wait for their answer before writing anything.

## 4. Add examples from the brand's category

Step 3 of `SKILL.md` teaches clustering with examples from one software category. Fill the template's "Category examples" section with the same examples written for the brand's category, using its real competitors and topics a buyer in that category would search. Keep the structure and the point each example makes: same two products in either order is one cluster; different product sets are two clusters; same format for a different audience is two clusters; a list of destinations and a list of reasons are two clusters. If the category is unclear, leave the section empty; the built-in examples still apply.

## 5. Save the settings document

Save the confirmed document, titled "GEO action plan brand settings", where the user chose:

- **Notion or Google Drive:** create the page or doc through that connector, then share its title and link.
- **Assistant memory:** save the settings to memory under that title. Memory holds less than a document, so keep every field but drop the explanatory lines.
- **Project files or instructions:** if you can add it to the project yourself, do; otherwise give the user the document as a file, or as text to paste, and say where to put it.
- **Nowhere available:** give the user the document as a file and tell them to attach or paste it at the start of a run.

Fill in "Last updated" with today's date. Never write passwords, API keys or tokens into the document.

Close with where the settings were saved, one line on what's set, one line on what's still `Not set` and when the skill will ask for it, and a first prompt to try, such as: "Build a GEO action plan for the prompt with the lowest visibility in my project. Last 30 days."

## Re-personalizing

If the user asks to update the settings later ("we have a new competitor", "our positioning changed"), find the settings document, change only what they mention, update "Last updated", show the change, and save it back to the same place. If the positioning sources are connected, offer to reread them and refresh the positioning fields too.
