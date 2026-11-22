"""Test the stability of SUMO phase order under step-length changes."""
from itertools import product
import json
from pathlib import Path
from tempfile import TemporaryDirectory

from p40_finite_link import sumo_run


def experiment(reference, steps=(.5, 1.0)):
    rows = []
    with TemporaryDirectory() as directory:
        for i, (case, step_size) in enumerate(product(reference, steps)):
            outcomes = [sumo_run(Path(directory) / f"{i}-{order}", order, case["capacity"],
                                 case["closed"], step_size=step_size)
                        for order in (False, True)]
            lag, lead = outcomes
            contrast = lead["approach_vehicle_seconds"] - lag["approach_vehicle_seconds"]
            rows.append({"capacity": case["capacity"], "closed": case["closed"],
                         "step": step_size, "contrast": contrast,
                         "reference": case["sumo_contrast"], "outcomes": outcomes,
                         "agrees": contrast * case["sumo_contrast"] > 0})
    return rows


if __name__ == "__main__":
    data = json.loads(Path(__file__).with_name("P40_RESULT.json").read_text())
    print(json.dumps(experiment(data), indent=2, sort_keys=True))
