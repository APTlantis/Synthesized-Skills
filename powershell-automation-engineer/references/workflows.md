# Reusable automation patterns

```powershell
function Get-CheckedFile {
  [CmdletBinding()]
  param([Parameter(Mandatory, ValueFromPipeline)][ValidateNotNullOrEmpty()][string]$LiteralPath)
  process {
    $item = Get-Item -LiteralPath $LiteralPath -ErrorAction Stop
    if ($item.PSIsContainer) { throw 'Expected a file' }
    [pscustomobject]@{ Path = $item.FullName; Bytes = $item.Length }
  }
}
$nativeArgs = @('-c', 'import sys,json; print(json.dumps(sys.argv[1:]))', 'space name', 'a&b', '[x]')
& python @nativeArgs
if ($LASTEXITCODE -ne 0) { throw "Native process failed: $LASTEXITCODE" }
```

This is an example, not a mandatory function architecture. Test the exact native runtime and argument mode for embedded quotes, empty strings and trailing backslashes. `.cmd`/`.bat` and legacy tools may use different parsing; `Start-Process -ArgumentList` is not a universal safe argv array. Prefer a supported process API with `ArgumentList` for precise argument boundaries when direct invocation is unsuitable. Avoid `Invoke-Expression`, shell interpolation and string-built paths.

| Concern | Operational choice |
|---|---|
| Errors | Use typed exceptions/actionable messages; catch narrowly and rethrow or emit a declared result. `finally` releases owned resources. A cmdlet error record and native stderr are different mechanisms. |
| Streaming | Read stdout and stderr concurrently; cancellation must terminate/wait for owned children. Preserve binary streams through a binary API; text pipes can corrupt media. |
| Parallelism | `ForEach-Object -Parallel` is a PowerShell 7 option; pass immutable values deliberately and use a throttle. Runspaces have isolated session state and serialization/lifetime constraints. Benchmark real workloads before adding them. |
| Output | Avoid accidental method return values on the success stream. Define whether arrays enumerate and whether no results means empty sequence or an explicit status. |
| Formats | Use JSON depth intentionally; CSV needs encoding, delimiter, culture and type decisions. Disable external entity resolution for untrusted XML. TOML needs a separately available parser. Roundtrip nested/Unicode fixtures. |
| Modules | Export intentional public functions, use a manifest where useful, and test clean-session import and dependencies. Do not dot-source arbitrary user content. |
| Performance | Avoid repeated array `+=`, repeated full-tree scans and per-item process spawning when batching preserves semantics. Measure elapsed time and memory before optimizing. |
| Portability | Use platform path APIs and conditional OS integration. Test case sensitivity, executability, newline/encoding and native dependencies on the real target. |

Pester: inspect `Get-Module -ListAvailable Pester` and use that major's invocation/assertion syntax. Do not install or upgrade global modules to satisfy an example. ScriptAnalyzer absence is a reported gap, not a pass. For destructive function tests use an owned temporary root and assert that similarly prefixed sibling paths remain untouched.
