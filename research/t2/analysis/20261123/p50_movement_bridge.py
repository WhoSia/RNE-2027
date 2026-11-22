"""Localize cross-engine cost discrepancies to scheduled movement cohorts."""
from itertools import product
import json
from pathlib import Path
from tempfile import TemporaryDirectory

from p39_engine_bridge import t2_case
from p40_finite_link import sumo_run
from sumo_phase_pair import DEMAND, HORIZON


def split(crossings):
    return {movement: sum(crossings.get(v.ident, HORIZON) - v.time
                          for v in DEMAND if v.movement == movement)
            for movement in ("L", "T")}


def experiment():
    rows = []
    with TemporaryDirectory() as root:
        for cap, closed in product((2, 4), (False, True)):
            row = {"capacity": cap, "closed": closed}
            sumo = [sumo_run(Path(root) / f"{cap}-{closed}-{order}", order, cap, closed,
                             step_size=.125, yellow=True, movement_details=True)
                    for order in (False, True)]
            t2 = [t2_case(order, 10, cap, receiver_mode="cells",
                          receiver_closures=((0, 50),) if closed else (),
                          movement_details=True) for order in (False, True)]
            for name, pair in (("sumo", sumo), ("t2", t2)):
                lag, lead = (split(arm["crossing_times"]) for arm in pair)
                row[name] = {movement: lead[movement] - lag[movement] for movement in ("L", "T")}
                if sum(row[name].values()) != (pair[1]["approach_vehicle_seconds"]
                                               - pair[0]["approach_vehicle_seconds"]):
                    raise ValueError("movement totals do not reproduce aggregate")
            rows.append(row)
    return rows


if __name__ == "__main__":
    print(json.dumps(experiment(), indent=2, sort_keys=True))
