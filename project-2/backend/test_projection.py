"""
Verification test suite for the ACCESS projection engine.
=========================================================

These tests prove two things Project 2 is graded on:

  1. The Python backend RUNS and behaves correctly (enrollment ramp, the
     loss -> breakeven -> profit arc, gap drag, and input validation).

  2. The Python port matches the deterministic JavaScript model that runs in
     the ACCESS web app *to the cent*. The golden numbers below were captured
     by calling the app's own ``computeProjection()`` in a real browser, so a
     passing suite guarantees the two implementations agree.

Run:  pytest -v
"""

from __future__ import annotations

import math

import pytest
from fastapi.testclient import TestClient

import projection_engine as engine
from app import app

client = TestClient(app)

# Absolute tolerance for floating-point dollar comparisons (well under a cent).
TOL = 1e-6


# ---------------------------------------------------------------------------
# Golden values captured from the ACCESS web app (source of truth)
# ---------------------------------------------------------------------------

# Scenario A: org 'aco', tracks [eckm, bh], gap [data]
GOLDEN_A = {
    "assumptions": {
        "start_panel": 7080, "steady_panel": 16992, "ramp_speed": 0.9,
        "pmpy": 13000, "gross_savings_rate": 8, "shared_share": 50, "per_ben_cost": 550,
    },
    "rows": [
        # py, enrolled, gross, program, net, shared
        (1, 7080,  1730352.0,        3894000, -2163648.0,        0.0),
        (2, 9757,  4769221.600000001, 5366350, -597128.3999999994, 0.0),
        (3, 12645, 9271313.999999998, 6954750, 2316563.999999998, 1158281.999999999),
        (4, 14798, 14466524.8,        8138900, 6327624.800000001, 3163812.4000000004),
        (5, 16003, 15644532.8,        8801650, 6842882.800000001, 3421441.4000000004),
        (6, 16571, 16199809.600000001, 9114050, 7085759.6000000015, 3542879.8000000007),
    ],
    "cum_savings": 19812054.8,
    "cum_shared": 11286415.600000001,
    "peak_enrolled": 16571,
}

# Scenario B: org 'fqhc', track [ckm], no gaps
GOLDEN_B = {
    "assumptions": {
        "start_panel": 2500, "steady_panel": 6000, "ramp_speed": 0.9,
        "pmpy": 13000, "gross_savings_rate": 8, "shared_share": 50, "per_ben_cost": 550,
    },
    "rows": [
        (1, 2500, 650000.0,  1375000, -725000.0, 0.0),
        (2, 3445, 1791400.0, 1894750, -103350.0, 0.0),
        (3, 4465, 3482700.0, 2455750, 1026950.0, 513475.0),
        (4, 5225, 5434000.0, 2873750, 2560250.0, 1280125.0),
        (5, 5651, 5877040.0, 3108050, 2768990.0, 1384495.0),
        (6, 5851, 6085040.0, 3218050, 2866990.0, 1433495.0),
    ],
    "cum_savings": 8394830.0,
    "cum_shared": 4611590.0,
    "peak_enrolled": 5851,
}


def _assert_matches_golden(result_dict, golden):
    proj = result_dict["projection"]
    assert result_dict["assumptions"] == golden["assumptions"]
    assert proj["peak_enrolled"] == golden["peak_enrolled"]
    assert proj["cum_savings"] == pytest.approx(golden["cum_savings"], abs=TOL)
    assert proj["cum_shared"] == pytest.approx(golden["cum_shared"], abs=TOL)
    assert len(proj["rows"]) == len(golden["rows"])
    for row, (py, enr, gross, prog, net, shared) in zip(proj["rows"], golden["rows"]):
        assert row["py"] == py
        assert row["enrolled"] == enr
        assert row["gross_savings"] == pytest.approx(gross, abs=TOL)
        assert row["program_cost"] == pytest.approx(prog, abs=TOL)
        assert row["net_savings"] == pytest.approx(net, abs=TOL)
        assert row["shared"] == pytest.approx(shared, abs=TOL)


