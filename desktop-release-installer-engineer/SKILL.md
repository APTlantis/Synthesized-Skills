---
name: desktop-release-installer-engineer
description: Prepare, build, inspect, and validate desktop distributables, installer targets, signing evidence, update artifacts, checksums, and release receipts. Use for Windows, Linux, or macOS release engineering. Exclude ordinary application development without packaging work.
---

# Desktop Release & Installer Engineer

Produce the requested distributables with evidence for each release stage. Obtain repository/ref, version, target OS/architecture, package formats, distribution channel, signing identity availability and installation-test scope. Inspect working-tree changes and existing release configuration before building; preserve unrelated artifacts.

## Plan targets and identity

1. Read manifests, lockfiles, bundler configuration, CI and prior release receipts. Reconcile application/package versions and package identities using format-specific rules. See [workflows.md](references/workflows.md).
2. Select bundle targets explicitly. Tauri v2 documents MSI/NSIS on Windows; do not assume MSIX is a native bundler target. MSIX needs a separate supported packaging route. Confirm current installed bundler capabilities.
3. Verify compiler, SDK, WebView/runtime, frontend build and platform dependencies. Choose build mode/target triple and output paths deliberately. A cross-compile is not evidence of target-native installer behavior.
4. Separate compilation, bundling, signing, signature verification, install/upgrade/uninstall, channel acceptance and publication. Each has its own evidence and can fail independently.

## Build and inspect

Use pinned project commands and record exact versions/configuration. Build to a known location and identify fresh artifacts from this invocation rather than selecting an old file by glob. Inspect format, architecture, identity, dependencies, entrypoint, version and embedded resources. Hash final bytes after any signing/metadata changes.

Use available secure signing infrastructure without logging private keys or credentials. Verify signature chain/timestamp with appropriate platform tooling. Development signing/trust is separate from public distribution. Never infer Store acceptance from a package build or local validation.

## Validate and recover

Test install, first launch, update over the supported previous version, repair where relevant, uninstall and user-data retention in an authorized disposable environment. Confirm shortcuts, file associations, runtime dependencies and per-user/per-machine behavior. Exercise updater signatures and compatibility separately from OS code signing.

On failure retain logs/config/receipts, distinguish app-build failure from bundler/signing failure, and rebuild only the affected stage when safe. Missing signing infrastructure permits a clearly labeled unsigned candidate if requested; it does not permit a signed-release claim. Missing native environments leave installation tests pending.

Deliver artifact paths, SHA-256, release receipt, exact completed stages and open gates. Optional Rust + Tauri Application Architect handles runtime/source changes. Read [source-index.md](references/source-index.md) and [evaluation.toml](evaluation.toml); revalidate channel/platform requirements before distribution.
