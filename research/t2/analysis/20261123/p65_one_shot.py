"""Replay P62 seed 401 against the P40 SUMO road with matched demand and clocks."""
import json
from itertools import groupby
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

import p40_finite_link as bridge
import sumo_phase_pair as network
from p39_policy_holdout import action, build_config, p31, tape_hash
from spatial_v10 import phase


def calendar(base, duration):
    windows = action(duration)
    codes = {"S": "Gr", "L": "rG", "-": "rr"}
    states = (codes[next((state for a, b, state in windows if a <= t < b),
                         phase(base, t))] for t in range(base.duration_s))
    return [(len(list(group)), state) for state, group in groupby(states)]


def compare():
    archived = json.loads(Path(__file__).with_name("P62_RESULT.json").read_text())["rows"]
    rows = []
    with TemporaryDirectory() as root:
        for row in archived:
            if row["seed"] != 401 or row["capacity"] != 4 or row["offset"] != 15:
                continue
            base = build_config(401, row["demand"], row["turn"], 14., 4, .5).base
            tape = p31.clock(base, row["family"])
            assert tape_hash(tape) == row["tape"]
            trips = tuple(network.Arrival(f"v{i:03}", t, "T" if m == "S" else "L")
                          for i, (t, m) in enumerate(tape))
            h = base.duration_s
            costs = []
            for d in (6, 10):
                with patch.multiple(network, DEMAND=trips, HORIZON=h), patch.multiple(
                        bridge, DEMAND=trips, HORIZON=h), patch.object(
                        network, "phases", return_value=calendar(base, d)):
                    result = bridge.sumo_run(Path(root)/f"{len(rows)}-{d}", False, 4, False,
                                             step_size=.25, receiver_offset=15, movement_details=True)
                exits = result["released"]
                costs.append(sum(exits.get(v.ident, h)-v.time for v in trips) + 60*(len(trips)-len(exits)))
            rows.append(dict(**row, sumo_costs=costs, sumo_delta=costs[1]-costs[0]))
    return rows


if __name__ == "__main__":
    print(json.dumps(compare(), indent=2))
