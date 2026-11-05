import unittest
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from lane_fifo import Demand,simulate

C={frozenset(('car','ped'))}

class SpatialConflictTests(unittest.TestCase):
    def test_legacy_global_behavior_preserved(self):
        ds=[Demand(0,'a','A',('r1',),5,'car'),Demand(1,'b','B',('r2',),1,'ped')]
        self.assertEqual(simulate(ds,{'r1':1,'r2':1},C).entries['b'],5)
    def test_separate_intersections_no_global_block(self):
        ds=[Demand(0,'a','A',('r1',),5,'car','intersection-A'),Demand(1,'b','B',('r2',),1,'ped','intersection-B')]
        self.assertEqual(simulate(ds,{'r1':1,'r2':1},C).entries['b'],1)
    def test_same_intersection_blocks(self):
        ds=[Demand(0,'a','A',('r1',),5,'car','junction'),Demand(1,'b','B',('r2',),1,'ped','junction')]
        self.assertEqual(simulate(ds,{'r1':1,'r2':1},C).entries['b'],5)
    def test_resource_capacity_global_even_in_other_zone(self):
        ds=[Demand(0,'a','A',('shared',),4,'car','A'),Demand(1,'b','B',('shared',),1,'ped','B')]
        self.assertEqual(simulate(ds,{'shared':1},C).entries['b'],4)
    def test_simultaneous_release_before_request(self):
        ds=[Demand(0,'a','A',('r1',),3,'car','same'),Demand(3,'b','B',('r2',),1,'ped','same')]
        self.assertEqual(simulate(ds,{'r1':1,'r2':1},C).entries['b'],3)
    def test_multi_intersection_independence(self):
        ds=[]
        for i in range(12):
            ds.append(Demand(0,f"car_{i}",f"C{i}",(f"rC{i}",),5,"car",f"J{i}"))
            ds.append(Demand(1,f"ped_{i}",f"P{i}",(f"rP{i}",),1,"ped",f"J{i}"))
        cap={r:1 for d in ds for r in d.resources}
        z=simulate(ds,cap,C)
        self.assertTrue(all(z.entries[f"ped_{i}"]==5 for i in range(12)))
        self.assertEqual(len(z.entries),24)
        self.assertEqual(len(z.exits),24)
    def test_empty_zone_rejected(self):
        ds=[Demand(0,'a','A',('r',),1,'car','')]
        with self.assertRaises(ValueError):simulate(ds,{'r':1},C)
    def test_no_intersection_conflict_when_no_rule(self):
        ds=[Demand(0,'a','A',('r1',),3,'car','j'),Demand(0,'b','B',('r2',),1,'ped','j')]
        self.assertEqual(simulate(ds,{'r1':1,'r2':1}).entries,{'a':0,'b':0})
    def test_default_conflict_zone_global_is_explicit_in_audit(self):
        self.assertEqual(Demand(0,'x','l',('r',),1).conflict_zone,'global')

if __name__=='__main__':unittest.main()
