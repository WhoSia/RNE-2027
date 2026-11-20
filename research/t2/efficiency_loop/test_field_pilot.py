import csv
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase

from field_pilot import CYCLE_FIELDS, GAP_FIELDS, audit, compare, template


def write(path, fields, rows):
    with path.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(fields)
        writer.writerows(rows)


class FieldPilotTests(TestCase):
    def setUp(self):
        directory = TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)
        self.a = self.root / "a"
        template(self.a)
        self.cycles = [[i + 1, i * 1000, (i + 1) * 1000, i * 1000 + 400,
                        "visible", "visible", "visible", "visible", ""] for i in range(8)]

    def fill(self, windows=(), folder=None):
        folder = folder or self.a
        write(folder / "cycles.csv", CYCLE_FIELDS, self.cycles)
        write(folder / "gaps.csv", GAP_FIELDS, windows)
        return audit(folder)

    def test_unknown_gaps_keep_partial_windows_without_fabricating_durations(self):
        self.cycles[0][6:] = ["unknown", "visible", "옆 차로 가림"]
        first, second, *rest = self.fill([(1, 100, 200, "unknown", "", "space", "frame 3")])["cycles"]
        self.assertEqual(first["gap_status"], "unknown")
        self.assertIsNone(first["gap_total_ms"])
        self.assertEqual(first["windows"][0]["start_offset_ms"], 100)
        self.assertEqual((second["gap_status"], second["gap_total_ms"]), ("none_observed", 0))
        self.assertEqual(len(rest), 6)

    def test_records_later_cycle_crossing_and_offsets(self):
        result = self.fill([(3, 2600, 2800, 2720, 3120, "blocked", "frame 81")])
        cycle = result["cycles"][2]
        self.assertEqual(cycle["gap_total_ms"], 200)
        self.assertEqual(cycle["windows"][0]["cross_ms"], 3120)
        self.assertEqual(cycle["windows"][0]["start_offset_ms"], 600)

    def test_rejects_skipped_cycles_and_out_of_window_moves(self):
        self.cycles[1][1] = 1001
        with self.assertRaisesRegex(ValueError, "consecutive"):
            self.fill()
        self.cycles[1][1] = 1000
        with self.assertRaisesRegex(ValueError, "inside its gap"):
            self.fill([(1, 100, 200, 200, "", "space", "frame 3")])

    def test_rejects_overlaps_and_unanchored_green_end(self):
        with self.assertRaisesRegex(ValueError, "overlap"):
            self.fill([(1, 100, 200, "no", "", "space", "frame 3"),
                       (1, 180, 250, "no", "", "space", "frame 6")])
        self.cycles[0][3] = ""
        with self.assertRaisesRegex(ValueError, "requires a green end"):
            self.fill()

    def test_does_not_pool_visibility_or_match_misaligned_cycles(self):
        a = self.fill()
        b_folder = self.root / "b"
        template(b_folder)
        self.cycles[0][7:] = ["unknown", "차가 하류 입구를 가림"]
        b = self.fill(folder=b_folder)
        self.assertEqual(compare(a, b)["joint_full_visibility_cycles"], list(range(2, 9)))
        self.cycles[0][1] = 20
        with self.assertRaisesRegex(ValueError, "boundaries differ"):
            compare(a, self.fill(folder=b_folder))
