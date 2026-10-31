"""Compare modeled and observed movement counts by aligned signal cycle.

No parameter fitting. Uses anonymous aggregate counts only.
Required CSV: end_s,left_exits,straight_exits (per-cycle, not cumulative).
"""
import csv
from pathlib import Path

METRICS=(('left_exits','exit_L'),('straight_exits','exit_S'))

def read_aggregate_csv(path):
    with Path(path).open(newline='',encoding='utf-8-sig') as f:
        r=csv.DictReader(f)
        required={'end_s','left_exits','straight_exits'}
        if not required.issubset(r.fieldnames or ()):
            raise ValueError('missing aggregate columns')
        out=[]
        for x in r:
            row={}
            for key in required:
                try: val=int(x[key])
                except (ValueError,TypeError):raise ValueError('invalid integer: '+key)
                if val<0:raise ValueError('negative measured count')
                row[key]=val
            out.append(row)
        if not out or any(out[i]['end_s']>=out[i+1]['end_s'] for i in range(len(out)-1)):
            raise ValueError('empty or unordered observation periods')
        return out

def compare(simulated_cycles,observed_cycles):
    if len(simulated_cycles)!=len(observed_cycles):
        raise ValueError('cycle count mismatch')
    residuals={'L':[],'S':[]}
    prev={'exit_L':0,'exit_S':0}
    for predicted,observed in zip(simulated_cycles,observed_cycles):
        if predicted['end_s']!=observed['end_s']:
            raise ValueError('cycle endpoint mismatch')
        for obs_name,model_name in METRICS:
            movement='L' if model_name=='exit_L' else 'S'
            delta=predicted[model_name]-prev[model_name]
            prev[model_name]=predicted[model_name]
            if delta<0:raise ValueError('model cumulative exit count decreased')
            residuals[movement].append(delta-observed[obs_name])
    return {m:{'MAE_veh_per_cycle':sum(abs(x) for x in errors)/len(errors),
               'bias_veh_per_cycle':sum(errors)/len(errors),
               'max_abs_error':max(map(abs,errors)),
               'signed_residuals':errors} for m,errors in residuals.items()}
