# ACCESS Rollout Planner
### A Policy Nest Digital Product

**Turn CMS ACCESS Model guidance into a phase-by-phase rollout plan your team can run.** Pick your organization type, track, phase, and readiness gaps, and the planner builds the roadmap, risks, KPIs, go-live gates, and enrollment and savings projections.

**[Open the live planner →](https://lauraibragimova.github.io/The-Policy-Nest-ACCESS/)**

Built for ACO administrators, value-based care program managers at FQHCs, health systems, and physician groups, and consultants supporting ACCESS participants.

---

## The problem it solves

The CMS ACCESS Model (Advancing Chronic Care with Effective, Scalable Solutions) launched July 5, 2026 and runs through 2036, with rolling participant start dates. It brings 4 chronic condition tracks (high blood pressure, diabetes, chronic musculoskeletal pain, and depression), outcome attainment thresholds, G-code billing requirements, 425-day reporting deadlines, and HIE integration mandates. Most participating organizations have the policy documents but no operational playbook for day-to-day execution.

---

## What a VBC leader should look at

- **The rollout plan.** A phase-by-phase plan generated from your organization's profile, with the readiness gaps you flag (data, workforce, interoperability, finance, governance) surfaced first.
- **Hard go-live gates.** A checklist that must be cleared before launch: FHIR/API submission, PCP Care Update delivery, HIPAA, and FDA/device review.
- **Projections.** An enrollment ramp and shared savings by performance year.
- **Risk registry, KPI tracker, and quality tracker.** OAT rate, 425-day compliance, alignment volume, withheld payment recovery, co-management billing, measure submission, baseline capture, and care update transmission.
- **Regulatory checkpoint log and work breakdown structure** across all 5 phases.
- **Export.** Download as text or print to PDF to share with your team.

---

## How it uses AI, and where it doesn't

The plan and the projections are **rule-based**. A reviewer can reproduce every number by hand, which matters when finance and compliance teams need to trust the output.

AI is used in one place only: an **optional plain-English executive summary** of the projections. When no AI model is configured, the tool uses a fixed template instead, so it always works and the summary is always labeled.

---

## Sources

| Source | Use |
|--------|-----|
| CMS ACCESS Model RFA | Track requirements, eligibility, payment rules |
| CMS ACCESS Technical FAQ | Billing codes, HIE requirements, device policy |
| ArentFox Schiff Payment Guidance | OAT thresholds, 425-day deadlines, substitute spend |
| Federal Register API | Live rulemaking updates (planned) |

---

## What's next

- Connect the planner to the projection API so the projections run live.
- Show the optional AI executive summary in the planner.
- Pull live Federal Register updates into the updates panel.

---

## For developers

### File structure

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
└── project-2/                  ← Projection engine and API
    ├── README.md               ← Pipeline design, setup, run, and deployment
    ├── pipeline_diagram.png    ← Workflow pipeline diagram
    ├── pipeline_diagram.svg
    └── backend/                ← FastAPI backend (engine, tests, demo)
        ├── projection_engine.py
        ├── app.py
        ├── ai_narrative.py
        ├── test_projection.py
        ├── demo_run.py
        └── requirements.txt
```

### Projection engine and API

The enrollment-ramp and shared-savings logic is also available as a Python/FastAPI backend with tests, a demo run, and a pipeline diagram. See **[`project-2/README.md`](./project-2/README.md)** for setup, run, verification, and deployment instructions.

### Build status

| Phase | Description | Status |
|-------|-------------|--------|
| 1 | README + Project Blueprint | ✅ Complete |
| 2 | App scaffold + design system | ✅ Complete |
| 3 | Plan generation logic + risk/KPI/quality panels | ✅ Complete |
| 4 | Projections tab (enrollment ramp + savings charts) | ✅ Complete |
| 5 | Python backend + workflow pipeline | ✅ Complete |
| 6 | Wire front-end to backend API | ⏳ Pending |
| 7 | Federal Register API integration | ⏳ Pending |
| 8 | Optional AI summary in UI, final polish + QA | ⏳ Pending |

---

## About The Policy Nest

The Policy Nest creates digital tools and frameworks that help healthcare organizations implement CMS policy with confidence. This product is part of the ACCESS Implementation Series. See also the [LEAD Model Readiness Toolkit](https://github.com/LauraIbragimova/The-Policy-Nest-LEAD).

*Built with AI assistance. Core planning and projections are rule-based; any AI-generated summaries are optional and clearly labeled. Not legal or clinical advice. Always verify against current CMS guidance.*
