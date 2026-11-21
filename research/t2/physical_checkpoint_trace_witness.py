"""PHYS-08 trace witnesses: seed53 receiver2 pocket14 B-share0, two regimes.

Each trace pair shares exactly one t84 microscopic checkpoint. A change in
exogenous demand is a new simulated world, NOT an identical-state comparison.
"""
import argparse
import hashlib
import json
from pathlib import Path
from dual_lane_v11 import run, checkpoint_observation
from spatial_v10 import arrivals
from physical_checkpoint_delay_and_shift import make_config, INTERVENTION
from physical_transfer_screen import score

WITNESS = {'seed':53,'capacity':2,'pocket_m':14.,'b_share':0.}
REGIMES = (('baseline',1800,.5),('lowturn',1350,.3))
METRICS = ('generated','exit_S','exit_L','network_out_S','network_out_L',
           'remaining','outside_vehicle_seconds','upstream_vehicle_seconds',
           'receiver_vehicle_seconds','changes_A_to_B')


def trace_case(demand,left_fraction):
    c=make_config(WITNESS['seed'],WITNESS['capacity'],WITNESS['pocket_m'],
                  WITNESS['b_share'],demand,left_fraction)
    tape=arrivals(c.base)
    checkpoint=run(c,tape,trace=True,checkpoint_at=84)
    baseline=run(c,tape,trace=True,resume_from=checkpoint)
    intervention=run(c,tape,trace=True,resume_from=checkpoint,
                     phase_overrides=INTERVENTION)
    if baseline['frames'][:84] != intervention['frames'][:84]:
        raise AssertionError('different predecision trajectories')
    if baseline != run(c,tape,trace=True):
        raise AssertionError('inexact checkpoint restart')
    pair={'decision_observation':checkpoint_observation(checkpoint),
          'identical_predecision_frames':True,
          'delta_intervention_minus_baseline':score(intervention,60)-score(baseline,60)}
    for name,run_result in (('baseline',baseline),('intervention',intervention)):
        pair[name]={key:run_result[key] for key in METRICS}
        pair[name]['objective']=score(run_result,60)
        pair[name]['crossings_ticks84_119']=[{'tick':e['t'],'movement':e['movement'],
            'vehicle_id':e['vehicle_id']} for e in run_result['service_events']
            if 84 <= e['t'] < 120 and e['reason']=='stopline_cross']
        pair[name]['postdecision_total_crossings']=sum(
            e['reason']=='stopline_cross' and e['t']>=84
            for e in run_result['service_events'])
    return pair


def experiment():
    data={label:{'demand_vph':demand,'left_share':left,
                 'trace':trace_case(demand,left)}
          for label,demand,left in REGIMES}
    return {'status':'SYNTHETIC_UNCALIBRATED',
            'witness_configuration':WITNESS,'regimes':data,
            'note':'within regime only, prefix is identical; across regimes demand and states differ'}


if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('output',type=Path)
    args=ap.parse_args()
    data=(json.dumps(experiment(),sort_keys=True,ensure_ascii=False,indent=2)+'\n').encode()
    args.output.write_bytes(data)
    print('SHA-256',hashlib.sha256(data).hexdigest())
