from __future__ import annotations

import json
import shutil
import tempfile
from pathlib import Path


DEFAULT_RECIPE = {
    "prompt": "Cobalt radio on a steel table, hard noon shadow",
    "negative_prompt": "watermark, low contrast",
    "seed": 240817,
    "width": 512,
    "height": 512,
    "steps": 20,
    "cfg": 7.0,
    "adapter": "mock",
    "simulate_failure": False,
}


def project_root() -> Path:
    return Path(__file__).resolve().parents[1]


class TempProject:
    def __init__(self):
        self._temp = tempfile.TemporaryDirectory()
        self.root = Path(self._temp.name)
        (self.root / "workflows").mkdir()
        shutil.copy2(
            project_root() / "workflows" / "base_workflow.json",
            self.root / "workflows" / "base_workflow.json",
        )
        shutil.copytree(project_root() / "static", self.root / "static")

    def close(self) -> None:
        self._temp.cleanup()


def canonical(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))
