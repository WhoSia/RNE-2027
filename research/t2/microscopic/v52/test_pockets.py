import unittest
from network_v52 import (PocketGeometry, Vehicle, make_arrivals, simulate, PLANS, DEMANDS, LENGTHS,
                         MOVEMENT_STAGE)

class PocketTests(unittest.TestCase):
    def test_invalid_geometry(self):
        for lengths in ((-1,0,0),(200,0,0),(float('nan'),0,0),(1,2), (0,0,float('inf')), (0,0,20)):
            with self.assertRaises(ValueError):PocketGeometry(lengths)

    def test_storage_capacity(self):
        self.assertEqual(PocketGeometry((0,30,0)).capacity(0),0)
        self.assertEqual(PocketGeometry((0,30,0)).capacity(1),4)
        self.assertEqual(PocketGeometry((0,30,0)).capacity(2),0)

    def test_zero_bays_backward_compatible(self):
        import network_v51 as original
        for d in DEMANDS:
            for plan in PLANS[:3]:
                a=make_arrivals(d,11,180.)
                ref=original.simulate(plan,a,horizon=310.)['summary']
                new=simulate(plan,a,horizon=310.,pockets=PocketGeometry())['summary']
                for field in ('generated','completed','pending_boundary','remaining_inside',
                              'system_vehicle_seconds_in_horizon','blocked_transfers','release_events'):
                    self.assertEqual(ref[field],new[field],(d.name,plan.name,field))

    def test_exit_only_diverts_into_bay(self):
        cars=[Vehicle(1,0.,('M0',)),Vehicle(2,0.,('M0','M1','M2'))]
        res=simulate(PLANS[0],cars,240.,pockets=PocketGeometry((60,0,0)))
        self.assertEqual(res['summary']['generated'],2)
        self.assertGreater(res['summary']['pocket_diversions'],0)
        exits=[x for x in res['crossings'] if x['movement']=='main_exit' and x['junction']==0]
        self.assertTrue(exits)
        self.assertTrue(all(x['physical_lane']=='P0' for x in exits))
        self.assertTrue(all(x['phase']=='main' for x in res['crossings']))

    def test_zero_bay_keeps_exit_in_main(self):
        res=simulate(PLANS[0],[Vehicle(1,0.,('M0',))],240.,pockets=PocketGeometry())
        self.assertEqual(res['summary']['pocket_diversions'],0)
        self.assertEqual(res['crossings'][0]['physical_lane'],'M0')

    def test_terminal_outflow_is_not_a_turn(self):
        from network_v52 import movement_for
        self.assertEqual(movement_for('M2',None),'main_outflow')
        result=simulate(PLANS[0],[Vehicle(1,0.,('M0','M1','M2'))],240.,pockets=PocketGeometry((60,60,0)))
        self.assertTrue(any(x['movement']=='main_outflow' for x in result['crossings']))
        self.assertFalse(any(x['physical_lane']=='P2' for x in result['crossings']))

    def test_capacity_and_conservation_under_stress(self):
        bay=PocketGeometry((15,30,0))
        cars=make_arrivals(DEMANDS[1],11,320.)
        r=simulate(PLANS[2],cars,580.,pockets=bay)
        s=r['summary']
        self.assertEqual(s['generated'],s['completed']+s['remaining_inside']+s['pending_boundary'])
        self.assertAlmostEqual(s['system_vehicle_seconds_in_horizon'],s['completed_vehicle_seconds']+s['right_censored_vehicle_seconds'])
        for k,n in s['pocket_peak_occupancy'].items():
            self.assertLessEqual(n,s['pocket_capacity_vehicles'][k])
        self.assertGreater(s['pocket_diversions'],0)

    def test_one_crossing_per_junction_tick(self):
        r=simulate(PLANS[1],make_arrivals(DEMANDS[2],29,240.),440.,pockets=PocketGeometry((30,30,0)))
        crossings={(e['junction'],e['t_s']) for e in r['crossings']}
        self.assertEqual(len(crossings),len(r['crossings']))
        for e in r['crossings']:
            self.assertEqual(e['phase'],MOVEMENT_STAGE[e['movement']])

    def test_trajectory_lane_is_physical(self):
        r=simulate(PLANS[0],make_arrivals(DEMANDS[0],73,180.),300.,
                   pockets=PocketGeometry((60,60,0)),save_trajectory=True)
        lanes={rec['link'] for rec in r['trajectories']}
        self.assertTrue(any(x.startswith('P') for x in lanes))
        self.assertTrue(all(0<=x['x_m']<=LENGTHS['M'+x['link'][1:]] if x['link'].startswith('P') else
                            0<=x['x_m']<=LENGTHS[x['link']] for x in r['trajectories']))

if __name__=='__main__':unittest.main()
