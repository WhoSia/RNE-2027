"""Exploratory P27 after documented diagnostic pilot: synthetic stage-dose test.

Not a deployable traffic controller; never infer real clearance safety.
"""
from collections import Counter
from dataclasses import replace
from itertools import product
from pathlib import Path
import hashlib,json,pickle

from dual_lane_v11 import run
from physical_transfer_screen import score
from p25_p26_physical_followups import worlds,action,tape_hash,frozen_p19,TERMINAL_PENALTY

HEADWAYS=(1,2)
DURATIONS=(6,10,16,24)
REFERENCE_ACTION=((84,87,'-'),(87,95,'L'),(95,120,'-'))


def longer_action(duration):
    if duration not in DURATIONS:raise ValueError('unregistered stage duration')
    return ((84,87,'-'),(87,87+duration,'L'),(87+duration,120,'-'))


def crossings(result):
    e=result['service_events']
    return {str(move):sum(x.get('reason')=='stopline_cross' and x.get('movement')==move
            and 87<=x['t']<120 for x in e) for move in ('L','S')}


def run_full(reference):
    lookup=frozen_p19(reference)
    records=[]
    for k,cfg,tape in worlds():
        for headway in HEADWAYS:
            conf=replace(cfg,receiver_headway_s=headway)
            checkpoint=run(conf,tape,trace=True,checkpoint_at=84)
            frozen=pickle.dumps(checkpoint,protocol=4)
            baseline=run(conf,tape,resume_from=checkpoint,trace=True)
            ref8=run(conf,tape,resume_from=checkpoint,phase_overrides=REFERENCE_ACTION,trace=True)
            if headway==2 and (score(ref8,60)-score(baseline,60),tape_hash(tape))!=lookup[k]:
                raise AssertionError(('P19 headway2 reference drift',k))
            effects={}
            for duration in DURATIONS:
                obj=run(conf,tape,resume_from=checkpoint,phase_overrides=longer_action(duration),trace=True)
                if obj['generated']!=baseline['generated']!=len(tape):
                    raise AssertionError('different arrival demand')
                effects[str(duration)]={'delta_cost':score(obj,TERMINAL_PENALTY)-score(baseline,TERMINAL_PENALTY),
                     'crossings_87_119':crossings(obj),
                     'network_out':obj['network_out_L']+obj['network_out_S'],
                     'receiver_denied_attempts':obj['receiver_denied_attempts']}
            if pickle.dumps(checkpoint,protocol=4)!=frozen:raise AssertionError('checkpoint mutated')
            records.append({'key':list(k),'headway_s':headway,'tape_sha256':tape_hash(tape),
                'checkpoint_sha256':hashlib.sha256(frozen).hexdigest(),
                'baseline_crossings_87_119':crossings(baseline),
                'baseline_cost':score(baseline,60),'effects':effects})
    if len(records)!=128:raise AssertionError('P27 incomplete')
    summary=[]
    for h in HEADWAYS:
        rows=[x for x in records if x['headway_s']==h]
        for d in DURATIONS:
            values=[x['effects'][str(d)]['delta_cost'] for x in rows]
            summary.append({'headway_s':h,'duration_s':d,'worlds':len(rows),
              'improved':sum(v<0 for v in values),'worsened':sum(v>0 for v in values),
              'ties':sum(v==0 for v in values),'delta_sum':sum(values),
              'left_crossing_diff_vs_baseline':sum(x['effects'][str(d)]['crossings_87_119']['L']-x['baseline_crossings_87_119']['L'] for x in rows)})
    first=Counter();pairs24vs6=Counter();same_service_different_cost=0
    for row in records:
        vals=[row['effects'][str(d)]['delta_cost'] for d in DURATIONS]
        different=[d for d,v in zip(DURATIONS,vals) if v!=vals[0]]
        first[str(different[0]) if different else 'never']=first.get(str(different[0]) if different else 'never',0)+1
        gap=vals[-1]-vals[0]
        pairs24vs6['better' if gap<0 else 'worse' if gap>0 else 'same']+=1
        same_service_different_cost+=int(gap!=0 and row['effects']['24']['crossings_87_119']==row['effects']['6']['crossings_87_119'])
    return {'protocol':'P27_EXPLORATORY_STAGE_EXTENSION_AFTER_PILOT',
        'status':'SYNTHETIC_UNCALIBRATED_NO_REAL_SIGNAL_CONTROL',
        'worlds':len(records),'unique_tapes':len({r['tape_sha256'] for r in records}),
        'pilot_informed':True,'dose_lengths_s':list(DURATIONS),
        'strata':summary,'first_tested_duration_differing_from6':dict(sorted(first.items())),
        'rank_24_vs6':dict(sorted(pairs24vs6.items())),
        'different_cost_but_same_87_119_crossings':same_service_different_cost,
        'records':records}


if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser();p.add_argument('frozen_p19',type=Path);p.add_argument('output',type=Path)
 args=p.parse_args();data=json.loads(args.frozen_p19.read_text(encoding='utf8'))
 args.output.write_text(json.dumps(run_full(data),sort_keys=True,indent=2)+'\n',encoding='utf8')
