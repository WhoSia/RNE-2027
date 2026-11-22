"""Compare integration steps with a fixed driver clock, retaining failed cases."""
from itertools import product
import json
from pathlib import Path
from tempfile import TemporaryDirectory

from p40_finite_link import SimulationCollision, sumo_run
from p44_crossing_bounds import bound


def experiment(nominal):
    rows = []
    with TemporaryDirectory() as directory:
        for i, (case, step) in enumerate(product(nominal, (.125, .25, .5, 1.))):
            row = {"capacity": case["capacity"], "closed": case["closed"], "step": step}
            arms = []
            for order in (False, True):
                try:
                    arms.append(sumo_run(Path(directory) / f"{i}-{order}", order,
                                         case["capacity"], case["closed"], step_size=step,
                                         action_step=1.))
                except SimulationCollision:
                    arms.append(None)
            row["collision_arms"] = [name for name, arm in zip(("lagging", "leading"), arms)
                                     if arm is None]
            if not row["collision_arms"]:
                lag, lead = arms
                contrast = lead["approach_vehicle_seconds"] - lag["approach_vehicle_seconds"]
                row.update(contrast=contrast, **bound(contrast, lag, lead, step))
            rows.append(row)
    return {"action_step": 1.0, "rows": rows}


if __name__ == "__main__":
    nominal = json.loads(Path(__file__).with_name("P40_RESULT.json").read_text())
    print(json.dumps(experiment(nominal), indent=2, sort_keys=True))
