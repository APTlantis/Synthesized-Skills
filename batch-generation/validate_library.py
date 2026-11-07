"""Read-only package checks; writes only the requested JSON evidence report.

Requires Python 3.11+ and PyYAML. Not an agent activation or task evaluator.
Run from any directory: python validate_library.py [--report PATH]
"""
from pathlib import Path
import argparse
import hashlib
import json
import re
import tomllib
from urllib.parse import unquote, urlsplit
import yaml

ROOT = Path(__file__).resolve().parent.parent


def validate():
    names = json.loads((ROOT / 'batch-generation/skill-names.json').read_text())
    problems, packages = [], []
    for name in names:
        folder = ROOT / name
        errors = []
        try:
            text = (folder / 'SKILL.md').read_text(encoding='utf-8')
            match = re.match(r'\A---\r?\n(.*?)\r?\n---\r?\n', text, re.S)
            if not match:
                raise ValueError('Missing YAML frontmatter')
            meta = yaml.safe_load(match[1])
            assert isinstance(meta, dict), 'Frontmatter must be a mapping'
            assert meta.get('name') == name, 'Name differs from directory'
            assert re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', name), 'Invalid name'
            assert len(name) <= 64, 'Name too long'
            assert isinstance(meta.get('description'), str) and 0 < len(meta['description']) <= 1024, 'Invalid description'
            assert '<' not in meta['description'] and '>' not in meta['description'], 'Description contains angle brackets'
            assert len(text.splitlines()) <= 500, 'Core exceeds configured line limit'
            assert 'evaluation.toml' in text and 'references/source-index.md' in text, 'Missing evidence links'
            plan = tomllib.loads((folder / 'evaluation.toml').read_text(encoding='utf-8'))
            assert plan['skill'] == name, 'Plan identity mismatch'
            counts = {kind: sum(c['kind'] == kind for c in plan['cases']) for kind in ('positive', 'negative', 'execution', 'recovery', 'integration')}
            for kind, minimum in {'positive': 3, 'negative': 3, 'execution': 2, 'recovery': 1, 'integration': 1}.items():
                assert counts[kind] >= minimum, f'Insufficient {kind} cases'
            assert len({c['id'] for c in plan['cases']}) == len(plan['cases']), 'Duplicate case IDs'
            assert all(c['prompt'] and c['expected'] and c['status'] == 'not-run' for c in plan['cases']), 'Invalid or unsupported agent trial status'
            for file in folder.rglob('*.md'):
                body = file.read_text(encoding='utf-8')
                # Examples inside fenced/inline code are not package links.
                body = re.sub(r'^(`{3,}|~{3,}).*?^\1\s*$', '', body, flags=re.M | re.S)
                body = re.sub(r'(`+).*?\1', '', body, flags=re.S)
                for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)', body):
                    target = target.strip('<>')
                    if urlsplit(target).scheme or target.startswith('#'):
                        continue
                    local = (file.parent / unquote(target.split('#')[0])).resolve()
                    assert local.is_relative_to(folder.resolve()), f'Nonportable package link: {file.name}: {target}'
                    assert local.exists(), f'Broken local link: {file.name}: {target}'
            packages.append(dict(name=name, status='pass', core_lines=len(text.splitlines()), cases=counts))
        except (OSError, ValueError, AssertionError, KeyError, TypeError, yaml.YAMLError, tomllib.TOMLDecodeError) as exc:
            errors.append(str(exc))
            packages.append(dict(name=name, status='fail', errors=errors))
            problems.extend(f'{name}: {e}' for e in errors)
    baseline = json.loads((ROOT / 'batch-generation/preservation-baseline.json').read_text())
    changed = [path for path, digest in baseline.items() if not (ROOT / path).is_file() or hashlib.sha256((ROOT / path).read_bytes()).hexdigest() != digest]
    problems.extend('Preserved file changed: ' + path for path in changed)
    for filename in ('SKILL-CATALOG.md', 'SOURCE-INVENTORY.md', 'VALIDATION-REPORT.md', 'batch-generation/INVENTORY-AND-DESIGN.md'):
        file = ROOT / filename
        if not file.is_file():
            problems.append('Missing library deliverable: ' + filename)
            continue
        body = file.read_text(encoding='utf-8')
        body = re.sub(r'^(`{3,}|~{3,}).*?^\1\s*$', '', body, flags=re.M | re.S)
        body = re.sub(r'(`+).*?\1', '', body, flags=re.S)
        for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)', body):
            if urlsplit(target).scheme or target.startswith('#'):
                continue
            local = (file.parent / unquote(target.split('#')[0])).resolve()
            if not local.is_relative_to(ROOT.resolve()) or not local.exists():
                problems.append(f'Broken library link in {filename}: {target}')
    assert len(names) == 12 and len(set(names)) == 12, 'Expected 12 distinct new skills'
    return dict(status='fail' if problems else 'pass', packages=packages, existing_files_checked=len(baseline), preserved_files_changed=changed, problems=problems, limits='Checks package structure and plan counts only; does not evaluate activation, technical completeness, or runtime behavior.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    report = validate()
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report, indent=2))
    raise SystemExit(report['status'] != 'pass')
