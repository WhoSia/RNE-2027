"""Build the offline exhibit from all eight continuations in an audited group."""
import argparse
import json
from pathlib import Path

from daypart_scenarios import worlds
from storage_information import BIN_STARTS, DECISION, matched_storage_cases

ROOT = Path(__file__).resolve().parent
DESIGN = (83, "night", "platooned", "constrained")
PREFIX = (1, 1, 0)


def example():
    seed, *expected = DESIGN
    scenario = next(w.scenario for w in worlds(seed)
                    if [w.band, w.shape, w.receiving] == expected)
    _, _, _, rows = next(group for group in matched_storage_cases(scenario)
                         if group[0] == "pocket")
    selected = [{"order": bits[len(PREFIX):], "area": area, "remaining": remaining}
                for bits, _, pocket, link, area, remaining in rows
                if bits[:len(PREFIX)] == PREFIX and (pocket, link) == (1, 0)]
    if len({row["order"] for row in selected}) != 8:
        raise ValueError("The exhibited information group must contain all eight continuations")
    return {"decision": DECISION, "starts": BIN_STARTS[len(PREFIX):], "cases": selected}


def render(data):
    template = (ROOT/"exhibition_demo.html").read_text(encoding="utf-8")
    return template.replace("__T2_DATA__", json.dumps(data, separators=(",", ":")))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    args.output.write_text(render(example()), encoding="utf-8")
