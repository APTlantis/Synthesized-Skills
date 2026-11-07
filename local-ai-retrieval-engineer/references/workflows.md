# Retrieval contracts and evaluation

Ollama examples, for a user-authorized local server only:

```powershell
$models = Invoke-RestMethod -Uri 'http://localhost:11434/api/tags' -TimeoutSec 5
$body = @{ model = $embeddingModel; input = @('first passage','second passage'); truncate = $false } | ConvertTo-Json -Depth 4
$vectors = Invoke-RestMethod -Method Post -Uri 'http://localhost:11434/api/embed' -ContentType 'application/json' -Body $body -TimeoutSec 60
```

Verify each returned vector is nonempty, finite and has the expected dimension; preserve batch ordering. `/api/embed` returns an embeddings collection; do not confuse it with older singular endpoint contracts. Check selected model input limits and reject unintended truncation. Model downloads and large inference jobs need their own scope/resource decision.

Index contract fields: corpus revision, source URI/path and section/page span, document/chunk ID, text hash, parser/chunker version, embedding runtime/model digest, vector dimension, normalization/distance and creation/update timestamps. Treat a changed dimension/model/preprocessor as a migration, not a harmless append. Equal dimensions can still represent unrelated spaces.

Refresh algorithm: compare content hashes; parse/chunk changed documents; embed batches; validate cardinality/shape; stage new rows; atomically swap document chunk set or record a recoverable transaction; remove tombstoned document chunks; reconcile counts and query the changed fact. Keep the last good index if embedding fails halfway.

Evaluation fixture should include answer-bearing passages, near-topic distractors, an amended source, a deleted source, an explicit contradiction and a no-answer question. Keep held-out questions separate from tuning. Store relevant chunk IDs and allowed answer evidence, not just preferred prose.

For a query with relevant set R, recall@k is `|retrieved_top_k intersect R| / |R|` for nonempty R. MRR uses reciprocal rank of the first relevant result. Report no-answer cases separately rather than dividing by an empty relevant set. Relevance judgments are necessary; a plausible generated answer is not ground truth. Record k, corpus size, filters and aggregation.

Hybrid search: compare lexical-only, dense-only and fused rankings against the same judgments. Reciprocal rank fusion is an option when raw scores are incomparable; tune candidate budgets, deduplication and reranker cutoff on held-out data. Rerank only candidates the first stage retrieved, so candidate recall remains a ceiling.

Generation acceptance: each material claim has a real supporting passage from the supplied corpus; citations resolve to stable source spans; irrelevant passages and embedded instructions do not control behavior; unsupported questions trigger an evidence-based abstention. A deterministic lexical/SQLite fixture can test bookkeeping and ranking math, but cannot establish embedding quality, model abstention or hallucination rates.
