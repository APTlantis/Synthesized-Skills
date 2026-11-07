"""Read-only SVG lint. Python 3 standard library; not a sanitizer or renderer."""
import argparse
from collections import Counter
import json
import math
from pathlib import Path
import re
import xml.etree.ElementTree as ET

SVG = "http://www.w3.org/2000/svg"
URL = re.compile(r"url\(\s*(['\"]?)(.*?)\1\s*\)", re.I)


def inspect_svg(path):
    errors, warnings = [], []
    result = {"file": str(path), "errors": errors, "warnings": warnings}
    try:
        source = Path(path).read_text(encoding="utf-8-sig")
        if re.search(r"<!\s*(DOCTYPE|ENTITY)\b", source, re.I):
            errors.append("DTD/entity declarations are outside this checker's input policy.")
            return result
        root = ET.fromstring(source)
    except (OSError, UnicodeError, ET.ParseError) as exc:
        errors.append(f"Cannot read UTF-8 SVG XML: {exc}")
        return result
    if root.tag != f"{{{SVG}}}svg":
        errors.append("Root must be svg in the SVG namespace for standalone output.")
    try:
        values = [float(v) for v in re.split(r"[\s,]+", root.get("viewBox", "").strip())]
        if len(values) != 4 or not all(math.isfinite(v) for v in values) or min(values[2:]) <= 0:
            raise ValueError
    except ValueError:
        errors.append("viewBox must contain four finite numbers with positive width and height.")
    ids = Counter(el.get("id") for el in root.iter() if el.get("id") is not None)
    for ident, count in ids.items():
        if not ident or re.search(r"\s", ident):
            errors.append(f"Empty or whitespace-containing ID: {ident!r}")
        if count > 1:
            errors.append(f"Duplicate ID: {ident}")
    refs = set()
    for el in root.iter():
        tag = el.tag.rsplit("}", 1)[-1]
        if tag in {"script", "foreignObject", "image", "animate", "animateMotion", "animateTransform", "set"}:
            warnings.append(f"Review portability/content of element: {tag}")
        text_values = [el.text or ""] if tag == "style" else []
        if tag == "style":
            warnings.append("Style element needs separate CSS and dependency review.")
        for key, value in el.attrib.items():
            name = key.rsplit("}", 1)[-1]
            text_values.append(value)
            if name.lower().startswith("on"):
                warnings.append(f"Review event-handler attribute: {name}")
            if name == "href":
                if value.startswith("#"):
                    refs.add(value[1:])
                else:
                    warnings.append(f"Review nonlocal href on {tag}.")
            if name in {"aria-labelledby", "aria-describedby"}:
                refs.update(value.split())
        for value in text_values:
            for match in URL.finditer(value):
                target = match.group(2).strip()
                if target.startswith("#"):
                    refs.add(target[1:])
                else:
                    warnings.append("Review nonlocal CSS URL.")
    for ref in sorted(refs):
        if ref not in ids:
            errors.append(f"Missing local reference target: {ref!r}")
    if not root.get("width") or not root.get("height"):
        warnings.append("No explicit intrinsic width/height pair; confirm embedding layout.")
    if any(el.tag == f"{{{SVG}}}text" for el in root.iter()):
        warnings.append("Text present; verify fonts, glyph coverage, and layout in the target.")
    result["warnings"] = sorted(set(warnings))
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("files", nargs="+", type=Path)
    args = parser.parse_args()
    results = [inspect_svg(path) for path in args.files]
    print(json.dumps(results, indent=2, ensure_ascii=True))
    return int(any(result["errors"] for result in results))


if __name__ == "__main__":
    raise SystemExit(main())
