from __future__ import annotations

import unittest

from printline.workflow import ValidationError, WorkflowTemplate, parse_recipe
from tests.support import DEFAULT_RECIPE, project_root


class WorkflowTests(unittest.TestCase):
    def setUp(self) -> None:
        self.template = WorkflowTemplate(project_root() / "workflows" / "base_workflow.json")

    def test_parameterizes_real_comfyui_graph(self) -> None:
        recipe = parse_recipe(DEFAULT_RECIPE)
        graph = self.template.compile(recipe, "printline/seed-240817")
        nodes = {details["class_type"]: details for details in graph.values()}

        self.assertEqual(nodes["KSampler"]["inputs"]["seed"], 240817)
        self.assertEqual(nodes["KSampler"]["inputs"]["steps"], 20)
        self.assertEqual(nodes["EmptyLatentImage"]["inputs"]["width"], 512)
        positive_id = str(nodes["KSampler"]["inputs"]["positive"][0])
        self.assertEqual(graph[positive_id]["inputs"]["text"], DEFAULT_RECIPE["prompt"])

    def test_same_recipe_has_same_workflow_digest(self) -> None:
        recipe = parse_recipe(DEFAULT_RECIPE)
        one = self.template.compile(recipe, "printline/seed-240817")
        two = self.template.compile(recipe, "printline/seed-240817")
        self.assertEqual(self.template.digest(one), self.template.digest(two))

    def test_rejects_unknown_fields_and_out_of_contract_size(self) -> None:
        bad = {**DEFAULT_RECIPE, "width": 2000, "height": 694, "callback_url": "x"}
        with self.assertRaisesRegex(ValidationError, "Unsupported field"):
            parse_recipe(bad)
        bad.pop("callback_url")
        with self.assertRaisesRegex(ValidationError, "Size must"):
            parse_recipe(bad)

    def test_rejects_empty_and_oversized_prompts(self) -> None:
        with self.assertRaisesRegex(ValidationError, "Prompt is required"):
            parse_recipe({**DEFAULT_RECIPE, "prompt": "  "})
        with self.assertRaisesRegex(ValidationError, "at most 600"):
            parse_recipe({**DEFAULT_RECIPE, "prompt": "x" * 601})


if __name__ == "__main__":
    unittest.main()
