# Standalone HTML and PDF

Prefer the locked project toolchain, including Bundler wrappers where present. The following CLI examples assume trusted source, installed Ruby CLIs, the current directory as the document root, and a writable output directory named build. Create that directory first.

```sh
asciidoctor --version
asciidoctor --failure-level=WARN -o build/guide.html guide.adoc
asciidoctor-pdf --version
asciidoctor-pdf --failure-level=WARN -o build/guide.pdf guide.adoc
```

- HTML is the default backend. Use `-e` for an embeddable HTML fragment when a host supplies the surrounding page. A standalone page can still depend on images, fonts, or scripts. Test offline if portability is required.
- Keep HTML styles in CSS and verify stylesheet resolution, including linked assets after moving output into build. A rendered page with no styling may be a fragment, reference a missing stylesheet, or use restrictive rendering settings.
- Asciidoctor PDF uses a YAML theme. Apply an existing theme with `-a pdf-theme=themes/print-theme.yml` and set `pdf-fontsdir` if needed. Check font glyph coverage, heading hierarchy, page breaks, clipped code/tables, and internal links. Inspect rendered pages, especially where wide blocks or large images meet page breaks.
- A missing include can come from the base directory, path case, a missing file, or safe mode. Check the effective paths and security mode before changing settings. Ruby CLI defaults to unsafe and its API defaults to secure. Secure disables includes. Safe mode permits local includes within its base directory but does not validate symlink targets.
- Inspect the diagnostics even when there is output. Validate emitted HTML links and asset paths separately. Warnings alone cannot establish that every link works.

## Official references

- [Asciidoctor CLI](https://docs.asciidoctor.org/asciidoctor/latest/cli/man1/asciidoctor/)
- [HTML stylesheet modes](https://docs.asciidoctor.org/asciidoctor/latest/html-backend/stylesheet-modes/)
- [Safe modes](https://docs.asciidoctor.org/asciidoctor/latest/safe-modes/)
- [PDF conversion](https://docs.asciidoctor.org/pdf-converter/latest/convert-to-pdf/)
- [Apply a PDF theme](https://docs.asciidoctor.org/pdf-converter/latest/theme/apply-theme/)
