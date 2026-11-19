---
name: asciidoc-docs
description: Write, edit, migrate, and validate AsciiDoc (.adoc) technical documentation. Use for Asciidoctor HTML, Asciidoctor PDF, and Antora documentation sites, including source includes, reusable examples, navigation, cross-references, themes, and build troubleshooting. For ASCII art or character encoding, use the workflow for that task.
---

# AsciiDoc documentation

## Choose the build path

| Deliverable | Build path |
| --- | --- |
| Source for an existing project | Match its dialect, conventions, and actual renderer |
| Standalone guide, manual, or book in HTML | Asciidoctor HTML |
| Paginated manual or book | Asciidoctor PDF |
| Documentation site with navigation and optionally several versions or repositories | Antora for a new AsciiDoc-first site. Keep an established generator when it supports the required output |
| Several outputs from shared source | Build each target independently and check that shared content works in each renderer |

1. Inspect entry points, build commands, dependency locks, CI, source layout, and existing conventions. Identify where links, images, code, and attributes are resolved. Use the project's wrapper if present. On Windows, show PowerShell-compatible commands and quote paths with spaces. Keep repository references portable.
2. Write for the task. Use ordered steps and expected results for procedures, concise definitions and examples for reference, and a coherent narrative for explanations. Keep one document title, use a consistent section hierarchy, and preserve stable IDs and public paths when editing.
3. Keep content and presentation separate. Use semantic blocks and source listings. Keep HTML styles, PDF themes, and Antora UI configuration with the relevant build target. Declare the extensions and tools needed by the target before adding extension-specific markup.
4. For migrations, inventory inbound links, explicit and generated anchors, code blocks, tables, images, and reusable content. Convert a representative page first, check rendered parity and target links, then expand. Map old URLs or add redirects through the existing site mechanism when URLs change.
5. Run the actual target build when available. Check the exit status and diagnostics, open representative output, and verify links, includes, navigation, images, tables, code and any target-specific styling. Resolve build errors at their source. If a renderer or asset is unavailable, give the exact remaining check and separate source inspection from executed rendering.

## Load what you need

- [Authoring and migration](references/authoring.md) for source patterns, cross-references, and includes.
- [Standalone builds](references/standalone.md) for HTML and PDF commands, themes, and diagnostics.
- [Antora sites](references/antora.md) for project layout, navigation, site builds, and local troubleshooting.

## Build boundaries

Render trusted inputs with the minimum access the workflow needs. For untrusted source, isolate the process with restricted filesystem and network access. Disable raw output and extensions where feasible and sanitize generated HTML before serving it. Asciidoctor safe modes constrain converter features and have implementation limits. Check before adding remote includes, third-party diagram services, or executable extensions.

Report files changed, outputs generated, commands checked, and any missing verification. Keep deployment separate from local build and preview unless publishing was requested.
