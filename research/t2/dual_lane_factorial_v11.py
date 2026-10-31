"""Two-through-lane, one-turn-pocket full factorial; matched route arrivals.

2 turning ratios * 8 seeds * 3 straight-lane-B splits * 2 lane-change
settings * 4 physical pocket lengths = 384 synthetic runs.
"""
from dataclasses import replace
from pathlib import Path
from statistics import mean
import csv,json
from dual_lane_v11 import DualConfig,run
from spatial_v10 import Config,arrivals

B_SHARES=(0.,.5,1.)
BAY_LENGTHS=(14.,28.,42.,70.)
TURN_RATIOS=(.3,.45)
SEEDS=tuple(range(8))

def experiment():
    rows=[]
    for turn_share in TURN_RATIOS:
        for seed in SEEDS:
            base=Config(seed=seed,left_fraction=turn_share)
            stream=arrivals(base)
            for B_share in B_SHARES:
                for changes in (False,True):
                    for pocket in BAY_LENGTHS:
                        c=DualConfig(base=replace(base,pocket_length_m=pocket),
                             through_B_share=B_share,allow_lane_changes=changes)
                        y=run(c,stream)
                        rows.append({"turn_share":turn_share,"seed":seed,
                             "B_share":B_share,"lane_change":changes,"pocket_m":pocket,
                             "arrivals":y["generated"],"through_exits":y["exit_S"],
                             "left_exits":y["exit_L"],"outside":y["outside"],
                             "lateral_changes":y["changes_A_to_B"],
                             "pocket_block_seconds":y["pocket_block_seconds"]})
    return rows

def summarize(rows):
    result=[]
    for turn_share in TURN_RATIOS:
        for B_share in B_SHARES:
            for changes in (False,True):
                for pocket in BAY_LENGTHS:
                    group=[r for r in rows if (r["turn_share"],r["B_share"],
                        r["lane_change"],r["pocket_m"])==(turn_share,B_share,changes,pocket)]
                    if len(group)!=len(SEEDS):raise AssertionError("incomplete design")
                    result.append({"turn_share":turn_share,"B_share":B_share,
                        "lane_change":changes,"pocket_m":pocket,
                        "mean_through_exits":mean(r["through_exits"] for r in group),
                        "mean_left_exits":mean(r["left_exits"] for r in group),
                        "mean_lateral_changes":mean(r["lateral_changes"] for r in group),
                        "mean_pocket_block_s":mean(r["pocket_block_seconds"] for r in group)})
    return result

if __name__=="__main__":
    rows=experiment();root=Path(__file__).resolve().parent/"results"
    root.mkdir(exist_ok=True)
    with (root/"dual_lane_factorial_384_v11.csv").open("w",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    (root/"dual_lane_summary_v11.json").write_text(json.dumps(summarize(rows),indent=2)+"\n")
    print("synthetic runs:",len(rows))
