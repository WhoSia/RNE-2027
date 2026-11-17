"""Mechanism counts using the protected-stage engine's pre-service observer."""
from signal_model import run


def assess(plan, scenario):
    pedestrian_area = pedestrian_red_ticks = 0
    downstream_blocked = approach_blocked = 0

    def observe(t, arrivals, source, bay, link, pedestrians, permitted, entry, exit_now):
        nonlocal pedestrian_area, pedestrian_red_ticks, downstream_blocked, approach_blocked
        pedestrian_area += pedestrians - int(pedestrians > 0 and 6 in permitted)
        pedestrian_red_ticks += int(pedestrians > 0 and 6 not in permitted)
        downstream_blocked += sum(m < 6 and bay[m] > 0 and link[m] == scenario.link[m]
                                  for m in permitted)
        approach_blocked += sum(bool(q) and bay[q[0]] == scenario.bay[q[0]] for q in source)

    result = run(plan, scenario, observe=observe)
    return {
        "cost": result.cost,
        "vehicle_time_area": result.area - pedestrian_area * scenario.weights[6],
        "pedestrian_wait_area": pedestrian_area,
        "pedestrian_wait_red_ticks": pedestrian_red_ticks,
        "vehicle_unfinished": sum(result.remaining[:6]),
        "pedestrian_unfinished": result.remaining[6],
        "downstream_blocked_opportunities": downstream_blocked,
        "approach_head_blocked_ticks": approach_blocked,
    }
