---
name: pandoc-document-engineer
description: Engineer Pandoc format conversions, templates, reference documents, metadata, citations, and Lua filters with explicit fidelity checks. Use when Pandoc performs document transformation. Exclude website crawling, documentation-site architecture, and unrelated document editing.
---

# Pandoc Document Engineer

Produce a converted document with an explicit fidelity contract. Obtain input format/dialect, output format, assets, bibliography, intended reader and required layout. Inspect a representative input before selecting flags; preserve originals.

## Establish the conversion route

1. Record `pandoc --version`, `--list-input-formats` and `--list-output-formats`. Reader and writer availability are directional. Do not assume AsciiDoc input support; use an installed Asciidoctor/DocBook route when the reader is absent and label its additional losses.
2. Choose explicit `--from` and `--to` values. Confirm extensions for tables, fenced code, math and raw markup. CommonMark, GFM and Pandoc Markdown have different capabilities.
3. Inventory structure, citations, cross-references, tables, images, alt text and styling that must survive. Layout-rich sources can lose information through the AST. See [workflows.md](references/workflows.md).
4. Choose standalone versus fragment output. HTML fragments do not apply a full page template. For DOCX use a reference DOCX for styles; a template is a different mechanism. For PDF identify and probe the chosen external engine.

## Transform deliberately

Use argument arrays in automation and UTF-8 text. Set resource search paths explicitly; resolve them against a known working directory. Extract media from office/EPUB sources into a fresh owned directory, preserving stable relative links. Keep acquisition and publication outside this skill.

Use metadata files for repeatable titles, language, bibliography and variables; validate their actual interpretation in the selected writer. Run `--citeproc` when required and check unresolved keys and bibliography output. Cross-reference numbering may require a compatible filter; do not invent a native capability.

Use a small Lua filter for AST changes that flags alone cannot express. Inspect filters before executing them; they are code. Apply filters in intentional order and compare the relevant AST/output. Keep reusable examples in project conventions rather than imposing a new config format on Pandoc.

## Recover, verify and deliver

Capture warnings and fail on native errors. Reduce fidelity problems to a minimal document and inspect `-t native` or JSON AST. If the reader lost content, downstream styling cannot restore it. Change route or report the loss.

Verify output existence, parseability, headings, tables, code, citations and local asset resolution. Open/render formatted outputs when layout matters; a ZIP check of DOCX is structural evidence only. Compare representative pages and explicitly record rendering that could not be performed. Report exact commands, versions, engine/filter dependencies and known losses.

Use [source-index.md](references/source-index.md) and [evaluation.toml](evaluation.toml). Optionally hand acquired documents to Documentation Ingestion & Mirroring or generated pages to Documentation Site Engineer; neither is required to run Pandoc.
