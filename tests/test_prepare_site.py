"""Unit tests for documentation staging (stdlib only)."""

import tempfile
import unittest
from pathlib import Path

from scripts.prepare_site import stage_site


class TestPrepareSite(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.root = Path(self.temp_dir.name)
        for filename in (
            "README.md", "ROADMAP.md", "SYLLABUS.md",
            "CHANGELOG.md", "CONTRIBUTING.md", "AGENTS.md"
        ):
            (self.root / filename).write_text(f"# {filename}\n", encoding="utf-8")
        (self.root / "modules" / "03-agent-architecture").mkdir(parents=True)
        (self.root / "examples").mkdir()
        (self.root / "tests").mkdir()
        (self.root / "modules" / "03-agent-architecture" / "README.md").write_text(
            "# Agent module\n[Homepage](../../README.md)\n[Module](README.md)\n",
            encoding="utf-8"
        )
        (self.root / "examples" / "demo.py").write_text("print('hello')\n", encoding="utf-8")
        (self.root / "examples" / "cases.jsonl").write_text('{"id":"SIM-01"}\n', encoding="utf-8")

    def test_generates_homepage_and_preserves_module_index(self):
        output = self.root / ".site-src"
        staged = stage_site(self.root, output)
        self.assertGreaterEqual(staged, 8)
        self.assertTrue((output / "index.md").is_file())
        self.assertFalse((output / "README.md").exists())
        lesson = (output / "modules" / "03-agent-architecture" / "README.md").read_text()
        self.assertIn("[Homepage](../../index.md)", lesson)
        self.assertIn("[Module](README.md)", lesson)

    def test_copies_source_code_as_downloadable_asset(self):
        output = self.root / ".site-src"
        stage_site(self.root, output)
        self.assertEqual((output / "examples" / "demo.py").read_text(), "print('hello')\n")
        self.assertEqual((output / "examples" / "cases.jsonl").read_text(), '{"id":"SIM-01"}\n')

    def test_cleans_stale_generated_content(self):
        output = self.root / ".site-src"
        stage_site(self.root, output)
        (output / "stale.md").write_text("old", encoding="utf-8")
        stage_site(self.root, output)
        self.assertFalse((output / "stale.md").exists())

    def test_keeps_external_links_unchanged(self):
        (self.root / "ROADMAP.md").write_text(
            "[remote](https://github.com/example/docs/README.md)\n", encoding="utf-8"
        )
        stage_site(self.root, self.root / ".site-src")
        self.assertIn(
            "https://github.com/example/docs/README.md",
            (self.root / ".site-src" / "ROADMAP.md").read_text(encoding="utf-8"),
        )

    def test_rejects_unsafe_destinations(self):
        with self.assertRaises(ValueError):
            stage_site(self.root, self.root)
        with self.assertRaises(ValueError):
            stage_site(self.root, self.root / "modules")


if __name__ == "__main__":
    unittest.main()
