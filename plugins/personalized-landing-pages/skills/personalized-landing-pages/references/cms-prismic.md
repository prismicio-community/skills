# CMS: Prismic

Everything specific to Prismic lives in this file. The rest of the skill talks
about sections, fields and drafts in CMS-neutral terms. To support another
CMS, add a sibling file (`cms-<name>.md`) with the same two parts: how to read
the base page as a structural contract, and how to write drafts safely.

Uses the Prismic MCP connector. Pass the same short `userIntent` string on
every call in a run.

## Part 1: Read the base page

### Resolve the document

- From a Prismic dashboard URL, take the repository and document ID.
- From a public page URL, find the document with
  `search_documents(repository, term=<uid or slug>, searchMode="exact")`.
- If the repository is unknown, `list_repositories` and ask which one.

### Read the structure

```
get_document(repository, documentId)
get_custom_type(repository, <meta.custom_type_id>)
```

`get_document` returns `content` and `paths`, the addressable path of every
field. For large pages whose content gets truncated, read one slice at a time:

```
get_document(repository, documentId, path="slices[<sliceKey>]")
```

For each slice, `get_shared_slice(repository, sliceId)` gives the model:
variations, primary fields, repeatable items, and field types. Use it to tell
copy fields apart from functional ones.

### Map Prismic to the structural contract

| Contract term | In Prismic |
|---|---|
| Section | A slice in the slice zone, identified by its key and variation |
| Field | A primary field on the slice, or a field on the document itself |
| Repeatable group | A slice's `items`, or a group field |
| Functional field | Link and content relationship fields, selects and booleans that drive behavior, embed fields, any key-text field used as an identifier (form IDs, widget keys) |
| Copy field | Rich text, title, and key-text fields that render as visible text |

Count characters on the rendered text of rich text fields, not on the JSON.
Record the slice key and variation alongside each field so the write step can
reuse them.

## Part 2: Write drafts safely

### Everything lands as a draft inside a release

No write goes straight to a live document. Create a named release, put every
draft inside it, and stop. A release can be reviewed and rolled back; a
published page cannot.

```
create_release(repository, label=<release name>)
create_document(repository, customTypeId, locale, title, content, releaseId)
```

When every draft is in, call `present_release` so the user can review it.
Publishing happens only when someone says publish, in that message. Never
chain create and publish in one turn, and never treat an earlier "go ahead and
build it" as permission to publish.

### The silent-success failure mode

**`create_release` and `create_document` can return an error while the write
actually succeeded.** The error looks convincing: a "try again in a moment"
message, or a parse error where an HTML error page arrived instead of JSON.

Retrying on that error creates duplicates. Three retries produce three
releases.

**On any write error, verify before retrying.**

```
# after a failed create_release
list_releases(repository)                                   # look for your label

# after a failed create_document
search_documents(repository, releaseId=<id>, searchMode="exact")
```

Only retry if verification shows the write genuinely did not happen. If it did
happen, carry on and mention that the error was spurious.

The search index is eventually consistent and can lag by a minute or more. If
a search comes back empty right after a write, wait and check again before
concluding it failed.

If duplicates do get created, report them with links so someone can remove
them in the Prismic dashboard.

### Building the document payload

Read the base document first and reuse its structure verbatim, changing only
the values you intend to change. Keep the slice keys, variation names, group
item keys and image objects from the base. Constructing a payload from scratch
invites silent normalization differences.

Build the payload in a script rather than by hand. Assemble the copy and the
structure programmatically, write it to a file, then pass it to the create
call. Hand-assembling a large nested payload is where typos in field values
come from.

Give each page its own UID. If `create_document` reports a UID conflict, pick
a new one and retry; that error is real, not a silent success.

To remove an image or an optional field, omit it. Do not carry over an image
that belongs to different content: a testimonial photo of the wrong person is
worse than no photo.

### Verify what landed

After creating a document, confirm it exists in the release and spot-check the
sections you changed most, particularly any where a section was swapped or a
field removed. Read a scoped path rather than the whole document:

```
get_document(repository, documentId, releaseId=<id>, path="slices[<sliceKey>]")
```

### Reporting

Report the document link, the release name and link, and the release's
publication state. Say explicitly that the release is unpublished. People
assume "created" means "live" unless told otherwise.
