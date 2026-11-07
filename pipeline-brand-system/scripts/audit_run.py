"""Read-only audit of current Logos-And-Theming runs; Python 3.11+, stdlib.

JSON to stdout; exit 0 for integrity checks passed, 2 for errors.
Does not execute source code, extract archives, render HTML, or modify inputs.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import sys
import tomllib


def sha256(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def audit(root):
    root = Path(root).resolve()
    report = {'schema': 'pipeline-brand-system.audit.v1', 'root': str(root),
              'errors': [], 'warnings': [], 'targets': {}, 'checked_files': 0}
    errors = report['errors']

    def bounded(base, relative):
        if not isinstance(relative, str) or not relative:
            raise ValueError('Expected a nonempty relative path')
        rel = Path(relative)
        if rel.is_absolute() or rel.drive or relative.startswith(('\\', '/')):
            raise ValueError(f'Absolute path refused: {relative}')
        path = (base / rel).resolve()
        if not path.is_relative_to(root):
            raise ValueError(f'Path escapes selected run: {relative}')
        return path

    def read(relative, base=root):
        path = bounded(base, relative)
        raw = path.read_bytes()
        report['checked_files'] += 1
        return (tomllib.loads(raw.decode('utf-8-sig')) if path.suffix == '.toml'
                else json.loads(raw.decode('utf-8-sig')))

    try:
        run = read('run.json')
        if run.get('schema') != 'aptlantis.theme-run.v1':
            raise ValueError('Unsupported run schema; inspect current/legacy contracts')
        palette = read('palette.toml')
        canonical = palette['palette']['canonical']
        if len(canonical) != 32:
            errors.append(f'Expected 32 canonical entries, got {len(canonical)}')
        for key, entry in canonical.items():
            if not re.fullmatch(r'#[0-9a-fA-F]{6}', entry['hex']):
                errors.append(f'Invalid canonical hex: {key}')
        theme = palette['theme']
        if theme.get('variant') != 'dark' or run.get('variant') != 'dark':
            errors.append('Expected dark variant')
        identity = run.get('theme_identity')
        if not identity or identity != theme.get('theme_identity'):
            errors.append('Run/palette identity missing or inconsistent')
        source_hash = run.get('source_sha256')
        if not isinstance(source_hash, str) or not re.fullmatch('[0-9a-fA-F]{64}', source_hash):
            errors.append('Missing or invalid source SHA-256')
        if source_hash != theme.get('source_sha256'):
            errors.append('Run/palette source hashes disagree')
        report.update(identity=identity, name=run.get('name'), canonical=canonical,
                      source_sha256=source_hash,
                      recorded_native_acceptance=run.get('native_application_acceptance', 'unknown'))
        semantics = read('semantics.json')
        for role, source in semantics['roles'].items():
            if source not in canonical:
                errors.append(f'Unknown canonical reference: {role} -> {source}')
        report['semantics'] = semantics
        report['warnings'].extend(semantics.get('findings', []))
        provenance = read('provenance.json')
        if provenance.get('sha256') != source_hash:
            errors.append('Provenance source hash disagrees')
        source_dir = bounded(root, 'source')
        sources = []
        for item in sorted(source_dir.iterdir()):
            item = bounded(root, str(item.relative_to(root)))
            if item.is_file():
                sources.append({'file': str(item.relative_to(root)), 'sha256': sha256(item)})
        report['sources'] = sources
        if not any(item['sha256'] == source_hash for item in sources):
            errors.append('No original source file matches recorded source hash')
        manifests = run['artifact_manifests']
        if not isinstance(manifests, dict):
            raise ValueError('artifact_manifests must be an object')
        if set(run['targets']) != set(manifests):
            errors.append('Selected targets and manifest targets disagree')
        for target, relative in manifests.items():
            result = {'manifest': relative, 'files': []}
            report['targets'][target] = result
            try:
                manifest_path = bounded(root, relative)
                manifest = read(relative)
                if manifest.get('schema') != 'aptlantis.artifact-manifest.v2':
                    raise ValueError('Unsupported artifact manifest schema')
                if manifest.get('target') != target or manifest.get('theme_identity') != identity:
                    errors.append(f'{target}: manifest identity/target mismatch')
                seen = set()
                for entry in manifest['files']:
                    path = bounded(manifest_path.parent, entry['file'])
                    if path in seen:
                        errors.append(f'{target}: duplicate file {entry["file"]}')
                    seen.add(path)
                    actual = sha256(path)
                    report['checked_files'] += 1
                    if actual != entry['sha256']:
                        errors.append(f'{target}: hash mismatch {entry["file"]}')
                    result['files'].append({'file': str(path.relative_to(root)),
                                            'role': entry.get('role'),
                                            'logical_name': entry.get('logical_name'),
                                            'sha256': actual})
                    if entry.get('role') == 'tokens' and path.suffix.lower() == '.json':
                        tokens = read(entry['file'], manifest_path.parent)
                        for name, token in tokens['tokens'].items():
                            source = token.get('origin', {}).get('source')
                            if source not in canonical:
                                errors.append(f'{target}: invalid token origin {name} -> {source}')
                        result['token_count'] = len(tokens['tokens'])
            except (OSError, ValueError, KeyError, TypeError, AttributeError) as exc:
                errors.append(f'{target}: {exc}')
    except (OSError, ValueError, KeyError, TypeError, AttributeError) as exc:
        errors.append(f'Intake failed: {exc}')
    report['integrity_checks_passed'] = not errors
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('run', type=Path)
    args = parser.parse_args()
    report = audit(args.run)
    json.dump(report, sys.stdout, ensure_ascii=True, indent=2)
    sys.stdout.write('\n')
    return 0 if report['integrity_checks_passed'] else 2


if __name__ == '__main__':
    raise SystemExit(main())
