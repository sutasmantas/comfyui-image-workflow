from __future__ import annotations

import copy
import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ALLOWED_SIZES = {(512, 512), (768, 1024), (1024, 768), (1024, 1024)}
MAX_PROMPT_LENGTH = 600
MAX_NEGATIVE_PROMPT_LENGTH = 300


class ValidationError(ValueError):
    """A client-visible recipe validation error."""


@dataclass(frozen=True)
class Recipe:
    prompt: str
    negative_prompt: str
    seed: int
    width: int
    height: int
    steps: int
    cfg: float
    adapter: str = "mock"
    simulate_failure: bool = False

    def public_dict(self) -> dict[str, Any]:
        return {
            "prompt": self.prompt,
            "negative_prompt": self.negative_prompt,
            "seed": self.seed,
            "width": self.width,
            "height": self.height,
            "steps": self.steps,
            "cfg": self.cfg,
            "adapter": self.adapter,
            "simulate_failure": self.simulate_failure,
        }


def parse_recipe(payload: Any) -> Recipe:
    if not isinstance(payload, dict):
        raise ValidationError("Request body must be a JSON object.")

    allowed = {
        "prompt",
        "negative_prompt",
        "seed",
        "width",
        "height",
        "steps",
        "cfg",
        "adapter",
        "simulate_failure",
    }
    unexpected = sorted(set(payload) - allowed)
    if unexpected:
        raise ValidationError(f"Unsupported field(s): {', '.join(unexpected)}")

    prompt = payload.get("prompt", "")
    if not isinstance(prompt, str) or not prompt.strip():
        raise ValidationError("Prompt is required.")
    prompt = prompt.strip()
    if len(prompt) > MAX_PROMPT_LENGTH:
        raise ValidationError(f"Prompt must be at most {MAX_PROMPT_LENGTH} characters.")

    negative = payload.get("negative_prompt", "")
    if not isinstance(negative, str):
        raise ValidationError("Negative prompt must be text.")
    negative = negative.strip()
    if len(negative) > MAX_NEGATIVE_PROMPT_LENGTH:
        raise ValidationError(
            f"Negative prompt must be at most {MAX_NEGATIVE_PROMPT_LENGTH} characters."
        )

    seed = _integer(payload, "seed", 0)
    if not 0 <= seed <= 9_223_372_036_854_775_807:
        raise ValidationError("Seed must be between 0 and 9223372036854775807.")

    width = _integer(payload, "width", 1024)
    height = _integer(payload, "height", 1024)
    if (width, height) not in ALLOWED_SIZES:
        raise ValidationError("Size must be 512x512, 768x1024, 1024x768, or 1024x1024.")

    steps = _integer(payload, "steps", 20)
    if not 1 <= steps <= 50:
        raise ValidationError("Steps must be between 1 and 50.")

    cfg = payload.get("cfg", 7.0)
    if isinstance(cfg, bool) or not isinstance(cfg, (int, float)):
        raise ValidationError("CFG must be a number.")
    cfg = round(float(cfg), 2)
    if not 1 <= cfg <= 20:
        raise ValidationError("CFG must be between 1 and 20.")

    adapter = payload.get("adapter", "mock")
    if adapter not in {"mock", "comfyui"}:
        raise ValidationError("Adapter must be 'mock' or 'comfyui'.")

    simulate_failure = payload.get("simulate_failure", False)
    if not isinstance(simulate_failure, bool):
        raise ValidationError("simulate_failure must be true or false.")
    if simulate_failure and adapter != "mock":
        raise ValidationError("Failure simulation is available only for the local adapter.")

    return Recipe(
        prompt=prompt,
        negative_prompt=negative,
        seed=seed,
        width=width,
        height=height,
        steps=steps,
        cfg=cfg,
        adapter=adapter,
        simulate_failure=simulate_failure,
    )


def _integer(payload: dict[str, Any], key: str, default: int) -> int:
    value = payload.get(key, default)
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValidationError(f"{key.capitalize()} must be an integer.")
    return value


class WorkflowTemplate:
    """Parameterizes the adopted ComfyUI API-format graph."""

    def __init__(self, path: Path):
        self.path = path
        self._template = json.loads(path.read_text(encoding="utf-8"))
        self._index = {
            details.get("class_type"): node_id
            for node_id, details in self._template.items()
        }
        required = {
            "KSampler",
            "EmptyLatentImage",
            "CLIPTextEncode",
            "SaveImage",
        }
        missing = required - set(self._index)
        if missing:
            raise RuntimeError(f"Workflow is missing required node types: {sorted(missing)}")

    def compile(self, recipe: Recipe, filename_prefix: str) -> dict[str, Any]:
        graph = copy.deepcopy(self._template)
        sampler_id = self._index["KSampler"]
        sampler = graph[sampler_id]["inputs"]
        sampler.update(seed=recipe.seed, steps=recipe.steps, cfg=recipe.cfg)

        positive_id = str(sampler["positive"][0])
        negative_id = str(sampler["negative"][0])
        graph[positive_id]["inputs"]["text"] = recipe.prompt
        graph[negative_id]["inputs"]["text"] = recipe.negative_prompt

        latent = graph[self._index["EmptyLatentImage"]]["inputs"]
        latent.update(width=recipe.width, height=recipe.height, batch_size=1)
        graph[self._index["SaveImage"]]["inputs"]["filename_prefix"] = filename_prefix
        return graph

    @staticmethod
    def digest(graph: dict[str, Any]) -> str:
        canonical = json.dumps(graph, sort_keys=True, separators=(",", ":")).encode()
        return hashlib.sha256(canonical).hexdigest()
