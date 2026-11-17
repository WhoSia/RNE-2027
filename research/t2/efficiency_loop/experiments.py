"""Reproduce the latent-observation and robust-control experiments."""
import argparse
from dataclasses import asdict
from itertools import combinations, product
import json
from pathlib import Path
from random import Random
from time import perf_counter

from d51_phase_order import Params
from optimize import catalog, oracle_offsets, search
from signal_model import Plan, Scenario, run
from timing_bounds import exact, probe, sequence_count


def timing():
    bins = ((1, 1), (2, 0), (2, 0), (1, 1))
    p = Params(left_capacity=1, horizon_s=180)
    base = exact(3, bins, p)
    probes = {}
    for labeled, k in product((False, True), (1, 2)):
        scores = [(probe(3, bins, p, ticks, labeled), ticks)
                  for ticks in combinations(range(12), k)]
        assert all(n == sequence_count(3, bins) == base.paths for (_, n), _ in scores)
        minimum = min(score for (score, _), _ in scores)
        probes[f"{'movement' if labeled else 'occupancy'}_{k}"] = {
            "worst_case_regret": minimum, "best_ticks": [ts for (score, _), ts in scores if score == minimum],
            "median_location_regret": sorted(score for (score, _), _ in scores)[len(scores)//2],
        }
    signatures = 0
    changed = []
    options = tuple((T, L) for T in range(4) for L in range(4-T) if 1 <= T+L <= 2)
    for signature in product(options, repeat=3):
        if sum(T for T,L in signature) == 0 or sum(L for T,L in signature) == 0:
            continue
        b = exact(3, signature, p)
        signatures += 1
        if b.low < 0 < b.high:
            changed.append((signature, b.low, b.high))
    initial = (("", 0, 0), ("", 1, 0), ("", 0, 1), ("LT", 0, 1))
    sensitivity = {str(start): asdict(exact(3, bins, p, initial=(start,))) for start in initial}
    combined = exact(3, bins, p, initial=initial)
    upper = ((2,1),(2,0),(2,1),(1,1))
    incomplete = exact(3,bins,p,bin_upper=upper)
    return {"missing_track_counts": {"lower_counts":bins,"upper_counts":upper,
                                     "bound":asdict(incomplete),"regret":incomplete.regret},
            "initial_state_sensitivity": sensitivity, "latent_initial": asdict(combined),
            "latent_initial_regret": combined.regret, "bin_counts_T_L": bins, "bounds": asdict(base), "unobserved_regret": base.regret,
            "probes": probes, "screened_signatures": signatures, "sign_reversals": changed}


def generated():
    demand = ((.16,.06,.15,.05,.14,.13,.10), (.21,.16,.12,.07,.10,.09,.07),
              (.08,.03,.10,.03,.20,.19,.13), (.16,.08,.15,.08,.15,.13,.16),
              (.03,.01,.03,.01,.04,.03,.03))
    scenarios = []
    for i, rates in enumerate(demand):
        rng = Random(431 + i)
        arrivals = tuple((t,m) for t in range(336) for m, rate in enumerate(rates)
                         if rng.random() < rate)
        scenarios.append(Scenario(("balanced", "turn-surge", "cross-surge", "tight-downstream", "light")[i],
                                  336, arrivals, bay=(8,2,8,2,10,10) if i == 1 else (8,3,8,3,10,10),
                                  link=(3,2,3,2,4,4) if i == 3 else (6,3,6,3,6,6),
                                  receive_green=12 if i == 3 else 23, receive_offset=i*4))
    return tuple(scenarios)


def measure(f, *args, **kwargs):
    start = perf_counter()
    value = f(*args, **kwargs)
    return value, round(perf_counter() - start, 4)


def optimize():
    plans, cases = catalog(), generated()
    baseline = Plan((28, 12, 20, 12), False, 0)
    modes = ((False, False), (True, False), (False, True), (True, True))
    table = {}

    def matrix_search():
        matrix = {p: tuple(run(p,s,fast=False).cost for s in cases) for p in plans}
        offsets = tuple(min(column) for column in zip(*matrix.values()))
        worst = min((max(row), p) for p,row in matrix.items())
        regret = min((max(c - off for c,off in zip(row,offsets)), p) for p,row in matrix.items())
        return worst, regret, offsets

    ((matrix_cost, matrix_plan), (matrix_regret, matrix_regret_plan), matrix_offsets), matrix_s = measure(matrix_search)
    for fast, prune, relax in tuple((f,p,False) for f,p in modes) + ((False,True,True),):
        # Cache is shared by all methods and warmed equally.
        row = {}
        kwargs = {"fast": fast, "prune": prune, "first": baseline, "relax": relax}
        worst, elapsed = measure(search, plans, cases, **kwargs)
        row["worst"] = asdict(worst) | {"seconds": elapsed}
        (offsets, oracle_runs), elapsed = measure(oracle_offsets, plans, cases, **kwargs)
        row["scenario_oracle"] = {"values": offsets, "evaluations": sum(x.evaluations for x in oracle_runs),
                                  "abandoned": sum(x.abandoned for x in oracle_runs),
                                  "screened": sum(x.screened for x in oracle_runs), "seconds": elapsed}
        regret, elapsed = measure(search, plans, cases, offsets, **kwargs)
        row["regret"] = asdict(regret) | {"seconds": elapsed}
        assert (worst.plan, worst.value, regret.plan, regret.value, offsets) == (
            matrix_plan, matrix_cost, matrix_regret_plan, matrix_regret, matrix_offsets)
        table[f"event_{fast}_bound_{prune}" + ("_relaxed" if relax else "")] = row
    return {"plans": len(plans), "matrix_benchmark": {"seconds": matrix_s,
            "evaluations": len(plans) * len(cases)}, "methods": table, "comparison": [
        {"scenario": s.name, "arrivals": len(s.arrivals), "oracle": minimum,
         "baseline": asdict(run(baseline,s)), "minimax": asdict(run(matrix_plan,s)),
         "minimax_regret": asdict(run(matrix_regret_plan,s))}
        for s, minimum in zip(cases, matrix_offsets)]}


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("mode", choices=("timing", "optimize"))
    p.add_argument("output", type=Path)
    a = p.parse_args()
    a.output.write_text(json.dumps({"timing": timing, "optimize": optimize}[a.mode](),
                                   indent=2, ensure_ascii=False) + "\n")
