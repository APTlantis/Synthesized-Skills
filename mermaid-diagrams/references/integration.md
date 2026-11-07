# Integration and rendering

Use the project's installed Mermaid version. These patterns follow the current documented async API; older hosts need their own version-compatible path. No runtime dependencies are bundled with this skill.

## Browser or bundled application

Run this in an application module with the installed `mermaid` dependency and an available DOM:

```javascript
import mermaid from 'mermaid';

mermaid.initialize({ startOnLoad: false, securityLevel: 'strict' });
await mermaid.run({ querySelector: '.mermaid' });
```

Place trusted source in the selected elements as text, not as unsanitized HTML. For dynamically supplied strings, assign `textContent` rather than interpolating them into `innerHTML`. Initialize once at the application's owning boundary. For later updates, restore fresh source into the intended elements and account for the framework's lifecycle rather than blindly rerunning every processed element.

For explicit rendering:

```javascript
const result = await mermaid.parse(source);
const { svg, bindFunctions } = await mermaid.render(uniqueRenderId, source);
// Mount svg only through the host's approved SVG insertion path.
// If supported and required, bindFunctions?.(mountedContainer) afterwards.
```

`parse` is asynchronous and normally throws on invalid syntax. With `{ suppressErrors: true }`, invalid syntax returns `false`; test that result instead of treating promise resolution as success. Parsing still depends on the installed build and environment; it is not universally a DOM-free Node API. `render` needs suitable browser/DOM support. `run` is the modern alternative to deprecated `init`; do not copy older initialization patterns without checking the project's version.

Make render IDs unique within the page and avoid conflicting library instances. Wait for relevant fonts before measuring output. An SVG using HTML labels or CSS may behave differently in an image element, converter, and inline DOM; test the actual delivery context. Rendering untrusted source requires the host's security and resource policies even when parsing succeeds.

## Per-diagram configuration

Where supported, frontmatter can sit before the declaration in raw source:

```text
---
config:
  theme: base
  themeVariables:
    primaryColor: '#E8F2FA'
    primaryTextColor: '#183247'
    primaryBorderColor: '#38617D'
    lineColor: '#38617D'
---
flowchart LR
    draft["Draft"] --> review["Review"]
```

This is an illustrative palette, not a mandated theme. Use documented hex color values for custom theme variables. Check that the renderer actually applies them; acceptance by the parser does not prove a key is effective. Prefer frontmatter for new diagram-specific configuration on compatible hosts; preserve a working legacy integration unless changing it is in scope. The owning host may restrict configuration, and diagram text must not override its security policy.

## CLI exports

The official package is `@mermaid-js/mermaid-cli`; its executable is `mmdc`. Find an existing local executable first. If installing for a task, select an exact compatible version and use a project-local or isolated location rather than an unpinned global installation. Record the resolved Mermaid core version too; CLI and core versions need not match. Chromium/Puppeteer and browser availability are separate runtime requirements. Check installed help for browser configuration and supported options.

```text
mmdc --version
mmdc --help
mmdc -i diagram.mmd -o diagram.svg
mmdc -i diagram.mmd -o diagram.png -t dark -b transparent
```

Run with paths appropriate to the shell and quote paths containing spaces. Use a new output destination for a review derivative. SVG is the usual vector export; request PNG/PDF only when needed. Markdown-to-Markdown CLI conversion can generate linked assets and rewrite the document: inspect output paths and review the resulting document before replacing an original.

If the browser fails to launch, inspect executable availability, Puppeteer compatibility, and environment permissions. Do not turn off the browser sandbox as a routine workaround. If dependencies cannot be installed or a runtime remains unavailable, deliver source and state precisely which checks were not executed.
