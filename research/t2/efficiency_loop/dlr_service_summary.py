"""Summarize overlapping queued samples at the signal-interval level."""
import argparse
from collections import defaultdict
import json
from pathlib import Path


def summarize(data):
    cycles = defaultdict(list)
    for block in data["blocks"]:
        for row in block["rows"]:
            cycles[block["block"],row["interval"]].append(row)
    rows = []
    for (block,interval), points in sorted(cycles.items()):
        # Each two-second window overlaps up to three neighboring windows.
        # Longest run below is elapsed span between sample starts, not delay.
        runs = [0]
        previous = None
        for row in points:
            t = row["from_first_green_s"]
            if row["through_or_unknown_2s"]:
                previous = None
                continue
            if previous is None or abs(t-previous-.5)>.001:
                runs.append(1)
            else:
                runs[-1] += 1
            previous = t
        rows.append({"block":block,"interval":interval,"queued_slots":len(points),
                     "slots_without_classified_through":sum(not r["through_2s"] for r in points),
                     "slots_without_through_or_unknown":sum(not r["through_or_unknown_2s"] for r in points),
                     "longest_no_through_or_unknown_run_slots":max(runs),
                     "last_queued_s":points[-1]["from_first_green_s"]})
    return rows


if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("input",type=Path)
    p.add_argument("output",type=Path)
    a=p.parse_args()
    a.output.write_text(json.dumps(summarize(json.loads(a.input.read_text())),indent=2)+"\n")
