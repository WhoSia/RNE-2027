"""Synthetic negative controls for d42_xosc_crosswalk.py; no sensor ground truth."""
import tempfile
import unittest
from pathlib import Path

from d42_xosc_crosswalk import accepted, crosswalk

XML = """<OpenSCENARIO><Trajectory name="123Trajectory"><Shape><Polyline>
<Vertex time="0.0"><Position><WorldPosition x="-7.023" y="28.363" h="0"/></Position></Vertex>
<Vertex time="0.05"><Position><WorldPosition x="-7.020" y="28.364" h="0"/></Position></Vertex>
</Polyline></Shape></Trajectory></OpenSCENARIO>"""
CSV = """timestamp,id,center_easting,center_northing
2023-09-24 12:00:00.016482+00:00,123,604755.977,5792823.363
2023-09-24 12:00:00.066482+00:00,123,604755.980,5792823.364
"""


class BridgeFixture(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.csv = Path(tmp.name) / "raw.csv"
        self.xosc = Path(tmp.name) / "derived.xosc"
        self.csv.write_text(CSV)
        self.xosc.write_text(XML)

    def test_exact_bridge(self):
        r = crosswalk(self.csv, self.xosc)
        self.assertTrue(accepted(r))
        self.assertEqual(r["matched_vertices"], 2)

    def test_coordinate_shift_rejected(self):
        self.xosc.write_text(XML.replace('x="-7.020"', 'x="-7.000"'))
        self.assertFalse(accepted(crosswalk(self.csv, self.xosc)))

    def test_timestamp_shift_rejected(self):
        self.xosc.write_text(XML.replace('time="0.05"', 'time="0.06"'))
        self.assertFalse(accepted(crosswalk(self.csv, self.xosc)))

    def test_missing_object_rejected(self):
        self.xosc.write_text(XML.replace("123Trajectory", "999Trajectory"))
        self.assertFalse(accepted(crosswalk(self.csv, self.xosc)))

    def test_missing_vertex_rejected(self):
        lost = '<Vertex time="0.05"><Position><WorldPosition x="-7.020" y="28.364" h="0"/></Position></Vertex>'
        self.xosc.write_text(XML.replace(lost, ""))
        self.assertFalse(accepted(crosswalk(self.csv, self.xosc)))


if __name__ == "__main__":
    unittest.main()
