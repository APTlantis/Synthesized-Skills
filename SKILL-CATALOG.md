# Skill catalog

Authoring date: 2026-11-06. All twelve new packages are **Structurally Valid** after the checks in [VALIDATION-REPORT.md](VALIDATION-REPORT.md). Agent trials remain unexecuted; tool smoke tests are separate evidence. Existing seven packages are preserved and retain their own status.

## [FFmpeg Media Engineer](ffmpeg-media-engineer/SKILL.md)

- Directory: `ffmpeg-media-engineer/`; family: Tool Specialists.
- Purpose: Media stream inspection and transformations.
- Positive examples: Remux an MKV with selected streams; Normalize audio with FFmpeg; Debug an FFmpeg filter graph.
- Exclusions: Recommend a media player; Copy movies unchanged; Discuss screenplay editing.
- Relationships: Reusable PowerShell orchestration is optional.
- Status: Structurally Valid; [10 planned agent cases](ffmpeg-media-engineer/evaluation.toml), all not run. Tool evidence is in the validation report.

## [Pandoc Document Engineer](pandoc-document-engineer/SKILL.md)

- Directory: `pandoc-document-engineer/`; family: Tool Specialists.
- Purpose: Format and AST transformation with fidelity checks.
- Positive examples: Convert Markdown to DOCX with Pandoc; Write a Pandoc Lua filter; Debug images missing after Pandoc conversion.
- Exclusions: Design site navigation; Crawl a documentation website; Edit prose without conversion.
- Relationships: Optional ingestion input and site publishing handoffs.
- Status: Structurally Valid; [10 planned agent cases](pandoc-document-engineer/evaluation.toml), all not run. Tool evidence is in the validation report.

## [ImageMagick Imaging Engineer](imagemagick-imaging-engineer/SKILL.md)

- Directory: `imagemagick-imaging-engineer/`; family: Tool Specialists.
- Purpose: ImageMagick 7 image operations and verification.
- Positive examples: Resize images with magick; Extract an ImageMagick histogram; Fix ImageMagick alpha compositing.
- Exclusions: Define brand voice; Draw an editable vector icon; Generate a photorealistic scene.
- Relationships: Pipeline Brand System owns supplied identity and tokens.
- Status: Structurally Valid; [10 planned agent cases](imagemagick-imaging-engineer/evaluation.toml), all not run. Tool evidence is in the validation report.

## [PowerShell Automation Engineer](powershell-automation-engineer/SKILL.md)

- Directory: `powershell-automation-engineer/`; family: Tool Specialists.
- Purpose: Reusable PowerShell 7 automation.
- Positive examples: Build a PowerShell module; Fix script native argument handling; Make file automation idempotent.
- Exclusions: Run one existing FFprobe command; Design a SQL schema; Explain Bash arrays.
- Relationships: Domain specialists retain domain-specific operations.
- Status: Structurally Valid; [10 planned agent cases](powershell-automation-engineer/evaluation.toml), all not run. Tool evidence is in the validation report.

## [Visual Engineering Architect](visual-engineering-architect/SKILL.md)

- Directory: `visual-engineering-architect/`; family: Visual & Documentation.
- Purpose: Choose and coordinate visual representations.
- Positive examples: Choose a renderer for a large graph; Compare static and interactive visuals; Plan editable diagrams and chart exports.
- Exclusions: Make this simple Mermaid flowchart; Change a Chart.js legend color; Repair one SVG path.
- Relationships: Optional existing Mermaid, Chart.js and SVG specialists; no mandatory dependency.
- Status: Structurally Valid; [10 planned agent cases](visual-engineering-architect/evaluation.toml), all not run. Tool evidence is in the validation report.

## [Documentation Site Engineer](documentation-site-engineer/SKILL.md)

- Directory: `documentation-site-engineer/`; family: Visual & Documentation.
- Purpose: Documentation site navigation, builds and integration.
- Positive examples: Build a documentation website; Repair docs navigation and routes; Configure MkDocs Material search.
- Exclusions: Convert one DOCX; Mirror a docs website; Build a transactional web application.
- Relationships: Optional Starlight specialist, Pandoc conversion and ingestion input.
- Status: Structurally Valid; [10 planned agent cases](documentation-site-engineer/evaluation.toml), all not run. Tool evidence is in the validation report.

