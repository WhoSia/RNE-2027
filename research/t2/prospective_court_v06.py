"""RITHM-style pre-registered falsification gates for T2 model v0.5.

Pure standard library, no random sampling within the court. A court result is
about simulator outputs only; it does not confer field/causal validity.
"""
from __future__ import annotations
from dataclasses import dataclass
from math import isfinite
from statistics import mean

EXPLORATION_SEEDS = tuple(range(10))
HOLDOUT_SEEDS = tuple(range(100, 120))
FORKS = (-21, -13)
CAPS = (2, 4)
MODES = ('leading', 'lagging')
UPDATES = ('sequential', 'parallel')

@dataclass(frozen=True)
class Verdict:
    status: str
    reason: str
    contrasts: tuple[float, ...]


def interaction(table: dict[tuple[int, int], float]) -> float:
    """I = Δ_K at f=-13 minus Δ_K at f=-21."""
    if set(table) != {(f, k) for f in FORKS for k in CAPS}:
        raise ValueError('exact four-cell factorial required')
    if any(not isfinite(v) for v in table.values()):
        raise ValueError('nonfinite outcome')
    return (table[-13, 4]-table[-13, 2])-(table[-21, 4]-table[-21, 2])


def negative_control_no_left(table: dict[tuple[int, int], float]) -> Verdict:
    """Same fork & arrivals, all straight: virtual bay limit must be inert."""
    diffs=tuple(table[f,4]-table[f,2] for f in FORKS)
    if any(d != 0 for d in diffs):
        return Verdict('FAIL', 'capacity K affected an all-through run', diffs)
    return Verdict('PASS', 'no-left capacity placebo is exactly zero', diffs)


def sign_court(discovery: tuple[float,...], holdout: tuple[float,...],
               *, expected: str='negative') -> Verdict:
    """No post-hoc redefinition: fixed negative sign, held-out seed units.

    An ordinal pass only means sign stability of a simulator interaction.
    """
    if expected != 'negative':
        raise ValueError('pre-registered sign is negative')
    if not discovery or not holdout:
        raise ValueError('both sets required')
    if any(not isfinite(x) for x in discovery+holdout):
        raise ValueError('nonfinite contrast')
    if not all(x < 0 for x in discovery):
        return Verdict('FAIL', 'discovery itself violates fixed sign', holdout)
    if not all(x < 0 for x in holdout):
        return Verdict('REFUTED', 'at least one held-out interaction is nonnegative', holdout)
    return Verdict('PASS_TOY_ONLY', f'holdout mean={mean(holdout):.3f}; all signs negative', holdout)


def validate_split(exploration=EXPLORATION_SEEDS, holdout=HOLDOUT_SEEDS) -> None:
    if not exploration or not holdout or len(set(exploration))!=len(exploration) \
            or len(set(holdout))!=len(holdout) or set(exploration)&set(holdout):
        raise ValueError('exploration/holdout must be nonempty, disjoint, and unique')


if __name__ == '__main__':
    validate_split()
    example={(-21,2):100,(-21,4):120,(-13,2):102,(-13,4):108}
    print('synthetic interaction', interaction(example))
    print('synthetic placebo',negative_control_no_left({(-21,2):10,(-21,4):10,(-13,2):12,(-13,4):12}))
