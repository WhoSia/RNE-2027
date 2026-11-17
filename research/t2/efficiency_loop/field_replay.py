"""Through-only replay against the seven previously opened DLR-UT windows."""
import argparse
from bisect import bisect_right
from collections import Counter
import csv
from datetime import datetime
from hashlib import file_digest
from itertools import product
import json
from math import ceil, floor
from pathlib import Path
from statistics import median

ORIGIN = datetime.fromisoformat("2023-09-24T12:00:00+00:00")
TRAIN = ("1100", "1215", "1230", "1445")
EVAL = ("1530", "1545", "1600")
STEP = 2  # half-seconds
START, END = 120, 780  # arrival cohort, with first two minutes available to warm up


def load(root, block):
    if block not in TRAIN + EVAL:
        raise ValueError("block is outside the opened data")
    hour, minute = int(block[:2]), int(block[2:])
    start = (hour - 12) * 3600 + minute * 60
    tracks = root / "week1" / "wide" / block / "daylight_crossings.csv"
    signals = root / "day" / f"day{block}_signals.csv"
    counts = Counter()
    vehicles = []
    with tracks.open(newline="") as stream:
        for row in csv.DictReader(stream):
            stop = float(row["stop"]) - start
            if not 0 <= stop < 900:
                continue
            kind = row["movement"] or "unclassified"
            counts[kind] += 1
            if kind == "through" and row["arrival"]:
                arrival = float(row["arrival"]) - start
                if 0 <= arrival <= stop:
                    vehicles.append((arrival, stop))
    samples = []
    with signals.open(newline="") as stream:
        for row in csv.DictReader(stream):
            if row["id"] == "3":
                t = (datetime.fromisoformat(row["timestamp"]) - ORIGIN).total_seconds() - start
                samples.append((t, int(row["state"]) in (5, 6)))
    samples.sort()
    times = tuple(t for t, _ in samples)
    if not samples or any(b <= a for a, b in zip(times, times[1:])):
        raise ValueError("missing or unordered samples")
    transitions = []
    gaps = []
    onset = None
    for (t0, g0), (t1, g1) in zip(samples, samples[1:]):
        if not g0 and g1:
            onset = t0, t1
        elif g0 and not g1 and onset:
            a0, a1 = onset
            left = bisect_right(times,a0) - 1
            right = bisect_right(times,t1)
            gap = max(b-a for a,b in zip(times[left:right-1],times[left+1:right]))
            if gap <= 2.05:
                transitions.append((a0, a1, t0, t1))
                gaps.append(gap)
            onset = None
    if not transitions:
        raise ValueError("no fully bracketed green intervals")
    hashes = {}
    for file in (tracks, signals):
        with file.open("rb") as stream:
            hashes[str(file.relative_to(root))] = file_digest(stream, "sha256").hexdigest()
    return tuple(sorted(vehicles)), tuple(transitions), tuple(gaps), dict(counts), hashes


def slots(transitions, timing, startup, headway):
    result = []
    for a0, a1, b0, b1 in transitions:
        begin, end = {"narrow": (a1, b0), "middle": ((a0+a1)/2, (b0+b1)/2),
                      "wide": (a0,b1)}[timing]
        result.extend(range(ceil(begin * STEP) + startup, floor(end * STEP) + 1, headway))
    return result


def predict(vehicles, departures, travel):
    out = []
    next_index = 0
    for a, b in vehicles:
        ready = ceil(a * STEP) + travel
        next_index = bisect_right(departures, ready - 1, lo=next_index)
        prediction = None if next_index == len(departures) else departures[next_index] / STEP
        next_index += prediction is not None
        out.append((a, b, prediction))
    return out


