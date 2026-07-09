# ACCESS Rollout Planner — MVP Scope & Product Blueprint

**Product:** ACCESS Rollout Planner  
**Version:** 1.0 MVP  
**Owner:** The Policy Nest  
**Last Updated:** July 2026  

---

## Objective

Build a single-page web application that converts a CMS ACCESS Model participant's profile into a structured, phase-by-phase implementation roadmap — including a risk registry, regulatory checkpoint log, KPI tracker, quality tracker, and work breakdown structure — aligned to actual CMS ACCESS requirements.

---

## Primary User

A value-based care operations director or program manager at an ACO, FQHC, health system, or physician group that has been selected for or is preparing to participate in the CMS ACCESS Model. They understand the program at a high level but need an executable operational plan.

---

## User Flow

1. User lands on the planner and sees an intake form on the left panel
2. User selects organization type, condition track(s), implementation phase, and readiness gap flags
3. User clicks "Generate My Rollout Plan"
4. The right panel populates with a full plan including:
   - Phase accordion with tasks, checkpoints, and risks
   - KPI tracker panel
   - Quality tracker panel
   - Regulatory checkpoint log
   - Live Federal Register updates
5. User can check off completed tasks and watch the progress bar update
6. User exports or prints the plan

---

## Input Fields

| Field | Type | Options |
|-------|------|---------|
| Organization Type | Dropdown | ACO, FQHC, Health System, Physician Group, Rural Health Clinic |
| Condition Track | Multi-select checkbox | CKM (Cardiometabolic), MSK (Musculoskeletal), BH (Behavioral Health), Oncology |
| Implementation Phase | Radio with badges | Phase 1: Readiness, Phase 2: Alignment, Phase 3: Care Delivery, Phase 4: Reporting, Phase 5: Reconciliation |
| Readiness Gap Flags | Multi-select checkbox | HIE/EHR Integration, Billing & Coding, Staff Training, Device Procurement, Beneficiary Engagement |

---

## Output Definitions

| Output | Description |
|--------|-------------|
| Phase Accordion | 5 collapsible phases, each with tasks (checkbox), checkpoints (Azure), and risks (warning badge) |
| Progress Bar | Live % of tasks checked off across all phases |
| KPI Tracker | OAT Rate, 425-Day Deadline Compliance, Alignment Volume, Withheld Payment Recovery Rate, Co-Management Billing Activation |
| Quality Tracker | Measure Submission Compliance, Baseline Capture Rate, Care Update Transmission Rate |
| Regulatory Checkpoint Log | 12 named checkpoints with status toggle (Not Started / In Progress / Complete) |
| Risk Registry | 15 risks with likelihood, impact, mitigation owner; gap-flagged risks surface first |
| FR Updates Panel | Live Federal Register API call for recent CMS ACCESS rulemaking |
| Export | Copy as text, Print/Save PDF |

---

## Work Breakdown Structure

### Phase 1 — Readiness (Weeks 1–8)
- [ ] Designate Physician Clinical Director (required by CMS)
- [ ] Complete PECOS enrollment verification for all billing practitioners
- [ ] Execute HIPAA Business Associate Agreements with all vendors
- [ ] Conduct FDA device classification review for all digital health tools (TEMPO pilot decision)
- [ ] Document AKS/Stark Law structuring review with legal counsel
- [ ] Select and contract HIE or CMS Aligned Network for care plan transmission
- [ ] Define beneficiary cost-sharing election (collect or waive 20%) — uniform policy required
- [ ] Establish EHR workflow for ACCESS G-code billing activation
- [ ] Configure FFS exclusion audit to prevent duplicate billing on aligned beneficiaries
- [ ] Develop staff training curriculum (clinical, billing, operations)
- [ ] Define device procurement and BYOD consent workflow

### Phase 2 — Alignment (Weeks 9–16)
- [ ] Submit application or confirm CMS selection confirmation documents
- [ ] Activate co-management G-code notifications to PCPs and referring clinicians
- [ ] Build beneficiary identification and outreach workflow
- [ ] Configure beneficiary alignment tracking in EHR/registry
- [ ] Establish control group management process (CMS randomization ~5% of aligned beneficiaries)
- [ ] Implement geographic flagging for rural add-on payment capture (CKM track)
- [ ] Build multi-track discount modeling into financial projections
- [ ] Train front-desk and care coordination staff on enrollment scripts
- [ ] Launch beneficiary consent and engagement workflow
- [ ] Activate HIE care plan transmission to PCPs at enrollment trigger

