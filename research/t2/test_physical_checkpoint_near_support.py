"""PHYS-10 feature-mask, no leakage, frozen split and exact-accumulation tests."""
import copy
import unittest
from physical_checkpoint_near_support import (
    TEST_SEEDS, REGIMES, SCENARIOS, FEATURES, omit_upstream_a_segment,
    support_distance, policy_outputs, summary, experiment)
from physical_checkpoint_ood_abstention import training_radii


def fake(seed=0, left_positions=(-20,-11,-10,-1), delta=100):
    obs={'outside_A':0,'outside_B':0,'approach_A':len(left_positions),
         'approach_B':1,'pocket_vehicles':1,'receiver_vehicles':2,
         'approach_A_positions':tuple(left_positions),
         'approach_B_positions':(-1,), 'pocket_positions':(-1,),
         'receiver_occupied_cells':(0,1)}
    return {'seed':seed,'capacity':4,'pocket_m':14.,'b_share':0.,
            'delta_p60':delta,'decision_observation':obs}


class NearSupportTests(unittest.TestCase):
    def test_locked_split_and_scenarios(self):
        self.assertEqual(TEST_SEEDS,tuple(range(72,80)))
        self.assertFalse(set(TEST_SEEDS) & set(range(72)))
        self.assertEqual(SCENARIOS,('exact','stale12','occluded'))
        self.assertEqual(FEATURES,('counts','positions'))
        self.assertEqual(REGIMES,(('left45',1800,.45),('left55',1800,.55),
                                  ('demand1650',1650,.5),('demand1950',1950,.5)))

    def test_blocking_detector_segment_is_consistent_and_pure(self):
        original=fake()['decision_observation']
        saved=copy.deepcopy(original)
        blocked=omit_upstream_a_segment(original)
        self.assertEqual(original,saved)
        self.assertEqual(blocked['approach_A'],2)
        self.assertEqual(blocked['approach_A_positions'],(-10,-1))
        self.assertEqual(blocked['approach_B'],1)
        self.assertEqual(blocked['decision_tick'] if 'decision_tick' in blocked else None,None)

    def test_support_and_policy_do_not_depend_on_future_labels(self):
        training=[fake(seed=i,delta=(-50 if i%2 else 80)) for i in range(8)]
        radii=training_radii(training)
        geom={'seed':72,'capacity':4,'pocket_m':14.,'b_share':0.}
        observed=fake(seed=72)['decision_observation']
        pre=policy_outputs(training,geom,observed,radii)
        self.assertEqual(pre,policy_outputs(training,dict(geom,delta_p60=999999),observed,radii))
        self.assertEqual(support_distance(training,dict(geom,decision_observation=observed),'counts'),0.)

    def test_abstention_aggregates_counterexamples(self):
        # Every row is treated by learned policy, one vetoed harmful and one
        # vetoed beneficial; one admitted harmful treatment must remain.
        def row(seed,delta,allowed):
            status={'in_support':allowed,'learned_action':True,
                    'vetoed_action':allowed}
            return {'seed':seed,'regime':'left45','delta_p60':delta,
                    'observations':{'exact':{'counts':status}}}
        rows=[row(72,10,True),row(72,5,False),row(73,-7,False)]
        # Summary also computes a seed-block interval, so remaining locked
        # seeds need zero-effect no-treatment dummy cases.
        for seed in range(74,80):
            rows.append(row(seed,0,False))
        r=summary(rows,'exact','counts')
        self.assertEqual(r['harmful_admitted'],1)
        self.assertEqual(r['blocked_harmful'],1)
        self.assertEqual(r['blocked_beneficial'],1)
        self.assertEqual(r['veto_savings'],-10)
        self.assertEqual(r['unconditional_savings'],-8)

    def test_bad_training_prevents_future_simulation(self):
        with self.assertRaisesRegex(ValueError,'144 PHYS-04'):
            experiment([])


if __name__=='__main__':
    unittest.main()
