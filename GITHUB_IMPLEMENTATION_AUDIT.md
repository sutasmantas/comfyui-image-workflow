# Printline GitHub implementation audit

Date: 2026-08-05
Policy: GitHub components were inspected before recommending custom logic.

## Current foundation and reuse boundary

Printline began from `9elements/comfyui-api` at
`3cc6b17af...`. The present `printline/` service is the active path. The inherited
root `basic_api.py` and `utils/actions/` scripts are not imported by the service
or tests and are not evidence for the current application.

The live adapter follows ComfyUI's official API example: submit an API-format
graph to `/prompt`, observe the matching prompt over `/ws`, read `/history`, and
retrieve the output through `/view`. Replacing those roughly 100 lines with a
second client wrapper would not unlock a new capability. Reuse should instead
concentrate on environment restoration, native workflow nodes, and evaluation.

All pins below are remote `HEAD` values observed with `git ls-remote <url> HEAD`
on 2026-08-05. They are research pins, not installed dependencies.

## Component comparison

| Component and pin | Maintained capability inspected | Integration seam | Disposition | Reason / known boundary |
| --- | --- | --- | --- | --- |
| `Comfy-Org/ComfyUI@6f7cd7f` | official graph runtime, API-format workflows, queue/WebSocket/history, core model/control/edit/upscale nodes | keep as external runtime behind `ComfyUIAdapter` | **adopt/pin later** | canonical contract; P0 must pin an actual release/revision and test validation/error events |
| `Comfy-Org/comfy-cli@5798668` | install, launch, workspace targeting, memory flags | experiment setup script | **adopt later** | avoids custom installer/launcher logic; not a receipt or evaluator |
| `Comfy-Org/ComfyUI-Manager@d47c934` | custom-node install and dependency snapshots/restoration | environment manifest | **adopt later** | avoids hand-written node dependency restoration; snapshot does not pin model weights or CUDA itself |
| official `script_examples/websockets_api_example.py` in ComfyUI pin above | reference `/prompt` + `/ws` behavior | reconcile with current adapter in P0 | **refit current code** | current adapter is already a small, application-specific derivation; add missing validation/interrupt/error receipts rather than a new client framework |
| `SaladTechnologies/comfyui-api@4dfc930` | scalable HTTP wrapper, storage providers, webhooks | alternative service boundary | **defer** | useful only if horizontal scale/storage/webhooks become a client requirement; duplicates Printline's current queue/API for this slice |
| `pydn/ComfyUI-to-Python-Extension@6cdcc23` | exports graphs as single-shot Python | alternative headless runner | **do not adopt now** | bypasses the server contract and caching used by Printline; useful for one-shot scripts, not this service comparison |
| `huggingface/diffusers@09514d4` | broad model/control pipelines and evaluation ecosystem | alternative inference engine | **do not add to core** | would create a second execution engine and integration surface; may remain evaluator/reference code outside the service |
| `black-forest-labs/flux@802fb47` | official FLUX.1 inference and model cards | foundation-model reference | **reuse model via native ComfyUI** | no reason to port its runner while ComfyUI natively supports the family |
| `QwenLM/Qwen-Image@6b5e1f5` | official 20B generation/edit model and examples | specialist text/layout/edit profile | **screen via native ComfyUI** | distinct capability, large resource surface; no direct integration until hardware gate |
| `Stability-AI/generative-models@e8cd657` | SDXL/Stable Diffusion research implementation | model reference | **reuse model via native ComfyUI** | existing graph shape makes SDXL the first integration control; avoid parallel engine |
| `lllyasviel/ControlNet@ed85cd1` | canonical edge/depth/pose/segmentation control family | structural-control evidence | **reuse weights/nodes, not code port** | base implementation is old and model compatibility matters; prefer ComfyUI core/current model-native nodes |
| `tencent-ailab/IP-Adapter@62e4af9` | official image-prompt adapter | reference/subject/style evidence | **reuse maintained ComfyUI node** | research repo establishes technique; application should not reimplement attention adapters |
| `comfyorg/comfyui-ipadapter@b188a6c` | maintained ComfyUI IP-Adapter nodes and example workflows | SDXL reference profile | **adopt candidate** | closest implementation seam; pins must be captured in Manager snapshot and compatibility tested |
| native ComfyUI GLIGEN/area/inpaint examples at ComfyUI pin | layout and localized edit controls | API workflow templates | **reuse first** | prefer core nodes/templates before custom region nodes; GLIGEN/model compatibility may limit route |
| `xinntao/Real-ESRGAN@a4abfb2` | practical restoration/upscale, tiling | pixel-space high-resolution candidate | **adopt candidate** | portable inference exists; documented tile seams and invented detail require acceptance checks |
| `JingyunLiang/SwinIR@6545850` | classical and real-world SR/restoration | second pixel-space candidate | **compare, do not stack by default** | retained only if it owns a quality/resource region not covered by native/Real-ESRGAN paths |
| `Karine-Huang/T2I-CompBench@1b70949` | compositional prompt set and evaluators | frozen prompt categories | **reuse dataset/categories** | full evaluator has heavyweight dependencies and imperfect proxies; use a bounded subset plus human review |
| `linzhiqiu/t2v_metrics@6ecb74f` | GenAI-Bench and VQAScore batch evaluation | semantic diagnostic adapter | **adopt candidate** | stronger published human correlation than CLIPScore for compositional prompts; still not sole acceptance truth |
| `MizzenAI/HPSv3@bd0c5fc` | current human-preference scorer | secondary triage score | **optional candidate** | preference is not control adherence and must not select a profile alone |
| `contentauth/c2pa-python@ea17c87` | read/sign/verify C2PA asset manifests | optional export after internal receipt | **defer** | client-facing portable provenance only; does not replace run-state evidence and may require signing policy |

