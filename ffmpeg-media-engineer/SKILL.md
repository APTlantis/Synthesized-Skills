---
name: ffmpeg-media-engineer
description: Inspect, transform, and troubleshoot media with FFmpeg and FFprobe. Use for stream mapping, remuxing, transcoding, filters, subtitles, normalization, and batch media pipelines. Exclude media-player selection, unrelated editing advice, and ordinary file copying.
---

# FFmpeg Media Engineer

Deliver a reproducible media operation and an inspected output. Accept source paths, desired streams, target player/container, quality or size constraints, and overwrite policy. Discover missing technical facts with FFprobe; ask only when the intended content or quality tradeoff cannot be inferred.

## Inspect and decide

1. Resolve the actual executables and versions. Check encoders, muxers, filters and hardware support in the installed build; advertised acceleration is not proof that the device can run it.
2. Probe each input with `ffprobe -v error -show_format -show_streams -of json input`. Record stream indices, codecs, language/disposition, duration, dimensions, pixel format, rate/time base, channels, sample rate, metadata and rotation/color information relevant to the task.
3. Write an explicit stream plan. Select streams with `-map`; quote optional selectors such as `'0:a?'` in PowerShell. Automatic selection may omit content. Container support and codec support are separate decisions.
4. Prefer `-c copy` when no decoded-media change is required and the destination can carry the streams. Filtering requires encoding the affected stream. Packet-copy cuts need not be frame accurate; choose re-encoding when exact boundaries matter.
5. Select a tested encoder and quality mode. CRF and hardware quality values are encoder-specific; do not transfer numbers between them. Size budgets require bitrate/duration planning and measured output.

## Execute and recover

Use argument arrays and the call operator in PowerShell; pass each graph as one argument. Avoid shell-built command strings. Input options precede their input; output options precede their output. Use a new destination and `-n` by default; only use `-y` for authorized disposable/replacement outputs. Capture stderr and the native exit code.

Read [workflows.md](references/workflows.md) for filters, audio, concat, subtitles, GIFs, and recovery. Start complex graphs with labeled pads and a short generated fixture. Preserve originals and temporary intermediates needed to diagnose a failure. If hardware initialization fails, report the error and use a compatible CPU encoder only when its output contract is acceptable. Recheck quality and metadata after fallback.

## Validate and deliver

Probe the produced file independently. Compare expected stream count, codecs, dimensions, duration tolerance, channel layout, language, disposition and requested metadata. Decode the relevant streams to a null sink to detect corruption. Inspect representative frames and listen to affected audio when fidelity matters; numeric inspection alone is not perceptual review. Report any unperformed review explicitly.

Deliver command/script, output paths, version/capability evidence, verification results, and material losses. Do not call a successful process an accepted encode without checking its artifact. For reusable automation, optionally use PowerShell Automation Engineer; domain stream choices remain here.

Load [source-index.md](references/source-index.md) for evidence and [evaluation.toml](evaluation.toml) for task cases. Recheck when build, codec, driver or target-player requirements change.
