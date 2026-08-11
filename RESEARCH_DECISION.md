# Printline research decision

Date: 2026-08-05
Gate: systematic dossier `PASS`; experiment/technique ceiling `PARTIAL`

## Decision

Preserve Printline's current queue, API-format graph, deterministic fixture,
retry lineage, and artifact receipt as the software control. Do not add another
orchestration framework. The next depth work is a measured, modular set of
generation profiles behind the existing service boundary, beginning with a real
ComfyUI execution and receipt oracle.

The preliminary five-profile plan is refined to six workload profiles plus one
shared acceptance layer:

| Profile | Retained family | Current status | Routing trigger |
| --- | --- | --- | --- |
| `prompt-fast` | non-dominated SDXL/SD3.5/FLUX base candidate | provisional; P1 | greenfield image where prompt following and accepted-output cost matter more than exact geometry |
| `structure-controlled` | ControlNet or compatible lighter/native control | externally established family; P2 | client supplies or can derive edge/depth/pose/segmentation condition |
| `layout-controlled` | regional/area/layout grounding or iterative masked edit | newly added provisional family; P2 | object count, placement, size, text region, or composition is contractual |
| `reference-controlled` | IP-Adapter or compatible native reference/edit path | externally established family; P2/P3 | approved subject/product/style reference must persist without training |
| `style-adapted` | LoRA only after tuning-free failure and repeated-volume gate | conditional; P3 | enough approved repeated assets justify training and versioning cost |
| `delivery-resolution` | native/latent second pass or measured restoration route | provisional; P4 | accepted content needs a larger delivery artifact without invented detail |
| shared `acceptance` | condition-specific metrics + blinded human review + receipt | established design; calibration pending P5 | every profile; no profile self-certifies quality |

Localized editing is a workflow operation that may use the layout/reference
profiles, not a universal seventh marketing profile. Multi-control and
multi-reference are interaction cases: they are not advertised until their
combined cells beat the relevant single controls.

## Consequential external answers

1. **Prompt-only is not an equivalent substitute for explicit structure or
   layout.** ControlNet/T2I-Adapter, layout benchmarks, and ComfyUI core paths
   establish separate families. External evidence closes the family decision;
   it does not choose Printline's weights or model.
2. **Reference conditioning and LoRA answer different delivery economics.** A
   tuning-free adapter is the first route for a reference; LoRA is conditional
   on repeated approved work, measured gain, diversity/editability, and training
   cost.
3. **Evaluation must match the promised control.** Compositional VQA,
   structure/layout/OCR/reference measures, preference scoring, and blind human
   acceptance are complementary. FID is not valid as Printline's primary
   small-sample metric.
4. **Composability is not correctness evidence.** Multiple guidance branches
   can conflict. Combined control needs an explicit factorial cell and resource
   receipt.
5. **A seed and graph digest are not a live replay guarantee.** The receipt must
   include runtime, model/node/input/control, precision, hardware and artifact
   facts, and P0 must define tolerance if GPU outputs are not byte-identical.
6. **Quality must be priced per accepted output.** A fast render that creates
   more rejects/retries can lose to a slower profile, so latency and preference
   scores cannot be reported without acceptance and attempts.

## GitHub reuse decision

- Adopt later: pinned official ComfyUI, comfy-cli, Manager snapshot workflow,
  core graph/control/edit/upscale nodes, maintained ComfyUI IP-Adapter, bounded
  T2I-CompBench categories, and VQAScore diagnostic.
- Refit rather than replace: the current official-example-derived
  `ComfyUIAdapter`; add complete event/error/receipt normalization only in P0.
- Compare as components: Real-ESRGAN and SwinIR; retain at most non-dominated
  routes.
- Defer: Salad's scale/storage wrapper, C2PA portable manifests, face-specific
  identity components, and any paid provider.
- Reject now: a second Diffusers execution core, workflow-to-Python runner for
  the service, custom diffusion/control/upscale/evaluator models, and a large
  all-in-one custom node.

