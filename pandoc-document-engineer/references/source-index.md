# Source evidence

Inspected: 2026-11-06 (America/New_York). Official references are paraphrased; no external code or assets are vendored. Rolling docs are not pinned compatibility guarantees. Execution evidence is reported separately.

| Source | Applicable version | Verification | Purpose |
|---|---|---|---|
| [User guide](https://pandoc.org/MANUAL.html) | local 3.13; rolling docs | Official guide and local format lists inspected | formats, metadata, templates, citations and PDF |
| [Lua filters](https://pandoc.org/lua-filters.html) | Pandoc 3.x; check API | Official guide inspected | AST transformations |
| [Asciidoctor](https://docs.asciidoctor.org/asciidoctor/latest/) | 2.0 docs | Official overview inspected; runtime not established | conditional DocBook bridge |

Revalidate when dependencies, platform, renderer, schema, model or channel requirements change. Supported guidance is not a claim of successful native execution. Resolve exact installed features before adopting version-sensitive examples.
