---
name: duckdb-sqlite-data-engineer
description: Design and troubleshoot local DuckDB and SQLite schemas, ingestion, SQL, migrations, query performance, backup, and integrity. Use for engine-specific analytical or transactional data work. Exclude general SQL teaching unrelated to these engines and retrieval relevance design.
---

# DuckDB & SQLite Data Engineer

Deliver a verified database operation with clear engine/version and data-grain assumptions. Obtain source/destination, analytical versus transactional needs, writer concurrency, schema, volume, refresh policy and acceptable losses. Use read-only inspection before writes; validate on disposable copies, never production data without explicit authorization.

## Select and inspect

1. Record actual engine/binding versions, extensions, connection mode and filesystem. Favor DuckDB for columnar analytical scans/interchange and SQLite for embedded transactional access; decide from workload, not branding. Do not assume SQL, types, indexes or concurrency are interchangeable.
2. Profile counts, keys, nulls, malformed values, duplicates, units and timestamp/timezone meaning. Determine row grain and expected joins before ingesting. Preserve raw inputs and record rejected/coerced rows.
3. Stage imports with explicit schema when inference could lose IDs, decimals, dates or leading zeros. Parameterize values and validate/quote dynamic identifiers. Untrusted file URLs, extensions and SQL functions can cross filesystem/network boundaries.
4. Read [workflows.md](references/workflows.md) for engine contracts, queries and recovery. Match docs to the installed version; current `stable` may target a newer engine.

## Change and optimize

Use explicit transactions and rollback tests. Enable/verify SQLite foreign-key enforcement on each relevant connection; handle busy/locked errors with bounded policy. SQLite WAL still permits only one writer at a time. For DuckDB verify deployed concurrency mode and do not assume arbitrary multi-process file writers are supported.

Version migrations, back up using an engine-supported method and test restore. Plan duplicate policy with a deterministic tie-breaker; `DISTINCT` is not a business-key conflict resolution rule. Make incremental updates repeatable and deletion semantics explicit.

Use query plans and representative timings to diagnose performance. SQLite indexes and DuckDB analytical storage have different costs; inspect predicate/type behavior before adding indexes. Do not infer an optimization from a smaller fixture alone.

## Verify and deliver

Check schema, constraints, row counts, key uniqueness, join fan-out, nulls and representative aggregates before/after. Test rollback, migration failure, rerun, export/reimport and backup/restore. In SQLite run both integrity and foreign-key checks where applicable; they cover different things. In DuckDB use supported consistency queries, counts and reopen/roundtrip checks rather than inventing a SQLite-equivalent pragma.

Report SQL/script, versions, input/output lineage, affected rows, plans, tests and remaining limitations. Local AI & Retrieval Engineer owns embedding/relevance contracts; this skill owns storage and SQL integrity. Read [source-index.md](references/source-index.md) and [evaluation.toml](evaluation.toml).
