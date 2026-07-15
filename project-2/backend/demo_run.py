"""
Demo run for the ACCESS workflow backend.
=========================================

Runs the full pipeline end-to-end WITHOUT needing a running server, prints a
readable projection table plus the executive-summary narrative, and writes the
raw JSON to ``sample_output.json`` for the Project 2 verification artifact.

Usage:
    python demo_run.py                # default scenario (ACO)
    python demo_run.py --scenario fqhc

This is the "sample input -> sample output" verification the assignment asks for.
"""

from __future__ import annotations

import argparse
import json
import sys

import projection_engine as engine
from ai_narrative import generate_narrative


SCENARIOS = {
    "aco": {
        "org_value": "aco",
        "tracks": ["eckm", "bh"],
        "gaps": ["data"],
        "overrides": None,
    },
    "fqhc": {
        "org_value": "fqhc",
        "tracks": ["ckm"],
        "gaps": [],
        "overrides": None,
    },
}


def print_table(payload: dict) -> None:
    a = payload["assumptions"]
    rows = payload["projection"]["rows"]

    print("=" * 78)
    print("  THE POLICY NEST — ACCESS PROJECTION (demo run)")
    print("=" * 78)
    print(f"  Organization : {payload['org_label']}")
    print(f"  Tracks       : {', '.join(payload['track_labels']) or '(none)'}")
    print(f"  Readiness gaps: {', '.join(payload['gap_labels']) or '(none)'}")
    print("-" * 78)
    print("  Assumptions (resolved):")
    print(f"    start panel {a['start_panel']:>7,}   steady panel {a['steady_panel']:>7,}"
          f"   ramp {a['ramp_speed']}")
    print(f"    PMPY ${a['pmpy']:,}   gross savings {a['gross_savings_rate']}%"
          f"   shared share {a['shared_share']}%   program cost/ben ${a['per_ben_cost']}")
    print("-" * 78)

    header = f"  {'PY':>3} {'Year':>5} {'Enrolled':>10} {'Gross':>12} {'Program':>12} {'Net':>12} {'Share':>12}"
    print(header)
    print("  " + "-" * (len(header) - 2))
    for r in rows:
        print(f"  {r['py']:>3} {r['year']:>5} {engine.fmt_num(r['enrolled']):>10} "
              f"{engine.fmt_usd(r['gross_savings']):>12} {engine.fmt_usd(r['program_cost']):>12} "
              f"{engine.fmt_usd(r['net_savings']):>12} {engine.fmt_usd(r['shared']):>12}")

    proj = payload["projection"]
    print("  " + "-" * (len(header) - 2))
    print(f"  Peak aligned panel      : {engine.fmt_num(proj['peak_enrolled'])}")
    print(f"  Cumulative net savings  : {engine.fmt_usd(proj['cum_savings'])}")
    print(f"  Cumulative entity share : {engine.fmt_usd(proj['cum_shared'])}")
    print("=" * 78)


def main() -> int:
    parser = argparse.ArgumentParser(description="ACCESS projection demo run.")
    parser.add_argument("--scenario", choices=sorted(SCENARIOS), default="aco")
    args = parser.parse_args()

    cfg = SCENARIOS[args.scenario]
    payload = engine.run_projection(
        org_value=cfg["org_value"],
        tracks=cfg["tracks"],
        gaps=cfg["gaps"],
        overrides=cfg["overrides"],
    )
    payload["narrative"] = generate_narrative(payload)

    print_table(payload)
    print()
    print("  EXECUTIVE SUMMARY"
          f"  (engine: {payload['narrative']['engine']})")
    print("  " + "-" * 74)
    # wrap the narrative to ~74 cols for the terminal
    words = payload["narrative"]["summary"].split()
    line = "  "
    for w in words:
        if len(line) + len(w) + 1 > 76:
            print(line)
            line = "  "
        line += w + " "
    print(line.rstrip())
    if payload["narrative"].get("note"):
        print(f"\n  [{payload['narrative']['note']}]")

    with open("sample_output.json", "w") as f:
        json.dump(payload, f, indent=2)
    print("\n  Raw JSON written to sample_output.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
