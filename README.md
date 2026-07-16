# ACCESS Rollout Planner
### A Policy Nest Digital Product

> Rule-based implementation planning tool for CMS ACCESS Model participants, with optional AI assistance

---

## What It Does

The ACCESS Rollout Planner converts an organization's profile — type, track selection, phase, and readiness gaps — into a structured, phase-by-phase implementation roadmap aligned with CMS ACCESS Model requirements. It also projects enrollment ramp and shared-savings over the performance-year horizon.

The core planning and projection logic is **deterministic and rule-based** — transparent, auditable math a reviewer can reproduce by hand — which matters for a healthcare-finance audience. An **optional AI layer** can generate a plain-English executive summary of the projections; when no AI model is configured, the tool falls back to a deterministic template so it always works.

It is designed for value-based care operations leads, ACO administrators, and healthcare consultants who need to move from CMS guidance to executable action fast.

---

## The Problem

The CMS ACCESS Model (Advancing Chronic Care with Effective, Scalable Solutions) launched July 5, 2026 and runs through 2036, with rolling participant start dates (the next on August 17, 2026 and October 1, 2026). It introduces 4 chronic condition tracks (high blood pressure, diabetes, chronic musculoskeletal pain, and depression), outcome attainment thresholds, G-code billing requirements, 425-day reporting deadlines, and HIE integration mandates. Most participating organizations lack a structured operational playbook to translate that policy complexity into day-to-day execution.

---

## Target User

- ACO administrators and operations directors
- Value-based care program managers at FQHCs, health systems, and physician groups
- Healthcare consultants supporting ACCESS applicants
- Policy Nest customers building implementation capacity

---

## MVP Features

- [x] Organization type selector (ACO, FQHC, Health System, Physician Group, Rural Health Clinic, Oncology, Digital Health)
- [x] Track selector (eCKM, CKM, MSK, BH, Oncology)
- [x] Phase selector (Phases 1–5)
- [x] Readiness gap flags (5 categories: data, workforce, interoperability, finance, governance)
- [x] Rule-based phase-by-phase rollout plan
- [x] Projections tab: enrollment ramp line chart + savings-by-year bar chart
- [x] Risk registry with gap-prioritized risks surfaced first
- [x] Regulatory checkpoint log
- [x] KPI tracker (OAT rate, 425-day compliance, alignment volume, withheld payment recovery, co-management billing)
- [x] Quality tracker (measure submission, baseline capture, care update transmission)
- [x] Work breakdown structure across 5 phases
- [x] Export to text / Print to PDF
- [x] Federal Register updates panel
- [x] Light and dark mode
- [x] Mobile responsive
- [ ] Optional AI executive-summary of projections (backend built in `project-2/`; UI wiring pending)
- [ ] Live Federal Register API integration (panel present; live feed pending)

---

## Data Sources

| Source | Use |
|--------|-----|
| CMS ACCESS Model RFA | Track requirements, eligibility, payment rules |
| CMS ACCESS Technical FAQ | Billing codes, HIE requirements, device policy |
| ArentFox Schiff Payment Guidance | OAT thresholds, 425-day deadlines, substitute spend |
| Federal Register API | Live rulemaking updates (planned) |

---

## File Structure

```
The-Policy-Nest-ACCESS/
├── README.md                   ← Project overview (this file)
├── index.html                  ← Landing page
├── ACCESS Rollout.html         ← Main app (single-file, self-contained)
├── style.css                   ← Shared styles
├── Policy Nest Logo.png        ← Brand logo
├── THE POLICY NEST.png         ← Brand wordmark
├── PNL RMVBG.png               ← Brand asset
├── data/
│   └── access-template.json    ← Track/condition reference data
├── notes/
│   ├── mvp-scope.md            ← Full product blueprint (WBS, risks, KPIs)
│   ├── access-workflow.md      ← Workflow notes
│   └── update-logic.md         ← Update/logic notes
└── project-2/                  ← Course Project 2: workflow pipeline + Python backend
    ├── README.md               ← Project 2 writeup
    ├── pipeline_diagram.png    ← Workflow pipeline diagram
    ├── pipeline_diagram.svg
    └── backend/                ← Runnable FastAPI backend (engine, tests, demo)
        ├── projection_engine.py
        ├── app.py
        ├── ai_narrative.py
        ├── test_projection.py
        ├── demo_run.py
        └── requirements.txt
```

---

## Build Roadmap

| Phase | Description | Status |
|-------|-------------|--------|
| 1 | README + Project Blueprint | ✅ Complete |
| 2 | App scaffold + design system | ✅ Complete |
| 3 | Plan generation logic + risk/KPI/quality panels | ✅ Complete |
| 4 | Projections tab (enrollment ramp + savings charts) | ✅ Complete |
| 5 | Python backend + workflow pipeline (Project 2) | ✅ Complete |
| 6 | Wire front-end to backend API | ⏳ Pending |
| 7 | Federal Register API integration | ⏳ Pending |
| 8 | Optional AI summary in UI, final polish + QA | ⏳ Pending |

---

## Course Project 2 — Workflow Pipeline & Backend

The course **Project 2** deliverable (workflow pipeline design + a runnable Python/FastAPI backend that implements the core enrollment-ramp and shared-savings projection logic, with tests, a demo run, and a pipeline diagram) lives in **[`project-2/`](./project-2)**. See **[`project-2/README.md`](./project-2/README.md)** for the full writeup, setup/run instructions, and verification results.

---

## About The Policy Nest

The Policy Nest creates digital tools and frameworks that help healthcare organizations implement CMS policy with confidence. This product is part of the ACCESS Implementation Series.

**[Visit The Policy Nest →](https://lauraibragimova.github.io/The-Policy-Nest-ACCESS/)**

---

*Built with AI assistance. Core planning and projections are rule-based; any AI-generated summaries are optional and clearly labeled. Not legal or clinical advice. Always verify against current CMS guidance.*
