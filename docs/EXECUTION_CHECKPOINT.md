# Printline execution checkpoint — 2026-08-03

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
