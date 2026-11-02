"""T2 v4.9 deterministic self-checks; no traffic-field validation implied."""
import unittest
from network_v51 import *

class T2Tests(unittest.TestCase):
    def setUp(self):
        self.arrivals=make_arrivals(DEMANDS[0],seed=41,arrive_until=75.)

    def test_three_active_signal_groups(self):
        for j in range(3):
            phases={PLANS[0].phase(j,t*.5) for t in range(120)}
            self.assertEqual(phases,{'main','side','all_red'})

    def test_min_green_constraint(self):
        with self.assertRaises(ValueError):
            SignalPlan('invalid',(43,43,43),(0,0,0))

    def test_demand_determinism(self):
        a=make_arrivals(DEMANDS[0],12)
        b=make_arrivals(DEMANDS[0],12)
        self.assertEqual([(x.born,x.route) for x in a],[(x.born,x.route) for x in b])

    def test_valid_routes(self):
        valid={('M0',),('M0','M1'),('M0','M1','M2'),
               ('S0',),('S0','M1'),('S0','M1','M2'),
               ('S1',),('S1','M2'),('S2',)}
        for event in make_arrivals(DEMANDS[2],seed=17):
            self.assertIn(event.route,valid)

    def test_vehicle_conservation(self):
        result=simulate(PLANS[1],self.arrivals,horizon=210.)
        s=result['summary']
        self.assertEqual(s['generated'],s['completed']+s['remaining_inside']+s['pending_boundary'])

    def test_observed_all_3_junctions(self):
        demand=[Vehicle(j,0.,(f'S{j}',)) for j in range(3)]
        r=simulate(PLANS[0],demand,horizon=160.)
        self.assertEqual(r['summary']['completed'],3)
        self.assertEqual({x['destination'] for x in r['trips']},{'S0','S1','S2'})

    def test_exogenous_demand_identical(self):
        r=[simulate(p,self.arrivals,horizon=210.)['summary'] for p in PLANS]
        self.assertEqual(len({z['generated'] for z in r}),1)

    def test_idm_free_and_braking(self):
        self.assertGreater(idm_accel(0.,100.,0.),0.)
        self.assertLess(idm_accel(12.,2.,0.),0.)

    def test_speed_position_and_gap_nonnegative(self):
        r=simulate(PLANS[0],self.arrivals,horizon=220.,save_trajectory=True)
        for e in r['trajectories']:
            self.assertGreaterEqual(e['speed_mps'],0.)
            self.assertGreaterEqual(e['x_m'],0.)
            self.assertLessEqual(e['x_m'],LENGTHS[e['link']]+1e-8)

    def test_high_congestion_has_pending_or_inside(self):
        d=Demand('stress',52.,(19.,19.,19.),.0,.9)
        arrivals=make_arrivals(d,11,arrive_until=120.)
        r=simulate(PLANS[3],arrivals,horizon=150.)['summary']
        self.assertGreater(r['remaining_inside']+r['pending_boundary'],0)

    def test_completed_trip_duration_bounded(self):
        for s in simulate(PLANS[2],self.arrivals,horizon=210.)['trips']:
            self.assertGreater(s['duration_s'],0.)
            self.assertGreaterEqual(s['stopped_s'],0.)

    def test_no_trajectory_without_request(self):
        self.assertFalse(simulate(PLANS[0],self.arrivals,horizon=210.)['trajectories'])

    def test_zero_demand(self):
        s=simulate(PLANS[0],[],horizon=10.)['summary']
        self.assertEqual(s['completed'],0)
        self.assertIsNone(s['mean_completed_duration_s'])
        self.assertEqual(s['system_vehicle_seconds_in_horizon'],0)

if __name__=='__main__':unittest.main()
