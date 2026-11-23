"""P143 posthoc cross-cohort audit. ZERO new simulator replays."""
from __future__ import annotations
import json
from pathlib import Path
from collections import defaultdict

HERE=Path(__file__).resolve().parent
NAMES=('P140','P141','P142')
TARGET=(7,15)

def audit():
    cohorts={}
    for name in NAMES:
        j=json.loads((HERE/f'{name}_RESULT.json').read_text())
        rows=j['rows']
        assert j['simulator_arms']==128 and len(rows)==64
        keys={(r['share'],r['label_seed'],r['time_seed'],r['family']) for r in rows}
        assert len(keys)==16
        assert all(sum((r['share'],r['label_seed'],r['time_seed'],r['family'])==key for r in rows)==4 for key in keys)
        calendar=sum(r['arms'][str(r['choices']['calendar'])]['cost']-min(r['arms']['30']['cost'],r['arms']['60']['cost']) for r in rows)
        guard=sum(r['arms'][str(r['choices']['guard'])]['cost']-min(r['arms']['30']['cost'],r['arms']['60']['cost']) for r in rows)
        assert calendar==j['pooled']['calendar']['total_regret']
        assert guard==j['pooled']['guard']['total_regret']
        byshare={}
        for share in (.5,.75):
            sub=[r for r in rows if r['share']==share and (r['phi30'],r['phi60'])==TARGET]
            assert len(sub)==8
            q=sorted(r['q_upstream'] for r in sub)
            triggers=[r for r in sub if r['choices']['calendar']!=r['choices']['guard']]
            helper=sum(r['arms']['30']['cost']<r['arms']['60']['cost'] for r in triggers)
            harmful=sum(r['arms']['30']['cost']>r['arms']['60']['cost'] for r in triggers)
            byshare[str(share)]={'n':8,'queue_values':q,'min_queue':min(q),'max_queue':max(q),
                'eligible_q_ge_14':sum(x>=14 for x in q),'activated':len(triggers),
                'helpful':helper,'harmful':harmful,
                'triggered_delta_cost': [r['delta_cost'] for r in triggers]}
        cohorts[name]={'source_status':j['status'],'simulator_arms_already_run':128,
           'new_arms_for_this_audit':0,'regret_calendar':calendar,
           'regret_guard':guard,'extra_regret_guard':guard-calendar,
           'correct_calendar':j['pooled']['calendar']['correct'],
           'correct_guard':j['pooled']['guard']['correct'],
           'trigger_count':j['pooled']['triggered'],'by_share_target_offset':byshare,
           'label_seeds': sorted({r['label_seed'] for r in rows}),
           'time_seeds':sorted({r['time_seed'] for r in rows})}
    assert cohorts['P140']['trigger_count']==8
    assert cohorts['P141']['trigger_count']==2
    assert cohorts['P142']['trigger_count']==0
    assert cohorts['P140']['extra_regret_guard']==17840
    assert cohorts['P141']['extra_regret_guard']==1996
    assert cohorts['P142']['extra_regret_guard']==0
    assert cohorts['P140']['by_share_target_offset']['0.5']['helpful']==2
    assert cohorts['P140']['by_share_target_offset']['0.75']['harmful']==6
    assert cohorts['P141']['by_share_target_offset']['0.5']['harmful']==2
    assert cohorts['P142']['by_share_target_offset']['0.5']['max_queue']==12
    return {'status':'P143_POSTHOC_COHORT_TRANSPORT_AUDIT',
        'new_simulator_arms':0,'inputs':[f'{name}_RESULT.json' for name in NAMES],
        'cohorts':cohorts,
        'verdict':'P140 reward-driven share interaction reverses on P141 unseen times; P142 novel route labels have no cutoff support; no reusable upstream >=14 controller demonstrated.',
        'method_limitations':'3 cohorts have 16 demand tapes each repeated at 4 offset packages, and one identical synthetic model. P141 adapts to P140 outcome; P142 rules were frozen before P141 output. Configured turn share is not a measured field variable.'}

def main():
    result=audit()
    (HERE/'P143_AUDIT_RESULT.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({k:result[k] for k in ('status','new_simulator_arms','cohorts','verdict')},ensure_ascii=False))
    return result

if __name__=='__main__':main()
