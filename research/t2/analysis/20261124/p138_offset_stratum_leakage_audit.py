"""P138 post-hoc audit: no new sims, detect offset-mixture confounding and within-tape comparison."""
import json
from pathlib import Path
from collections import defaultdict
HERE=Path(__file__).resolve().parent

def regret(row,p):
    arms=row['arms'];return arms[str(p)]['cost']-min(arms['30']['cost'],arms['60']['cost'])

def assess(path):
    j=json.loads((HERE/path).read_text());rows=j['rows'];assert len(rows)==64
    ks={(r['share'],r['label_seed'],r['time_seed'],r['family']) for r in rows}
    assert len(ks)==16 and all(sum((r['share'],r['label_seed'],r['time_seed'],r['family'])==k for r in rows)==4 for k in ks)
    count30=sum(r['delta_cost']<0 for r in rows);count60=sum(r['delta_cost']>0 for r in rows)
    assert count30+count60==64
    offset={(0,30):{},(15,0):{},(7,15):{},(23,45):{}}
    for off in offset:
        x=[r for r in rows if (r['phi30'],r['phi60'])==off]
        assert len(x)==16
        offset[off]={'n':16,'short_cheaper':sum(r['delta_cost']<0 for r in x),'long_cheaper':sum(r['delta_cost']>0 for r in x)}
    return j,{'n':64,'distinct_tapes':len(ks),'short_wins':count30,'long_wins':count60,
        'by_offset':{f'{a},{b}':v for (a,b),v in offset.items()}}

def main():
    p136,a=assess('P136_RESULT.json');p137,b=assess('P137_RESULT.json')
    assert (a['short_wins'],a['long_wins'])==(35,29)
    assert (b['short_wins'],b['long_wins'])==(35,29)
    trained={(0,30):60,(15,0):30,(7,15):60,(23,45):30}
    assert p137['frozen_calendar_policy']=={f'{a},{b}':v for (a,b),v in trained.items()}
    if {(r['share'],r['label_seed'],r['time_seed'],r['family']) for r in p136['rows']} & {(r['share'],r['label_seed'],r['time_seed'],r['family']) for r in p137['rows']}:
        raise AssertionError('demand tape overlap')
    group=defaultdict(list)
    for r in p137['rows']:
        group[(r['share'],r['label_seed'],r['time_seed'],r['family'])].append(r)
    wins={'calendar_better':0,'proxy_better':0,'equal':0}; rows=[]
    for k,rs in sorted(group.items()):
        rc=sum(regret(r,trained[(r['phi30'],r['phi60'])]) for r in rs)
        rp=sum(regret(r,30 if r['metric_delta']['receiver_denied_seconds']<0 else 60) for r in rs)
        wins['calendar_better' if rc<rp else 'proxy_better' if rc>rp else 'equal']+=1
        rows.append({'share':k[0],'label_seed':k[1],'time_seed':k[2],'family':k[3],
                     'calendar_regret':rc,'denied_seconds_proxy_regret':rp,'excess_proxy_regret':rp-rc})
    assert wins=={'calendar_better':11,'proxy_better':2,'equal':3}
    assert sum(r['calendar_regret'] for r in rows)==1646
    assert sum(r['denied_seconds_proxy_regret'] for r in rows)==19280
    assert sum(r['excess_proxy_regret'] for r in rows)==17634
    result={'status':'P138_POSTHOC_OFFSET_MIXTURE_AUDIT','simulator_arms':0,'inputs':['P136_RESULT.json','P137_RESULT.json'],
         'P136':a,'P137':b,'P137_within_tape_calendar_vs_proxy':wins,'P137_total_calendar_regret':1646,
         'P137_total_denied_seconds_proxy_regret':19280,'P137_proxy_minus_calendar_regret':17634,
         'P137_by_tape':rows,
         'method_warning':'P136/P137 overall class balance is offset mixture; each within-offset stratum strongly one-sided, and four pairs share each demand tape. Calendar-only mapping fit to P136, frozen P137. Post-treatment local proxy uses outcomes from both policies and is NOT available to real-time controller. P138 posthoc only, not independent simulation or field generality.'}
    (HERE/'P138_AUDIT_RESULT.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='P137_by_tape'},ensure_ascii=False,indent=2))
    return result
if __name__=='__main__':main()
