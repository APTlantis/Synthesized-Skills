# Batch inventory and design

Authoring date: 2026-11-06 (America/New_York). Framework: existing `skill-synthesis-engine/SKILL.md`, standard profile from its inspected `config.toml`. No per-skill TOML schema is imposed. No new runtime dependency is required to use the instructions.

## Inventory checkpoint

Seven existing packages were found in the workspace: aptlantis-blue-slate, aptlantis-neonink, chartjs-charts, mermaid-diagrams, pipeline-brand-system, skill-synthesis-engine, svg-creator. All 47 files were hashed before generation in [preservation-baseline.json](preservation-baseline.json). The five requested reference skills' core instructions were inspected. Their prose and assets are preserved, not repackaged. Detailed specialist references should be loaded by their owning skills only as needed.

Tools detected: PowerShell 7.6.9; Python 3.13 with PyYAML 6.0.3, Pillow and BeautifulSoup; FFmpeg/FFprobe 9.0.2; Pandoc 3.13; ImageMagick 7.1.2-34 Q16-HDRI; Cargo 1.98.1; Node 24.22.2; Graphviz 16.1.0; DuckDB CLI 1.5.6. Python DuckDB and MkDocs modules are absent. Pester 3.4.0 is available; PSScriptAnalyzer was not found. Ollama client 0.40.15 is present but reports no running server. Asciidoctor and XeLaTeX command paths exist; execution support remains to be tested. Mermaid CLI was not found. No production app or database is a test target.

Git initially rejected repository ownership. Read-only inspection uses a command-local `-c safe.directory=...` exception; no global Git configuration changes. Initial status was clean. No applicable AGENTS.md was found at workspace or ancestor locations checked.

## Architecture checkpoint

| Batch | Directory / operational contract | Optional handoff |
|---|---|---|
| A | ffmpeg-media-engineer: inspect and transform media streams | PowerShell for reusable orchestration |
| A | pandoc-document-engineer: transform document AST and formats | Ingestion supplies sources; sites publish |
| A | imagemagick-imaging-engineer: inspect and transform raster images | Brand system supplies identity/tokens |
| A | powershell-automation-engineer: engineer reusable shell automation | Domain specialists choose domain operations |
| B | visual-engineering-architect: choose representation and renderer | Existing Mermaid, Chart.js, SVG specialists |
| B | documentation-site-engineer: navigation, builds and publishing preparation | Existing Starlight specialist when available |
| B | documentation-ingestion-mirroring: bounded acquisition and offline reconstruction | Pandoc transforms acquired content |
| C | rust-tauri-app-architect: application boundaries and IPC | Release engineer packages app |
| C | desktop-release-installer-engineer: distributable artifacts and evidence | App architect fixes runtime construction |
| C | repository-archaeologist: evidence-backed reconnaissance | Implementation passed to relevant specialist |
| D | duckdb-sqlite-data-engineer: database integrity, queries and exchange | Retrieval engineer owns relevance |
| D | local-ai-retrieval-engineer: local inference and retrieval evaluation | Database skill owns storage |

Each package has a self-contained core, local workflows/source references and a local evaluation plan. Handoffs are optional: discover installed specialists by name; absence never prevents using the core instructions. No sibling-relative links make a package dependent on this folder layout.

Validation plan: parse real YAML; resolve local Markdown links; verify names/descriptions and line budget; check test-class counts; compare preserved hashes; execute disposable fixtures with available tools. Activation and task plans are not claims of agent evaluation. Native app, installer, browser and model tests need their respective environments. Review each batch before proceeding to the next.

## Evidence reconciliation

- Current DuckDB `stable` documentation redirects to 2.0 while the local CLI is 1.5.6: use 1.5 references and probe features before using newer APIs.
- Tauri v2 capabilities do not automatically constrain every application command. Registered application commands are available by default unless enrolled in app permissions; backend checks remain necessary.
- Pandoc reader/writer direction is determined by the installed format lists, especially AsciiDoc. PDF generation needs a separate engine.
- Initial FFmpeg website fetches timed out. Official indexed documentation and installed CLI help provide fallback evidence; record remote fetch failure rather than calling all pages inspected.
- SiYuan's repository establishes the product source, not proof of a particular Markdown ZIP import contract. Import conventions remain conditional until tested in the target version.
