"""XR7: per-vehicle T2âSUMO timing-stage audit. Requires SUMO to execute.

No SUMO policy-sign inference is permitted unless ALL matching gates pass.
The pure `analyze` helper is independently unit-testable without SUMO.
"""
from pathlib import Path
from collections import defaultdict
import json
import statistics

HERE = Path(__file__).resolve().parent


def quantile90(values):
    values = sorted(abs(x) for x in values)
    if not values:
        return None
    return values[int(.9 * (len(values) - 1))]


def distribution(values):
    data = [abs(x) for x in values]
    if not data:
        return {'n': 0, 'median_abs': None, 'p90_abs': None, 'max_abs': None, 'n_abs_over_3s': 0}
    return {'n': len(data), 'median_abs': statistics.median(data),
            'p90_abs': quantile90(data), 'max_abs': max(data),
            'n_abs_over_3s': sum(x > 3 for x in data)}


def analyze(tape, ref, depart, crossing, exits):
    """All inputs keyed with native T2 integer IDs or SUMO vXX IDs, never ordinal order."""
    ids = list(range(len(tape)))
    missing = defaultdict(list)
    rows = []
    for i in ids:
        name = f'v{i:02d}'
        signals = {'t2_admission': ref['admit'].get(i), 't2_stopline': ref['cross'].get(i),
                   't2_exit': ref['exit'].get(i), 'sumo_admission': depart.get(name),
                   'sumo_stopline': crossing.get(name), 'sumo_exit': exits.get(name)}
        absent = [k for k, v in signals.items() if v is None]
        if absent:
            missing[name] = absent
            continue
        au = signals['sumo_admission'] - signals['t2_admission']
        us = (signals['sumo_stopline'] - signals['sumo_admission']) - (signals['t2_stopline'] - signals['t2_admission'])
        se = (signals['sumo_exit'] - signals['sumo_stopline']) - (signals['t2_exit'] - signals['t2_stopline'])
        total = signals['sumo_exit'] - signals['t2_exit']
        assert abs((au + us + se) - total) < 1e-8, (name, au, us, se, total)
        rows.append({'vehicle_id': i, 'movement': tape[i][1], 'arrival_tape_s': tape[i][0],
                     **signals, 'admission_error_s': au, 'upstream_segment_error_s': us,
                     'receiver_segment_error_s': se, 'stopline_error_s': signals['sumo_stopline']-signals['t2_stopline'],
                     'exit_error_s': total})
    stats = {}
    for movement in ('ALL', 'L', 'S'):
        sub = rows if movement == 'ALL' else [r for r in rows if r['movement'] == movement]
        stats[movement] = {field: distribution([r[field] for r in sub]) for field in
                           ('admission_error_s','upstream_segment_error_s','receiver_segment_error_s',
                            'stopline_error_s','exit_error_s')}
    all_known = len(rows) == len(tape) and not missing
    g = {'D1_all_ids_have_all_timestamps': all_known,
         'D3_admission_p90_abs_le_1s': all_known and stats['ALL']['admission_error_s']['p90_abs'] <= 1,
         'D4_stopline_p90_abs_le_3s': all_known and stats['ALL']['stopline_error_s']['p90_abs'] <= 3,
         'D4_exits_p90_abs_le_10s': all_known and stats['ALL']['exit_error_s']['p90_abs'] <= 10}
    return {'status': 'XR7_PER_ID_DIAGNOSTIC_COMPLETE' if all_known else 'XR7_MISSING_ID_TIMESTAMPS',
            'tape_vehicles': len(tape), 'matched_vehicles': len(rows),
            'missing_per_id': dict(missing), 'stats':stats, 'gates':g,
            'policy_sign_comparison_allowed': False, 'rows': rows,
            'note': 'D5 native T2 score must be externally checked before the policy-sign gate can be reconsidered.'}


def main():
    # Import SUMO only inside the runtime path: pure tests run without SUMO.
    from dataclasses import replace
    from tempfile import TemporaryDirectory
    from unittest.mock import patch
    from xr3_sumo_parity import t2_reference, calendars, build, simulate
    from p85_signal_coordination import build_config, run, phases, score
    from p118_temporal_arrival_holdout import tape_with_random_times
    from receiving_cells_v15 import ReceivingCells

    seed, ts, family, share, cap = 86001, 88501, 'stochastic_uniform', .75, 4
    tape = tape_with_random_times(build_config(seed,900,share,7,4,.5),seed,ts,family)
    cfg = build_config(seed,900,share,7,cap,.5)
    cfg = replace(cfg,base=replace(cfg.base,duration_s=4800))
    result={'status':'XR7_EXECUTION_STARTED','world':{'label_seed':seed,'time_seed':ts,'family':family,
            'share':share,'capacity':cap},'arms':{}}
    for period, phi in ((30,15),(60,30)):
        ref=t2_reference(cfg,tape,period,phi)
        cp=run(cfg,tape,checkpoint_at=84,trace=True)
        def green(self,t): return ((t-84+phi)%period)<period//2
        with patch.object(ReceivingCells,'green',green):
            native=run(cfg,tape,resume_from=cp,phase_overrides=phases(6,'left_first'),trace=True)
        native_cost=score(native,0)
        d5=native_cost==ref['cost']
        up,down=calendars(cfg,period,phi)
        with TemporaryDirectory() as directory:
            build(directory,cfg,tape,ref,period,phi)
            depart,exits,cross,max_rcv,signal_bad=simulate(directory,tape,up,down)
        entry=analyze(tape,ref,depart,cross,exits)
        entry['gates']['D5_T2_score_equals_reconstructed_exit_cost']=d5
        entry['gates']['XR3_signal_calendar_match']=signal_bad==0
        entry['gates']['XR3_receiver_reaches_capacity']=max_rcv==cap
        entry['policy_sign_comparison_allowed']=all(entry['gates'].values())
        entry['native_t2_cost']=native_cost
        entry['reconstructed_t2_cost']=ref['cost']
        entry['sumo_signal_mismatch_samples']=signal_bad
        entry['sumo_max_receiver']=max_rcv
        result['arms'][f'{period}/phi{phi}']=entry
        print('XR7',period,phi,entry['gates'],flush=True)
    result['policy_sign_comparison_allowed']=all(a['policy_sign_comparison_allowed'] for a in result['arms'].values())
    result['status']='XR7_ALL_PARITY_GATES_PASS' if result['policy_sign_comparison_allowed'] else 'XR7_PARITY_FAILED_NO_POLICY_SIGN_COMPARISON'
    (HERE/'XR7_RESULT.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print('XR7_SUMMARY',result['status'],flush=True)

if __name__=='__main__':main()
