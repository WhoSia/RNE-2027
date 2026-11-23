"""Prospective SUMO replication for four consecutive seeds after the pilot."""
import json
from collections import Counter
from p65_one_shot import compare


def direction(value):
    return "improved" if value < 0 else "worse" if value > 0 else "tie"


def experiment():
    seeds = range(402, 406)
    rows = compare(seeds)
    keys = {(r["seed"], r["demand"], r["turn"], r["family"]) for r in rows}
    if len(keys) != 32 or len(rows) != 32:
        raise ValueError("Incomplete or duplicated factorial block")
    counts = Counter((direction(r["delta60"]), direction(r["sumo_delta"])) for r in rows)
    return dict(rows=rows, counts={f"{t}/{s}": n for (t,s),n in sorted(counts.items())})


if __name__ == "__main__":
    print(json.dumps(experiment(), indent=2))
