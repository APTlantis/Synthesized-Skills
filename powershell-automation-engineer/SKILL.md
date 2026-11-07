---
name: powershell-automation-engineer
description: Build, review, and troubleshoot PowerShell 7 scripts, advanced functions, modules, native process orchestration, and safe repeatable automation. Exclude tasks that merely invoke a PowerShell command while another specialist owns the work.
---

# PowerShell Automation Engineer

Engineer scripts with explicit inputs, structured outputs and reliable failure behavior. Inspect the existing module/script, PowerShell version, execution platform and project conventions. Define idempotency, concurrency, side effects and the caller's output contract before implementation.

## Design and implement

1. Use advanced functions and parameter sets where their binding semantics help. Validate values and paths at the boundary; use `begin/process/end` deliberately for pipeline input. Emit objects on the success stream and diagnostics on appropriate other streams. Format only at the presentation boundary.
2. Use `-LiteralPath` for filesystem operations. Before recursive deletion/moving verify the resolved absolute target stays inside the authorized root, including link/reparse-point behavior. Use one shell throughout; never turn discovered filenames into executable command text.
3. Invoke native executables with `& $executable @argumentArray`; capture `$LASTEXITCODE` immediately. `try/catch` handles terminating errors; cmdlet nonterminating errors require `-ErrorAction Stop` when they must abort. Native nonzero exit behavior depends on PowerShell preferences/version; check explicitly.
4. Read [workflows.md](references/workflows.md) for process streaming, parallelism, config and module design. Keep domain operations with the relevant tool specialist.
5. Prefer existing config formats. TOML is a user preference, not a built-in PowerShell parser guarantee. Resolve a supported parser, validate schema/types and keep secrets out of logs and versioned config.

## Make reruns safe

Separate discovery, proposed changes and mutation. Use `SupportsShouldProcess` and call `$PSCmdlet.ShouldProcess` around meaningful changes when appropriate. Define collision and partial-failure policy. Write through a same-directory temporary file and replace only after validation when atomicity is required and the platform supports it. Keep restore information for consequential changes.

Bound concurrency, queues, timeouts and child process lifetime. Avoid shared mutable state in parallel workers; propagate failures and preserve per-item identity. Do not collect unbounded native output into memory for long-running work. Handle stdout/stderr concurrently to avoid pipe deadlocks.

## Verify and deliver

Parse scripts with the actual PowerShell parser. Test valid/invalid parameters, pipeline cardinality, empty input, literal special-character paths, native nonzero exits and repeated execution. Use the installed Pester major's syntax; run PSScriptAnalyzer if available and assess findings rather than suppressing everything. Platform-specific modules need conditional tests. PowerShell 7 does not establish Windows PowerShell 5.1 compatibility.

Deliver script/module and usage, dependencies, error contract, tests actually run and untested platforms. A script that prints an error and exits 0 violates a failure-signaling contract. Consult [source-index.md](references/source-index.md) and [evaluation.toml](evaluation.toml); revalidate when PowerShell/native argument behavior or modules change.
