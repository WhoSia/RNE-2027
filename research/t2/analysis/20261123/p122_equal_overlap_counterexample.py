"""Exploratory P122: falsify sufficiency of aggregated calendar overlap by exact equality."""
import json
from collections import Counter
from pathlib import Path
HERE=Path(__file__).resolve().parent

def main():
    p=json.loads((HERE/'P114_RESULT.json').read_text())
    c=Counter();rows=[]
    for data in p['rows']:
        a=[v for v in data['arms'] if v['period_s']==30]
        b=[v for v in data['arms'] if v['period_s']==60]
        for x in a:
            for y in b:
                if x['left_green_overlap_t84_400'] != y['left_green_overlap_t84_400']:continue
                delta=x['cost']-y['cost']; c['same_overlap_pairs']+=1
                c['cost_30_higher']+=delta>0;c['cost_30_lower']+=delta<0;c['cost_equal']+=delta==0
                rows.append({'seed':data['seed'],'family':data['family'],
                             'offset30':x['offset_s'],'offset60':y['offset_s'],
                             'same_left_overlap_seconds':x['left_green_overlap_t84_400'],
                             'cost30':x['cost'],'cost60':y['cost'],'cost30_minus60':delta})
    result={'status':'EXPLORATORY_SAME_SOURCE_COUNTEREXAMPLE','source':'P114_RESULT.json',
            'same_overlap_pair_count':c['same_overlap_pairs'],'cost_signs':dict(c),
            'max_absolute_cost_difference':max(abs(r['cost30_minus60']) for r in rows),
            'small_sample_examples':{
                '30_more_expensive':next((r for r in rows if r['cost30_minus60']>0),None),
                '30_less_expensive':next((r for r in rows if r['cost30_minus60']<0),None),
                'largest_abs':max(rows,key=lambda r:abs(r['cost30_minus60']))},
            'rows':rows,
            'inference':'Identical sum of left-phase/downstream-green overlap seconds on t84..400 is insufficient to determine the sign or magnitude of total network vehicle-second cost. Conditional on differing period offsets and corresponding time placement; this does not refute use as a useful predictor.',
            'limitation':'Post-hoc reuse of P114 four tapes and 360 scenario arms; 176 crossed comparisons not independent.'}
    (HERE/'P122_RESULT.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k in ('same_overlap_pair_count','cost_signs','max_absolute_cost_difference','small_sample_examples')},indent=2))
if __name__=='__main__':main()
