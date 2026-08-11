# Printline controlled benchmark design

Date: 2026-08-05
Status: design only; P0–P5 are unexecuted

## Evidence-reuse result

External evidence closes the existence and broad operating regions of
structural control, image-reference adapters, layout control, localized editing,
restoration, and condition-specific evaluation. It does **not** close which
combination works on Printline's hardware, pinned ComfyUI revision, professional
creative prompts, or acceptance policy. Only those unresolved routing questions
receive local experiments.

## Shared protocol

- Freeze an experiment manifest before generation: prompt/case ID, profile,
  graph digest, model/auxiliary weight IDs and SHA-256, ComfyUI/custom-node pins,
  seed, dimensions, sampler/scheduler/steps/guidance/precision, input/control
  hashes, hardware/software, and evaluator pins.
- Separate development and held-out cases by prompt concept/reference asset,
  not by generated image. Never tune weights or thresholds on held-out output.
- Use matched seeds and randomized blinded presentation. Human reviewers do not
  see model/profile names.
- Export per-image metrics and rejection reasons. Report medians, bootstrap
  intervals for pairwise/preferences where sample size permits, and categories,
  not only an overall mean.
- Record cold start, warm generation, end-to-end latency, peak VRAM/RAM, disk
  footprint, failures/OOM, outputs attempted, outputs accepted, and
  **compute/time per accepted output**.
- A correctness/control gate cannot be traded away for preference score. Any
  profile with a safety, provenance, missing-artifact, or declared control-gate
  failure is not promoted.
- Stop an experiment at 12 GPU-hours, 250 GB added disk, 200 generated images,
  or three repeated infrastructure failures unless a checkpoint explicitly
  approves a narrower continuation. No paid API is required.

## Frozen workload plan

Prepare only after P0 is admitted:

- 24 compositional text prompts sampled across attribute binding, count,
  spatial/non-spatial relations, text rendering, and professional product/poster
  scenes; 12 development and 12 held-out.
- 12 structural cases with public/owned Canny, depth, or pose controls; six
  development and six held-out, with expected control features frozen.
- 10 reference cases separated into object/product, non-person subject, and
  style; faces are excluded from the first slice.
- 8 localized-edit cases with explicit target masks and non-target regions.
- 12 accepted 1MP images for delivery-size restoration, including fine lines,
  small text, texture, faces/skin only when consented, and flat graphics.

Public benchmark prompts are anchors, not a claim that leaderboard scores
transfer to client work. Any future client comparison replaces or extends the
held-out cases with approved assets and acceptance criteria.

## P0 — real execution, receipt, and replay oracle

**Question:** can the existing API graph run on a pinned real ComfyUI/SDXL
environment and produce a complete, replayable receipt?

- Cells: current fixture control; live SDXL run; same live manifest repeated
  after warm start; one invalid/missing-model failure.
- Cases: three prompts × two seeds at 512 and 1024 where supported.
- Metrics: terminal state reconciliation, artifact presence/hash, receipt-field
  completeness, graph/model/input/output digests, pixel equality plus SSIM/LPIPS
  if hashes differ, cold/warm time, peak VRAM/RAM, and error classification.
- PASS: all live runs and the failure reconcile to one terminal receipt; no
  artifact is reported before retrieval/hash; repeated runs preserve declared
  inputs and stay within a pre-registered image tolerance; missing model/node is
  actionable and not marked retryable without a changed environment.
- Decision: only PASS admits P1. Byte-identical GPU output is not assumed.
- Minimal integration checks: official API event reconciliation, timeout,
  validation error, execution error, and history/output retrieval.

## P1 — foundation and compute screen

**Question:** which foundation candidates own a useful quality/compute region?

- Initial cells: SDXL integration control, SD3.5 Medium, FLUX.1-schnell.
  Qwen-Image is a separate text/layout specialist cell only if its model and
  evaluator fit the frozen hardware/disk budget.
- Screen: 12 development prompts × two seeds. Promote at most two non-dominated
  candidates to 12 held-out prompts × four seeds.
- Quality: compositional VQAScore, OCR exact/normalized character accuracy for
  text cases, randomized human accept/reject and pairwise preference, artifact
  taxonomy, and diversity across seeds.
- Operations: cold/warm latency, model-load time, peak VRAM/RAM, disk size,
  OOM/failure, attempts per accepted output.
