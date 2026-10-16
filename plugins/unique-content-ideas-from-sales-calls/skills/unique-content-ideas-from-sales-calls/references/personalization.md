# Personalizing the skill

Run this when the user asks to personalize, set up or customize the unique content ideas skill for their brand, or to update their brand settings. The output is a brand settings document, built from `assets/brand-settings-template.md` and saved where the user chooses. Every later run reads it. The user never edits a file; they answer questions and share sources. Never change this skill's own files.

If a settings document already exists (look for it as `SKILL.md` describes), this is an update: read it, change only what the user mentions, show the change, and save it back (see "Re-personalizing" below).

## 1. Ask for what the skill needs, in one message

Before writing the message, check which connectors are available in this session: a call recorder (Gong, Modjo, Fireflies, Fathom, Avoma, Chorus or similar), a document tool (Notion, Google Drive, Confluence, SharePoint and similar), and the brand's CMS. That tells you which sources you can read yourself.

Open by saying what personalizing does: future runs already know the company, where its calls and content live, and which complaints in its category are too common to count as insights. Then list the details below, with one line on what each is for. Make it easy to answer:

- **Any form works.** A link, a Notion page, a Google Drive doc, an uploaded PDF or deck, pasted text, or "don't have it". Anything they don't have stays `Not set`.
- **Offer to look for it.** If a document tool is connected, offer to search it for positioning material and a content calendar yourself. If none is connected, suggest connecting the one their documents live in, so you can find them and re-read them on later runs.
- **Check the call recorder.** If one is connected, say which. If none is, say the skill still works with uploaded transcripts, and name the kinds of recorder connectors that work.

**I need from you**
- **Company name and website.** Used to check whether an idea is already covered on your site, and to write one line per idea on how your company fits the story.
- **Your call recorder**, or "uploaded transcripts" if you don't have a connector. Where the transcripts come from.
- **Positioning and messaging material** (optional), wherever it lives. Used only for the company-fit line on each idea. It never decides what counts as an insight.
- **Where your existing content lives** (optional): your CMS if its connector is set up, and your content calendar or editorial backlog if you have one. Read-only, so ideas you've already published or planned are marked as updates.
- **Where to save your brand settings.** One short document that every run reads first. Offer the places that work in this session: a Notion page or Google Doc (if that connector can create documents), the assistant's memory (if it has memory), or the project's files or instructions (if the user works in a project). Default to the tool their positioning material already lives in.

**I'll work out myself, then ask you to check**
- Your sitemap (from the website).
- Five to ten complaints buyers in your category make all the time (from a few searches). These are rejected as commodity on every run, so they're never reported as insights.

Keep it to one message. Don't ask for anything else: not competitors, personas, keywords, brand voice, target accounts, or who on the calls works for the company (each run works that out from the call recorder's internal and external labels and the website's email domain).

## 2. Get each detail from wherever it lives

| They send | How to read it |
| --- | --- |
| A URL | Fetch it. |
| A Notion page or link | Use the Notion connector (search by title, then fetch the page). |
| A Google Drive link or file name | Use the Google Drive connector (search, then read the file). |
| An uploaded PDF, deck or doc | Read the file in the conversation. |
| Pasted text | Use it as given. |
| A name or description only ("our messaging doc in Confluence") | Search the matching connector if one is connected; if not, suggest connecting it, or ask them to paste or upload it instead. |
| "Search my Drive / Notion for it" | Search the connector for positioning, messaging and content calendar or backlog docs. Show the titles you found and confirm which to use before reading them in full. |

If a connector the source needs isn't connected, say so in one line and offer the alternatives. Don't stop the whole setup for one missing source.

Read the website's homepage and the sitemap (`<website>/sitemap.xml`, following sitemap indexes) yourself. Run two or three searches for common complaints in the company's category to draft the known pain points.

## 3. Draft the settings and confirm them

Fill in every field of `assets/brand-settings-template.md` from what the user gave you or a source you read in this conversation; never guess. Anything the user didn't have: `Not set`. For positioning sources, record where each lives and how to read it (for example `Notion page "Messaging" via the Notion connector`). If it's an uploaded file that can't be re-read later, record `Uploaded PDF "<name>", attach again if needed`.

Show the draft as a short list and ask the user to correct it. Wait for their answer before writing anything.

## 4. Save the settings document

Save the confirmed document, titled "Unique content ideas brand settings", where the user chose:

- **Notion or Google Drive:** create the page or doc through that connector, then share its title and link.
- **Assistant memory:** save the settings to memory under that title. Keep every field but drop the explanatory lines.
- **Project files or instructions:** if you can add it to the project yourself, do; otherwise give the user the document as a file, or as text to paste, and say where to put it.
- **Nowhere available:** give the user the document as a file and tell them to attach or paste it at the start of a run.

Fill in "Last updated" with today's date. Never write passwords, API keys or tokens into the document. Never save insights, quotes, account names or article ideas from a run into it.

Close with where the settings were saved, one line on what's set, one line on what's still `Not set`, and a first prompt to try, such as: "Find unique content ideas in this week's sales calls."

## Re-personalizing

If the user asks to update the settings later ("we moved from Modjo to Gong", "add this complaint to the reject list"), find the settings document, change only what they mention, update "Last updated", show the change, and save it back to the same place.
