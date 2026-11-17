"""Guard a few distinct endpoint and geometry regressions."""
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase

from dlr_path_cases import vehicle_cells
from dlr_path_screen import raster
from sumo_phase_pair import crossing_times, outcome, phases, point_departures, prepare


class ComparisonContract(TestCase):
    def test_only_signal_program_changes_between_plans(self):
        with TemporaryDirectory() as d:
            a, b = Path(d)/"a", Path(d)/"b"
            prepare(a, False)
            prepare(b, True)
            changes = {p.name for p in a.iterdir() if p.read_bytes() != (b/p.name).read_bytes()}
            self.assertEqual(changes, {"signal.tll.xml"})
        for leading in (False, True):
            self.assertEqual(sum(t for t,_ in phases(leading)), 60)
            self.assertEqual(outcome(point_departures(leading))["crossed"], 24)

    def test_detector_requires_an_adjacent_incoming_observation(self):
        with TemporaryDirectory() as d:
            fcd = Path(d)/"fcd.xml"
            template = '<fcd-export><timestep time="10"><vehicle id="v00" lane="A_0"/></timestep>'
            template += '<timestep time="{}"><vehicle id="v00" lane="T_0"/></timestep></fcd-export>'
            fcd.write_text(template.format(10.25))
            self.assertEqual(crossing_times(fcd, .25), {"v00": 10.25})
            fcd.write_text(template.format(10.50))
            with self.assertRaises(ValueError):
                crossing_times(fcd, .25)

    def test_footprint_handles_center_outside_and_degrees(self):
        cells = [(0.25, 1.5), (1.5, 0.25)]
        self.assertEqual(list(vehicle_cells(0, 0, 90, 4, 1, cells)), [(0.25, 1.5)])
        self.assertEqual(len(raster([(0,0), (2,0), (2,1), (0,1)], .25)), 32)
