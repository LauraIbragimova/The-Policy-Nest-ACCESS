# MVP Scope — ACCESS Rollout Planner

**Version:** 1.0  
**Date:** July 2026  
**Owner:** The Policy Nest

---

## Objective

Build a focused, interactive web app that takes organization-specific inputs and generates a phased ACCESS Model implementation roadmap — with a lightweight update-flagging panel for new CMS guidance.

---

## Primary User

An operations lead, ACO director, or VBC strategist at a provider organization that is evaluating or preparing to participate in the CMS ACCESS Model.

---

## User Flow (MVP)

1. User lands on the app
2. User completes a short intake form (organization type, track, readiness, timeline)
3. App generates a phased rollout plan based on inputs
4. User reviews and edits tasks, owners, and dates
5. User sees a "Recent Updates" panel showing flagged CMS/Federal Register changes
6. User exports or copies a clean plan summary

---

## Inputs

| Field | Type | Options |
|-------|------|---------|
| Organization type | Select | Health system, ACO, NP-led practice, FQHC, Other |
| Chronic condition track | Select | Hypertension, Diabetes, MSK pain, Depression, Multi-condition |
| Planned participation start | Date | Month/Year picker |
| Staffing readiness | Scale | Not ready / Partially ready / Ready |
| Technology readiness | Scale | Not ready / Partially ready / Ready |
| Reporting/data readiness | Scale | Not ready / Partially ready / Ready |
| Care model readiness | Scale | Not ready / Partially ready / Ready |
| Key constraints (optional) | Text | Free text |

---

## Outputs

| Output | Description |
|--------|-------------|
| Phased rollout plan | 4–5 phases with tasks, owners, and timeline |
| Risk register | 5–8 most relevant risks based on readiness inputs |
| Regulatory checkpoints | Key ACCESS compliance milestones |
| Recent updates panel | Flagged CMS/Federal Register changes (Phase 3) |
| Export summary | Printable/copyable plan overview |

---

## Rollout Phases (Base Template)

| Phase | Name | Focus |
|-------|------|-------|
| 1 | Readiness Assessment | Gap analysis, team alignment, eligibility confirmation |
| 2 | Operational Design | Workflow mapping, care team roles, vendor selection |
| 3 | Technology & Reporting Setup | EHR configuration, data feeds, reporting infrastructure |
| 4 | Enrollment & Launch | Beneficiary alignment, staff training, go-live |
| 5 | Monitoring & Optimization | Performance tracking, compliance, continuous improvement |

---

## MVP Limits (What Version 1 Will NOT Do)

- No user accounts or saved plans
- No PHI collection or processing
- No backend server or database
- No automatic plan rewriting from federal updates (flagging only)
- No multi-user collaboration
- No EHR or CMS system integration
- No coverage of non-ACCESS VBC programs

---

## Technology Stack (MVP)

- HTML / CSS / JavaScript (static, no framework required)
- JSON data files for plan templates and source config
- Federal Register API (Phase 3, read-only monitoring)
- GitHub Pages for hosting (optional)

---

## Success Criteria

- A user can complete the intake and receive a usable rollout plan in under 3 minutes
- The plan output is specific enough to use as a starting point for real project management
- The update panel clearly shows what changed and which plan section it may affect
- The app works on desktop without any installation or login
