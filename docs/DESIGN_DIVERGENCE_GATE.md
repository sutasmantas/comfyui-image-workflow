# Printline design-divergence gate

Date: 2026-08-01

## Restart boundary

- repository: `portfolio_demos/generative_workflow`
- baseline: clean local `main` at `48ae8082edb030cef3bcb683f5cc8401cae7f73f`
- branch: `agent/printline-design-divergence`
- isolated worktree: `portfolio_demos/worktrees/printline_design`
- read-only repositories: every other portfolio repository and worktree,
  especially ContextSidecar
- exact next action: replace Printline's marketing-like paper layout with the
  image-dominant creative workstation specified below, without changing its
  queue/API behavior

## Why the former identity failed

The first Printline MRE differed in interaction, but its warm paper background,
oversized uppercase masthead, bordered controls, and editorial landing-page
rhythm overlapped Website Assistant and parts of Atlas. The project-start record
described a metaphor but did not prove visual difference from rendered peers.

## Rendered portfolio comparison

| Product | Evidence inspected | Spatial model | Navigation | Palette/type | Surface model | Dominant interaction |
| --- | --- | --- | --- | --- | --- | --- |
| Atlas | `knowledge_assistant/docs/screenshots/atlas-library.png`, `qa_cover_distinct.png` | editorial answer/library canvas | compact top nav | warm light, navy/violet, serif display | quiet rounded panels and tables | ask, inspect citations/sources |
| Relay | `support_automation/docs/screenshots/relay-case-workspace.png` | dense three-region case workspace | dark left work rail | white/navy/teal, compact sans | dividers, panes, restrained cards | select case, approve action |
| Website Assistant | running page source and widget | centered storefront landing page plus floating chat | none | warm cream, cobalt/orange, huge uppercase sans | bordered content blocks | read page, open assistant |
| Voice direction | `ui_design_previews/rendered/voice.png` | immersive session stage | session controls | graphite/cyan, technical sans | minimal dark panels | listen, speak, transfer |
| Ledger direction | `ui_design_previews/rendered/ledger.png` | document and field split | collapsible queue | paper/charcoal/amber | square document geometry | inspect and correct evidence |
| SignalRoom direction | `ui_design_previews/rendered/signal.png` | analytical curve and ranked table | compact rail/top controls | navy/lime, analytical sans | dense chart/table panels | adjust policy and compare |
| Printline corrected | `docs/screenshots/printline-workstation-1440.png` | dominant artboard with L-shaped recipe/filmstrip console | compact utility bar | metallic gray/carbon/coral, compact sans + mono | hard-edged instrument deck | tune, render, inspect/select frame |

### Pairwise difference audit

The hard dimensions are spatial model and dominant interaction. The five
additional dimensions are navigation, palette, typography, geometry, and
information density.

| Compared with | Spatial model | Dominant interaction | Additional dimensions that differ | Result |
| --- | --- | --- | --- | --- |
| Atlas | artboard console vs answer/library canvas | render/select frame vs ask/inspect evidence | navigation, palette, typography, geometry, density | PASS |
| Relay | L-shaped creative workspace vs three-region case workspace | tune/render vs select/approve action | navigation, palette, typography, geometry, density | PASS |
| Website Assistant | viewport workstation vs scrolling landing page + floating widget | tune/render vs read/open chat | navigation, palette, typography, geometry, density | PASS |
| Voice | metallic artboard console vs immersive dark session stage | render/select frame vs speak/interrupt/transfer | navigation, palette, geometry, density | PASS |
| Ledger Lens | artboard + bottom filmstrip vs queue + document + field inspector | generate/select output vs inspect/correct source evidence | navigation, palette, typography, density | PASS |
| SignalRoom | image workstation vs chart/table decision canvas | render/select frame vs change/compare policy | navigation, palette, typography, geometry, density | PASS |

## Replacement identity

- product metaphor: a creative render workstation, not a campaign landing page
- spatial model: one dominant artboard at left, a narrow recipe deck at right,
  and a bottom render filmstrip; no hero, no card grid, no full-width form strip
- navigation: one compact utility bar; the workspace itself is the product
- palette: cool aluminum gray, carbon black, white artboard, signal coral, and
  sparse ultraviolet markers; no warm paper or acid-yellow application chrome
- typography: compact mixed-case grotesque/system labels with monospace run
  metadata; no oversized uppercase display headline
- geometry: square instrument panels, hairline dividers, inset rails, and hard
  artboard edges; no floating rounded-card collection
- density: medium creative-tool density with the generated image dominant
- primary interaction: tune a recipe beside the artboard, render, watch a small
  stage meter, and inspect the selected output in the filmstrip

## Hard acceptance ledger

| Requirement | Evidence | Status |
| --- | --- | --- |
| Queue, validation, deterministic artifact, error, and retry behavior do not regress | `python -m unittest discover -s tests -v`: 11 passed; Playwright: 4 passed | PASS |
| Spatial model and dominant interaction differ from every compared project | pairwise audit above and 1440 px successful working-state comparison | PASS |
| At least three additional dimensions differ from every closest neighbor | pairwise audit records four or five differences for every project | PASS |
| 1440 px working state passes without relying on logo/accent | `docs/screenshots/printline-workstation-1440.png`; image/artboard/console silhouette remains unique | PASS |
| 1024 px layout has no overlap or horizontal clipping | `printline-workstation-1024.png` plus DOM `scrollWidth` and key-element bounds assertions | PASS |
| 390 px layout has no overlap or horizontal clipping | `printline-workstation-390.png` plus DOM `scrollWidth` and key-element bounds assertions | PASS |
| Failure and retry remain visible and usable in the new composition | Playwright provider-failure test reached `failed`, exposed handoff, retried to `succeeded`, and retained `retry_of` | PASS |
| Future-project template contains a rendered differentiation gate | updated portfolio template and authoritative plan | PASS |
| Clean-checkout verification | detached worktree at `9f95f02` passed compileall, 11 tests, smoke demo, and clean status; worktree then removed | PASS |

## Verification record

- branch: `agent/printline-design-divergence`
- application commit: `db5d20a`
- evidence candidate: `9f95f02`
- static/syntax: `python -m compileall -q printline tests scripts main.py`
- focused behavior: `python -m unittest discover -s tests -v` — 11 passed
- rendered behavior: Playwright — 4 passed at 1440, 1024, and 390 plus
  provider failure/retry; no page errors, document overflow, or key-element
  bounds failures
- manual review correction: the first 1440 render exposed a vertically clipped
  square artboard; sizing was changed from viewport width to available canvas
  height and all screenshots/tests were rerun
- remaining boundary: screenshots prove this local deterministic workflow; they
  do not add evidence of a live model/GPU execution

Every redesign row is `PASS`, including clean-checkout verification. This
checkpoint commit is the merge handback; stop before unrelated polish.
