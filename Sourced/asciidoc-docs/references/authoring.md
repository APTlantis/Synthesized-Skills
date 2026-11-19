# Authoring and migration

Use UTF-8 .adoc files. Set the title and document attributes in the header, with a blank line before the body. Explicit IDs preserve important anchors across heading edits.

```asciidoc
= Operator Guide
:toc:

[#check-version]
== Check the version

[source,powershell]
----
asciidoctor --version
----

NOTE: Use the version specified by the project.

Return to xref:check-version[].
```

## Select the correct reference

| Target | Example | Check |
| --- | --- | --- |
| Section in this document | `xref:check-version[]` | Explicit ID exists and is unique |
| Section in another standalone page | `xref:setup.adoc#requirements[Requirements]` | Render both pages and check the actual output path and fragment |
| Antora page in another module of this component | `xref:admin:setup.adoc#requirements[Requirements]` | Component, module, version and anchor resolve in the Antora build |
| External URL | `https://example.org/docs[External docs]` | Link text identifies the destination |

For assembled manuals, check the final link destinations after includes and check for duplicate IDs across included sections. Inspect generated output when changing how pages are split or assembled.

## Reuse source snippets

For standalone documents, include a file relative to the current source and use tagged regions for maintained excerpts. The tag markers use the included file's comment syntax.

```asciidoc
[source,powershell]
----
include::examples/check.ps1[tag=version]
----
```

```powershell
# tag::version[]
asciidoctor --version
# end::version[]
```

In Antora, use the examples resource family and a single attribute list.

```asciidoc
[source,powershell]
----
include::example$check.ps1[tag=version]
----
```

For an image with informative alternative text, use `image::build-flow.svg[Build steps from source to published output]` and place it where the target expects assets. Verify the emitted image URL and render. For diagrams with a fixed-width layout, use a literal block and review it at narrow widths. Use generated SVG or a configured diagram extension for more complex diagrams, checking support in each backend and keeping sensitive input local.

## Migration checks

- Preserve code languages, whitespace, and command prompts as appropriate. Verify runnable examples separately where requested.
- Check Markdown frontmatter mappings, heading level changes, nested lists, table separators, admonitions, and link destinations.
- Keep relative image paths and explicit anchors stable where practical. Check layout and text in the renderer that will actually ship.

## Official references

- [AsciiDoc language documentation](https://docs.asciidoctor.org/asciidoc/latest/)
- [Tagged includes](https://docs.asciidoctor.org/asciidoc/latest/directives/include-tagged-regions/)
- [Antora xrefs](https://docs.antora.org/antora/latest/page/xref/)
