"""P19: exact-core synthetic finite-receiver stage/service interaction.

No real controller, amber, pedestrian or external Wi-Fi measurement.
Worlds with different receiving offsets/capacities are NOT identical states.
"""
from pathlib import Path
from collections import Counter, defaultdict
from dataclasses import replace
from itertools import product
import hashlib
import json
import pickle

from p18_clock_position_action import (arrival_clock_pair, tape_hash, build_config,
                                       OVERRIDES, DECISION_TICK)
from dual_lane_v11 import run, checkpoint_observation
from physical_transfer_screen import score

SEEDS=tuple(range(112,120))
REGIMES=((1650,.50),(1800,.45))
RECEIVERS=(2,4)
OFFSETS=(0,15)
POCKETS=(14.,28.)
B_SHARES=(0.,.5)
WINDOW=(84,130)
ACTION=OVERRIDES['left_8s']


def _events(result):
    selected=[e for e in result['service_events'] if WINDOW[0]<=e['t']<WINDOW[1]]
    early_l=sum(e.get('movement')=='L' and e.get('reason')=='stopline_cross'
                and 87<=e['t']<95 for e in selected)
    later_block=sum(e.get('reason') in ('receiver_entry_cell_busy','receiver_capacity_full')
                    and 120<=e['t']<130 for e in selected)
    by_reason=Counter(e.get('reason','UNKNOWN') for e in selected)
    return {'early_left_crossings_87_94':early_l,
            'later_receiver_denials_120_129':later_block,
            'total_stopline_crossings_84_129':by_reason.get('stopline_cross',0),
            'receiver_denials_84_129':by_reason.get('receiver_entry_cell_busy',0)+by_reason.get('receiver_capacity_full',0)}


def evaluate(config,tape):
    checkpoint=run(config,tape,checkpoint_at=DECISION_TICK,trace=True)
    sha=hashlib.sha256(pickle.dumps(checkpoint,protocol=4)).hexdigest()
    obs=checkpoint_observation(checkpoint)
    baseline=run(config,tape,resume_from=checkpoint,trace=True)
    treatment=run(config,tape,resume_from=checkpoint,trace=True,phase_overrides=ACTION)
    assert hashlib.sha256(pickle.dumps(checkpoint,protocol=4)).hexdigest()==sha
    assert baseline['generated']==treatment['generated']==len(tape)
    return {'seed':config.base.seed,'demand_vph':config.base.demand_vph,
            'left_fraction':config.base.left_fraction,'pocket_m':config.base.pocket_length_m,
            'b_share':config.through_B_share,'receiver_capacity':config.receiver_slots,
            'downstream_offset_s':config.downstream_offset_s,
            'tape_hash':tape_hash(tape),'counts_at84':{
                k:obs[k] for k in ('outside_A','outside_B','approach_A','approach_B','pocket_vehicles','receiver_vehicles')},
            'checkpoint_sha256':sha,'model_delta':score(treatment,60)-score(baseline,60),
            'baseline':{'remaining':baseline['remaining'],'out_S':baseline['network_out_S'],
                        'out_L':baseline['network_out_L'],**_events(baseline)},
            'treatment':{'remaining':treatment['remaining'],'out_S':treatment['network_out_S'],
                         'out_L':treatment['network_out_L'],**_events(treatment)},
            'scope':'SIMULATED_NATIVE_TRANSITIONS_NOT_LEGAL_SIGNAL_FEASIBILITY'}


def experiment():
    rows=[]
    for (demand,left_share),seed,capacity,offset,pocket,bshare in product(REGIMES,SEEDS,RECEIVERS,OFFSETS,POCKETS,B_SHARES):
        cfg=build_config(seed,demand,left_share,pocket,capacity,bshare)
        cfg=replace(cfg,downstream_offset_s=offset)
        _,clock=arrival_clock_pair(cfg.base)
        rows.append(evaluate(cfg,clock))
    assert len(rows)==256
    blocks={ (r['demand_vph'],r['seed']):r['tape_hash'] for r in rows}
    assert len(blocks)==16
    summary=[]
    for cap,offset in product(RECEIVERS,OFFSETS):
        subset=[r for r in rows if r['receiver_capacity']==cap and r['downstream_offset_s']==offset]
        diffs=[r['model_delta'] for r in subset]
        summary.append({'receiver_capacity':cap,'downstream_offset_s':offset,'worlds':len(subset),
                        'unique_arrival_tapes':len({r['tape_hash'] for r in subset}),
                        'delta_negative':sum(d<0 for d in diffs),'delta_positive':sum(d>0 for d in diffs),
                        'delta_ties':sum(d==0 for d in diffs),'delta_sum':sum(diffs),
                        'early_additional_turn_crossings':sum(r['treatment']['early_left_crossings_87_94']-r['baseline']['early_left_crossings_87_94'] for r in subset),
                        'extra_late_receiver_denials':sum(r['treatment']['later_receiver_denials_120_129']-r['baseline']['later_receiver_denials_120_129'] for r in subset)})
    grouped=defaultdict(dict)
    for r in rows:
        key=(r['demand_vph'],r['seed'],r['receiver_capacity'],r['pocket_m'],r['b_share'])
        grouped[key][r['downstream_offset_s']]=r
    assert len(grouped)==128
    rank_reversals=[]
    for key,pair in sorted(grouped.items()):
        assert set(pair)==set(OFFSETS)
        x,y=pair[OFFSETS[0]]['model_delta'],pair[OFFSETS[1]]['model_delta']
        if x<-5 and y>5 or x>5 and y<-5:
            rank_reversals.append({'key':list(key),'offset0':x,'offset15':y,
                                   'same_predecision_state':False,
                                   'tape_hash':pair[0]['tape_hash']})
    return {'protocol':'T2_P19_RECEIVER_OPPORTUNITY_PROSPECTIVE',
            'worlds':len(rows),'independent_tape_blocks':len(blocks),'matched_offset_pairs':len(grouped),
            'effect_modification_cross_offset_not_same_state':True,
            'offset_sign_reversals_epsilon5':rank_reversals,
            'strata':summary,'records':rows}

if __name__=='__main__':
    import argparse
    a=argparse.ArgumentParser();a.add_argument('output',type=Path);args=a.parse_args()
    args.output.write_text(json.dumps(experiment(),sort_keys=True,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
