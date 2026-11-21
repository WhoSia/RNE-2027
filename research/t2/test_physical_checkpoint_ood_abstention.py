"""PHYS-09 nearest-training-support abstention invariants."""
import unittest
from physical_checkpoint_ood_abstention import (
    SEEDS, REGIMES, QUANTILE, training_radii,
    is_supported, evaluate, squared_distance)


def toy(seed, count=1, delta=0):
    return {'seed': seed, 'capacity': 4, 'pocket_m': 14., 'b_share': 0.,
            'delta_p60': delta,
            'decision_observation': {'outside_A':0,'outside_B':0,
               'approach_A':count,'approach_B':1,'pocket_vehicles':1,
               'receiver_vehicles':2, 'approach_A_positions':(-1,),
               'approach_B_positions':(-1,), 'pocket_positions':(-1,),
               'receiver_occupied_cells':(0,1)}}


class SupportAbstentionTests(unittest.TestCase):
    def test_new_seeds_frozen_and_not_reused(self):
        self.assertEqual(SEEDS, tuple(range(56,72)))
        self.assertFalse(set(SEEDS) & set(range(56)))
        self.assertEqual(REGIMES,(('uniform_baseline',1800,.5),
                                  ('uniform_lowturn',1350,.3)))
        self.assertEqual(QUANTILE,.95)

    def test_training_only_radius_does_not_use_outcomes(self):
        a=[toy(0,1,-100),toy(1,2,100),toy(2,4,-50)]
        first=training_radii(a)
        for x in a:x['delta_p60']=999999
        self.assertEqual(first,training_radii(a))
        self.assertGreaterEqual(first['counts'],0)
        self.assertGreaterEqual(first['positions'],0)

    def test_support_detects_far_counts(self):
        train=[toy(0,1),toy(1,2),toy(2,4)]
        radius=training_radii(train)['counts']
        self.assertTrue(is_supported(train,toy(3,1),'counts',radius))
        self.assertFalse(is_supported(train,toy(4,20),'counts',radius))

    def test_squared_distance_symmetric_and_nonnegative(self):
        self.assertEqual(squared_distance((0,2),(3,4)),13)
        self.assertEqual(squared_distance((3,4),(0,2)),13)

    def test_invalid_training_fails_before_experiment(self):
        with self.assertRaisesRegex(ValueError,'expected seeds'):
            evaluate([])


if __name__=='__main__':
    unittest.main()
