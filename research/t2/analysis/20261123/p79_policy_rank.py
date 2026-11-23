"""Classify P76 policy ranks and attribute positive interactions to individual exits."""
from collections import Counter
import json
from pathlib import Path
from p78_capacity_event_timing import replay


def winner(delta):
    if delta == 0:
        return "tie"
    return "10s" if delta < 0 else "6s"


def experiment():
    transitions = Counter()
    cases = []
    for cell in json.loads(Path(__file__).with_name("P76_RESULT.json").read_text()):
        for ref in cell["rows"]:
            two, four = (ref[f"delta_capacity_{c}"] for c in (2, 4))
            transitions[winner(two) + "->" + winner(four)] += 1
            if four <= two:
                continue
            costs = Counter()
            movement = {}
            for cap, sign in ((2, -1), (4, 1)):
                arms, horizon = replay(cell, ref, cap)
                for arm, weight in zip(arms, (-sign, sign), strict=True):
                    for _, vehicle, turn in arm["crossing"]:
                        assert movement.setdefault(vehicle, turn) == turn
                    for t, vehicle in arm["departure"]:
                        costs[vehicle] -= weight * (horizon - t + 60)
            by_turn = Counter()
            vehicles = []
            for vehicle, cost in sorted(costs.items()):
                if cost:
                    turn = movement[vehicle]
                    by_turn[turn] += cost
                    vehicles.append([vehicle, turn, cost])
            assert sum(by_turn.values()) == four - two
            cases.append(dict(seed=ref["seed"], clock=cell["clock"], share=cell["share"],
                              contrast=four-two, by_turn=by_turn, vehicles=vehicles))
    return dict(transitions=transitions, positive_cases=cases)


if __name__ == "__main__":
    print(json.dumps(experiment(), indent=2))
