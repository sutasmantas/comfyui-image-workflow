from __future__ import annotations

import json
import threading
import unittest
import urllib.error
import urllib.request

from printline.server import create_server
from printline.service import JobService
from tests.support import DEFAULT_RECIPE, TempProject


class HttpTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = TempProject()
        self.service = JobService(self.temp.root, mock_step_delay=0)
        self.server = create_server(
            "127.0.0.1", 0, root=self.temp.root, service=self.service
        )
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.base = f"http://127.0.0.1:{self.server.server_port}"

    def tearDown(self) -> None:
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=1)
        self.temp.close()

    def post(self, path: str, payload: dict) -> tuple[int, dict]:
        request = urllib.request.Request(
            self.base + path,
            data=json.dumps(payload).encode(),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(request) as response:
                return response.status, json.loads(response.read())
        except urllib.error.HTTPError as error:
            return error.code, json.loads(error.read())

    def test_job_endpoint_accepts_and_exposes_completed_run(self) -> None:
        status, queued = self.post("/api/jobs", DEFAULT_RECIPE)
        self.assertEqual(status, 202)
        finished = self.service.wait(queued["id"])
        with urllib.request.urlopen(
            self.base + f"/api/jobs/{queued['id']}"
        ) as response:
            observed = json.loads(response.read())
        self.assertEqual(observed["status"], "succeeded")
        self.assertEqual(observed["artifact"]["sha256"], finished["artifact"]["sha256"])
        with urllib.request.urlopen(
            self.base + observed["artifact"]["url"]
        ) as response:
            self.assertEqual(response.headers.get_content_type(), "image/png")
            self.assertTrue(response.read().startswith(b"\x89PNG\r\n\x1a\n"))

    def test_browser_surface_is_served(self) -> None:
        with urllib.request.urlopen(self.base + "/") as response:
            page = response.read().decode()
        self.assertIn("printline", page)
        self.assertIn("Render frame", page)

    def test_invalid_recipe_returns_structured_422(self) -> None:
        status, body = self.post("/api/jobs", {**DEFAULT_RECIPE, "steps": 100})
        self.assertEqual(status, 422)
        self.assertEqual(body["error"]["code"], "invalid_recipe")
        self.assertIn("between 1 and 50", body["error"]["message"])


if __name__ == "__main__":
    unittest.main()