This is the required component-level GitHub check. Larger custom logic is not
justified. The only anticipated custom work is thin Printline-specific graph
parameterization, receipt normalization, manifest/result adapters, and routing.

## External-answer versus experiment queue

| Question | Evidence-reuse level | Result |
| --- | --- | --- |
| Does explicit structural/layout control add a real family? | established external answer | yes; retain independent profiles |
| Should reference conditioning automatically become LoRA training? | triangulated external answer | no; route by tuning-free acceptance and repeated volume |
| Is one automatic image score sufficient? | triangulated external answer plus contrary studies | no; require task metrics and human review |
| Is FID the primary small-sample metric? | established external contrary answer | no; exclude |
| Can official components own install, graph execution and core nodes? | implementation evidence | yes; adopt/refit instead of custom frameworks |
| Which base model wins on Printline hardware/workload? | unresolved/hardware-sensitive | P1 after P0 |
| Do combined structure/reference controls help rather than interfere? | contested | P2 factorial cell |
| When does LoRA earn its training cost? | client-data and volume sensitive | conditional P3 |
| Which delivery-resolution route preserves approved details? | asset sensitive | P4 |
| Which diagnostics can reduce human review safely? | domain/calibration sensitive | P5 |

## Exact first controlled experiment

P0 is the only admitted next experiment after a later checkpoint authorizes
work:

1. pin ComfyUI, comfy-cli/Manager snapshot, one real SDXL artifact set, and the
   existing seven-node graph;
2. reconcile the current adapter with official validation, execution-error,
   completion/history, timeout, and output events;
3. capture normalized run receipts for three prompts × two seeds, a warm replay,
   and one missing-model/node failure;
4. verify state/artifact/receipt reconciliation, graph and file digests, replay
   tolerance, wall time, peak memory, and actionable failure classification;
5. stop and write results before any P1 model comparison.

No model download, experiment, code implementation, UI change, generated image,
merge, or push is part of this dossier.

## Known limitations and claim boundary

- Printline has still not executed ComfyUI against a real checkpoint or GPU.
- No base model, control stack, evaluator, upscaler, latency, VRAM requirement,
  or quality threshold has won locally.
- The current fixed PNG remains the only exercised artifact path.
- Public benchmark prompts and papers do not prove client brand, product,
  person, typography, or delivery acceptance.
- The service remains an in-memory single-worker demo; durability, multi-worker
  scale, auth, external storage, webhooks, and production exactly-once behavior
  are unsupported.
- Licenses were intentionally irrelevant to discovery/ranking; a future client
  delivery can still require separate legal or provider-policy review.

## Systematic gate result

| Gate | Result | Evidence |
| --- | --- | --- |
| Problem decomposition | PASS | eight independent decisions in `TECHNIQUE_TAXONOMY.md` |
| Search protocol | PASS | dated sources, rules, iterations, and queries in taxonomy |
| Survey coverage | PASS | controllable-generation, T2I/editing, and quality-metric surveys |
| Benchmark coverage | PASS | T2I-CompBench++, GenAI-Bench, ConceptMix, LayoutBench, ImagenHub, and commercial-design applicability |
| Existing-answer search | PASS | every major question has reuse level in this file and `EVIDENCE_MATRIX.csv` |
| Technique-family saturation | PASS | two consecutive post-expansion searches added no top-level family |
| Candidate comparison | PASS | 36-row matrix plus component audit cover capability, quality, resources, integration, maintenance, and failures |
| Contrary evidence | PASS | FID, automatic metrics, LoRA overfit, OOD layout, and multi-control conflict recorded |
| Implementation evidence | PASS | 18 GitHub HEAD pins and explicit adopt/refit/defer/reject seams |
| Portfolio fit | PASS | controllable media receipts remain distinct from other projects |
| Review status | PASS | conclusions labeled established, provisional, contested, or unknown |

The dossier gate is `PASS`. P0–P5 remain unexecuted, so Printline's experiment
and technique-ceiling gate remains `PARTIAL`.
