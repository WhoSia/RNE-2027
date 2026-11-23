"""P89: startup lost-green sensitivity at fixed 50% displayed downstream green.

The lost-second mask starts at EVERY downstream green onset, not at the
upstream decision only. It is additional to the model's receiver headway.
Run from this directory: python p89_startup_loss.py > P89_RESULT.json
"""
from collections import Counter
from dataclasses import replace
from itertools import product
import json
from pathlib import Path
from unittest.mock import patch

from receiving_cells_v15 import ReceivingCells
from p85_signal_coordination import build_config, p31, phases, run, score

HERE = Path(__file__).resolve().parent
START = 84
LOSSES = (0, 1, 2, 3)
PERIODS = (30, 60)


def clock_state(t, period, onset, lost):
    phase = (t - START) % period
    first = 0 if onset == "green" else period // 2
    displayed = (phase < period // 2) if onset == "green" else (phase >= period // 2)
    effective = displayed and (phase - first >= lost)
    return displayed, effective


def exposure(period, onset, lost, stop):
    displayed = effective = 0
    transitions = 0
    for t in range(START, stop):
        d, e = clock_state(t, period, onset, lost)
        displayed += d
        effective += e
        if d and (t == START or not clock_state(t-1, period, onset, lost)[0]):
            transitions += 1
    return dict(displayed_green_seconds=displayed,
                effective_green_seconds=effective,
                removed_green_seconds=displayed-effective,
                green_onsets=transitions,
                window_seconds=stop-START)


def trial(cfg, tape, checkpoint, period, onset, lost):
    def green(link, tick):
        assert tick >= START and not link.config.closure_windows
        return clock_state(tick, period, onset, lost)[1]
    with patch.object(ReceivingCells, "green", green):
        result = run(cfg, tape, resume_from=checkpoint,
                     phase_overrides=phases(6, "left_first"))
    assert result["remaining"] == 0 and result["generated"] == len(tape)
    return dict(cost=score(result, 0), denied=result["receiver_denied_seconds"])


def experiment():
    reference = json.loads((HERE / "P87_RESULT.json").read_text())
    baseline = {(r["seed"], r["share"], r["clock"], r["onset"]): r["delta"]
                for r in reference["rows"]}
    assert len(baseline) == 192
    rows = []
    summary = Counter()
    exposure_table = {}
    for period, onset, loss in product(PERIODS, ("green", "red"), LOSSES):
        exposure_table[f"{period}/{onset}/{loss}"] = exposure(period, onset, loss, 1440)
    for seed, share, clock in product(range(85001, 85017), (.25, .5, .75), p31.FAMILIES):
        cfg = build_config(seed, 900, share, 7, 4, .5)
        tape = p31.clock(cfg.base, clock)
        cfg = replace(cfg, base=replace(cfg.base, duration_s=1440), downstream_offset_s=0)
        cp = run(cfg, tape, checkpoint_at=START)
        for onset, loss in product(("green", "red"), LOSSES):
            short, long = (trial(cfg, tape, cp, p, onset, loss) for p in PERIODS)
            delta = {k: short[k]-long[k] for k in ("cost", "denied")}
            if loss == 0:
                expected = baseline[(seed, share, clock, onset)]
                assert all(delta[k] == expected[k] for k in delta), (
                    "P87 loss=0 mismatch", seed, share, clock, onset)
            summary[f"{onset}/{loss}/cost_{'lower' if delta['cost'] < 0 else 'higher' if delta['cost'] > 0 else 'equal'}"] += 1
            summary[f"{onset}/{loss}/cost_sum"] += delta["cost"]
            rows.append(dict(seed=seed, share=share, clock=clock, onset=onset,
                             lost_seconds_per_green=loss, delta_30_minus_60=delta))
    assert len(rows) == 768
    return dict(method="additional startup blanking of 0/1/2/3 seconds at every displayed green onset",
                exposures=exposure_table, summary=dict(summary), rows=rows)


if __name__ == "__main__":
    print(json.dumps(experiment(), ensure_ascii=False, indent=2))
