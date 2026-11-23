"""XR5 (external review r2): test the preregistered storage-threshold rule C* ~ R/h on new period pairs."""
import json
from dataclasses import replace
from itertools import product
from pathlib import Path
from unittest.mock import patch
from p85_signal_coordination import build_config, run, score, phases
from p118_temporal_arrival_holdout import tape_with_random_times
from receiving_cells_v15 import ReceivingCells

HERE = Path(__file__).resolve().parent
PAIRS = {(24, 48): (5, 7), (30, 60): (7, 9), (40, 80): (9, 11), (50, 100): (12, 14)}
CAPS = range(4, 17)


def arm(cfg, tape, cp, period):
    def green(self, t):
        return ((t - 84) % period) >= period // 2  # red onset
    with patch.object(ReceivingCells, "green", green):
        r = run(cfg, tape, resume_from=cp, phase_overrides=phases(6, "left_first"))
    assert r["remaining"] == 0
    return score(r, 0), r["receiver_denied_seconds"]


def main():
    rows = []
    for seed, ts, fam in product((86001, 86002), range(88701, 88709), ("stochastic_uniform", "stochastic_platoon4")):
        tape = tape_with_random_times(build_config(seed, 900, .75, 7, 4, .5), seed, ts, fam)
        for cap in CAPS:
            cfg = build_config(seed, 900, .75, 7, cap, .5)
            cfg = replace(cfg, base=replace(cfg.base, duration_s=6000))
            cp = run(cfg, tape, checkpoint_at=84)
            for short, long in PAIRS:
                cs, ds = arm(cfg, tape, cp, short); cl, dl = arm(cfg, tape, cp, long)
                rows.append(dict(seed=seed, time_seed=ts, family=fam, capacity=cap, pair=f"{short}/{long}",
                                 delta_cost=cs - cl, delta_denied=ds - dl, paradox=ds < dl and cs > cl))
    verdict = {}
    for (short, long), (lo, hi) in PAIRS.items():
        key = f"{short}/{long}"
        rate = {c: sum(r["paradox"] for r in rows if r["pair"] == key and r["capacity"] == c) / 32 for c in CAPS}
        first_low = next((c for c in CAPS if rate[c] <= .10), None)
        below_ok = all(rate[c] >= .5 for c in CAPS if c <= lo - 2)
        verdict[key] = dict(rate_by_C={str(c): rate[c] for c in CAPS}, first_C_at_or_below_10pct=first_low,
                            predicted_window=[lo, hi], passed=bool(first_low is not None and lo <= first_low <= hi and below_ok))
    new_fail = sum(not verdict[k]["passed"] for k in ("24/48", "40/80", "50/100"))
    out = dict(status="XR5_COMPLETE", prereg="XR5_THRESHOLD_PREDICTION_PREREG.md", arms=len(rows) * 2,
               verdict=verdict, rule_falsified=new_fail >= 2, rows=rows)
    (HERE / "XR5_RESULT.json").write_text(json.dumps(out, indent=1) + "\n")
    for k, v in verdict.items():
        print(k, v["predicted_window"], v["first_C_at_or_below_10pct"], v["passed"],
              {c: round(x, 2) for c, x in v["rate_by_C"].items()})
    print("rule_falsified", out["rule_falsified"])


if __name__ == "__main__":
    main()
