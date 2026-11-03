import unittest
from geometry import ClearanceGraph
from network_v56 import (GEOMETRY_GRAPH,GEOMETRY_MOVEMENTS,ParallelSignalPlan,
                         PLANS,PocketGeometry,DEMANDS,make_arrivals,simulate,Vehicle)
class GeometryIntegrationTests(unittest.TestCase):
    def test_parallel_pair_is_geometry_compatible(self):
        self.assertTrue(GEOMETRY_GRAPH.compatible(('W>E','N>W')))
        self.assertFalse(GEOMETRY_GRAPH.compatible(('W>E','N>E')))
    def test_unchanged_standard_stage_is_still_sequential(self):
        a=make_arrivals(DEMANDS[0],42,arrive_until=90)
        z=simulate(PLANS[0],a,horizon=160,pockets=PocketGeometry((30,30,0)))
        self.assertEqual(z['summary']['parallel_crossing_slots'],0)
    def test_parallel_timing_zero_preserves_exact_prior_result(self):
        a=make_arrivals(DEMANDS[0],42,arrive_until=90)
        kw=dict(horizon=160,pockets=PocketGeometry((30,30,0)))
        old=simulate(PLANS[0],a,**kw)
        new=simulate(ParallelSignalPlan(PLANS[0],0),a,**kw)
        for k in ('completed','generated','system_vehicle_seconds_in_horizon','release_events','blocked_transfers'):
            self.assertEqual(old['summary'][k],new['summary'][k])
    def test_parallel_dispatch_actually_occurs(self):
        a=make_arrivals(DEMANDS[2],102,arrive_until=130)
        kw=dict(horizon=240,pockets=PocketGeometry((30,30,0)))
        res=simulate(ParallelSignalPlan(PLANS[0],12),a,**kw)
        self.assertGreater(res['summary']['parallel_crossing_slots'],0)
        self.assertEqual(res['summary']['generated'],res['summary']['completed']+res['summary']['remaining_inside']+res['summary']['pending_boundary'])
        self.assertAlmostEqual(res['summary']['exposure_reconstruction_error_s'],0)
    def test_conflicting_side_merge_does_not_dispatch_with_main(self):
        # Independently test geometry gating for merging into same receiving lane.
        self.assertFalse(GEOMETRY_GRAPH.compatible((GEOMETRY_MOVEMENTS['main_through'],GEOMETRY_MOVEMENTS['side_merge'])))
    def test_simulated_crossings_are_geometry_safe_per_tick(self):
        a=make_arrivals(DEMANDS[2],102,arrive_until=130)
        res=simulate(ParallelSignalPlan(PLANS[0],12),a,horizon=240,pockets=PocketGeometry((30,30,0)))
        groups={}
        for c in res['crossings']:
            groups.setdefault((c['junction'],round(c['t_s']/.5)),[]).append(GEOMETRY_MOVEMENTS[c['movement']])
        self.assertTrue(all(GEOMETRY_GRAPH.compatible(m) for m in groups.values()))
    def test_invalid_od(self):
        with self.assertRaises(ValueError):simulate(PLANS[0],[Vehicle(1,0,('S0','M2'))],horizon=10)
if __name__=='__main__':unittest.main()
