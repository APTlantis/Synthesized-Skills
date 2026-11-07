# Design system construction

## Token layers

1. `primitive.color.<original-id>`: exact canonical values and IDs.
2. `semantic.*`: meaning-based aliases such as `surface.canvas`, `text.default`, `action.primary`, `status.error`. Preserve imported semantic assignments as source evidence; new system aliases can reference suitable existing target-derived colors without rewriting that evidence.
3. `component.*`: usage aliases such as `button.primary.background.hover`, linked to semantic decisions.
4. `adapter.<target>.*`: target-specific values with origin preserved. Different applications may legitimately need different values for the same broad purpose.

Avoid one flattened map that loses lineage. Reuse recorded derived colors first. Any new derived color must preserve the allowed hue family, document its transformation and gamut handling, and pass actual usage checks. Do not infer a derivation method solely from matching output hex values.

## Local interchange schema (not an external standard)

Use JSON `{ "schema": "pipeline-brand-system.tokens.v1", "tokens": { ... } }`. Each token key is a dot-separated stable name and each entry has:

| Field | Contract |
|---|---|
| `type` | `color`, `dimension`, `number`, `fontFamily`, `fontWeight`, `duration`, `string`, or `shadow` |
| `value` / `ref` | Exactly one: a literal or a key in the same `tokens` map; resolve refs recursively and reject missing keys/cycles |
| `status` | `source-derived`, `proposed`, or `reviewed` |
| `source` | For source-derived values, file, key, and source run identity; for originals include canonical ID; for proposals record rationale |
| `derivation` | When transformed, parent key, operation, parameters, gamut handling and validation evidence; do not invent unknown pipeline parameters |
| `description` | Usage, limitations and relevant states |

Example shape only; values must come from the selected run:

```json
{"schema":"pipeline-brand-system.tokens.v1","tokens":{
  "primitive.color.color_01":{"type":"color","value":"#000000","status":"source-derived","source":{"file":"palette.toml","key":"palette.canonical.color_01.hex","run":"EXAMPLE"},"description":"Illustrative original ID"},
  "semantic.surface.canvas":{"type":"color","ref":"primitive.color.color_01","status":"proposed","source":{"rationale":"Example alias only"},"description":"Replace with selected surface decision"}
}}
```

Use explicit dimension/duration units (for example `rem`, `px`, `ms`). Keep number values numeric. Document shadow structures before using them. Generate CSS custom properties from resolved tokens with deterministic name conversion and collision checking. Never hand-edit duplicated color tables across guide, CSS and specimens. Record font-family escaping and units correctly. Provide a migration note for renamed or deleted keys.

## Foundations

Specify a small, purposeful type and spacing scale, responsive content widths, grids, alignment, density, radii, elevation, border hierarchy, icon sizes/strokes, imagery, and reduced-motion alternatives. New numeric scales are proposals, not extracted facts. Demonstrate how they relate visually to the source identity.

## Component coverage

For digital systems start with buttons/links, fields and validation, selection controls, navigation, cards/panels, dialogs, notifications, tables and empty/loading states, then add channel-specific needs. For each document anatomy, aliases, variants, applicable states, semantics, keyboard interaction, focus management and responsive rules. Dialogs need focus entry/return and dismissal; form fields need labels and errors; charts need readable labels and non-color differentiation.

For communications define page/slide hierarchy, title/body/caption roles, chart style, image placement, margins, callouts, tables, headers/footers and source/citation treatment. Reference usable native templates; do not claim editable masters exist when only a PDF or screenshot is available.

For charts separate categorical, sequential and diverging roles. A narrow palette may require patterns, markers, direct labels or fewer simultaneous categories. Do not imply perceptual uniformity or color-vision safety without tests.
