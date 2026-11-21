"""Holdout clock-isolation contracts: fixed route sequence, distinct timestamps."""
import unittest
from spatial_v10 import Config
from t2_route_matched_clock_screen import SEEDS,REGIMES,CLOCKS,route_matched_tapes,experiment

class RouteMatchedContracts(unittest.TestCase):
    def test_prespecified_seeds_and_combinations(self):
        self.assertEqual(SEEDS,tuple(range(96,104)))
        self.assertEqual(REGIMES,(('left45',1800,.45),('demand1650',1650,.5)))
        self.assertEqual(CLOCKS,('legacy','randomized_timestamps'))

    def test_routes_and_total_are_exactly_matched(self):
        for seed in SEEDS:
            c=Config(seed=seed,duration_s=240,demand_vph=1800,left_fraction=.45)
            tapes=route_matched_tapes(c)
            left,right=tapes['legacy'],tapes['randomized_timestamps']
            self.assertEqual(len(left),len(right))
            self.assertEqual(tuple(r for _,r in left),tuple(r for _,r in right))
            self.assertNotEqual(tuple(t for t,_ in left),tuple(t for t,_ in right))

    def test_frozen_holdout_results_not_reinterpreted_as_independent_worlds(self):
        result=experiment()
        self.assertEqual(len(result['worlds']),192)
        self.assertEqual(result['summary']['left45']['strict_sign_oppositions'],1)
        self.assertEqual(result['summary']['demand1650']['strict_sign_oppositions'],9)
        for regime,s in result['summary'].items():
            self.assertTrue(s['exact_route_match_all'])
            self.assertEqual(len(s['contrasts']),48)
            for clock,v in s['by_clock'].items():
                self.assertEqual(v['by_width']['4']['n'],48)

if __name__=='__main__':unittest.main()
