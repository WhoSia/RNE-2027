"""Separate individual phase effects and evaluation-window sensitivity."""
import json

from p54_vehicle_mechanism import experiment as vehicles


def evaluate(rows, horizon):
    return {
        engine: sum(min(row["crossing_lag_lead"][engine][1], horizon)
                    - min(row["crossing_lag_lead"][engine][0], horizon)
                    for row in rows if row["scheduled"] < horizon)
        for engine in ("SUMO", "T2")
    }


def experiment():
    cases = []
    for offset in (0, 50):
        rows = vehicles(offset, include_observed=True)
        windows = {horizon: evaluate(rows, horizon) for horizon in (90, 120, 150, 180)}
        cases.append({"offset_s": offset, "vehicles": rows, "windows": windows,
                      "top_four_signed_gap": sum(row["gap"] for row in rows[:4]),
                      "net_gap": sum(row["gap"] for row in rows),
                      "fixed_cohort_size": len(rows)})
    return cases


if __name__ == "__main__":
    print(json.dumps(experiment(), indent=2, sort_keys=True))
