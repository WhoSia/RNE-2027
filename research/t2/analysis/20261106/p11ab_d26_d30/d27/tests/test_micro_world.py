import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from micro_world import *

class MicroWorldTests(unittest.TestCase):
    def test_single_car_conservation(self):
        r={'A':Road('A',30,1,10)}
        o=run(r,[Vehicle('v',('A',),0)],horizon_s=30)
        self.assertEqual(o.admissions,{'v':0});self.assertIn('v',o.finishes)
        self.assertEqual(o.throughput_by_road['A'],1)
    def test_queue_following_no_overlaps(self):
        r={'A':Road('A',45,1,7)}
        o=run(r,[Vehicle(str(i),('A',),i) for i in range(7)],horizon_s=70)
        self.assertEqual(o.collision_violations,0);self.assertEqual(len(o.finishes),7)
    def test_storage_limit_two_buses_not_fit(self):
        r={'A':Road('A',17,1,2)}
        o=run(r,[Vehicle('bus',('A',),0,length_m=11),Vehicle('car',('A',),1,length_m=4.5)],horizon_s=20)
        self.assertGreater(o.admissions['car'],1)
    def test_signal_holds_until_green(self):
        r={'A':Road('A',9,1,10)}
        v=[Vehicle('a',('A',),0,desired_mps=10,accel_mps2=10)]
        o=run(r,v,horizon_s=20,signals={'A':FixedSignal(10,3,5)})
        self.assertGreaterEqual(o.finishes['a'],5)
    def test_pedestrian_crosswalk_occupancy_blocks(self):
        r={'A':Road('A',9,1,10)}
        v=[Vehicle('a',('A',),0,desired_mps=10,accel_mps2=10)]
        blocked=run(r,v,horizon_s=20,pedestrians={'A':[(0,5)]})
        free=run(r,v,horizon_s=20)
        self.assertGreater(blocked.finishes['a'],free.finishes['a'])
    def test_multi_link_and_bus_dwell(self):
        roads={'A':Road('A',20,1,10,('B',)),'B':Road('B',20,1,10)}
        v=[Vehicle('bus',('A','B'),0,length_m=8,stop_road='B',bus_dwell_s=3)]
        b=run(roads,v,horizon_s=40);c=run(roads,[Vehicle('car',('A','B'),0,length_m=8)],horizon_s=40)
        self.assertGreater(b.finishes['bus'],c.finishes['car'])
    def test_road_config_invalid(self):
        with self.assertRaises(ValueError):run({'A':Road('A',3,1,4,('Z',))},[],horizon_s=2)
    def test_two_link_backpressure(self):
        roads={'U':Road('U',13,1,8,('D',)),'D':Road('D',8,1,8)}
        vs=[Vehicle(str(i),('U','D'),i,length_m=5,accel_mps2=3) for i in range(5)]
        slow=run(roads,vs,horizon_s=40,pedestrians={'D':[(0,12)]})
        fast=run(roads,vs,horizon_s=40)
        self.assertEqual(slow.collision_violations,0)
        self.assertGreaterEqual(max(slow.admissions.values()),max(fast.admissions.values()))
    def test_curved_grade_bounds(self):
        r={'A':Road('A',45,1,15,grade=.1,curve_radius_m=12)}
        o=run(r,[Vehicle('a',('A',),0,desired_mps=15)],horizon_s=70)
        self.assertIn('a',o.finishes)
        self.assertLessEqual(max(row['a'][3] for row in o.states.values() if 'a' in row),24**.5+1e-8)
    def test_non_unit_dt_explicitly_rejected(self):
        with self.assertRaises(ValueError):run({'A':Road('A',30,1,10)},[],dt_s=.5)
    def test_multi_lane_parallel(self):
        r={'A':Road('A',30,2,10)}
        vs=[Vehicle('a',('A',),0,0),Vehicle('b',('A',),0,1)]
        o=run(r,vs,horizon_s=30)
        self.assertEqual(len(o.finishes),2)

if __name__=='__main__':unittest.main()

class LaneChangeTests(unittest.TestCase):
    def test_lane_change_when_clear(self):
        r={'A':Road('A',30,2,8)}
        v=[Vehicle('x',('A',),0,lane=0,target_lane=1)]
        o=run(r,v,horizon_s=20)
        self.assertTrue(any(e[1]=='lane_change' for e in o.events))
        self.assertEqual(o.collision_violations,0)
    def test_reverse_swap_not_accepted_simultaneously(self):
        r={'A':Road('A',30,2,8)}
        v=[Vehicle('x',('A',),0,lane=0,target_lane=1),Vehicle('y',('A',),0,lane=1,target_lane=0)]
        o=run(r,v,horizon_s=20)
        self.assertEqual(sum(e[1]=='lane_change' for e in o.events if e[0]==0),0)
    def test_lane_change_target_validation(self):
        with self.assertRaises(ValueError):run({'A':Road('A',30,1,8)},[Vehicle('x',('A',),0,target_lane=1)])
