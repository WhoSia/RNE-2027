import unittest
from geometry import ClearanceGraph
from temporal_conflicts import Occupancy, audit, can_enter, overlap
from network_v57 import make_arrivals,DEMANDS,PLANS,PocketGeometry,ParallelSignalPlan,simulate
from network_v56 import simulate as historical_simulate

G=ClearanceGraph(2.5)
class IntervalTests(unittest.TestCase):
    def test_overlap_strict_half_open(self):
        a=Occupancy(0,'W>E',1,3,1)
        self.assertTrue(overlap(a,Occupancy(0,'N>E',2.999,4,2)))
        self.assertFalse(overlap(a,Occupancy(0,'N>E',3,4,2)))
    def test_cross_stage_conflict_detected(self):
        events=[Occupancy(0,'W>E',2.,5.,1),Occupancy(0,'N>E',4.,6.,2)]
        self.assertEqual(audit(events,G)['conflicting_intervals'],1)
        self.assertFalse(can_enter(0,'N>E',4.,2.,events[:1],G))
    def test_cross_stage_after_clearance_allowed(self):
        events=[Occupancy(0,'W>E',2.,5.,1)]
        self.assertTrue(can_enter(0,'N>E',5.,2.,events,G))
    def test_nonconflicting_parallel_allowed(self):
        events=[Occupancy(1,'W>E',2.,5.,1),Occupancy(1,'N>W',3.,6.,2)]
        self.assertEqual(audit(events,G)['conflicting_intervals'],0)
        self.assertTrue(can_enter(1,'N>W',3.,3.,events[:1],G))
    def test_different_junction_is_independent(self):
        a=[Occupancy(0,'W>E',2.,8.,1)]
        self.assertTrue(can_enter(1,'N>E',3.,2.,a,G))
    def test_same_movement_uses_external_headway(self):
        a=[Occupancy(0,'W>E',2.,8.,1)]
        self.assertTrue(can_enter(0,'W>E',3.,3.,a,G))
    def test_bad_occupancy_inputs(self):
        with self.assertRaises(ValueError):Occupancy(0,'N>E',3,2,1)
        with self.assertRaises(ValueError):can_enter(0,'W>E',0,-1,[],G)
        with self.assertRaises(ValueError):audit([Occupancy(0,'unknown',0,1,1)],G)
    def test_zero_duration_bit_exact_historical(self):
        for d in DEMANDS:
            for seed in (202,203,204,205):
                a=make_arrivals(d,seed,arrive_until=130)
                kw=dict(horizon=240,pockets=PocketGeometry((30,30,0)))
                for plan in (PLANS[0],ParallelSignalPlan(PLANS[0],12)):
                    old=historical_simulate(plan,a,**kw)['summary']
                    new=simulate(plan,a,occupancy_s=0,**kw)['summary']
                    for col in ('completed','system_vehicle_seconds_in_horizon','release_events','blocked_transfers','parallel_crossing_slots'):
                        self.assertEqual(old[col],new[col],(d.name,seed,col))
    def test_real_occupancy_intervals_never_conflict(self):
        for d in DEMANDS:
            a=make_arrivals(d,208,arrive_until=130)
            res=simulate(ParallelSignalPlan(PLANS[0],12),a,horizon=240,pockets=PocketGeometry((30,30,0)),occupancy_s=5)
            self.assertEqual(audit(res['occupancies'],G)['conflicting_intervals'],0)
            self.assertEqual(res['summary']['occupancy_conflicts'],0)
            self.assertAlmostEqual(res['summary']['exposure_reconstruction_error_s'],0)
            s=res['summary']
            self.assertEqual(s['generated'],s['completed']+s['remaining_inside']+s['pending_boundary'])
    def test_occupancy_stress_changes_result(self):
        a=make_arrivals(DEMANDS[2],201,arrive_until=180)
        kw=dict(horizon=300,pockets=PocketGeometry((30,30,0)))
        p=ParallelSignalPlan(PLANS[0],12)
        early=simulate(p,a,occupancy_s=0,**kw)['summary']
        late=simulate(p,a,occupancy_s=9,**kw)['summary']
        self.assertGreater(late['system_vehicle_seconds_in_horizon'],early['system_vehicle_seconds_in_horizon'])
        self.assertLess(late['completed'],early['completed'])

if __name__=='__main__':unittest.main()
