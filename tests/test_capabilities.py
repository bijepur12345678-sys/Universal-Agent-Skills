from __future__ import annotations

import unittest
from pathlib import Path

from universal_skills.capabilities import load_capabilities, route_task, validate_capabilities

ROOT = Path(__file__).resolve().parents[1]


class CapabilityRegistryTests(unittest.TestCase):
    def test_capability_catalogue_is_valid(self) -> None:
        self.assertEqual(validate_capabilities(ROOT), [])

    def test_catalogue_covers_all_22_domains(self) -> None:
        document = load_capabilities(ROOT)
        records = document["capabilities"]
        self.assertEqual(len(records), 88)
        self.assertEqual(len({item["domain"] for item in records}), 22)

    def test_every_domain_has_four_capabilities(self) -> None:
        records = load_capabilities(ROOT)["capabilities"]
        for domain in {item["domain"] for item in records}:
            self.assertEqual(sum(item["domain"] == domain for item in records), 4)

    def test_cloudflare_worker_task_routes_to_cloud_capability(self) -> None:
        results = route_task("build a Cloudflare Workers serverless API", root=ROOT, limit=5)
        self.assertTrue(results)
        self.assertEqual(results[0]["domain"], "cloud")
        self.assertEqual(results[0]["capability_id"], "cloud-serverless-apps")

    def test_youtube_analytics_routes_to_youtube(self) -> None:
        results = route_task("analyze YouTube channel analytics and audience retention", root=ROOT)
        self.assertTrue(results)
        self.assertEqual(results[0]["domain"], "youtube")
        self.assertEqual(results[0]["capability_id"], "youtube-analytics")

    def test_domain_filter_is_respected(self) -> None:
        results = route_task("build a responsive UI and React component", root=ROOT, domain="frontend")
        self.assertTrue(results)
        self.assertTrue(all(item["domain"] == "frontend" for item in results))

    def test_missing_tools_are_reported_not_hidden(self) -> None:
        results = route_task(
            "MCP server integration and OAuth scopes",
            root=ROOT,
            available_tools=set(),
        )
        self.assertTrue(results)
        self.assertTrue(results[0]["missing_tools"])
        self.assertFalse(results[0]["tools_ready"])

    def test_elevated_risk_requires_approval(self) -> None:
        records = load_capabilities(ROOT)["capabilities"]
        elevated = [item for item in records if item["risk_level"] == "elevated"]
        self.assertTrue(elevated)
        self.assertTrue(all(item["approval_required"] for item in elevated))

    def test_empty_task_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            route_task("  ", root=ROOT)


if __name__ == "__main__":
    unittest.main()
