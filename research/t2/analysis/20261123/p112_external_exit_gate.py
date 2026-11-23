"""P112: strict adapter for *independently generated* terminal-exit CSV evidence.

This verifier does not run SUMO. Mock fixtures in tests are clearly labeled
T2-derived; they prove the gate rejects invalid external data, not equivalence.

CSV fields: seed,family,onset,period_s,vehicle_id,movement,arrival_second,exit_second
Each row is one FINAL network/receiver endpoint crossing in the external model.
"""
import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path

REQUIRED=('seed','family','onset','period_s','vehicle_id','movement','arrival_second','exit_second')


def audit(manifest, external_rows):
    tapes={(t['seed'],t['family']):t for t in manifest['tapes']}
    arms={(a['seed'],a['family'],a['onset'],a['period_s']):a for a in manifest['arms_data']}
    assert len(tapes)==manifest['unique_arrival_tapes'] and len(arms)==manifest['arms']
    indexed=defaultdict(dict)
    failures=[]
    for line,row in enumerate(external_rows,2):
        try:
            key=(int(row['seed']),row['family'],row['onset'],int(row['period_s']))
            vid=int(row['vehicle_id'])
            arrival=int(row['arrival_second'])
            departure=float(row['exit_second'])
            move=row['movement']
            assert key in arms, 'unregistered policy arm'
            expected=tapes[key[:2]]['events']
            assert 0<=vid<len(expected), 'vehicle ID out of range'
            assert vid not in indexed[key], 'duplicate final vehicle exit'
            assert arrival==expected[vid]['enter_time_s'], 'arrival-tape timestamp mismatch'
            assert move==expected[vid]['movement'], 'turn-route mismatch'
            assert departure>=arrival, 'exit before arrival'
            assert departure < 1440, 'exit beyond preregistered horizon (censoring)'
            indexed[key][vid]=(arrival,departure,move)
        except (ValueError,TypeError,KeyError,AssertionError) as error:
            failures.append({'line':line,'reason':str(error)})
    per_arm=[]
    for key,ref in sorted(arms.items()):
        t=tapes[key[:2]]['events'];actual=indexed[key]
        expected_ids=set(range(len(t)))
        missing=sorted(expected_ids-set(actual))
        if missing:
            failures.append({'arm':key,'reason':'missing terminal vehicle IDs','n_missing':len(missing),
                             'sample_ids':missing[:5]})
        if not missing:
            per_arm.append({'seed':key[0],'family':key[1],'onset':key[2],
                            'period_s':key[3],
                            'sum_external_residence_seconds':sum(d-a for a,d,_ in actual.values()),
                            'n':len(actual)})
    if failures:
        return {'status':'REJECTED_EXTERNAL_EVIDENCE','passed':False,
                'failure_count':len(failures),'failures':failures[:20],
                'complete_arms':len(per_arm),'required_arms':len(arms),
                'policy_comparison_allowed':False}
    by={(a['seed'],a['family'],a['onset'],a['period_s']):a for a in per_arm}
    contrasts=[]
    for seed,family in sorted(tapes):
        for onset in ('green','red'):
            short=by[seed,family,onset,30]
            long=by[seed,family,onset,60]
            refshort=arms[seed,family,onset,30]
            reflong=arms[seed,family,onset,60]
            ext=short['sum_external_residence_seconds']-long['sum_external_residence_seconds']
            t2=refshort['t2_cost']-reflong['t2_cost']
            contrasts.append({'seed':seed,'family':family,'onset':onset,
                              'external_cost_delta_30_minus_60':ext,
                              't2_cost_delta_30_minus_60':t2,
                              'sign_agrees':(ext>0)-(ext<0)==(t2>0)-(t2<0)})
    return {'status':'EXTERNAL_EVENT_CSV_SCHEMA_COMPLETE_ONLY','passed':True,
            'failure_count':0,'complete_arms':len(per_arm),'required_arms':len(arms),
            'contrasts':contrasts,'sign_agreement':sum(x['sign_agrees'] for x in contrasts),
            'physical_equivalence_verified':False,'policy_comparison_allowed':False,
            'warning':'This gate checks matched events, not physical geometry or signal parity. E0 must be approved separately.'}


def load_csv(path):
    with open(path,newline='',encoding='utf-8') as f:
        reader=csv.DictReader(f)
        if set(REQUIRED)-set(reader.fieldnames or ()):raise ValueError('missing columns')
        return list(reader)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--manifest',type=Path,default=Path(__file__).with_name('P111_RESULT.json'))
    parser.add_argument('--external-csv',type=Path,required=True)
    args=parser.parse_args()
    result=audit(json.loads(args.manifest.read_text(encoding='utf-8')),load_csv(args.external_csv))
    print(json.dumps(result,ensure_ascii=False,indent=2))
    if not result['passed']:raise SystemExit(2)


if __name__=='__main__':main()
