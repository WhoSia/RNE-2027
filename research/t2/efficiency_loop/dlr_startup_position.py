"""Evaluate initial distance using the existing DLR startup cohort and split."""
from collections import defaultdict
from statistics import median


def fit_position(training):
    """Fit a common distance slope from within-rank variation in training."""
    groups = defaultdict(list)
    for row in training:
        midpoint = sum(row["crossing_s_bounds"]) / 2
        groups[row["rank"]].append((row["front_distance_m"], midpoint))
    rank_times = {rank: median(t for _, t in rows) for rank, rows in groups.items()}
    rank_distances = {rank: median(d for d, _ in rows) for rank, rows in groups.items()}
    centered = []
    for rows in groups.values():
        mean_d = sum(d for d, _ in rows) / len(rows)
        mean_t = sum(t for _, t in rows) / len(rows)
        centered.extend((d - mean_d, t - mean_t) for d, t in rows)
    variance = sum(d*d for d, _ in centered)
    slope = sum(d*t for d, t in centered) / variance if variance else 0.0
    overall = median(t for rows in groups.values() for _, t in rows)
    return slope, rank_times, rank_distances, overall


def predict_position(model, row):
    slope, rank_times, rank_distances, overall = model
    rank = row["rank"]
    baseline = rank_times.get(rank, overall)
    distance = row["front_distance_m"]
    centered = distance - rank_distances.get(rank, distance)
    return baseline, max(0.0, baseline + slope * centered)


def phase_loss_bounds(predictions):
    """Compare both predictions under one shared green onset per phase."""
    widths = [hi - lo for _, _, (lo, hi) in predictions]
    width = widths[0]
    if any(abs(w - width) > 1e-8 for w in widths):
        raise ValueError("Rows do not share a green onset bracket")
    offsets = {0.0, width}
    for baseline, position, (lo, _) in predictions:
        offsets.update(p - lo for p in (baseline, position) if 0 < p - lo < width)
    values = [sum(abs(position - (lo+dt)) - abs(baseline - (lo+dt))
                  for baseline, position, (lo, _) in predictions)
              for dt in offsets]
    return min(values), max(values)


def evaluate(data, *, rank_filter=None, omit_training_block=None):
    from dlr_startup_baseline import through_rows
    from field_replay import EVAL, TRAIN

    rows = [row for row in through_rows(data)
            if rank_filter is None or row["rank"] == rank_filter]
    training = [r for r in rows if r["block"] in TRAIN and r["block"] != omit_training_block]
    model = fit_position(training)
    outputs = {}
    for block in EVAL:
        block_rows = [r for r in rows if r["block"] == block]
        by_phase = defaultdict(list)
        for row in block_rows:
            baseline, position = predict_position(model, row)
            by_phase[row["interval"]].append((baseline, position, row["crossing_s_bounds"]))
        by_vehicle = [p for phase in by_phase.values() for p in phase]
        midpoints = [sum(bounds)/2 for _, _, bounds in by_vehicle]
        n = len(by_vehicle)
        phase_bounds = [phase_loss_bounds(phase) for phase in by_phase.values()]
        outputs[block] = {
            "vehicles": n,
            "phases": len(by_phase),
            "midpoint_rank_mae_s": sum(abs(p[0]-t) for p,t in zip(by_vehicle,midpoints))/n,
            "midpoint_position_mae_s": sum(abs(p[1]-t) for p,t in zip(by_vehicle,midpoints))/n,
            "position_minus_rank_mae_bounds_s": [sum(b[k] for b in phase_bounds)/n for k in (0,1)],
        }
    return {"training_vehicles": len(training), "slope_s_per_m": model[0],
            "rank_counts": {str(k): sum(r["rank"] == k for r in training) for k in model[1]},
            "evaluation_blocks": outputs}


if __name__ == "__main__":
    import argparse
    import json
    from pathlib import Path

    parser = argparse.ArgumentParser()
    parser.add_argument("cohort", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    result = evaluate(json.loads(args.cohort.read_text()))
    args.output.write_text(json.dumps(result, indent=2) + "\n")
