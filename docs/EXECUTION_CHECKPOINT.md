# Printline systematic-dossier checkpoint — 2026-08-05

## Restart boundary

- repository: `portfolio_demos/generative_workflow`
- isolated branch: `agent/printline-technique-dossier`
- assigned worktree:
  `portfolio_demos/worktrees/printline_technique_dossier`
- clean base: `ba92ce2545e93416b236b686921bd7f639d00863`
- dossier commit: `3aaebdd` (`docs: add Printline technique dossier`)
- checkpoint commit: this commit; resolve with `git rev-parse HEAD` and use the
  exact hash returned in the handback
- central expertise index: `../../../UPWORK_EXPERTISE_INDEX.md` relative to this
  assigned worktree (`../../UPWORK_EXPERTISE_INDEX.md` from the canonical
  repository); updated in the shared CV workspace
- experiment/model execution: not run

## Dossier gate

| Gate | Evidence | Status |
| --- | --- | --- |
| Problem decomposition | eight independent foundation/control/edit/resolution/execution/evaluation decisions in `TECHNIQUE_TAXONOMY.md` | PASS |
| Search protocol | dated sources, inclusion/exclusion rules, queries, iterations, and explicit license-irrelevant policy | PASS |
| Survey coverage | controllable-generation, T2I/editing, and image-quality metric surveys | PASS |
| Benchmark coverage | T2I-CompBench++, GenAI-Bench, ConceptMix, LayoutBench, ImagenHub, and commercial-design applicability | PASS |
| Existing-answer search | each major question records its evidence-reuse level in `RESEARCH_DECISION.md` and the matrix | PASS |
| Technique-family saturation | two consecutive post-expansion searches added no decision-relevant top-level family | PASS |
| Candidate comparison | 36 unique matrix rows compare capabilities, resources, integration, maintenance, and failure boundaries | PASS |
| Contrary evidence | FID limitations, evaluator disagreement, LoRA overfit, OOD layout, and multi-control conflict recorded | PASS |
| Implementation evidence | 18 GitHub HEAD pins with adopt/refit/defer/reject seams in `GITHUB_IMPLEMENTATION_AUDIT.md` | PASS |
| Portfolio fit | controllable generative-media receipts remain distinct from Gauge and the other portfolio projects | PASS |
| Review status | conclusions are labelled established, provisional, contested, or unknown | PASS |

Systematic dossier: **PASS**. P0–P5 experiments and the technique ceiling:
**PARTIAL / unexecuted**. This checkpoint does not authorize implementation.

## Required dossier artifacts

- `TECHNIQUE_TAXONOMY.md`
- `EVIDENCE_MATRIX.csv`
- `GITHUB_IMPLEMENTATION_AUDIT.md`
- `BENCHMARK_DESIGN.md`
- `RESEARCH_DECISION.md`
- `docs/EXPERTISE_NOTES.md`

## Expertise-extraction closure

`docs/EXPERTISE_NOTES.md` contains six consequential decision notes with
measured/engineering/client-unknown claim separation, delivery controls,
interview follow-ups, and central-index dispositions.

Distinct central cards added:

- `Match image evaluation to the promised control`
- `Test combined image controls against each single-control fallback`
- `Price generation profiles per accepted asset`
- `Test tuning-free reference control before training a LoRA`

The existing `Reproducibility needs the recipe and the artifact` card was
updated to the actual deterministic PNG boundary and the missing live-receipt
fields. The layout-only note records an explicit no-index reason because a new
card would duplicate those retrieval paths.

## Verification

Executed from the isolated worktree at base `ba92ce2` before dossier writing:

| Command | Result |
| --- | --- |
| `python -m compileall -q printline tests scripts main.py` | PASS |
| `python -m unittest discover -s tests -v` | PASS — 11 tests |
| `python scripts/smoke_workflow.py` | PASS — deterministic PNG fixture, seven-node graph digest and artifact receipt |
| `Import-Csv EVIDENCE_MATRIX.csv` | PASS — 36 rows and 36 unique IDs |
| required-file existence check | PASS — all six dossier artifacts |
| `git diff --cached --check` before dossier commit | PASS |

