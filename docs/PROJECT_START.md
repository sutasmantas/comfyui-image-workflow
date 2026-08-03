# Generative workflow project foundation and identity record

## 1. Restart boundary

- repository: `portfolio_demos/generative_workflow`
- baseline branch and commit: `main` at `3cc6b17af9725c42b9a3eb1f8be960f0e66215b6`
- implementation branch: `agent/generative-workflow-mre`
- assigned isolated worktree: `portfolio_demos/worktrees/generative_workflow_mre`
- owner/session: current Codex portfolio breadth stream
- repositories/worktrees that are read-only: every other repository and worktree, especially `context_sidecar`, `support_automation`, and `website_assistant`
- exact next action: implement and verify the one-workflow queued generative-media slice below

Never share an active worktree or switch branches inside this assigned worktree.

## 2. Client outcome and non-duplication

- one client-purchased outcome this project proves: a parameterized image-generation workflow can be queued, observed, reproduced, failed safely, retried, and handed back with artifact metadata
- existing portfolio evidence closest to it: Relay proves agent/tool approvals and webhook delivery; Website Assistant proves streamed conversation and consented handoff
- mechanism or deliverable that is genuinely new: a reproducible ComfyUI-compatible media workflow with generation settings, execution progress, and media artifact provenance
- why this is better coverage than deepening an existing project: it unlocks generative-media automation claims without duplicating chat, RAG, or support-agent behavior

## 3. GitHub foundation comparison

These are private working projects for the user. License research and ranking were deliberately excluded.

| Candidate | Repository | Activity/version checked | Central behavior reusable for this MRE | Adaptation cost/risk | Decision |
| --- | --- | --- | --- | --- | --- |
| 9elements ComfyUI API | `https://github.com/9elements/comfyui-api` | HEAD `3cc6b17`, checked 2026-08-01 | Small Python client already queues `/prompt`, consumes `/ws` progress, reads `/history`, retrieves `/view` artifacts, and parameterizes a real text-to-image workflow | Old dependency pins and hard-coded paths require replacement, but the protocol surface is compact | SELECTED |
| Comfy-Org comfy-cli | `https://github.com/Comfy-Org/comfy-cli` | HEAD `d3220c9`, checked 2026-08-01 | Installs/launches ComfyUI and runs workflows, including UI-to-API conversion | CLI-first surface does not provide the job/provenance product slice; adopting it would still require a service layer | Reuse guidance only |
| SaladTechnologies ComfyUI API | `https://github.com/SaladTechnologies/comfyui-api` | HEAD `4dfc930`, checked 2026-08-01 | Queues ComfyUI prompts and adds webhooks, storage providers, model download, and horizontal scaling | Production orchestration is materially broader than this one-day local MRE | Reject for scope |

Selected foundation:

- repository URL: `https://github.com/9elements/comfyui-api`
- pinned tag/commit: `3cc6b17af9725c42b9a3eb1f8be960f0e66215b6`
- exact code/package/contracts reused: API-format workflow JSON; `/prompt` queue submission; `/ws` progress and completion events; `/history/{prompt_id}` output metadata; `/view` artifact retrieval
- upstream history/identity preservation: repository was cloned with its upstream history; the original remote is retained as `upstream`; adaptation starts on a separate branch/worktree
- why this is faster/safer than starting blank: queue, progress, history, image retrieval, and a runnable ComfyUI graph already exist together and can be wrapped behind a tested adapter contract

## 4. Distinct visual direction

- correction record: the initial paper/oversized-heading direction failed user
  review because it overlapped Website Assistant and parts of Atlas; it is
  superseded by `docs/DESIGN_DIVERGENCE_GATE.md`
- comparison projects/screenshots reviewed: rendered Atlas, Relay, Website
  Assistant source, Voice, Ledger Lens, and SignalRoom working environments plus
  the five-product direction board
- product/audience metaphor: a creative render workstation for an art director
  preparing and reproducing a campaign key visual
- layout structure: dominant artboard, L-shaped recipe/filmstrip console, compact
  utility bar, and a small execution transport; no hero, card grid, floating
  chat, permanent navigation rail, or three-column document/case workspace
- palette: cool aluminum, carbon, white artboard, signal coral, and sparse
  ultraviolet markers; no warm-paper application chrome
- typography character: compact mixed-case system typography with monospaced
  run metadata; no oversized uppercase display headline
- primary interaction pattern: tune the recipe beside the image, render, inspect
  progress, and select the generated frame in the filmstrip
- explicit patterns avoided because another project already uses them: Atlas
  editorial research canvas, Relay queue/case panes, Website Assistant landing
  page and floating widget, Voice dark session stage, Ledger three-column
  document review, and SignalRoom chart/table dashboard
- responsive and side-by-side evidence: `docs/screenshots/` and
  `docs/DESIGN_DIVERGENCE_GATE.md`

The corrected structural identity is implemented and verified; decorative
animation and non-functional embellishment remain out of scope.

## 5. Minimum referenceable evidence contract

| Gate | Observable acceptance evidence | Status |
| --- | --- | --- |
| Central similarity | The pinned ComfyUI API-format graph is parameterized and the live adapter implements `/prompt`, `/ws`, `/history`, and `/view` | PASS |
| Working vertical slice | Browser check queued the default campaign-key-visual recipe, reached `succeeded / 100%`, rendered an artifact, and exposed metadata | PASS |
| No-key deterministic proof | Two identical local runs produced workflow digest `b6073f41d9acc...` and artifact SHA `8c3185972134...` | PASS |
| Invalid input and abuse behavior | Structured validation rejects unknown fields, empty/oversized prompts, unsupported dimensions, invalid settings, and bodies over 32 KiB | PASS |
| Provider/tool failure and retry/refusal/handoff | Unit and browser checks observed the safe error panel, actionable handoff, retry refusal for success, and a successful linked retry | PASS |
| Focused mechanism tests | `python -m unittest discover -s tests -v` passed 11 workflow/service/HTTP tests | PASS |
| Clean-checkout quickstart | `compileall`, 11 tests, and smoke demo passed from detached worktree at `f70ec62`; detached worktree was then removed | PASS |
| Cover-letter claim ledger | `docs/CLAIM_LEDGER.md` maps six supported claims to concrete code/tests and supplies safe wording | PASS |
| Honest unsupported-claim boundary | Ledger explicitly excludes hosted/GPU/model success, production scale, durability, auth, and image-quality claims | PASS |

Only all `PASS` closes the MRE. Stop before decorative polish, extra providers, or broad production hardening.

## 6. Verification and handback

- static/type/lint command: `git diff --check`
- focused tests: `python -m unittest discover -s tests -v` — 11 passed
- integration command: `python scripts/smoke_workflow.py` — succeeded with stable digest/SHA; two Playwright flows passed for completion and failure/retry
- build/package command: `python -m compileall -q printline tests scripts main.py`
- branch and verified implementation commit: `agent/generative-workflow-mre` at `f70ec62f9ca87b746472fc2633d65fcf81892af6`; the checkpoint commit follows it
- clean state: detached clean-checkout verification passed at `f70ec62`; branch state is rechecked at handback
- known boundaries: default execution is deterministic/local; the SVG is a contract proof rather than AI output; live ComfyUI requires a compatible server/checkpoint and was not executed here
- exact next portfolio action: integrate this MRE locally, update the authoritative breadth checkpoint, and stop before polish
