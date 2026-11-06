from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from universal_skills.registry import RegistryError, load_module, search_catalog, validate_registry

ROOT = Path(__file__).resolve().parents[1]


class RegistryTests(unittest.TestCase):
    def test_repository_registry_is_valid(self) -> None:
        self.assertEqual(validate_registry(ROOT), [])

    def test_catalogue_has_one_public_entrypoint(self) -> None:
        catalog = json.loads((ROOT / "registry/catalog.json").read_text(encoding="utf-8"))
        entrypoints = [item for item in catalog["skills"] if item["entrypoint"]]
        self.assertEqual(len(entrypoints), 1)
        self.assertEqual(entrypoints[0]["path"], catalog["entrypoint"])

    def test_search_finds_github_research_module(self) -> None:
        results = search_catalog("GitHub repository source research", limit=5, root=ROOT)
        self.assertTrue(results)
        self.assertEqual(results[0]["id"], "github-source-research")

    def test_load_module_returns_first_party_instructions(self) -> None:
        text = load_module("license-provenance-review", root=ROOT)
        self.assertIn("A public repository is not public domain.", text)

    def test_unknown_module_is_rejected(self) -> None:
        with self.assertRaises(RegistryError):
            load_module("not-a-real-skill", root=ROOT)

    def test_path_traversal_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "registry").mkdir()
            (root / "skills").mkdir()
            catalog = {
                "schema_version": 1,
                "generated_at": "2026-11-06",
                "entrypoint": "../outside.md",
                "skills": [{
                    "id": "outside", "name": "Outside",
                    "description": "A sufficiently descriptive test module path traversal case.",
                    "domain": "agentic-ai", "path": "../outside.md",
                    "version": "0.1.0", "status": "experimental",
                    "tags": [], "source_ids": [], "license": "Apache-2.0",
                    "entrypoint": True
                }]
            }
            (root / "registry/catalog.json").write_text(json.dumps(catalog), encoding="utf-8")
            (root / "registry/sources.json").write_text(json.dumps({"schema_version": 1, "sources": []}), encoding="utf-8")
            (root / "registry/domains.json").write_text(json.dumps({"schema_version": 1, "domains": [{"id": "agentic-ai"}]}), encoding="utf-8")
            (root / "outside.md").write_text("do not load", encoding="utf-8")
            errors = validate_registry(root)
            self.assertTrue(any("Unsafe repository-relative path" in error for error in errors))

    def test_deprecated_modules_are_not_returned_by_search(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "registry").mkdir()
            (root / "registry/catalog.json").write_text(json.dumps({
                "schema_version": 1, "skills": [{
                    "id": "old-skill", "name": "Old Skill",
                    "description": "A deprecated old skill for testing search filtering.",
                    "domain": "agentic-ai", "path": "skills/old.md",
                    "version": "0.1.0", "status": "deprecated",
                    "tags": ["old"], "source_ids": [], "license": "Apache-2.0",
                    "entrypoint": True
                }]
            }), encoding="utf-8")
            self.assertEqual(search_catalog("old skill", root=root), [])


if __name__ == "__main__":
    unittest.main()
