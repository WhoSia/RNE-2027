from unittest import TestCase

from dlr_paired_leaders import compare


class PairedLeaders(TestCase):
    def test_same_onset_cancels_in_lane_difference(self):
        rows = [{"interval":1,"lane":lane,"rank":1,"movement":"through",
                 "crossing_s_bounds":times} for lane,times in
                ((-3,[3,4]),(-4,[4,5]))]
        pair = compare([{"block":"1230","rows":rows}])["pairs"][0]
        self.assertEqual(pair["lane_minus3_minus_minus4_s"],-1)
        self.assertEqual(pair["mean_leader_time_bounds_s"],[3.5,4.5])

    def test_incompatible_onset_is_rejected(self):
        rows = [{"interval":1,"lane":lane,"rank":1,"movement":"through",
                 "crossing_s_bounds":times} for lane,times in
                ((-3,[3,5]),(-4,[4,5]))]
        with self.assertRaisesRegex(ValueError,"same onset"):
            compare([{"block":"1230","rows":rows}])
