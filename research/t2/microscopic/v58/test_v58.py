import math,unittest
from geometry_v58 import path,ClearanceGraph
from path_occupancy import clipped_length,PathTimeModel
from network_v58 import make_arrivals,DEMANDS,PLANS,ParallelSignalPlan,PocketGeometry,simulate
from network_v57 import simulate as old_simulate

class PathOccupancyTests(unittest.TestCase):
    def test_straight_clip_exact(self):
        self.assertAlmostEqual(clipped_length(path('W','E'),8),16.)
        self.assertAlmostEqual(clipped_length(path('N','S'),8),16.)
    def test_path_asymmetry(self):
        routes=[path('W','E'),path('W','S'),path('N','W')]
        lens=[clipped_length(p,8) for p in routes]
        self.assertTrue(all(x>0 for x in lens));self.assertGreater(max(lens)-min(lens),0.1)
    def test_speed_effect_and_rounding(self):
        m=PathTimeModel()
        p=path('W','E')
        self.assertEqual(m.duration(p,8,.5),3.)
        self.assertEqual(m.duration(p,4,.5),5.5)
        self.assertEqual(m.duration(p,0,.5),5.5)
        self.assertEqual(m.duration(p,50,.5),2.)
    def test_corrected_right_turn_has_local_intersection_travel(self):
        from geometry import path as historical_path
        for origin,dest in [('N','W'),('W','S'),('S','E'),('E','N')]:
            self.assertEqual(clipped_length(historical_path(origin,dest),8),0.)
            self.assertGreater(clipped_length(path(origin,dest),8),0.)
    def test_clearance_conflicts_retained_at_original_threshold(self):
        from geometry import ClearanceGraph as HistoricGraph
        self.assertEqual(ClearanceGraph(2.5).incompatible,HistoricGraph(2.5).incompatible)
    def test_original_zero_duration_output_unchanged(self):
        for demand in DEMANDS:
            arrivals=make_arrivals(demand,202,arrive_until=90)
            p=ParallelSignalPlan(PLANS[0],12)
            kw=dict(horizon=160,pockets=PocketGeometry((30,30,0)),occupancy_s=0)
            a=old_simulate(p,arrivals,**kw)['summary']
            b=simulate(p,arrivals,**kw)['summary']
            for k in ('completed','system_vehicle_seconds_in_horizon','release_events','parallel_crossing_slots'):
                self.assertEqual(a[k],b[k])
    def test_bad_params(self):
        for kwargs in ({'half_width_m':-1},{'minimum_cross_speed_mps':0},{'maximum_cross_speed_mps':1},{'response_buffer_s':-1}):
            with self.assertRaises(ValueError):PathTimeModel(**kwargs)
        with self.assertRaises(ValueError):clipped_length(path('W','E'),float('nan'))
    def test_fixed_mode_regression(self):
        d=make_arrivals(DEMANDS[0],101,arrive_until=90)
        kw=dict(horizon=160,pockets=PocketGeometry((30,30,0)),occupancy_s=2.)
        p=ParallelSignalPlan(PLANS[0],12)
        a=old_simulate(p,d,**kw)['summary'];b=simulate(p,d,**kw)['summary']
        for k in ('completed','system_vehicle_seconds_in_horizon','blocked_transfers','release_events','occupancy_conflicts'):
            self.assertEqual(a[k],b[k])
    def test_path_mode_safe_and_conservative(self):
        for demand in (DEMANDS[0],DEMANDS[2]):
            arrivals=make_arrivals(demand,102,arrive_until=120)
            p=ParallelSignalPlan(PLANS[0],12)
            r=simulate(p,arrivals,horizon=220,pockets=PocketGeometry((30,30,0)),path_time=PathTimeModel())
            s=r['summary']
            self.assertEqual(s['occupancy_conflicts'],0)
            self.assertEqual(s['generated'],s['completed']+s['remaining_inside']+s['pending_boundary'])
            self.assertAlmostEqual(s['exposure_reconstruction_error_s'],0)
            self.assertGreater(s['occupancy_interval_events'],0)
            self.assertTrue(s['occupancy_mean_by_movement_s'])
    def test_invalid_both_sources(self):
        with self.assertRaises(ValueError):simulate(PLANS[0],[],horizon=10,occupancy_s=1,path_time=PathTimeModel())
if __name__=='__main__':unittest.main()
