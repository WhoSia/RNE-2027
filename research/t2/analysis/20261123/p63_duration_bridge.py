"""Compare recurring 6/10-second greens on the fixed P56 arrival tape."""
import json
from itertools import product
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

import sumo_phase_pair
from p39_engine_bridge import Config, t2_case
from p40_finite_link import sumo_run


def compare():
    rows = []
    with TemporaryDirectory() as root:
        for capacity, offset in product((2, 4), (0, 15)):
            costs = {}
            for duration in (6, 10):
                schedule = ((24, "Gr"), (5, "rr"), (duration, "rG"), (31-duration, "rr"))
                with patch.object(sumo_phase_pair, "phases", return_value=schedule):
                    s = sumo_run(Path(root)/f"{capacity}-{offset}-{duration}", False,
                                 capacity, False, step_size=.125, receiver_offset=offset)
                def config(**kwargs):
                    return Config(**(kwargs | dict(left_green_s=duration)))
                with patch("p39_engine_bridge.Config", side_effect=config):
                    t = t2_case(False, 10, capacity, receiver_mode="cells", receiver_offset=offset)
                costs[duration] = dict(sumo=s["approach_vehicle_seconds"], t2=t["approach_vehicle_seconds"])
            delta = {key: costs[10][key]-costs[6][key] for key in costs[6]}
            rows.append(dict(capacity=capacity, offset=offset, costs=costs, delta=delta))
    return rows


if __name__ == "__main__":
    print(json.dumps(compare(), indent=2))