- Promotion: retain a fast default and/or quality/text specialist only when it
  adds an acceptance region and does not violate the resource ceiling. No
  universal winner is required.
- Confounders: native resolution, recommended step counts, prompt style, and
  quantization/offload. Compare declared deployment profiles, not misleadingly
  identical sampler parameters across incompatible architectures.

## P2 — structure, layout, and composition

**Question:** when do explicit controls beat prompting, and do combined controls
interfere?

- Structure cells on matched base model: prompt-only, Canny ControlNet,
  depth/pose ControlNet as applicable, lighter/model-native control candidate.
- Layout cells: prompt-only and the best compatible regional/area/layout path.
- Interaction cells: best structure-only, IP-Adapter-only, and
  structure + IP-Adapter with fixed weights, followed by one development-only
  weight sweep if the combined cell is not dominated.
- Metrics: edge precision/recall or chamfer, depth rank/RMSE, keypoint PCK,
  detection/count/layout IoU, VQAScore, reference similarity, blind acceptance,
  artifacts, latency/VRAM, and control-conflict rejection reason.
- Promotion: each profile must beat prompt-only on its declared control metric
  and not lose more than the pre-registered human-acceptance margin. Combined
  control is retained only if it beats both single controls on cases needing
  both; “nodes connect” is not evidence.

## P3 — reference, editing, and adaptation routing

**Question:** when is tuning-free reference/editing sufficient, and when would
LoRA training be justified?

- Cells: plain img2img/inpaint control, IP-Adapter, compatible native
  instruction-edit profile; LoRA only after an approved repeated-asset dataset
  and volume threshold exist.
- Metrics: subject/reference similarity (DINO-style; face-specific metric only
  for consented face cases), style similarity kept separate from content,
  target-edit success, non-target LPIPS/structure preservation, text alignment,
  diversity, human acceptance, setup/training/inference time, and storage.
- Promotion: prefer tuning-free route when it meets acceptance. Admit LoRA only
  if the same held-out prompt/style cases show a material repeated-output gain
  after training cost and overfitting/diversity gates.
- Boundary: no identity or privacy claim from generic CLIP similarity; client
  consent and approved assets are prerequisites for people.

## P4 — delivery-resolution routes

**Question:** which path reaches delivery size without unacceptable invention,
seams, or text damage?

- Cells: native target-size render, latent two-pass/hires fix, Real-ESRGAN, and
  SwinIR only if it is non-dominated in the development screen.
- Metrics: output dimensions, OCR retention, edge/line consistency,
  no-reference quality only as diagnostic, paired human artifact/rejection
  review, tile seams, time, VRAM/RAM, and accepted-output cost.
- Promotion: route by asset type. A restorer cannot win merely because it
  sharpens or increases pixels; hallucinated detail or altered approved text is
  a hard rejection.

## P5 — evaluator calibration and acceptance policy

**Question:** which automatic diagnostics safely reduce review without silently
accepting failures?

- Inputs: blinded outputs and human labels accumulated from P1–P4; freeze P5
  split before fitting any threshold.
- Compare: condition-specific metrics, VQAScore, HPSv3, simple conjunctions,
  and human-only control. FID is excluded.
- Metrics: pairwise agreement, rank correlation, false-accept rate for each hard
  failure category, selective risk/coverage, review volume, evaluator runtime
  and memory.
- Promotion: automatic acceptance requires zero observed hard control/text/
  provenance false accepts on the held-out slice and a declared coverage bound.
  Otherwise scores remain triage/ranking aids and a human approval is required.

## Exact next controlled action

After a later checkpoint authorizes experiments, execute **P0 only**. First pin
ComfyUI/comfy-cli/Manager and the SDXL model artifacts, export the seven-node API
graph, add receipt normalization by refitting the current official-example-based
adapter, and run the small success/replay/failure matrix. Stop and reconcile the
P0 manifest/results before P1. This dossier does not authorize that work.

## Reproduction commands for the current baseline only

```powershell
python -m compileall -q printline tests scripts main.py
python -m unittest discover -s tests -v
python scripts/smoke_workflow.py
git diff --check
```

These commands exercise the deterministic PNG fixture and current service
contract. They do not reproduce any P0–P5 result.
