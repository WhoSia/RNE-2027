"""Bound contrast from adjacent trajectory samples under a fixed simulated run."""
import json
from pathlib import Path


def bound(contrast, lag, lead, step):
    lower = contrast - lead["crossed"] * step
    upper = contrast + lag["crossed"] * step
    sign = "leading" if upper < 0 else "lagging" if lower > 0 else "ambiguous"
    return {"lower": lower, "upper": upper, "sign": sign}


def experiment(directory):
    nominal = json.loads((directory / "P40_RESULT.json").read_text())
    coarse = json.loads((directory / "P43_RESULT.json").read_text())
    rows = [
        (row["capacity"], row["closed"], .25, row["sumo_contrast"], row["sumo"])
        for row in nominal
    ] + [(row["capacity"], row["closed"], row["step"], row["contrast"], row["outcomes"])
         for row in coarse]
    return [
        {"capacity": cap, "closed": closed, "step": step, "contrast": contrast,
         **bound(contrast, *pair, step)}
        for cap, closed, step, contrast, pair in rows
    ]


if __name__ == "__main__":
    print(json.dumps(experiment(Path(__file__).parent), indent=2, sort_keys=True))
