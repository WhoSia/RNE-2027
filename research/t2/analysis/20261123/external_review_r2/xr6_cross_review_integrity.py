"""XR6 post-hoc review reconciliation: NOT a new simulation or prereg.

Read XR1/XR2/XR3/XR5 results from external_review_r2 and P135 baseline,
then check logical interpretation, paired topology transitions, overlapping
arrival tapes, and fidelity/independence gates. No T2 engine import.
"""
import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent / 'src/research/t2/analysis/20261123'
XR = ROOT / 'external_review_r2'


def audit(xr1, xr2, xr3, xr5, p135):
    assert xr1['arms_primary'] == 1152 and len(xr1['rows']) == 576
    assert xr2['configs'] == 64 and xr2['t2_arms'] == 5760
    assert xr3['status'] == 'E0_PARITY_FAILED_E0e_EXITS'
    assert xr5['rule_falsified'] is True
    assert p135['simulator_arms'] == 128 and len(p135['rows']) == 64
    assert xr1['verdict'] == 'STRONG_ATTENUATION_WITH_RESIDUAL'
    grouped = defaultdict(dict)
    for r in xr1['rows']:
        key = (r['share'], r['capacity'], r['label_seed'], r['time_seed'], r['family'])
        assert r['topology'] not in grouped[key]
        grouped[key][r['topology']] = r
    assert len(grouped) == 192
    by_cell = {}
    for share in (.25, .50, .75):
        for capacity in (4, 8):
            matched = [v for k, v in grouped.items() if k[:2] == (share, capacity)]
            assert len(matched) == 32
            assert all(set(v) == {'shared', 'split_same_clock', 'split_left_free'} for v in matched)
            n = lambda top: sum(v[top]['paradox'] for v in matched)
            by_cell[f'{share}/C{capacity}'] = {
                'matched_tapes': 32, 'shared_paradox': n('shared'),
                'split_same_clock_paradox': n('split_same_clock'),
                'split_left_free_paradox': n('split_left_free'),
                'shared_true_to_split_false': sum(v['shared']['paradox'] and not v['split_same_clock']['paradox'] for v in matched),
                'shared_false_to_split_true': sum(not v['shared']['paradox'] and v['split_same_clock']['paradox'] for v in matched),
                'shared_true_and_split_true': sum(v['shared']['paradox'] and v['split_same_clock']['paradox'] for v in matched),
                'split_short_cost_worse': sum(v['split_same_clock']['delta_cost'] > 0 for v in matched),
            }
    assert by_cell['0.75/C4']['shared_paradox'] == 32
    assert by_cell['0.75/C4']['split_same_clock_paradox'] == 7
    assert by_cell['0.75/C4']['shared_true_to_split_false'] == 25
    assert by_cell['0.5/C4']['split_same_clock_paradox'] == 2
    assert by_cell['0.5/C8']['split_left_free_paradox'] == 8
    assert by_cell['0.75/C8']['split_left_free_paradox'] == 6
    # Every P135 tape is contained in XR1, despite XR1 claiming unseen timing seeds.
    p135_tapes = {(r['share'], r['label_seed'], r['time_seed'], r['family']) for r in p135['rows']}
    xr1_tapes = {(r['share'], r['label_seed'], r['time_seed'], r['family']) for r in xr1['rows']}
    assert len(p135_tapes) == 32 and len(xr1_tapes) == 96
    assert p135_tapes <= xr1_tapes
    assert sorted({k[2] for k in p135_tapes}) == [88401, 88402, 88403, 88404]
    assert sorted({k[2] for k in xr1_tapes}) == list(range(88401, 88409))
    assert xr2['by_stratum']['0.75/C8']['red_onset_M1_agrees'] == 1
    assert xr2['pooled']['M1']['strict_n'] > 100000
    for arm in xr3['arms'].values():
        assert not arm['gates']['E0e_exits'] and not arm['all_pass']
    return {
        'status': 'XR6_POSTHOC_CROSS_REVIEW_AUDIT', 'new_simulator_arms': 0,
        'by_cell': by_cell,
        'p135_unique_tapes': len(p135_tapes), 'p135_tapes_reused_in_xr1': len(p135_tapes),
        'xr1_unique_tapes': len(xr1_tapes),
        'xr1_prereg_necessity_gate_not_logically_sufficient': True,
        'xr1_75_C4_split_residual': '7/32',
        'xr2_pooled_M1_accuracy': xr2['pooled']['M1']['strict_accuracy'],
        'xr2_strict_comparisons_not_independent': xr2['pooled']['M1']['strict_n'],
        'xr2_distinct_configurations': xr2['configs'],
        'xr2_75_C8_red_onset_M1_agrees': xr2['by_stratum']['0.75/C8']['red_onset_M1_agrees'],
        'xr2_75_C8_red_onset_n': 16,
        'xr3_all_parity_gates_pass': False,
        'xr5_threshold_rule_falsified': True,
        'limitations': 'Code-only reaggregation: no new T2 or SUMO executions. XR1 and P135 share every P135 tape (though different network interventions); XR2 pooled pairwise comparisons are highly dependent within 64 configs / 16 timestamp roots. Does not refute the descriptive 25/32 attenuation under split same clock; rejects logical necessity only.'
    }


def main():
    get = lambda path: json.loads(path.read_text())
    result = audit(*[get(XR / f'XR{i}_RESULT.json') for i in (1, 2, 3, 5)], get(ROOT / 'P135_RESULT.json'))
    (XR / 'XR6_CROSS_REVIEW_AUDIT_RESULT.json').write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n')
    print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == '__main__': main()
