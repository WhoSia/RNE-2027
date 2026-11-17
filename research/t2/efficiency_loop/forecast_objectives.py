"""Small exhaustive comparison of worst absolute cost and worst regret."""

from dataclasses import replace
from functools import cache
from itertools import product

from d51_phase_order import phase
from phase_bounds_dp import EMPTY, advance, inventory
from prospective_sensing import QUEUE_STARTS, WIDTH, information_at_decision


def bounded_sequences(lower, upper, ceilings, width):
    def admissible(word, low, high, cap):
        through, left = word.count("T"), word.count("L")
        return (low[0] <= through <= high[0] and low[1] <= left <= high[1]
                and through + left <= cap)

    candidates = tuple(product(("", "T", "L"), repeat=width))
    bins = [tuple(word for word in candidates if admissible(word, low, high, cap))
            for low, high, cap in zip(lower, upper, ceilings, strict=True)]
    for path in product(*bins):
        yield tuple(mark for word in path for mark in word)


@cache
def schedules(config, decision):
    lag, lead = replace(config, left_first=False), replace(config, left_first=True)
    return tuple((phase(t-decision, lag), phase(t-decision, lead)) if t >= decision else ("R", "R")
                 for t in range(config.horizon_s))


@cache
def next_state(queue, move, green, through_capacity, left_capacity):
    return advance(queue, move, green, through_capacity, left_capacity, False)


def paired_cost(path, initial, config, decision):
    lag = lead = initial
    cost_lag = cost_lead = 0
    for tick, (green_lag, green_lead) in enumerate(schedules(config, decision)):
        move = path[tick] if tick < len(path) else ""
        lag = next_state(lag, move, green_lag, config.through_capacity, config.left_capacity)
        lead = next_state(lead, move, green_lead, config.through_capacity, config.left_capacity)
        cost_lag += inventory(lag)
        cost_lead += inventory(lead)
        if tick + 1 >= len(path) and lag == lead == EMPTY:
            return cost_lag, cost_lead
    raise RuntimeError("Compatible queue path did not drain")


def choice(lag, lead):
    return "lag" if lag < lead else "lead" if lead < lag else "either"


def objective_records(costs):
    worst_lag = worst_lead = best_delta = worst_delta = None
    worlds = 0
    for lag, lead, path, initial in costs:
        record = {"costs_lag_lead": [lag, lead], "arrivals": path, "initial": initial}
        if worst_lag is None or lag > worst_lag["costs_lag_lead"][0]:
            worst_lag = record
        if worst_lead is None or lead > worst_lead["costs_lag_lead"][1]:
            worst_lead = record
        delta = lead - lag
        if best_delta is None or delta < best_delta[0]:
            best_delta = delta, record
        if worst_delta is None or delta > worst_delta[0]:
            worst_delta = delta, record
        worlds += 1
    if not worlds:
        raise ValueError("No compatible worlds")
    absolute = [worst_lag["costs_lag_lead"][0], worst_lead["costs_lag_lead"][1]]
    regret = [max(0, -best_delta[0]), max(0, worst_delta[0])]
    return {"worlds": worlds, "absolute": absolute, "regret": regret,
            "delta_bounds": [best_delta[0], worst_delta[0]],
            "absolute_choice": choice(*absolute), "regret_choice": choice(*regret),
            "witnesses": {"max_lag": worst_lag, "max_lead": worst_lead,
                          "min_delta": best_delta[1], "max_delta": worst_delta[1]}}


def evaluate(visible, decision, cap, config):
    lower, upper, ceilings = information_at_decision(visible + ((0, 0),), WIDTH, decision, cap)
    worlds = ((*paired_cost(path, state, config, decision), path, state)
              for path in bounded_sequences(lower, upper, ceilings, WIDTH)
              for state in QUEUE_STARTS)
    return objective_records(worlds)
