# Project 2 — Workflow Pipeline & Backend Implementation
## The Policy Nest: ACCESS Rollout Planner

**Author:** Laura Ibragimova (solo submission)
**Course project:** builds directly on our final project topic.
**Live UI (existing front-end):** https://lauraibragimova.github.io/The-Policy-Nest-ACCESS/
**Repository:** https://github.com/LauraIbragimova/The-Policy-Nest-ACCESS (this `project-2/` folder)
**Main project overview:** see the [root README](../README.md) for the full product context, features, and roadmap.

> This folder is the **Project 2** submission. It implements and verifies the backend/workflow engine for the ACCESS Rollout Planner described in the [root README](../README.md).

---

## 1. Final Project Topic

**The Policy Nest — ACCESS** is a value-based care (VBC) planning tool for the CMS
**ACCESS model** (an Accountable Care / shared-savings style program running in the
2026–2036 window). A healthcare organization — an ACO, FQHC, rural clinic, health
system, oncology practice, or digital-health provider — uses the tool to plan its
rollout: which clinical tracks to run, which readiness gaps it must close, and what
its **enrollment ramp** and **shared-savings** trajectory look like over the
performance-year horizon.

The current scope is the **ACCESS model specifically**. If it proves useful, the same
engine is designed to expand to other VBC programs (MSSP, other CMS Innovation Center
models) by adding new parameter sets.

The existing front-end (`ACCESS Rollout.html`, in the repo root) is a self-contained
single-page tool. **Project 2 takes the core logic that runs inside that page and
re-implements it as a real, runnable, testable Python backend** — the "behind the
scenes" layer the assignment asks for.

---

## 2. Workflow Pipeline

See **`pipeline_diagram.png`** for the visual version. In words, a request flows
through six stages plus an error/fallback path:

| # | Stage | What happens | Where |
|---|-------|--------------|-------|
| 1 | **User / data input** | Organization type, selected clinical tracks, flagged readiness gaps, and optional assumption overrides enter the system (as an HTTP POST body, or as a function call in the demo). | client / `demo_run.py` |
| 2 | **Validation** | FastAPI + Pydantic validate the payload: org / track / gap codes must be known; numeric overrides must be in range. Bad input is rejected here. | `app.py` |
| 3 | **Resolve assumptions** | The org's base panel is scaled by a track factor, then user overrides are merged on top of computed defaults (user edits win). Produces 7 tunable parameters. | `projection_engine.py` |
| 4 | **Core projection model** | Deterministic, rule-based math. A **logistic S-curve** ramps enrollment from the starting panel toward steady state. A **savings-maturity** curve (full by ~year 4) is dragged down by unresolved readiness gaps. Each year computes gross savings → program cost → **net savings** → **entity shared-savings share**, for 6 performance years (2026–2031). | `projection_engine.py` |
| 5 | **Optional AI narrative** | *(optional)* If an `OPENAI_API_KEY` is configured, an LLM writes a short executive summary of the projection. If not, a deterministic template summary is produced instead. | `ai_narrative.py` |
| 6 | **Output / result** | A JSON result: per-year rows, cumulative net savings, cumulative entity share, peak enrolled panel, and (optionally) the executive summary. Consumed by the API response, the demo table, or a future UI. | `app.py` / `demo_run.py` |

**Error handling / fallback steps**
- **Invalid input** → HTTP `422` with a clear message naming the valid options (never a stack trace).
- **AI unavailable** (no key, offline, or API error) → automatically falls back to the deterministic template summary, so the `/narrative` endpoint **always succeeds**.

### A note on "AI/tool/model interaction"
The **core** ACCESS workflow is intentionally **deterministic rule-based modeling, not
AI** — the numbers must be transparent and auditable for a healthcare-finance audience.
To satisfy the assignment's AI-interaction dimension honestly, the pipeline adds an
**optional** AI layer (stage 5) that *explains* the numbers but never changes them, and
degrades gracefully when no model is available.

---

## 3. What Backend / Workflow Parts I Completed

Everything in `backend/`:

- **`projection_engine.py`** — the core workflow logic. A **1:1 port** of the model that
  runs in `ACCESS Rollout.html`: assumption defaults, the logistic enrollment ramp,
  savings maturity + gap drag, and the gross → cost → net → share calculation, plus
  formatting helpers.
