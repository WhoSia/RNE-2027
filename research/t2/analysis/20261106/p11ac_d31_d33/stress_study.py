"""Predeclared synthetic demand stress and holdout. No fitting on the holdout."""
from __future__ import annotations
import sys,json,csv
from pathlib import Path
from collections import defaultdict
from statistics import mean
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'src'))
from policy_audit import compare,aggregate

def main():
    aggregate_rows=[];details=[]
    for demand,headway in [(18,3),(28,2),(40,1)]:
        rows,_=compare(seeds=(301,303,305,307),holdout=(401,403,405,407),horizon=260,n=demand,headway=headway)
        for r in rows:r['demand_label']=f'n{demand}_h{headway}'
        details.extend(rows)
        for r in aggregate(rows):r['demand_label']=f'n{demand}_h{headway}';aggregate_rows.append(r)
    (ROOT/'results/d33_stress.json').write_text(json.dumps({'cohorts':aggregate_rows,'per_seed':details},indent=2)+'\n')
    with (ROOT/'results/d33_stress.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(aggregate_rows[0]));w.writeheader();w.writerows(aggregate_rows)
    print(json.dumps(aggregate_rows,indent=2))
if __name__=='__main__':main()
