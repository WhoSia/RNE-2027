"""Evaluate imperfect decision-time pocket measurements on the D51 grid."""
import argparse
from fractions import Fraction
from itertools import product
import json
from pathlib import Path

from d51_phase_order import Params
from prospective_sensing import PROFILE, QUEUE_STARTS, WIDTH, information_at_decision
from timing_bounds import exact

ACTIONS = ("lag","lead")


def by_count(visible, decision, forecast_cap, config):
    bins = visible + ((0,0),)
    lower,upper,ceilings = information_at_decision(bins, WIDTH, decision, forecast_cap)
    options = {"bin_upper":upper,"bin_total_upper":ceilings,"initial":QUEUE_STARTS,"decision_tick":decision}
    base = exact(WIDTH,lower,config,**options)
    groups = {}
    for count in range(config.left_capacity+1):
        b = exact(WIDTH,lower,config,**options,decision_left=(count,))
        if b is not None:
            groups[count] = b
    if sum(b.paths for b in groups.values()) != base.paths:
        raise RuntimeError("Decision snapshots do not partition all possible arrivals")
    if (min(b.low for b in groups.values()), max(b.high for b in groups.values())) != (base.low,base.high):
        raise RuntimeError("Snapshot union changed the forecast interval")
    return base,groups


def reading_support(count, capacity, mode):
    """Return readings that an adversarial but bounded sensor can emit."""
    if mode == "fullness":
        return {int(count == capacity)}
    if mode == "exact":
        return {count}
    if mode == "off_by_one":
        return set(range(max(0,count-1), min(capacity,count+1)+1))
    if mode == "miss_one":
        return {max(0,count-1),count}
    raise ValueError(f"Unknown reading mode {mode}")


def action_regrets(low, high):
    return max(0,-low), max(0,high)


def bounded_error(groups, capacity, mode):
    # Two different readings may be compatible with the same physical world.
    # Only the true-count groups are a partition.
    preimages = {}
    for count,bounds in groups.items():
        for reading in reading_support(count,capacity,mode):
            preimages.setdefault(reading,[]).append(bounds)
    branches = {}
    for reading,possible in sorted(preimages.items()):
        low = min(world.low for world in possible)
        high = max(world.high for world in possible)
        scores = action_regrets(low,high)
        branches[reading] = {"delta":[low,high],"worst_regret":min(scores),
                             "choice":"either" if scores[0] == scores[1] else ACTIONS[scores.index(min(scores))]}
    return {"worst_regret":max(branch["worst_regret"] for branch in branches.values()),"branches":branches}


def erasure_policy(groups, upper):
    """Minimize worst expected regret when correct readings may be erased.

    The erasure chance may depend on the true world but is bounded by upper.
    One policy maps each readable count to an action and chooses a fallback.
    """
    if not 0 <= upper <= 1:
        raise ValueError("Erasure probability must be between zero and one")
    intervals = [(b.low,b.high) for b in groups.values()]
    best = None
    for fallback,*actions in product(ACTIONS,repeat=len(groups)+1):
        values = []
        for (low,high),choice in zip(intervals,actions,strict=True):
            # For any realized delta, lead pays positive delta and lag pays negative delta.
            # The expectation is affine in the erasure probability for that same world.
            for probability in (0,upper):
                weight = (1-probability)*(choice == "lead") + probability*(fallback == "lead")
                values.append(max(weight*max(0,high),(1-weight)*max(0,-low)))
        candidate = max(values), fallback, tuple(actions)
        if best is None or candidate < best:
            best = candidate
    regret,fallback,actions = best
    return regret,{"fallback":fallback,"readable":dict(zip(groups,actions,strict=True))}


def grid(capacities=(1, 2)):
    modes = ("exact","fullness","miss_one","off_by_one")
    erasure_limits = (Fraction(0), Fraction(1,10), Fraction(1,4), Fraction(1,2), Fraction(1))
    rows = []
    for capacity,decision,cap,visible in product(capacities,(6,8),(2,3),product(PROFILE,repeat=2)):
        config = Params(left_capacity=capacity,horizon_s=180)
        base,groups = by_count(visible,decision,cap,config)
        reports = {mode:bounded_error(groups,capacity,mode) for mode in modes}
        erased = [erasure_policy(groups,q) for q in erasure_limits]
        assert reports["exact"]["worst_regret"] == erased[0][0]
        assert erased[-1][0] == base.regret
        assert all(a[0] <= b[0] for a,b in zip(erased,erased[1:]))
        assert reports["exact"]["worst_regret"] <= reports["miss_one"]["worst_regret"] <= reports["off_by_one"]["worst_regret"] <= base.regret
        rows.append({"capacity":capacity,"decision":decision,"future_cap":cap,"visible_counts":visible,
                     "unmeasured_regret":base.regret,"modes":reports,
                     "erasure":[{"max_probability":str(q),"worst_expected_regret":float(value),"policy":policy}
                                for q,(value,policy) in zip(erasure_limits,erased,strict=True)]})
    def summary(values):
        return {"improved_contexts":sum(c["unmeasured_regret"] > value for c,value in zip(rows,values,strict=True)),
                "maximum_regret_reduction":max(c["unmeasured_regret"]-value for c,value in zip(rows,values,strict=True))}
    return {"capacities":list(capacities), "contexts":len(rows),"ambiguous_without_sensor":sum(c["unmeasured_regret"]>0 for c in rows),
            "reading_error":{mode:summary([c["modes"][mode]["worst_regret"] for c in rows]) for mode in modes},
            "erasure":{str(q):summary([c["erasure"][i]["worst_expected_regret"] for c in rows])
                       for i,q in enumerate(erasure_limits)},
            "example":max(rows,key=lambda c:c["unmeasured_regret"]-c["modes"]["exact"]["worst_regret"]),
            "scope":"Synthetic point queue. Rates are assumed for sensitivity, not estimated from traffic data."}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("output",type=Path)
    parser.add_argument("--capacities", type=int, nargs="+", default=(1, 2))
    args = parser.parse_args()
    if any(capacity < 1 for capacity in args.capacities):
        parser.error("capacities must be positive")
    args.output.write_text(json.dumps(grid(tuple(dict.fromkeys(args.capacities))), indent=2)+"\n")
