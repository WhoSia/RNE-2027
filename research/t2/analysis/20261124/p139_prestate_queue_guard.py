"""P139: preregistered t84-only queue guard against frozen calendar-only policy.

WARNING: Executing this module is necessary to obtain P139 results. Merely
committing this source is NOT experimental validation.
"""
from __future__ import annotations

import hashlib
import json
from collections import defaultdict
from itertools import product
from pathlib import Path

from p85_signal_coordination import build_config
from p118_temporal_arrival_holdout import tape_with_random_times
from p136_offset_diversified_proxy_regret import (
    LABEL_SEEDS, FAMILIES, SHARES, OFFSETS, arm,
)
import p130_split_shared_outflow as topology
from dual_lane_separate_receivers_p130 import checkpoint_observation

HERE = Path(__file__).resolve().parent
TIME_SEEDS = (88801, 88802)
CALENDAR = {(0, 30): 60, (15, 0): 30, (7, 15): 60, (23, 45): 30}
assert set(CALENDAR) == set(OFFSETS)


def prestate_snapshot(cp):
    """No post-84 data and no hidden label/time seeds; six aggregate counters."""
    ob = checkpoint_observation(cp)
    assert ob["decision_tick"] == 84, ob["decision_tick"]
    keys = ("outside_A", "outside_B", "approach_A", "approach_B",
            "pocket_vehicles", "receiver_vehicles")
    s = {key: ob[key] for key in keys}
    assert all(isinstance(v, int) and v >= 0 for v in s.values())
    assert 0 <= s["receiver_vehicles"] <= 4
    return s


def calendar_choice(offset):
    return CALENDAR[tuple(offset)]


def guard_choice(offset, state):
    """Fixed, zero-fit policy chosen BEFORE reading P139 result outcomes."""
    baseline = calendar_choice(offset)
    q = (state["outside_A"] + state["outside_B"] +
         state["approach_A"] + state["approach_B"] +
         state["pocket_vehicles"])
    if tuple(offset) == (7, 15) and state["receiver_vehicles"] >= 3 and q >= 6:
        assert baseline == 60
        return 30
    return baseline


def cost_regret(row, policy):
    costs = row["arms"]
    return costs[str(policy)]["cost"] - min(costs["30"]["cost"], costs["60"]["cost"])


def summarize(rows):
    def score(k):
        return {
            "correct": sum(cost_regret(r, r["choices"][k]) == 0 for r in rows),
            "total_regret": sum(cost_regret(r, r["choices"][k]) for r in rows),
        }
    result = {"n": len(rows), "calendar": score("calendar"),
              "guard": score("guard"), "fixed30": score("fixed30"),
              "fixed60": score("fixed60")}
    result["guard_triggered"] = sum(r["choices"]["guard"] != r["choices"]["calendar"]
                                    for r in rows)
    result["guard_beneficial"] = sum(
        cost_regret(r, r["choices"]["guard"]) < cost_regret(r, r["choices"]["calendar"])
        for r in rows
    )
    result["guard_harmful"] = sum(
        cost_regret(r, r["choices"]["guard"]) > cost_regret(r, r["choices"]["calendar"])
        for r in rows
    )
    return result


