"""Compare fixed-lane phase contrasts across matched downstream calendars."""
import json
from pathlib import Path
from tempfile import TemporaryDirectory

from p39_engine_bridge import t2_case
from p40_finite_link import sumo_run
from p44_crossing_bounds import bound
from p50_movement_bridge import split


def experiment():
    step = .125
    rows = []
    with TemporaryDirectory() as root:
        for offset in range(0, 60, 10):
            sumo = [sumo_run(Path(root) / f"{offset}-{order}", order, 2, True,
                             step_size=step, movement_details=True, receiver_offset=offset)
                    for order in (False, True)]
            t2 = [t2_case(order, 10, 2, receiver_mode="cells", receiver_closures=((0, 50),),
                          movement_details=True, receiver_offset=offset)
                  for order in (False, True)]
            row = {"offset_s": offset}
            for name, pair in (("sumo", sumo), ("t2", t2)):
                lag, lead = pair
                through = split(lead["crossing_times"])["T"] - split(lag["crossing_times"])["T"]
                total = lead["approach_vehicle_seconds"] - lag["approach_vehicle_seconds"]
                row[name] = {"through": through, "total": total}
                if name == "sumo":
                    row[name]["total_bounds"] = bound(total, lag, lead, step)
            rows.append(row)
    return rows


if __name__ == "__main__":
    print(json.dumps(experiment(), indent=2, sort_keys=True))
