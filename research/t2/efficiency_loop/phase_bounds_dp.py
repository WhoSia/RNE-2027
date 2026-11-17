"""Exact paired D51 bounds under aligned movement-count observations."""
from collections import defaultdict
from dataclasses import dataclass, replace
from pathlib import Path
import csv

from d51_phase_order import Params, phase

EMPTY = ("", 0, 0)  # shared FIFO, through bay count, left bay count


@dataclass(frozen=True)
class Bounds:
    low: int
    high: int
    orders: int
    peak_states: int
    low_left_ticks: tuple[int, ...]
    high_left_ticks: tuple[int, ...]


def advance(state, arrival, green, through_capacity, left_capacity, reuse):
    source, through, left = state
    if arrival:
        source += arrival
    after_through = through - int(green == "T" and through > 0)
    after_left = left - int(green == "L" and left > 0)
    if source.startswith("T") and (after_through if reuse else through) < through_capacity:
        return source[1:], after_through + 1, after_left
    if source.startswith("L") and (after_left if reuse else left) < left_capacity:
        return source[1:], after_through, after_left + 1
    return source, after_through, after_left


def inventory(state):
    source, through, left = state
    return len(source) + through + left


def exact_bounds(arrival_ticks, width, left_counts, config, reuse=False, known=None):
    """Track both policies on one hidden sequence, with exact extrema and count.

    Every integer bin starts at 0, width, 2*width, etc. The caller supplies
    every arrival tick. Multiple vehicles in the same tick are outside D51's
    one-arrival-per-tick experiment. Known entries may fix a movement at a tick.
    Raise when a compatible sequence fails to drain by the configured horizon.
    """
    ticks = tuple(arrival_ticks)
    counts = tuple(left_counts)
    known = known or {}
    if width < 1 or not ticks or sorted(set(ticks)) != list(ticks):
        raise ValueError("sorted distinct ticks and a positive width required")
    if ticks[0] < 0 or ticks[-1] >= config.horizon_s or len(counts) != ticks[-1] // width + 1:
        raise ValueError("bins or horizon do not cover the arrival ticks")
    if any(t not in ticks or m not in ("L", "T") for t, m in known.items()):
        raise ValueError("known movements must refer to arrival ticks")
    if any(c < 0 or c > sum(t // width == i for t in ticks) for i, c in enumerate(counts)):
        raise ValueError("invalid bin counts")

    lag = replace(config, left_first=False)
    lead = replace(config, left_first=True)
    # Both queues begin empty. Each state stores (min, max, number of prefixes).
    states = {(EMPTY, EMPTY, 0): (0, 0, 1, 0, 0)}
    peak = 1
    tick_set = set(ticks)
    slot_groups = defaultdict(list)
    for t in ticks:
        slot_groups[t // width].append(t)
    slots_after = {t: len(group)-i-1 for group in slot_groups.values() for i,t in enumerate(group)}
    for t in range(config.horizon_s):
        at_arrival = t in tick_set
        moves = (known[t],) if t in known else ("L", "T") if at_arrival else ("",)
        next_states = {}
        last_tick_in_bin = (t + 1) % width == 0 or t == ticks[-1]
        lag_green, lead_green = phase(t, lag), phase(t, lead)
        bit = 1 << t if at_arrival else 0
        for (l_state, r_state, used), (low, high, ways, low_path, high_path) in states.items():
            for move in moves:
                left_used = used + (move == "L")
                if at_arrival and not left_used <= counts[t // width] <= left_used + slots_after[t]:
                    continue
                l_new = advance(l_state, move, lag_green, config.through_capacity, config.left_capacity, reuse)
                r_new = advance(r_state, move, lead_green, config.through_capacity, config.left_capacity, reuse)
                step = inventory(r_new) - inventory(l_new)
                key = l_new, r_new, 0 if last_tick_in_bin else left_used
                prev = next_states.get(key)
                lo, hi = low + step, high + step
                turn = bit if move == "L" else 0
                lo_path, hi_path = low_path | turn, high_path | turn
                if prev is not None:
                    if prev[0] < lo:
                        lo, lo_path = prev[0], prev[3]
                    if prev[1] > hi:
                        hi, hi_path = prev[1], prev[4]
                    ways_to_state = ways + prev[2]
                else:
                    ways_to_state = ways
                next_states[key] = lo, hi, ways_to_state, lo_path, hi_path
        states = next_states
        peak = max(peak, len(states))
        if t >= ticks[-1] and states and all(a == b == EMPTY for a, b, _ in states):
            break
    if not states:
        raise ValueError("no compatible sequences")
    if any(a != EMPTY or b != EMPTY for a, b, _ in states):
        raise ValueError("at least one sequence did not drain")
    low, high, order_count, low_bits, high_bits = states[EMPTY, EMPTY, 0]
    return Bounds(low, high, order_count, peak, tuple(t for t in ticks if low_bits >> t & 1),
                  tuple(t for t in ticks if high_bits >> t & 1))


def signature(sequence, width, ticks):
    return tuple(sum(t // width == i for t in sequence) for i in range(ticks[-1] // width + 1))


def verify(oracle, probes, output):
    ticks = tuple(range(12))
    grouped = defaultdict(list)
    with oracle.open(newline="") as file:
        for row in csv.DictReader(file):
            times = tuple(map(int, row["left_times_s"].split()))
            for width in (1, 2, 3, 4, 6, 12):
                key = row["rule"], int(row["left_capacity"]), width, signature(times, width, ticks)
                grouped[key].append(int(row["delta_lead_minus_lag_vehicle_seconds"]))
    result = []
    for (rule, capacity, width, counts), values in sorted(grouped.items()):
        bounds = exact_bounds(ticks, width, counts, Params(left_capacity=capacity,horizon_s=120), rule != "D51")
        assert (bounds.low, bounds.high, bounds.orders) == (min(values), max(values), len(values))
        result.append((rule, capacity, width, " ".join(map(str, counts)), bounds.orders,
                       bounds.low, bounds.high, bounds.peak_states))
    with output.open("w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(("rule","capacity","bin_seconds","left_counts","orders","low","high","peak_states"))
        writer.writerows(result)
    with probes.open(newline="") as file:
        probe_rows = list(csv.DictReader(file))
    for row in probe_rows:
        observed = int(row["observed_left_at_s"])
        cfg = Params(left_capacity=3, horizon_s=120, left_green_s=int(row["left_green_s"]))
        b = exact_bounds(ticks, 2, (0,1,0,1,1,1), cfg, row["rule"] != "D51", {observed: "L"})
        assert (b.low, b.high, b.orders) == tuple(int(row[k]) for k in (
            "min_vehicle_seconds","max_vehicle_seconds","compatible_orders"))
    print(f"matched {len(result)} aggregate classes and {len(probe_rows)} one-observation bounds")
    from d50_turn_pocket import Vehicle
    from d51_phase_order import simulate
    with output.with_name("phase_dp_scaling.csv").open("w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(("arrival_ticks","left_per_6_ticks","orders","low","high","peak_states",
                         "low_left_ticks","high_left_ticks"))
        for n in (18,24,30,36):
            width = 6
            cfg = Params(left_capacity=3,horizon_s=300)
            ticks = tuple(range(n))
            counts = (2,) * (n // width)
            b = exact_bounds(ticks, width, counts, cfg)
            for expected, example in ((b.low,b.low_left_ticks),(b.high,b.high_left_ticks)):
                assert signature(example,width,ticks) == counts
                arrivals = tuple(Vehicle(t,"L" if t in example else "T",t) for t in ticks)
                lag = simulate(arrivals,cfg)
                lead = simulate(arrivals,replace(cfg,left_first=True))
                assert not (lag.unserved or lead.unserved)
                assert round(n*(lead.mean_vehicle_delay_s-lag.mean_vehicle_delay_s)) == expected
            writer.writerow((n,2,b.orders,b.low,b.high,b.peak_states,
                             " ".join(map(str,b.low_left_ticks)), " ".join(map(str,b.high_left_ticks))))
            print(n,b)


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    for field in ("oracle", "probes", "output"):
        p.add_argument("--" + field, type=Path, required=True)
    args = p.parse_args()
    verify(args.oracle,args.probes,args.output)
