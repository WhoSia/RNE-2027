import sys, unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from network import Lane,Movement,Phase,SignalPlan,Network
from multihop import RouteEngine,RouteDemand
from multihop_demo import make_network

def network(storage=6.5,offset=0):
    n=make_network(offset=offset)
    lanes=tuple(Lane(l.id,l.length_m,storage if l.id=='source' else l.storage_m) for l in n.lanes)
    return Network(lanes,n.movements,n.plans)

class SourceBoundTests(unittest.TestCase):
    def test_source_boundary_backpressure_and_conservation(self):
        n=network(storage=6.5)
        ds=tuple(RouteDemand(str(i),('J0_main','J1_main'),0) for i in range(3))
        z=RouteEngine(n,ds,100,{'link':3}).run()
        self.assertEqual(z['total'],3)
        self.assertEqual(z['completed'],3)
        self.assertAlmostEqual(z['peak_source_occupancy_m']['source'],6.5)
        self.assertEqual(sum(1 for e in z['events'] if e['event']=='source_enter'),3)
        ent=[e['t_s'] for e in z['events'] if e['event']=='source_enter']
        self.assertEqual(ent, sorted(ent))
        # Source occupancy can free at connector admission at the SAME instant;
        # distinct vehicle connector entrances must still honor clearance.
        admits=[e['t_s'] for e in z['events'] if e['event']=='admit' and e['movement']=='J0_main']
        self.assertEqual(len(admits),3)
        self.assertGreater(admits[1],admits[0]);self.assertGreater(admits[2],admits[1])
        self.assertEqual(z['external_waiting'],0)
    def test_external_queue_remains_unfinished_on_early_horizon(self):
        z=RouteEngine(network(),tuple(RouteDemand(str(i),('J0_main','J1_main'),0) for i in range(3)),1,{'link':3}).run()
        self.assertEqual(z['completed'],0)
        self.assertGreaterEqual(z['external_waiting'],1)
        self.assertEqual(z['total'],z['completed']+z['unfinished'])
    def test_reject_oversized_exogenous_vehicle(self):
        with self.assertRaisesRegex(ValueError,'entry lane'):
            RouteEngine(network(storage=6.5),(RouteDemand('truck',('J0_main','J1_main'),0,10),),50,{'link':3})
    def test_unbounded_baseline_changed_only_at_source(self):
        ds=tuple(RouteDemand(str(i),('J0_main','J1_main'),i*10) for i in range(4))
        a=RouteEngine(make_network(),ds,150,{'link':3}).run()
        b=RouteEngine(network(storage=6.5),ds,150,{'link':3}).run()
        self.assertEqual(a['completion_times'],b['completion_times'])
    def test_horizon_robustness_and_time_monotonicity(self):
        z=RouteEngine(network(storage=6.5,offset=2),tuple(RouteDemand(str(i),('J0_main','J1_main'),0) for i in range(8)),300,{'link':5}).run()
        times=[x['t_s'] for x in z['events']]
        self.assertEqual(times,sorted(times))
        self.assertEqual(z['completed'],8)
    def test_first_source_event_never_precedes_arrival(self):
        ds=(RouteDemand('first',('J0_main','J1_main'),1.7),)
        z=RouteEngine(network(),ds,50,{'link':1}).run()
        entry=next(e['t_s'] for e in z['events'] if e['event']=='source_enter')
        self.assertAlmostEqual(entry,1.7)
if __name__=='__main__': unittest.main()

class SharedLaneFIFOTests(unittest.TestCase):
    def test_shared_lane_no_bypass_on_green_other_movement(self):
        lane=(Lane('s',30,13),Lane('a',30,13),Lane('b',30,13))
        moves=(Movement('M','J','s','a','straight',1,('S',)),Movement('S','J','s','b','left',1,('M',)))
        plan=(SignalPlan('J',(Phase(4,frozenset({'M'})),Phase(2,frozenset()),Phase(4,frozenset({'S'})),Phase(2,frozenset()))),)
        net=Network(lane,moves,plan)
        demand=(RouteDemand('first',('S',),0),RouteDemand('second',('M',),0))
        z=RouteEngine(net,demand,40,{}).run()
        enter={e['vehicle']:e['t_s'] for e in z['events'] if e['event']=='admit'}
        self.assertEqual((enter['first'],enter['second']),(6,12))
        self.assertEqual(z['completed'],2)
    def test_capacity_throttles_source_enter_events_but_not_source_arrivals(self):
        ds=tuple(RouteDemand(str(i),('J0_main','J1_main'),0) for i in range(6))
        z=RouteEngine(network(storage=6.5),ds,200,{'link':5}).run()
        self.assertEqual(sum(e['event']=='arrival' for e in z['events']),6)
        self.assertEqual(sum(e['event']=='source_enter' for e in z['events']),6)
        self.assertEqual(z['completed'],6)
