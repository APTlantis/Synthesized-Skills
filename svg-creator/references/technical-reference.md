# SVG construction and recovery

These are practical recommendations for static vector artwork, not a complete specification. Sources and evidence classifications are in [source-index.md](source-index.md).

## Coordinates and geometry

`viewBox="0 0 640 400"` defines artwork coordinates, not a required pixel export size. A different viewport ratio is normally fitted using `preserveAspectRatio`; `none` permits unequal scaling. Positive viewBox extents are a package convention that avoids a disabled or invalid drawing region. Leave deliberate padding for strokes, whose default placement extends around the path centerline.

Use explicit coordinate math for symmetry, evenly spaced repetitions, and connector alignment. For paths, `M` starts a subpath; `L`, `H`, and `V` draw lines; `C` and `Q` draw curves; `A` draws elliptical arcs; `Z` closes a subpath. Lowercase commands use relative coordinates. An arc takes radii, rotation, large-arc flag, sweep flag, and destination; flags are 0 or 1. Use the specification for detailed grammar and degenerate cases. XML parsing cannot establish path correctness.

When debugging transforms, temporarily isolate the group, simplify its transform list, and inspect an asymmetric test shape. Do not flatten transforms before confirming their effect. Do not round coordinates to an arbitrary precision if that changes small-size contours.

## Paint, reuse, and effects

- Reuse a gradient or symbol through a same-document reference such as `url(#art-gradient)` or `href="#art-symbol"`. SVG 2 uses `href`; older targets may require a compatibility form. Confirm the target before adding deprecated `xlink:href` and its namespace.
- A clip defines the visible region geometrically; a mask controls visibility using mask values. Specify units and regions deliberately when defaults do not match the desired coordinate system.
- For a gradient spanning a whole composition, `gradientUnits="userSpaceOnUse"` may be easier to reason about than object-relative coordinates. This is a design decision, not a universal requirement.
- `vector-effect="non-scaling-stroke"` is useful when strokes should retain display width as artwork scales; ordinary scalable illustration often needs normal scaling instead.
- Check filter regions and canvas bounds when shadows are cut off. Broadening a filter region has rendering costs; do not apply huge filter bounds to every object as a default fix.
- `currentColor`, CSS variables, external style sheets, fonts, and embedded HTML depend on the delivery context. Test that context. Do not assume a PNG preview exercises them faithfully.

## Text and portability

Use text anchoring and deliberate baselines; SVG text does not behave like a normal HTML paragraph. Lay out lines explicitly when the target lacks a tested wrapping feature. Check actual font metrics and glyph coverage, especially for non-Latin scripts. A font-family name does not embed a font. State dependencies or supply an authorized font strategy. Keep a text master if a separate outlined export is needed.

Inline SVG shares the host document's ID namespace. Prefix gradient, clip, marker, and accessibility IDs together with every reference. Test repeated icons on one page. Source edits for a framework component may require that framework's attribute conventions; valid standalone XML is the default output here, not a substitute for JSX syntax checks.

## Failure triage

| Symptom | First checks | Recovery |
|---|---|---|
| Blank artwork | XML error, namespace, viewBox, hidden styles, fill/stroke, unresolved references | Isolate a visible primitive, then restore groups incrementally |
| Cropped edges | Stroke/marker extent, filter region, clip and viewport | Adjust intended bounds or region without distorting geometry |
| Strange filled region | Open path, implicit closure, winding and compound subpaths | Set fill deliberately; correct closure or fill rule |
| Wrong repeated instance | Duplicate IDs, use reference, host CSS | Prefix IDs and references together; isolate style scope |
| Changed typography | Missing font, fallback metrics, unsupported layout | Use an available approved font, explicit layout, or separate outlined derivative |
| Renderer mismatch | Unsupported CSS/effect/font or embedding restrictions | Test actual target and simplify only the affected feature |

The checker intentionally accepts only UTF-8 input and rejects DTD/entity declarations. This is its input policy, not a statement that all other XML encodings or DTD-bearing SVG documents are inherently invalid. Convert a trusted source to a self-contained UTF-8 copy when necessary. Its reference inspection covers literal fragment `href`, `url(...)` values, and two ARIA ID-list attributes; CSS escapes, external fragments, animation timing references, and other reference forms require separate review.