- **`app.py`** — a **FastAPI backend** exposing the engine over HTTP:
  `GET /health`, `GET /options`, `POST /projection`, `POST /narrative`.
  Input validation and error handling live here (Pydantic models + validators).
- **`ai_narrative.py`** — the optional AI executive-summary layer with graceful
  template fallback.
- **`test_projection.py`** — a **19-test pytest suite**. Two tests assert the Python
  output matches the web app **to the cent** (golden values captured from the app's own
  `computeProjection()`); the rest cover model behavior, validation, error handling, and
  the API routes.
- **`demo_run.py`** — a runnable demo (no server needed) that prints a formatted
  projection table + executive summary and writes `sample_output.json`.
- **`requirements.txt`** — dependencies.

Verification artifacts (in `backend/`): **`verification_log.txt`** (captured test +
demo run) and **`sample_output.json`** (a full sample result). A screenshot of the
diagram is `pipeline_diagram.png`.

---

## 4. How to Set Up and Run

Requires Python 3.10+.

```bash
cd project-2/backend
python -m venv .venv && source .venv/bin/activate     # optional
pip install -r requirements.txt
```

### Run the verification tests
```bash
pytest -v
# 19 passed — including the two "matches the web app" parity tests
```

### Run the demo (sample input → sample output)
```bash
python demo_run.py                 # ACO scenario
python demo_run.py --scenario fqhc # FQHC scenario
# prints a projection table + executive summary; writes sample_output.json
```

### Run the API server
```bash
uvicorn app:app --reload --port 8000
```
Then, in another terminal:
```bash
# valid request
curl -X POST http://127.0.0.1:8000/projection \
  -H "Content-Type: application/json" \
  -d '{"org_value":"aco","tracks":["eckm","bh"],"gaps":["data"]}'

# projection + executive summary
curl -X POST http://127.0.0.1:8000/narrative \
  -H "Content-Type: application/json" \
  -d '{"org_value":"fqhc","tracks":["ckm"],"gaps":[]}'
```
Interactive API docs are auto-generated at http://127.0.0.1:8000/docs.

### (Optional) Enable the AI summary
```bash
export OPENAI_API_KEY=sk-...       # if unset, the template summary is used automatically
```

---

## 5. Sample Output (verification)

Running `python demo_run.py` produces (ACO, tracks eCKM + BH, gap Data):

```
   PY  Year   Enrolled        Gross      Program          Net        Share
    1  2026      7,080       $1.73M       $3.89M      -$2.16M           $0
    2  2027      9,757       $4.77M       $5.37M       -$597K           $0
    3  2028     12,645       $9.27M       $6.95M       $2.32M       $1.16M
    4  2029     14,798      $14.47M       $8.14M       $6.33M       $3.16M
    5  2030     16,003      $15.64M       $8.80M       $6.84M       $3.42M
    6  2031     16,571      $16.20M       $9.11M       $7.09M       $3.54M
  Peak aligned panel      : 16,571
  Cumulative net savings  : $19.81M
  Cumulative entity share : $11.29M
```

These figures are identical to what the live web app displays for the same inputs — the
parity is enforced by the test suite. See `backend/verification_log.txt` for the full
captured run and `backend/sample_output.json` for the raw JSON.

---

## 6. What Still Needs to Be Completed for the Final Project

- **Wire the front-end to the backend.** The existing `ACCESS Rollout.html` currently
  runs the math client-side; the final version will call the `POST /projection` and
  `POST /narrative` endpoints so a single engine powers everything.
- **Persist scenarios server-side** (save/compare multiple rollout plans per user)
  instead of `localStorage` only.
- **Expand beyond ACCESS** — add parameter sets for other CMS VBC programs (MSSP, etc.),
  which the engine is structured to support.
- **Harden the AI layer** — prompt tuning, caching, and cost controls for the executive
  summary; potentially add an AI-assisted assumption-suggestion feature.
- **Deployment** — containerize and host the API; add authentication.

---

## 7. Connection Between Project 2 and the Final Project

Project 2 **is** the engine of the final project. The final deliverable is the ACCESS
planner; this submission implements and verifies the exact backend workflow that turns a
user's rollout choices into a multi-year enrollment-and-savings projection — the part
that runs "behind the scenes." The parity tests guarantee that when the final UI is
pointed at this backend, users see the same results they see today, now served by a
runnable, testable, extensible Python service.
