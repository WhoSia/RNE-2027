from dataclasses import replace
from unittest import TestCase

from daypart_scenarios import BASELINE, worlds
from green_service_diagnosis import Opportunity, THROUGH, measure
from green_service_experiment import change_storage
from signal_model import calendar, run


class GreenServiceDiagnosisTests(TestCase):
    def test_labels_distinguish_hidden_upstream_demand_from_empty_approach(self):
        empty = Opportunity(0, 0, 0, 0, 1, 1, True, 1, False)
        pocket = replace(empty, through_upstream=1)
        self.assertEqual(empty.diagnosis, "no_through_demand")
        self.assertEqual(pocket.diagnosis, "pocket_signature")
        self.assertEqual(replace(pocket, downstream_space=0).diagnosis, "joint_signature")
        self.assertEqual(replace(empty, through_ready=1, downstream_space=0).diagnosis,
                         "downstream_blocked")
        self.assertEqual(replace(pocket, shared_head_is_left=False).diagnosis,
                         "upstream_pending")
        self.assertEqual(replace(pocket, through_ready=1, entered=True).diagnosis, "served")

    def test_observer_keeps_all_scheduled_through_opportunities_and_outcome(self):
        scenario = change_storage(next(worlds(17)).scenario, 1, 2)
        outcome, counts, samples = measure(BASELINE, scenario)
        slots = calendar(BASELINE, scenario.headway)
        expected = sum(t % BASELINE.cycle in slots[m]
                       for t in range(scenario.horizon) for m in THROUGH)
        self.assertEqual(sum(counts.values()), expected)
        self.assertEqual(outcome, run(BASELINE, scenario))
        self.assertTrue(all(row.diagnosis == label for label, row in samples.items()))
