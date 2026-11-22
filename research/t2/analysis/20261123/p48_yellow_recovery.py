"""Retest driver-clock collision pairs with upstream amber restored."""
import json
from pathlib import Path
from tempfile import TemporaryDirectory

from p40_finite_link import SimulationCollision, sumo_run
from p44_crossing_bounds import bound


def experiment(failed, action_step=1.):
    rows = []
    with TemporaryDirectory() as directory:
        for i, case in enumerate(failed):
            step = case["step"]
            row = {"step": step, "capacity": case["capacity"], "closed": case["closed"]}
            pair = []
            for order in (False, True):
                try:
                    pair.append(sumo_run(Path(directory) / f"{i}-{order}", order,
                                         case["capacity"], case["closed"], step_size=step,
                                         action_step=action_step, yellow=True))
                except SimulationCollision:
                    pair.append(None)
            row["collision_arms"] = [name for name, arm in zip(("lagging", "leading"), pair)
                                     if arm is None]
            if not row["collision_arms"]:
                lag, lead = pair
                contrast = lead["approach_vehicle_seconds"] - lag["approach_vehicle_seconds"]
                row.update(contrast=contrast, **bound(contrast, lag, lead, step))
            rows.append(row)
    return rows


if __name__ == "__main__":
    upstream = json.loads(Path(__file__).with_name("P46_RESULT.json").read_text())
    print(json.dumps(experiment([r for r in upstream["rows"] if r["collision_arms"]]),
                     indent=2, sort_keys=True))
