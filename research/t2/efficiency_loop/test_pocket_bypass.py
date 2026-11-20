from collections import deque
from unittest import TestCase

from pocket_bypass import access_uncertainty, summarize
from signal_model import Plan, Scenario, admit_source, run


class PocketBypassTests(TestCase):
    def test_only_a_straight_vehicle_within_reach_passes(self):
        queue = deque([1, 1, 0])
        bay, capacity = (0, 1), (2, 1)
        self.assertIsNone(admit_source(queue, bay, capacity, 0, 1))
        self.assertEqual(admit_source(queue, bay, capacity, 0, 3), 0)
        self.assertEqual(list(queue), [1, 1])

    def test_no_same_tick_space_credit_or_reverse_bypass(self):
        queue = deque([1, 0])
        self.assertIsNone(admit_source(queue, (1, 1), (1, 1), 0, 3))
        self.assertEqual(list(queue), [1, 0])
        queue = deque([0, 1])
        self.assertIsNone(admit_source(queue, (1, 0), (1, 1), 0, 3))

    def test_run_releases_one_through_vehicle_earlier(self):
        plan = Plan((6, 6, 6, 6), False, 0)
        scenario = Scenario("test", 6, ((0, 1), (0, 1), (1, 0)),
                            bay=(1, 1, 1, 1, 1, 1), receive_green=36)
        self.assertEqual(run(plan, scenario).completed[0], 0)
        self.assertEqual(run(plan, scenario, bypass_depth=1).completed[0], 1)
        with self.assertRaises(ValueError):
            run(plan, scenario, fast=True, bypass_depth=1)

    def test_observation_changes_partition_and_preserve_matched_costs(self):
        prefix = (1, 1, 0)
        a, b = prefix + (0, 0, 0), prefix + (1, 0, 0)
        same = summarize([(a, -5, 1, 0, 0, 0), (b, 7, 1, 0, 0, 0)])
        split = summarize([(a, -5, 1, 0, 0, 0), (b, 7, 0, 0, 0, 0)])
        self.assertEqual(same["ambiguous"]["110/1/0"]["bounds"], [-5, 7])
        self.assertFalse(split["ambiguous"])

    def test_unknown_access_can_dominate_even_perfect_arrival_information(self):
        stream = (1, 0, 0)
        models = {0: {stream: (-5, (1, 0))}, 1: {stream: (7, (1, 0))},
                  3: {stream: (9, (0, 0))}}
        report = access_uncertainty(models)
        self.assertEqual(report["incompatible_streams"], 1)
        self.assertEqual(report["witness"]["upper"], (1, 7))
        self.assertEqual(report["witness"]["regret"], 5)
