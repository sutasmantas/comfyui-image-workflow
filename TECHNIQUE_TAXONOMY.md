# Printline technique taxonomy

Date: 2026-08-05
Status: systematic dossier; no experiment or model execution performed

## Decision boundary

Printline is a reusable ComfyUI media-workflow service, not an image-model
leaderboard. Its technique question is: which generation, control, evaluation,
and execution profiles add a distinct client-visible operating region while
preserving a replayable job receipt? The current fixed PNG is a software
fixture, not a visual baseline.

The task decomposes into eight independent decisions. “Use ComfyUI” does not
answer any of them.

| Decision | Observable client failure | Serious families | Required evidence |
| --- | --- | --- | --- |
| Foundation model | prompt is ignored, text is malformed, or a useful image costs too much to obtain | mature latent diffusion (SDXL), newer MMDiT (SD3.5), rectified-flow/DiT (FLUX), large multimodal DiT (Qwen-Image) | matched prompt/seed budget; accepted-output rate; warm/cold time; peak VRAM/RAM |
| Structural control | pose, edges, depth, or silhouette drift | ControlNet; T2I-Adapter/control LoRA; model-native structural control | metric matched to the condition plus blind review |
| Spatial/layout control | objects have the wrong count, size, or position | regional/area conditioning; GLIGEN/layout grounding; iterative masked editing | detection/count/layout IoU and boundary cases |
| Reference/subject/style control | product, person, or visual language drifts | IP-Adapter; native reference/edit models; LoRA/fine-tuning | subject and style separated; prompt editability and diversity retained |
| Local editing | an approved asset must be changed without regenerating everything | img2img; inpainting/outpainting; instruction editing | target-change success and non-target preservation |
| Resolution/restoration | final dimensions reveal blur, seams, invented texture, or typography damage | native resolution; latent second pass/hires fix; Real-ESRGAN; SwinIR | artifact/rejection rate at delivery size; time and memory |
| Execution/provenance | an output cannot be replayed or a failure cannot be diagnosed | API-format graph; pinned model/node environment; internal receipt; optional C2PA export | graph/model/control/input/output digests and environment receipt |
| Evaluation/acceptance | one attractive score promotes unusable images | condition-specific metrics; compositional VQA; preference models; randomized human pairwise review | metric/human agreement, per-category failures, rejection reasons |

## Current method inventory

The current seven-node graph uses `CheckpointLoaderSimple`, positive and
negative `CLIPTextEncode`, `EmptyLatentImage`, `KSampler`, `VAEDecode`, and
`SaveImage`. `WorkflowTemplate` changes prompt, negative prompt, seed,
dimensions, steps, CFG, and output prefix. `JobService` adds a single in-memory
worker, lifecycle state, retry lineage, workflow digest, and artifact hash.
`ComfyUIAdapter` implements the official `/prompt`, `/ws`, `/history`, and
`/view` flow.

Only `DeterministicAdapter` is exercised in the baseline. It copies
`campaign-radio-showcase.png`; equal hashes prove fixture stability, not model
determinism or prompt adherence. The graph names an SDXL checkpoint but no
checkpoint, GPU, custom node, or live ComfyUI execution is part of the evidence.

## Field taxonomy and dispositions

### 1. Foundation models

- **SDXL:** retain as the first live integration control because the existing
  graph already has the right node shape, mature ComfyUI examples and broad
  compatibility with ControlNet/IP-Adapter. It is not presumed to win quality.
- **SD3.5 Medium:** admit to the compute-balanced comparison. Its 2.5B parameter
  scale and 0.25–2MP stated range make it a credible consumer-hardware profile,
  but Printline has not measured it.
- **FLUX.1-schnell:** admit as a fast few-step candidate. Its official card
  describes a 12B rectified-flow transformer and one-to-four-step generation;
  parameter count and offload needs make local resource measurement mandatory.
- **Qwen-Image:** route to a text/layout specialist screen, not the default
  bake-off. Its 20B size and native ComfyUI control/edit paths may own a useful
  professional-creative region, but it is not a like-for-like low-compute
  replacement.
- **Closed API models and every new checkpoint:** excluded from the first local
  experiment. They can be added only for a client access/cost question, without
  changing the shared receipt contract.

Status: candidate selection is **provisional**. Published model claims do not
close Printline's hardware- and workload-specific routing decision.

### 2. Structure and layout

- **ControlNet:** established as a distinct structural-control family for
  edge/depth/pose/segmentation conditions. The external evidence closes the
  question that prompt-only generation is not an equivalent control.
- **T2I-Adapter/control LoRA:** retain as an interchangeable lower-weight or
  model-native structural implementation, not a second product feature.
- **Regional/area conditioning and GLIGEN:** retain as the layout family because
  count, location and size are different from preserving an edge/depth map.
  GLIGEN's model compatibility is dated, so native regional/masked paths must be
  screened before it is adopted.
- **Multiple controls:** treat as an interaction. The fact that controls can be
  composed does not establish that their guidance will remain compatible.

Status: family separation is **established**; Printline implementation and
composition settings remain **provisional**.

### 3. Reference, subject, style, and editing

- **IP-Adapter:** admit for tuning-free image-reference conditioning, initially
  on the SDXL control. Reference similarity, text editability, and diversity
  are separate outcomes.
- **LoRA:** admit only for repeated brand/style/subject work with enough approved
  training assets. It adds training, dataset, overfitting, privacy, versioning,
  and review costs; it is not the automatic upgrade from IP-Adapter.
- **Native instruction editing (Qwen-Image-Edit class):** retain as a localized
  revision candidate when the job starts from an approved asset. It answers a
  different question than greenfield generation.