### Phase 3 — Care Delivery (Weeks 17–36)
- [ ] Launch care delivery operations across selected tracks
- [ ] Submit baseline measures within 60 days of each beneficiary alignment
- [ ] Activate quarterly outcome data collection workflow
- [ ] Monitor OAT rate (target: ≥50% of aligned beneficiaries meeting all outcome targets)
- [ ] Escalate if OAT rate trends below 45% mid-period
- [ ] Monitor substitute spend utilization against CMS thresholds
- [ ] Transmit standardized care plan updates to PCP at treatment initiation, milestones, and completion
- [ ] Track co-management G-code billing activation rate by PCP
- [ ] Conduct mid-period billing audit (FFS exclusion compliance check)
- [ ] Report any adverse events or program integrity concerns to CMS within required window

### Phase 4 — Reporting (Weeks 37–52 / Day 1–425 Post-Alignment)
- [ ] Submit quarterly outcome data on schedule
- [ ] Confirm all 425-day final outcome submissions are calendared per beneficiary cohort
- [ ] Conduct pre-submission quality review for each measure set
- [ ] Validate care update transmission logs for HIE completeness
- [ ] Prepare performance narrative for CMS program team (if required by track)
- [ ] Audit PECOS and billing records for accuracy before final submission
- [ ] Escalate any missed 425-day deadlines immediately to Compliance Officer

### Phase 5 — Reconciliation (Post-Day 425)
- [ ] Receive CMS reconciliation report
- [ ] Review OAT attainment rate against 50% threshold
- [ ] Confirm release or forfeiture of withheld 50% payment
- [ ] Reconcile substitute spend adjustments
- [ ] Prepare financial variance report (projected vs. actual ACCESS revenue)
- [ ] Conduct lessons learned review with clinical, operations, and billing teams
- [ ] Update roadmap for next performance period

---

## Regulatory Checkpoint Log

| # | Checkpoint | Regulatory Basis | Phase | Status |
|---|-----------|-----------------|-------|--------|
| 1 | Physician Clinical Director Designated | ACCESS RFA Section 4.2 | 1 | — |
| 2 | PECOS Enrollment Verified (All Practitioners) | ACCESS FAQ — Billing Eligibility | 1 | — |
| 3 | HIPAA BAAs Executed (All Vendors) | 45 CFR § 164.502 | 1 | — |
| 4 | FDA Device Classification Review Complete | ACCESS FAQ — TEMPO Pilot | 1 | — |
| 5 | AKS/Stark Law Structuring Review | 42 USC § 1320a-7b(b) | 1 | — |
| 6 | Cost-Sharing Election Documented (Uniform) | ACCESS RFA — Beneficiary Policy | 1 | — |
| 7 | FFS Exclusion Audit Activated | ACCESS FAQ — Billing Rules | 2 | — |
| 8 | HIE/Aligned Network Contract Executed | ACCESS FAQ — Care Coordination | 1 | — |
| 9 | Control Group Management Process Active | ACCESS FAQ — Randomization | 2 | — |
| 10 | Baseline Measures Submitted (60-Day Window) | ACCESS Payment Guidance | 3 | — |
| 11 | 425-Day Deadline Calendar Confirmed | ACCESS Payment Guidance | 4 | — |
| 12 | Pre-Reconciliation Billing Audit Complete | ACCESS Payment Guidance | 5 | — |

---

## Risk Registry

