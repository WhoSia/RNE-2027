"""Exact finite-catalog minimax and minimax-regret searches."""
from dataclasses import dataclass
from itertools import product

from signal_model import Plan, lower_cost, run


@dataclass(frozen=True)
class Search:
    plan: Plan
    value: int
    evaluations: int
    abandoned: int
    skipped: int
    screened: int
    ticks: int


def catalog(cycle=84):
    return tuple(Plan((T, L, X, P), lead, off)
                 for T, L, P, lead, off in product((24, 28, 32, 36), (8, 12, 16),
                                                   (8, 12), (False, True), range(0, cycle, 4))
                 if (X := cycle - 12 - T - L - P) >= 12)


def search(plans, scenarios, offsets=None, *, prune=True, fast=False, first=None, relax=False):
    """Minimize max_s(cost(plan,s) - offsets[s]) over the supplied catalog.

    An admissible lower bound is the largest completed scenario score and
    the partial queue area of the current scenario minus its offset.
    """
    plans = tuple(plans)
    scenarios = tuple(scenarios)
    if not plans or not scenarios:
        raise ValueError("a nonempty catalog and scenario set are required")
    offsets = (0,) * len(scenarios) if offsets is None else tuple(offsets)
    if len(offsets) != len(scenarios):
        raise ValueError("one offset per scenario is required")
    if first is not None and first not in plans:
        raise ValueError("initial incumbent must be in the catalog")
    order = sorted(range(len(scenarios)),
                   key=lambda i: (offsets[i], len(scenarios[i].arrivals)), reverse=True)
    winner = None
    evaluations = abandoned = skipped = screened = ticks = 0
    candidates = plans if first is None else (first,) + tuple(p for p in plans if p != first)
    for p in candidates:
        worst = -float("inf")
        for step, i in enumerate(order):
            limit = winner[0] + offsets[i] if prune and winner else None
            if relax and limit is not None and lower_cost(p, scenarios[i]) > limit:
                screened += 1
                skipped += len(scenarios) - step - 1
                break
            outcome = run(p, scenarios[i], fast=fast, limit=limit)
            evaluations += 1
            if outcome is None:
                abandoned += 1
                skipped += len(scenarios) - step - 1
                break
            ticks += outcome.ticks
            worst = max(worst, outcome.cost - offsets[i])
            if prune and winner and worst > winner[0]:
                skipped += len(scenarios) - step - 1
                break
        else:
            candidate = worst, p
            if winner is None or candidate < winner:
                winner = candidate
    return Search(winner[1], winner[0], evaluations, abandoned, skipped, screened, ticks)


def oracle_offsets(plans, scenarios, **options):
    runs = tuple(search(plans, (s,), **options) for s in scenarios)
    return tuple(r.value for r in runs), runs
