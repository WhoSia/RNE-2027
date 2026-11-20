"""Build the offline exhibit from all eight continuations in an audited group."""
import argparse
import json
from pathlib import Path
from fractions import Fraction

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


def exact_queries(cases, penalty, available):
    """Choose a zero-regret query tree, minimizing depth and then total questions."""
    deltas = [row["area"] + penalty * row["remaining"] for row in cases]
    if min(deltas) >= 0 or max(deltas) <= 0:
        return {"depth": 0, "total": 0, "order": "left" if max(deltas) <= 0 else "through"}

    alternatives = []
    for index in available:
        groups = [[row for row in cases if row["order"][index] == bit] for bit in (0, 1)]
        if not all(groups):
            continue
        remaining = tuple(i for i in available if i != index)
        branches = [exact_queries(group, penalty, remaining) for group in groups]
        alternatives.append({
            "question": index,
            "depth": 1 + max(branch["depth"] for branch in branches),
            "total": len(cases) + sum(branch["total"] for branch in branches),
            "branches": branches,
        })
    return min(alternatives, key=lambda tree: (tree["depth"], tree["total"], tree["question"]))


def query_report(data):
    report = {}
    for penalty in (0, 60, 120):
        tree = exact_queries(data["cases"], penalty, tuple(range(len(data["starts"]))))
        report[penalty] = {"tree": tree, "mean_questions_equal_weight":
                           str(Fraction(tree["total"], len(data["cases"])))}
    return report


def render(data):
    template = (ROOT/"exhibition_demo.html").read_text(encoding="utf-8")
    payload = {**data, "queries": query_report(data)}
    return template.replace("__T2_DATA__", json.dumps(payload, separators=(",", ":")))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    parser.add_argument("--queries", type=Path)
    args = parser.parse_args()
    data = example()
    args.output.write_text(render(data), encoding="utf-8")
    if args.queries:
        args.queries.write_text(json.dumps(query_report(data), indent=2)+"\n", encoding="utf-8")