| # | Risk | Likelihood | Impact | Mitigation | Gap Flag |
|---|------|-----------|--------|-----------|----------|
| 1 | OAT rate falls below 50% threshold at reconciliation | High | Critical | Weekly OAT monitoring dashboard; escalation at <45% | ⚠ Yes |
| 2 | 425-day reporting deadline missed for any beneficiary cohort | Medium | Critical | Per-beneficiary deadline calendar; automated alerts at 30/60/90 days out | ⚠ Yes |
| 3 | FFS duplicate billing on aligned beneficiary | Medium | High | Pre-claim audit rule in billing system; monthly compliance review | ⚠ Yes |
| 4 | HIE transmission failure at care plan milestones | Medium | High | Transmission log monitoring; fallback fax/secure message protocol | ⚠ Yes |
| 5 | PECOS enrollment lapse for billing practitioner | Low | High | Quarterly PECOS audit; enrollment renewal calendar | ⚠ Yes |
| 6 | FDA clearance required for deployed digital health tool | Medium | High | Pre-deployment device classification review; TEMPO pilot enrollment if applicable | ⚠ Yes |
| 7 | AKS/Stark violation in vendor or co-management arrangement | Low | Critical | Legal review before any arrangement; document safe harbor basis | ⚠ Yes |
| 8 | Substitute spend threshold exceeded (payment reduction) | Medium | Medium | Monthly utilization monitoring against CMS thresholds; care manager alert | ⚠ Yes |
| 9 | Control group beneficiary confusion in care team | Low | Medium | Control group flag in EHR; staff training on notification script | ⚠ Yes |
| 10 | Rural add-on payment not captured for CKM beneficiaries | Medium | Medium | Geographic flag at alignment; billing team audit | ⚠ Yes |
| 11 | Multi-track discount not modeled (revenue projection error) | Medium | Medium | Update financial model before alignment; CFO sign-off | ⚠ Yes |
| 12 | Cost-sharing election applied inconsistently across beneficiaries | Low | High | Uniform policy documentation; billing audit at 30 days | ⚠ Yes |
| 13 | Baseline measure submission missed within 60-day window | Medium | High | 60-day deadline trigger at each alignment event; clinical ops owner assigned | No |
| 14 | Staff turnover disrupts care delivery continuity | Medium | Medium | Cross-training protocol; role backup assignments documented | No |
| 15 | CMS system changes delay G-code activation (2026–2027 transition) | High | Medium | Monitor CMS operational updates; contingency billing workflow | No |

---

## KPI Tracker

| KPI | Target | Measurement Frequency | Owner |
|-----|--------|----------------------|-------|
| Outcome Attainment Threshold (OAT) Rate | ≥50% of aligned beneficiaries | Weekly (mid-period), Monthly | Clinical Director |
| 425-Day Deadline Compliance Rate | 100% | Per cohort | Compliance Officer |
| Beneficiary Alignment Volume | Per track capacity plan | Monthly | Operations Director |
| Withheld Payment Recovery Rate | ≥90% of withheld amount | Per reconciliation period | CFO |
| Co-Management G-Code Billing Activation Rate | ≥60% of eligible PCPs | Monthly | Billing Manager |

---

## Quality Tracker

| Measure | Target | Frequency | Owner |
|---------|--------|-----------|-------|
| Baseline Measure Submission Compliance (60-day) | 100% | Per alignment event | Clinical Ops |
| Quarterly Outcome Data Submission Rate | 100% on schedule | Quarterly | Reporting Manager |
| Care Plan Transmission Rate to PCP via HIE | ≥95% at each milestone | Monthly | Care Coordination Lead |
| Beneficiary Consent Documentation Rate | 100% | Ongoing | Front Desk / Enrollment |
| FFS Exclusion Audit Pass Rate | 100% | Monthly | Billing Compliance |

---

## MVP Limits (v1 Will NOT Include)

- EHR integration or live patient data
- Actual CMS API connectivity (Federal Register API only)
- PHI or any individually identifiable health data
- Multi-user accounts or authentication
- Saved plans (no database — browser session only)
- Clinical decision support or AI clinical recommendations

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend | HTML5, CSS3 (custom design tokens), vanilla JavaScript |
| Fonts | Fontshare (Satoshi body, Cabinet Grotesk display) |
| Icons | Lucide Icons (CDN) |
| Charts | Chart.js (CDN) |
| API | Federal Register API (federalregister.gov) |
| Export | Browser Print API + JS clipboard |
| Hosting | GitHub Pages |

---

## Success Criteria

- A first-time user can generate a complete rollout plan in under 3 minutes
- All 12 regulatory checkpoints are surfaced in the correct phase
- All 15 risks appear in the registry, with gap-flagged risks at the top
- KPI and Quality trackers update visually as tasks are checked off
- The app loads and runs fully on mobile at 375px
- No PHI is collected, stored, or transmitted

---

*The Policy Nest — ACCESS Implementation Series*  
*Not legal or clinical advice. Always verify against current CMS guidance.*
