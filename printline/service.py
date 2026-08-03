from __future__ import annotations

import copy
import queue
import threading
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .adapters import ComfyUIAdapter, DeterministicAdapter, ProviderError
from .workflow import Recipe, WorkflowTemplate, parse_recipe


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


class JobNotFound(KeyError):
    pass


class JobService:
    def __init__(
        self,
        root: Path,
        *,
        mock_step_delay: float = 0.015,
        start_worker: bool = True,
    ):
        self.root = root
        self.outputs = root / "outputs"
        self.workflow = WorkflowTemplate(root / "workflows" / "base_workflow.json")
        self.adapters = {
            "mock": DeterministicAdapter(self.outputs, mock_step_delay),
            "comfyui": ComfyUIAdapter(self.outputs),
        }
        self._jobs: dict[str, dict[str, Any]] = {}
        self._pending: queue.Queue[str | None] = queue.Queue()
        self._lock = threading.RLock()
        self._worker: threading.Thread | None = None
        if start_worker:
            self._worker = threading.Thread(target=self._work, daemon=True, name="printline-worker")
            self._worker.start()

    def create(self, payload: Any, *, retry_of: str | None = None) -> dict[str, Any]:
        recipe = parse_recipe(payload)
        job_id = uuid.uuid4().hex
        created = utc_now()
        # Keep the graph itself stable for the same recipe. ComfyUI appends its own
        # output counter; the local adapter uses the job ID only for storage.
        graph = self.workflow.compile(recipe, f"printline/seed-{recipe.seed}")
        job = {
            "id": job_id,
            "status": "queued",
            "stage": "queued",
            "progress": 0,
            "created_at": created,
            "updated_at": created,
            "started_at": None,
            "completed_at": None,
            "retry_of": retry_of,
            "recipe": recipe.public_dict(),
            "workflow": {
                "format": "comfyui-api",
                "digest": self.workflow.digest(graph),
                "node_count": len(graph),
            },
            "artifact": None,
            "error": None,
            "_graph": graph,
        }
        with self._lock:
            self._jobs[job_id] = job
        self._pending.put(job_id)
        return self._public(job)

    def retry(self, job_id: str) -> dict[str, Any]:
        original = self.get(job_id)
        if original["status"] != "failed":
            raise ValueError("Only failed jobs can be retried.")
        payload = copy.deepcopy(original["recipe"])
        payload["simulate_failure"] = False
        return self.create(payload, retry_of=job_id)

    def get(self, job_id: str) -> dict[str, Any]:
        with self._lock:
            job = self._jobs.get(job_id)
            if job is None:
                raise JobNotFound(job_id)
            return self._public(job)

    def list(self) -> list[dict[str, Any]]:
        with self._lock:
            jobs = sorted(self._jobs.values(), key=lambda item: item["created_at"], reverse=True)
            return [self._public(job) for job in jobs]

    def wait(self, job_id: str, timeout: float = 3.0) -> dict[str, Any]:
        deadline = datetime.now().timestamp() + timeout
        while datetime.now().timestamp() < deadline:
            job = self.get(job_id)
            if job["status"] in {"succeeded", "failed"}:
                return job
            threading.Event().wait(0.01)
        raise TimeoutError(f"Job {job_id} did not finish within {timeout}s")

    def close(self) -> None:
        self._pending.put(None)
        if self._worker:
            self._worker.join(timeout=1)

    def _work(self) -> None:
        while True:
            job_id = self._pending.get()
            if job_id is None:
                self._pending.task_done()
                return
            self._execute(job_id)
            self._pending.task_done()

    def _execute(self, job_id: str) -> None:
        with self._lock:
            job = self._jobs[job_id]
            job.update(
                status="running",
                stage="starting adapter",
                progress=5,
                started_at=utc_now(),
                updated_at=utc_now(),
            )
            recipe = parse_recipe(job["recipe"])
            graph = copy.deepcopy(job["_graph"])

        def progress(value: int, stage: str) -> None:
            with self._lock:
                live = self._jobs[job_id]
                live["progress"] = max(live["progress"], min(99, int(value)))
                live["stage"] = stage
                live["updated_at"] = utc_now()

        try:
            artifact = self.adapters[recipe.adapter].run(job_id, recipe, graph, progress)
            completed = utc_now()
            with self._lock:
                self._jobs[job_id].update(
                    status="succeeded",
                    stage="complete",
                    progress=100,
                    completed_at=completed,
                    updated_at=completed,
                    artifact={
                        "url": f"/outputs/{artifact.filename}",
                        "filename": artifact.filename,
                        "mime_type": artifact.mime_type,
                        "size_bytes": artifact.size_bytes,
                        "sha256": artifact.sha256,
                        "provider_metadata": artifact.provider_metadata,
                    },
                )
        except ProviderError as exc:
            completed = utc_now()
            with self._lock:
                self._jobs[job_id].update(
                    status="failed",
                    stage="adapter error",
                    completed_at=completed,
                    updated_at=completed,
                    error={
                        "code": "provider_failure",
                        "message": str(exc),
                        "retryable": True,
                        "handoff": "Review the recipe and provider health, then retry this run.",
                    },
                )
        except Exception as exc:
            completed = utc_now()
            with self._lock:
                self._jobs[job_id].update(
                    status="failed",
                    stage="internal error",
                    completed_at=completed,
                    updated_at=completed,
                    error={
                        "code": "internal_failure",
                        "message": f"The workflow stopped before producing an artifact: {exc}",
                        "retryable": False,
                        "handoff": "Inspect server logs before submitting a new run.",
                    },
                )

    @staticmethod
    def _public(job: dict[str, Any]) -> dict[str, Any]:
        return {key: copy.deepcopy(value) for key, value in job.items() if not key.startswith("_")}
