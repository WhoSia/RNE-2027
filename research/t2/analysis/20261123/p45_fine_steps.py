"""Check finer SUMO steps using the same observation bounds."""
import json
from pathlib import Path

from p43_resolution_audit import experiment
from p44_crossing_bounds import bound


if __name__ == "__main__":
    nominal = json.loads(Path(__file__).with_name("P40_RESULT.json").read_text())
    rows = experiment(nominal, (.125,))
    for row in rows:
        row.update(bound(row["contrast"], *row["outcomes"], row["step"]))
    print(json.dumps(rows, indent=2, sort_keys=True))
