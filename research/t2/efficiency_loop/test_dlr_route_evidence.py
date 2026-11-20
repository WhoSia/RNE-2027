from unittest import TestCase

from dlr_route_evidence import bracket_code, has_sequence, movement_report


class RouteEvidenceTests(TestCase):
    def test_raw_code_requires_one_pair_covering_both_vehicle_samples(self):
        clock = ((0, 1, 2, 3, 5), (5, 5, 3, 3, 3))
        self.assertEqual(bracket_code(clock, .1, .2), "5")
        self.assertEqual(bracket_code(clock, .9, 1.1), "missing_or_transition")
        self.assertEqual(bracket_code(clock, 1.1, 1.2), "missing_or_transition")
        self.assertEqual(bracket_code(clock, 2.1, 2.2), "3")
        self.assertEqual(bracket_code(clock, 3.1, 3.2), "missing_or_transition")
        self.assertEqual(bracket_code(clock, -.1, .2), "missing_or_transition")
        self.assertEqual(bracket_code(clock, 5.1, 5.2), "missing_or_transition")

    def test_sequence_cannot_share_a_sample_or_run_backwards(self):
        hits = {"entry": (1, 3), "middle": (1, 2), "exit": (4,)}
        self.assertTrue(has_sequence(hits, ("entry", "middle", "exit"), 0, 4))
        self.assertFalse(has_sequence(hits, ("entry", "middle", "exit"), 1, 4))
        self.assertFalse(has_sequence(hits, ("entry", "middle", "exit"), 0, 3))
        self.assertFalse(has_sequence(hits, ("middle", "entry", "exit"), 0, 2))

    def test_nonconfirmed_track_stays_in_signal_denominator(self):
        gate = {
            "matched": [(.1, -1, -4), (.15, 1, -4)],
            "lost": [(.2, -1, -4), (.25, 1, -4)],
        }
        hits = {"matched": {"entry": (.16,), "west": (.2,)}}
        clocks = {3: ((0, 1), (5, 5)), 4: ((0, 1), (3, 3))}
        result = movement_report(gate, hits, ((-6, -3),), 0, clocks, 3, ("entry",), "west")
        self.assertEqual(result["counts"]["lane_gate_candidates"], 2)
        self.assertEqual(result["counts"]["ordered_connector_and_receiver"], 1)
        self.assertEqual(result["mapped_group_codes"], {"5": 2})
        self.assertEqual(result["exit_confirmed_mapped_codes"], {"5": 1})