def metrics(predictions, transitions):
    rows = [(b, c) for a,b,c in predictions if START <= a < END]
    if not rows:
        raise ValueError("empty arrival cohort")
    errors = [c-b for b,c in rows if c is not None]
    penalty = 180  # explicit loss for a model departure unresolved in the block
    green = [(a1,b0) for _,a1,b0,_ in transitions if START <= a1 and b0 < END]
    counts = [(sum(a <= b <= z for b,c in rows),
               sum(c is not None and a <= c <= z for b,c in rows)) for a,z in green]
    return {"n": len(rows), "predicted": len(errors),
            "mae_if_predicted": sum(map(abs, errors))/len(errors) if errors else None,
            "signed_error_if_predicted": sum(errors)/len(errors) if errors else None,
            "penalized_absolute_sum": sum(map(abs, errors)) + penalty*(len(rows)-len(errors)),
            "green_windows": len(green), "window_count_abs_sum": sum(abs(a-b) for a,b in counts),
            "observed_in_windows": sum(a for a,b in counts),
            "predicted_in_windows": sum(b for a,b in counts)}


def calibrate(root):
    blocks = {w: load(root,w) for w in TRAIN}

    def green_filter(block, limit):
        return tuple(g for g,gap in zip(block[1],block[2]) if gap <= limit)

    def fit(limit):
        datasets = [(block[0], green_filter(block,limit)) for block in blocks.values()]
        candidates = []
        for travel, startup, headway in product(range(10,23,2), range(0,7,2), range(1,8)):
            score = sum(metrics(predict(v, slots(g,"middle",startup,headway),travel),g)
                        ["penalized_absolute_sum"] for v,g in datasets)
            candidates.append((score,travel,startup,headway))
        return min(candidates)

    strict = fit(1.2)
    medium = fit(2.05)
    score,travel,startup,headway = strict
    constant = median(b-a for v,*_ in blocks.values() for a,b in v if START <= a < END)
    blocks.update((w,load(root,w)) for w in EVAL)
    result = {"train": TRAIN, "evaluation": EVAL, "grid_candidates_per_fit": 196,
              "fit_seconds": {"travel": travel/STEP, "startup": startup/STEP,
                              "aggregate_headway": headway/STEP, "constant_lag": constant},
              "fit_2_05_seconds": dict(zip(("train_loss","travel","startup","aggregate_headway"),
                                          (medium[0], *(x/STEP for x in medium[1:])))),
              "train_loss": score, "blocks": {}}
    for name, block in blocks.items():
        vehicles, all_green, gaps, counts, hashes = block
        g = green_filter(block,1.2)
        result["blocks"][name] = {
            "observed_stop_crossings": counts,
            "matched_through": len(vehicles),
            "complete_green_intervals": {"1.2s_gap": len(g), "2.05s_gap": len(all_green)},
            "extra_max_gaps_s": [round(gap,3) for gap in gaps if gap > 1.2],
            "inputs_sha256": hashes,
            "bracket_sensitivity": {
                mode: metrics(predict(vehicles, slots(g,mode,startup,headway),travel),g)
                for mode in ("narrow","middle","wide")},
            "gap_sensitivity_same_fit": {
                mode: metrics(predict(vehicles, slots(all_green,mode,startup,headway),travel),g)
                for mode in ("narrow","middle","wide")},
            "gap_sensitivity_refit": metrics(
                predict(vehicles, slots(all_green,"middle",medium[2],medium[3]),medium[1]),g),
            "constant_lag": metrics([(a,b,a+constant) for a,b in vehicles],g),
            "constant_free_flow": metrics([(a,b,a+travel/STEP) for a,b in vehicles],g),
            "green_compatibility_matched_through": {
                "certain": sum(any(a1 <= b <= b0 for _,a1,b0,_ in g) for a,b in vehicles if START <= a < END),
                "possible": sum(any(a0 <= b <= b1 for a0,_,_,b1 in g) for a,b in vehicles if START <= a < END),
                "possible_2_05_gap": sum(any(a0 <= b <= b1 for a0,_,_,b1 in all_green)
                                         for a,b in vehicles if START <= a < END)},
        }
    return result


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("input", type=Path)
    p.add_argument("output", type=Path)
    a = p.parse_args()
    a.output.write_text(json.dumps(calibrate(a.input), indent=2) + "\n")
