# Source evidence

Inspected: 2026-11-06 (America/New_York). Official references are paraphrased; no external code or assets are vendored. Rolling docs are not pinned compatibility guarantees. Execution evidence is reported separately.

| Source | Applicable version | Verification | Purpose |
|---|---|---|---|
| [Parsing](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_parsing?view=powershell-7.5) | 7.5 docs; local 7.6.9 | Official documentation inspected | arguments and parsing |
| [Try/catch](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_try_catch_finally?view=powershell-7.5) | PowerShell 7 | Official documentation inspected | error semantics |
| [Pester](https://pester.dev/docs/quick-start) | current docs; local 3.4.0 differs | Official quick-start inspected | version-aware tests |
| [ScriptAnalyzer](https://learn.microsoft.com/en-us/powershell/utility-modules/psscriptanalyzer/overview) | module dependent | Official overview inspected; module absent | optional static analysis |

Revalidate when dependencies, platform, renderer, schema, model or channel requirements change. Supported guidance is not a claim of successful native execution. Resolve exact installed features before adopting version-sensitive examples.
