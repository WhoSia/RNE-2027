"""Extend the amber intervention beyond selected collision cases."""
import json
from itertools import product
from pathlib import Path

from p48_yellow_recovery import experiment


if __name__ == "__main__":
    nominal = json.loads(Path(__file__).with_name("P40_RESULT.json").read_text())
    cases = [dict(case, step=step) for case, step in product(nominal, (.125, .25))]
    rows = {name: experiment(cases, action_step=clock)
            for name, clock in (("default_clock", None), ("fixed_clock", 1.))}
    print(json.dumps(rows, indent=2, sort_keys=True))
