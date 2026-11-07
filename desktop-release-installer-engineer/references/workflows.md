# Target-specific release checklist

| Target | Preparation | Required evidence boundary |
|---|---|---|
| Windows MSI | Installed bundler/WiX integration, architecture, upgrade identity and scope | Actual MSI inspection plus install/upgrade/uninstall; `.exe` compilation is insufficient |
| Windows NSIS | Bundler/NSIS version, install mode, shortcuts, runtime dependencies | Fresh installer executable and lifecycle logs |
| Windows MSIX | Separate packaging project/toolchain, manifest identity/publisher, capabilities and assets | Inspect manifest/package; verify signing and trust separately; Store channel rules checked at release time |
| Linux AppImage | Appropriate Linux build environment, libraries/assets and runtime assumptions | Actual AppImage and launch on supported distributions; portability is bounded by tested environments |
| Linux deb/rpm | Explicit distribution/dependency metadata | Format inspection and package-manager lifecycle in disposable native targets |
| macOS app/dmg | macOS SDK/build tools, bundle ID, entitlements and channel | Bundle/signature verification; notarization/stapling where required, Gatekeeper/native testing |

Version synchronization is mapping, not blindly identical strings: Cargo/frontend SemVer, Windows package version fields and installer upgrade rules have different syntax/ranges. Preserve stable application identity across upgrades unless a deliberate migration says otherwise. Record the mapping and reject ambiguous prerelease conversions.

For Tauri inspect the resolved v2 CLI's build/bundle help and `bundle.targets`, then choose requested formats explicitly using project scripts. Common output directories under `target/.../release/bundle` are hints; target triples/custom target dirs change paths. Discover from actual logs and verify file modification/hash evidence.

Release receipt (project-defined TOML example, not a platform standard):

```toml
version = "1.2.3"
source_revision = "record-actual-revision"
working_tree = "clean-or-described"
target = "x86_64-pc-windows-msvc"
build_mode = "release"
[[artifacts]]
path = "artifacts/app-installer.exe"
sha256 = "record-actual-final-hash"
signing = "unsigned"
installation_test = "not-run"
```

Add actual compiler/bundler/SDK versions, timestamps, build command/config hashes, package identity, dependency lock hashes, signing verifier output and test logs when applicable. A checksum detects byte changes; it does not authenticate the publisher without a trusted distribution/signature channel.

CI: use platform jobs with pinned dependencies, protected signing secrets, explicit artifact collection and evidence retention. Avoid placing certificate material in artifacts. Updater metadata must point to the exact tested version/architecture and final bytes. Test interrupted updates and data-schema compatibility; never use a user's live installation as a disposable test environment.
