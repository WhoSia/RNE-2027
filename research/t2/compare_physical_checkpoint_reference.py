"""Compare the canonical PHYS-04 capacity run with an independent reference.

Usage:
 PYTHONPATH=research/t2 python research/t2/compare_physical_checkpoint_reference.py \
    canonical_capacity_screen.json reference_capacity2.json \
    reference_capacity4.json reference_capacity8.json

This fails closed if a key, score, exit tally, or remaining count differs.
The reference JSONs must be independently obtained and their provenance
recorded. A successful match demonstrates implementation agreement, not
field validation or model correctness.
"""
import argparse
import json
from pathlib import Path

CAPACITIES=(2,4,8)


def compare(canonical,references):
    observed={}
    for row in canonical['pairs']:
        key=(row['capacity'],row['seed'],row['pocket_m'],row['b_share'])
        if key in observed:
            raise AssertionError(('duplicate canonical pair',key))
        observed[key]=row
    expected={}
    for capacity,reference in zip(CAPACITIES,references):
        if reference.get('provenance')!='INDEPENDENT_REIMPLEMENTATION_NOT_CANONICAL_GITHUB_ENGINE':
            raise AssertionError(('invalid reference provenance',capacity))
        if reference.get('capacity')!=capacity:
            raise AssertionError(('reference capacity mismatch',capacity))
        for row in reference['rows']:
            key=(capacity,row['seed'],row['pocket_m'],row['b_share'])
            if key in expected:
                raise AssertionError(('duplicate reference pair',key))
            expected[key]=row
    if set(observed)!=set(expected) or len(observed)!=144:
        raise AssertionError(('pair key set differs',len(observed),len(expected)))
    fields={
        'cost_baseline_p60':'baseline_cost',
        'cost_treatment_p60':'treatment_cost',
        'delta_p60':'delta',
        'delta_p0':'delta_p0',
        'delta_p120':'delta_p120',
        'baseline_remaining':'baseline_remaining',
        'treatment_remaining':'treatment_remaining',
        'baseline_out_S':'baseline_out_S',
        'baseline_out_L':'baseline_out_L',
        'treatment_out_S':'treatment_out_S',
        'treatment_out_L':'treatment_out_L',
        'baseline_bypass':'baseline_lane_changes',
        'treatment_bypass':'treatment_lane_changes'}
    mismatches=[]
    for key in sorted(expected):
        real=observed[key]
        ref=expected[key]
        for actual_field,ref_field in fields.items():
            if real[actual_field]!=ref[ref_field]:
                mismatches.append((key,actual_field,real[actual_field],ref[ref_field]))
    return mismatches


if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('canonical',type=Path)
    p.add_argument('reference2',type=Path)
    p.add_argument('reference4',type=Path)
    p.add_argument('reference8',type=Path)
    args=p.parse_args()
    files=(args.reference2,args.reference4,args.reference8)
    canonical=json.loads(args.canonical.read_text(encoding='utf-8'))
    refs=[json.loads(f.read_text(encoding='utf-8')) for f in files]
    diffs=compare(canonical,refs)
    if diffs:
        print('MISMATCHES',len(diffs))
        for row in diffs[:30]:
            print(row)
        raise SystemExit(1)
    print('PASS: canonical vs independent reference, 144/144 paired cases, all mapped fields')
