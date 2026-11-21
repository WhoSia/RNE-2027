"""Exploratory comparison of score-equivalent model worlds with changed event attempts.

Consumes exact frozen P25/P26 and P27 outputs; not a new empirical model.
"""
import hashlib
import json
from collections import Counter
from pathlib import Path

SHA_P25P26='640ec195830abae2ab99d202d43d92aaf3cbbc5f875a0ddc6765fe82f20c19e4'
SHA_P27='339a9aacc5f3539bbc65931ab9655f362a58ed19305debca53a25e1a6de9b962'

def source(path,sha):
    data=Path(path).read_bytes()
    if hashlib.sha256(data).hexdigest()!=sha:
        raise ValueError('source result was modified')
    return json.loads(data)


def inspect(p25p26,p27):
    a=p25p26['P26']['records']
    b=p27['records']
    if len(a)!=64 or len(b)!=128:raise ValueError('incomplete prior cohorts')
    keys=[tuple(r['key']) for r in a]
    if len(set(keys))!=64:raise ValueError('duplicate P26 scenario')
    lookup={tuple(r['key']):r for r in a}
    crosschecked=0
    equal_score_changed_attempts=0
    exact_denial_increment=Counter()
    altered_terminal_state=0
    for r in a:
        dose=r['deltas']
        if not (dose['6']==dose['8']==dose['10']):
            raise AssertionError('frozen equal-cost premise contradicted')
        den6=r['treated']['6']['receiver_denied_attempts']
        den10=r['treated']['10']['receiver_denied_attempts']
        if den6!=den10:equal_score_changed_attempts+=1
        exact_denial_increment[den10-den6]+=1
        if r['treated']['6']['remaining']!=r['treated']['10']['remaining']:
            altered_terminal_state+=1
    by_head=Counter()
    same_cost_more_L=Counter()
    same_cost_same_L_more_attempts=Counter()
    attempt_increments_6to10=Counter()
    attempt_increments_10to16=Counter()
    crossing_deltas_6to10=Counter()
    cost_differences_16to24=Counter()
    repeated_keys=set()
    for r in b:
        key=tuple(r['key']);h=r['headway_s']
        if (key,h) in repeated_keys:raise ValueError('duplicate P27 world')
        repeated_keys.add((key,h))
        if key not in lookup:raise ValueError('unpaired P27 scenario')
        if h==2:
            original=lookup[key]
            if r['effects']['6']['delta_cost']!=original['deltas']['6'] or r['effects']['10']['delta_cost']!=original['deltas']['10']:
                raise AssertionError('P26/P27 64-row repeated action cost disagrees')
            if r['effects']['6']['receiver_denied_attempts']!=original['treated']['6']['receiver_denied_attempts']:
                raise AssertionError('P26/P27 denied-attempt count disagrees')
            crosschecked+=1
        fx=r['effects']
        for x,y,counts in (('6','10',attempt_increments_6to10),('10','16',attempt_increments_10to16)):
            counts[fx[y]['receiver_denied_attempts']-fx[x]['receiver_denied_attempts']]+=1
        L6=fx['6']['crossings_87_119']['L']
        L10=fx['10']['crossings_87_119']['L']
        crossing_deltas_6to10[L10-L6]+=1
        if fx['6']['delta_cost']==fx['10']['delta_cost'] and L10!=L6:
            same_cost_more_L[h]+=1
        if (fx['6']['delta_cost']==fx['10']['delta_cost'] and L10==L6
                and fx['6']['receiver_denied_attempts']!=fx['10']['receiver_denied_attempts']):
            same_cost_same_L_more_attempts[h]+=1
        cost_differences_16to24[fx['24']['delta_cost']-fx['16']['delta_cost']]+=1
        by_head[h]+=1
    if crosschecked!=64 or by_head!={1:64,2:64}:
        raise AssertionError('P26/P27 matching incomplete')
    return {
      'protocol':'P28_POST_HOC_EVENT_METRIC_COLLISION',
      'status':'SYNTHETIC_INSTRUMENTATION_BIAS_NOT_EMPIRICAL_CONGESTION',
      'P26_worlds':len(a),'P27_worlds':len(b),
      'cross_reproduced_P26_P27_h2_worlds':crosschecked,
      'P26_equal_cost_but_changed_denial_attempts':equal_score_changed_attempts,
      'P26_6_vs10_denial_attempt_delta_hist':dict(sorted(exact_denial_increment.items())),
      'P26_6_vs10_terminal_remaining_different':altered_terminal_state,
      'P27_6_vs10_denial_attempt_delta_hist':dict(sorted(attempt_increments_6to10.items())),
      'P27_10_vs16_denial_attempt_delta_hist':dict(sorted(attempt_increments_10to16.items())),
      'P27_6_vs10_left_crossing_delta_hist':dict(sorted(crossing_deltas_6to10.items())),
      'P27_same_cost_different_left_crossings_by_headway':dict(sorted(same_cost_more_L.items())),
      'P27_same_cost_same_left_crossings_more_denials_by_headway':dict(sorted(same_cost_same_L_more_attempts.items())),
      'P27_16_vs24_distinct_cost_gaps':len(cost_differences_16to24),
      'interpretation':'Denial attempt is conditioned on a phase presenting a service opportunity, not invariant across treatments. Repeated attempts are not unique vehicles or queue size.',
      'independent_full_arrival_tapes':4,
      'pilot_informed':True,
    }


if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('p25p26',type=Path)
    p.add_argument('p27',type=Path);p.add_argument('out',type=Path)
    a=p.parse_args()
    o=inspect(source(a.p25p26,SHA_P25P26),source(a.p27,SHA_P27))
    a.out.write_text(json.dumps(o,sort_keys=True,indent=2)+'\n',encoding='utf8')
