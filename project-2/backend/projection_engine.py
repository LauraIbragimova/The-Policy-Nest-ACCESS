"""
ACCESS Projection Engine
=========================

Core rule-based workflow logic for The Policy Nest ACCESS tool.

This module is a 1:1 Python port of the deterministic projection model that
runs client-side in the ACCESS Rollout web app (``ACCESS Rollout.html``). It
models, for an aligned value-based care (VBC) entity entering the ACCESS
program, how its aligned-beneficiary panel ramps up over the performance-year
horizon and how gross savings, program cost, net savings, and the entity's
shared-savings share evolve year over year.

Nothing here is AI. It is transparent, auditable, rule-based arithmetic — the
same math a reviewer can reproduce by hand. (An *optional* AI narrative layer
lives separately in ``ai_narrative.py`` and never touches these numbers.)

Keeping this logic in a standalone, importable module means the FastAPI routes,
the test suite, and the demo script all exercise the exact same code path.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field, asdict
from typing import Any


# ---------------------------------------------------------------------------
# Reference data (mirrors the option values baked into the web app)
# ---------------------------------------------------------------------------

#: Default starting panel (eligible aligned beneficiaries at go-live) by
#: organization type. Rough planning defaults; every value is editable via the
#: ``assumptions`` override.
ORG_PANEL_DEFAULT: dict[str, int] = {
    "aco": 6000,
    "fqhc": 2500,
    "rhc": 1200,
    "independent": 1500,
    "health-system": 9000,
    "oncology-center": 1800,
    "digital": 4000,
}

#: Human-readable organization-type labels (for API responses / narratives).
ORG_LABELS: dict[str, str] = {
    "aco": "ACO / MSSP Participant",
    "fqhc": "FQHC / Community Health Center",
    "rhc": "Rural Health Clinic (RHC)",
    "independent": "Independent Practice / Group Practice",
    "health-system": "Health System / Hospital",
    "oncology-center": "Oncology Practice / Cancer Center",
    "digital": "Digital Health / Tech-Enabled Provider",
}

#: Valid clinical-track codes and their labels.
TRACK_LABELS: dict[str, str] = {
    "eckm": "eCKM - Early cardio-kidney-metabolic",
    "ckm": "CKM - Diabetes, CKD, ASCVD",
    "msk": "MSK - Chronic musculoskeletal pain",
    "bh": "BH - Depression or anxiety",
    "onc": "Oncology - Active cancer treatment & survivorship",
}

#: Valid readiness-gap codes and their labels.
GAP_LABELS: dict[str, str] = {
    "data": "Data & Analytics",
    "workforce": "Workforce",
    "interop": "Interoperability",
    "finance": "Finance / P&L",
    "governance": "Governance",
}

#: Projection horizon. ACCESS runs an aligned entity for up to ~6 performance
#: years inside the 2026-2036 model window.
PROJ_YEARS: int = 6
PROJ_START_YEAR: int = 2026


# ---------------------------------------------------------------------------
# Assumptions
# ---------------------------------------------------------------------------

@dataclass
class Assumptions:
    """Editable projection assumptions.

    These mirror the seven inputs surfaced in the app's Projections tab. Field
    defaults are filled by :func:`projection_defaults`; individual fields can be
    overridden by the user via the API ``assumptions`` object.
    """

    start_panel: int          # aligned beneficiaries in performance year 1
    steady_panel: int         # steady-state enrollment ceiling
    ramp_speed: float = 0.9   # logistic growth rate (0.4 slow - 1.6 fast)
    pmpy: float = 13000       # baseline total cost per beneficiary / yr ($)
    gross_savings_rate: float = 8   # % gross reduction vs. baseline at maturity
    shared_share: float = 50  # % of net savings kept by the entity
    per_ben_cost: float = 550  # program cost per aligned beneficiary / yr ($)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def projection_defaults(org_value: str, tracks: list[str]) -> Assumptions:
    """Compute the default assumptions for an org type + clinical tracks.

    Mirrors ``projectionDefaults(orgValue, tracks, gaps)`` in the web app.
    Each additional clinical track widens the eligible panel by ~18%.
    """
    base = ORG_PANEL_DEFAULT.get(org_value, 2000)
    track_factor = 1 + max(0, (len(tracks) - 1)) * 0.18
    start_panel = round(base * track_factor)
    return Assumptions(
        start_panel=start_panel,
        steady_panel=round(start_panel * 2.4),
        ramp_speed=0.9,
        pmpy=13000,
        gross_savings_rate=8,
        shared_share=50,
        per_ben_cost=550,
    )


def current_assumptions(
    org_value: str,
    tracks: list[str],
    overrides: dict[str, Any] | None = None,
) -> Assumptions:
    """Merge user overrides on top of computed defaults (user edits win).

    Mirrors ``currentProjAssumptions`` + the persisted-override merge in the app.
    ``overrides`` keys use the snake_case field names of :class:`Assumptions`.
    """
    a = projection_defaults(org_value, tracks)
    if overrides:
        for key, val in overrides.items():
            if val is None:
                continue
            if hasattr(a, key):
                setattr(a, key, val)
    return a


# ---------------------------------------------------------------------------
# Core projection math
# ---------------------------------------------------------------------------

@dataclass
class ProjectionRow:
    """One performance year of the projection."""

    year: int
    py: int
    enrolled: int
    gross_savings: float
    program_cost: float
    net_savings: float
    shared: float

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class ProjectionResult:
    """Full projection: per-year rows plus roll-up totals."""

    rows: list[ProjectionRow] = field(default_factory=list)
    cum_savings: float = 0.0
    cum_shared: float = 0.0
    peak_enrolled: int = 0

    def to_dict(self) -> dict[str, Any]:
        return {
            "rows": [r.to_dict() for r in self.rows],
            "cum_savings": self.cum_savings,
            "cum_shared": self.cum_shared,
            "peak_enrolled": self.peak_enrolled,
        }


def compute_projection(a: Assumptions, gaps: list[str] | None = None) -> ProjectionResult:
    """Run the deterministic projection.

    1:1 port of ``computeProjection(a, gaps)`` from the web app.

    Workflow, per performance year (1..PROJ_YEARS):
      * Enrollment follows a logistic S-curve from ``start_panel`` toward
        ``steady_panel``, normalized so year 1 starts at ``start_panel``.
      * The gross-savings rate matures linearly to full capability by ~year 4
        and is dragged down by each unresolved readiness gap (up to 30%).
      * gross_savings = enrolled x pmpy x effective_rate
      * program_cost  = enrolled x per_ben_cost
      * net_savings   = gross_savings - program_cost  (negative early = ramp loss)
      * shared        = max(0, net_savings) x shared_share%
    """
    gap_count = len(gaps) if gaps else 0
    # Gap drag: each unresolved readiness gap slows capability maturity, capped at 30%.
    gap_drag = min(gap_count * 0.06, 0.30)

    rows: list[ProjectionRow] = []
    cum_savings = 0.0
    cum_shared = 0.0

    for y in range(1, PROJ_YEARS + 1):
        # Logistic S-curve enrollment between start_panel and steady_panel.
        L = a.steady_panel
        k = a.ramp_speed
        x0 = 2.2
        logistic = 1 / (1 + math.exp(-k * (y - x0)))
        logistic1 = 1 / (1 + math.exp(-k * (1 - x0)))
        # Normalize so year 1 begins at start_panel and matures toward steady_panel.
        frac = (logistic - logistic1) / (1 - logistic1)
        enrolled = round(a.start_panel + (L - a.start_panel) * max(0.0, frac))

        # Savings rate matures over time and is dragged by open gaps.
        maturity = min(y / 4, 1)  # full capability by ~yr4
        eff_rate = (a.gross_savings_rate / 100) * maturity * (1 - gap_drag)

        gross_savings = enrolled * a.pmpy * eff_rate
        program_cost = enrolled * a.per_ben_cost
        net_savings = gross_savings - program_cost
        shared = max(0.0, net_savings) * (a.shared_share / 100)

        cum_savings += net_savings
        cum_shared += shared

        rows.append(
            ProjectionRow(
                year=PROJ_START_YEAR + y - 1,
                py=y,
                enrolled=enrolled,
                gross_savings=gross_savings,
                program_cost=program_cost,
                net_savings=net_savings,
                shared=shared,
            )
        )

    return ProjectionResult(
        rows=rows,
        cum_savings=cum_savings,
        cum_shared=cum_shared,
        peak_enrolled=rows[-1].enrolled if rows else 0,
    )


# ---------------------------------------------------------------------------
# Formatting helpers (mirror fmtUSD / fmtNum in the app)
# ---------------------------------------------------------------------------

def fmt_usd(n: float) -> str:
    """Format a dollar amount as $X.XXM / $XK / $X, handling negatives."""
    v = round(n)
    sign = "-$" if v < 0 else "$"
    av = abs(v)
    if av >= 1_000_000:
        return f"{sign}{av / 1_000_000:.2f}M"
    if av >= 1_000:
        return f"{sign}{round(av / 1_000)}K"
    return f"{sign}{av}"


def fmt_num(n: float) -> str:
    """Format an integer with thousands separators."""
    return f"{round(n):,}"


# ---------------------------------------------------------------------------
# High-level orchestration used by the API / demo
# ---------------------------------------------------------------------------

def run_projection(
    org_value: str,
    tracks: list[str],
    gaps: list[str] | None = None,
    overrides: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """End-to-end: validate-ready inputs -> assumptions -> projection -> dict.

    Returns a JSON-serializable dict including the resolved assumptions, the
    per-year rows, totals, and echoed human-readable labels.
    """
    gaps = gaps or []
    a = current_assumptions(org_value, tracks, overrides)
    result = compute_projection(a, gaps)
    return {
        "org_value": org_value,
        "org_label": ORG_LABELS.get(org_value, org_value),
        "tracks": tracks,
        "track_labels": [TRACK_LABELS.get(t, t) for t in tracks],
        "gaps": gaps,
        "gap_labels": [GAP_LABELS.get(g, g) for g in gaps],
        "assumptions": a.to_dict(),
        "projection": result.to_dict(),
    }
