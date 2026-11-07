# IPC and service patterns

Illustrative Tauri v2 command (integrate into the existing builder; not a complete app):

```rust
#[tauri::command]
fn greet(user_name: String) -> Result<String, String> {
    let name = user_name.trim();
    if name.is_empty() || name.len() > 128 {
        return Err("Provide a name of 1 to 128 bytes".into());
    }
    Ok(format!("Hello, {name}"))
}
// Add to the existing single handler registration:
// .invoke_handler(tauri::generate_handler![greet, other_existing_commands])
```

```typescript
import { invoke } from '@tauri-apps/api/core';
const message = await invoke<string>('greet', { userName: 'Ada' });
```

Handle rejection in the UI and expose an actionable message. Default argument naming is camelCase from Rust snake_case unless configured otherwise. TypeScript generic assertions do not validate runtime payloads. A serializable structured error with a stable code is preferable to arbitrary strings for larger applications; redact internal paths/secrets as appropriate.

Permission review: inspect `src-tauri/capabilities` and plugin permission identifiers against installed schemas. Capabilities can target windows/webviews and platforms; combining grants can enlarge authority. For application commands inspect `tauri_build::AppManifest::commands` enrollment and generated permission definitions. Backend authorization is still required for operations with user-selected roots or sensitive application state. Do not copy broad allow-all shell/filesystem grants from examples.

State: keep transport, domain, persistence and OS adapters separate when their dependencies warrant it. Store a service in managed state and keep its fields synchronized rather than spreading global locks. Plan poison/error recovery; `Arc` provides shared ownership, not automatic thread safety of arbitrary contents. Test cancellation and stale UI results so a completed earlier operation cannot overwrite newer user intent.

Persistence: resolve OS paths through the version-correct Tauri path API or a project abstraction. Use same-directory staged writes for replaceable config, validate before replacement and test interrupted migrations on copies. Avoid lossy string conversion of native paths in core filesystem logic; define an explicit serialized path contract at IPC boundaries.

Testing layers: pure domain tests; adapter tests in disposable directories; command serialization/error tests; frontend loading/error/progress behavior; native WebView end-to-end tests; platform-specific integration. Record which layers executed. `cargo check --locked` can require cached dependencies or authorized network access; use an offline check only when the needed cache is present, and report missing crates accurately.
