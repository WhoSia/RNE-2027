import unittest
from network_v51 import (
    Vehicle, DriverParameters, TurnParameters, MOVEMENTS, MOVEMENT_STAGE,
    SUCCESSOR, check_route, movement_for, DEMANDS, PLANS,
    make_arrivals, simulate,
)

class ConnectionTests(unittest.TestCase):
    def test_legal_generated_od(self):
        for demand in DEMANDS:
            for v in make_arrivals(demand, 19, 120.):
                self.assertTrue(check_route(v.route))

    def test_teleport_rejected(self):
        for route in (("M0","M2"),("S1","M1"),("M1",),("S2","M0"),()):
            with self.assertRaises(ValueError):check_route(route)
        with self.assertRaises(ValueError):
            simulate(PLANS[0],[Vehicle(0,0.,("M0","M2"))], horizon=20.)

    def test_duplicate_ids_rejected(self):
        with self.assertRaisesRegex(ValueError,"duplicate"):
            simulate(PLANS[0],[Vehicle(7,0.,("M0",)),Vehicle(7,0.,("S1",))],horizon=20.)

    def test_birth_alignment_rejected(self):
        with self.assertRaisesRegex(ValueError,"timestep aligned"):
            simulate(PLANS[0],[Vehicle(0,.31,("S0",))],horizon=20.)

    def test_connection_taxonomy(self):
        self.assertEqual(movement_for("M0","M1"),"main_through")
        self.assertEqual(movement_for("M0",None),"main_exit")
        self.assertEqual(movement_for("S0","M1"),"side_merge")
        self.assertEqual(movement_for("S0",None),"side_exit")
        with self.assertRaises(ValueError):movement_for("S2","M2")

    def test_invalid_turn_headways(self):
        for val in (0.,float('inf'),float('nan')):
            with self.assertRaises(ValueError):TurnParameters(side_merge_s=val)

    def test_crossing_phase_and_route_and_counts(self):
        arrivals=make_arrivals(DEMANDS[0], 11, arrive_until=120)
        r=simulate(PLANS[2],arrivals,horizon=250.)
        c=r['crossings']
        self.assertTrue(c)
        for e in c:
            self.assertEqual(e['phase'],MOVEMENT_STAGE[e['movement']])
            self.assertEqual(e['to_link'],SUCCESSOR[e['from_link']] if e['movement'] in ('main_through','side_merge') else None)
        counts=r['summary']['crossings_by_movement']
        self.assertEqual(sum(counts.values()),len(c))
        self.assertEqual(len(c),r['summary']['release_events'])
        self.assertTrue(any(e['movement']=='side_merge' for e in c))
        self.assertTrue(any(e['movement']=='main_through' for e in c))
        self.assertEqual(r['summary']['generated'],r['summary']['completed']+r['summary']['remaining_inside']+r['summary']['pending_boundary'])
        self.assertAlmostEqual(r['summary']['system_vehicle_seconds_in_horizon'],r['summary']['completed_vehicle_seconds']+r['summary']['right_censored_vehicle_seconds'])

    def test_turning_headway_has_effect(self):
        arrivals=make_arrivals(DEMANDS[2],29,arrive_until=200)
        p=PLANS[0]
        base=simulate(p,arrivals,horizon=360.)['summary']['system_vehicle_seconds_in_horizon']
        delayed=simulate(p,arrivals,horizon=360.,turns=TurnParameters(side_merge_s=8.,main_exit_s=5.))['summary']['system_vehicle_seconds_in_horizon']
        self.assertNotEqual(base,delayed)

    def test_no_simultaneous_conflicting_stage(self):
        r=simulate(PLANS[1],make_arrivals(DEMANDS[2],11,130.),horizon=220.)
        use={}
        for e in r['crossings']:
            k=(e['junction'],e['t_s'])
            use.setdefault(k,set()).add(e['phase'])
        self.assertTrue(all(len(v)<=1 for v in use.values()))

    def test_rejected_merge_does_not_compress_followers(self):
        # Regression for observed v5.1 failure near step 951, side S1.
        from experiment_v50 import plan
        arrivals=make_arrivals(DEMANDS[1],11,arrive_until=320.)
        r=simulate(plan(38,'progression'),arrivals,horizon=480.,
            turns=TurnParameters(main_exit_s=5.,side_merge_s=7.))
        self.assertGreater(r['summary']['blocked_transfers'],0)
        self.assertEqual(r['summary']['generated'],r['summary']['completed']+
                         r['summary']['remaining_inside']+r['summary']['pending_boundary'])

    def test_default_turn_matches_explicit_baseline(self):
        a=make_arrivals(DEMANDS[0],11,80.)
        s1=simulate(PLANS[1],a,horizon=150.)['summary']
        s2=simulate(PLANS[1],a,horizon=150.,turns=TurnParameters())['summary']
        self.assertEqual(s1,s2)

if __name__=='__main__':unittest.main()
