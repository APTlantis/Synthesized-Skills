# Skill library validation report

Authoring/validation date: 2026-11-06 (America/New_York).

All twelve requested packages exist and are **Structurally Valid**. They are not labeled Behaviorally Validated or Release Ready. The 120 local agent-trial scenarios are plans, all marked `not-run`; they were reviewed for fit against the authored boundaries but were not executed as agent trials or a with/without-skill comparison.

## Structural evidence

[structure.json](batch-generation/evidence/structure.json) records passing checks for all twelve packages: real YAML parsing with PyYAML 6.0.3, valid directory-matching names, nonempty bounded descriptions, local resource links, the configured 500-line core limit, parseable TOML plans and required scenario counts. Each skill has 3 positive, 3 negative, 2 execution, 1 recovery and 1 integration case. Core files are 28–31 lines of substantive instructions; detail resides in local references.

The validator also compared every file in all seven pre-existing packages against [47 baseline hashes](batch-generation/preservation-baseline.json): **zero changed files**. The checker is purpose-built package lint, not a complete Markdown/specification validator or an activation evaluator. It does not infer readiness from document length or scenario count.

## Executed tool fixtures

[smoke-results.json](batch-generation/evidence/smoke-results.json) records **14 passing fixture groups, 0 failing groups, 1 skipped group**. This is a group count, not 14 proven agent capabilities. Tests used generated content, disposable databases and owned temporary directories; no production project or database was changed. Evidence retains actual argv, exits, bounded process output and timings. Temporary source/artifact paths in logs are historical and have been cleaned up.

| Skill / fixture | Actual execution and assertions | Limits |
|---|---|---|
| FFmpeg | Generated A/V source; FFprobe JSON; mapped stream-copy remux; title preservation; H.264 scale graph and AAC conversion; FLAC extraction; decode to null; unsupported encoder rejection. | Hardware acceleration/fallback, subtitles, loudness, GIFs and perceptual A/V review unexecuted. |
| Pandoc | Markdown → standalone HTML/DOCX → Markdown; table, code and image checks; metadata/template/Lua filter; native AsciiDoc reader conversion. | DOCX was inspected as ZIP/XML, not rendered in Word; complex fidelity cases untested. |
| Pandoc PDF | XeLaTeX route generated a PDF; signature/header checked. | Layout and PDF page rendering not inspected. |
| ImageMagick | Resize/crop dimensions; known alpha Over composite; Gray conversion; histogram count; bounded palette; repeated stripped PNG byte hash. | ICC transforms, animation, SVG delegates, large-image limits and cross-build determinism untested. |
| PowerShell | Five Pester 3.4.0 tests: literal special-character path pipeline; invalid/missing input; exact native argv including quotes/empty strings; nonzero exit detection; idempotent write hash/mtime. | ScriptAnalyzer missing; Linux, runspaces and long-running process cancellation untested. |
| Visual Engineering | Graphviz DOT → SVG/PNG; 3 nodes and 2 edges asserted. Rendered PNG visually inspected: labels fit and arrows/read order are clear. Editable [DOT](batch-generation/evidence/workflow.dot), [SVG](batch-generation/evidence/workflow.svg) and [text equivalent](batch-generation/evidence/graph-description.txt) retained. | Mermaid, Chart.js, D3, large-graph performance and destination accessibility not rendered/tested. |
| Documentation Sites | Dependency probe executed. | **Skipped:** MkDocs module absent. No generator production build or browser/search test is claimed. |
| Documentation Ingestion | URL helper: 3 allowed and 9 rejected origin/path cases; loopback fixture redirects blocked before outside fetch; ETag/304 body reuse; Pandoc AST page/image target inspection; relative page/asset files and code preservation; YAML title parsing. | Fixture is a small protocol/parser integration, not a complete crawler. Changed/deleted-page refresh, generalized path rewriting, robots/rate policy, offline UI and native SiYuan import remain untested. |
| Rust/Tauri | Official API/capability source review and scenario design. | No Rust/Tauri app build, native IPC or permission test executed. |
| Desktop Release | TOML receipt roundtrip, final-byte SHA-256 equality and changed-byte mismatch detection on a disposable binary fixture. | Fixture is explicitly not an installer. No bundle build, signing, installation, Store acceptance or publication performed. |
| Repository Archaeology | Created a tiny disposable repository, inventoried manifest/service/data, searched the real import chain and stale README; source hashes stayed unchanged during inspection. | These verify available search/evidence mechanics, not an agent's reconstructed architecture; meaningful history and complex repo cases untested. |
| SQLite | Constraint/FK rejection, transaction rollback, indexed query plan, schema/version migration, idempotent upsert, online backup restore, integrity/FK checks and CSV logical roundtrip. | Multi-process concurrency, production-scale plans and failure during a real migration remain untested. |
| DuckDB | CSV all-text staging, typed aggregate, exact-row fixture dedup, rollback, Parquet export/reimport and database reopen. Leading-zero IDs preserved. | Production business-key tie-breaking, extensions and performance not benchmarked. |
| Local retrieval baseline | Three-passage SQLite FTS5 corpus, one judged query, no-match query, update/deletion and contract mismatch fixtures. Recall@3 and MRR are 1.0 for that single trivial judged query. | These are fixture assertions, not general relevance scores, embedding evaluation or model abstention evidence. |
| Ollama availability | Local `/api/tags` responded with 27 installed models. Initial CLI check had reported no server; the later API probe superseded that observation. | No model downloads; existence alone says nothing about every model's execution support. |
| Live embeddings | Existing `embeddinggemma:latest`, digest recorded in JSON; 4 synthetic texts returned finite vectors of dimension 768; one query ranked its expected passage first. Request elapsed 25.154 seconds in the recorded run, including unspecified load/runtime effects. | Single-query compatibility/ranking smoke only; no answer generation, citation entailment, model abstention, sustained latency or memory benchmark. |

