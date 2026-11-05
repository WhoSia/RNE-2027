import random
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'src'))
from phase_network import Step, Movement, DeadlockError, simulate


def m(identity, at, lane, steps):
    return Movement(identity, at, lane, 'car', tuple(Step(tuple(z), d) for z,d in steps))


class PhaseNetworkTests(unittest.TestCase):
    def test_y_hold_and_wait_case(self):
        xs=[m('ped',0,'P',[(('B',),3)]),m('car',0,'A',[(('A',),2),(('B',),2)]),m('following',1,'A',[(('A',),1)])]
        r=simulate(xs, {'A':1,'B':1})
        self.assertEqual((r.starts['following'],r.finishes['car']), (3,5))
        self.assertIn((3,'transition','car',('B',)),r.log)
    def test_nonoverlapping_zones_parallel(self):
        xs=[m('a',0,'L1',[(('A',),5)]),m('b',1,'L2',[(('B',),2)])]
        self.assertEqual(simulate(xs,{'A':1,'B':1}).starts['b'],1)
    def test_partial_overlap_blocks(self):
        xs=[m('car',0,'A',[(('north','shared'),5)]),m('ped',1,'B',[(('shared','south'),1)]),m('far',1,'C',[(('remote',),1)])]
        r=simulate(xs,{'north':1,'shared':1,'south':1,'remote':1})
        self.assertEqual((r.starts['ped'],r.starts['far']), (5,1))
    def test_multizone_atomic(self):
        xs=[m('holder',0,'A',[(('Z2',),4)]),m('multi',1,'B',[(('Z1','Z2'),2)]),m('independent',1,'C',[(('Z3',),1)])]
        r=simulate(xs,{'Z1':1,'Z2':1,'Z3':1})
        self.assertEqual((r.starts['multi'],r.starts['independent']), (4,1))
        self.assertLessEqual(r.max_occupancy['Z2'], 1)
    def test_finite_storage_capacity(self):
        xs=[m(str(i),0,'L'+str(i),[(('A',),3)]) for i in range(3)]
        r=simulate(xs,{'A':2})
        self.assertEqual(sorted(r.starts.values()),[0,0,3])
        self.assertEqual(r.max_occupancy['A'],2)
    def test_same_lane_queue(self):
        xs=[m('a',0,'L',[(('A',),2)]),m('b',0,'L',[(('B',),1)])]
        r=simulate(xs,{'A':1,'B':1})
        self.assertEqual(r.starts['b'],0)
    def test_cycle_detected(self):
        xs=[m('a',0,'L1',[(('A',),2),(('B',),1)]),m('b',0,'L2',[(('B',),2),(('A',),1)])]
        with self.assertRaises(DeadlockError) as e:
            simulate(xs,{'A':1,'B':1})
        self.assertEqual(set(e.exception.cycle[:-1]),{'a','b'})
    def test_no_future_source_capacity(self):
        xs=[m('a',0,'A',[(('A',),4)]),m('b',1,'B',[(('A',),1)])]
        self.assertEqual(simulate(xs,{'A':1}).starts['b'],4)
    def test_validates_bad_inputs(self):
        for xs, cap in [([m('a',-1,'L',[(('A',),1)])],{'A':1}),([m('a',0,'L',[(('A',),0)])],{'A':1}),([m('a',0,'L',[(('A',),1)])],{'A':0}),([m('a',0,'L',[(('X',),1)])],{'A':1})]:
            with self.assertRaises(ValueError):simulate(xs,cap)
    def test_randomized_capacity_and_conservation(self):
        rng=random.Random(20261106)
        for _ in range(100):
            xs=[]
            for i in range(40):
                lane='L'+str(i%4)
                zone='Z'+str(i%4)
                xs.append(m(str(i),rng.randrange(0,20),lane,[((zone,),rng.randrange(1,8))]))
            r=simulate(xs,{f'Z{i}':2 for i in range(4)})
            self.assertEqual(len(r.starts),40)
            self.assertEqual(len(r.finishes),40)
            self.assertTrue(all(r.finishes[k]>r.starts[k] for k in r.starts))
            self.assertTrue(all(v<=2 for v in r.max_occupancy.values()))

if __name__ == '__main__':unittest.main()
