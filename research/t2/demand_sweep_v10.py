"""Demand-regime screen for v1.0 spatial pocket model.

384 paired runs: 6 demand rates * 2 arrival patterns * 8 seeds * 4
physical pocket lengths. Synthetic scenarios, not measured field rates.
"""
from dataclasses import replace
from statistics import mean
from pathlib import Path
import csv,json
from spatial_v10 import Config,arrivals,simulate

RATES=(300,600,900,1200,1500,2100)
POCKETS=(14.,28.,42.,70.)

def evaluate():
    rows=[]
    for rate in RATES:
        for pattern in ("uniform","platoon"):
            for seed in range(8):
                base=Config(demand_vph=rate,seed=seed,arrival_pattern=pattern)
                stream=arrivals(base)
                for pocket in POCKETS:
                    y=simulate(replace(base,pocket_length_m=pocket),stream)
                    rows.append({"demand_vph":rate,"pattern":pattern,"seed":seed,"pocket_m":pocket,
                       "generated":y["generated"],"through_exits":y["exit_S"],
                       "left_exits":y["exit_L"],"outside_end":y["outside"],
                       "inside_end":y["remaining"]-y["outside"],
                       "pocket_block_seconds":y["blocked_pocket_entry_s"]})
    return rows

def summarize(rows):
    out=[]
    for rate in RATES:
        for pattern in ("uniform","platoon"):
            for pocket in POCKETS:
                g=[r for r in rows if r["demand_vph"]==rate and
                   r["pattern"]==pattern and r["pocket_m"]==pocket]
                if len(g)!=8:raise AssertionError("missing seed")
                out.append({"demand_vph":rate,"pattern":pattern,"pocket_m":pocket,
                    "mean_through_exits":mean(r["through_exits"] for r in g),
                    "mean_left_exits":mean(r["left_exits"] for r in g),
                    "mean_outside_end":mean(r["outside_end"] for r in g),
                    "mean_pocket_block_seconds":mean(r["pocket_block_seconds"] for r in g)})
    return out

if __name__=="__main__":
    rows=evaluate()
    out=Path(__file__).resolve().parent/"results"
    out.mkdir(exist_ok=True)
    with (out/"demand_sweep_384_v10.csv").open("w",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    (out/"demand_sweep_summary_v10.json").write_text(json.dumps(summarize(rows),indent=2)+"\n")
    print("synthetic runs:",len(rows))
