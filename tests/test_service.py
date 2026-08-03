from __future__ import annotations

import unittest

from printline.service import JobService
from tests.support import DEFAULT_RECIPE, TempProject


class ServiceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = TempProject()
        self.service = JobService(self.temp.root, mock_step_delay=0)

    def tearDown(self) -> None:
        self.service.close()
        self.temp.close()

    def test_runs_queued_recipe_and_records_artifact_metadata(self) -> None:
        queued = self.service.create(DEFAULT_RECIPE)
        self.assertEqual(queued["status"], "queued")
        finished = self.service.wait(queued["id"])

        self.assertEqual(finished["status"], "succeeded")
        self.assertEqual(finished["progress"], 100)
        self.assertEqual(finished["workflow"]["format"], "comfyui-api")
        self.assertEqual(finished["artifact"]["mime_type"], "image/png")
        self.assertEqual(
            finished["artifact"]["provider_metadata"]["fixture_boundary"],
            "showcase image; not a live ComfyUI execution",
        )
        self.assertTrue(
            (self.temp.root / "outputs" / finished["artifact"]["filename"]).is_file()
        )

    def test_same_seed_and_settings_produce_same_artifact_hash(self) -> None:
        first = self.service.wait(self.service.create(DEFAULT_RECIPE)["id"])
        second = self.service.wait(self.service.create(DEFAULT_RECIPE)["id"])
        self.assertEqual(first["workflow"]["digest"], second["workflow"]["digest"])
        self.assertEqual(first["artifact"]["sha256"], second["artifact"]["sha256"])

    def test_provider_failure_is_actionable_and_retry_succeeds(self) -> None:
        failed = self.service.wait(
            self.service.create({**DEFAULT_RECIPE, "simulate_failure": True})["id"]
        )
        self.assertEqual(failed["status"], "failed")
        self.assertEqual(failed["error"]["code"], "provider_failure")
        self.assertTrue(failed["error"]["retryable"])

        retried = self.service.wait(self.service.retry(failed["id"])["id"])
        self.assertEqual(retried["status"], "succeeded")
        self.assertEqual(retried["retry_of"], failed["id"])
        self.assertFalse(retried["recipe"]["simulate_failure"])

    def test_successful_job_refuses_retry(self) -> None:
        finished = self.service.wait(self.service.create(DEFAULT_RECIPE)["id"])
        with self.assertRaisesRegex(ValueError, "Only failed jobs"):
            self.service.retry(finished["id"])


if __name__ == "__main__":
    unittest.main()
