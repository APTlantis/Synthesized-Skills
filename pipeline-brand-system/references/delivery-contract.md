# Full-system delivery contract

This is a downstream package, not a new theme-run schema. Use a fresh destination outside source runs. File names below are defaults, adjustable for the request.

| Deliverable | Minimum useful content |
|---|---|
| `README.md` | Scope, chosen run(s), status, quick use, entry links, prerequisites and limitations |
| `source-audit.json` | Helper output plus separately recorded visual/rights audit; never falsify helper results |
| `asset-ledger.json` | Source paths/hashes, asset roles, rights, use, derivatives, identity and missing variants |
| `brand-guide.md` | Brief, positioning status, verbal identity, marks, typography, palette, imagery, composition, examples and misuse |
| `tokens.json`, `tokens.css` | Linked machine-readable foundations/semantic/component tokens and a consistent resolved browser export |
| `components.md` | Anatomy, token references, variants, states, interaction and accessibility contracts |
| `specimens/index.html` | Offline responsive living specimen using delivered tokens, assets with supported rights, and realistic content; no external trackers or required CDN |
| `application-map.md` | Native asset paths, intended uses, target limitations, integration instructions and actual acceptance status |
| `decisions.md` | Evidence, rationale, proposals, conflicts and unresolved owner decisions |
| `validation.md` | Checks performed, artifacts/tools, outcomes, failures, pending native/visual checks and release limits |

Keep missing items visible; do not fill deliverables with empty headings. Partial requests may omit irrelevant outputs with an explicit scope note. A full brand request should cover strategy, verbal identity, visual foundations, implementation and governance, with unsupported parts labeled provisional.

Native PPTX/POTX, PDF, print sheets, icon libraries, social assets or framework code are conditional deliverables. Use relevant authoring tools/skills and validate their actual native formats. Do not silently expand the work into exporter development, application installation or public deployment.

For multiple brands: create separate per-brand packages, then an optional family index and comparison matrix. Share only genuinely common structural rules. Record relationship decisions; do not average palettes, rename canonical IDs globally, or blend source hashes.

Version the downstream system separately from artwork/theme identity and pipeline package versions. Record source hashes, authoring date, ownership/review status, change process, deprecations, accessibility exceptions and review triggers. Avoid invented approvers or approval dates.