The alpha fixture output was numerically checked at RGB (128, 0, 127); no additional visual-image quality claim is inferred from that pixel assertion.

## Failures and corrections

Initial evidence is retained in [smoke-results-initial.json](batch-generation/evidence/smoke-results-initial.json). Corrections were followed by targeted reruns, without repeating unchanged expensive tests.

| Issue | Expected / observed | Severity and disposition |
|---|---|---|
| Sandbox process launcher | Expected commands to start; sandbox launcher began failing before execution with HRESULT `0x80070020`. | Environment limitation. Authorized workspace generation/tests continued through reviewed execution outside the failing sandbox. No user approval rejection occurred. |
| Package link lint | Expected actual links only; initial scanner treated an inline-code Markdown image example as a package asset link. | Low, validator false positive. Excluded code examples; all actual links rechecked and passed. |
| PowerShell path assertion | Expected literal path identity; fixture compared Windows 8.3 temp-root spelling with expanded `FullName`. | Low, fixture defect. Compare resolved file identity and separately assert literal basename; retest passed. |
| Legacy Pester error assertion | Parameter validation threw correctly in an isolated PowerShell probe, while Pester 3 `Should Throw` did not recognize the fixture as expected. A subsequent typed catch referenced an unavailable exception type. | Low, fixture compatibility issue. Use explicit catch plus stable validation error ID and missing-file exception; final five tests passed. No claim that old Pester is universally compatible with current PowerShell. |
| DuckDB alias | Expected aggregate output; bare `rows` alias produced a parser error. | Low, fixture SQL defect. Use `row_count`; corrected the analogous reference example and retested. |
| DuckDB JSON type | Expected numeric aggregate JSON value; CLI serialized wide integer sum as string `"15"`. | Medium interoperability lesson. Parse the logical aggregate intentionally, preserve identifier strings, add reference guidance; retest passed. |
| MkDocs absence | Expected optional generator for site fixture; module probe reported absent. | Coverage gap, not a package failure. Kept skipped; no installation or build claim. |

## Cross-skill review

Author review checked all positive/negative cases against descriptions and ownership. Explicitly named simple Mermaid/Chart.js/SVG tasks route to the preserved specialists; visual architecture selects across technologies. Ingestion owns acquisition, provenance and reconstruction; Pandoc transforms; site engineering owns navigation/build. ImageMagick does not invent brand tokens. Tauri construction and release artifacts have separate contracts. Archaeology remains read-only unless implementation is separately authorized. Retrieval owns relevance/model compatibility while databases own SQL/integrity. PowerShell activates for reusable automation work, not every command invocation.

No mandatory or circular skill dependencies were introduced. Every package links only to its own resources and describes optional handoffs by installed skill name. The core does not force Windows, a new config parser, a shared runtime, a particular theme or all framework installations. TOML is used for the human-readable trial plans and the illustrative release receipt, while native tool configuration formats are retained.

Technical conflicts were bounded rather than silently flattened: installed versus current DuckDB documentation, version-specific Pandoc reader direction, plugin versus custom-command Tauri permissions, and unverified SiYuan/native distribution contracts. No original skill, artwork, token set or production project was rewritten.

## Remaining acceptance work

The file-library completion criteria are satisfied with the documented evidence limitations. Operational readiness remains gated on representative agent trials and the appropriate target environments. Prioritize the 72 activation cases and missing-input cases, then site production/browser checks, a small native Tauri app, installer lifecycle/signature checks, SiYuan import and retrieval no-answer/citation tests. Extend hardware/ICC/large-data benchmarks only when a concrete workload requires them.

## Reproduce

From the library root, with Python 3.11+ and PyYAML available:

```powershell
python batch-generation/validate_library.py --report batch-generation/evidence/structure.json
python batch-generation/smoke_tests.py
# Targeted rerun, preserving other evidence:
python batch-generation/smoke_tests.py --only powershell duckdb
```

The smoke runner additionally needs Pillow for image checks and the relevant installed CLI for each fixture. Its ingestion fixture uses a temporary loopback HTTP server and Pandoc; live embedding tests use an already installed `embeddinggemma:latest` model and local Ollama only. No dependency is installed automatically. The authoring workspace contains everything needed to read/use each skill without these batch-validation scripts.