## [Documentation Ingestion & Mirroring](documentation-ingestion-mirroring/SKILL.md)

- Directory: `documentation-ingestion-mirroring/`; family: Visual & Documentation.
- Purpose: Bounded documentation acquisition and offline reconstruction.
- Positive examples: Mirror an authorized documentation subtree; Refresh an offline collection; Reconstruct local document and image links.
- Exclusions: Read one web page; Design a docs theme; Convert one local DOCX.
- Relationships: Optional Pandoc transformation and site publication.
- Status: Structurally Valid; [10 planned agent cases](documentation-ingestion-mirroring/evaluation.toml), all not run. Tool evidence is in the validation report.

## [Rust + Tauri Application Architect](rust-tauri-app-architect/SKILL.md)

- Directory: `rust-tauri-app-architect/`; family: Application Engineering.
- Purpose: Application architecture, IPC and native boundaries.
- Positive examples: Design Tauri frontend-to-Rust IPC; Debug Tauri shared state; Add scoped native access to a Tauri app.
- Exclusions: Teach Rust lifetimes generally; Generate only an MSI; Build a browser-only React app.
- Relationships: Release engineer owns distributables.
- Status: Structurally Valid; [10 planned agent cases](rust-tauri-app-architect/evaluation.toml), all not run. Tool evidence is in the validation report.

## [Desktop Release & Installer Engineer](desktop-release-installer-engineer/SKILL.md)

- Directory: `desktop-release-installer-engineer/`; family: Application Engineering.
- Purpose: Distributable artifacts and release-stage evidence.
- Positive examples: Produce a Windows installer candidate; Audit artifact signing and versions; Prepare an AppImage release receipt.
- Exclusions: Implement an app command; Refactor Rust modules; Review a UI palette.
- Relationships: Tauri architect owns runtime/source construction.
- Status: Structurally Valid; [10 planned agent cases](desktop-release-installer-engineer/evaluation.toml), all not run. Tool evidence is in the validation report.

## [Repository Archaeologist](repository-archaeologist/SKILL.md)

- Directory: `repository-archaeologist/`; family: Application Engineering.
- Purpose: Read-only source-backed repository reconnaissance.
- Positive examples: Map an inherited application; Locate true entrypoint and stale docs; Assess change impact in an unfamiliar repo.
- Exclusions: Fix a known typo; Run a release build only; Explain a self-contained function.
- Relationships: Engineering specialists implement after reconnaissance.
- Status: Structurally Valid; [10 planned agent cases](repository-archaeologist/evaluation.toml), all not run. Tool evidence is in the validation report.

## [DuckDB & SQLite Data Engineer](duckdb-sqlite-data-engineer/SKILL.md)

- Directory: `duckdb-sqlite-data-engineer/`; family: Data & AI.
- Purpose: Local analytical/transactional storage integrity and SQL.
- Positive examples: Design a SQLite migration; Ingest CSV and export DuckDB Parquet; Debug engine-specific locking or plans.
- Exclusions: Teach generic SQL; Tune PostgreSQL; Evaluate embedding relevance.
- Relationships: AI skill owns embedding/relevance contracts.
- Status: Structurally Valid; [10 planned agent cases](duckdb-sqlite-data-engineer/evaluation.toml), all not run. Tool evidence is in the validation report.

## [Local AI & Retrieval Engineer](local-ai-retrieval-engineer/SKILL.md)

- Directory: `local-ai-retrieval-engineer/`; family: Data & AI.
- Purpose: Local inference, retrieval and grounded evaluation.
- Positive examples: Build local Ollama retrieval; Debug incompatible embeddings; Evaluate chunking and citation grounding.
- Exclusions: Explain AI generally; Rewrite an ordinary chat prompt; Optimize a database-only query.
- Relationships: Database specialist owns storage/query integrity.
- Status: Structurally Valid; [10 planned agent cases](local-ai-retrieval-engineer/evaluation.toml), all not run. Tool evidence is in the validation report.
