import unittest
from dual_lane_v11 import run,DualConfig
from spatial_v10 import Config

class QueueAreaTests(unittest.TestCase):
    def test_empty_demand_has_zero_areas(self):
        r=run(DualConfig(base=Config(duration_s=240,demand_vph=0)))
        for key in ('outside_vehicle_seconds','upstream_vehicle_seconds','receiver_vehicle_seconds'):
            self.assertEqual(r[key],0)
    def test_integrals_conserve_occupancy_time_bound(self):
        b=Config(duration_s=480,demand_vph=1800)
        for h in (2,4,8):
            r=run(DualConfig(base=b,receiver_slots=2,receiver_headway_s=h))
            area=sum(r[k] for k in ('outside_vehicle_seconds','upstream_vehicle_seconds',
                                     'receiver_vehicle_seconds'))
            self.assertGreater(area,0)
            self.assertLessEqual(area,r['generated']*b.duration_s)
    def test_nonnegative_queue_areas(self):
        r=run(DualConfig(base=Config(duration_s=360),receiver_slots=1,receiver_headway_s=8))
        for key in ('outside_vehicle_seconds','upstream_vehicle_seconds','receiver_vehicle_seconds'):
            self.assertGreaterEqual(r[key],0)

if __name__=='__main__':unittest.main(verbosity=2)
