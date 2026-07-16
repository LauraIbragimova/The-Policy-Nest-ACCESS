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

See **Section 8 (Deployment)** below for hosting the API on a server and configuring
`OPENAI_API_KEY` there.

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

- **Wire the front-end to the backend.** *(done)* The Projections tab of
  `ACCESS Rollout.html` now has an optional "Backend API" control: paste a running
  backend URL to compute via `POST /narrative` and show the executive summary. The
  built-in client-side math remains the default so the tool still works fully offline,
  and any API failure falls back to it gracefully.
- **Persist scenarios server-side** (save/compare multiple rollout plans per user)
  instead of `localStorage` only.
- **Expand beyond ACCESS** — add parameter sets for other CMS VBC programs (MSSP, etc.),
  which the engine is structured to support.
- **Harden the AI layer** — prompt tuning, caching, and cost controls for the executive
  summary; potentially add an AI-assisted assumption-suggestion feature.
- **Production deployment** — containerize, add authentication, and restrict CORS to the
  known front-end origin (see Section 8).

---

## 7. Connection Between Project 2 and the Final Project

Project 2 **is** the engine of the final project. The final deliverable is the ACCESS
planner; this submission implements and verifies the exact backend workflow that turns a
user's rollout choices into a multi-year enrollment-and-savings projection — the part
that runs "behind the scenes." The parity tests guarantee that when the final UI is
pointed at this backend, users see the same results they see today, now served by a
runnable, testable, extensible Python service.

---

## 8. Deployment Guide

The front-end (`ACCESS Rollout.html`) is a static file hosted on **GitHub Pages**, which
**cannot run Python**. So the backend is deployed *separately* and the front-end is
pointed at its URL. Because the app falls back to its built-in engine when no backend is
reachable, the hosted site keeps working whether or not the API is running.

### 8.1 Environment variables

| Variable | Required? | Purpose |
|----------|-----------|---------|
| `OPENAI_API_KEY` | Optional | Enables the **AI** executive summary at `POST /narrative`. If unset (or the call fails), the endpoint automatically returns the deterministic **template** summary instead — it never hard-fails. |
| `ACCESS_AI_MODEL` | Optional | Overrides the OpenAI model used for the summary. Defaults to `gpt-4o-mini`. Only relevant when `OPENAI_API_KEY` is set. |

There is no `PORT` environment variable read by the code — the port is set on the start
command via `--port` (or `-b` for Gunicorn). Most hosts expose a `$PORT` value you pass
into that flag, e.g. `--port $PORT` (shown in Section 8.4).

Set the key locally:
```bash
export OPENAI_API_KEY=sk-...        # macOS / Linux
setx OPENAI_API_KEY "sk-..."        # Windows (new shell after)
```
**Never commit the key.** `backend/.gitignore` already excludes `.env`; keep secrets
there or in the host's secrets manager (below), not in code.

Optional `backend/.env` for local dev (loaded manually or via your shell):
```
OPENAI_API_KEY=sk-...
```

### 8.2 Run locally (development)
```bash
cd project-2/backend
pip install -r requirements.txt
export OPENAI_API_KEY=sk-...        # optional — omit to use the template summary
uvicorn app:app --reload --port 8000
```
Verify it is up:
```bash
curl http://127.0.0.1:8000/health   # -> {"status":"ok"}
```
Then open the front-end (`ACCESS Rollout.html`), go to the **Projections** tab, and paste
`http://127.0.0.1:8000` into the **Backend API** field. Click **Sync with API** — the
status should read *"Mode: Live API"* and an executive summary appears. This is the
simplest way to demo the API live (e.g. for grading).

### 8.3 Run for production (single command)
```bash
cd project-2/backend
pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port ${PORT:-8000}
```
`--host 0.0.0.0` makes it reachable from outside the machine; drop `--reload` in
production. For heavier load, run under Gunicorn with Uvicorn workers:
```bash
pip install gunicorn
gunicorn -k uvicorn.workers.UvicornWorker -w 2 -b 0.0.0.0:${PORT:-8000} app:app
```

### 8.4 Deploy to a host (Render / Railway / Fly.io / etc.)
Any host that runs a Python web process works. General steps:
1. Point the service at this repo, **root directory `project-2/backend`**.
2. **Build command:** `pip install -r requirements.txt`
3. **Start command:** `uvicorn app:app --host 0.0.0.0 --port $PORT`
4. **Environment variables:** add `OPENAI_API_KEY` in the host's dashboard (optional).
5. Deploy, then confirm `https://<your-app>.<host>/health` returns `{"status":"ok"}`.
6. In the deployed front-end's **Backend API** field, paste `https://<your-app>.<host>`
   and click **Sync with API**.

### 8.5 Deploy with Docker (optional)
No Dockerfile is committed yet; a minimal one:
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```
```bash
cd project-2/backend
docker build -t access-api .
docker run -p 8000:8000 -e OPENAI_API_KEY=sk-... access-api
```

### 8.6 CORS note
The API currently allows all origins (`allow_origins=["*"]` in `app.py`) so the
front-end can call it from a local file or from GitHub Pages during development. For a
real production deployment, restrict it to the known front-end origin, e.g.:
```python
allow_origins=["https://lauraibragimova.github.io"]
```

### 8.7 Deployment checklist
- [ ] `pip install -r requirements.txt` succeeds
- [ ] `GET /health` returns `{"status":"ok"}`
- [ ] `POST /projection` returns a projection for a valid payload
- [ ] `OPENAI_API_KEY` set (AI summary) **or** confirmed the template summary is acceptable
- [ ] Front-end **Backend API** field points at the deployed URL and syncs successfully
- [ ] (Production) CORS narrowed to the real front-end origin
