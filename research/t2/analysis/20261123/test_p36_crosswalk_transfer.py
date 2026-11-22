import unittest

from p36_crosswalk_transfer import audit


class CrosswalkTest(unittest.TestCase):
    def setUp(self):
        self.crossing = {
            "id": "vehicle", "source_arm": "East", "road_id": "100000",
            "map_lane_id": -3, "crossing_time_utc": "estimate",
            "bracket_start_utc": "start", "bracket_end_utc": "end",
        }
        self.event = {
            "object_id": "vehicle", "source_arm": "East",
            "crossing_estimate": "estimate", "bracket_start": "start",
            "bracket_end": "end", "causal_sample_age_at_bracket_end_s": 1.0,
            "sampled_state_discordant_head_ids": [4],
        }

    def test_distinguishes_other_head_discordance(self):
        self.assertEqual(audit([self.crossing], [self.event]), {
            "group_3_candidates": 1, "prior_sample_age_le_1s": 1,
            "candidate_group_discordant": 0, "any_group_discordant": 1,
        })

    def test_left_candidate_uses_group_four(self):
        crossing = dict(self.crossing, map_lane_id=-2)
        result = audit([crossing], [self.event])
        self.assertEqual(result["group_4_candidates"], 1)
        self.assertEqual(result["candidate_group_discordant"], 1)

    def test_other_road_and_unsupported_lane_remain_unmapped(self):
        for crossing in (dict(self.crossing, road_id="179000"),
                         dict(self.crossing, map_lane_id=-5)):
            self.assertEqual(audit([crossing], [self.event]), {"unmapped": 1})

    def test_duplicate_event_and_changed_bracket_fail(self):
        for events in ([self.event, self.event],
                       [dict(self.event, bracket_end="different")]):
            with self.assertRaisesRegex(ValueError, "one to one"):
                audit([self.crossing], events)
