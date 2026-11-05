import unittest
from src.micro_network import Link,Signal,Crossing,BusStop,Demand,Network,shortest_distance_route
from src.experiments import OD,generate_od_demand, network_fixture,run_pair
from src.validation import validate_trajectories,score_pair,split_dates,emission_conservation

class KinematicsAndGeometry(unittest.TestCase):
    def test_speed_is_nonnegative_and_bounded(self):
        net=Network([Link('a',50,speed_mps=6)],dt_s=.25)
        out=net.run([Demand('v',0,('a',),desired_speed_mps=10)],30)
        data=out.traces['v']
        self.assertTrue(all(0 <= p[3] <= 6.0001 for p in data))
        self.assertTrue(all(b[2]>=a[2] for a,b in zip(data,data[1:])))
        self.assertIn('v',out.completed_s)
    def test_curve_and_grade_reduce_speed_ceiling(self):
        n=Network([Link('a',50,10,grade=.1,curve_radius_m=10)])
        self.assertLess(n.speed_cap(n.links['a']),10)
    def test_invalid_geometry_rejected(self):
        with self.assertRaises(ValueError):Network([Link('a',-1)])
        with self.assertRaises(ValueError):Network([Link('a',10,curve_radius_m=0)])
    def test_long_vehicle_rejected(self):
        net=Network([Link('a',5)])
        with self.assertRaises(ValueError):net.run([Demand('b',0,('a',),length_m=11)],20)

class FiniteStorageAndCausality(unittest.TestCase):
    def test_two_cars_no_overlap(self):
        net=Network([Link('a',20)],dt_s=.25)
        out=net.run([Demand('a',0,('a',)),Demand('b',0,('a',))],60)
        self.assertEqual(len(out.completed_s),2)
        self.assertGreater(out.admitted_s['b'],out.admitted_s['a'])
    def test_bus_defers_following_car(self):
        net=Network([Link('a',15)],dt_s=.5)
        out=net.run([Demand('b',0,('a',),length_m=11,kind='bus'),Demand('c',0,('a',))],60)
        self.assertGreater(out.admitted_s['c'],0)
    def test_fixed_red_signal_delays_without_policy_search(self):
        n=Network([Link('a',12,8)],signals={'a':Signal(30,((15,30),))},dt_s=.5)
        out=n.run([Demand('v',0,('a',))],60)
        self.assertGreaterEqual(out.completed_s['v'],15)
        self.assertGreater(out.blocked.get('red',0),0)
    def test_downstream_closed_prevents_retroactive_transfer(self):
        n=Network([Link('a',10,8),Link('b',10,8)],dt_s=.5)
        a=n.run([Demand('v',0,('a','b'))],40,{'a':15})
        b=n.run([Demand('v',0,('a','b'))],40)
        self.assertGreater(a.completed_s['v'],b.completed_s['v'])
        self.assertTrue(all(t>=15 for t,vid,src,dst in a.transfers if src=='a'))
    def test_vehicle_conservation_and_time_order(self):
        net,demands,closed=network_fixture(downstream_block=20)
        r=net.run(demands,120,closed)
        self.assertEqual(len(r.completed_s),len(demands))
        self.assertTrue(all(r.completed_s[k]>=r.admitted_s[k] for k in r.completed_s))
        self.assertTrue(all(b[0]>=a[0] for a,b in zip(r.occupancies,r.occupancies[1:])))
        self.assertGreater(r.blocked.get('downstream_closed',0),0)
        for t,occ in r.occupancies:self.assertTrue(all(n>=0 for n in occ.values()))

class CrosswalkBusAndRoutes(unittest.TestCase):
    def test_crossing_occupancy_block(self):
        base=[Link('a',10,8,junction='J')]
        plain=Network(base,dt_s=.5).run([Demand('v',0,('a',))],30)
        blocked=Network(base,dt_s=.5,crossings=[Crossing('J',((0,15),))]).run([Demand('v',0,('a',))],30)
        self.assertGreaterEqual(blocked.completed_s['v'],15)
        self.assertGreater(blocked.completed_s['v'],plain.completed_s['v'])
    def test_bus_stop_increases_dwell(self):
        net=[Link('a',30,8)]
        bus=Demand('bus',0,('a',),length_m=11,kind='bus')
        plain=Network(net,dt_s=.5).run([bus],50)
        dwell=Network(net,stops=[BusStop('a',20,0,5)],dt_s=.5).run([bus],50)
        self.assertGreater(dwell.completed_s['bus'],plain.completed_s['bus'])
    def test_merging_one_transfer_per_junction_tick(self):
        links=[Link('a',10,8,junction='J'),Link('b',10,8,junction='J'),Link('c',15,8)]
        ds=[Demand('x',0,('a','c')),Demand('y',0,('b','c'))]
        r=Network(links,dt_s=.5).run(ds,70)
        times=[t for t,mid,a,b in r.transfers]
        self.assertEqual(len(times),2)
        self.assertEqual(len(set(times)),2)
    def test_static_network_distance(self):
        links=[Link('a',10),Link('b',100),Link('c',20),Link('d',10)]
        d,p=shortest_distance_route(links,{'a':('b','c'),'c':('d',)},'a','d')
        self.assertEqual(p,('a','c','d'))
        self.assertEqual(d,30)

class ReproductionAndDemand(unittest.TestCase):
    def test_seed_repeatability(self):
        o=OD('a','b',900)
        self.assertEqual(generate_od_demand(o,('a',),100,42),generate_od_demand(o,('a',),100,42))
    def test_date_disjoint(self):
        a=[{'date':'2026-11-06','value':2},{'date':'2026-11-07','value':3}]
        x,y=split_dates(a,{'2026-11-07'})
        self.assertEqual(len(x),1);self.assertEqual(len(y),1)
    def test_traj_must_increase(self):
        with self.assertRaises(ValueError):validate_trajectories([{'id':'1','t_s':1,'x_m':1,'v_mps':1,'link':'a'},{'id':'1','t_s':1,'x_m':2,'v_mps':1,'link':'a'}])
    def test_scoring_unit(self):
        result=score_pair([1,2,4],[1,3,5],'m')
        self.assertAlmostEqual(result['mae'],2/3)
        with self.assertRaises(ValueError):score_pair([1],[2],'km')
    def test_conservation_gate(self):
        emission_conservation(4,1,1,2)
        with self.assertRaises(AssertionError):emission_conservation(4,1,1,1)
    def test_pair_comparison(self):
        r=run_pair()
        self.assertEqual(r['closed']['completed'],5)
        self.assertGreater(r['closed']['blocked']['downstream_closed'],0)

if __name__=='__main__':unittest.main()
