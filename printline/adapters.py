from __future__ import annotations

import hashlib
import json
import os
import time
import urllib.parse
import urllib.request
import uuid
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .workflow import Recipe, WorkflowTemplate

ProgressCallback = Callable[[int, str], None]


class ProviderError(RuntimeError):
    """A generation provider failed after accepting the job."""


@dataclass(frozen=True)
class Artifact:
    filename: str
    mime_type: str
    size_bytes: int
    sha256: str
    provider_metadata: dict[str, Any]


class DeterministicAdapter:
    """Credential-free adapter backed by a documented showcase fixture."""

    name = "generated-fixture"

    def __init__(
        self,
        output_dir: Path,
        step_delay: float = 0.015,
        fixture_path: Path | None = None,
    ):
        self.output_dir = output_dir
        self.step_delay = step_delay
        self.fixture_path = fixture_path or (
            Path(__file__).parent / "fixtures" / "campaign-radio-showcase.png"
        )

    def run(
        self,
        job_id: str,
        recipe: Recipe,
        graph: dict[str, Any],
        progress: ProgressCallback,
    ) -> Artifact:
        progress(12, "preparing graph")
        time.sleep(self.step_delay)
        if recipe.simulate_failure:
            progress(38, "provider accepted job")
            time.sleep(self.step_delay)
            raise ProviderError(
                "Local adapter simulated a provider timeout. Retry after clearing the failure toggle."
            )

        progress(45, "loading generated showcase fixture")
        time.sleep(self.step_delay)
        data = self.fixture_path.read_bytes()
        progress(82, "persisting artifact")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        filename = f"{job_id}.png"
        (self.output_dir / filename).write_bytes(data)
        digest = hashlib.sha256(data).hexdigest()
        progress(96, "recording provenance")
        return Artifact(
            filename=filename,
            mime_type="image/png",
            size_bytes=len(data),
            sha256=digest,
            provider_metadata={
                "renderer": self.name,
                "deterministic": True,
                "fixture": self.fixture_path.name,
                "fixture_boundary": "showcase image; not a live ComfyUI execution",
                "workflow_digest": WorkflowTemplate.digest(graph),
            },
        )


class ComfyUIAdapter:
    """Live adapter derived from the selected foundation's queue/ws/history flow."""

    name = "comfyui"

    def __init__(
        self, output_dir: Path, address: str | None = None, timeout: int = 180
    ):
        self.output_dir = output_dir
        self.address = address or os.getenv("COMFYUI_ADDRESS", "127.0.0.1:8188")
        self.timeout = timeout

    def run(
        self,
        job_id: str,
        recipe: Recipe,
        graph: dict[str, Any],
        progress: ProgressCallback,
    ) -> Artifact:
        try:
            import websocket
        except ImportError as exc:
            raise ProviderError(
                "Live ComfyUI mode requires `pip install -r requirements.txt`."
            ) from exc

        client_id = str(uuid.uuid4())
        ws = websocket.create_connection(
            f"ws://{self.address}/ws?clientId={client_id}", timeout=self.timeout
        )
        try:
            body = json.dumps({"prompt": graph, "client_id": client_id}).encode()
            request = urllib.request.Request(
                f"http://{self.address}/prompt",
                data=body,
                headers={"Content-Type": "application/json"},
            )
            with urllib.request.urlopen(request, timeout=15) as response:
                prompt_id = json.loads(response.read())["prompt_id"]
            progress(12, f"queued in ComfyUI as {prompt_id[:8]}")

            while True:
                raw = ws.recv()
                if not isinstance(raw, str):
                    continue
                event = json.loads(raw)
                data = event.get("data", {})
                if data.get("prompt_id") not in {None, prompt_id}:
                    continue
                if event.get("type") == "progress":
                    maximum = max(1, int(data.get("max", 1)))
                    current = int(data.get("value", 0))
                    progress(15 + int(65 * current / maximum), "sampling in ComfyUI")
                elif event.get("type") == "execution_error":
                    raise ProviderError(
                        data.get("exception_message", "ComfyUI execution failed.")
                    )
                elif event.get("type") == "executing" and data.get("node") is None:
                    break

            progress(84, "retrieving ComfyUI history")
            history = self._json_get(f"/history/{prompt_id}")[prompt_id]
            image = self._first_image(history)
            query = urllib.parse.urlencode(
                {
                    "filename": image["filename"],
                    "subfolder": image.get("subfolder", ""),
                    "type": image.get("type", "output"),
                }
            )
            with urllib.request.urlopen(
                f"http://{self.address}/view?{query}", timeout=30
            ) as response:
                data = response.read()
                mime = response.headers.get_content_type()
            suffix = {
                "image/png": ".png",
                "image/jpeg": ".jpg",
                "image/webp": ".webp",
            }.get(mime, ".png")
            self.output_dir.mkdir(parents=True, exist_ok=True)
            filename = f"{job_id}{suffix}"
            (self.output_dir / filename).write_bytes(data)
            return Artifact(
                filename=filename,
                mime_type=mime,
                size_bytes=len(data),
                sha256=hashlib.sha256(data).hexdigest(),
                provider_metadata={
                    "renderer": self.name,
                    "prompt_id": prompt_id,
                    "source_filename": image["filename"],
                },
            )
        except ProviderError:
            raise
        except Exception as exc:
            raise ProviderError(f"ComfyUI adapter failed: {exc}") from exc
        finally:
            ws.close()

    def _json_get(self, path: str) -> dict[str, Any]:
        with urllib.request.urlopen(
            f"http://{self.address}{path}", timeout=15
        ) as response:
            return json.loads(response.read())

    @staticmethod
    def _first_image(history: dict[str, Any]) -> dict[str, Any]:
        for output in history.get("outputs", {}).values():
            images = output.get("images", [])
            for image in images:
                if image.get("type") == "output":
                    return image
        raise ProviderError("ComfyUI completed without an output image.")
