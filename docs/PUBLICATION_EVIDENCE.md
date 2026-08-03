# Printline publication evidence — 2026-08-03

## Verification results

| Gate | Command or artifact | Result |
| --- | --- | --- |
| Syntax | `python -m compileall -q printline tests scripts main.py` | PASS |
| Behavior | `python -m unittest discover -s tests -v` | 11 passed |
| End-to-end smoke | `python scripts/smoke_workflow.py` | succeeded PNG artifact, graph digest and explicit fixture metadata |
| Changed Python lint | Ruff on the adapter, changed tests, and publication scripts | PASS |
| Changed Python format | Ruff format check on the same files | PASS |
| Responsive browser | `python scripts/check_viewer_layout.py` | PASS at 1600×1200, 1024×900, and 390×844; filmstrip overflow is intentionally contained |
| Visual review | final screenshots and 1440/1024/390 repository screenshots | PASS |

## Final media

| File | Format | SHA-256 |
| --- | --- | --- |
| `final_upload/01_cover.png` | 1600×1200 PNG | `1784A7C4E4961D83FFD76C2691D4C51442F2F864F9CB7EB0C7FD04D5628B48A4` |
| `final_upload/02_workflow.png` | 1600×1200 PNG | `F960631228FE62E17F12E60BAFBDF5E7E7428DB77C8AC89FBF02A3A13A352EBC` |
| `final_upload/03_recovery.png` | 1600×1200 PNG | `A9D0CA16380CE7AA79F31B9F5351F836C1BE7F1A56CEA999EBC71AE4142285F2` |
| `final_upload/04_printline_walkthrough.mp4` | 17.68 s, 1600×1200, H.264/yuv420p | `3625DCD16025A71AD336A0B90EB3FD6E92ABE35622A1A47CCE9F1B1FC2CC05AA` |

The walkthrough has a stable opening frame, visible synthetic pointer,
full-sentence captions, smooth section navigation, real failure/retry
interaction, and a dedicated ending card.

## Evidence boundary

The no-key adapter copies a documented generated fixture through the real
service path. Provider metadata explicitly says it is not a live ComfyUI
execution. The graph compiler and live `/prompt` → `/ws` → `/history` → `/view`
adapter remain implemented and tested at their local contract boundary; a live
GPU/model run is not claimed.
