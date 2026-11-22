"""Locate persistent disagreement at the insertion, crossing and release boundaries."""
import json
from pathlib import Path
from tempfile import TemporaryDirectory

from p39_engine_bridge import t2_case
from p40_finite_link import sumo_run
from sumo_phase_pair import HORIZON


def experiment():
    with TemporaryDirectory() as root:
        pairs = {
            "SUMO": [sumo_run(Path(root) / str(order), order, 2, True, step_size=.125,
                              movement_details=True, receiver_offset=50) for order in (False, True)],
            "T2": [t2_case(order, 10, 2, receiver_mode="cells", receiver_closures=((0, 50),),
                           movement_details=True, receiver_offset=50) for order in (False, True)],
        }
    rows = []
    for ident in ("v02", "v03", "v05"):
        row = {"vehicle": ident}
        for engine, pair in pairs.items():
            stamps = [[arm[field].get(ident) for field in ("admitted", "crossing_times", "released")]
                      for arm in pair]
            differences = [None if a is None or b is None else b - a
                           for a, b in zip(*stamps, strict=True)]
            row[engine] = {"lag_lead_times": stamps, "boundary_deltas": differences,
                           "censored_crossing_delta": (
                               (stamps[1][1] if stamps[1][1] is not None else HORIZON)
                               - (stamps[0][1] if stamps[0][1] is not None else HORIZON)
                           )}
        rows.append(row)
    return {"boundaries": ["insert", "cross", "release"], "vehicles": rows}


if __name__ == "__main__":
    print(json.dumps(experiment(), indent=2, sort_keys=True))
