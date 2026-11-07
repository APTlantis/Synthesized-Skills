---
name: rust-tauri-app-architect
description: Design, extend, and troubleshoot Rust/Tauri desktop applications, including IPC, state, capabilities, persistence, native processes, and frontend integration. Exclude general Rust tasks, unrelated web apps, and installer-only release work.
---

# Rust + Tauri Application Architect

Deliver a maintainable application change with explicit frontend/backend and OS boundaries. Inspect workspace instructions, Cargo/frontend manifests and locks, Tauri major, plugin versions, config, capabilities, entrypoints and existing tests. Use the existing frontend and package manager; do not migrate frameworks incidentally.

## Define the boundary

1. Trace one user action from UI through IPC, domain logic, storage/OS work and result display. Keep transport-specific code thin; make domain services independently testable.
2. Define serialized request/response/error types and ownership. Tauri v2 imports differ from v1; verify installed APIs before copying examples. See [workflows.md](references/workflows.md).
3. Treat frontend data as untrusted. Validate paths, identifiers, sizes and operations in Rust. Plugin scopes and application-command authorization are distinct: registered application commands are broadly callable by default unless enrolled in app permission controls. Do not assume a capability file alone confines custom Rust filesystem/process code.
4. Scope filesystem and shell access to necessary windows/origins/resources. Canonicalization, symlinks, nonexistent destinations and race conditions require deliberate handling. Avoid arbitrary shell-command IPC.

## Implement lifecycle and persistence

Own shared services through managed state with explicit synchronization. Keep locks short and avoid holding synchronous guards across await. Use appropriate blocking work isolation for expensive filesystem/CPU operations. Define cancellation, progress, timeout and shutdown behavior for long tasks.

Use platform path APIs and application data/config directories; do not depend on the working directory or executable folder being writable. Prefer TOML for new application config when appropriate, while preserving Tauri's actual supported schema/features. Version persisted schemas and protect atomic updates, backup and migrations.

For child processes specify executable/argv, environment, working directory and resource/lifetime limits. Consume stdout/stderr without deadlock, propagate nonzero exits, and clean up owned children. Events convey notifications/progress, not an implicit durable request/result protocol. Remove frontend listeners during teardown.

## Verify and deliver

Run relevant Rust formatting/check/tests and frontend type/build checks using pinned project tooling. Test IPC success, serialization failure, rejected input, permission denial, missing files, concurrent operations and error display. Verify OS-specific behavior on each claimed platform; conditional compilation is not native validation.

If WebView/SDK/toolchain dependencies are absent, test domain logic separately and mark native integration pending. Report source changes, architecture decisions, executed checks and remaining platform tests. Installer production belongs to Desktop Release & Installer Engineer; compilation alone is not an installer. Read [source-index.md](references/source-index.md) and [evaluation.toml](evaluation.toml) for evidence and scenarios.
