# Focused media workflows

Examples are illustrative PowerShell 7 commands; replace inputs and use a fresh output directory. Check each native exit code immediately.

```powershell
$mediaArgs = @('-n','-i',$source,'-map','0:v:0','-map','0:a?',
  '-c','copy','-map_metadata','0',$destination)
& ffmpeg @mediaArgs
if ($LASTEXITCODE -ne 0) { throw 'Remux failed' }
```

For compatibility-oriented H.264 MP4, verify `libx264` and AAC availability before choosing `-c:v libx264 -crf 20 -preset medium -pix_fmt yuv420p -c:a aac -b:a 160k`. These are example quality choices. Even dimensions may be required for subsampled formats. HDR-to-SDR requires deliberate tone mapping and color metadata; pixel-format conversion alone is insufficient.

| Operation | Decision and check |
|---|---|
| Resize/filter | `-vf 'scale=320:-2'`; encode video, copy compatible unaffected audio. Compare aspect ratio and sample/display geometry. |
| Multiple graph outputs | Label pads, map each output once, check stream ordering; shell quoting and graph escaping are distinct layers. |
| Audio | `-vn -c:a flac` for lossless decoded audio; encoding lossy input to FLAC does not restore lost information. Use `pan`/`channelmap` for deliberate channel selection. |
| Loudness | Measure with `loudnorm`; for two-pass delivery feed measured values into a second pass with the same targets and inspect achieved loudness/true peak. Dynamic mode can change sample rate; set the intended output rate. |
| Trim/split | Specify whether timestamps or exact decoded boundaries matter. Input/output `-ss` placement affects seeking; verify actual start/duration and A/V sync. |
| Concat | Demuxer copy requires compatible streams/time bases. Use a correctly escaped concat-list file; file-list syntax differs from shell quoting. Keep default safe mode unless trusted absolute paths require a documented exception. Otherwise normalize and use the concat filter. |
| Subtitles | Map a known subtitle index. Text conversion may lose styling; image subtitles cannot become text without OCR. Soft mux and burned-in filters have different editability and encoding costs. |
| Metadata | `-map_metadata 0` is not a promise of all tags, chapters, dispositions or attachments. Map/check each required item and destination support. |
| Frames/GIF | Record input sequence start/rate; use a quoted `%04d` pattern. For GIF generate/apply a palette on the same resized/fps-limited content; inspect looping, timing and size. |
| Batch | Enumerate literal paths, handle basename collisions, keep per-item logs and exit status; do not overwrite input from output enumeration. |

Decode check: `ffmpeg -v error -i output.mp4 -map 0:v? -map 0:a? -f null -`. Probe JSON plus decode checks establish technical properties, not perceptual equivalence. For reproducibility record executable version/build, exact arguments and hashes; timestamps and encoder threading may affect bytes.

For an unknown encoder, inspect `ffmpeg -encoders` and `ffmpeg -h encoder=NAME`; fix the selected encoder or choose a documented alternative. For mux errors inspect supported codecs before changing file extensions. For filter errors minimize the graph and inspect `ffmpeg -h filter=NAME`. Do not silently discard rejected streams.
