# Validation record

Checked 2026-11-06. Official sources for each workflow are linked in its reference file. Versioned documentation and installed tool help take precedence when project versions differ.

| Check | Result |
| --- | --- |
| Skill frontmatter and local reference targets | Passed structural validation |
| Standalone HTML | Asciidoctor.js 4.2.1 rendered the authoring example with a document wrapper, section anchor, and tagged PowerShell include |
| Antora site | Antora 3.2.2 built the playbook example with a local test UI bundle, generated the start page, and resolved the navigation entry, section anchor, and tagged include |
| Broken site link | An unresolved xref emitted an error and the Antora build returned a nonzero status |
| Ruby HTML CLI and PDF CLI | Official commands reviewed. Ruby CLI execution, PDF output, and visual PDF checks remain untested |
| Skill activation | Examples reviewed manually. No automated activation or model comparison run |

## Activation examples

| Request | Expected routing |
| --- | --- |
| Turn these Markdown standards into an AsciiDoc operator manual | Authoring and migration, then verify the target |
| Generate a printable PDF from this .adoc manual | Standalone PDF workflow |
| Fix unresolved xrefs on this versioned Antora site | Antora build and content catalog workflow |
| Draw a banner from ASCII characters | Outside scope |
| Identify which characters are valid ASCII | Outside scope |
| Build a Docusaurus site from Markdown | Outside scope unless AsciiDoc is part of the request |
