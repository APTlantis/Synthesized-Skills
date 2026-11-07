# Capture manifest and offline reconstruction

Use TOML for human policy when the project has no established format. A conceptual policy includes allowed origins, segment-aware path prefixes, asset origins, max pages/bytes, user agent, delay, timeout and retry limit. It is not a standard crawler schema and does not configure a tool automatically.

Manifest fields per captured item: requested URL, final URL, canonical URL, local path, fetch timestamp, status, content type, ETag, Last-Modified, content SHA-256, parent discovery URL, title, license/source note, normalization version and failure detail. JSONL or a project database may suit large manifests better than TOML. Exclude tokens/cookies from stored URLs and logs.

Canonicalization examples:

- Allowing `https://docs.example.test/guide/` must exclude `/guidebook/`, `https://docs.example.test.evil/guide/`, credentials in URLs, and redirects to another origin.
- Fragment variants fetch once but retain distinct link anchors. Do not lowercase path segments or drop query strings globally; either can identify distinct content.
- Decode/normalize dot segments carefully, reject filesystem traversal, and prevent Windows reserved names, case collisions and writes outside the capture root. URL encoding is not filesystem sanitization.

Reconstruction steps:

1. Discover a bounded URL set from permitted seeds, sitemaps and in-scope links. Validate scope before enqueue and again before network I/O.
2. Capture raw response/provenance where retention is appropriate. HTML extraction must not execute scripts. Respect encoding and content type; distinguish soft-404 bodies from real documentation.
3. Allocate a deterministic URL-to-path map. Resolve relative links using final source URL and any valid base URL subject to scope policy.
4. Convert content with a parser/approved transformer; preserve fenced code bytes and examples. Frontmatter must escape arbitrary titles; use a real YAML serializer.
5. Rewrite only parsed link/image destinations; global replacement risks corrupting code blocks and unrelated text. Use the map to compute relative paths.
6. Validate all local references, fragments, assets and aliases. Leave external references explicit rather than inventing local captures.
7. For refresh, send conditional headers when a retained representation exists. Treat 404/410 deletion as a reviewed content change, transient failure as pending, and 304 as reuse. Update manifest and content atomically enough to recover from interruption.

SiYuan handoff: start with ordinary UTF-8 Markdown, conservative tables/code and relative image references inside the exported tree. Package an assets directory with the documents when the target import supports it. Test one linked page and one image with the target SiYuan version before scaling. Markdown ZIP organization, frontmatter interpretation, heading links and native block links require consumer verification; repository-level information alone does not establish them.

Fixture acceptance: two pages, one image, duplicate fragment link, external tangent, prefix-lookalike path, redirect escape, code containing URL-like text, an ETag/304 response, and a changed/deleted page. All network traffic stays on an explicitly allowed loopback fixture server. Passing pure URL helper tests is narrower evidence than a complete crawler integration test.

The bundled `scripts/url_scope.py` deliberately rejects credentials, dot segments, encoded separators, repeated slashes, trailing-dot hosts and control/whitespace in URLs rather than resolving every equivalent spelling. It preserves query strings and removes fetch fragments. It can reject valid URLs outside this conservative subset. Call it for every redirect/asset URL. It does not resolve DNS, prevent DNS rebinding, implement robots rules, rate limits, retries or filesystem allocation; callers must implement those separately. A true origin allowlist is necessary before using an asset host outside the primary documentation origin.
