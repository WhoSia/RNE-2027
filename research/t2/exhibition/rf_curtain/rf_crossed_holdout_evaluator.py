"""RF05: preregistered independent session×placement diagnostic RF trial groups.

This module evaluates TEST splits only. It does not capture CSI, synthesize
radio measurements, or actuate traffic signals. Source: research plan
RF05_CROSSED_HOLDOUT_PREREG_20261121.md. Predictions are made from one
fit on independently reset P1/S1 + P1/S2 trials; no held-out rows
are passed to feature fitting. Pilot labels are not real road causes.
"""
from __future__ import annotations

import json
from collections import Counter

from rf_pilot_evaluator import LABELS, MODELS, validate, vector, fit_predict, summarize

SESSIONS = ("S1", "S2", "S3")
PLACEMENTS = ("P1", "P2")

TRAIN_CELLS = (("S1", "P1"), ("S2", "P1"))
TEST_CELLS = {
    "placement_only": ("S2", "P2"),
    "session_only": ("S3", "P1"),
    "joint": ("S3", "P2"),
}
UNUSED_RESERVE = ("S1", "P2")


def _cell(rows: list[dict], session: str, placement: str) -> list[dict]:
    return [r for r in rows
            if r["session_id"] == session and r["placement_id"] == placement]


def _group_counts(rows: list[dict], name: str) -> dict:
    c = Counter(row["label"] for row in rows)
    if any(c[label] < 10 for label in LABELS):
        raise ValueError(f"RF05 {name}: at least ten independently reset trials "
                         "per each of five labels required")
    return {label: c[label] for label in LABELS}


def evaluate_crossed(rows: list[dict]) -> dict:
    """Evaluate three frozen holdouts without refitting on any of them."""
    validate(rows)
    allowed = set((session, placement)
                  for session in SESSIONS for placement in PLACEMENTS)
    unexpected = {(r["session_id"], r["placement_id"]) for r in rows} - allowed
    if unexpected:
        raise ValueError(f"RF05 unexpected session/placement cells {sorted(unexpected)}")
    full_grid = {(s, p): _cell(rows, s, p) for s, p in allowed}
    for (s, p), group in full_grid.items():
        _group_counts(group, f"{s}/{p}")
    train = [r for s, p in TRAIN_CELLS for r in full_grid[s, p]]
    test = {name: full_grid[sp] for name, sp in TEST_CELLS.items()}
    reserve = full_grid[UNUSED_RESERVE]
    train_ids = {r["trial_id"] for r in train}
    test_ids = {r["trial_id"] for group in test.values() for r in group}
    if train_ids & test_ids:
        raise ValueError("RF05 leakage: train/test same reset trial_id")
    if set(r["trial_id"] for r in reserve) & (train_ids | test_ids):
        raise ValueError("RF05 leakage: reserve reused")

    reports = {}
    for name, group in test.items():
        models = {}
        for model_name, features in MODELS.items():
            predictions, fit = fit_predict(train, group, features)
            models[model_name] = {**summarize(group, predictions), **fit}
        rf_valid = sum(r["quality"] == "ok"
                       and vector(r, MODELS["csi_both"]) is not None
                       for r in group)
        reports[name] = {
            "session_id": TEST_CELLS[name][0],
            "placement_id": TEST_CELLS[name][1],
            "n": len(group),
            "class_counts": _group_counts(group, name),
            "csi_valid_rate": rf_valid / len(group),
            "models": models
        }

    session_quality = {}
    for session in SESSIONS:
        session_rows = [r for r in rows if r["session_id"] == session]
        session_quality[session] = (
            sum(r["quality"] == "ok" for r in session_rows)/len(session_rows))

    primary = reports["joint"]
    csi = primary["models"]["csi_both"]
    rssis = (primary["models"]["rssi_one"]["macro_f1"],
             primary["models"]["rssi_both"]["macro_f1"])
    enough = (
        len(train) >= 100
        and all(g["n"] >= 50 for g in reports.values())
        and all(g["csi_valid_rate"] >= 0.8 for g in reports.values())
        and all(v >= 0.8 for v in session_quality.values())
        and csi["fit_possible"]
    )
    meets = (
        enough
        and csi["macro_f1"] >= 0.70
        and min(csi["per_class"][label]["recall"] for label in LABELS) >= 0.50
        and csi["macro_f1"] - max(rssis) >= 0.10
    )
    origin = rows[0]["trial_origin"]
    if origin == "synthetic_test_fixture":
        gate = "NOT_APPLICABLE_SYNTHETIC_FIXTURE"
        evidence = "SYNTHETIC_PIPELINE_TEST_NOT_RF_EVIDENCE"
    else:
        evidence = "LAB_TRIAL_ANALYSIS_REQUIRES_INDEPENDENT_SOURCE_AUDIT"
        gate = ("INSUFFICIENT_DATA" if not enough else
                "PASS_PROVISIONAL_REQUIRES_SOURCE_AUDIT" if meets else "FAIL")
    return {
        "status": evidence,
        "trial_origin": origin,
        "train_cells": [list(x) for x in TRAIN_CELLS],
        "train_n": len(train),
        "test_cells": {key: list(value) for key, value in TEST_CELLS.items()},
        "test_reports": reports,
        "unused_cell": list(UNUSED_RESERVE),
        "unused_n": len(reserve),
        "session_valid_quality_rate": session_quality,
        "primary_gate": gate,
        "warning": (
            "P2/S2 is a placement shift conditional on P1/S2 in training; "
            "P1/S3 is a new session at familiar placement; P2/S3 combines both. "
            "These are NOT controlled physical causal effects or RF field measurements. "
            "Never tune on diagnostic or primary test cells."
        ),
    }


if __name__ == "__main__":
    import argparse
    from pathlib import Path
    from rf_pilot_evaluator import read_trials
    parser = argparse.ArgumentParser()
    parser.add_argument("trial_csv", type=Path)
    parser.add_argument("output_json", type=Path)
    args = parser.parse_args()
    args.output_json.write_text(
        json.dumps(evaluate_crossed(read_trials(args.trial_csv)),
                   ensure_ascii=False, sort_keys=True, indent=2) + "\n",
        encoding="utf-8")
