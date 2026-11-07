# Validation record

Date: 2026-11-06. Status: **Structurally Valid**, with representative rendering and syntax-rejection tests executed. This is not a claim of full agent behavioral validation or universal host compatibility.

## Environment and dependencies

- Windows; Node.js 24.22.2.
- Official `@mermaid-js/mermaid-cli` 12.2.0 and Mermaid core 12.3.0, confirmed with CLI version output and `npm ls`.
- Isolated test dependencies installed under the chat's `work/mermaid-runtime`, with lifecycle scripts disabled. Used existing local Google Chrome via a Puppeteer executable-path configuration. Runtime dependencies and machine-specific browser configuration are not bundled in the skill.
- The restricted command sandbox initially prevented browser launch. The same local checks succeeded with execution outside that sandbox; browser sandbox protections were not disabled. Browser launch failures were not counted as expected parser rejections.

## Executed checks

| Check | Result |
|---|---|
| SKILL.md YAML parsed using PyYAML; name and description checked | Passed |
| Instructions below 500 lines | Passed: 71 lines |
| Relative resource links across Markdown files | Passed |
| Flowchart, sequence, state, class, ER, Gantt samples exported to PNG | Six passed |
| Flowchart additionally exported to SVG | Passed |
| SVG title, description, aria-labelledby and aria-describedby presence | Passed; not a full accessibility audit |
| Malformed flowchart label, malformed sequence message, invalid ER relationship | Three rejected with parser errors and nonzero exit codes |
| Custom-theme example extracted from integration.md and rendered | Passed; colors visually inspected |
| Gantt visual correction and rerender | Passed; explicit daily ticks remove repeated displayed dates |

Visually inspected all six rendered samples. Confirmed arrow directions, decision branch labels and return loop, cache hit/miss blocks, state initial/final symbols and revision loop, class inheritance/composition ends and multiplicities, ER cardinality and dashed relationship, and schedule order. The final Gantt shows January 5–9 with one tick per day. No visible clipped labels or overlapping nodes were observed at the rendered inspection size. This does not establish readability at every display size.

Reproduction with an available compatible installation: run `mmdc --version`, then `mmdc -i examples/flowchart.mmd -o NEW_OUTPUT.svg`; repeat for the other five files and inspect outputs. Check installed help for Puppeteer configuration if using an existing browser. Use the actual destination's version before relying on these results.

## Manual instruction review

These cases were inspected against the written workflow, not run through independent agents; no trigger-accuracy score is claimed.

| Case | Expected behavior | Review |
|---|---|---|
| Create a Mermaid process diagram | Activate; choose flowchart and label decisions | Covered |
| Debug Mermaid sequence parse failure | Activate; isolate source and validate with actual parser | Covered |
| Embed Mermaid with project theme | Activate; inspect installed version, lifecycle and theme support | Covered |
| Create a freeform SVG illustration | Do not activate | Explicit exclusion |
| Draw a diagram in a different named tool | Do not activate | Explicit exclusion |
| Analyze sales data and choose a statistical chart | Do not activate on chart need alone | Explicit exclusion |
| Missing ER optionality or required schedule dates | Ask or explicitly bound uncertainty; do not invent facts | Covered |
| New syntax conflicts with an older embedded runtime | Use the destination feature set; preserve meaning | Covered |
| Supplied palette differs from the example | Use supplied tokens; sample palette is illustrative | Covered |
| No local renderer or installation allowed | Deliver source; mark execution unperformed | Covered |
| Diagram parses but contains an incorrect dependency | Fail meaning validation | Separate validation level |
| Private diagram and an available public editor | Use approved local rendering; no implicit upload | Covered |

## Limitations

No with/without-skill agent comparison, automated routing evaluation, older-version matrix, or destination-app integration was run. The browser API integration snippets were reviewed against official documentation but were not exercised inside a real web application. Dynamic rerendering, screen readers, full accessibility trees, light/dark variants, mobile layouts, PDF output, Markdown document conversion, experimental diagram types, alternate layouts, and custom icon packs were not tested. All examples were tested with one CLI/core/browser combination.

No custom syntax checker is shipped: validation deliberately uses Mermaid's own parser/renderer. PyYAML was needed only for authoring-time package inspection, not for using the skill. No global Mermaid installation, skill installation, activation, or modification of another project was performed.
