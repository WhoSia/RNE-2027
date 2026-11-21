"""The known zero-distance alias is an effect-magnitude, not strict-rank, witness."""
import unittest
from physical_checkpoint_alias_factorial_audit import experiment


class AliasFactorialAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.payload = experiment()

    def test_original_seed_split_and_full_four_cell_cross(self):
        rows = self.payload['cells']
        self.assertEqual(len(rows), 4)
        self.assertEqual([(r['prefix_seed'], r['future_seed'], r['delta_p60'])
                          for r in rows],
                         [(3, 3, 0), (3, 76, 0), (76, 3, 0), (76, 76, 306)])
        self.assertTrue(self.payload['observed_count_feature_identical'])
        self.assertTrue(all(r['matched_policy_checkpoint'] and
                            r['prefix_state_independent_of_future'] for r in rows))

    def test_effect_is_not_only_terminal_penalty(self):
        matched = self.payload['cells'][-1]
        c = matched['components']
        self.assertEqual(sum(c[k] for k in ('outside_vehicle_seconds',
                                            'upstream_vehicle_seconds',
                                            'receiver_vehicle_seconds')), 186)
        self.assertEqual(c['remaining'], 2)
        self.assertEqual(c['network_out_S'], -2)
        self.assertEqual(c['network_out_L'], 0)
        self.assertEqual(matched['delta_p60'], 186 + 60 * 2)

    def test_no_strict_opposite_optimal_policy(self):
        self.assertTrue(self.payload['not_strict_policy_rank_reversal'])
        self.assertFalse(any(r['delta_p60'] < 0 for r in self.payload['cells']))


if __name__ == '__main__':
    unittest.main()
