"""Select review intervals and write a clean sheet plus a separate answer key."""
import argparse
import csv
from datetime import timedelta
import json
from pathlib import Path

from dlr_path_cases import CLOCK

UNRESOLVED = "unresolved_movement_ahead_of_through"
CONTROL = "slow_through_ahead_of_through_control"


def select(report):
    cases = []
    for filename, block in report.items():
        baseline = block["results"]["2"]
        pool = baseline[CONTROL]["green"]["longest_runs"][:]
        for target in baseline[UNRESOLVED]["green"]["longest_runs"]:
            # Review segments close in time are redundant for the visual queue check.
            if any(name == filename and kind == UNRESOLVED
                   and abs(row["clock_start_s"]-target["clock_start_s"]) < 2
                   for name, row, kind in cases):
                continue
            if not pool:
                break
            comparison = min(pool,key=lambda r: abs(r["clock_start_s"]-target["clock_start_s"]))
            pool.remove(comparison)
            cases.extend([(filename,target,UNRESOLVED),(filename,comparison,CONTROL)])
    return sorted(cases,key=lambda item:(item[0],item[1]["clock_start_s"],item[1]["lane"]))


def write_sheet(report, sheet, key):
    keys = {}
    with sheet.open("w",newline="",encoding="utf-8") as stream:
        writer = csv.writer(stream, lineterminator="\n")
        writer.writerow(["case","lane","leader_s_m","follower_s_m","focus_start_utc","focus_end_utc","replay_from_utc",
                         "replay_until_utc","leader_movement","follower_movement",
                         "cannot_advance","lead_or_lane_change","downstream_space",
                         "signal_for_follower","tracking_gap","judgment","evidence"])
        for i,(filename,row,bucket) in enumerate(select(report),1):
            ident = f"K047-{i:02}"
            a,b = row["clock_start_s"],row["clock_end_s"]
            times = [(CLOCK+timedelta(seconds=t)).isoformat(timespec="milliseconds")
                     for t in (a,b,a-4,b+8)]
            writer.writerow([ident,row["lane"],row["leader_s_m"],row["follower_s_m"],*times,*([""]*9)])
            keys[ident] = {"trajectory_file":filename, "automatic_bucket":bucket,
                           "scope":"green per head 3 brackets; route control is not a manual label"}
    key.write_text(json.dumps(keys,indent=2)+"\n",encoding="utf-8")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    for name in ("report","sheet","key"):
        parser.add_argument(name,type=Path)
    args = parser.parse_args()
    write_sheet(json.loads(args.report.read_text()),args.sheet,args.key)
