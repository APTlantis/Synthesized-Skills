# Source inventory

Inspected on 2026-11-06 (America/New_York). Sources are distributed with each package so the package remains independently usable. Each local index records identity/URL, applicable version, purpose and verification status. No official documentation corpus, external example code or third-party assets was copied into this library.

| Package | Source ledger | Version and evidence boundary |
|---|---|---|
| FFmpeg Media Engineer | [Sources](ffmpeg-media-engineer/references/source-index.md) | Local FFmpeg/FFprobe 9.0.2; official indexed CLI reference plus installed help. Direct official page fetches timed out. |
| Pandoc Document Engineer | [Sources](pandoc-document-engineer/references/source-index.md) | Pandoc 3.13; guide/Lua docs and local reader/writer lists. This installed version has an AsciiDoc reader and passed a minimal native conversion. Older builds must be checked. |
| ImageMagick Imaging Engineer | [Sources](imagemagick-imaging-engineer/references/source-index.md) | ImageMagick 7 documentation; local 7.1.2-34 Q16-HDRI. Delegates, ICC behavior and policy remain build-specific. |
| PowerShell Automation Engineer | [Sources](powershell-automation-engineer/references/source-index.md) | Microsoft PowerShell 7 documentation; local 7.6.9. Pester 3.4.0 is older than current documentation. ScriptAnalyzer is absent. |
| Visual Engineering Architect | [Sources](visual-engineering-architect/references/source-index.md) | Mermaid, Chart.js, Graphviz and D3 official references plus preserved local specialists. Only Graphviz 16.1.0 was rendered in this batch. Vega-Lite is an explicitly conditional extension requiring further official research. |
| Documentation Site Engineer | [Sources](documentation-site-engineer/references/source-index.md) | Starlight, Docusaurus, MkDocs, Material and Antora official docs. Version examples are observations of documentation, not installed-version claims. |
| Documentation Ingestion & Mirroring | [Sources](documentation-ingestion-mirroring/references/source-index.md) | RFC 9309, RFC 9110, CommonMark 0.31.2, official SiYuan repository. The precise SiYuan import contract remains unverified. |
| Rust + Tauri Application Architect | [Sources](rust-tauri-app-architect/references/source-index.md) | Tauri v2 commands/capabilities and Rust shared-state guide. No application dependencies or native app were built. |
| Desktop Release & Installer Engineer | [Sources](desktop-release-installer-engineer/references/source-index.md) | Tauri v2, Microsoft MSIX/MSI, NSIS and AppImage docs. Apple's notarization landing page required JavaScript; detailed policy is a revalidation pointer, not verified release guidance. |
| Repository Archaeologist | [Sources](repository-archaeologist/references/source-index.md) | Official Git references and disposable fixture source/configuration. Source inspection and runtime proof are explicitly distinct. |
| DuckDB & SQLite Data Engineer | [Sources](duckdb-sqlite-data-engineer/references/source-index.md) | SQLite pragmas/backup, DuckDB 1.5 concurrency and CSV references. Local SQLite binding 3.50.4 and DuckDB CLI 1.5.6. Stable DuckDB docs redirected to 2.0; local features were exercised independently. |
| Local AI & Retrieval Engineer | [Sources](local-ai-retrieval-engineer/references/source-index.md) | Ollama endpoint/context docs, Sentence Transformers retrieve/rerank guidance and SQLite FTS5. One installed embedding model was exercised; no generation system was evaluated. |

## Preserved local sources

The authoring framework is [Skill Synthesis Engine](skill-synthesis-engine/SKILL.md), using the inspected standard profile in [config.toml](skill-synthesis-engine/config.toml). Its requirements shaped progressive disclosure, evidence classification, scenario counts and honest validation levels.

Existing [Mermaid Diagrams](mermaid-diagrams/SKILL.md), [Chart.js Charts](chartjs-charts/SKILL.md), [SVG Creator](svg-creator/SKILL.md) and [Pipeline Brand System](pipeline-brand-system/SKILL.md) were inspected for operational ownership and delegation. Their content and supporting assets remain with their original packages. The Aptlantis Blue Slate and NeonInk packages were inventoried and preserved; they were not used as universal style requirements.

## Revalidation

Recheck precise official sections and local help when software, lockfiles, models, output consumers, platform SDKs or channel policies change. Source support, a local command pass, rendered inspection and target-native acceptance are different evidence levels. The [validation report](VALIDATION-REPORT.md) records which were actually obtained.
