"""Compare the common and differential components of two-lane startup."""
import argparse
from collections import defaultdict
import json
from pathlib import Path
from statistics import median

from dlr_startup_baseline import through_rows


def compare(blocks):
    cycles = defaultdict(dict)
    for row in through_rows(blocks):
        if row["rank"] == 1:
            cycles[row["block"],row["interval"]][row["lane"]] = row
    pairs = []
    for (block,interval), lanes in sorted(cycles.items()):
        if set(lanes) != {-3,-4}:
            continue
        a,b = (lanes[lane]["crossing_s_bounds"] for lane in (-3,-4))
        if abs((a[1]-a[0])-(b[1]-b[0])) > 1e-8:
            raise ValueError("paired leaders must use the same onset bracket")
        pairs.append({"block":block,"interval":interval,
                      "mean_leader_time_bounds_s":[(x+y)/2 for x,y in zip(a,b)],
                      "lane_minus3_minus_minus4_s":a[0]-b[0],
                      "first_leader_bounds_s":[min(x,y) for x,y in zip(a,b)]})
    for r in pairs:
        peers = [q for q in pairs if q["block"]==r["block"] and q is not r]
        lower,upper = r["mean_leader_time_bounds_s"]
        r["same_block_peer_count"] = len(peers)
        r["definitely_later_than"] = sum(q["mean_leader_time_bounds_s"][1]<lower for q in peers)
        r["definitely_earlier_than"] = sum(q["mean_leader_time_bounds_s"][0]>upper for q in peers)
    return {"pairs":pairs,"median_abs_lane_gap_s":median(abs(r["lane_minus3_minus_minus4_s"]) for r in pairs)}


if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("input",type=Path)
    p.add_argument("output",type=Path)
    a=p.parse_args()
    a.output.write_text(json.dumps(compare(json.loads(a.input.read_text())),indent=2)+"\n")
