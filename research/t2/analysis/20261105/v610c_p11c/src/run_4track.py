from itertools import product
import csv,json
from pathlib import Path
from policy_baselines import compare
base=Path(__file__).resolve().parents[1]/'results';base.mkdir(exist_ok=True)
summary=[];runs=[]
for pat,src,link,travel in product(('balanced','main_peak'),(6.5,13.0),(6.5,13.0),(3.0,5.0)):
 s,t=compare(pat,src,link,travel);summary.extend(s);runs.extend(t)
for name,arr in [('policy_baselines.csv',summary),('offset_trials.csv',[r.__dict__ for r in runs])]:
 with (base/name).open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(arr[0]));w.writeheader();w.writerows(arr)
report={
 'cells':len(summary)//5,'actual_unique_simulations':len(runs),'policy_comparisons':len(summary),
 'all_complete':all(r.completed==r.total for r in runs),
 'mean_regret_by_method':{m:round(sum(r['regret_vs_oracle_veh_s'] for r in summary if r['policy_search']==m)/(len(summary)//5),6) for m in sorted({r['policy_search'] for r in summary})},
 'nonzero_regret_cases':{m:sum(r['regret_vs_oracle_veh_s']>0 for r in summary if r['policy_search']==m) for m in sorted({r['policy_search'] for r in summary})},
 'source_effect_cases':sum(1 for pat,link,travel in product(('balanced','main_peak'),(6.5,13.0),(3.0,5.0))
  if next(x for x in summary if (x['pattern'],x['link_storage_m'],x['travel_s'],x['source_storage_m'],x['policy_search'])==(pat,link,travel,6.5,'oracle_all_8'))['oracle_offset_s']!=next(x for x in summary if (x['pattern'],x['link_storage_m'],x['travel_s'],x['source_storage_m'],x['policy_search'])==(pat,link,travel,13.,'oracle_all_8'))['oracle_offset_s'])
}
(base/'summary.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
