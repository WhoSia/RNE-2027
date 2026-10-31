"""v1.0 matched update-order stress: 768 runs and all per-seed deltas."""
from dataclasses import replace
from pathlib import Path
from statistics import mean
import json,csv
from spatial_v10 import Config,arrivals,simulate

def evaluate():
    rows=[]
    for pattern in ("uniform","platoon"):
        for share in (.15,.30,.45):
            for seed in range(8):
                base=Config(seed=seed,left_fraction=share,arrival_pattern=pattern)
                stream=arrivals(base)
                for phase in ("leading","lagging"):
                    for length in (14.,28.,42.,70.):
                        for update in ("sequential","parallel"):
                            r=simulate(replace(base,phase_order=phase,pocket_length_m=length,
                                update_mode=update),stream)
                            rows.append({"pattern":pattern,"share":share,"seed":seed,
                                "phase":phase,"pocket_m":length,"update":update,
                                "through_exits":r["exit_S"],"left_exits":r["exit_L"],
                                "external":r["outside"],"pocket_block_s":r["blocked_pocket_entry_s"]})
    return rows

def summarize(rows):
    lookup={(r["pattern"],r["share"],r["seed"],r["phase"],r["pocket_m"],r["update"]):r
             for r in rows}
    if len(lookup)!=len(rows):raise ValueError("duplicate factorial cells")
    results=[]
    for pattern in ("uniform","platoon"):
        for share in (.15,.30,.45):
            for phase in ("leading","lagging"):
                for length in (14.,28.,42.,70.):
                    differences=[]
                    for seed in range(8):
                        key=(pattern,share,seed,phase,length)
                        differences.append(lookup[key+("parallel",)]["through_exits"]-
                                           lookup[key+("sequential",)]["through_exits"])
                    results.append({"pattern":pattern,"share":share,"phase":phase,
                         "pocket_m":length,"paired_deltas":differences,
                         "mean_parallel_minus_sequential":mean(differences),
                         "min":min(differences),"max":max(differences)})
    return results

if __name__=="__main__":
    rows=evaluate()
    p=Path(__file__).resolve().parent/"results"
    p.mkdir(exist_ok=True)
    with (p/"update_768_v10.csv").open("w",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    (p/"update_summary_v10.json").write_text(json.dumps(summarize(rows),indent=2)+"\n")
    print(len(rows),"runs")
