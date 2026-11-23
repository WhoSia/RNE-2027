"""Exploratory calendar-only prediction on already-seen P114 arms. NO holdout."""
import json
from collections import Counter
from pathlib import Path
from scipy.stats import spearmanr

BASE=Path(__file__).resolve().parent

def sign(x):return (x>0)-(x<0)

def main():
    ref=json.loads((BASE/'P114_RESULT.json').read_text())
    rows=[];pool=Counter()
    for r in ref['rows']:
        a=[z for z in r['arms'] if z['period_s']==30]
        b=[z for z in r['arms'] if z['period_s']==60]
        c=Counter()
        alltrue=[];allpred=[]
        for x in a:
            for y in b:
                observed=sign(x['cost']-y['cost'])
                pred=sign(y['left_green_overlap_t84_400']-x['left_green_overlap_t84_400'])
                c['total']+=1
                c['true_tie']+=observed==0
                c['overlap_tie']+=pred==0
                c['strict_prediction_count']+=pred!=0
                c['strict_prediction_correct']+=pred!=0 and pred==observed
                c['overall_prediction_correct_with_ties']+=pred==observed
                c['always_30_better_correct']+=observed==-1
                alltrue.append(x['cost']-y['cost'])
                allpred.append(y['left_green_overlap_t84_400']-x['left_green_overlap_t84_400'])
        rho,p=spearmanr(alltrue,allpred)
        c['spearman_rank_correlation']=float(rho)
        for k,v in c.items():
            if k!='spearman_rank_correlation':pool[k]+=v
        rows.append({'seed':r['seed'],'family':r['family'],'counts':dict(c),
                     'accuracy_non_tie':c['strict_prediction_correct']/c['strict_prediction_count'],
                     'accuracy_all_with_ties':c['overall_prediction_correct_with_ties']/c['total']})
    result={'status':'EXPLORATORY_ON_DISCOVERY_GRID_NOT_OUT_OF_SAMPLE','source':'P114_RESULT.json',
            'primary_feature':'signed LEFT green-overlap seconds t84..400 (calendar only)',
            'tested_pairs':pool['total'], 'cohort_count':4,
            'pooled':dict(pool),
            'pooled_non_tie_accuracy':pool['strict_prediction_correct']/pool['strict_prediction_count'],
            'pooled_all_accuracy':pool['overall_prediction_correct_with_ties']/pool['total'],
            'always_30_better_accuracy':pool['always_30_better_correct']/pool['total'],
            'cohorts':rows,
            'limitations':['1800 offset comparisons per tape share policy arms and are not independent observations',
                            'same 4 tapes used to inspect heuristic and assess predictions: no predictive validation',
                            'calendar overlap includes policy clock; storage and upstream queue can mediate delay',
                            'overlap window was chosen after Claude report and P114 outcomes, not preregistered']}
    (BASE/'P116_RESULT.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'pooled':result['pooled'],'pooled_non_tie_accuracy':result['pooled_non_tie_accuracy'],'pooled_all_accuracy':result['pooled_all_accuracy'],'always_30_better_accuracy':result['always_30_better_accuracy'],'rhos':[x['counts']['spearman_rank_correlation'] for x in rows]},indent=2))
if __name__=='__main__':main()
