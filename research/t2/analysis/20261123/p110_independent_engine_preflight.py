"""P110 executable physical-parity gate for P100 T2-to-SUMO transport.

The program explicitly refuses to assert parity without an independent SUMO
runtime and a corresponding calibrated physical-network/route artifact.
It does NOT run SUMO or accept a previous non-identical intervention as proof.

Run with research/t2 and analysis/20261122 on PYTHONPATH.
"""
import importlib.util
import json
import shutil
from dataclasses import asdict
from pathlib import Path
from p85_signal_coordination import build_config, p31
from spatial_v10 import validate

HERE=Path(__file__).resolve().parent


def experiment():
    c=build_config(86001,900,.75,7,4,.5)
    n,k=validate(c.base)
    assert c.base.pocket_length_m==7 and c.base.cell_m==7 and k==1
    assert c.base.approach_length_m==140 and n==20
    assert c.receiver_slots==4 and c.receiver_headway_s==2
    assert c.through_B_share==.5 and c.allow_lane_changes
    tape=p31.clock(c.base,'uniform')
    assert tape and all(m in ('L','S') for _,m in tape)
    repo=HERE.parents[1]
    sumo=shutil.which('sumo')
    netconvert=shutil.which('netconvert')
    traci=importlib.util.find_spec('traci') is not None
    sumolib=importlib.util.find_spec('sumolib') is not None
    available={'sumo_executable':bool(sumo),'netconvert_executable':bool(netconvert),
               'traci_python':traci,'sumolib_python':sumolib}
    # Presence is required but never sufficient. No equivalence is inferred from package availability.
    gate={
      'identical_arrival_times_and_vehicle_IDs':'NOT_TESTED_IN_SUMO',
      'lane_A_B_and_turn_route_geometry':'NOT_TESTED_IN_SUMO',
      'pocket_length_7m_not_7_cells':'SOURCE_CONFIRMED_ONLY',
      'finite_4_cell_receiver_equivalent_storage':'NOT_TESTED_IN_SUMO',
      'green_red_30_60_onset_at_t84':'NOT_TESTED_IN_SUMO',
      'upstream_left_first_6s_and_clearance':'NOT_TESTED_IN_SUMO',
      'cellular_1s_tick_vs_micro_headway':'NOT_TESTED_IN_SUMO',
      'matched_initial_state_at_84':'NOT_TESTED_IN_SUMO',
      'per_ID_end_of_receiving_segment_event':'NOT_TESTED_IN_SUMO',
      'pedestrian_and_opposing_flow':'NOT_MODELED_IN_T2',
    }
    if not all(available.values()):
        status='BLOCKED_NO_SUMO_RUNTIME'
    else:
        status='PENDING_PHYSICAL_NETWORK_EQUIVALENCE'
    return dict(source='actual P100 T2 build_config and runtime validate',
        engine_status=status,
        runtime_presence=available,
        t2_source_locked_geometry={
          'cell_length_m':c.base.cell_m,'approach_length_m':c.base.approach_length_m,
          'approach_cells_per_lane':n,'pocket_length_m':c.base.pocket_length_m,
          'pocket_cells':k,'receiver_cells':c.receiver_slots,
          'nominal_receiver_length_if_same_cell_m':c.receiver_slots*c.base.cell_m,
          'receiver_discharge_headway_s':c.receiver_headway_s,
          'upstream_approach_green_mode':'left-first, 6s left (overridden after t84)',
          'downstream_cycle_options_s':[30,60], 'downstream_green_fraction':.5,
          'decision_tick':84,'warmup_is_checkpoint_with_identical_events':True,
          'through_B_share':c.through_B_share,'lane_change_zone_m':c.change_zone_m,
          'allow_lane_changes':c.allow_lane_changes,
          'change_gap_cells':c.lane_change_target_gap_cells,
          'change_confirmation_s':c.lane_change_gap_confirmation_s,
          'seed':86001, 'arrivals_on_tape':len(tape)},
        parity_gates=gate,
        policy_effect_compare_allowed=False,
        reason='SUMO package availability cannot prove equivalence; policy sign analysis strictly forbidden until E0 geometry, signal and per-ID routes are locked.',
        past_sumo_p71='Different 10s-versus-6s upstream intervention with unmatched downstream geometry; cannot be reused as P100 matched intervention')


if __name__=='__main__':
    print(json.dumps(experiment(),ensure_ascii=False,indent=2))
