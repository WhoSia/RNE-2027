"""XR4 (external review r2): scale-up of the P126/P127 frontier cells that rested on n=4..16 tapes.

Unseen timing seeds 88601..88632 x label seeds 86001/86002 x two P118 families; left share .50/.75;
shared receiver C = 6,7,8,9; red onset (phi30=15, phi60=30) exactly as P118/P126/P127.
Clusters: a timing seed x family x label seed = one tape; rates are reported with a cluster
bootstrap over timing seeds (1000 draws, fixed RNG). Same T2 engine, no field claim.
"""
import json, random
from dataclasses import replace
from itertools import product
from pathlib import Path
from p85_signal_coordination import build_config, run
from p118_temporal_arrival_holdout import tape_with_random_times, arm

HERE = Path(__file__).resolve().parent
TS = range(88601, 88633)


def main():
    rows = []
    for share, seed, ts, fam in product((.5, .75), (86001, 86002), TS, ("stochastic_uniform", "stochastic_platoon4")):
        tape = tape_with_random_times(build_config(seed, 900, share, 7, 4, .5), seed, ts, fam)
        for cap in (6, 7, 8, 9):
            cfg = build_config(seed, 900, share, 7, cap, .5)
            cfg = replace(cfg, base=replace(cfg.base, duration_s=4800))
            cp = run(cfg, tape, checkpoint_at=84)
            s, l = arm(cfg, tape, cp, 30), arm(cfg, tape, cp, 60)
            rows.append(dict(share=share, label_seed=seed, time_seed=ts, family=fam, capacity=cap,
                             delta_cost=s["cost"] - l["cost"], delta_denied=s["denied"] - l["denied"],
                             paradox=s["denied"] < l["denied"] and s["cost"] > l["cost"]))
    rng = random.Random(132)  # seed kept from first local run
    summary = {}
    for share, cap, fam in product((.5, .75), (6, 7, 8, 9), ("stochastic_uniform", "stochastic_platoon4")):
        sub = [r for r in rows if r["share"] == share and r["capacity"] == cap and r["family"] == fam]
        by_ts = {}
        for r in sub:
            by_ts.setdefault(r["time_seed"], []).append(r["paradox"])
        keys = sorted(by_ts)
        boots = []
        for _ in range(1000):
            draw = [by_ts[rng.choice(keys)] for _ in keys]
            boots.append(sum(sum(x) for x in draw) / sum(len(x) for x in draw))
        boots.sort()
        summary[f"{share}/C{cap}/{fam}"] = dict(n=len(sub), paradox=sum(r["paradox"] for r in sub),
                                                rate=sum(r["paradox"] for r in sub) / len(sub),
                                                ci95=[boots[24], boots[974]],
                                                mean_delta_cost=sum(r["delta_cost"] for r in sub) / len(sub))
    out = dict(status="XR4_COMPLETE", arms=len(rows) * 2, tapes_per_cell=64, summary=summary, rows=rows)
    (HERE / "XR4_RESULT.json").write_text(json.dumps(out, indent=1) + "\n")
    for k, v in summary.items():
        print(k, f"{v['paradox']}/{v['n']}", [round(x, 3) for x in v["ci95"]], round(v["mean_delta_cost"], 1))


if __name__ == "__main__":
    main()