No model, auxiliary weight, evaluator, or dataset was downloaded; no ComfyUI or
GPU execution occurred; no new image was generated; no UI, polish, application
logic, merge, or push was performed.

## Retained decisions and limitations

- Preserve the current service/queue/receipt boundary; reuse official ComfyUI,
  comfy-cli/Manager, core nodes, maintained IP-Adapter, and evaluators instead
  of adding a second execution framework.
- Add the missing `layout-controlled` operating region; treat localized editing
  as an operation and multi-control/multi-reference as interactions.
- The first later experiment is P0 real SDXL execution, receipt, replay, and
  missing-model/node failure reconciliation. P1–P5 remain gated.
- No foundation model, control stack, evaluator, upscaler, quality threshold,
  latency, VRAM envelope, or automatic-accept policy has won locally.
- The only exercised artifact path remains the fixed PNG fixture. The service
  remains in-memory and single-worker; production durability/scale/auth/storage
  claims remain unsupported.

## Exact next action

Stop Printline work. Update the shared portfolio restart/checkpoint files to
mark order item 7 complete at dossier `3aaebdd` and this checkpoint commit, then
advance the systematic-dossier queue to order item 8, **Gauge**. Do not start
Gauge in this slice. If Printline is resumed later for experiments, start P0
only after the authoritative portfolio checkpoint explicitly admits it.

## Previous publication checkpoint

### Printline execution checkpoint — 2026-08-03

## Restart boundary

- repository: `portfolio_demos/generative_workflow`
- canonical local and remote `main`: publication merge
  `327b43509393454584e8a3d649819ff752ef2aaf`
- publication implementation: `d7a8acbec507bc0d932a8ce7928dedcfa59d657b`
- public-proof checkpoint: `17f1fcd`
- publication branch: `agent/printline-publication`
- assigned worktree: `portfolio_demos/worktrees/printline_publication`
- staged source fixture: `portfolio_demos/publication_staging/printline/campaign-radio-imagegen-fixture.png`
- live ComfyUI/model execution: not required and not claimed

## Publication gate

| Gate | Evidence | Status |
| --- | --- | --- |
| Zero-cost visual fixture | generated radio fixture copied into `printline/fixtures/` with prompt, hash, and boundary recorded | PASS |
| Real application path | fixture crosses the existing queue, job status, output storage, metadata, and HTTP artifact path | PASS |
| ComfyUI-compatible contract | seven-node graph parameterization plus optional `/prompt`, `/ws`, `/history`, `/view` adapter retained | PASS |
| Failure/retry evidence | provider stop is visible; retry creates a new run linked by `retry_of` | PASS |
| Client-facing depth | workflow-contract section explains recipe, graph, queue, run, artifact, and adapter split | PASS |
| Responsive browser | 1600×1200, 1024×900, and 390×844 checks pass without document overflow | PASS |
| Repository evidence | refreshed 1440, 1024, and 390 screenshots | PASS |
| Upwork media | three visually inspected 1600×1200 PNGs and one inspected 17.68-second H.264 walkthrough | PASS |
| Technical verification | compileall, 11 tests, smoke demo, and changed-file Ruff gates pass | PASS |
| Claim boundary | no paid/live model, hosted GPU, quality, scale, or client-outcome claim added | PASS |
| Public repository | [`sutasmantas/comfyui-image-workflow`](https://github.com/sutasmantas/comfyui-image-workflow), README fetched at exact commit `d7a8acbec507bc0d932a8ce7928dedcfa59d657b` | PASS |

## Exact next action

Printline is complete, public, and merged. Close the cross-portfolio
publication queue, promote Printline to active evidence, then begin the
public-repository reconciliation sweep. Do not add live-model work unless a
real job requires it.
