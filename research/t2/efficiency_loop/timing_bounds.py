"""Exact paired D51 queue-area bounds with latent arrival time and turn."""
from dataclasses import dataclass, replace
from functools import lru_cache
from itertools import product
from math import comb

from d51_phase_order import Params, phase
from phase_bounds_dp import EMPTY, advance, inventory

ALPHABET = ("", "T", "L")


@dataclass(frozen=True)
class Bounds:
    low: int
    high: int
    paths: int
    peak: int
    low_path: tuple
    high_path: tuple
    low_start: tuple
    high_start: tuple

    @property
    def regret(self):
        return min(max(0, self.high), max(0, -self.low))


def exact(width, bins, config=Params(horizon_s=180), observed=None, reuse=False, initial=(EMPTY,), decision_tick=0, bin_upper=None, bin_total_upper=None, decision_left=None):
    """A bin specifies (through arrivals, left arrivals); at most one per tick.

    bin_upper allows bounded missing arrivals over each observed bin count.
    bin_total_upper optionally caps arrivals across both movements in each bin.
    decision_left restricts the observed left-pocket occupancy just before the
    first controlled tick. Before this snapshot the two queues are identical.
    observed maps a tick to the set of possible symbols. Each returned bound
    has an explicit witness, including its shared starting queue. The common
    horizon must drain every path. Before decision_tick both plans are red.
    """
    observed = observed or {}
    last = width * len(bins)
    if width <= 0 or not bins or last > config.horizon_s or not 0 <= decision_tick < config.horizon_s:
        raise ValueError("invalid bins or horizon")
    upper = bins if bin_upper is None else bin_upper
    if (len(upper) != len(bins) or any(min(T,L) < 0 or T + L > width or
            not T <= uT <= width or not L <= uL <= width
            for (T,L),(uT,uL) in zip(bins,upper))):
        raise ValueError("invalid bin count bounds")
    ceilings = (width,) * len(bins) if bin_total_upper is None else tuple(bin_total_upper)
    if len(ceilings) != len(bins) or any(type(cap) is not int or not sum(counts) <= cap <= width
                                         for cap, counts in zip(ceilings, bins)):
        raise ValueError("invalid bin total upper bounds")
    if decision_left is not None:
        decision_left = frozenset(decision_left)
        if not decision_left or any(type(n) is not int or not 0 <= n <= config.left_capacity
                                    for n in decision_left):
            raise ValueError("invalid decision-time left occupancy")
    if any(not 0 <= t < last or not choices or set(choices) - set(ALPHABET)
           for t, choices in observed.items()):
        raise ValueError("invalid observation")
    lead = replace(config, left_first=True)
    lag = replace(config, left_first=False)
    starts = tuple(dict.fromkeys(initial))
    if not starts or any(set(source) - {"T", "L"} or not 0 <= T <= config.through_capacity
                         or not 0 <= L <= config.left_capacity for source, T, L in starts):
        raise ValueError("invalid initial queues")
    states = {(state, state, 0, 0): (0, 0, 1, (state,), (state,)) for state in starts}
    peak = len(states)

    @lru_cache(maxsize=None)
    def step(queue, move, green):
        new = advance(queue, move, green, config.through_capacity, config.left_capacity, reuse)
        return new, inventory(new)

    for t in range(config.horizon_s):
        if t == decision_tick and decision_left is not None:
            states = {key: value for key, value in states.items() if key[0][2] in decision_left}
            if not states:
                return None
        lag_green, lead_green = ((phase(t-decision_tick,lag), phase(t-decision_tick,lead))
                                  if t >= decision_tick else ("R","R"))
        current = {}
        choices = observed.get(t, ALPHABET) if t < last else ("",)
        remaining = width - 1 - t % width if t < last else 0
        target_T, target_L = bins[t // width] if t < last else (0, 0)
        max_T, max_L = upper[t // width] if t < last else (0, 0)
        total_upper = ceilings[t // width] if t < last else 0
        for (a, b, n_T, n_L), (lo, hi, ways, path_lo, path_hi) in states.items():
            for m in choices:
                T, L = n_T + (m == "T"), n_L + (m == "L")
                needed = max(0,target_T-T) + max(0,target_L-L)
                if T > max_T or L > max_L or needed > remaining or T + L + needed > total_upper:
                    continue
                aa, ia = step(a, m, lag_green)
                bb, ib = step(b, m, lead_green)
                delta = ib - ia
                key = (aa, bb, T, L) if remaining else (aa, bb, 0, 0)
                candidate_lo, candidate_hi = lo + delta, hi + delta
                w_lo = path_lo + (m,) if t < last else path_lo
                w_hi = path_hi + (m,) if t < last else path_hi
                prior = current.get(key)
                if prior:
                    if prior[0] <= candidate_lo:
                        candidate_lo, w_lo = prior[0], prior[3]
                    if prior[1] >= candidate_hi:
                        candidate_hi, w_hi = prior[1], prior[4]
                current[key] = (candidate_lo, candidate_hi, ways + (prior[2] if prior else 0), w_lo, w_hi)
        states = current
        peak = max(peak, len(states))
        if not states:
            return None
        if t + 1 >= last and (decision_left is None or t >= decision_tick) and len(states) == 1 and (EMPTY, EMPTY, 0, 0) in states:
            break
    if len(states) != 1 or (EMPTY, EMPTY, 0, 0) not in states:
        raise ValueError("at least one compatible path failed to drain")
    low, high, paths, low_path, high_path = states[EMPTY, EMPTY, 0, 0]
    return Bounds(low, high, paths, peak, low_path[1:], high_path[1:], low_path[0], high_path[0])


def probe(width, bins, config, ticks, labeled, reuse=False, initial=(EMPTY,)):
    partition = (("",), ("T",), ("L",)) if labeled else (("",), ("T", "L"))
    branches = []
    for responses in product(partition, repeat=len(ticks)):
        result = exact(width, bins, config, dict(zip(ticks, responses)), reuse=reuse, initial=initial)
        if result:
            branches.append(result)
    return max(b.regret for b in branches), sum(b.paths for b in branches)


def sequence_count(width, bins):
    answer = 1
    for T, L in bins:
        answer *= comb(width, L) * comb(width-L, T)
    return answer
