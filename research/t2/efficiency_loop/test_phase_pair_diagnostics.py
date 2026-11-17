from unittest import TestCase

from phase_pair_diagnostics import bracket_state, paired_departure_cost
from sumo_phase_pair import HORIZON, phases, point_departures


class PhasePairDiagnostics(TestCase):
    def test_state_straddling_amber_is_reported_as_transition(self):
        self.assertEqual(bracket_state(phases(True), 11.75, 12, "L"), "transition:G>y")
        self.assertEqual(bracket_state(phases(True), 12, 12.25, "L"), "y")
        self.assertEqual(bracket_state(phases(True, yellow=False), 12, 12.25, "L"), "r")
        self.assertEqual(bracket_state(phases(True), 59.75, 60, "L"), "transition:r>G")

    def test_pair_explains_baseline_and_retains_censored_vehicle(self):
        lag, lead = point_departures(False), point_departures(True)
        baseline = paired_departure_cost(lag, lead)
        self.assertEqual(baseline["delta"], 110)
        self.assertEqual(baseline["movement_delta"], {"T": -138, "L": 248})
        previous = lead.pop("v01")
        censored = paired_departure_cost(lag, lead)
        self.assertEqual(censored["delta"], 110 + HORIZON - previous)
        self.assertEqual(censored["uncrossed"], [0, 1])
        self.assertIsNone(censored["vehicles"]["v01"]["lead_time"])
