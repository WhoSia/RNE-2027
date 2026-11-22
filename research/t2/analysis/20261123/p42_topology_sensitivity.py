"""Compare T2 pocket/headway sensitivity against the frozen SUMO grid."""
import json
from itertools import product
from pathlib import Path

from p39_engine_bridge import t2_case


def experiment(reference):
    rows = []
    for pocket, headway, base in product((10, 30, 95), (1, 2, 3), reference):
        lag, lead = (t2_case(order, pocket, base["capacity"], receiver_mode="cells",
                            receiver_headway=headway,
                            receiver_closures=((0, 50),) if base["closed"] else ())
                     for order in (False, True))
        contrast = lead["approach_vehicle_seconds"] - lag["approach_vehicle_seconds"]
        rows.append({
            "pocket": pocket, "headway": headway, "capacity": base["capacity"],
            "closed": base["closed"], "t2_contrast": contrast,
            "sumo_contrast": base["sumo_contrast"],
            "agrees": contrast * base["sumo_contrast"] > 0,
            "absolute_error": abs(contrast - base["sumo_contrast"]),
        })
    return rows


if __name__ == "__main__":
    reference = json.loads(Path(__file__).with_name("P40_RESULT.json").read_text())
    print(json.dumps(experiment(reference), indent=2, sort_keys=True))
