"""Replay the discovery tape in SUMO and estimate strict reversal on new T2 tapes."""
import json
from dataclasses import replace
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

import p65_one_shot as adapter
from p69_fixed_budget import build_config, p31, run, schedule, score, tape_hash

DISCOVERY = "ee33978e44d4bb953ad049d92d212db911d778e7216db9bd73e2624a7f8f98a1"


def compare(seed, folder):
    base = build_config(seed, 900, .5, 7, 4, .5)
    tape = p31.clock(base.base, "platoon4")
    result = dict(seed=seed, tape=tape_hash(tape), t2=[])
    for offset in (0, 15):
        cfg = replace(base, downstream_offset_s=offset)
        cp = run(cfg, tape, checkpoint_at=84)
        costs = [score(run(cfg, tape, resume_from=cp, phase_overrides=schedule(d)), 60)
                 for d in (6, 10)]
        result["t2"].append(costs[1]-costs[0])
        if seed == 402:
            assert result["tape"] == DISCOVERY
            trips = tuple(adapter.network.Arrival(f"v{i:03}", t, "T" if m=="S" else "L")
                          for i,(t,m) in enumerate(tape))
            h = cfg.base.duration_s
            costs = []
            for d in (6,10):
                with patch.object(adapter, "action", schedule), patch.multiple(
                    adapter.network, DEMAND=trips, HORIZON=h, APPROACH_M=140,
                    phases=lambda *args, **kwargs: adapter.calendar(cfg.base,d)
                ), patch.multiple(adapter.bridge, DEMAND=trips, HORIZON=h):
                    events = adapter.bridge.sumo_run(folder/f"{offset}-{d}", False, 4, False,
                                step_size=.25, movement_details=True, receiver_offset=offset)
                exits = events["released"]
                costs.append(sum(exits.get(v.ident,h)-v.time for v in trips)+60*(len(trips)-len(exits)))
            result.setdefault("sumo", []).append(costs[1]-costs[0])
    return result


if __name__ == "__main__":
    with TemporaryDirectory() as root:
        rows = [compare(seed, Path(root)) for seed in (402, *range(701, 765))]
    if rows[0]["t2"] != [58,-109] or len({r["tape"] for r in rows}) != len(rows):
        raise ValueError("Discovery replay or unique tape check failed")
    print(json.dumps(rows, indent=2))
