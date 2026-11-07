# Source evidence

Inspected: 2026-11-06 (America/New_York). Official references are paraphrased; no external code or assets are vendored. Rolling docs are not pinned compatibility guarantees. Execution evidence is reported separately.

| Source | Applicable version | Verification | Purpose |
|---|---|---|---|
| [SQLite pragmas](https://sqlite.org/pragma.html) | query runtime version | Official reference inspected | foreign keys and integrity |
| [SQLite backup](https://sqlite.org/backup.html) | runtime SQLite | Official reference inspected | online backup/restore |
| [DuckDB concurrency](https://duckdb.org/docs/1.5/connect/concurrency) | local CLI 1.5.6 | Version-specific official page inspected; stable redirects to 2.0 | write deployment model |
| [DuckDB CSV](https://duckdb.org/docs/stable/data/csv/overview) | stable redirected to 2.0; local 1.5.6 | Official reference inspected; local fixtures needed for options | staging/types |

Revalidate when dependencies, platform, renderer, schema, model or channel requirements change. Supported guidance is not a claim of successful native execution. Resolve exact installed features before adopting version-sensitive examples.
