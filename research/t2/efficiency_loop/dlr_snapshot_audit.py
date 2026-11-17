"""Compare snapshot cohorts using uniquely matched observed crossing events."""
import argparse
from collections import defaultdict
import json
from pathlib import Path

from dlr_startup_baseline import through_rows
from dlr_startup_position import evaluate


def indexed(blocks):
    events = defaultdict(list)
    for row in through_rows(blocks):
        key = row["block"], row["interval"], *row["crossing_s_bounds"]
        events[key].append(row)
    return events


def compare(before, after):
    early, late = indexed(before), indexed(after)
    unique = {key for key in early.keys() & late.keys()
              if len(early[key]) == len(late[key]) == 1}
    aligned = {"before": [], "after": []}
    audit = {}
    for block in before:
        name = block["block"]
        keys = sorted(k for k in unique if k[0] == name)
        audit[name] = {
            "matched_events": len(keys),
            "before_only_or_ambiguous_rows": sum(len(v) for k,v in early.items()
                                                 if k[0] == name and k not in unique),
            "after_only_or_ambiguous_rows": sum(len(v) for k,v in late.items()
                                                if k[0] == name and k not in unique),
            "changed_lane_or_rank": sum(
                (early[k][0]["lane"], early[k][0]["rank"]) != (late[k][0]["lane"], late[k][0]["rank"])
                for k in keys),
        }
        for stage, events in (("before", early), ("after", late)):
            aligned[stage].append({"block": name, "rows": [events[k][0] for k in keys]})
    return {"coverage": audit, "matched_event_analysis": {
        stage: evaluate(blocks) for stage, blocks in aligned.items()}}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("before", type=Path)
    parser.add_argument("after", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    result = compare(json.loads(args.before.read_text()), json.loads(args.after.read_text()))
    args.output.write_text(json.dumps(result, indent=2) + "\n")
