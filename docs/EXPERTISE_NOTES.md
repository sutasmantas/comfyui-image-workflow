# Printline expertise notes

**Verification:** [claim-to-artifact map and rerun commands](https://sutasmantas.github.io/evidence/#printline) · [machine-readable receipt](https://sutasmantas.github.io/evidence/receipt.json)

Date: 2026-08-05
Evidence state: systematic research only; P0–P5 are unexecuted

These notes preserve consequential routing and delivery decisions. “Result”
means an externally established or provisional research conclusion unless a
local measurement is explicitly named. The current 11 tests and smoke run prove
only the deterministic fixture-backed service contract.

## Match image evaluation to the control being promised

### Client trigger

- Job wording or deliverable that makes this relevant: controlled image
  generation, pose/layout adherence, product or style consistency, text in
  images, or an image-quality comparison.
- How often it appeared in the measured corpus or proposal log: no defensible
  frequency is recorded; it is a direct Printline delivery risk.
- Existing project/component that can be reused: Printline receipts,
  T2I-CompBench categories, VQAScore, OCR/CV measures, and blind review design.

### Failure symptom or unanswered choice

An output can receive an attractive semantic or preference score while missing
the supplied pose, depth, object position, exact text, or reference subject.

### Competing options

| Option | Why it is plausible | Main cost or failure risk |
| --- | --- | --- |
| One aggregate reward/preference score | cheap ranking and simple dashboard | hides which contractual control failed and transfers evaluator bias |
| Condition-specific metric only | directly measures edge/depth/pose/layout/OCR/reference | proxy threshold can miss visible artifacts and client taste |
| Condition metric + semantic diagnostic + blind acceptance | separates hard control from overall usability | more evaluator and review work |

### Controlled comparison

- Evidence-reuse level: triangulated external answer.
- External sources and applicability checks: the T2I quality-metric survey
  separates compositional/general quality; GenAI-Bench finds VQAScore stronger
  than CLIPScore on compositional prompts; ImagenHub reports that automatic
  metrics have weak human correlation for most conditional-generation tasks.
  Those findings match Printline's mixed control profiles.
- Contrary evidence, benchmark limitations, or unresolved disagreement:
  VQAScore can miss fine visual detail; preference models do not measure control;
  condition metrics can be gamed or mis-thresholded.
- Representative cases or fixtures: P1 text/composition prompts and P2
  edge/depth/pose/layout/reference cases.
- Frozen development/held-out split: defined in `BENCHMARK_DESIGN.md`; not yet
  materialized.
- Metrics and decision thresholds chosen before the run: each hard condition
  uses its matching metric; automatic acceptance requires no observed held-out
  hard-failure false accept and a reported coverage bound.
- Runtime, hardware, model/provider version, cost assumptions, and date:
  unmeasured; pins and compute are required in P1–P5 receipts.
- What is deliberately outside the comparison: a universal aesthetic truth or
  client brand acceptance without client review.

### Result

Established research conclusion: no single automatic score closes Printline's
acceptance decision. FID is also unsuitable as the primary small-sample metric.
Local evaluator thresholds and selective coverage remain unknown until P5.

### Decision rule

Choose the hard metric from the supplied control, add semantic/preference scores
as diagnostics, and retain blind human accept/reject for visible artifacts and
client fit. Re-test thresholds when the base model, control type, asset domain,
or failure cost changes.

### Delivery control

Return per-asset control results and rejection reasons with the run receipt; do
not release or auto-accept an image that fails a declared hard control even when
its aggregate score improves.

### Reuse boundary

- Reusable without client data: metric routing, frozen rubric, blinded review,
  and receipt schema.
- Requires client data, credentials, environment, or acceptance criteria:
  thresholds, brand/style judgment, exact text and allowed-error policy.
- Unsupported claim that must not appear in a proposal: “Printline automatically
  proves image quality” or any local metric accuracy before P5.

### Proposal-safe insight

I separate the requested control—such as pose, layout, text, or reference
consistency—from general image preference, so a visually appealing score cannot
hide a failed requirement. Final thresholds still need representative client
assets and acceptance criteria.

### Evidence

- Code: `printline/adapters.py`, `printline/service.py` (receipt foundation).
- Tests: current 11 tests; no evaluator calibration test yet.
- Raw comparison artifacts: none; P1–P5 unexecuted.
- Human review, if used: planned randomized blind protocol only.
- Reproduction command: current baseline commands in `BENCHMARK_DESIGN.md`.

### Interview follow-up

- Likely technical question: why not use CLIPScore, HPS, or FID alone?
- Short answer: each measures a different proxy; none proves the supplied
  control, and FID is ill-suited to a small conditional comparison.
- Deeper evidence to open if challenged: `EVIDENCE_MATRIX.csv` rows P20–P26 and
  P5 in `BENCHMARK_DESIGN.md`.

### Central index disposition

- Added or updated card in `UPWORK_EXPERTISE_INDEX.md`: yes.
- Card heading, if indexed: `Match image evaluation to the promised control`.
- If not indexed, exact reason: not applicable.

## Treat multiple image controls as an interaction, not an additive guarantee

### Client trigger

- Job wording or deliverable that makes this relevant: preserve a product or
  person reference while also enforcing pose, depth, edges, layout, or style.
- How often it appeared in the measured corpus or proposal log: no defensible
  frequency recorded; it is explicitly proposed by Printline's portfolio plan.
- Existing project/component that can be reused: ComfyUI graph profiles,
  ControlNet, IP-Adapter, and the P2 factorial design.

### Failure symptom or unanswered choice

Two controls work separately, but when combined one is ignored or the image
develops distortion, semantic leakage, or excessive compute/rejection cost.

### Competing options

| Option | Why it is plausible | Main cost or failure risk |
| --- | --- | --- |
| Prompt-only | lowest weight and dependency surface | cannot enforce supplied visual conditions |
| One control at a time | isolates the declared requirement | cannot satisfy tasks that genuinely require both |
| Combined branches | graph is composable and can express both | guidance competition, weight tuning, VRAM, and failure interactions |

### Controlled comparison

- Evidence-reuse level: triangulated external answer plus required portfolio
  comparison.
- External sources and applicability checks: ControlNet and IP-Adapter establish
  composability; newer multi-condition work documents conflicting guidance and
  motivates adaptive/unified selection. The conflict applies directly to a
  ControlNet + IP-Adapter Printline profile.
- Contrary evidence, benchmark limitations, or unresolved disagreement: a
  compatible pair may work at selected weights; no external study pins
  Printline's model, references, and settings.
- Representative cases or fixtures: P2 cases that require both structure and
  reference preservation.
- Frozen development/held-out split: six development and six held-out structural
  cases, with reference cases separated by source.
- Metrics and decision thresholds chosen before the run: both individual
  control gates, human acceptance, artifact rejection, and resource budget.
- Runtime, hardware, model/provider version, cost assumptions, and date:
  unmeasured; maximum P2 budget in `BENCHMARK_DESIGN.md`.
- What is deliberately outside the comparison: arbitrary many-control graphs or
  automatic weight search.

### Result

Contested research conclusion: connection-level composition is established,
but quality-level composition is not. The combined profile remains blocked
until it beats both relevant single-control cells on cases needing both.

### Decision rule

Use the smallest control set that expresses the requirement. Add a second
control only when a frozen interaction cell passes both control gates and the
resource/acceptance budget; re-test after model, node, or auxiliary-weight
changes.

### Delivery control

Ship single-control fallbacks and record control weights/start-stop schedules in
the receipt. A combined path cannot silently fall back to an unverified graph.

### Reuse boundary

- Reusable without client data: factorial cell design and separate gates.
- Requires client data, credentials, environment, or acceptance criteria:
  client reference/control images, priority when constraints conflict, and
  acceptable degradation.
- Unsupported claim that must not appear in a proposal: “ControlNet and
  IP-Adapter combine reliably” before P2.

### Proposal-safe insight

When a workflow must preserve both structure and a reference, I validate the
combined path against each single-control fallback; connecting two nodes does
not prove that both requirements survive generation.

### Evidence

- Code: no combined graph implemented.
- Tests: none; P2 is unexecuted.
- Raw comparison artifacts: none.
- Human review, if used: planned blind acceptance.
- Reproduction command: P2 design in `BENCHMARK_DESIGN.md`.

### Interview follow-up

- Likely technical question: how would you detect one control suppressing the
  other?
- Short answer: factorial cells with matched seeds and a separate metric for
  each supplied condition, plus human artifact review.
- Deeper evidence to open if challenged: matrix row P27 and P2.

### Central index disposition

- Added or updated card in `UPWORK_EXPERTISE_INDEX.md`: yes.
- Card heading, if indexed: `Test combined image controls against each single-control fallback`.
- If not indexed, exact reason: not applicable.

## Compare generation cost per accepted output

### Client trigger

- Job wording or deliverable that makes this relevant: choose a fast/local image
  model, reduce GPU spend, batch creative generation, or meet turnaround time.
- How often it appeared in the measured corpus or proposal log: no defensible
  frequency recorded; it is a direct model-routing decision.
- Existing project/component that can be reused: Printline attempts, terminal
  receipts, artifact hashes, and P1/P4 resource instrumentation.

### Failure symptom or unanswered choice

A candidate has lower per-render latency or higher preference score but produces
more rejected images, OOMs, retries, or manual rework.

### Competing options

| Option | Why it is plausible | Main cost or failure risk |
| --- | --- | --- |
| Optimize render latency | easy and objective | ignores load time, failures, rejects, and regeneration |
| Optimize quality score | rewards better-looking outputs | ignores compute and proxy/acceptance mismatch |
| Optimize accepted-output cost under hard gates | maps to delivery outcome | needs explicit rejection labels and full receipts |

### Controlled comparison

- Evidence-reuse level: engineering decision grounded in external model/resource
  diversity; portfolio comparison required.
- External sources and applicability checks: official cards span 2.5B, 12B and
  20B candidates and one-to-many step counts, demonstrating that resource
  profiles differ; they do not report Printline acceptance economics.
- Contrary evidence, benchmark limitations, or unresolved disagreement: a
  small workload may value absolute quality over throughput; reviewer time can
  dominate GPU time.
- Representative cases or fixtures: P1 held-out prompt categories and P4
  delivery-size assets.
- Frozen development/held-out split: defined, not yet materialized.
- Metrics and decision thresholds chosen before the run: attempts, accepts,
  failure/OOM, cold/warm time, peak memory, disk, reviewer rejects, and total
  time/compute per accepted output.
- Runtime, hardware, model/provider version, cost assumptions, and date:
  all must be in the live receipt; currently unmeasured.
- What is deliberately outside the comparison: a production cloud price or SLA.

### Result

Provisional decision rule established; no candidate has a measured cost or
acceptance advantage. P1/P4 will determine non-dominated operating regions.

### Decision rule

Promote a fast or quality profile only when it satisfies hard controls and owns
a lower accepted-output cost or higher accepted coverage inside the declared
resource limit. Re-test when hardware, model, delivery dimensions, or rejection
cost changes.

### Delivery control

Report attempted, failed, rejected, and accepted outputs together; set an OOM,
time, disk, and regeneration stop budget before a batch.

### Reuse boundary

- Reusable without client data: receipt fields and accepted-output calculation.
- Requires client data, credentials, environment, or acceptance criteria:
  rejection cost, reviewer time, target hardware, throughput/SLA.
- Unsupported claim that must not appear in a proposal: any Printline model is
  “fastest,” “cheapest,” or “best quality” before P1/P4.

### Proposal-safe insight

I compare image-generation routes on time and compute per accepted asset, not
only per render, because a faster model can cost more once rejects and retries
are included. The actual route depends on the client's hardware and approval
criteria.

### Evidence

- Code: current job timestamps and artifact state are a partial receipt.
- Tests: current lifecycle tests; no GPU/resource tests.
- Raw comparison artifacts: none.
- Human review, if used: planned accept/reject labels.
- Reproduction command: P1 and P4 designs.

### Interview follow-up

- Likely technical question: how do you compare models with different native
  step counts and resolutions?
- Short answer: compare declared deployable profiles and normalize at the
  accepted delivery artifact, while preserving each profile's native settings.
- Deeper evidence to open if challenged: foundation rows P01–P04 and P1/P4.

### Central index disposition

- Added or updated card in `UPWORK_EXPERTISE_INDEX.md`: yes.
- Card heading, if indexed: `Price generation profiles per accepted asset`.
- If not indexed, exact reason: not applicable.

## Start with tuning-free reference control before training a LoRA

### Client trigger

- Job wording or deliverable that makes this relevant: consistent product,
  character, subject, or visual style across generated assets.
- How often it appeared in the measured corpus or proposal log: no defensible
  frequency recorded.
- Existing project/component that can be reused: IP-Adapter, native reference
  editing, conditional P3 LoRA cell, and versioned receipts.

### Failure symptom or unanswered choice

Prompting drifts from an approved reference, but immediately training a custom
adapter may add dataset, overfitting, privacy, training, and maintenance cost
before simpler reference conditioning has been tested.

### Competing options

| Option | Why it is plausible | Main cost or failure risk |
| --- | --- | --- |
| Prompt-only | no reference pipeline | weak subject/style consistency |
| IP-Adapter/native reference edit | tuning-free and fast to change references | similarity/editability tradeoff and model compatibility |
| LoRA | reusable learned style/subject | training/data/versioning cost and overfit/diversity loss |

### Controlled comparison

- Evidence-reuse level: triangulated external answer; client-specific P3 only if
  tuning-free route fails.
- External sources and applicability checks: IP-Adapter establishes a small
  tuning-free adapter compatible with text/control; LoRA ecosystem and newer
  work establish efficient training but document overfit and diversity risks.
- Contrary evidence, benchmark limitations, or unresolved disagreement: LoRA
  may win for many repeated assets; generic similarity scores do not prove
  identity or style.
- Representative cases or fixtures: approved non-face product, subject, and
  style references; faces excluded initially.
- Frozen development/held-out split: split by reference source and prompt.
- Metrics and decision thresholds chosen before the run: subject/style separated,
  text editability, diversity, acceptance, setup/training time, and storage.
- Runtime, hardware, model/provider version, cost assumptions, and date:
  unknown until P3.
- What is deliberately outside the comparison: unauthorized identity cloning or
  unconsented reference assets.

### Result

Established routing principle, unmeasured Printline winner: tuning-free
reference control is the first comparison; LoRA is conditional on repeated
volume and a held-out gain that pays for training and governance.

### Decision rule

Use prompt-only when consistency is not contractual; test a tuning-free adapter
for an approved reference; train/version LoRA only when repeated volume and
held-out acceptance justify it. Re-test when the base model or reference domain
changes.

### Delivery control

Require approved/consented reference assets, keep a prompt-only fallback, and
version every trained adapter with its dataset and held-out receipt.

### Reuse boundary

- Reusable without client data: route and experiment protocol.
- Requires client data, credentials, environment, or acceptance criteria:
  approved references, consent, repetition volume, and similarity/style target.
- Unsupported claim that must not appear in a proposal: identity preservation,
  brand consistency, or superior LoRA quality before P3/client validation.

### Proposal-safe insight

I test tuning-free reference conditioning before proposing custom training, then
reserve LoRA for repeated approved assets where a held-out gain justifies the
extra training and versioning surface.

### Evidence

- Code: no reference or LoRA profile implemented.
- Tests: none; P3 unexecuted.
- Raw comparison artifacts: none.
- Human review, if used: planned P3 protocol.
- Reproduction command: P3 design.

### Interview follow-up

- Likely technical question: when would you skip IP-Adapter and train?
- Short answer: only when tuning-free reference control fails a repeated,
  accepted workload and the gain covers data/training/maintenance cost.
- Deeper evidence to open if challenged: rows P12–P15 and P3.

### Central index disposition

- Added or updated card in `UPWORK_EXPERTISE_INDEX.md`: yes.
- Card heading, if indexed: `Test tuning-free reference control before training a LoRA`.
- If not indexed, exact reason: not applicable.

## A replayable image receipt needs more than prompt and seed

### Client trigger

- Job wording or deliverable that makes this relevant: reproducible generation,
  audit trail, retry, disputed output, or migration between GPU environments.
- How often it appeared in the measured corpus or proposal log: already present
  as the canonical Printline expertise card.
- Existing project/component that can be reused: workflow/artifact digest,
  recipe, timestamps, retry lineage, ComfyUI Manager snapshot, and P0.

### Failure symptom or unanswered choice

The same prompt and seed produce a different image or a failed run cannot be
explained because model, nodes, control inputs, precision, or hardware changed.

### Competing options

| Option | Why it is plausible | Main cost or failure risk |
| --- | --- | --- |
| Save output only | simplest artifact record | cannot reconstruct inputs/environment |
| Save prompt and seed | familiar reproducibility claim | omits graph/model/node/input/precision/hardware |
| Normalized live receipt | supports diagnosis and bounded replay | more hashes and environment capture; GPU may still be nondeterministic |

### Controlled comparison

- Evidence-reuse level: current implemented control plus narrow P0 reproduction.
- External sources and applicability checks: ComfyUI embeds workflows in
  generated files and Manager snapshots environment components; current
  Printline already proves graph/artifact/retry receipt fields.
- Contrary evidence, benchmark limitations, or unresolved disagreement:
  same-seed byte equality can fail across kernels/hardware; snapshots omit some
  model/driver facts.
- Representative cases or fixtures: current fixed PNG, P0 live SDXL success,
  warm replay, and missing-model/node failure.
- Frozen development/held-out split: P0 three prompts × two seeds; no model
  quality claim.
- Metrics and decision thresholds chosen before the run: receipt completeness,
  terminal reconciliation, artifact hash, pixel equality or declared SSIM/LPIPS
  tolerance, time, memory, and error classification.
- Runtime, hardware, model/provider version, cost assumptions, and date:
  current fixture is CPU/no-key; live facts unknown until P0.
- What is deliberately outside the comparison: production durability and
  universal bitwise determinism.

### Result

Measured current fact: identical fixture-backed recipes preserve graph and PNG
hashes in tests. Established gap: this is not a live GPU replay result. P0 must
add model/node/input/control/hardware/precision facts and define replay tolerance.

### Decision rule

Persist the complete recipe, graph/model/node/control/input revisions/digests,
runtime settings, hardware/software, artifact hashes, timestamps, state, and
retry lineage. Claim exact replay only if P0 demonstrates it within the pinned
environment; otherwise state the measured tolerance.

### Delivery control

Do not mark success before history/output retrieval and hashing reconcile to one
terminal receipt. A retry creates a linked new receipt; it never overwrites the
failed attempt.

### Reuse boundary

- Reusable without client data: schema, hashes, lineage, and failure receipt.
- Requires client data, credentials, environment, or acceptance criteria:
  live weights, GPU environment, inputs, and acceptable replay tolerance.
- Unsupported claim that must not appear in a proposal: live ComfyUI
  reproducibility, exact GPU determinism, or durable production audit trail.

### Proposal-safe insight

I preserve the workflow, model/environment facts, inputs, artifact hash, and
retry lineage together, so a disputed render can be traced to the execution that
produced it. Printline's live GPU replay tolerance still needs P0 measurement.

### Evidence

- Code: `printline/workflow.py`, `printline/adapters.py`, `printline/service.py`.
- Tests: `test_same_recipe_has_same_workflow_digest` and
  `test_same_seed_and_settings_produce_same_artifact_hash`.
- Raw comparison artifacts: fixed PNG only; no live run.
- Human review, if used: not applicable to P0 receipt correctness.
- Reproduction command: current baseline commands in `BENCHMARK_DESIGN.md`.

### Interview follow-up

- Likely technical question: does a seed guarantee identical GPU images?
- Short answer: no; pin all execution facts and measure byte equality or a
  declared pixel/perceptual tolerance in the actual environment.
- Deeper evidence to open if challenged: P0 and matrix rows P28–P33.

### Central index disposition

- Added or updated card in `UPWORK_EXPERTISE_INDEX.md`: updated existing card.
- Card heading, if indexed: `Reproducibility needs the recipe and the artifact`.
- If not indexed, exact reason: not applicable; this deepens an existing card
  rather than adding a duplicate retrieval path.

## Separate layout control from structure control

### Client trigger

- Job wording or deliverable that makes this relevant: exact object count,
  placement, size, poster regions, or text blocks rather than merely preserving
  an edge/depth/pose map.
- How often it appeared in the measured corpus or proposal log: no defensible
  frequency recorded; professional design applicability exposed the gap.
- Existing project/component that can be reused: ComfyUI area/mask nodes,
  GLIGEN example, img2img/inpaint graph, and P2 layout cells.

### Failure symptom or unanswered choice

A structural control preserves the supplied contours yet produces the wrong
object count, semantic placement, text region, or out-of-distribution boundary
layout.

### Competing options

| Option | Why it is plausible | Main cost or failure risk |
| --- | --- | --- |
| Prompt-only | no input authoring | unreliable count/position/size |
| Edge/depth/pose control | strong geometry signal | does not express semantic layout by itself |
| Regional/layout or iterative masked path | explicitly assigns regions and can repair locally | compatibility, leakage, ordering, and extra passes |

### Controlled comparison

- Evidence-reuse level: established external family plus portfolio comparison.
- External sources and applicability checks: modern surveys separate layout from
  structure and subject control; LayoutBench shows in-distribution success may
  fail at arbitrary boundaries; commercial-design benchmarks separately measure
  text and layout.
- Contrary evidence, benchmark limitations, or unresolved disagreement: native
  newer models may follow simple layouts from text; GLIGEN compatibility is
  dated.
- Representative cases or fixtures: count, position, size, boundary, text-region,
  and product/poster cases.
- Frozen development/held-out split: P2 layout split; not yet materialized.
- Metrics and decision thresholds chosen before the run: detection/count,
  layout IoU, OCR where relevant, non-target artifacts, acceptance, time/VRAM.
- Runtime, hardware, model/provider version, cost assumptions, and date:
  unmeasured.
- What is deliberately outside the comparison: full editable graphic-design
  document generation or vector/layer export.

### Result

Established taxonomy correction: layout is a separate Printline decision
family. The compatible implementation winner is unknown, so GLIGEN, regional
conditioning, and iterative editing remain provisional P2 candidates.

### Decision rule

Use structural control for supplied geometry and layout control for semantic
count/placement/size. Prefer the simplest native regional path that passes
boundary cases; route failed global layouts to bounded masked iteration rather
than adding more prompt text.

### Delivery control

Freeze expected regions/counts and require layout/OCR plus visual acceptance
before release; keep the prompt-only or structure-only artifact as a comparison,
not a silent fallback.

### Reuse boundary

- Reusable without client data: family distinction, boundary cases, and metrics.
- Requires client data, credentials, environment, or acceptance criteria:
  actual layout, typography, editability, and acceptable pixel/region tolerance.
- Unsupported claim that must not appear in a proposal: production graphic
  design, exact typography, or a validated layout winner before P2.

### Proposal-safe insight

I treat semantic layout as a separate acceptance problem from edge, depth, or
pose control; preserving a contour does not prove the right object, count, or
text landed in the right region.

### Evidence

- Code: existing `workflows/basic_image_to_image.json` is only an unused input
  graph; no layout profile implemented.
- Tests: none; P2 unexecuted.
- Raw comparison artifacts: none.
- Human review, if used: planned P2 protocol.
- Reproduction command: P2 design.

### Interview follow-up

- Likely technical question: why not use ControlNet for layout too?
- Short answer: structural conditions and semantic regions express different
  constraints; measure count/position/size separately.
- Deeper evidence to open if challenged: taxonomy structure/layout sections,
  rows P06–P11, and P2.

### Central index disposition

- Added or updated card in `UPWORK_EXPERTISE_INDEX.md`: no.
- Card heading, if indexed: not applicable.
- If not indexed, exact reason: too narrow for a separate retrieval path; the
  distinct buyer behavior is already captured by `Match image evaluation to the
  promised control` and the combined-control card.