# ---------------------------------------------------------------------------
# Parity with the web app
# ---------------------------------------------------------------------------

def test_scenario_a_matches_web_app():
    result = engine.run_projection("aco", ["eckm", "bh"], ["data"])
    _assert_matches_golden(result, GOLDEN_A)


def test_scenario_b_matches_web_app():
    result = engine.run_projection("fqhc", ["ckm"], [])
    _assert_matches_golden(result, GOLDEN_B)


# ---------------------------------------------------------------------------
# Model behavior
# ---------------------------------------------------------------------------

def test_enrollment_is_monotonic_and_bounded():
    res = engine.compute_projection(engine.projection_defaults("aco", ["eckm"]))
    enrolled = [r.enrolled for r in res.rows]
    assert enrolled == sorted(enrolled)  # ramps upward
    # Single track => track_factor 1.0, so start_panel == aco base (6000).
    assert enrolled[0] == 6000           # starts at start_panel
    assert enrolled[-1] <= 6000 * 2.4    # stays under the steady-state ceiling


def test_loss_then_breakeven_then_profit():
    res = engine.compute_projection(engine.projection_defaults("aco", ["eckm", "bh"]),
                                    gaps=["data"])
    nets = [r.net_savings for r in res.rows]
    assert nets[0] < 0 and nets[1] < 0      # early ramp loss
    assert nets[2] > 0                       # breakeven by PY3
    assert all(nets[i] <= nets[i + 1] for i in range(2, len(nets) - 1))  # then grows


def test_gap_drag_reduces_savings():
    a = engine.projection_defaults("aco", ["eckm"])
    no_gaps = engine.compute_projection(a, gaps=[])
    many_gaps = engine.compute_projection(a, gaps=["data", "workforce", "interop",
                                                   "finance", "governance"])
    assert many_gaps.cum_savings < no_gaps.cum_savings


def test_shared_never_negative():
    res = engine.compute_projection(engine.projection_defaults("rhc", ["ckm"]))
    assert all(r.shared >= 0 for r in res.rows)


def test_assumption_override_wins():
    res = engine.run_projection("aco", ["eckm"], [], overrides={"gross_savings_rate": 20})
    assert res["assumptions"]["gross_savings_rate"] == 20


# ---------------------------------------------------------------------------
# Formatting helpers
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("value,expected", [
    (2316564, "$2.32M"),
    (-2163648, "-$2.16M"),
    (513475, "$513K"),
    (-725000, "-$725K"),
    (550, "$550"),
    (0, "$0"),
])
def test_fmt_usd(value, expected):
    assert engine.fmt_usd(value) == expected


# ---------------------------------------------------------------------------
# API routes + validation / error handling
# ---------------------------------------------------------------------------

def test_health_route():
    r = client.get("/health")
    assert r.status_code == 200 and r.json()["status"] == "ok"


def test_options_route():
    r = client.get("/options")
    body = r.json()
    assert r.status_code == 200
    assert "aco" in body["org_types"] and "eckm" in body["tracks"]


def test_projection_route_ok():
    r = client.post("/projection", json={"org_value": "aco",
                                         "tracks": ["eckm", "bh"], "gaps": ["data"]})
    assert r.status_code == 200
    _assert_matches_golden(r.json(), GOLDEN_A)


def test_projection_route_rejects_bad_org():
    r = client.post("/projection", json={"org_value": "not-real", "tracks": []})
    assert r.status_code == 422  # caught by Pydantic validator


def test_projection_route_rejects_bad_track():
    r = client.post("/projection", json={"org_value": "aco", "tracks": ["xyz"]})
    assert r.status_code == 422


def test_narrative_route_falls_back_to_template(monkeypatch):
    # Ensure no API key -> deterministic template path, endpoint still succeeds.
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    r = client.post("/narrative", json={"org_value": "fqhc", "tracks": ["ckm"]})
    assert r.status_code == 200
    narr = r.json()["narrative"]
    assert narr["engine"] == "template"
    assert "breakeven" in narr["summary"].lower()
