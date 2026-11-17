"""Compare displacement and speed thresholds on the common observed clock."""
import argparse
import json
from pathlib import Path


def summarize(report):
    cases = {}
    for label, case in report["cases"].items():
        leaders = {}
        for lane, trace in case["leaders"].items():
            samples = [r for r in trace["samples"] if 0 <= r[0] <= trace["crossing_s"]]
            first_t, _, first_distance, _ = samples[0]
            leaders[lane] = {
                "first_sample_s": first_t,
                "first_front_distance_m": first_distance,
                "first_forward_displacement_s": {
                    str(distance): next((t for t, _, d, _ in samples
                                         if first_distance - d >= distance), None)
                    for distance in (.25, .5, 1.)
                },
                "first_over_2ms_s": next((t for t, v, _, _ in samples if v > 2), None),
                "center_crossing_s": trace["crossing_s"],
                "max_sample_gap_before_crossing_s": round(max(
                    (b[0] - a[0] for a, b in zip(samples, samples[1:])), default=0), 3),
            }
        last_crossing = max(row["center_crossing_s"] for row in leaders.values())
        cases[label] = {
            "leaders": leaders,
            "left_queue_detections_before_last_crossing": [
                r for r in case["queues"] if 0 <= r[0] <= last_crossing and r[1] in (-1,-2) and r[2] > 0],
            "west_positive_slots_before_last_crossing": [
                r for r in case["outlet_ticks"] if 0 <= r[0] <= last_crossing and any(n for n, _ in r[1])],
        }
    return cases


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("timeline", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    args.output.write_text(json.dumps(summarize(json.loads(args.timeline.read_text())), indent=2) + "\n")
