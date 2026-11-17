"""Paired synthetic dayparts, with no calibration to observed locations."""
from dataclasses import dataclass
from itertools import product
from random import Random

from signal_model import Plan, Scenario

BASELINE = Plan((28, 12, 24, 8), False, 0)
SPLITS = (BASELINE.greens, (36, 12, 16, 8), (24, 12, 20, 16))
COUNTS = {
    "night": (20, 3, 17, 3, 9, 7, 3),
    "midday": (35, 10, 29, 8, 22, 20, 42),
    "peak": (54, 18, 49, 16, 31, 27, 27),
}
HORIZON = 336
ARRIVAL_WINDOW = 252


@dataclass(frozen=True)
class World:
    band: str
    shape: str
    receiving: str
    scenario: Scenario


def plans():
    return tuple(Plan(split, order, offset)
                 for split, order, offset in product(SPLITS, (False, True), (0, 20, 40)))


def arrival_times(seed, band, shape):
    rng = Random(seed)
    rows = []
    for movement, count in enumerate(COUNTS[band]):
        for i in range(count):
            jitter = rng.randrange(7) - 3
            if shape == "dispersed" or movement == 6:
                t = (2 * i + 1) * ARRIVAL_WINDOW // (2 * count) + jitter
            else:
                group, within_group = divmod(i, 5)
                groups = (count + 4) // 5
                t = group * ARRIVAL_WINDOW // groups + 3 * within_group + jitter
            rows.append((min(ARRIVAL_WINDOW - 1, max(0, t)), movement))
    return tuple(sorted(rows))


def worlds(seed):
    for index, (band, shape) in enumerate(product(COUNTS, ("dispersed", "platooned"))):
        arrivals = arrival_times(seed + 101 * index, band, shape)
        for downstream, link, receive_green in (
            ("open", (12, 8, 12, 8, 10, 10), 36),
            ("constrained", (3, 2, 3, 2, 4, 4), 12),
        ):
            name = f"{band}/{shape}/{downstream}"
            yield World(band, shape, downstream, Scenario(
                name, HORIZON, arrivals, bay=(8, 3, 8, 3, 10, 10), link=link,
                receive_green=receive_green, receive_offset=7,
                travel=(7, 4, 7, 4, 5, 5),
            ))
