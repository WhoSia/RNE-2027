"""P92: independently executable queue negative control for 'effective green = departures'.

This is a pedagogical single FIFO with 2-second service headway, not the
four-cell T2 receiver. Run: python p92_exposure_negative_control.py > P92_RESULT.json
"""
import json

START, STOP, LOSS, HEADWAY = 84, 684, 2, 2
PERIODS = (30, 60)

def green(t, period):
    phase = (t - START) % period
    return LOSS <= phase < period // 2

def simulate(arrivals, period):
    events = {}
    for t in arrivals:
        assert START <= t < STOP
        events[t] = events.get(t, 0) + 1
    waiting = 0
    exited = 0
    cumulative_queue_seconds = 0
    last = -10**9
    last_exit = None
    for t in range(START, STOP):
        waiting += events.get(t, 0)
        if waiting and green(t, period) and t-last >= HEADWAY:
            waiting -= 1
            exited += 1
            last = t
            last_exit = t
        cumulative_queue_seconds += waiting
    nominal = sum((t-START) % period < period//2 for t in range(START, STOP))
    effective = sum(green(t, period) for t in range(START, STOP))
    return dict(nominal_green_seconds=nominal, service_eligible_seconds=effective,
                departures=exited, remaining=waiting, queue_vehicle_seconds=cumulative_queue_seconds,
                last_exit_second=last_exit)

def experiment():
    demands = {
        "empty": [],
        "sparse": [START+10+60*i for i in range(5)],
        "single_initial_platoon_80": [START]*80,
        "uniform_90": [START+2*i for i in range(90)],
    }
    rows = []
    for label, arrivals in demands.items():
        outcomes = {str(p):simulate(arrivals,p) for p in PERIODS}
        assert outcomes["30"]["remaining"] == outcomes["60"]["remaining"] == 0
        assert outcomes["30"]["departures"] == outcomes["60"]["departures"] == len(arrivals)
        assert outcomes["30"]["nominal_green_seconds"] == outcomes["60"]["nominal_green_seconds"] == 300
        assert outcomes["30"]["service_eligible_seconds"] == 260
        assert outcomes["60"]["service_eligible_seconds"] == 280
        rows.append(dict(demand=label,generated=len(arrivals),outcomes=outcomes,
                         delta_queue_vehicle_seconds=outcomes["30"]["queue_vehicle_seconds"]-outcomes["60"]["queue_vehicle_seconds"]))
    assert rows[0]["delta_queue_vehicle_seconds"] == 0
    return dict(model="independent transparent FIFO negative control, not calibrated T2",
                interval="[84,684)", lost_green_seconds_per_onset=LOSS,
                headway_seconds=HEADWAY, rows=rows)

if __name__ == "__main__":
    print(json.dumps(experiment(),indent=2))
