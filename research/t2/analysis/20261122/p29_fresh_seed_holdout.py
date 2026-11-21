"""P29 prospective NEW synthetic arrival seeds: 24s vs6s duration transport.

Model-only 1D cells, no signal legality or field use.
"""
from dataclasses import replace
from itertools import product
from collections import Counter,defaultdict
import hashlib,json,pickle
from pathlib import Path
from dual_lane_v11 import run
from physical_transfer_screen import score
from p19_receiver_service_opportunity import build_config,arrival_clock_pair,tape_hash
from p27_stage_opportunity_extension import longer_action,crossings

FRESH_SEEDS=((120,1650,.5),(121,1650,.5),(122,1800,.45),(123,1800,.45))
RECEIVERS=(2,4)
OFFSETS=(0,15)
POCKETS=(14.,28.)
B_SHARES=(0.,.5)
HEADWAYS=(1,2)

def holdout():
    records=[]
    for seed,demand,turn in FRESH_SEEDS:
        for cap,offset,pocket,bshare,headway in product(RECEIVERS,OFFSETS,POCKETS,B_SHARES,HEADWAYS):
            cfg=replace(build_config(seed,demand,turn,pocket,cap,bshare),
                receiver_headway_s=headway,downstream_offset_s=offset)
            _,tape=arrival_clock_pair(cfg.base)
            cp=run(cfg,tape,checkpoint_at=84,trace=True)
            chk=pickle.dumps(cp,protocol=4)
            baseline=run(cfg,tape,resume_from=cp,trace=True)
            variants={}
            for dur in (6,24):
                r=run(cfg,tape,resume_from=cp,trace=True,phase_overrides=longer_action(dur))
                if r['generated']!=baseline['generated'] or r['generated']!=len(tape):
                    raise AssertionError('future request tape differed')
                variants[str(dur)]={'delta':score(r,60)-score(baseline,60),
                  'L_crossings_87_119':crossings(r)['L'],
                  'receiver_denied_attempts':r['receiver_denied_attempts'],
                  'remaining':r['remaining']}
            if pickle.dumps(cp,protocol=4)!=chk:raise AssertionError('checkpoint mutated')
            records.append({'seed':seed,'regime':[demand,turn],'receiver_slots':cap,
                'downstream_offset_s':offset,'pocket_m':pocket,
                'b_share':bshare,'receiver_headway_s':headway,
                'tape_sha256':tape_hash(tape),'checkpoint_sha256':hashlib.sha256(chk).hexdigest(),
                'baseline_L_crossings_87_119':crossings(baseline)['L'],
                'baseline_remaining':baseline['remaining'],
                'effects':variants})
    if len(records)!=128:raise AssertionError('P29 grid drift')
    strata=[]
    for headway,offset in product(HEADWAYS,OFFSETS):
        rows=[r for r in records if r['receiver_headway_s']==headway and r['downstream_offset_s']==offset]
        diffs=[r['effects']['24']['delta']-r['effects']['6']['delta'] for r in rows]
        crossings_diff=[r['effects']['24']['L_crossings_87_119']-r['effects']['6']['L_crossings_87_119'] for r in rows]
        strata.append({'headway_s':headway,'offset_s':offset,'worlds':len(rows),
            '24_better':sum(x<0 for x in diffs),'24_equal':sum(x==0 for x in diffs),
            '24_worse':sum(x>0 for x in diffs),'sum_cost24_minus6':sum(diffs),
            '24_more_L_crossings':sum(x>0 for x in crossings_diff),
            '24_equal_L_crossings':sum(x==0 for x in crossings_diff),
            '24_less_L_crossings':sum(x<0 for x in crossings_diff)})
    return {'protocol':'P29_NEW_SEED_HOLDOUT_PRE_FROZEN',
        'status':'SYNTHETIC_MODEL_TRANSPORT_NOT_EXTERNAL_FIELD_VALIDATION',
        'seeds':[s for s,_,_ in FRESH_SEEDS],'worlds':len(records),
        'unique_tapes':len({r['tape_sha256'] for r in records}),
        'all_fixed_checkpoint':True,'dose_s':[6,24],
        'strata':strata,'records':records,
        'limitations':['4 independent timestamp sequences reused across 128 geometry variants',
            '24s action is an exploratory hypothesis from P27, not actual signal legality',
            'Reference engine synthetic, not SUMO or empirical traffic']}


if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser();p.add_argument('output',type=Path)
 a=p.parse_args()
 a.output.write_text(json.dumps(holdout(),sort_keys=True,indent=2)+'\n',encoding='utf8')
