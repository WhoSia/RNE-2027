"""Regression tests for split-diverge prototype v0.3."""
import unittest
from spatial_v03 import Config,simulate

class TestSpatialV03(unittest.TestCase):
    def test_conservation(self):
        for ft in (100,200,400,500):
            s=simulate(Config(storage_ft=ft,duration=600))['stats']
            self.assertEqual(s['arrivals'],s['exits']+s['remaining'])
    def test_deterministic(self):
        a=simulate(Config(duration=300,seed=2))
        b=simulate(Config(duration=300,seed=2))
        self.assertEqual(a,b)
    def test_known_seed_zero(self):
        values=[simulate(Config(seed=0,storage_ft=L))['stats']['exits'] for L in (100,200,400,500)]
        self.assertEqual(values,[1960,2021,2066,2071])
    def test_all_seed_results(self):
        expected=[
        [1960,2021,2066,2071],[1944,2007,2054,2054],
        [1979,2027,2071,2083],[1964,2017,2034,2035],
        [1980,2027,2062,2063],[1937,1979,1994,2013],
        [1958,2021,2048,2049],[1937,1976,1993,1993],
        [1952,2020,2035,2036],[1968,2019,2056,2059]]
        for seed,row in enumerate(expected):
            observed=[simulate(Config(seed=seed,storage_ft=L))['stats']['exits'] for L in (100,200,400,500)]
            self.assertEqual(observed,row)
if __name__=='__main__':
    unittest.main()
