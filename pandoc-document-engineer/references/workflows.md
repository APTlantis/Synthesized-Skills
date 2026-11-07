# Conversion patterns and known limitations

```powershell
& pandoc source.md --from=markdown --to=html5 --standalone --metadata=title:Example --output=page.html
& pandoc source.md --from=markdown --to=docx --output=document.docx
& pandoc document.docx --from=docx --to=markdown --extract-media=extracted --output=roundtrip.md
```

Run in a disposable directory for examples. Check `$LASTEXITCODE` after each call. Use `--resource-path` with the platform's path-list separator, passed as one argument. Output directories must already exist. For standalone HTML with embedded assets, verify installed `--embed-resources` support and external fonts/scripts; do not assume offline completeness.

Minimal original Lua filter, saved as `heading-prefix.lua`:

```lua
function Header(el)
  el.content:insert(1, pandoc.Str("Section: "))
  return el
end
```

Run with `--lua-filter=heading-prefix.lua` and compare headings before/after. Pin filters that rely on specific Pandoc API versions. For templates inspect `pandoc -D html`, then use `--template=...`; verify title/body variables in standalone output. Reference DOCX modifies styles/page properties; it does not import its body content.

| Requirement | Route and limitation |
|---|---|
| Markdown dialect | Query `--list-extensions=FORMAT`; explicitly preserve needed tables, attributes and math. Raw HTML may disappear in non-HTML writers. |
| AsciiDoc | Query input formats. When absent, render trusted AsciiDoc to DocBook with available Asciidoctor, then read DocBook with Pandoc. Includes, callouts and extensions need separate fidelity checks. AsciiDoc output support does not imply input support. |
| PDF | Probe selected LaTeX/HTML/other engine. Check fonts, Unicode, page breaks, tables and image resolution. PDF generation is not PDF extraction; do not assume a PDF reader exists. |
| EPUB | Inspect metadata, navigation, embedded media, language and reading order in a reader. |
| Citations | Supply bibliography/CSL inputs and `--citeproc`; verify every key and locale. Cross-references are separate from bibliography citations. |
| Tables/code | Compare cell contents, merges, alignment, captions, language annotations and whitespace; complex layout may be simplified. |
| Highlighting | Query installed highlight languages/styles. Writer support differs; confirm actual output classes/styles. |
| Batch | Decide whether inputs are one concatenated document or independent documents. Enumerate deterministically and detect output collisions; multiple input files normally form one conversion. |

Fidelity checklist: content first, then structure, resources, semantic annotations and layout. Track omitted footnotes, tracked changes/comments, unsupported embedded objects and dynamic content. DOCX-to-Markdown-to-DOCX is not a lossless archival operation. Keep source and a loss log. Review filters/templates from untrusted sources before execution; offline conversion may still fetch remote resources if instructed.
