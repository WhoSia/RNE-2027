"""Check whether the intermediate capacity's policy contrast lies between endpoints."""
import json
from pathlib import Path


def summarize(cells):
    findings = []
    for cell in cells:
        below = []
        above = []
        matches_two = 0
        distinct_endpoints = 0
        for row in cell["rows"]:
            low, high = sorted((row["delta_capacity_2"], row["delta_capacity_4"]))
            if low != high:
                distinct_endpoints += 1
                matches_two += row["delta"] == row["delta_capacity_2"]
            if row["delta"] < low:
                below.append(row["seed"])
            elif row["delta"] > high:
                above.append(row["seed"])
        findings.append(dict(share=cell["share"], clock=cell["clock"],
                             pairs=len(cell["rows"]), distinct_endpoints=distinct_endpoints,
                             matches_two_when_distinct=matches_two, below=below, above=above))
    return findings


if __name__ == "__main__":
    archive = Path(__file__).with_name("P76_RESULT.json")
    print(json.dumps(summarize(json.loads(archive.read_text())), indent=2))
