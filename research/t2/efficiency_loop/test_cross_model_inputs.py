"""Guard a few distinct endpoint and geometry regressions."""
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase

from dlr_path_cases import vehicle_cells
from dlr_path_screen import raster
from sumo_phase_pair import crossing_times, outcome, phases, point_departures, prepare, validate_network


class ComparisonContract(TestCase):
    def test_compiled_timeline_accepts_coalesced_red_and_rejects_shift(self):
        with TemporaryDirectory() as d:
            network = Path(d) / "model.net.xml"
            for left_first in (False, True):
                expected = phases(left_first)
                coalesced = expected[:-2] + ((16, "rr"),)
                phases_xml = "".join(f'<phase duration="{duration}" state="{state}"/>'
                                     for duration, state in coalesced)
                xml = ('<net><connection from="A" to="T" fromLane="0" tl="j" linkIndex="0"/>'
                       '<connection from="A" to="L" fromLane="1" tl="j" linkIndex="1"/>'
                       '<tlLogic id="j" programID="0" type="static" offset="{}">'
                       + phases_xml + '</tlLogic></net>')
                network.write_text(xml.format(0))
                validate_network(network, left_first)
                network.write_text(xml.format(1))
                with self.assertRaisesRegex(ValueError, "phase program"):
                    validate_network(network, left_first)
                network.write_text(xml.format(0).replace('duration="16"', 'duration="15"'))
                with self.assertRaisesRegex(ValueError, "phase program"):
                    validate_network(network, left_first)

    def test_yellow_and_tau_change_independent_input_files(self):
        with TemporaryDirectory() as d:
            base, red, gap = (Path(d) / name for name in ("base", "red", "gap"))
            prepare(base, False)
            prepare(red, False, yellow=False)
            prepare(gap, False, tau=1.5)
            for folder, expected in ((red, {"signal.tll.xml"}), (gap, {"demand.rou.xml"})):
                changed = {p.name for p in base.iterdir() if p.read_bytes() != (folder/p.name).read_bytes()}
                self.assertEqual(changed, expected)
        for left_first in (False, True):
            a, b = phases(left_first), phases(left_first, yellow=False)
            self.assertEqual(b, tuple((duration, state.replace("y", "r")) for duration, state in a))

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
