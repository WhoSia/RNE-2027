"""Independent receiver-cell event shadow audit of canonical synthetic T2 frames.

Not a SUMO run, empirical measurement, or legal signal plan. Reconstructs
receiver-state transitions from public frames + stopline-crossing events,
without calling ReceivingCells or modifying the underlying simulator.
"""
from collections import defaultdict


class LedgerViolation(AssertionError):
    pass


def audit_trace(config, tape, result):
    if config.receiver_mode != 'cells' or config.receiver_slots < 1:
        raise ValueError('explicit finite cellular receiver is required')
    duration = config.base.duration_s
    frames = result['frames']
    if len(frames) != duration or not all(frame['t'] == i for i, frame in enumerate(frames)):
        raise LedgerViolation('missing or out-of-order frames')
    by_service = defaultdict(list)
    for event in result['service_events']:
        by_service[event['t']].append(event)
    by_access = defaultdict(list)
    for event in result['access_events']:
        by_access[event['t']].append(event)
    by_lane_change = defaultdict(list)
    for event in result['lane_change_events']:
        by_lane_change[event['t']].append(event)
    occupied = {}  # cell -> (vehicle id, movement)
    last_exit = -10**9
    left_network = []
    admitted_to_receiver = []
    denied_attempts = 0
    prev_road = {}
    rows = []
    for t, frame in enumerate(frames):
        # Independent automaton: departure -> synchronous shift -> admission.
        c = config
        is_green = ((t+c.downstream_offset_s) % c.downstream_cycle_s < c.downstream_green_s
                    and not any(a <= t < b for a,b in c.receiver_closures))
        if (is_green and c.receiver_slots-1 in occupied and
                t-last_exit >= c.receiver_headway_s):
            vehicle = occupied.pop(c.receiver_slots-1)
            left_network.append((t, vehicle[0], vehicle[1]))
            last_exit = t
        old = dict(occupied)
        occupied = {idx+1 if idx+1 not in old and idx+1 < c.receiver_slots else idx: vehicle
                    for idx, vehicle in old.items()}
        incoming = [e for e in by_service[t] if e['reason'] == 'stopline_cross']
        for event in incoming:
            if 0 in occupied:
                raise LedgerViolation(f't={t}: crossing while cell0 occupied')
            vehicle = (event['vehicle_id'], event['movement'])
            occupied[0] = vehicle
            admitted_to_receiver.append((t,*vehicle))
        denied = [e for e in by_service[t]
                  if e['reason'] in ('receiver_entry_cell_busy','receiver_capacity_full')]
        for event in denied:
            denied_attempts += 1
            if 0 not in occupied:
                raise LedgerViolation(f't={t}: denial while entry clear')
        reference = {cell:(vehicle_id,route) for cell,vehicle_id,route in frame['receiver']}
        if occupied != reference:
            raise LedgerViolation(f't={t}: independent receiver shadow differs from frame')
        road = {}
        for lane in ('A','B'):
            for x,vid,movement in frame[lane]:
                if vid in road:raise LedgerViolation(f't={t}: duplicate road ID')
                road[vid]=(lane,x,movement)
        for x,vid in frame['pocket']:
            if vid in road:raise LedgerViolation(f't={t}: duplicate pocket ID')
            road[vid]=('pocket',x,'L')
        if len(road) != len(frame['A'])+len(frame['B'])+len(frame['pocket']):
            raise LedgerViolation('duplicate road record')
        if set(road) & {v[0] for v in occupied.values()}:
            raise LedgerViolation(f't={t}: simultaneous road and receiver occupancy')
        for vid, (lane,x,movement) in road.items():
            if vid in prev_road:
                old_lane,old_x,old_movement=prev_road[vid]
                if movement != old_movement:
                    raise LedgerViolation(f't={t}: movement label changed')
                if (lane == old_lane or (old_lane == 'A' and lane == 'B')) and x not in (old_x,old_x+1):
                    raise LedgerViolation(f't={t}: unphysical lane displacement')
                if old_lane == 'A' and lane == 'pocket' and x != old_x+1:
                    raise LedgerViolation(f't={t}: pocket jump')
                if (lane != old_lane and not (old_lane == 'A' and lane in ('B','pocket'))):
                    raise LedgerViolation(f't={t}: unexpected lateral move')
        for event in by_lane_change[t]:
            vid = event['vehicle_id']
            if vid not in road or road[vid][:2] != ('B',event['cell']):
                raise LedgerViolation(f't={t}: lane change absent from final frame')
        for event in by_access[t]:
            if event['event']=='pocket_entry':
                if event['vehicle_id'] not in road or road[event['vehicle_id']][0] != 'pocket':
                    raise LedgerViolation(f't={t}: pocket entry not present')
            elif event['event']=='pocket_entry_denied' and event['reason']=='pocket_entry_cell_busy':
                if event['blocker_id'] not in road or road[event['blocker_id']][0] != 'pocket':
                    raise LedgerViolation(f't={t}: reported blocker absent')
        generated_by_t = sum(arrival_t <= t for arrival_t,_ in tape)
        current = len(road)+len(occupied)+frame['outside']
        if current + len(left_network) != generated_by_t:
            raise LedgerViolation(f't={t}: reconstructed conservation failure')
        rows.append({'t':t,'receiver_size':len(occupied),'outside':frame['outside'],
                     'road_size':len(road),'cumulative_network_exits':len(left_network),
                     'receiver_entry_attempts':len(incoming)+len(denied)})
        prev_road=road
    if len(admitted_to_receiver) != result['exit_L'] + result['exit_S']:
        raise LedgerViolation('crossing event vs engine count mismatch')
    if denied_attempts != result['receiver_denied_attempts']:
        raise LedgerViolation('receiver denial event vs engine count mismatch')
    if len(left_network) != result['network_out_L']+result['network_out_S']:
        raise LedgerViolation('network exit vs engine count mismatch')
    return {'status':'EXACT_SIMULATED_EVENT_LEDGER_NO_EXTERNAL_MODEL',
            'ticks':duration,'generated':len(tape),
            'receiver_admissions':len(admitted_to_receiver),
            'receiver_exits':len(left_network),'receiver_denials':denied_attempts,
            'last_tick_conservation':rows[-1],
            'receiver_exit_events':left_network,
            'receiver_entry_events':admitted_to_receiver}
