# Sources and maintenance

Inspected 2026-11-06. Official Mermaid documentation displayed version 12.3.0 at inspection. Pages are living documentation, not immutable snapshots. Follow the target's installed version when it differs. No external source code, assets, or documentation excerpts are bundled; examples and prose were authored for this skill.

| Official resource | Relevant claims | Evidence |
|---|---|---|
| [Introduction](https://mermaid.js.org/intro/) | Diagram families and Mermaid's text-to-diagram scope | Documentation verified |
| [Syntax and configuration](https://mermaid.js.org/intro/syntax-reference.html) | Declarations, comments, frontmatter, unsupported configuration behavior | Documentation verified |
| [Flowcharts](https://mermaid.js.org/syntax/flowchart.html) | IDs, shapes, edges, subgraphs, reserved tokens and layout caveats | Documentation verified; sample execution recorded separately |
| [Sequences](https://mermaid.js.org/syntax/sequenceDiagram.html) | Participants, messages, alternatives and blocks | Same |
| [States](https://mermaid.js.org/syntax/stateDiagram.html) | State transitions and pseudo-states | Same |
| [Classes](https://mermaid.js.org/syntax/classDiagram.html) | Inheritance, composition, multiplicity | Same |
| [ER](https://mermaid.js.org/syntax/entityRelationshipDiagram.html) | Cardinality, relationship types, attributes | Same |
| [Gantt](https://mermaid.js.org/syntax/gantt.html) | Date format, task IDs, dependencies, calendar exclusions | Same |
| [Usage](https://mermaid.js.org/config/usage.html) | Initialization, modern run API, deprecated init, runtime needs | Documentation verified; integration snippets not application-tested |
| [Mermaid interface](https://mermaid.js.org/config/setup/mermaid/interfaces/Mermaid.html) | Async parse/render, suppressErrors and return behavior | Documentation verified; execution scope in validation report |
| [Theming](https://mermaid.js.org/config/theming.html) | Base theme, themeVariables, hex colors | Documentation verified; sample theme execution scope in report |
| [Accessibility](https://mermaid.js.org/config/accessibility.html) | accTitle, accDescr and generated metadata | Documentation verified; not accessibility conformance certification |
| [Configuration schema](https://mermaid.js.org/config/schema-docs/config.html) | Host-owned security configuration and supported keys | Documentation verified |
| [Official CLI repository](https://github.com/mermaid-js/mermaid-cli) | Package, executable, export commands, Markdown conversion | Documentation verified; installed tool checks in report |

Universal correctness constraints: preserve supplied facts, maintain valid syntax for the chosen runtime, and distinguish source, meaning, and presentation checks. Host version, DOM lifecycle, fonts, security configuration, layout availability, and accessibility behavior are environment-specific. Conservative syntax and local source-first delivery are overridable preferences. Example dates, model relationships, palettes, and names are illustrative only.

No material source conflict was found. New documentation and older embedded runtimes are reconciled by feature detection and target testing, not by claiming the latest syntax is universally supported. Review this skill when Mermaid APIs, supported versions, host restrictions, CLI flags, or recurring failures materially change the workflow. See the package's validation report for executed checks and remaining limits.
