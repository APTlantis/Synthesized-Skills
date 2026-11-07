# Validation and evidence

## Source and implementation

- Confirm selected run identity, source hash and original 32 ID/hex pairs. Verify declared artifact hashes; never repair them silently.
- Resolve aliases; reject missing references and cycles. Check token types/units and deterministic CSS names. Compare resolved colors across JSON, CSS, specimens and documentation.
- Check every adopted target-derived token against its recorded origin. Keep proposed roles distinct from upstream semantic mappings.
- Ensure missing assets, unsupported fonts and redistribution gaps remain visible. Hash retained original copies against their sources.
- Check links and offline dependencies; never claim a file was generated merely because it is mentioned in a guide.

## Accessibility and rendering

For WCAG 2.2 AA text contrast, check at least 4.5:1 for ordinary text and 3:1 for large text (18pt, or 14pt bold), with applicable exceptions described in the source. Measure final composited sRGB colors; gradients, images and alpha need actual usage-specific treatment. Do not round a failing ratio up to a pass. [W3C text contrast](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html).

Check required visual information identifying UI controls/states and meaningful graphics at 3:1 against adjacent colors, accounting for criterion-specific exceptions. Decorative borders do not all require this ratio. [W3C non-text contrast](https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html).

Do not use color as the sole means of conveying information. Add error text, status symbols, labels, patterns or other cues, especially for pipeline semantic collisions. [W3C use of color](https://www.w3.org/WAI/WCAG22/Understanding/use-of-color.html).

Record exact foreground/background, state, role, measured ratio, criterion and outcome. Keyboard-test focus visibility and order, dialogs, forms and selection controls; inspect disabled/loading/error states. Review zoom, narrow widths, long labels, typography fallback, images and charts. Contrast checks alone do not establish WCAG conformance.

Visually inspect identity overview, small logo use, representative component states and compositions. Capture filenames, viewport/zoom, environment and observed issues. Static HTML inspection is not browser rendering. Browser rendering is not native SiYuan, PowerPoint or editor acceptance. Pipeline validation from an older run does not validate new specimens.

## Reporting

Use `executed`, `manual-inspection`, `simulated`, or `not-run` for each test. Include evidence paths and limitations. Separate package structure, token correctness, visual quality, interaction behavior, native application acceptance, and rights clearance.

Stop release claims when material required checks fail; deliver reviewable partial work with clearly bounded gaps. Do not call a skill behaviorally validated based only on reading these instructions.
