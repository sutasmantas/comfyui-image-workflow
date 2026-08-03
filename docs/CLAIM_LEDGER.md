# Printline cover-letter claim ledger

## Supported now

| Claim | Direct evidence | Verification |
| --- | --- | --- |
| Built a parameterized generative-media workflow | `WorkflowTemplate.compile` mutates prompt, negative prompt, seed, dimensions, steps, CFG, and output prefix in a real ComfyUI API-format graph | `test_parameterizes_real_comfyui_graph` |
| Implemented queued execution with observable progress and errors | `JobService` serializes work through a worker and records queued/running/succeeded/failed stages | service and HTTP tests; browser conveyor |
| Made runs reproducible and auditable | Run record retains recipe, workflow digest, artifact SHA-256, adapter metadata, and timestamps | `test_same_seed_and_settings_produce_same_artifact_hash` |
| Added failure recovery | Provider failures retain an actionable message and handoff; retry creates a new run linked by `retry_of` | `test_provider_failure_is_actionable_and_retry_succeeds` |
| Integrated a local model-workflow protocol | Optional adapter implements ComfyUI `/prompt`, `/ws`, `/history`, and `/view` flow inherited from the pinned foundation | adapter code plus graph test; live server is not required for local proof |
| Delivered a no-key end-to-end workflow | Fixture adapter persists a generated PNG showcase image through the same service and UI contract, with an explicit non-live boundary in metadata | `scripts/smoke_workflow.py` and HTTP artifact test |

Safe compact wording:

> Built a queued generative-media workflow around a ComfyUI-compatible graph,
> with parameterized recipes, progress/error states, a documented no-key fixture,
> retry provenance, and artifact metadata.

## Not supported

Do not claim any of the following without new evidence:

- production deployment, horizontal scaling, multi-tenant isolation, or uptime;
- a hosted GPU, installed diffusion checkpoint, or successful live ComfyUI run;
- subjective image quality, model benchmarking, or improved generation metrics;
- video generation, batch campaigns, external storage, callbacks, or webhooks;
- authentication, authorization, billing, or persistent database storage;
- exact-once queue delivery, crash recovery, or durable jobs after restart.

The bundled PNG is a generated showcase fixture. It is not evidence that this
repository executed a live ComfyUI model.
