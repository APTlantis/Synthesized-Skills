# Source evidence

Inspected: 2026-11-06 (America/New_York). Official references are paraphrased; no external code or assets are vendored. Rolling docs are not pinned compatibility guarantees. Execution evidence is reported separately.

| Source | Applicable version | Verification | Purpose |
|---|---|---|---|
| [Ollama tags](https://docs.ollama.com/api/tags) | current API; local client 0.40.15 | Official endpoint docs inspected; server unavailable | availability |
| [Ollama embed](https://docs.ollama.com/api/embed) | current API | Official endpoint docs inspected | batch embeddings and truncation |
| [Ollama context](https://docs.ollama.com/context-length) | runtime/model dependent | Official guide inspected; no universal default adopted | memory/context checks |
| [Retrieve/rerank](https://www.sbert.net/examples/sentence_transformer/applications/retrieve_rerank/README.html) | current project docs | Official project guide inspected | candidate/reranking separation |
| [SQLite FTS5](https://sqlite.org/fts5.html) | binding compile options dependent | Official reference inspected | lexical baseline |

Revalidate when dependencies, platform, renderer, schema, model or channel requirements change. Supported guidance is not a claim of successful native execution. Resolve exact installed features before adopting version-sensitive examples.
