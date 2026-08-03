# Printline MRE architecture

```text
recipe form
   │ POST /api/jobs
   ▼
validation ──► ComfyUI API-format graph compiler
   │
   ▼
single worker queue ──► adapter contract ──► artifact storage
   │                        │
   │                        ├─ deterministic local SVG
   │                        └─ optional ComfyUI /prompt + /ws + /history + /view
   ▼
job state + recipe + graph digest + artifact hash
   │ GET /api/jobs/{id}
   ▼
horizontal run timeline and contact sheet
```

The queue is intentionally in-memory and single-process. That is sufficient to
prove lifecycle handling but is not durable infrastructure. The browser polls a
small status endpoint; ComfyUI's own adapter consumes its WebSocket events on
the worker side.
