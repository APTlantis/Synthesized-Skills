"""Run with: python -m unittest discover -s scripts -p test_*.py"""
from pathlib import Path
import tempfile
import unittest

from validate_svg import inspect_svg


class SVGChecks(unittest.TestCase):
    def check(self, body="", attrs='viewBox="0 0 24 24" width="24" height="24"'):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "case.svg"
            path.write_text(f'<svg xmlns="http://www.w3.org/2000/svg" {attrs}>{body}</svg>', encoding="utf-8")
            return inspect_svg(path)

    def test_valid_geometry(self):
        self.assertFalse(self.check('<circle cx="12" cy="12" r="4"/>')["errors"])

    def test_bad_viewboxes(self):
        for value in ["", "0 0 0 24", "0 0 -1 24", "0 0 nan 24", "0 0 inf 24", "0 0 24", "0 0 24 24 5"]:
            with self.subTest(value=value):
                self.assertTrue(self.check(attrs=f'viewBox="{value}"')["errors"])

    def test_duplicate_id(self):
        self.assertTrue(self.check('<g id="a"/><g id="a"/>')["errors"])

    def test_valid_refs(self):
        self.assertFalse(self.check('<defs><linearGradient id="paint"/></defs><rect fill="url(#paint)"/><title id="t">Art</title><g aria-labelledby="t"/>')["errors"])

    def test_broken_refs(self):
        for body in ['<use href="#missing"/>', '<rect fill="url(\'#missing\')"/>', '<g aria-describedby="missing"/>', '<style>.a {fill:url(#missing)}</style>']:
            with self.subTest(body=body):
                self.assertTrue(self.check(body)["errors"])

    def test_portability_warnings(self):
        for body in ['<script/>', '<g onclick="x()"/>', '<image href="https://example.test/a.png"/>', '<text>Hi</text>', '<style>@import "x.css";</style>']:
            with self.subTest(body=body):
                self.assertTrue(self.check(body)["warnings"])

    def test_parse_error(self):
        self.assertTrue(self.check('<g>')["errors"])

    def test_bad_ids(self):
        self.assertTrue(self.check('<g id="a b"/>')["errors"])

    def test_missing_file(self):
        self.assertTrue(inspect_svg(Path("nonexistent-file-for-svg-tests.svg"))["errors"])

    def test_dtd_policy(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "case.svg"
            path.write_text('<!DOCTYPE svg><svg/>', encoding="utf-8")
            self.assertIn("DTD/entity", inspect_svg(path)["errors"][0])

    def test_namespace(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "case.svg"
            path.write_text('<svg viewBox="0 0 24 24"/>', encoding="utf-8")
            self.assertTrue(inspect_svg(path)["errors"])


if __name__ == "__main__":
    unittest.main()
