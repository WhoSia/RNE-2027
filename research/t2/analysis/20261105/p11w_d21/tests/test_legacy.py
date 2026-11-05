import unittest, random, sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from lane_fifo import Demand,simulate

class TestLaneFIFO(unittest.TestCase):
    def test_independent_lane_not_blocked(self):
        ds=[Demand(0,'holdA','A',('ra',),10),Demand(.1,'a2','A',('ra',),1),Demand(.2,'b','B',('rb',),1)]
        s=simulate(ds,{'ra':1,'rb':1});self.assertEqual(s.entries['b'],.2);self.assertEqual(s.entries['a2'],10)
    def test_lane_fifo(self):
        ds=[Demand(0,'a','A',('r',),4),Demand(.1,'b','A',('r',),1),Demand(.2,'c','A',('r',),1)]
        self.assertEqual(simulate(ds,{'r':1}).entries,{'a':0,'b':4,'c':5})
    def test_conflicts_cross_lanes(self):
        ds=[Demand(0,'car','A',('road',),2,'car'),Demand(.2,'walk','P',('cross',),3,'ped')]
        z=simulate(ds,{'road':1,'cross':1},{frozenset(('ped','car'))});self.assertEqual(z.entries['walk'],2)
    def test_concurrent_release_before_arrival(self):
        ds=[Demand(0,'a','A',('r',),2),Demand(2,'b','B',('r',),1)];self.assertEqual(simulate(ds,{'r':1}).entries['b'],2)
    def test_resource_capacity(self):
        ds=[Demand(0,'a','A',('r',),3),Demand(0,'b','B',('r',),3),Demand(0,'c','C',('r',),1)]
        z=simulate(ds,{'r':2});self.assertEqual(z.entries['c'],3);self.assertEqual(z.max_occupation['r'],2)
    def test_invalid(self):
        with self.assertRaises(ValueError):simulate([Demand(0,'x','A',('r',),1)] ,{'r':0})
        with self.assertRaises(ValueError):simulate([Demand(0,'x','A',('r',),1),Demand(1,'x','B',('r',),1)],{'r':1})
        with self.assertRaises(ValueError):simulate([Demand(0,'x','A',('s',),1)],{'r':1})
        with self.assertRaises(ValueError):simulate([Demand(0,'x','A',('r',),float('nan'))],{'r':1})
    def test_many_random_demands_conservation_monotonicity(self):
        rng=random.Random(20261105)
        for _ in range(20):
            ds=[Demand(rng.randint(0,25)/5,str(i),f'L{i%3}',(f'R{i%3}',),rng.randint(1,10)/5) for i in range(120)]
            z=simulate(ds,{f'R{k}':1 for k in range(3)})
            self.assertEqual(len(z.entries),120);self.assertEqual(len(z.exits),120)
            tt=[t for t,_,_ in z.log];self.assertTrue(all(a<=b for a,b in zip(tt,tt[1:])))
            self.assertTrue(all(z.entries[d.identity]>=d.at for d in ds))
            self.assertTrue(all(z.max_occupation[r]<=1 for r in z.max_occupation))
    def test_two_resources_atomic(self):
        ds=[Demand(0,'a','A',('r','s'),2),Demand(.2,'b','B',('s',),1),Demand(.3,'c','C',('r',),1)]
        z=simulate(ds,{'r':1,'s':1});self.assertEqual(z.entries['b'],2);self.assertEqual(z.entries['c'],2)
