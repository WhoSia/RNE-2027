import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from network import Lane,Movement,Phase,SignalPlan,Network
from events import EventEngine,Demand

def net(length=18):
 return Network((Lane('a',100,30),Lane('b',length,length),Lane('c',100,30)),
  (Movement('main','J','a','b','straight',2,('side',)),Movement('side','J','c','b','left',2,('main',))),
  (SignalPlan('J',(Phase(5,frozenset(['main']),'main green'),Phase(1,frozenset(),'all red'),Phase(5,frozenset(['side']),'side green'),Phase(1,frozenset(),'all red'))),))
class ContractTests(unittest.TestCase):
 def test_signal_half_open(self):
  p=net().plan('J')
  self.assertTrue(p.permits('main',0,2));self.assertTrue(p.permits('main',3,2));self.assertFalse(p.permits('main',4,2))
  self.assertFalse(p.permits('main',5));self.assertTrue(p.permits('side',6,2));self.assertFalse(p.permits('side',10,2))
 def test_periodic_and_offset(self):
  p=SignalPlan('J',(Phase(3,frozenset({'m'})),Phase(5,frozenset())),2)
  self.assertTrue(p.permits('m',2,3));self.assertFalse(p.permits('m',4,2));self.assertTrue(p.permits('m',10,3))
 def test_conflicting_simultaneous_green_blocked(self):
  n=net();with_conflict=SignalPlan('J',(Phase(10,frozenset(['main','side'])),))
  with self.assertRaisesRegex(ValueError,'conflicting'):Network(n.lanes,n.movements,(with_conflict,))
 def test_nonreciprocal_conflict_blocked(self):
  n=net();bad=Movement('side','J','c','b','left',2)
  with self.assertRaisesRegex(ValueError,'nonreciprocal'):Network(n.lanes,(n.movements[0],bad),n.plans)
 def test_missing_lane_blocked(self):
  n=net();bad=Movement('x','J','missing','b','right',2)
  with self.assertRaises(ValueError):Network(n.lanes,n.movements+(bad,),n.plans)
 def test_bad_storage_blocked(self):
  with self.assertRaises(ValueError):Lane('x',5,6)
 def test_zero_phase_blocked(self):
  with self.assertRaises(ValueError):Phase(0,frozenset())
 def test_arrival_and_clearance(self):
  z=EventEngine(net(),(Demand('a','main',0),),20).run()
  self.assertEqual((z['completed'],z['unfinished']),(1,0))
  self.assertEqual(next(e['t_s'] for e in z['events'] if e['event']=='release'),2)
 def test_queue_waits_for_signal(self):
  z=EventEngine(net(),(Demand('s','side',0),),20).run()
  self.assertEqual(next(e['t_s'] for e in z['events'] if e['event']=='admit'),6)
 def test_capacity_release_before_next_admit(self):
  z=EventEngine(net(7),(Demand('a','main',0),Demand('b','main',0)),20).run()
  entrants=[e['t_s'] for e in z['events'] if e['event']=='admit']
  self.assertEqual(entrants,[0,2]);self.assertEqual(z['completed'],2)
 def test_block_next_cycle_from_clearance(self):
  z=EventEngine(net(),(Demand('late','main',4),),20).run()
  self.assertEqual(next(e['t_s'] for e in z['events'] if e['event']=='admit'),12)
 def test_arrivals_do_not_backdate(self):
  z=EventEngine(net(),(Demand('a','main',0),Demand('s','side',0)),30).run()
  ts=[e['t_s'] for e in z['events']];self.assertEqual(ts,sorted(ts))
 def test_vehicle_conservation(self):
  z=EventEngine(net(),tuple(Demand(str(i),'main',i*.5) for i in range(10)),40).run()
  self.assertEqual(z['completed']+z['unfinished'],z['total'])
  self.assertEqual(z['completed'],10)
 def test_duplicate_id_blocked(self):
  with self.assertRaises(ValueError):EventEngine(net(),(Demand('a','main',0),Demand('a','side',1)),20)
if __name__=='__main__':unittest.main()
