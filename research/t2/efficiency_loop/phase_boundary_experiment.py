"""Paired point-queue and SUMO sensitivity without retiming the green phases."""

import argparse
import json
from collections import Counter
from itertools import product
from pathlib import Path

from phase_pair_diagnostics import bracket_state, paired_departure_cost
from sumo_phase_pair import execute, crossing_brackets, phases, point_departures, prepare


def point_grid():
    rows = []
    for amber, headway, travel in product((0, .25, .5, 1, 3), (1.5, 1.75, 2, 2.25), (9.75, 10, 10.25)):
        contrast = paired_departure_cost(*(point_departures(
            lead, headway=headway, travel_time=travel, amber_service_s=amber) for lead in (False, True)))
        witness = contrast.pop("vehicles")["v01"]
        rows.append({"amber_service_s": amber, "headway_s": headway, "travel_s": travel,
                     **contrast, "first_left": witness})
    return rows

