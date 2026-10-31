"""Generate a small, paired exhibition scenario table from the finite-pocket baseline.

Inputs are representative synthetic signal settings, NOT measured Korean
intersection values. Run from repo root:
  python research/t2/exhibition_scenarios_v07.py
"""
from __future__ import annotations
from dataclasses import replace
from statistics import mean
import csv
from pathlib import Path
from exhibition_baseline_v07 import Scenario, arrivals, simulate

LENGTHS_M=(14.0,28.0,42.0,70.0)
LEFT_FRACTIONS=(.15,.30,.45)
PHASES=('leading','lagging')
SEEDS=tuple(range(10))
DURATION_S=3600

def study():
    rows=[]
    for p in LEFT_FRACTIONS:
        for seed in SEEDS:
            base=Scenario(duration_s=DURATION_S,left_fraction=p,seed=seed)
            fixed_stream=arrivals(base)
            for phase in PHASES:
                for length in LENGTHS_M:
                    c=replace(base,phase=phase,pocket_m=length)
                    result=simulate(c,fixed_stream)
                    rows.append({
                        'scenario':'SYNTHETIC_NOT_FIELD_CALIBRATED',
                        'seed':seed,'left_fraction':p,'phase':phase,
                        'pocket_m':length,'slots':result['pocket_capacity_veh'],
                        'arrivals':result['arrivals'],
                        'through_exits':result['through_exits'],
                        'left_exits':result['left_exits'],
                        'total_exits':result['total_exits'],
                        'remaining':result['remaining'],
                        'spillback_s':result['spillback_block_seconds'],
                        'spillback_during_through_green_s':result['spillback_during_through_green_s'],
                        'max_shared_queue':result['max_shared_queue'],
                        'max_pocket_queue':result['max_pocket_queue']})
    return rows

def main():
    rows=study()
    dest=Path(__file__).resolve().parent/'results'
    dest.mkdir(exist_ok=True)
    with (dest/'exhibition_baseline_v07.csv').open('w',newline='',encoding='utf-8') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    print('synthetic scenario records',len(rows))
    print('left_fraction,phase,length_m,mean_through,mean_total,mean_spillback_s')
    for p in LEFT_FRACTIONS:
        for phase in PHASES:
            for length in LENGTHS_M:
                z=[r for r in rows if r['left_fraction']==p and
                   r['phase']==phase and r['pocket_m']==length]
                print(p,phase,length,round(mean(r['through_exits'] for r in z),2),
                      round(mean(r['total_exits'] for r in z),2),
                      round(mean(r['spillback_s'] for r in z),2))

if __name__=='__main__':
    main()
