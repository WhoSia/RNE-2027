"""Choose fixed or chronological adaptive observations before intervention."""
from functools import lru_cache
from itertools import combinations, product

from timing_bounds import ALPHABET, exact

PRESENCE = (("",), ("T", "L"))
MOVEMENT = (("",), ("T",), ("L",))


def compare(width, bins, config, decision, partition, budget, initial, *, bin_upper=None, bin_total_upper=None):
    ticks = tuple(range(min(width * len(bins), decision)))
    labels = tuple(symbol for branch in partition for symbol in branch)
    if sorted(labels) != sorted(ALPHABET) or any(not branch for branch in partition):
        raise ValueError("responses must partition the arrival symbols")
    if budget < 0 or budget > len(ticks):
        raise ValueError("invalid observation budget")

    @lru_cache(maxsize=None)
    def bounds(observed):
        return exact(width, bins, config, dict(observed), initial=initial, decision_tick=decision,
                     bin_upper=bin_upper, bin_total_upper=bin_total_upper)

    def branches(observed, t):
        for label in partition:
            key = observed + ((t, label),)
            if bounds(key):
                yield label, key

    @lru_cache(maxsize=None)
    def tree(observed, available, depth):
        r = bounds(observed).regret
        best = r, None
        if depth == 0 or r == 0:
            return best
        for j, t in enumerate(available):
            options = [(response, tree(key, available[j+1:], depth-1))
                       for response,key in branches(observed,t)]
            if len(options) > 1:
                score = max(value for _,(value,_) in options)
                if score < best[0]:
                    best = score, (t, options)
        return best

    base = bounds(())
    if base is None:
        raise ValueError("infeasible bins")
    fixed = None
    pruned_fixed_plans = 0
    for plan in combinations(ticks, budget):
        worst = paths = 0
        for responses in product(partition, repeat=budget):
            result = bounds(tuple(zip(plan, responses)))
            if result is None:
                continue
            paths += result.paths
            worst = max(worst, result.regret)
            # Plans are visited in lexicographic order, so ties keep the incumbent.
            if fixed is not None and worst >= fixed[0]:
                pruned_fixed_plans += 1
                break
        else:
            assert paths == base.paths
            fixed = worst, plan
    score, policy = tree((),ticks,budget)
    assert score <= fixed[0]
    starting_queue_revealed = max(exact(width,bins,config,initial=(state,),
                                        decision_tick=decision, bin_upper=bin_upper,
                                        bin_total_upper=bin_total_upper).regret for state in initial)
    return {"starting_queue_revealed_regret": starting_queue_revealed, "before_action": decision, "observations": budget, "bounds": (base.low,base.high),
            "paths":base.paths, "unobserved_regret":base.regret, "fixed":fixed,
            "adaptive_regret":score, "adaptive_tree":policy, "exact_dp_calls":bounds.cache_info().misses,
            "pruned_fixed_plans":pruned_fixed_plans}


if __name__ == "__main__":
    import argparse
    import json
    from pathlib import Path

    from d51_phase_order import Params

    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    bins = ((1,1),(2,0),(2,0),(1,1))
    config = Params(left_capacity=1,horizon_s=180)
    initial = (("",0,0),("",0,1))
    sensors = (("presence",PRESENCE),("movement",MOVEMENT))
    rows = [{"sensor":label, **compare(3,bins,config,decision,partition,budget,initial)}
            for decision,(label,partition),budget in product((4,8,12),sensors,(1,2))]
    options = ((1,1),(2,0),(0,2),(1,0),(0,1))
    screen = {"ambiguous": 0, "reduced": [], "adaptive_advantage": []}
    for signature, decision in product(product(options,repeat=3),(4,8,9)):
        b = exact(3,signature,config,initial=initial,decision_tick=decision)
        if b.regret == 0:
            continue
        screen["ambiguous"] += 1
        result = compare(3,signature,config,decision,MOVEMENT,2,initial)
        if result["adaptive_regret"] < b.regret:
            screen["reduced"].append({"bins":signature,**result})
        if result["adaptive_regret"] < result["fixed"][0]:
            screen["adaptive_advantage"].append({"bins":signature,**result})
    args.output.write_text(json.dumps({"fixed_example":rows, "screen":screen},indent=2)+"\n")
