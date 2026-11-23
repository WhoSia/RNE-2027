"""Pair the intermediate storage condition with both P74 endpoints by tape."""
import json
from pathlib import Path
from p74_arrival_screen import screen


def experiment():
    previous = json.loads(Path(__file__).with_name("P74_RESULT.json").read_text())
    by_design = {(c["share"], c["clock"], c["capacity"]): c for c in previous}
    cells = screen((3,))
    for cell in cells:
        for capacity in (2, 4):
            reference = by_design[cell["share"], cell["clock"], capacity]["rows"]
            for row, old in zip(cell["rows"], reference, strict=True):
                assert (row["seed"], row["tape"]) == (old["seed"], old["tape"])
                row[f"delta_capacity_{capacity}"] = old["delta"]
    return cells


if __name__ == "__main__":
    print(json.dumps(experiment(), indent=2))
