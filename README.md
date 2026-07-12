# ACCESS Rollout Planner
### A Policy Nest Digital Product

> AI-powered implementation planning tool for CMS ACCESS Model participants

---

## What It Does

The ACCESS Rollout Planner converts an organization's profile — type, track selection, phase, and readiness gaps — into a structured, phase-by-phase implementation roadmap aligned with CMS ACCESS Model requirements.

It is designed for value-based care operations leads, ACO administrators, and healthcare consultants who need to move from CMS guidance to executable action fast.

---

## The Problem

The CMS ACCESS Model (Advancing Chronic Care with Effective, Scalable Solutions) launched July 5, 2026 and runs through 2036. It introduces 10 chronic condition tracks, outcome attainment thresholds, G-code billing requirements, 425-day reporting deadlines, and HIE integration mandates. Most participating organizations lack a structured operational playbook to translate that policy complexity into day-to-day execution.

---

## Target User

- ACO administrators and operations directors
- Value-based care program managers at FQHCs, health systems, and physician groups
- Healthcare consultants supporting ACCESS applicants
- Policy Nest customers building implementation capacity

---

## MVP Features

- [ ] Organization type selector (ACO, FQHC, Health System, Physician Group, Rural Health Clinic)
- [ ] Track selector (CKM, MSK, BH, Oncology)
- [ ] Phase selector (Phases 1–5)
- [ ] Readiness gap flags (5 categories)
- [ ] AI-generated phase-by-phase rollout plan
- [ ] Risk registry with gap-prioritized risks surfaced first
- [ ] Regulatory checkpoint log (12 checkpoints)
- [ ] KPI tracker (OAT rate, 425-day compliance, alignment volume, withheld payment recovery, co-management billing)
- [ ] Quality tracker (measure submission, baseline capture, care update transmission)
- [ ] Work breakdown structure with 40+ tasks across 5 phases
- [ ] Federal Register live updates panel
- [ ] Export to text / Print to PDF
- [ ] Light and dark mode
- [ ] Mobile responsive

---

## Data Sources

| Source | Use |
|--------|-----|
| CMS ACCESS Model RFA | Track requirements, eligibility, payment rules |
| CMS ACCESS Technical FAQ | Billing codes, HIE requirements, device policy |
| ArentFox Schiff Payment Guidance | OAT thresholds, 425-day deadlines, substitute spend |
| Federal Register API | Live rulemaking updates surfaced in the app |

---

## File Structure

```
The-Policy-Nest-ACCESS/
├── README.md                   ← Project overview
├── index.html                  ← Main app (single-file, pending approval)
├── assets/
│   └── policy-nest-logo.jpg   ← Brand logo
├── data/
│   └── access-tracks.json     ← Track/condition reference data
└── notes/
    └── mvp-scope.md           ← Full product blueprint (WBS, risks, KPIs)
```

---

## Build Roadmap

| Phase | Description | Status |
|-------|-------------|--------|
| 1 | README + Project Blueprint | ✅ Complete |
| 2 | App scaffold + design system | ⏳ Pending approval |
| 3 | Plan generation logic + risk/KPI/quality panels | ⏳ Pending |
| 4 | Federal Register API integration | ⏳ Pending |
| 5 | Export, polish, QA | ⏳ Pending |

---

## About The Policy Nest

The Policy Nest creates digital tools and frameworks that help healthcare organizations implement CMS policy with confidence. This product is part of the ACCESS Implementation Series.

**[Visit The Policy Nest →](https://lauraibragimova.github.io/The-Policy-Nest-ACCESS/)**

---

*Built with AI assistance. Not legal or clinical advice. Always verify against current CMS guidance.*
