"""PHYS-05b smoke tests for observation-only noise, deterministic replay, bounds."""
import copy
import unittest
from physical_checkpoint_measurement_stress import corrupt


def observation():
    return {'seed': 12, 'capacity': 4, 'pocket_m': 14., 'b_share': .5,
            'delta_p60': 1600,
            'decision_observation': {
                'outside_A': 0, 'outside_B': 1,
                'approach_A': 20, 'approach_B': 18,
                'pocket_vehicles': 2, 'receiver_vehicles': 4,
                'approach_A_positions': (-20, -4, -1),
                'approach_B_positions': (-20, -3, -1),
                'pocket_positions': (-2, -1),
                'receiver_occupied_cells': (0, 1, 2, 3)}}


class SensorNoiseTests(unittest.TestCase):
    def test_zero_noise_is_identity(self):
        row = observation()
        self.assertEqual(corrupt(row, 0, 0., 0), row)

    def test_input_and_outcome_remain_unchanged(self):
        row = observation()
        frozen = copy.deepcopy(row)
        altered = corrupt(row, 2, .3, 4)
        self.assertEqual(row, frozen)
        self.assertEqual(altered['delta_p60'], row['delta_p60'])
        self.assertEqual(altered['seed'], row['seed'])
        self.assertEqual(altered['capacity'], row['capacity'])

    def test_reproducible_random_corruption(self):
        row = observation()
        self.assertEqual(corrupt(row, 2, .3, 4),
                         corrupt(row, 2, .3, 4))

    def test_physical_count_bounds(self):
        row = observation()
        for trial in range(20):
            x = corrupt(row, 2, .3, trial)['decision_observation']
            self.assertTrue(0 <= x['approach_A'] <= 20)
            self.assertTrue(0 <= x['approach_B'] <= 20)
            self.assertTrue(0 <= x['pocket_vehicles'] <= 2)
            self.assertTrue(0 <= x['receiver_vehicles'] <= 4)
            self.assertGreaterEqual(x['outside_A'], 0)
            self.assertGreaterEqual(x['outside_B'], 0)


if __name__ == '__main__':
    unittest.main()
