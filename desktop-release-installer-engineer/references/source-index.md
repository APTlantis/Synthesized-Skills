# Source evidence

Inspected: 2026-11-06 (America/New_York). Official references are paraphrased; no external code or assets are vendored. Rolling docs are not pinned compatibility guarantees. Execution evidence is reported separately.

| Source | Applicable version | Verification | Purpose |
|---|---|---|---|
| [Tauri distribute](https://v2.tauri.app/distribute/) | Tauri v2 | Official guide inspected | bundle targets |
| [Tauri Windows](https://v2.tauri.app/distribute/windows-installer/) | Tauri v2 | Official guide inspected | MSI/NSIS versus separate MSIX route |
| [MSIX](https://learn.microsoft.com/en-us/windows/msix/overview) | current Windows docs | Official overview inspected | identity/packaging |
| [MSI](https://learn.microsoft.com/en-us/windows/win32/msi/windows-installer-portal) | Windows Installer | Official overview inspected | installer lifecycle |
| [NSIS](https://nsis.sourceforge.io/Docs/) | check installed version | Official manual inspected | installer configuration |
| [AppImage](https://docs.appimage.org/packaging-guide/overview.html) | rolling | Official overview inspected | Linux packaging routes |
| [Apple notarization](https://developer.apple.com/documentation/security/notarizing-macos-software-before-distribution) | current channel rules | Landing page only; detailed content not verified | revalidation pointer; no acceptance claim |

Revalidate when dependencies, platform, renderer, schema, model or channel requirements change. Supported guidance is not a claim of successful native execution. Resolve exact installed features before adopting version-sensitive examples.
