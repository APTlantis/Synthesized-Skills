---
name: imagemagick-imaging-engineer
description: Inspect and process images with ImageMagick 7, including geometry, alpha, compositing, color, palettes, animation, and batch verification. Use for ImageMagick CLI engineering and debugging. Exclude brand identity decisions and vector illustration without ImageMagick work.
---

# ImageMagick Imaging Engineer

Produce checked image derivatives while preserving originals. Establish source assets, target dimensions/formats, crop intent, transparency, color requirements, animation behavior and acceptable losses. Identity and canonical colors belong to the supplied brand system, not to an image-processing heuristic.

## Inspect and plan

1. Resolve `magick`, record `-version`, and inspect `identify -verbose`, available formats/delegates and policy when relevant. Use ImageMagick 7 `magick`, avoiding Windows `convert.exe` ambiguity.
2. Inspect all frames, orientation, dimensions/page offsets, channels, depth, colorspace, ICC profile and metadata. Decide whether to auto-orient before geometry and whether profiles/metadata must survive.
3. Choose fit, fill, crop or distortion intentionally. Preserve aspect ratio by default. Quote geometry arguments in PowerShell. Image order and option placement affect results; see [workflows.md](references/workflows.md).
4. Choose working color/alpha behavior before compositing or resampling. A colorspace label is not an ICC transform. Do not strip profiles before a required color conversion.

## Execute and recover

Use new destination paths and literal-path enumeration. Avoid `mogrify` on originals. Put limits/cache settings before heavy reads, using an owned temporary cache when needed. Do not globally weaken security policy to permit a blocked coder; choose an approved delegate or alternate route.

For batch operations use argument arrays, collision checks and per-item error results. SVG rendering depends on the delegate, fonts and supported features; retain the SVG master. For animation consider frame disposal, delay and page geometry before coalescing/optimizing. Do not turn every frame into an unrelated still accidentally.

On native failure capture executable identity, error, policy, delegate and input details. Minimize the failing operation. If switching builds or Q16/HDRI variants, use a session-scoped executable choice and repeat affected checks. Never claim pixel equivalence across builds without measurement.

## Validate and deliver

Identify the output independently: dimensions, format, channels, depth, frame count, delays, profiles and size. Use pixel samples/histograms and comparison metrics for relevant properties, plus visual inspection at target size and on light/dark backgrounds for alpha. A comparison metric alone does not establish visual quality.

Record command, build/delegates, settings and verification. For deterministic requirements separate decoded pixel equality from file-byte equality and compare repeated runs. Expose compression and palette tradeoffs. Load [source-index.md](references/source-index.md) and [evaluation.toml](evaluation.toml) as needed. Optionally consult Pipeline Brand System for token lineage; do not load it for ordinary resizing.
