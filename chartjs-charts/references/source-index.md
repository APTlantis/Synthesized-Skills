# Sources and maintenance

Inspected 2026-11-06. Official Chart.js living documentation informed the workflow; the runtime tested was 4.6.1, resolved from the official npm package. No immutable documentation revision is pinned. Use documentation for the owning project's version when it differs.

| Source | Type / authority | Relevant evidence |
|---|---|---|
| [Chart.js documentation](https://www.chartjs.org/docs/latest/) | Official project documentation | Canvas-based charting scope and documentation entry point |
| [Integration](https://www.chartjs.org/docs/latest/getting-started/integration.html) | Official guide | Auto and modular loading, component registration, script integration |
| [API](https://www.chartjs.org/docs/latest/developers/api.html) | Official API reference | Update, resize, destroy, image export and instance access |
| [Updating charts](https://www.chartjs.org/docs/latest/developers/updates.html) | Official guide | Data/options mutation, nonanimated update, scale reference changes |
| [Responsive charts](https://www.chartjs.org/docs/latest/configuration/responsive.html) | Official guide | Dedicated parent, sizing, aspect ratio, flex/grid, print caveats |
| [Accessibility](https://www.chartjs.org/docs/latest/general/accessibility.html) | Official guide | Canvas needs explicit accessible labeling or alternatives |
| [Data structures](https://www.chartjs.org/docs/latest/general/data-structures.html) | Official reference | Labels, primitive/object data, nulls, parsing requirements |
| [Bar](https://www.chartjs.org/docs/latest/charts/bar.html) | Official type reference | Horizontal orientation, stacking and axes |
| [Line](https://www.chartjs.org/docs/latest/charts/line.html) | Official type reference | Fill, interpolation, points and gap behavior |
| [Scatter](https://www.chartjs.org/docs/latest/charts/scatter.html) | Official type reference | Numeric x/y data and default scales |
| [Mixed charts](https://www.chartjs.org/docs/latest/charts/mixed.html) | Official type reference | Dataset types, defaults and drawing order |
| [Doughnut and pie](https://www.chartjs.org/docs/latest/charts/doughnut.html) | Official type reference | Dataset values, arcs and legend behavior |
| [Time axis](https://www.chartjs.org/docs/latest/axes/cartesian/time.html) | Official scale reference | Date library/adapter, epoch milliseconds, input interpretation |
| [Performance](https://www.chartjs.org/docs/latest/general/performance.html) | Official guide | Parsing, normalization, decimation, animation and measurement |
| [Decimation](https://www.chartjs.org/docs/latest/configuration/decimation.html) | Official plugin reference | Preconditions for optional built-in decimation |
| [Plugins](https://www.chartjs.org/docs/latest/developers/plugins.html) | Official developer guide | Plugin identity, registration, hooks and option namespace |
| [Canvas background](https://www.chartjs.org/docs/latest/configuration/canvas-background.html) | Official guide | Export background differs from CSS canvas background |
| [v4 migration](https://www.chartjs.org/docs/latest/migration/v4-migration.html) | Official migration guide | Breaking changes, option and distribution-path drift |

Technical claims above are verified by official documentation where inspected; execution evidence is bounded in [VALIDATION.md](../VALIDATION.md). Visual-design and analytical guardrails such as meaningful totals, explicit units, ordinary zero-based magnitude bars, and not bridging missing observations silently are authoring recommendations rather than Chart.js parser restrictions.

Constraint classification: data fidelity and honest validation claims are universal. Registration, adapters, wrappers, SSR, fonts, host access, and browser backends are environment-specific. Palette tokens and chart ownership follow the project. Conservative defaults, local tooling, and per-chart overrides are overridable preferences. Every sample value, color, label and deterministic-animation setting is illustrative only.

No material source conflict was identified. Different Chart.js versions are handled through version-aware integration, not by treating modern docs as universally compatible. Plugin versions, date adapter compatibility, framework lifecycle and native/server rendering require their own checks. Review after dependency changes, repeated failures, new target environments, or changed accessibility/export needs.

No external code, figures, datasets, or documentation excerpts are redistributed. Example code and data were authored for this package. Runtime dependencies used for tests remain outside the package; this record does not grant rights to third-party plugins or assets.