## Custom-logic decision record

| Proposed logic | GitHub-first result | Decision |
| --- | --- | --- |
| ComfyUI installation, launch, and dependency restoration | official comfy-cli and Manager already own it | reuse them; do not build an installer |
| Graph execution and event parsing | official API example matches current adapter; Salad adds scale features not needed here | keep/refit the thin adapter and reconcile all error events in P0 |
| Model/control workflow nodes | core ComfyUI plus maintained IP-Adapter provide them | compose pinned API-format graphs; do not port diffusion/control code |
| Workflow-to-Python conversion | maintained exporter exists but changes the execution boundary | reject for the service; reconsider only for a single-shot offline deliverable |
| Image evaluation | T2I-CompBench, VQAScore, HPSv3, and task-specific CV/OCR components exist | write only a thin manifest/result normalizer; no new reward model or benchmark framework |
| GPU timing and memory | ComfyUI events/logs plus platform telemetry expose most inputs; no audited component supplied the exact Printline receipt | allow small receipt glue around monotonic time and sampled peak GPU/RAM; do not create a profiler framework |
| Upscaling/restoration | native nodes, Real-ESRGAN, and SwinIR exist | compare components; do not implement a custom super-resolution model |
| Portable provenance | C2PA binding exists | integrate only for a client requirement after the internal receipt is complete |

## Integration checks required after research

Every adopted component still needs: installation from a frozen manifest; one
successful case; one relevant failure (missing model/node, invalid graph, OOM or
timeout as applicable); the shared Printline receipt; and one composition case
for any profile advertised as composable. No component is authorized for
implementation by this dossier.

## Maintenance and security boundary

Custom ComfyUI nodes execute Python in the generation environment. A workflow
gallery link or Manager listing is not a trust decision. Later implementation
must pin an allowlist, review repository/source changes, restore in an isolated
environment, and keep unneeded partner/API nodes disabled. Model provenance and input consent remain client-specific checks.
