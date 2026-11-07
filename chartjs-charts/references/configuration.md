# Data and chart configuration

Patterns target Chart.js 4.x and must be checked against the installed release. Use [source-index.md](source-index.md) for official references beyond these focused notes. Example values and colors are illustrative.

## Data contracts

- Category charts: keep `data.labels` aligned to primitive dataset arrays. For different-length series, make gaps intentional. A label is a category unless a numeric or time scale interprets it otherwise.
- Numeric relationships: use `{x, y}` data and compatible numeric scales. Scatter defaults to numeric axes; an ordinary line's default x-axis is categorical. Sort numeric/time line data by the intended traversal order; do not sort an already ordered route without understanding its meaning.
- `null` can represent a skipped value. For line gaps, choose `spanGaps` deliberately; connecting through missing measurements is an analytical decision. Reject or explicitly handle non-finite values before plotting. Missing observations are not zero observations.
- Custom objects can use documented parsing keys. With `parsing: false`, supply the internal format for the chart and scales and the required ordering. `normalized: true` asserts that indices are unique, sorted, and consistent across datasets; do not set it as a universal performance switch.
- Time axes require a compatible date library and adapter. Internal timestamps use milliseconds since epoch. Confirm timezone interpretation and ordering; labeling a category axis with dates does not produce time-proportional spacing. Do not install a particular adapter without checking project conventions and compatibility.

## Types and scales

For v4 horizontal bars, use `type: 'bar'` and `options.indexAxis: 'y'`. Configure `options.scales.x` and `.y`, not legacy `xAxes`/`yAxes` arrays. Name alternate scales explicitly and match datasets' `xAxisID` or `yAxisID`. For stacks, set stacked axes as needed and consistent dataset `stack` names. Validate negative values and compare totals only where the model supports it.

For a line, set `fill: false` unless area conveys meaning, and make interpolation intentional. For doughnuts, keep a meaningful nonnegative total; display an explicit host empty state for an all-zero or missing total. For mixed charts, set per-dataset types and inspect draw order: a larger dataset `order` is drawn earlier, behind smaller-order datasets. Mixing defaults is not equivalent to automatically applying every type's chart-level defaults.

Choose axis ranges with the message in mind. Hard `min`/`max` can hide outliers; `suggestedMin`/`suggestedMax` do not force clipping in the same way. Label log scales and validate their positive-domain requirements. Use explicit unit titles and numeric formatting. Percentage inputs must have a stated 0–1 or 0–100 convention before display formatting.

## Options, plugins and performance

Keep tooltips and legend settings under `options.plugins`. Custom plugin objects belong in the chart configuration's `plugins` array or are registered with Chart.js; their configurable options live under `options.plugins[pluginId]`. Give custom plugins stable unique IDs and use version-correct hooks. Chart.js core does not include every popular feature: data labels, zoom, and annotation commonly require separate compatible plugins. Do not configure an absent plugin and claim the feature works.

Use scriptable options and callbacks only where the specific option supports them. Store functions in JavaScript/TypeScript and avoid serializing a working config through JSON. Global defaults affect other charts; prefer per-chart overrides unless a shared change is intended.

Measure before performance work. Consider aggregation or pre-decimation when more points are drawn than the display can resolve; preserve the source and explain analytical effects. The built-in decimation plugin is conditional, not a universal fix. Consult its exact prerequisites before enabling it. Disable animation when appropriate, limit expensive callbacks, and keep resize work bounded. Do not lower data fidelity without documenting the tradeoff.

## Demo configurations

[configs.mjs](../examples/configs.mjs) returns fresh configs for `bar`, `line`, `scatter`, `doughnut`, `stacked`, and `mixed`. It uses `animation: false` for deterministic previews and `maintainAspectRatio: false` for a host-sized container; these are example choices, not mandatory production defaults. The month labels in the line example are ordered categories, not an adapter-backed time scale. The line's missing March value stays `null` and is not bridged.
