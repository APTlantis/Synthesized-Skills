---
name: visual-engineering-architect
description: Select and coordinate diagram, chart, graph, and vector technologies based on meaning, interaction, scale, accessibility, and delivery needs. Use when multiple rendering approaches need evaluation. Prefer the named Mermaid, Chart.js, or SVG specialist for straightforward tasks in that tool.
---

# Visual Engineering Architect

Choose a representation that answers the user's question, then deliver editable source and checked rendering. Obtain entities/relationships or data, audience, required interactions, destination, size, export and editability constraints. Preserve supplied facts and tokens; label examples and unresolved relationships explicitly.

## Select before implementing

1. Decide whether the task represents relationships/processes, quantitative evidence, spatial geometry, or a composition combining them. Validate data meaning before drawing.
2. Read the [selection matrix](references/workflows.md). Compare native host support, layout control, graph size, dependency cost, accessible alternatives and export fidelity. Honor an explicitly selected framework unless a material limitation requires discussion.
3. Inspect installed renderer versions and existing project integrations. Prefer the current toolchain when it meets the contract. Do not install all supported renderers or load all specialist skills.
4. For a simple Mermaid, Chart.js or SVG request, use the existing specialist directly. Discover `mermaid-diagrams`, `chartjs-charts`, or `svg-creator` by name and follow the relevant implementation instructions. They are optional aids: when unavailable, use the official references and a minimal verified implementation. Do not modify those skills.

## Build a representative specimen

Start with the difficult case: long labels, dense connections, missing data, narrow viewport or unusual export. Preserve semantic IDs and editable source. Use supplied design tokens only when relevant; identity decisions belong to the owning brand system. Separate data transformations from rendering.

Use automatic graph layout for changing relationships; use manually authored SVG when exact geometry matters. Provide overview/detail views rather than silently dropping edges. For charts check units, domains, missing versus zero and misleading baselines. For interactive outputs provide keyboard-operable controls and persistent access to facts hidden by hover.

## Verify and recover

Validate syntax with the actual engine. Compare all required relationships/data to the specification, then inspect rendered output at intended sizes for clipping, crossings, labels, contrast and readability. Check accessible naming plus a text/table equivalent; attributes alone do not establish accessibility conformance. Preserve a source master and export settings.

If the renderer is missing, deliver editable source and explicitly mark rendering pending, or choose an available alternative that satisfies the contract. Do not substitute raster output for a required editable vector master. Do not upload private diagrams to external editors without authorization. Capture renderer errors, reduce the failing specimen and repeat affected checks.

Deliver the selection rationale, source, requested exports, meaningful alternatives, versions and tests actually performed. Use [source-index.md](references/source-index.md) for engine evidence and [evaluation.toml](evaluation.toml) for cases. No centralized runtime or mandatory specialist dependency is required.
