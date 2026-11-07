"""Synthetic integrity/recovery fixtures; no source-run changes."""
import hashlib
import json
from pathlib import Path
import tempfile
import unittest

from audit_run import audit


class AuditTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / 'source').mkdir()
        (self.root / 'source/input.png').write_bytes(b'fixture only; not an actual image')
        self.digest = hashlib.sha256((self.root / 'source/input.png').read_bytes()).hexdigest()
        self.identity = {'version': 1, 'prefix': 'apt', 'slug': 'fixture'}
        self.run = {'schema': 'aptlantis.theme-run.v1', 'name': 'Fixture', 'variant': 'dark',
                    'source_sha256': self.digest, 'theme_identity': self.identity,
                    'targets': ['website'], 'artifact_manifests': {'website': 'website/files.json'}}
        colors = '\n'.join(f'color_{i:02} = {{ hex = "#{i:02X}{i:02X}{i:02X}" }}' for i in range(1, 33))
        (self.root / 'palette.toml').write_text(
            f'[theme]\nvariant="dark"\nsource_sha256="{self.digest}"\n'
            '[theme.theme_identity]\nversion=1\nprefix="apt"\nslug="fixture"\n'
            '[palette.canonical]\n' + colors, encoding='utf-8')
        (self.root / 'website').mkdir()
        self.tokens = {'tokens': {'background': {'hex': '#010101', 'origin': {'source': 'color_01'}}}}
        self.write('website/tokens.json', self.tokens)
        token_hash = hashlib.sha256((self.root / 'website/tokens.json').read_bytes()).hexdigest()
        self.manifest = {'schema': 'aptlantis.artifact-manifest.v2', 'target': 'website',
                         'theme_identity': self.identity,
                         'files': [{'file': 'tokens.json', 'role': 'tokens', 'sha256': token_hash}]}
        self.write('run.json', self.run)
        self.write('website/files.json', self.manifest)
        self.write('semantics.json', {'roles': {'background': 'color_01'}, 'findings': []})
        self.write('provenance.json', {'sha256': self.digest})

    def write(self, relative, value):
        (self.root / relative).write_text(json.dumps(value), encoding='utf-8')

    def test_valid_manifest_relative_tokens(self):
        result = audit(self.root)
        self.assertEqual(result['errors'], [])
        self.assertEqual(result['targets']['website']['token_count'], 1)

    def test_tampered_artifact(self):
        self.write('website/tokens.json', {'tokens': {}})
        self.assertTrue(any('hash mismatch' in e for e in audit(self.root)['errors']))

    def test_css_and_json_share_token_role(self):
        css = self.root / 'website/tokens.css'
        css.write_text(':root { --background: #010101; }', encoding='utf-8')
        self.manifest['files'].insert(0, {'file': 'tokens.css', 'role': 'tokens',
            'logical_name': 'tokens.css', 'sha256': hashlib.sha256(css.read_bytes()).hexdigest()})
        self.write('website/files.json', self.manifest)
        self.assertEqual(audit(self.root)['errors'], [])

    def test_escape(self):
        self.manifest['files'][0]['file'] = '../../outside.json'
        self.write('website/files.json', self.manifest)
        self.assertTrue(any('escapes' in e for e in audit(self.root)['errors']))

    def test_missing_target(self):
        (self.root / 'website/files.json').unlink()
        self.assertFalse(audit(self.root)['integrity_checks_passed'])

    def test_identity_conflict(self):
        self.run['theme_identity']['version'] = 2
        self.write('run.json', self.run)
        self.assertTrue(any('identity' in e for e in audit(self.root)['errors']))

    def test_semantic_unknown(self):
        self.write('semantics.json', {'roles': {'error': 'invented'}})
        self.assertTrue(any('Unknown canonical' in e for e in audit(self.root)['errors']))

    def test_invalid_json(self):
        (self.root / 'run.json').write_text('{', encoding='utf-8')
        self.assertFalse(audit(self.root)['integrity_checks_passed'])

    def test_source_tampering(self):
        (self.root / 'source/input.png').write_bytes(b'changed')
        self.assertTrue(any('original source' in e for e in audit(self.root)['errors']))

    def test_schema_drift(self):
        self.run['schema'] = 'future'
        self.write('run.json', self.run)
        self.assertTrue(any('Unsupported run schema' in e for e in audit(self.root)['errors']))


if __name__ == '__main__':
    unittest.main()
