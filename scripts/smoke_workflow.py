from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT))

from printline.service import JobService  # noqa: E402


def main() -> None:
    with tempfile.TemporaryDirectory() as output_parent:
        service = JobService(PROJECT, mock_step_delay=0)
        service.outputs = Path(output_parent)
        service.adapters["mock"].output_dir = Path(output_parent)
        try:
            queued = service.create(
                {
                    "prompt": "Cobalt radio on red steel, screen-print campaign key visual",
                    "negative_prompt": "watermark, low contrast",
                    "seed": 240817,
                    "width": 512,
                    "height": 512,
                    "steps": 20,
                    "cfg": 7.0,
                    "adapter": "mock",
                }
            )
            finished = service.wait(queued["id"])
            print(json.dumps(finished, indent=2))
            if finished["status"] != "succeeded":
                raise SystemExit(1)
        finally:
            service.close()


if __name__ == "__main__":
    main()
