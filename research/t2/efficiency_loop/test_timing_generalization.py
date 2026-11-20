from unittest import TestCase

from timing_generalization import NEW_SEEDS, SEEDS, orientation


class TimingGeneralizationTests(TestCase):
    def test_seed_inputs_are_distinct_after_context_offsets(self):
        seeds = (*SEEDS, *NEW_SEEDS)
        self.assertEqual(len({seed + 101*i for seed in seeds for i in range(6)}),
                         len(seeds)*6)

    def test_previous_counterexample_depends_on_terminal_cost(self):
        early, late = (57, -1), (95, -1)
        self.assertEqual([orientation(early, late, p) for p in (0, 30, 57, 60, 90, 95, 120)],
                         [0, 0, 0, 1, 1, 0, 0])

    def test_both_reversal_directions_and_ties(self):
        self.assertEqual(orientation((1, 0), (-2, 0), 60), -1)
        self.assertEqual(orientation((-2, 0), (1, 0), 60), 1)
        self.assertEqual(orientation((0, 0), (-2, 0), 60), 0)
