# Engine-specific operations

| Area | SQLite | DuckDB |
|---|---|---|
| Probe | `SELECT sqlite_version();`, compile options | `SELECT version();`, installed extensions |
| CSV/JSON/Parquet | CLI/import or explicitly chosen parser/extensions; not all formats native in every binding | Table functions/readers; inspect inferred types and explicit schema options |
| Constraints | Foreign keys require connection-level enforcement; flexible typing needs deliberate constraints/STRICT support | Check supported constraints/types in installed version; not interchangeable with SQLite |
| Planning | `EXPLAIN QUERY PLAN SELECT ...` | `EXPLAIN SELECT ...`; `EXPLAIN ANALYZE` executes the query |
| Backup | Online Backup API or supported backup command; do not copy only the main live WAL database file | Version-appropriate snapshot/export/backup route; quiesce writers and test reopen/restore |
| Integrity | `PRAGMA integrity_check;` plus `PRAGMA foreign_key_check;` | Constraints, reconciliation, export/reimport and reopen tests; no assumed SQLite pragma |

Illustrative SQLite workflow in a disposable database:

```sql
PRAGMA foreign_keys = ON;
BEGIN;
CREATE TABLE item(id INTEGER PRIMARY KEY, code TEXT NOT NULL UNIQUE, amount INTEGER NOT NULL);
INSERT INTO item VALUES (1, '0007', 12);
COMMIT;
SELECT code, SUM(amount) FROM item GROUP BY code;
EXPLAIN QUERY PLAN SELECT * FROM item WHERE code = '0007';
PRAGMA integrity_check;
PRAGMA foreign_key_check;
```

Use binding parameters for user values. SQLite `INTEGER PRIMARY KEY` behavior is not a portable DuckDB sequence/default design. Money should use an intentional fixed-point/minor-unit representation, not accidental binary floats. Specify UTC/local meaning and conversion rules; string timestamps do not automatically carry timezones.

DuckDB example, confirm functions/options with installed help/docs:

```sql
CREATE TABLE staged AS SELECT * FROM read_csv('fixture.csv', header=true, all_varchar=true);
SELECT COUNT(*) AS row_count, COUNT(DISTINCT code) AS codes FROM staged;
COPY (SELECT * FROM staged ORDER BY code) TO 'roundtrip.parquet' (FORMAT PARQUET);
SELECT COUNT(*) FROM read_parquet('roundtrip.parquet');
```

`all_varchar` is a staging choice; validate then cast into a typed target. Do not silently ignore malformed rows or let schema union hide drift. For deduplication use `row_number()` partitioned by the business key with a total ordering (timestamp plus stable tie-breaker), preserve rejected duplicates and test reruns.

Interchange check: the inspected DuckDB 1.5.6 CLI serializes this fixture's integer `SUM` as a JSON string (`"15"`) because the aggregate has a wide numeric type. Verify logical SQL types and parse intentionally; do not assume every numeric SQL result becomes a JSON number or coerce identifier strings such as `0007` into numbers.

Migration acceptance: restore a disposable backup; migrate inside supported transactional boundaries; assert schema version/content; force an error and prove rollback; rerun without duplicates; reopen and compare counts/checks. Export ordering is undefined without `ORDER BY`; byte equality is not a general database equivalence criterion. Treat extension installation/loading and remote file readers as additional trust/network decisions.
