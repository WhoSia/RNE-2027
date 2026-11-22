"""Frozen-state policy comparison on unseen synthetic arrival tapes."""
from collections import Counter, defaultdict
from dataclasses import replace
from itertools import product
import json
import pickle
from unittest.mock import patch

from dual_lane_v11 import checkpoint_observation, run
from p19_receiver_service_opportunity import build_config, tape_hash
from p25_p26_physical_followups import action
from physical_transfer_screen import score
import p31_two_arrival_families as p31

REGIMES = ((132, 1650, .50), (133, 1650, .50), (134, 1800, .45), (135, 1800, .45))
POLICIES = ("fixed", "pressure_proxy", "guarded")


def select(obs, capacity):
    other = sum(obs[k] for k in ("outside_A", "outside_B", "approach_A", "approach_B"))
    extend = obs["pocket_vehicles"] > 0 and 2 * obs["pocket_vehicles"] >= other
    return (6, 10 if extend else 6,
            10 if extend and capacity - obs["receiver_vehicles"] >= 2 else 6)


def experiment():
    rows = []
    diagnostics = Counter()
    with patch.object(p31, "PLATOON_SPAN", 5):
        for (seed, demand, turn), family, cap, offset, pocket, share in product(
                REGIMES, p31.FAMILIES, (2, 4), (0, 15), (14., 28.), (0., .5)):
            cfg = replace(build_config(seed, demand, turn, pocket, cap, share),
                          downstream_offset_s=offset)
            tape = p31.clock(cfg.base, family)
            cp = run(cfg, tape, checkpoint_at=84)
            frozen = pickle.dumps(cp, protocol=4)
            observation = checkpoint_observation(cp)
            diagnostics["pocket_positive"] += observation["pocket_vehicles"] > 0
            diagnostics["receiver_two_free"] += cap - observation["receiver_vehicles"] >= 2
            durations = select(observation, cap)
            costs = {d: score(run(cfg, tape, resume_from=cp, phase_overrides=action(d)), 60)
                     for d in (6, 10)}
            if pickle.dumps(cp, protocol=4) != frozen:
                raise ValueError("checkpoint mutated")
            rows.append((family, tape_hash(tape), costs, durations))
    results = {}
    for index, name in enumerate(POLICIES):
        deltas, regrets, tape_deltas = [], [], defaultdict(int)
        for _, tape, costs, durations in rows:
            value = costs[durations[index]]
            delta = value - costs[6]
            deltas.append(delta)
            regrets.append(value - min(costs.values()))
            tape_deltas[tape] += delta
        results[name] = {
            "total_delta_vs_fixed": sum(deltas), "worst_regret": max(regrets),
            "total_regret": sum(regrets), "worse_worlds": sum(d > 0 for d in deltas),
            "better_worlds": sum(d < 0 for d in deltas),
            "worse_tapes": sum(d > 0 for d in tape_deltas.values()),
            "extensions": sum(r[3][index] == 10 for r in rows),
        }
    for stats in results.values():
        stats["advances"] = (stats["total_delta_vs_fixed"] < 0
                             and stats["worst_regret"] <= results["fixed"]["worst_regret"]
                             and stats["worse_tapes"] == 0)
    diagnostics["oracle_prefers_extension"] = sum(r[2][10] < r[2][6] for r in rows)
    diagnostics["oracle_prefers_fixed"] = sum(r[2][6] < r[2][10] for r in rows)
    return {"worlds": len(rows), "tapes": len({r[1] for r in rows}),
            "diagnostics": dict(diagnostics), "policies": results}


if __name__ == "__main__":
    print(json.dumps(experiment(), sort_keys=True, indent=2))
