"""Tests: interventions differ in one intended dimension only.
Run: python -m unittest discover -s research/t2 -p 'test_spatial_v04.py' -v
"""
import unittest
from spatial_v04_factorial import Config, simulate

class TestV04(unittest.TestCase):
    def test_capacity_coupling(self):
        for seed in (0,1):
            runs=[simulate(Config(duration=300, seed=seed, fixed_fork_cells=-21, bay_capacity_vehicles=k))['stats'] for k in (1,2,4,8)]
            self.assertEqual(len({x['arrivals'] for x in runs}),1)
            for x in runs:
                self.assertEqual(x['arrivals'],x['exits']+x['remaining'])
    def test_fixed_geometry_unchanged_when_capacity_varies(self):
        configs=[Config(fixed_fork_cells=-21,bay_capacity_vehicles=k) for k in (1,2,4,8)]
        self.assertEqual({c.fixed_fork_cells for c in configs},{-21})
        self.assertEqual({c.storage_ft for c in configs},{100})
    def test_identical_replay(self):
        c=Config(duration=300, fixed_fork_cells=-21,bay_capacity_vehicles=4,seed=3)
        self.assertEqual(simulate(c),simulate(c))
    def test_incompatible_storage_rejected(self):
        with self.assertRaises(AssertionError):
            simulate(Config(duration=30,storage_ft=200,fixed_fork_cells=-21))
if __name__=='__main__':
    unittest.main()
