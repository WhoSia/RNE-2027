"""Out-of-design stochastic replication of the closest two signal policies.
Seeds are prelisted and differ from the 4 discovery seeds. Synthetic only.
"""
import csv, json, math, statistics
from pathlib import Path
from network_v51 import DEMANDS, make_arrivals, simulate
from experiment_v50 import plan
from experiment_v51 import TURN_VARIANTS
ROOT=Path(__file__).resolve().parent
SEEDS=tuple(range(101,149))
TURN_KEYS=('equal_2s','turn_stress')


def experiment():
    rows=[]
    demand=DEMANDS[0]
    for seed in SEEDS:
        arrivals=make_arrivals(demand,seed,arrive_until=320.)
        for turn_name in TURN_KEYS:
            params=TURN_VARIANTS[turn_name]
            obs={}
            for offset in ('zero','progression'):
                s=simulate(plan(38,offset),arrivals,horizon=580.,turns=params)['summary']
                obs[offset]=s
            rows.append({'seed':seed,'turn_model':turn_name,
                'g38_zero_vehicle_seconds':obs['zero']['system_vehicle_seconds_in_horizon'],
                'g38_progression_vehicle_seconds':obs['progression']['system_vehicle_seconds_in_horizon'],
                'delta_progression_minus_zero':obs['progression']['system_vehicle_seconds_in_horizon']-obs['zero']['system_vehicle_seconds_in_horizon'],
                'completed_zero':obs['zero']['completed'],
                'completed_progression':obs['progression']['completed']})
    path=ROOT/'heldout_paired_offsets.csv'
    with path.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    by={}
    for name in TURN_KEYS:
        deltas=[r['delta_progression_minus_zero'] for r in rows if r['turn_model']==name]
        n=len(deltas)
        mean=statistics.mean(deltas);sd=statistics.stdev(deltas)
        # 95% Student-t interval, df=47, t_crit approx 2.012 (rounded).
        radius=2.012*sd/math.sqrt(n)
        by[name]={'n':n,'paired_mean_delta_s':mean,'paired_sd_s':sd,
              'approx_95pct_t_interval_s':[mean-radius,mean+radius],
              'progression_better_seeds':sum(x<0 for x in deltas),
              'zero_better_seeds':sum(x>0 for x in deltas),
              'ties':sum(x==0 for x in deltas)}
    summary={'replication':'48 unseen stochastic seeds 101..148, balanced demand, split38, same arrivals per comparison',
      'simulation_runs':len(rows)*2,'paired_rows':len(rows),'turn_models':by,
      'caution':'independent synthetic random seeds, NOT independent observed Gyeongnam days; 95pct t interval assumes independent seeds and approximate normality of paired differences'}
    (ROOT/'heldout_summary.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False),encoding='utf-8')
    return summary

if __name__=='__main__':print(json.dumps(experiment(),indent=2))
