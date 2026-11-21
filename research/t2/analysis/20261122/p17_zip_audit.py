"""P17: read-only audit of the specifically designated PHYS-04 historic ZIP.

This is an analysis of historical *synthetic* results, not a PHYS rerun.
No data other than the explicitly supplied ZIP path is accessed.
"""
import argparse
import collections
import hashlib
import json
import zipfile

SOURCE='canonical_local_capacity144.json'
COUNTS=('outside_A','outside_B','approach_A','approach_B','pocket_vehicles','receiver_vehicles')
EXPECTED_SHA256='7f7eff90b83cfe5e1f071bb02d5880face9c0e047abcd17349cd3fb06392758e'
EXPECTED_RESULT_SHA256='0d91beab746b8e67bf1fa5ea327e3c982d10e39b57cd5cf2fef020ad328e1001'


def validate(row):
    if row.get('checkpoint_identity') is not True:
        raise ValueError('missing matched policy checkpoint')
    ob=row['decision_observation']
    c=row['capacity']
    if type(c) is not int or c<=0:
        raise ValueError('unsupported receiving capacity')
    if any(type(ob[k]) is not int or ob[k]<0 for k in COUNTS):
        raise ValueError('invalid six counts')
    for pos,num in [('approach_A_positions','approach_A'),('approach_B_positions','approach_B'),('pocket_positions','pocket_vehicles'),('receiver_occupied_cells','receiver_vehicles')]:
        values=ob[pos]
        if not isinstance(values,list) or len(values)!=ob[num] or any(type(x) is not int for x in values) or len(values)!=len(set(values)):
            raise ValueError('invalid occupancy array: '+pos)
    indices=ob['receiver_occupied_cells']
    if any(x<0 or x>=c for x in indices) or ob['receiver_vehicles']>c:
        raise ValueError('invalid receiver physical capacity')
    if ob['receiver_vehicles']==c and 0 not in indices:
        raise ValueError('full receiving link must occupy entry cell')
    for p in (0,60,120):
        if row[f'delta_p{p}']!=row[f'cost_treatment_p{p}']-row[f'cost_baseline_p{p}']:
            raise ValueError('inconsistent paired cost')


def key_for(row,mode='strict'):
    o=row['decision_observation']
    prefix=(row['capacity'],row['pocket_m'])
    if mode in ('strict','strict_positions'):prefix+=(row['b_share'],)
    elif mode!='drop_b_share':raise ValueError('unknown mode')
    key=prefix+tuple(o[k] for k in COUNTS)
    if mode=='strict_positions':
        key+=tuple(tuple(o[p]) for p in ('pocket_positions','approach_A_positions','approach_B_positions','receiver_occupied_cells'))
    return key


def screen(rows,epsilon=5,penalty=60,mode='strict'):
    if type(epsilon) is not int or epsilon<0 or penalty not in (0,60,120):
        raise ValueError('unsupported model threshold')
    groups=collections.defaultdict(list)
    for r in rows:
        validate(r)
        groups[key_for(r,mode)].append(r)
    witnesses=[];duplicates=0;duplicate_rows=0
    for key,group in sorted(groups.items()):
        if len(group)>1:
            duplicates+=1;duplicate_rows+=len(group)
        n=[r for r in group if r[f'delta_p{penalty}'] < -epsilon]
        p=[r for r in group if r[f'delta_p{penalty}'] > epsilon]
        if n and p:
            witnesses.append({
                'key':list(key),'negative':[{'seed':r['seed'],'b_share':r['b_share'],'delta':r[f'delta_p{penalty}'],'approach_B_positions':r['decision_observation']['approach_B_positions']} for r in n],
                'positive':[{'seed':r['seed'],'b_share':r['b_share'],'delta':r[f'delta_p{penalty}'],'approach_B_positions':r['decision_observation']['approach_B_positions']} for r in p],
                'independent_seed_identifiers':len({r['seed'] for r in n+p}),
                'independent_arrival_tapes_verified':False,
            })
    return {'mode':mode,'penalty':penalty,'epsilon':epsilon,'rows':len(rows),
            'observation_groups':len(groups),'collision_groups':duplicates,
            'collision_rows':duplicate_rows,'opposition_groups':len(witnesses),
            'witnesses':witnesses,
            'scope':'HISTORICAL_SOURCE_DERIVED_SYNTHETIC_NOT_NEW_PHYS_RUN_NOT_CSI'}


def audit_zip(zip_path):
    with open(zip_path,'rb') as f:zip_sha=hashlib.sha256(f.read()).hexdigest()
    if zip_sha!=EXPECTED_SHA256:
        raise ValueError('wrong historical evidence ZIP (SHA-256 mismatch)')
    with zipfile.ZipFile(zip_path) as z:
        if z.testzip() is not None:raise ValueError('corrupt member')
        raw=z.read(SOURCE)
    result_sha=hashlib.sha256(raw).hexdigest()
    if result_sha!=EXPECTED_RESULT_SHA256:raise ValueError('wrong PHYS-04 result JSON')
    data=json.loads(raw)
    if data['checkpoint_identity_cases']!=144 or data['mismatches'] or data['reference_compared_fields']!=13:
        raise ValueError('prior parity record inconsistent')
    rows=data['pairs']
    if len(rows)!=144:raise ValueError('wrong row count')
    outputs=[screen(rows,epsilon=eps,penalty=p,mode=mode)
             for mode in ('strict','strict_positions','drop_b_share') for eps in (0,5,20) for p in (0,60,120)]
    return {'archive_sha256':zip_sha,'result_sha256':result_sha,'original_provenance':data['provenance'],
            'historical_parity_record':{'checkpoint_identity_cases':144,'mismatches':0,'independent_reference_fields_per_case':13},
            'comparisons':outputs}


if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('evidence_zip')
    ap.add_argument('output_json')
    args=ap.parse_args()
    with open(args.output_json,'w',encoding='utf-8') as f:
        json.dump(audit_zip(args.evidence_zip),f,sort_keys=True,indent=2,ensure_ascii=False)
        f.write('\n')
