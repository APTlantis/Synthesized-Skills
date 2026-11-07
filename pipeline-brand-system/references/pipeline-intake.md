# Pipeline intake and authority

Verified against local `apt-Clojure` and current project documentation on 2026-11-06. Recheck on schema change. Local paths are reference locations, not bundled dependencies.

| Resource | Interpretation |
|---|---|
| `run.json` | Observed schema `aptlantis.theme-run.v1`; identity, selected targets, source hash, artifact manifest paths, findings and recorded acceptance status |
| `palette.toml` | `[theme]`, `[theme.theme_identity]`, `[palette.canonical]`; exactly 32 original ID/value pairs. Entries carry hex, RGB, OKLCH and weight. Do not regenerate extraction |
| `semantics.json` | `roles` maps names to canonical IDs; `findings` records suitability problems. A role named red need not contain red |
| `provenance.json` | Observed `sha256`, dimensions and normalization/extraction evidence; imported palettes may differ from image provenance |
| `source/` | Original input, possibly image or imported TOML; inspect type, verify recorded source hash, retain bytes |
| `candidates.json`, `selection.json` | Extraction diagnostics, not additional approved brand colors |
| Target manifest | Observed schema `aptlantis.artifact-manifest.v2`; `files[]` entries contain `file`, `role`, `logical_name`, `sha256`. Resolve file relative to the manifest directory, not run root |
| Target `tokens` artifact | `tokens` object; entries include hex and `origin.source`, purpose, derived status, requested OKLCH and gamut mapping where present |
| Validation artifacts | Recorded declared pairs and checks; inspect scope before reusing claims |
| `review.html`, `palette.png` | Review materials; not normative palette data or proof of application acceptance |

Use `run.json.artifact_manifests[target]`, then select entries by `role` and format/`logical_name`. Roles are not unique: Markdown emits both `tokens.css` and `tokens.json` with role `tokens`; parse only the JSON as structured token evidence. Do not reconstruct filenames from display names. Reject paths escaping the selected run, including symlink/junction escapes. Do not treat archives as automatically safe to extract.

The helper supports the observed current schemas only. For older missing-manifest runs, inventory explicitly as legacy and inspect current project compatibility rules; do not pretend helper rejection proves corruption.

Select sources by the user's intent, matching run identity and lineage, not modification time. A newer pilot may have different mappings but is not automatically adopted. Record conflicts between palette, run and manifest identity. Separate artifact corruption from expected target derivation.

Relevant existing targets: website and Markdown for digital content; PowerPoint for editable communication templates; SVG for visual language specimens; data_visualization for chart palettes/scales; SiYuan, Typora, CodeMirror and editors for application adapters. Their syntax/structure remain owned by the pipeline. No target implies a complete brand identity or proprietary product approval.

Repository policy is project-specific: immutable canonical 32 colors, dark outputs, no new hue families, source preservation, fresh destinations, exporter expansion paused. Those constraints are not universal rules for every branding engagement.
