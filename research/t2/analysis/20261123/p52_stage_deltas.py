"""Decompose phase-order costs over scheduled vehicles and event boundaries."""
import json
from pathlib import Path
from tempfile import TemporaryDirectory

from p39_engine_bridge import t2_case
from p40_finite_link import sumo_run
from sumo_phase_pair import DEMAND, HORIZON


def stages(arm):
    totals = {"left": [0, 0, 0], "through": [0, 0, 0]}
    for vehicle in DEMAND:
        stamps = [vehicle.time, *(arm[field].get(vehicle.ident, HORIZON)
                                  for field in ("admitted", "crossing_times", "released"))]
        if stamps != sorted(stamps) or stamps[-1] > HORIZON:
            raise ValueError(f"Invalid event ordering for {vehicle.ident}: {stamps}")
        key = "left" if vehicle.movement == "L" else "through"
        for i in range(3):
            totals[key][i] += stamps[i + 1] - stamps[i]
    return totals


def experiment():
    with TemporaryDirectory() as root:
        branches = {
            "SUMO": [sumo_run(Path(root) / str(order), order, 2, True, step_size=.125,
                              movement_details=True) for order in (False, True)],
            "T2": [t2_case(order, 10, 2, receiver_mode="cells", receiver_closures=((0, 50),),
                           movement_details=True) for order in (False, True)],
        }
    result = {}
    for engine, (lag, lead) in branches.items():
        earlier, later = stages(lag), stages(lead)
        result[engine] = {movement: [b - a for a, b in zip(earlier[movement], values, strict=True)]
                          for movement, values in later.items()}
        if sum(sum(values[:2]) for values in result[engine].values()) != (
            lead["approach_vehicle_seconds"] - lag["approach_vehicle_seconds"]
        ):
            raise ValueError("Stage costs do not reproduce the original approach contrast")
    return {"stages": ["insertion", "approach", "receiver"], "contrasts": result}


if __name__ == "__main__":
    print(json.dumps(experiment(), indent=2, sort_keys=True))
