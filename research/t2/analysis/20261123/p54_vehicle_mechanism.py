"""Localize straight-vehicle differences in the closed receiver comparison."""
from collections import Counter
import json
from pathlib import Path
from tempfile import TemporaryDirectory

from p39_engine_bridge import t2_case
from p40_finite_link import sumo_run
from sumo_phase_pair import DEMAND, HORIZON

DENIALS = {"receiver_entry_cell_busy", "receiver_capacity_full"}


def experiment():
    with TemporaryDirectory() as directory:
        sumo = [sumo_run(Path(directory) / str(order), order, 2, True,
                         step_size=.125, movement_details=True) for order in (False, True)]
    t2 = [t2_case(order, 10, 2, receiver_mode="cells", receiver_closures=((0, 50),),
                  movement_details=True) for order in (False, True)]
    denied = [Counter(e["vehicle_id"] for e in arm["service_events"] if e["reason"] in DENIALS)
              for arm in t2]
    rows = []
    for i, v in enumerate(DEMAND):
        if v.movement != "T":
            continue
        crossing = {name: [arm["crossing_times"].get(v.ident, HORIZON) for arm in pair]
                    for name, pair in (("SUMO", sumo), ("T2", t2))}
        deltas = {name: lead - lag for name, (lag, lead) in crossing.items()}
        rows.append({"vehicle": v.ident, "scheduled": v.time, "crossing_lag_lead": crossing,
                     "delta": deltas, "gap": deltas["T2"] - deltas["SUMO"],
                     "t2_receiver_denials_lag_lead": [c[i] for c in denied]})
    return sorted(rows, key=lambda row: (-abs(row["gap"]), row["vehicle"]))


if __name__ == "__main__":
    print(json.dumps(experiment(), indent=2, sort_keys=True))
