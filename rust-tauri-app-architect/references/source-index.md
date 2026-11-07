# Source evidence

Inspected: 2026-11-06 (America/New_York). Official references are paraphrased; no external code or assets are vendored. Rolling docs are not pinned compatibility guarantees. Execution evidence is reported separately.

| Source | Applicable version | Verification | Purpose |
|---|---|---|---|
| [Commands](https://v2.tauri.app/develop/calling-rust/) | Tauri v2 | Official guide inspected | IPC registration and API imports |
| [Capabilities](https://v2.tauri.app/security/capabilities/) | Tauri v2 | Official guide inspected, including custom-command enrollment | plugin/app permission boundary |
| [Rust state](https://doc.rust-lang.org/book/ch16-03-shared-state.html) | Rust book; local Cargo 1.98.1 | Official chapter inspected | ownership/synchronization |

Revalidate when dependencies, platform, renderer, schema, model or channel requirements change. Supported guidance is not a claim of successful native execution. Resolve exact installed features before adopting version-sensitive examples.
