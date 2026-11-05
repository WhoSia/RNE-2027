import unittest
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from lane_fifo import Demand, simulate

RULES = {frozenset({'car', 'ped'})}
C = {'ra':1, 'rb':1, 'rc':1, 'rd':1}

def d(t, ident, lane, resource, kind, zones, duration=2):
    return Demand(t, ident, lane, (resource,), duration, kind, zones)

class MultiZoneTests(unittest.TestCase):
    def test_partial_overlap_prevents_conflicting_admission(self):
        ds=[d(0,'a','A','ra','car',('j1','shared'),5),d(1,'b','B','rb','ped',('shared','j2'))]
        z=simulate(ds,C,RULES)
        self.assertEqual(z.entries['b'],5)
    def test_disjoint_sets_admit_concurrently(self):
        ds=[d(0,'a','A','ra','car',('j1','shared'),5),d(1,'b','B','rb','ped',('j2','j3'))]
        self.assertEqual(simulate(ds,C,RULES).entries['b'],1)
    def test_shared_zone_but_compatible_kind(self):
        ds=[d(0,'a','A','ra','car',('j1','shared'),5),d(1,'b','B','rb','car',('shared','j2'))]
        self.assertEqual(simulate(ds,C,RULES).entries['b'],1)
    def test_resource_capacity_remains_independent_of_zone(self):
        ds=[d(0,'a','A','ra','car',('j1',),5),d(1,'b','B','ra','ped',('j2',))]
        self.assertEqual(simulate(ds,C,RULES).entries['b'],5)
    def test_exact_release_admits(self):
        ds=[d(0,'a','A','ra','car',('shared',),5),d(5,'b','B','rb','ped',('shared',))]
        self.assertEqual(simulate(ds,C,RULES).entries['b'],5)
    def test_scalar_legacy(self):
        ds=[d(0,'a','A','ra','car','shared',5),d(1,'b','B','rb','ped',('shared','j2'))]
        self.assertEqual(simulate(ds,C,RULES).entries['b'],5)
    def test_reject_invalid_zone_shapes(self):
        invalid=[(),('',),('j','j'),['j'],42,('j',42)]
        for item in invalid:
            with self.subTest(item=item), self.assertRaises(ValueError):
                simulate([d(0,'a','A','ra','car',item)],C,RULES)
    def test_multi_hop_hold_is_atomic_for_full_duration(self):
        ds=[d(0,'a','A','ra','car',('junction1','junction2'),5),d(1,'b','B','rb','ped','junction2',1)]
        self.assertEqual(simulate(ds,C,RULES).entries['b'],5)
    def test_separate_8_junctions_have_no_cross_talk(self):
        ds=[]
        for i in range(8):
            ds += [d(0,f'c{i}',f'C{i}',f'car{i}','car',(f'j{i}',f'bridge{i}'),5), d(1,f'p{i}',f'P{i}',f'ped{i}','ped',(f'j{i}',))]
        cap={r:1 for demand in ds for r in demand.resources}
        z=simulate(ds,cap,RULES)
        self.assertEqual([z.entries[f'p{i}'] for i in range(8)],[5]*8)
        self.assertEqual(len(z.exits),16)
