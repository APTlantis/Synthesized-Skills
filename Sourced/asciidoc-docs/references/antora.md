# Antora documentation sites

Antora collects versioned documentation from Git content sources and renders them using a UI bundle. For existing sites, use their playbook, dependency locks, and CI entry point. For a new site, consult the quickstart for Node requirements, install Antora locally in the project, and commit its package manifest and lockfile.

## Minimal local layout

| Path | Role |
| --- | --- |
| `antora-playbook.yml` | Site build configuration |
| `antora.yml` | Component descriptor at the content source root |
| `modules/ROOT/pages/index.adoc` | Start page |
| `modules/ROOT/nav.adoc` | Navigation listed in the component descriptor |
| `modules/ROOT/partials/` | Reusable content, addressed with `partial$` |
| `modules/ROOT/examples/` | Example sources, addressed with `example$` |
| `modules/ROOT/images/` | Page images |
| `modules/ROOT/attachments/` | Downloadable assets |

`antora.yml`

```yaml
name: operator
title: Operator Guide
version: '1.0'
nav:
  - modules/ROOT/nav.adoc
```

`modules/ROOT/nav.adoc`

```asciidoc
* xref:index.adoc[Overview]
```

`antora-playbook.yml`

```yaml
site:
  title: Operator Documentation
  start_page: operator::index.adoc
content:
  sources:
    - url: .
      branches: HEAD
ui:
  bundle:
    url: ./ui-bundle.zip
output:
  dir: ./build/site
runtime:
  log:
    failure_level: warn
```

For this example, run from the root of a Git repository with an initial commit, put a known Antora UI bundle at `ui-bundle.zip`, and place the descriptor and content at the repository root. For a docs subdirectory, set the content source's `start_path` and place the descriptor there. Run `npx --no-install antora antora-playbook.yml` after installing the project's dependencies. For shared builds, use a versioned UI bundle and explicitly select the intended Git branches or tags.

## Validation and recovery

- Serve the output locally over HTTP and check the landing page, navigation, cross-module links, and images. Check representative older versions and deployment subpaths when applicable. In CI, fail on warning diagnostics for new sites. For established sites, honor the project's policy and resolve inherited warnings deliberately.
- If a component is missing, check the Git URL, branch/tag selection, worktree behavior, `start_path`, and descriptor location. Verify the actual files visible to the selected source.
- If a page is generated but absent from navigation, check the descriptor's nav list and nav file contents. If an xref fails, inspect the target component, version, module, resource family, filename case, and anchor.
- For local previews without network, use a local UI bundle and local content sources. Preview generated output with the configured URL strategy before deployment.
- Keep Antora resource IDs in Antora content. If sharing content with standalone HTML or PDF, use compatible shared markup or thin target-specific entry points. Validate each target independently.

## Official references

- [Install and run Antora](https://docs.antora.org/antora/latest/install-and-run-quickstart/)
- [Standard directories](https://docs.antora.org/antora/latest/standard-directories/)
- [Git branch and worktree selection](https://docs.antora.org/antora/latest/playbook/content-branches/)
- [Xrefs and resource IDs](https://docs.antora.org/antora/latest/page/xref/)
- [UI bundle paths](https://docs.antora.org/antora/latest/playbook/ui-bundle-url/)
- [Build failure threshold](https://docs.antora.org/antora/latest/playbook/runtime-log-failure-level/)
