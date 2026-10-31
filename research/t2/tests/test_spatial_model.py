"""Minimal deterministic tests. Run: python -m unittest discover -s research/t2/tests -v"""
import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from spatial_model import Config,simulate

class TestSpatialModel(unittest.TestCase):
    def test_vehicle_conservation(self):
        for ft in (100,500):
            r=simulate(Config(storage_ft=ft,duration=600))
            s=r['stats']
            self.assertEqual(s['arrivals'],s['exits']+s['remaining'])
    def test_deterministic_seed(self):
        a=simulate(Config(duration=450,storage_ft=100))
        b=simulate(Config(duration=450,storage_ft=100))
        self.assertEqual(a['stats'],b['stats'])
        self.assertEqual(a['trajectories'],b['trajectories'])
    def test_coordinates_change(self):
        r=simulate(Config(duration=600),trace=(100,180))
        from collections import defaultdict
        byvehicle=defaultdict(set)
        for t,i,l,m,x in r['trajectories']:
            byvehicle[i].add(x)
        self.assertTrue(any(len(x)>1 for x in byvehicle.values()))
    def test_outside_lane_unchanged_with_bay_length(self):
        a=simulate(Config(duration=600,storage_ft=100))['stats']
        b=simulate(Config(duration=600,storage_ft=500))['stats']
        self.assertEqual(a.get('exit_outer',0),b.get('exit_outer',0))
    def test_known_unresolved_comparison(self):
        # Diagnostic, not an expected model property:
        # current prototype paradoxically predicts worse flow for longer bay.
        # Do not convert this to a claim about real intersections.
        a=simulate(Config(storage_ft=100))['stats']['exits']
        b=simulate(Config(storage_ft=500))['stats']['exits']
        self.assertEqual((a,b),(1700,1288))
if __name__=='__main__':
    unittest.main()
