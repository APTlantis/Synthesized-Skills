# Pipeline Brand System skill

One skill with focused references turns selected Logos-And-Theming runs into a comprehensive identity and implementable design system. It covers strategic/verbal identity, marks, visual foundations, traceable tokens, component states, applications, specimens, governance and validation.

Start with [SKILL.md](SKILL.md). The skill is portable; its audit helper requires Python 3.11+ and no third-party packages. Run the helper against a selected pipeline run, not the whole output collection. Source folders remain read-only.

Example invocation after installing or explicitly loading this skill:

> Use pipeline-brand-system to build a brand identity and design system from D:/CTS/Logos-And-Theming/output/apt-Clojure. Preserve the canonical palette and artwork, and produce a brand guide, linked tokens, component specifications and offline specimens in a fresh destination. Label unsupported strategic decisions as proposals.

For collection requests, the skill first establishes which run or brand family is intended. The Clojure screenshot was used to identify available output types, not as an instruction to produce that brand now.

## Package contents

- `SKILL.md`: entry point and complete operational workflow.
- `references/`: pipeline intake, identity, system architecture, delivery contract, validation and source evidence.
- `scripts/audit_run.py`: manifest/hash/source/identity audit, JSON stdout, exit 0 or 2.
- `scripts/test_audit_run.py`: ten synthetic integrity and recovery tests.
- `VALIDATION.md`: actual checks and known limits.

Install by placing the `pipeline-brand-system` folder inside the skill directory used by your agent. This deliverable is packaged, not installed. No pipeline files, public copies or native application settings were changed.

The proposed design-system token format is explicitly local, not claimed to be a standards-compliant interchange format. Brand assets and fonts are not bundled; distribution rights must be established when producing a brand package.
