# The Policy Nest — ACCESS Rollout Planner

> AI-assisted implementation planning tool for the CMS ACCESS (Advancing Chronic Care with Effective, Scalable Solutions) Model

---

## What This Is

The ACCESS Rollout Planner is a lightweight, interactive web app that helps healthcare organizations translate the CMS ACCESS Model requirements into a structured, operational implementation roadmap. Users answer a short intake about their organization and readiness, and the app generates a phased rollout plan with tasks, suggested owners, risks, and regulatory checkpoints.

The app also monitors publicly available federal and CMS sources for ACCESS program updates, and flags which plan sections may be affected — surfacing suggested revisions for human review rather than automatically overwriting content.

---

## Problem It Solves

The CMS ACCESS Model is a 10-year voluntary payment model for technology-enabled chronic care. Organizations that want to participate need to understand program requirements, sequence their operational steps, and stay current as guidance evolves. Most teams lack a structured planning tool that is specific to ACCESS — generic project plan generators do not understand the program's tracks, timelines, or regulatory structure.

This tool bridges the gap between policy text and operational execution.

---

## Target User

- ACO directors and operations leads preparing for ACCESS participation
- NP-led practices and federally qualified health centers evaluating the model
- VBC strategy consultants supporting provider onboarding
- Healthcare policy and implementation teams at health systems

---

## MVP Features (Version 1)

- [ ] Organization intake form (type, track, timeline, readiness)
- [ ] Phased rollout plan generated from inputs
- [ ] Editable task list with suggested owners, risks, and checkpoints
- [ ] "Recent Updates" panel flagging new CMS ACCESS guidance
- [ ] Export-ready plan summary view

---

## Planned Features (Future Builds)

- Federal Register API integration for automated regulatory monitoring
- CMS ACCESS page change detection and impact mapping
- Multi-track comparison view (chronic condition tracks)
- Payer alignment pathway module
- Plan versioning and change log

---

## Data Sources

| Source | Type | Use |
|--------|------|-----|
| [CMS ACCESS Model Page](https://www.cms.gov/priorities/innovation/innovation-models/access) | Public CMS webpage | Program requirements, eligibility, deadlines |
| [CMS ACCESS Technical FAQ](https://www.cms.gov/priorities/innovation/access-technical-frequently-asked-questions) | Public CMS webpage | Implementation guidance |
| [Federal Register API](https://www.federalregister.gov/developers/documentation/api/v1) | Public REST API | Regulatory rule monitoring |

All data sources are publicly available. No PHI is collected or processed.

---

## Project Structure

```
The-Policy-Nest-ACCESS/
├── index.html                  # Main app shell
├── style.css                   # Layout and design
├── app.js                      # Input handling, plan generation, update logic
├── data/
│   ├── access-template.json    # Base rollout phases, tasks, risks, checkpoints
│   └── source-config.json      # Source URLs and monitoring rules
├── notes/
│   ├── mvp-scope.md            # MVP scope and decision log
│   ├── access-workflow.md      # ACCESS planning framework
│   └── update-logic.md        # Update monitoring approach
└── README.md
```

---

## Build Phases

| Phase | Goal | Status |
|-------|------|--------|
| 1 | Project blueprint and documentation | 🔄 In Progress |
| 2 | Static planner — form + generated plan view | ⬜ Not Started |
| 3 | Update monitor — CMS/Federal Register flag panel | ⬜ Not Started |
| 4 | UI polish and export summary | ⬜ Not Started |

---

## Built By

**The Policy Nest** — a healthcare policy and operations studio building the toolkits ACO directors, NP-led practices, and VBC strategists need for CMS model transitions.

---

## License

© 2026 The Policy Nest. All Rights Reserved.
