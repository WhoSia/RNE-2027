"""T2 v2.2 physical movement and event genealogy tests."""
import unittest
from dual_lane_v11 import DualConfig,run
from spatial_v10 import Config

class PhysicalInvariantsV22(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r=run(DualConfig(base=Config(duration_s=720,demand_vph=1800,
            pocket_length_m=14.,left_fraction=.5),through_B_share=0,
            allow_lane_changes=True,receiver_mode="cells",receiver_slots=4),trace=True)

    def test_model_actually_changes_lanes(self):
        self.assertGreater(self.r["changes_A_to_B"],0)

    def test_each_car_moves_at_most_one_dimension_per_tick(self):
        prev={}
        for f in self.r["frames"]:
            now={vid:(lane,x) for lane in ("A","B") for x,vid,route in f[lane]}
            for vid,(lane,x) in now.items():
                if vid in prev:
                    oldlane,oldx=prev[vid]
                    self.assertLessEqual(int(lane!=oldlane)+abs(x-oldx),1,
                        (f["t"],vid,(oldlane,oldx),(lane,x)))
            prev=now

    def test_exact_pocket_refusals_match_counters(self):
        a=[e for e in self.r["access_events"] if e["event"]=="pocket_entry_denied"]
        self.assertEqual(len(a),self.r["pocket_block_seconds"])
        self.assertGreater(len(a),0)
        self.assertTrue(all("blocker_id" in e for e in a))

    def test_receiver_denial_attempts_vs_seconds(self):
        events=[e for e in self.r["service_events"] if e["reason"] in
                 ("receiver_entry_cell_busy","receiver_capacity_full")]
        self.assertEqual(len(events),self.r["receiver_denied_attempts"])
        self.assertEqual(len({e["t"] for e in events}),self.r["receiver_denied_seconds"])

    def test_repeatability(self):
        c=DualConfig(base=Config(duration_s=120,seed=0))
        self.assertEqual(run(c),run(c))

if __name__=="__main__":unittest.main(verbosity=2)