- **Plain img2img/inpainting:** keep as the simplest localized-edit control and
  fallback before adopting a larger instruction-edit model.
- **Face-specific identity components:** out of the generic first slice. They
  require consent, face-specific metrics, and a client use case.

Status: the operating-region split is **established**; winners are **unknown**.

### 4. Resolution and restoration

Native target-size generation, a latent second pass, and pixel-space
restoration are not interchangeable. Real-ESRGAN and SwinIR are maintained
reusable implementations, but either may invent detail or damage small text.
They enter only a matched delivery-size comparison. A larger pixel count is not
accepted as higher quality.

Status: need for matched comparison is **established**; route is **unknown**.

### 5. Evaluation

No single score covers Printline's profiles:

- use T2I-CompBench++/GenAI-Bench categories for prompt compositionality;
- use the generating condition's own observable—edge overlap, depth error,
  keypoint distance, segmentation/layout IoU, OCR accuracy, or identity/style
  similarity—for control adherence;
- use VQAScore as an automated semantic diagnostic, not sole truth;
- use HPSv3 or another preference model only as a secondary triage score;
- use randomized blind human review for acceptability, artifacts, brand/style
  fit, and pairwise preference;
- record rejected generations and regeneration count so quality is not divorced
  from operational cost.

FID is rejected for the small prompt-conditioned portfolio comparison. It needs
a meaningful reference distribution and has documented sample-complexity and
representation problems. An attractive aggregate metric cannot override a
pre-registered control or acceptance failure.

Status: metric routing is **established**; thresholds require calibration.

### 6. Execution, reproducibility, and portable provenance

The current graph digest is necessary but insufficient for live replay. A live
receipt must add ComfyUI revision, core/custom-node snapshot, model and auxiliary
weight identifiers/digests, input/control digests, sampler/scheduler/precision,
hardware, software versions, wall time, peak memory, and all output hashes.
Same-seed GPU output must be tested rather than assumed byte-identical.

ComfyUI-Manager snapshots and `comfy-cli` should own environment installation
and dependency restoration. Printline should own only the experiment manifest,
receipt normalization, and its service adapter. C2PA is a portable downstream
manifest option when a client needs asset-level provenance; it does not replace
the internal run receipt.

Status: missing receipt fields are **established**; exact replay tolerance is
**unknown** until P0.

## Search protocol

Research ran on 2026-08-05 using Google/web search, arXiv, conference/open-review
pages, official model cards/documentation, and GitHub repositories. License was
neither queried nor used to filter or rank candidates, per portfolio policy.

Inclusion rules: relevant to local/open-weight image generation or editing;
maps to a client-visible failure; has a paper, benchmark, official model card,
or inspectable maintained implementation; can fit the ComfyUI graph/receipt
boundary; and adds a distinct operating region. Exclusion rules: visual-only UI
packs, unpinned workflow galleries, popularity-only claims, duplicate wrappers,
video/3D/audio, and a new technique whose only benefit is keyword breadth.

Search iterations:

1. Taxonomy seed: `controllable text-to-image generation survey ControlNet
   IP-Adapter benchmark`, `text-to-image quality metrics survey`, and
   `T2I-CompBench official repository` established generation, structural,
   reference/style, and evaluation families.
2. Maintained implementation expansion: official ComfyUI, comfy-cli, Manager,
   ControlNet, IP-Adapter, model, evaluator, and upscaler repositories established
   reusable components and integration seams.
3. Contrary-evidence expansion: `FID limitations`, `reward model human
   correlation`, `LoRA overfitting`, and `multi-condition control conflict`
   established metric and composition risks.
4. Newer-taxonomy expansion: 2025–2026 controllable-generation and professional
   design searches added **layout grounding/local editing** as a missing
   decision family and text/layout accuracy as an evaluation category.
5. First saturation expansion: condition lists across surveys, official ComfyUI
   workflows, and production acceptance added multi-reference/multi-control only
   as interaction cases; no new top-level decision family.
6. Second saturation expansion: controllable-generation benchmarks across
   arXiv, GitHub, CVF, and OpenReview again mapped to structure, layout,
   subject/style/reference, editing, resolution, or evaluation; no new top-level
   family. Technique-family saturation therefore passed.

## Survey and benchmark anchors

- Cao et al., *Controllable Generation with Text-to-Image Diffusion Models: A
  Survey* (v2, 2026): https://arxiv.org/abs/2403.04279
- Hartwig et al., *A Survey on Quality Metrics for Text-to-Image Generation*:
  https://arxiv.org/abs/2403.11821
- Yang et al., *Text to Image Generation and Editing: A Survey*:
  https://arxiv.org/abs/2505.02527
- ImagenHub standardized conditional generation and found weak automatic-metric
  correlation outside subject-driven generation:
  https://arxiv.org/abs/2310.01596
- T2I-CompBench++: https://github.com/Karine-Huang/T2I-CompBench
- GenAI-Bench/VQAScore: https://github.com/linzhiqiu/t2v_metrics
- LayoutBench: https://arxiv.org/abs/2304.06671
- ConceptMix: https://openreview.net/forum?id=MU2s9wwWLo
- BizGenEval's commercial-design categories are recorded as a newer external
  applicability check, not a locally reproduced leaderboard:
  https://arxiv.org/abs/2603.25732

## Portfolio fit

Printline remains distinct from the other projects because the core evidence is
a graph-driven generative-media workflow with artifact and retry provenance.
The dossier deepens that product with controllable generation and calibrated
visual acceptance; it does not turn Printline into a generic computer-vision
benchmark or duplicate Gauge's defect-inspection decisioning.
