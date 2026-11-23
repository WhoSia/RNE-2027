"""Evaluate paired P71 policy costs in SUMO, with ties assigned to six seconds."""
import json
from pathlib import Path
from statistics import mean

root = Path(__file__).resolve().parent
rows = json.loads((root / "P71_RESULT.json").read_text())
assert sorted(row["seed"] for row in rows) == list(range(701, 765))
results = {}
for index, offset in enumerate((0, 15)):
    costs = [row["sumo"][index] for row in rows]
    policies = {
        "fixed6": [False] * len(rows),
        "fixed10": [True] * len(rows),
        "transfer": [row["t2"][index] < 0 for row in rows],
        "offset_holdout": [sum(costs) - cost < 0 for cost in costs],
        "oracle": [cost < 0 for cost in costs],
    }
    results[offset] = {}
    for name, choices in policies.items():
        realized = [cost if choose else 0 for cost, choose in zip(costs, choices)]
        regret = [value - min(0, cost) for value, cost in zip(realized, costs)]
        assert min(regret) >= 0
        results[offset][name] = dict(mean_delta_vs_6=mean(realized),
                                     mean_regret=mean(regret), ten_count=sum(choices),
                                     optimal_fraction=regret.count(0) / len(rows))
print(json.dumps(results, indent=2))
