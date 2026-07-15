"""
ACCESS Backend API (FastAPI)
============================

HTTP surface for The Policy Nest ACCESS workflow. This is the "backend / core
workflow implementation" required by Project 2. It exposes the deterministic
projection engine (``projection_engine.py``) and the optional AI narrative
layer (``ai_narrative.py``) as clean, validated JSON routes.

Routes
------
  GET  /                 -> service metadata + link map
  GET  /health           -> liveness probe
  GET  /options          -> valid org types, tracks, gaps (drives a future UI)
  POST /projection       -> run the projection for a given input payload
  POST /narrative        -> projection + AI/template executive summary

Run locally:
    uvicorn app:app --reload --port 8000
Interactive docs are auto-generated at http://127.0.0.1:8000/docs
"""

from __future__ import annotations

from typing import Any

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator

import projection_engine as engine
from ai_narrative import generate_narrative

app = FastAPI(
    title="The Policy Nest ACCESS API",
    version="0.2.0",
    description=(
        "Rule-based workflow backend that models enrollment ramp and shared "
        "savings for a VBC entity entering the ACCESS program, with an optional "
        "AI executive-summary layer."
    ),
)


# ---------------------------------------------------------------------------
# Request / response models (input validation + error handling live here)
# ---------------------------------------------------------------------------

VALID_ORGS = set(engine.ORG_PANEL_DEFAULT.keys())
VALID_TRACKS = set(engine.TRACK_LABELS.keys())
VALID_GAPS = set(engine.GAP_LABELS.keys())


class AssumptionOverrides(BaseModel):
    """Optional per-field overrides. Any omitted field uses the computed default."""

    start_panel: int | None = Field(default=None, ge=0)
    steady_panel: int | None = Field(default=None, ge=0)
    ramp_speed: float | None = Field(default=None, gt=0)
    pmpy: float | None = Field(default=None, ge=0)
    gross_savings_rate: float | None = Field(default=None, ge=0, le=100)
    shared_share: float | None = Field(default=None, ge=0, le=100)
    per_ben_cost: float | None = Field(default=None, ge=0)


class ProjectionRequest(BaseModel):
    """Input payload: the same choices a user makes in the app's planner."""

    org_value: str = Field(..., description="Organization type code, e.g. 'aco'.")
    tracks: list[str] = Field(default_factory=list, description="Clinical track codes.")
    gaps: list[str] = Field(default_factory=list, description="Readiness gap codes.")
    assumptions: AssumptionOverrides | None = None

    @field_validator("org_value")
    @classmethod
    def _check_org(cls, v: str) -> str:
        if v not in VALID_ORGS:
            raise ValueError(
                f"Unknown org_value '{v}'. Valid: {sorted(VALID_ORGS)}"
            )
        return v

    @field_validator("tracks")
    @classmethod
    def _check_tracks(cls, v: list[str]) -> list[str]:
        bad = [t for t in v if t not in VALID_TRACKS]
        if bad:
            raise ValueError(
                f"Unknown track(s) {bad}. Valid: {sorted(VALID_TRACKS)}"
            )
        return v

    @field_validator("gaps")
    @classmethod
    def _check_gaps(cls, v: list[str]) -> list[str]:
        bad = [g for g in v if g not in VALID_GAPS]
        if bad:
            raise ValueError(
                f"Unknown gap(s) {bad}. Valid: {sorted(VALID_GAPS)}"
            )
        return v


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.get("/")
def root() -> dict[str, Any]:
    return {
        "service": "The Policy Nest ACCESS API",
        "version": app.version,
        "docs": "/docs",
        "routes": {
            "GET /health": "liveness probe",
            "GET /options": "valid org types, tracks, and gaps",
            "POST /projection": "run the rule-based projection",
            "POST /narrative": "projection + AI/template executive summary",
        },
    }


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/options")
def options() -> dict[str, Any]:
    """Expose the valid input choices (drives a future dropdown / chip UI)."""
    return {
        "org_types": engine.ORG_LABELS,
        "tracks": engine.TRACK_LABELS,
        "gaps": engine.GAP_LABELS,
        "horizon_years": engine.PROJ_YEARS,
        "start_year": engine.PROJ_START_YEAR,
    }


@app.post("/projection")
def projection(req: ProjectionRequest) -> dict[str, Any]:
    """Run the deterministic projection for the given inputs.

    Pydantic has already validated the input; any modeling failure surfaces as
    a clean HTTP 422 rather than a stack trace.
    """
    try:
        overrides = req.assumptions.model_dump(exclude_none=True) if req.assumptions else None
        return engine.run_projection(
            org_value=req.org_value,
            tracks=req.tracks,
            gaps=req.gaps,
            overrides=overrides,
        )
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=422, detail=f"Projection failed: {exc}") from exc


@app.post("/narrative")
def narrative(req: ProjectionRequest) -> dict[str, Any]:
    """Projection plus an executive summary (AI if configured, else template)."""
    try:
        overrides = req.assumptions.model_dump(exclude_none=True) if req.assumptions else None
        payload = engine.run_projection(
            org_value=req.org_value,
            tracks=req.tracks,
            gaps=req.gaps,
            overrides=overrides,
        )
        payload["narrative"] = generate_narrative(payload)
        return payload
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=422, detail=f"Narrative failed: {exc}") from exc
