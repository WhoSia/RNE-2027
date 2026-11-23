"""XR2 test (external review r2): M0/M1/M2 against T2 on an unseen offset grid (see XR2_QUEUE_MODEL_PREREG.md)."""
import json
from dataclasses import replace
from itertools import product
from pathlib import Path
from statistics import median
from unittest.mock import patch

from p85_signal_coordination import build_config, run, score, phases
from p118_temporal_arrival_holdout import tape_with_random_times
from receiving_cells_v15 import ReceivingCells
import xr2_queue_model as qm

HERE = Path(__file__).resolve().parent


def t2_cost(cfg, tape, cp, period, phi):
    def green(self, t):
        return ((t - 84 + phi) % period) < period // 2
    with patch.object(ReceivingCells, "green", green):
        r = run(cfg, tape, resume_from=cp, phase_overrides=phases(6, "left_first"))
    assert r["remaining"] == 0
    return score(r, 0), r["receiver_denied_seconds"]


def spearman(x, y):
    def rk(v):
        o = sorted(range(len(v)), key=lambda i: v[i]); r = [0.0] * len(v); i = 0
        while i < len(o):
            j = i
            while j + 1 < len(o) and v[o[j + 1]] == v[o[i]]:
                j += 1
            for k in range(i, j + 1):
                r[o[k]] = (i + j) / 2
            i = j + 1
        return r
    a, b = rk(x), rk(y); n = len(a); ma = sum(a) / n; mb = sum(b) / n
    cov = sum((p - ma) * (q - mb) for p, q in zip(a, b))
    va = sum((p - ma) ** 2 for p in a) ** .5; vb = sum((q - mb) ** 2 for q in b) ** .5
    return cov / (va * vb) if va and vb else float("nan")


def sgn(x):
    return (x > 0) - (x < 0)


def main():
    ov = {p: {phi: qm.left_overlap(p, phi) for phi in range(p)} for p in (30, 60)}
    configs = []
    for share, cap, seed, ts, fam in product((.5, .75), (4, 8), (86001, 86002), range(88501, 88505),
                                             ("stochastic_uniform", "stochastic_platoon4")):
        tape = tape_with_random_times(build_config(seed, 900, share, 7, 4, .5), seed, ts, fam)
        cfg = build_config(seed, 900, share, 7, cap, .5)
        cfg = replace(cfg, base=replace(cfg.base, duration_s=4800))
        cp = run(cfg, tape, checkpoint_at=84)
        T2 = {p: {phi: t2_cost(cfg, tape, cp, p, phi) for phi in range(p)} for p in (30, 60)}
        M = {v: {p: {phi: qm.simulate(tape, C=cap, period=p, phi=phi, variant=v)[:2] for phi in range(p)}
                 for p in (30, 60)} for v in ("M1", "M2")}
        stats = {}
        for v in ("M0", "M1", "M2"):
            hit = n = eq_hit = eq_n = 0
            for a, b in product(range(30), range(60)):
                truth = sgn(T2[30][a][0] - T2[60][b][0])
                if v == "M0":
                    pred = sgn(ov[60][b] - ov[30][a])
                else:
                    pred = sgn(M[v][30][a][0] - M[v][60][b][0])
                if truth and pred:
                    n += 1; hit += truth == pred
                    if ov[30][a] == ov[60][b]:
                        eq_n += 1; eq_hit += truth == pred
            rho = None
            if v != "M0":
                rho = [spearman([T2[p][phi][0] for phi in range(p)], [M[v][p][phi][0] for phi in range(p)]) for p in (30, 60)]
            stats[v] = dict(hit=hit, n=n, eq_hit=eq_hit, eq_n=eq_n, rho30_60=rho)
        red = {s: dict(t2_paradox=T2[30][15][1] < T2[60][30][1] and T2[30][15][0] > T2[60][30][0],
                       t2_cost_worse=T2[30][15][0] > T2[60][30][0]) for s in ("x",)}["x"]
        for v in ("M1", "M2"):
            red[v + "_cost_worse"] = M[v][30][15][0] > M[v][60][30][0]
            red[v + "_paradox"] = M[v][30][15][1] < M[v][60][30][1] and M[v][30][15][0] > M[v][60][30][0]
        configs.append(dict(share=share, capacity=cap, label_seed=seed, time_seed=ts, family=fam,
                            stats=stats, red_onset=red))
        print("done", share, cap, seed, ts, fam, {v: round(stats[v]["hit"] / stats[v]["n"], 3) for v in stats}, flush=True)
    pooled = {}
    for v in ("M0", "M1", "M2"):
        H = sum(c["stats"][v]["hit"] for c in configs); N = sum(c["stats"][v]["n"] for c in configs)
        EH = sum(c["stats"][v]["eq_hit"] for c in configs); EN = sum(c["stats"][v]["eq_n"] for c in configs)
        pooled[v] = dict(strict_accuracy=H / N, strict_n=N, equal_overlap_accuracy=(EH / EN if EN else None), equal_overlap_n=EN,
                         per_config_accuracy_min=min(c["stats"][v]["hit"] / c["stats"][v]["n"] for c in configs))
        if v != "M0":
            rhos = [r for c in configs for r in c["stats"][v]["rho30_60"]]
            pooled[v]["median_spearman"] = median(rhos); pooled[v]["min_spearman"] = min(rhos)
    by_stratum = {}
    for share, cap in product((.5, .75), (4, 8)):
        sub = [c for c in configs if c["share"] == share and c["capacity"] == cap]
        by_stratum[f"{share}/C{cap}"] = {v: sum(c["stats"][v]["hit"] for c in sub) / sum(c["stats"][v]["n"] for c in sub)
                                         for v in ("M0", "M1", "M2")}
        by_stratum[f"{share}/C{cap}"]["red_onset_t2_cost_worse"] = sum(c["red_onset"]["t2_cost_worse"] for c in sub)
        for v in ("M1", "M2"):
            by_stratum[f"{share}/C{cap}"][f"red_onset_{v}_agrees"] = sum(c["red_onset"][f"{v}_cost_worse"] == c["red_onset"]["t2_cost_worse"] for c in sub)
    g = {v: dict(G1=pooled[v]["strict_accuracy"] >= pooled["M0"]["strict_accuracy"] + .03,
                 G2=(pooled[v]["equal_overlap_accuracy"] or 0) >= .75,
                 G3=pooled[v]["median_spearman"] >= .7) for v in ("M1", "M2")}
    out = dict(status="XR2_COMPLETE", prereg="XR2_QUEUE_MODEL_PREREG.md", t2_arms=len(configs) * 90,
               configs=len(configs), pooled=pooled, by_stratum=by_stratum, gates=g, rows=configs,
               limitation="Model compared to T2 only; agreement with T2 is not physical validation.")
    (HERE / "XR2_RESULT.json").write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n")
    print(json.dumps(dict(pooled=pooled, by_stratum=by_stratum, gates=g), indent=1))


if __name__ == "__main__":
    main()
