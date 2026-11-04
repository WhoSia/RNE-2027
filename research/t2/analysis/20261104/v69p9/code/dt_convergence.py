"""P9: numerical time-step convergence on UNCHANGED T2 v6.9-P2 model.
No traffic field validation or SUMO run claimed. Same paired arrivals per policy/dt.
"""
from __future__ import annotations
import argparse,csv,json,sys
from pathlib import Path
from dataclasses import replace
from itertools import combinations

ROOT=Path(__file__).resolve().parents[2]/'T2_P8_20261104/reference/T2_v69_P2'
if not ROOT.exists():
    # P9 archive can be reproduced beside an extracted P8 archive.
    ROOT=Path(__file__).resolve().parents[1]/'reference/T2_v69_P2'
if not ROOT.exists():
    raise SystemExit('Blocked: missing byte-identical original P2 source: '+str(ROOT))
sys.path.insert(0,str(ROOT))
from optimize import SCENARIOS,PLANS,arrivals_for,make_config
from corridor import run

DTS=(0.5,0.25)
SEEDS=(211,223)
STORAGES=(18.,60.)
HORIZON=1200.0

def one(plan, arr, storage, dt, horizon=HORIZON):
    c=replace(make_config(plan,storage,horizon_s=horizon),dt=dt)
    s=run(c,arr)['summary']
    if s['issues'] or s['generated'] != len(arr):
        raise AssertionError('simulation invariants failed')
    return {'objective':s['exposure_vehicle_seconds'],'unfinished':s['unfinished'],
            'generated':s['generated'],'completed':s['completed'],'issues':s['issues']}

def compare(rows):
    groups={}
    for r in rows:
        groups.setdefault((r['scenario'],r['storage_m'],r['seed']),{}).setdefault(r['dt'],{})[r['plan']]=r
    results=[];allpair=[]
    for key,data in sorted(groups.items()):
        x,y=(data[d] for d in DTS)
        assert x.keys()==y.keys() and len(x)==len(PLANS)
        best0=min(x,key=lambda p:(x[p]['objective'],p))
        best1=min(y,key=lambda p:(y[p]['objective'],p))
        diffs=[{'plan':p,'delta':y[p]['objective']-x[p]['objective']} for p in x]
        inversions=0; ties=0; num=0
        for a,b in combinations(sorted(x),2):
            d0=x[a]['objective']-x[b]['objective']
            d1=y[a]['objective']-y[b]['objective']
            if d0 == 0 or d1 == 0: ties+=1;continue
            num+=1
            if d0*d1<0:
                inversions+=1
                allpair.append({'scenario':key[0],'storage_m':key[1],'seed':key[2],'policy_a':a,'policy_b':b,
                                'dt05_a':x[a]['objective'],'dt05_b':x[b]['objective'],
                                'dt025_a':y[a]['objective'],'dt025_b':y[b]['objective']})
        results.append({'scenario':key[0],'storage_m':key[1],'seed':key[2],'best_dt05':best0,'best_dt025':best1,
                        'best_changed':best0!=best1,'strict_pairs':num,'pairs_with_ties':ties,'rank_reversals':inversions,
                        'mean_abs_exposure_difference':sum(abs(t['delta']) for t in diffs)/len(diffs),
                        'max_abs_exposure_difference':max(abs(t['delta']) for t in diffs),
                        'unfinished_at_05':sum(r['unfinished']>0 for r in x.values()),
                        'unfinished_at_025':sum(r['unfinished']>0 for r in y.values())})
    return results,allpair

def write_csv(file,rows):
    if not rows: return
    with open(file,'w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

def main(out,scenarios=SCENARIOS,seeds=SEEDS,storages=STORAGES,plans=PLANS):
    out=Path(out);out.mkdir(parents=True,exist_ok=True)
    rows=[]
    for s in scenarios:
        for st in storages:
            for seed in seeds:
                a=arrivals_for(s,seed)
                for p in plans:
                    for dt in DTS:
                        r=one(p,a,st,dt)
                        rows.append({'scenario':s.name,'storage_m':st,'seed':seed,'plan':str(p.key),
                                     'dt':dt,**r})
    stats,pairs=compare(rows)
    write_csv(out/'paired_dt_runs.csv',rows);write_csv(out/'cell_summary.csv',stats);write_csv(out/'pairwise_reversals.csv',pairs)
    summary={'conditions':len(stats),'executions':len(rows),'time_steps_s':DTS,'horizon_s':HORIZON,
             'best_policy_changed_cells':sum(int(x['best_changed']) for x in stats),
             'strict_pairwise_comparisons':sum(x['strict_pairs'] for x in stats),
             'strict_rank_reversals':len(pairs),
             'cells_with_any_inversions':sum(x['rank_reversals']>0 for x in stats),
             'any_censoring':sum(x['unfinished_at_05']+x['unfinished_at_025'] for x in stats),
             'mean_abs_exposure_difference_all_cells':sum(x['mean_abs_exposure_difference'] for x in stats)/len(stats)}
    (out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,indent=2))
    return summary
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,default=Path(__file__).resolve().parents[1]/'results')
    args=ap.parse_args();main(args.out)
