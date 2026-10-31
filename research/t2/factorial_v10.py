"""v1.0 spatial model: predeclared full 384-run factorial with matched arrivals.

2 arrival patterns * 3 turning shares * 8 seeds * 2 protected orders
* 4 physical pocket lengths. Writes all cells and per-seed contrasts.
"""
from dataclasses import replace
from pathlib import Path
from statistics import mean
from collections import defaultdict
import csv,json,hashlib
from spatial_v10 import Config,arrivals,simulate

SEEDS=range(8)
LENGTHS=(14.,28.,42.,70.)
SHARES=(.15,.30,.45)
PHASES=("leading","lagging")
PATTERNS=("uniform","platoon")

def evaluate():
    rows=[]
    for pattern in PATTERNS:
        for share in SHARES:
            for seed in SEEDS:
                base=Config(seed=seed,left_fraction=share,arrival_pattern=pattern)
                stream=arrivals(base)
                digest=hashlib.sha256(repr(stream).encode("utf8")).hexdigest()
                for order in PHASES:
                    for length in LENGTHS:
                        cfg=replace(base,phase_order=order,pocket_length_m=length)
                        y=simulate(cfg,stream)
                        rows.append({"pattern":pattern,"share":share,"seed":seed,
                            "phase":order,"pocket_m":length,"stream_sha256":digest,
                            "through_exits":y["exit_S"],"left_exits":y["exit_L"],
                            "generated":y["generated"],"outside":y["outside"],
                            "blocked_pocket_s":y["blocked_pocket_entry_s"],
                            "blocked_through_green_s":y["pocket_block_during_S_green_s"],
                            "end_inside":y["remaining"]-y["outside"]})
    return rows

def contrasts(rows):
    groups=defaultdict(dict)
    for r in rows:
        key=(r["pattern"],r["share"],r["phase"],r["seed"])
        if r["pocket_m"] in groups[key]:raise ValueError("duplicate cell")
        groups[key][r["pocket_m"]]=r
    out=[]
    for pattern in PATTERNS:
        for share in SHARES:
            for order in PHASES:
                for lo,hi in zip(LENGTHS,LENGTHS[1:]):
                    d=[groups[(pattern,share,order,seed)][hi]["through_exits"]-
                       groups[(pattern,share,order,seed)][lo]["through_exits"] for seed in SEEDS]
                    out.append({"pattern":pattern,"share":share,"phase":order,
                        "from_m":lo,"to_m":hi,"per_seed_delta":d,
                        "mean_delta":mean(d),"min_delta":min(d),"max_delta":max(d)})
    return out

if __name__=="__main__":
    p=Path(__file__).resolve().parent/"results"
    p.mkdir(exist_ok=True)
    rows=evaluate()
    with (p/"factorial_384_v10.csv").open("w",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    summary={"status":"SYNTHETIC_NOT_CALIBRATED","n":len(rows),
        "contrasts":contrasts(rows),
        "caution":"Simulation seeds are not independent real-world intersections."}
    (p/"contrasts_v10.json").write_text(json.dumps(summary,indent=2)+"\n")
    print("runs",len(rows))
