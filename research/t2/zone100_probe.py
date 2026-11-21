"""PHYS-03 exploratory controlled extension: 70m pocket, 100m change zone."""
from itertools import product
import json
from pathlib import Path
from dual_lane_v11 import DualConfig,run
from spatial_v10 import Config,arrivals
from physical_transfer_screen import score
from timed_physical_screen import WINDOWS

def experiment(original_zone70=None):
 rows=[]
 for seed,share,regime,order in product(range(8),(0.,.5),('never','early','late','always'),('leading','lagging')):
  base=Config(seed=seed,duration_s=720,demand_vph=1800,left_fraction=.5,
              pocket_length_m=70.,phase_order=order)
  c=DualConfig(base=base,through_B_share=share,allow_lane_changes=regime!='never',
               change_zone_m=100.,lane_change_windows=WINDOWS.get(regime,()),
               receiver_mode='cells',receiver_slots=4)
  r=run(c,arrivals(base))
  values=('generated','network_out_S','network_out_L','remaining','outside_vehicle_seconds',
          'upstream_vehicle_seconds','receiver_vehicle_seconds','changes_A_to_B',
          'pocket_block_seconds','receiver_denied_attempts','receiver_denied_seconds')
  row={'seed':seed,'pocket_m':70.,'b_share':share,'regime':regime,'order':order,
       **{key:r[key] for key in values},
       **{f'cost_p{p}':score(r,p) for p in (0,60,120)}}
  rows.append(row)
 lookup={(x['seed'],x['b_share'],x['regime'],x['order']):x for x in rows}
 pairs=[]
 for seed,share,regime in product(range(8),(0.,.5),('never','early','late','always')):
  left=lookup[seed,share,regime,'leading'];through=lookup[seed,share,regime,'lagging']
  pairs.append({'seed':seed,'b_share':share,'regime':regime,
   **{f'delta_p{p}':left[f'cost_p{p}']-through[f'cost_p{p}'] for p in (0,60,120)},
   'lane_changes_both_orders':left['changes_A_to_B']+through['changes_A_to_B']})
 d={(x['seed'],x['b_share'],x['regime']):x for x in pairs}
 contrasts=[]
 for seed,share in product(range(8),(0.,.5)):
  e=d[seed,share,'early'];l=d[seed,share,'late']
  contrasts.append({'seed':seed,'b_share':share,'early_delta_p60':e['delta_p60'],
    'late_delta_p60':l['delta_p60'],'early_changes':e['lane_changes_both_orders'],
    'late_changes':l['lane_changes_both_orders'],
    'early_delta_p0':e['delta_p0'],'late_delta_p0':l['delta_p0'],
    'early_delta_p120':e['delta_p120'],'late_delta_p120':l['delta_p120']})
 same_never=0
 if original_zone70 is not None:
  old={(x['seed'],x['b_share'],x['regime'],x['order']):x for x in original_zone70['runs'] if x['pocket_m']==70.}
  checks=('generated','network_out_S','network_out_L','remaining','outside_vehicle_seconds',
          'upstream_vehicle_seconds','receiver_vehicle_seconds','changes_A_to_B',
          'pocket_block_seconds','receiver_denied_attempts','receiver_denied_seconds')
  for new in rows:
   if new['regime']=='never':
    prev=old[new['seed'],new['b_share'],new['regime'],new['order']]
    if any(new[k]!=prev[k] for k in checks) or new['cost_p60']!=prev['cost_p60']:
     raise AssertionError('baseline mismatch')
    same_never+=1
  assert same_never==32
 assert len(rows)==128 and len(pairs)==64 and len(contrasts)==16
 return {'status':'EXPLORATORY_UNCALIBRATED','zone_m':100.,'pocket_m':70.,
  'summary':{'n_runs':len(rows),'n_phase_pairs':len(pairs),'n_timing_pairs':len(contrasts),
   'reversal_by_penalty':{str(p):sum(x[f'early_delta_p{p}']*x[f'late_delta_p{p}']<0 for x in contrasts) for p in (0,60,120)},
   'ties_p60':sum(x['early_delta_p60']==0 or x['late_delta_p60']==0 for x in contrasts),
   'early_changes':sum(x['early_changes'] for x in contrasts),
   'late_changes':sum(x['late_changes'] for x in contrasts),'original_never_identical':same_never},
  'runs':rows,'phase_pairs':pairs,'early_late_contrasts':contrasts}

if __name__=='__main__':
 import argparse
 ap=argparse.ArgumentParser();ap.add_argument('output',type=Path);ap.add_argument('--zone70',type=Path)
 args=ap.parse_args()
 old=json.loads(args.zone70.read_text()) if args.zone70 else None
 args.output.write_text(json.dumps(experiment(old),indent=2)+'\n',encoding='utf-8')
