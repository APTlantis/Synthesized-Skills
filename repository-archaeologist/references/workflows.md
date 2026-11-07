# Evidence-first reconnaissance

Read-only starter commands, adapted to the actual repository and shell:

```text
git status --short
git rev-parse HEAD
rg --files -g '!node_modules' -g '!target' -g '!dist'
rg -n 'main|invoke_handler|createRoot|entry' src src-tauri
git log -n 10 -- path/to/owner
git log -S 'symbol_name' -- path/to/owner
git blame -L 10,35 -- path/to/owner
```

Missing paths and shallow history are limitations to record, not excuses to scan unrelated drives. Git ownership rejection does not justify changing global safe-directory settings. Verify the intended repository and use a narrowly scoped exception only when authorized/appropriate. Do not reset, stash, checkout, clean, fetch or update submodules as part of read-only reconnaissance.

Trace table:

| Stage | Evidence to find |
|---|---|
| Build entry | package/Cargo/project manifest, script and workspace membership |
| Runtime entry | actual main/module initialization and environment selection |
| Public interface | route/command/event registrations plus request/response shapes |
| Domain work | called service/function, side effects and errors |
| Storage/integration | connection ownership, migrations, paths, authentication boundary |
| Output | UI/render/serialized response and error handling |
| Validation | relevant test assertions and CI/build checks |

Finding format: `Claim — status — source path:line/symbol — implication — remaining check`. Example: “The build runs `src/main.ts`, while README points at `legacy.ts` — confirmed configuration discrepancy — package.json build script and import chain — update documentation or investigate obsolete path.” Do not claim the built app behaves correctly from this evidence alone.

Review negative evidence carefully: no search hit can result from a wrong scope, ignored files, dynamic registration, generated code or another language. Search definitions, exports, consumers, build inputs and feature gates before a deletion recommendation. Check tracked versus generated files and current configuration rather than treating every directory as an active subsystem.

Fixture for evaluation: a tiny repository with a manifest entrypoint, an imported service and JSON data file, a stale README naming a legacy entrypoint, a disabled feature and a test that covers the service. Expected output identifies the real import chain, mismatch and change fan-out with citations; it makes no writes and does not run arbitrary build scripts.
