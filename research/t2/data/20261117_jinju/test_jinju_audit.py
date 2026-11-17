from unittest import TestCase

from jinju_audit import summarize, vector


class JinjuAuditTest(TestCase):
    def test_vector_width_and_sign(self):
        self.assertEqual(vector("1/0", 2), (1, 0))
        with self.assertRaises(ValueError):
            vector("1/0", 3)
        with self.assertRaises(ValueError):
            vector("1/-1", 2)

    def test_distinguishes_parsed_row_equivalence_from_key_collisions(self):
        row = ["2025-11-01 00:00:01", "2025-11-01 00:00:15", "site", "1",
               "2/0/0/0/4/0", "2/0/0/0/0/0/0"] + [""] * 10
        changed = row.copy()
        changed[5] = "1/0/0/0/0/0/0"
        result = summarize([row, row, changed])
        self.assertEqual(result["exact_duplicate_excess"], 1)
        self.assertEqual(result["repeated_site_time_excess"], 2)
        self.assertEqual(result["movement_class_count_differences"], 1)
        self.assertEqual(result["recorded_elapsed_seconds"], {14: 3})