def main():
    rows = []
    timehashes = {str(s): set() for s in SHARES}
    tape_identities = set()
    for share, label_seed, time_seed, family in product(
        SHARES, LABEL_SEEDS, TIME_SEEDS, FAMILIES
    ):
        proto = build_config(label_seed, 900, share, 7, 2, .5)
        tape = tape_with_random_times(proto, label_seed, time_seed, family)
        assert len(tape) == 60
        key = (share, label_seed, time_seed, family)
        assert key not in tape_identities
        tape_identities.add(key)
        checksum = hashlib.sha256(json.dumps(tape).encode()).hexdigest()
        assert checksum not in timehashes[str(share)]
        timehashes[str(share)].add(checksum)

        cfg = topology.config(label_seed, share)
        cp = topology.run(cfg, tape, checkpoint_at=84, trace=True)
        observation = prestate_snapshot(cp)

        for phi30, phi60 in OFFSETS:
            offset = (phi30, phi60)
            # Even the first arm cannot mutate the checkpoint used by the second.
            x = arm(cfg, tape, cp, 30, phi30)
            assert prestate_snapshot(cp) == observation, "first arm mutated checkpoint"
            y = arm(cfg, tape, cp, 60, phi60)
            assert prestate_snapshot(cp) == observation, "second arm mutated checkpoint"
            c0 = calendar_choice(offset)
            c1 = guard_choice(offset, observation)
            rows.append({
                "share": share, "label_seed": label_seed,
                "time_seed": time_seed, "family": family,
                "tape_sha256": checksum, "phi30": phi30, "phi60": phi60,
                "prestate": dict(observation),
                "arms": {"30": x, "60": y},
                "delta_cost": x["cost"] - y["cost"],
                "choices": {"calendar": c0, "guard": c1,
                            "fixed30": 30, "fixed60": 60},
            })
        print("FINISHED", share, label_seed, time_seed, family, flush=True)

    assert len(tape_identities) == 16 and len(rows) == 64
    assert all(len(hashes) == 8 for hashes in timehashes.values())
    assert set(time_seed for _, _, time_seed, _ in tape_identities) == set(TIME_SEEDS)
    assert all(sum((r["share"], r["label_seed"], r["time_seed"], r["family"]) == k
                   for r in rows) == 4 for k in tape_identities)

    pooled = summarize(rows)
    per_offset = {f"{a},{b}": summarize([
        r for r in rows if (r["phi30"], r["phi60"]) == (a, b)
    ]) for a, b in OFFSETS}
    per_share = {str(s): summarize([r for r in rows if r["share"] == s])
                 for s in SHARES}
    per_family = {f: summarize([r for r in rows if r["family"] == f])
                  for f in FAMILIES}

    group = defaultdict(list)
    for r in rows:
        group[(r["share"], r["label_seed"], r["time_seed"], r["family"])].append(r)
    compare = {"guard_better": 0, "calendar_better": 0, "equal": 0}
    for tape_rows in group.values():
        cr = sum(cost_regret(r, r["choices"]["calendar"]) for r in tape_rows)
        gr = sum(cost_regret(r, r["choices"]["guard"]) for r in tape_rows)
        compare["guard_better" if gr < cr else
                "calendar_better" if cr < gr else "equal"] += 1

    if pooled["guard_triggered"] == 0:
        status = "P139_UNINFORMATIVE_NO_TRIGGERS"
    else:
        bc = pooled["calendar"]["total_regret"]
        bg = pooled["guard"]["total_regret"]
        pass_agg = (bg == 0 if bc == 0 else bg <= .9 * bc)
        pass_strata = all(
            (
                group_result["guard"]["total_regret"] <= 1.1 *
                group_result["calendar"]["total_regret"]
                if group_result["calendar"]["total_regret"] > 0
                else group_result["guard"]["total_regret"] == 0
            )
            for group_result in (*per_share.values(), *per_family.values())
        )
        status = ("P139_PREDECLARED_PASS" if pass_agg and pass_strata
                  else "P139_PREDECLARED_FAIL")

    result = {
        "status": status, "prereg": "P139_PRESTATE_QUEUE_GUARD_PREREG.md",
        "simulator_arms": 128, "matched_policy_pairs": 64,
        "distinct_demand_tapes": 16, "time_seeds": list(TIME_SEEDS),
        "all_arms_cleared": True, "refusal_trace_audited_by_p136_arm": True,
        "feature_time": 84, "feature_source": "checkpoint_observation",
        "calendar": {f"{a},{b}": p for (a,b), p in CALENDAR.items()},
        "guard_thresholds": {"target_offset": [7,15],
                             "receiver_at_least": 3,
                             "upstream_plus_pocket_at_least": 6},
        "pooled": pooled, "by_offset": per_offset, "by_share": per_share,
        "by_family": per_family, "within_tape_regret": compare, "rows": rows,
        "limits": "Within same synthetic T2 model, no independent SUMO/field. "
                  "Queue observation is known at t84 inside model but physical "
                  "sensor feasibility unproven. Changing period and offset together."
    }
    (HERE / "P139_RESULT.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    )
    print("P139_RESULT", json.dumps(
        {k: result[k] for k in ("status", "pooled", "by_offset",
                                "by_share", "within_tape_regret")},
        ensure_ascii=False
    ), flush=True)
    return result


if __name__ == "__main__":
    main()
