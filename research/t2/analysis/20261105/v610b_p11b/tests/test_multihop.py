import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from network import Network,Lane,Movement,Phase,SignalPlan
from multihop import RouteEngine,RouteDemand
from multihop_demo import make_network,run

class MultiHopTest(unittest.TestCase):
 def test_route_continuity(self):
  with self.assertRaises(ValueError):RouteEngine(make_network(),(RouteDemand('a',('J0_main','J1_cross'),0),),100,{'link':3})
 def test_unknown_movement(self):
  with self.assertRaises(KeyError):RouteEngine(make_network(),(RouteDemand('a',('missing',),0),),100,{})
 def test_length_based_gate(self):
  a=(RouteDemand('a',('J0_main','J1_main'),0),RouteDemand('b',('J0_main','J1_main'),0))
  z=RouteEngine(make_network(link_storage=6.5),a,80,{'link':3}).run()
  self.assertEqual(z['completed'],2);self.assertEqual(z['peak_occupancy_m']['link'],6.5)
 def test_no_teleporting(self):
  z=RouteEngine(make_network(),(RouteDemand('a',('J0_main','J1_main'),0),),50,{'link':3}).run()
  a=[e for e in z['events'] if e['vehicle']=='a']
  x=next(e['t_s'] for e in a if e['event']=='connector_exit' and e['movement']=='J0_main')
  ready=next(e['t_s'] for e in a if e['event']=='link_ready')
  y=next(e['t_s'] for e in a if e['event']=='admit' and e['movement']=='J1_main')
  self.assertAlmostEqual(ready-x,3);self.assertGreaterEqual(y,ready)
 def test_upstream_held_until_downstream_admitted(self):
  z=RouteEngine(make_network(offset=4), (RouteDemand('a',('J0_main','J1_main'),0),),80,{'link':3}).run()
  a=[e for e in z['events'] if e['vehicle']=='a']
  ready=next(e['t_s'] for e in a if e['event']=='link_ready')
  free=next(e['t_s'] for e in a if e['event']=='upstream_freed')
  assert free>=ready
 def test_conservation_and_time_monotonicity(self):
  z=RouteEngine(make_network(), tuple(RouteDemand(str(i),('J0_main','J1_main'),i*.6) for i in range(9)),150,{'link':4}).run()
  self.assertEqual(z['completed']+z['unfinished'],z['total']);self.assertEqual(z['completed'],9)
  self.assertEqual([e['t_s'] for e in z['events']],sorted(e['t_s'] for e in z['events']))
 def test_earliest_source_arrival(self):
  z=RouteEngine(make_network(),(RouteDemand('a',('J0_main','J1_main'),2.5),),50,{'link':1}).run()
  self.assertGreaterEqual(min(e['t_s'] for e in z['events'] if e['event']=='admit'),2.5)
 def test_connected_offset_experiment(self):
  for x in (0,2,4):self.assertEqual(run(x)['completed'],20)
 def test_reproducible(self):
  self.assertEqual(run(3),run(3))
 def test_variable_cycle(self):
  n=make_network();self.assertEqual(n.plan('J0').cycle_s,6);self.assertEqual(n.plan('J1').cycle_s,8)
 def test_partial_horizon_counts_vehicles(self):
  z=RouteEngine(make_network(),(RouteDemand('a',('J0_main','J1_main'),0),),1,{'link':3}).run()
  self.assertEqual((z['completed'],z['unfinished']),(0,1))
 def test_footprint_rejected(self):
  with self.assertRaises(ValueError):RouteEngine(make_network(link_storage=6.5),(RouteDemand('a',('J0_main',),0,11),),10,{})

if __name__=='__main__':unittest.main()
