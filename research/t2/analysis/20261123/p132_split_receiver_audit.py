"""P132: post-experiment adversarial topology/metric-sensitivity audit; NO new sims."""
import json
from collections import Counter
from pathlib import Path
HERE=Path(__file__).resolve().parent

def main():
    p={i:json.loads((HERE/f'P{i}_RESULT.json').read_text()) for i in (127,129,130,131)}
    assert (p[129]['simulator_arms'],p[130]['simulator_arms'],p[131]['simulator_arms'])==(96,32,32)
    assert all(p[i]['all_cleared'] for i in (129,130,131))
    assert p[129]['legacy_regression_exact'] and p[130]['unit_test_shared_exit_pass'] and p[131]['unit_test_shared_exit_pass']
    key=lambda r:(r['share'],r['label_seed'],r['time_seed'],r['family'])
    old={key(r):r for r in p[130]['rows']}
    new={key(r):r for r in p[131]['rows']}
    assert len(old)==len(new)==16 and set(old)==set(new)
    changed=[]
    for k in sorted(old):
        o,n=old[k],new[k]
        if o['paradox']!=n['paradox']:
            changed.append({'share':k[0],'label_seed':k[1],'time_seed':k[2],'family':k[3],
                's_first':{'cost_delta':o['delta_cost'],'denied_delta':o['delta_denied'],'paradox':o['paradox']},
                'l_first':{'cost_delta':n['delta_cost'],'denied_delta':n['delta_denied'],'paradox':n['paradox']},
                'cost_delta_change':n['delta_cost']-o['delta_cost'],
                'denied_delta_change':n['delta_denied']-o['delta_denied']})
    assert len(changed)==3
    unchanged_cost=sum(old[k]['delta_cost']==new[k]['delta_cost'] for k in old)
    assert unchanged_cost==12
    identical_denied=sum(old[k]['delta_denied']==new[k]['delta_denied'] for k in old)
    assert identical_denied==0
    cost_sign_flips=sum((old[k]['delta_cost']>0)!=(new[k]['delta_cost']>0) for k in old)
    assert cost_sign_flips==0
    paradox_counts={str(share):{top:sum(row['paradox'] for row in p[129]['rows'] if row['share']==share and row['topology']==top)
        for top in ('shared4','separate2+2','separate4+4')} for share in (.5,.75)}
    for share in (.5,.75):
        paradox_counts[str(share)]['separate2+2_shared_exit_S_first']=sum(x['paradox'] for x in p[130]['rows'] if x['share']==share)
        paradox_counts[str(share)]['separate2+2_shared_exit_L_first']=sum(x['paradox'] for x in p[131]['rows'] if x['share']==share)
    assert paradox_counts['0.5']=={'shared4':3,'separate2+2':2,'separate4+4':1,
        'separate2+2_shared_exit_S_first':2,'separate2+2_shared_exit_L_first':5}
    assert paradox_counts['0.75']=={'shared4':8,'separate2+2':1,'separate4+4':1,
        'separate2+2_shared_exit_S_first':1,'separate2+2_shared_exit_L_first':1}
    result={'status':'P132_TOPOLOGY_AUDIT_COMPLETE','replayed_simulator_arms':0,
        'input_sources':['P127_RESULT.json','P129_RESULT.json','P130_RESULT.json','P131_RESULT.json'],
        'p129_p130_p131_distinct_simulator_arms':160,
        'p129_legacy_regression_exact_arms':32,
        'paradox_counts_by_left_share':paradox_counts,
        's_first_vs_l_first_compared_tapes':16,
        'paradox_label_flips':len(changed),'paradox_label_flip_rows':changed,
        'unchanged_cost_contrast_count':unchanged_cost,'unchanged_denied_contrast_count':identical_denied,
        'cost_sign_flips':cost_sign_flips,
        'headline':'Paradox label flips in three tapes when the split-receiver global-exit tie arbitration changes; in two of three the signed network cost contrast stays numerically identical but local receiver-denial sign reverses.',
        'metric_caution':'receiver_denied_seconds is one tick-level boolean for any denied upstream receiver-admission attempt, not the sum of individual vehicle waiting seconds. The period contrast in this indicator can flip under exit precedence without a cost-ranking flip.',
        'topology_caution':'shared4 vs separate2+2 conserves aggregate receiving CELL COUNT but not link traversal length or downstream service order. separate4+4 doubles storage and service opportunities. Any cross-topology causal isolation statement is invalid.',
        'status_limits':'Exact arithmetic, deterministic fork controls, same T2 model. No SUMO, no empirical validation or known theorem novelty. These same 16 label/timestamp tapes appear in P129–P131 and are not independent draws across interventions.'}
    (HERE/'P132_AUDIT_RESULT.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'count':paradox_counts,'flips':changed,'unchanged_cost':unchanged_cost,'sign_flip':cost_sign_flips},ensure_ascii=False,indent=2))
    return result
if __name__=='__main__':main()
