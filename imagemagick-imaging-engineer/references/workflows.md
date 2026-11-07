# Image operations and recovery

Illustrative PowerShell 7 examples use fresh destinations:

```powershell
& magick input.png -auto-orient -resize '320x200>' fit.png
& magick input.png -auto-orient -resize '320x200^' -gravity center -extent '320x200' fill.png
& magick input.png -crop '100x80+10+20' +repage crop.png
& magick background.png foreground.png -gravity center -compose Over -composite composite.png
& magick input.png -colors 16 reduced.png
& magick input.png -format %c histogram:info:
```

Check `$LASTEXITCODE` for failures. `>` avoids enlargement; `^` fills before crop; `!` forces dimensions and may distort. `-trim +repage` removes the border matching the selected background/fuzz criterion, not every unwanted visual margin. Inspect the result before adopting a crop recipe.

Alpha: enabling a channel is different from making pixels transparent. Avoid flattening onto an implicit background. For JPEG explicitly select the background and remove alpha in the derivative. For masks test a tiny image with known alpha values and verify compositing order and `CopyOpacity`/other operator semantics in the installed build.

Color: inspect embedded profiles first. `-colorspace sRGB` and `-profile destination.icc` serve different contracts; a profile transform requires a meaningful source profile. When assigning a missing source profile, confirm the assumed source space. Use linear-light operations where physically correct blending/resizing is needed, then convert for display. Do not treat histogram frequency as semantic brand-role extraction.

Comparison: use `magick compare -metric AE expected.png actual.png diff.png` or an appropriate RMSE metric. Exit 1 can mean images differ; distinguish it from an execution error using diagnostics and version-specific behavior. Normalize dimensions, color and alpha intentionally before interpreting metrics. Quantization changes colors; inspect banding and transparency after palette reduction.

Animation: inspect frame delays/disposal, coalesce for operations requiring full frames, then optimize only a derivative. Verify playback and loop count. SVG: record renderer delegate, fonts, density before reading, viewport and resulting pixel size. ImageMagick rasterization cannot replace editable vector authoring.

Large images: inspect policy and cache availability with `-list policy` and `-list resource`; set explicit memory/map/disk limits proportionate to the job. Metadata can change file hashes; byte determinism requires recorded build, compression, profiles, metadata and environment, not simply a fixed resize command. Test repeated outputs and pixel signatures separately.
