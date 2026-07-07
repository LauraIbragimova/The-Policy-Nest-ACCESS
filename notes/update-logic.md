# Update Monitoring Logic

**Version:** 1.0  
**Date:** July 2026  
**Owner:** The Policy Nest

> This document defines how the ACCESS Rollout Planner will detect, classify, and surface regulatory and program updates to users — without automatically rewriting their plans.

---

## Design Principle

The update system is a **monitoring and flagging tool**, not an autonomous plan editor. When a relevant change is detected from a public federal or CMS source, the app:

1. Surfaces the update in a "Recent Updates" panel
2. Identifies which rollout phase(s) or task(s) may be affected
3. Proposes a suggested revision for the user to review
4. Requires user approval before any plan content changes

This approach keeps the planner accurate and credible without silently overwriting content the user has customized.

---

## Data Sources

### Source 1 — Federal Register API
**URL:** `https://www.federalregister.gov/api/v1/documents.json`  
**Type:** Public REST API, no authentication required  
**Use:** Monitor for formal proposed rules, final rules, and notices related to CMS ACCESS or related chronic care payment models

**Query parameters to use:**
```
agencies[]=centers-for-medicare-medicaid-services
conditions[terms]=ACCESS+Model
conditions[type][]=Rule
conditions[type][]=Proposed Rule
conditions[type][]=Notice
order=newest
per_page=5
```

**What to extract:**
- Document title
- Publication date
- Document type (Rule / Proposed Rule / Notice)
- Abstract/summary
- Full text URL

---

### Source 2 — CMS ACCESS Model Page
**URL:** `https://www.cms.gov/priorities/innovation/innovation-models/access`  
**Type:** Public CMS webpage  
**Use:** Monitor for program updates, application deadline changes, new participation guidance, and model document releases

**What to watch for:**
- New PDF documents linked on the page
- Changes to eligibility language
- New FAQ entries or updates
- Deadline announcements

**Monitoring approach:** Periodic fetch + content hash comparison to detect changes. Flag when hash differs from last stored version.

---

### Source 3 — CMS ACCESS Technical FAQ
**URL:** `https://www.cms.gov/priorities/innovation/access-technical-frequently-asked-questions`  
**Type:** Public CMS webpage  
**Use:** Monitor for new technical implementation questions and answers that may affect Phase 3 (technology/reporting setup) or Phase 5 (monitoring/compliance)

---

## Update Classification

When an update is detected, it is classified into one of four categories:

| Category | Description | Plan Impact |
|----------|-------------|-------------|
| **Deadline Change** | New or revised submission, application, or reporting deadline | Phases 1, 4, 5 |
| **Eligibility Update** | Changes to qualifying conditions, organization types, or patient criteria | Phase 1 |
| **Technical Requirement** | New or revised data, reporting, or technology requirements | Phases 2, 3 |
| **Payment/Outcome Change** | Changes to OAP structure, performance thresholds, or measure definitions | Phases 3, 5 |

---

## Impact Mapping

Each update category maps to specific plan sections that may need revision:

| Update Category | Affected Phases | Affected Task Types |
|-----------------|----------------|--------------------|
| Deadline Change | 1, 4, 5 | Application, go-live, reporting tasks |
| Eligibility Update | 1 | Eligibility review, patient population tasks |
| Technical Requirement | 2, 3 | EHR config, vendor selection, data governance tasks |
| Payment/Outcome Change | 3, 5 | Outcome tracking, dashboard, performance review tasks |

---

## User-Facing Update Panel

The "Recent Updates" panel in the app shows:

```
┌─────────────────────────────────────────────────────────┐
│ 📋 RECENT UPDATES                          Last checked │
│                                                         │
│ ⚠️  [Source] Title of update               Date        │
│     Category: Technical Requirement                     │
│     May affect: Phase 3 — Technology & Reporting Setup  │
│     → View source   → See suggested revision            │
│                                              [Dismiss]  │
│                                                         │
│ ✅  No changes detected in last 7 days                  │
└─────────────────────────────────────────────────────────┘
```

---

## Suggested Revision Workflow

When a user clicks "See suggested revision":

1. App displays the detected change and the affected plan section side by side
2. App shows a proposed edit to the task, checkpoint, or risk
3. User can: **Apply revision**, **Edit before applying**, or **Dismiss**
4. Applied revisions are marked with a revision note and timestamp
5. Dismissed updates are logged but do not modify the plan

---

## MVP Implementation Plan

For Phase 3 of the build, update monitoring will be implemented as follows:

| Step | Action | Technology |
|------|--------|------------|
| 1 | Connect to Federal Register API on page load | JavaScript fetch() |
| 2 | Query for CMS ACCESS-related documents published in last 30 days | Federal Register REST API |
| 3 | Display raw results in "Recent Updates" panel | HTML/JS |
| 4 | Manually define impact mapping rules in source-config.json | JSON config file |
| 5 | Match detected document keywords to impact categories | JavaScript rules engine |
| 6 | Surface flagged items with affected phase labels | UI panel |

CMS webpage monitoring (hash comparison) is planned for a post-MVP release due to CORS constraints in a static app environment. A lightweight backend proxy or scheduled GitHub Action may be used in a future build.

---

## Limitations (Version 1)

- Federal Register API only covers formally published rules and notices — informal CMS guidance updates on cms.gov may not appear
- Keyword matching is rule-based and may miss contextual nuances in complex rulemakings
- CMS webpage monitoring requires either a backend proxy or manual refresh trigger in the MVP version
- No notification system (email, push) in Version 1 — updates are visible only on app load
