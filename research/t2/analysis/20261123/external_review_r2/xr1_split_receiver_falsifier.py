"""XR1 (external review r2): shared vs movement-separated downstream receivers (see XR1_SPLIT_RECEIVER_PREREG.md)."""
import hashlib, json
from dataclasses import replace
from itertools import product
from pathlib import Path
from unittest.mock import patch

from p85_signal_coordination import build_config, run, score, phases
from p118_temporal_arrival_holdout import tape_with_random_times
from receiving_cells_v15 import ReceivingCells

HERE = Path(__file__).resolve().parent
TOPOLOGIES = {"shared": {}, "split_same_clock": {"receiver_split": True},
              "split_left_free": {"receiver_split": True, "receiver_split_left_free": True}}
SHARES = (.25, .50, .75)
CAPS = (4, 8)
TIME_SEEDS = range(88401, 88409)
LABEL_SEEDS = (86001, 86002)
FAMILIES = ("stochastic_uniform", "stochastic_platoon4")


def arm(cfg, tape, cp, period, phi):
    def green(self, t):
        c = self.config
        if c.downstream_green_s == c.downstream_cycle_s:  # uncontrolled (left_free) link
            return True
        return ((t - 84 + phi) % period) < period // 2

    with patch.object(ReceivingCells, "green", green):
        r = run(cfg, tape, resume_from=cp, phase_overrides=phases(6, "left_first"))
    assert r["generated"] == 60 and r["remaining"] == 0 and r["network_out_S"] + r["network_out_L"] == 60
    return score(r, 0), r["receiver_denied_seconds"]


def config(seed, share, cap, topo):
    cfg = build_config(seed, 900, share, 7, cap, .5)
    return replace(cfg, base=replace(cfg.base, duration_s=4800), **TOPOLOGIES[topo])


def left_overlap(phi, period):
    # left-green calendar of the P116 rule: upstream L at t in [87,93) then t%120 in [0,35), t in [84,400)
    from spatial_v10 import phase as up
    cfg = build_config(86001, 900, .5, 7, 4, .5)
    n = 0
    for t in range(84, 400):
        light = next((v for a, b, v in phases(6, "left_first") if a <= t < b), up(cfg.base, t))
        n += light == "L" and ((t - 84 + phi) % period) < period // 2
    return n


def main():
    rows = []
    hashes = set()
    for share, seed, ts, fam in product(SHARES, LABEL_SEEDS, TIME_SEEDS, FAMILIES):
        tape = tape_with_random_times(build_config(seed, 900, share, 7, 4, .5), seed, ts, fam)
        stamp = hashlib.sha256(json.dumps([t for t, _ in tape]).encode()).hexdigest()
        hashes.add((share, stamp))
        for cap, topo in product(CAPS, TOPOLOGIES):
            cfg = config(seed, share, cap, topo)
            cp = run(cfg, tape, checkpoint_at=84)
            c30, d30 = arm(cfg, tape, cp, 30, 15)
            c60, d60 = arm(cfg, tape, cp, 60, 30)
            rows.append(dict(share=share, label_seed=seed, time_seed=ts, family=fam, time_sha256=stamp,
                             capacity=cap, topology=topo, cost30=c30, cost60=c60, denied30=d30, denied60=d60,
                             delta_cost=c30 - c60, delta_denied=d30 - d60, paradox=d30 < d60 and c30 > c60))
    assert len(rows) == 3 * 2 * 8 * 2 * 2 * 3 and len(hashes) == 3 * 32
    summary = {}
    for share, cap, topo in product(SHARES, CAPS, TOPOLOGIES):
        sub = [r for r in rows if r["share"] == share and r["capacity"] == cap and r["topology"] == topo]
        summary[f"{share}/C{cap}/{topo}"] = dict(n=len(sub), paradox=sum(r["paradox"] for r in sub),
                                                 cost30_worse=sum(r["delta_cost"] > 0 for r in sub),
                                                 sum_delta_cost=sum(r["delta_cost"] for r in sub),
                                                 by_family={f: sum(r["paradox"] for r in sub if r["family"] == f) for f in FAMILIES})
    split = summary["0.75/C4/split_same_clock"]["paradox"]
    verdict = ("REQUIRES_SHARED_RECEIVER" if split <= 8 else "SURVIVES_SEPARATION" if split >= 24 else "PARTIAL")
    # secondary: full offset grid
    ov = {p: {phi: left_overlap(phi, p) for phi in range(p)} for p in (30, 60)}
    grid = []
    for seed, ts, fam in product(LABEL_SEEDS, (88401, 88402), FAMILIES):
        tape = tape_with_random_times(build_config(seed, 900, .75, 7, 4, .5), seed, ts, fam)
        for topo in ("shared", "split_same_clock"):
            cfg = config(seed, .75, 4, topo)
            cp = run(cfg, tape, checkpoint_at=84)
            c = {p: {phi: arm(cfg, tape, cp, p, phi)[0] for phi in range(p)} for p in (30, 60)}
            signs = set(); hit = tot = 0
            for a, b in product(range(30), range(60)):
                d = c[30][a] - c[60][b]; signs.add((d > 0) - (d < 0))
                dov = ov[60][b] - ov[30][a]
                if dov and d:
                    tot += 1; hit += (dov > 0) == (d > 0)
            grid.append(dict(label_seed=seed, time_seed=ts, family=fam, topology=topo,
                             both_signs=1 in signs and -1 in signs, overlap_rule_hits=hit, overlap_rule_n=tot,
                             min30=min(c[30].values()), min60=min(c[60].values()),
                             mean30=sum(c[30].values()) / 30, mean60=sum(c[60].values()) / 60))
    sec = {topo: dict(tapes=sum(g["topology"] == topo for g in grid),
                      both_signs=sum(g["both_signs"] for g in grid if g["topology"] == topo),
                      overlap_rule_accuracy=sum(g["overlap_rule_hits"] for g in grid if g["topology"] == topo) /
                      sum(g["overlap_rule_n"] for g in grid if g["topology"] == topo),
                      best60_beats_best30=sum(g["min60"] < g["min30"] for g in grid if g["topology"] == topo),
                      mean30_beats_mean60=sum(g["mean30"] < g["mean60"] for g in grid if g["topology"] == topo))
           for topo in ("shared", "split_same_clock")}
    out = dict(status="XR1_COMPLETE", prereg="XR1_SPLIT_RECEIVER_PREREG.md", arms_primary=len(rows) * 2,
               arms_grid=len(grid) * 90, primary_split_paradox=f"{split}/32",
               primary_shared_paradox=f"{summary['0.75/C4/shared']['paradox']}/32", verdict=verdict,
               summary=summary, offset_grid=sec, grid_rows=grid, rows=rows,
               limitation="Same T2 engine with an optional separated receiver; not SUMO or field. "
                          "32 tapes per share = 2 label seeds x 8 timing seeds x 2 families.")
    (HERE / "XR1_RESULT.json").write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n")
    print(json.dumps({k: out[k] for k in ("primary_shared_paradox", "primary_split_paradox", "verdict", "offset_grid")}, indent=1))
    for k, v in summary.items():
        print(k, v["paradox"], v["cost30_worse"], v["sum_delta_cost"], v["by_family"])


if __name__ == "__main__":
    main()
