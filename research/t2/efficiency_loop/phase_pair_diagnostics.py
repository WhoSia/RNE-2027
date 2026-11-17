"""Crossing brackets, movement totals, and per-vehicle paired contrasts."""

from sumo_phase_pair import DEMAND, HORIZON, outcome


def movement_state(cycle, stamp, movement):
    index = ("T", "L").index(movement)
    elapsed = stamp % sum(duration for duration, _ in cycle)
    for duration, state in cycle:
        if elapsed < duration:
            return state[index]
        elapsed -= duration
    raise ValueError("invalid phase timeline")


def bracket_state(cycle, low, high, movement):
    states = (movement_state(cycle, low, movement), movement_state(cycle, high, movement))
    return states[0] if states[0] == states[1] else "transition:" + ">".join(states)


def paired_departure_cost(lag, lead):
    lag_outcome, lead_outcome = map(outcome, (lag, lead))
    costs = {}
    for trip in DEMAND:
        a, b = lag.get(trip.ident, HORIZON), lead.get(trip.ident, HORIZON)
        costs[trip.ident] = {"movement": trip.movement, "lag_time": lag.get(trip.ident),
                             "lead_time": lead.get(trip.ident), "delta": b - a}
    totals = {
        move: sum(row["delta"] for row in costs.values() if row["movement"] == move)
        for move in ("T", "L")
    }
    delta = lead_outcome["approach_vehicle_seconds"] - lag_outcome["approach_vehicle_seconds"]
    if abs(sum(totals.values()) - delta) > 1e-8:
        raise RuntimeError("Movement contributions do not reproduce the paired cost")
    return {"delta": round(delta, 8), "movement_delta": {m: round(v, 8) for m, v in totals.items()},
            "vehicles": costs, "uncrossed": [lag_outcome["uncrossed"], lead_outcome["uncrossed"]]}
