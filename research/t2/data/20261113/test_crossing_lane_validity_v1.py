"""Regression checks for GitHub standalone mirror; run python -m unittest -v."""
import unittest,xml.etree.ElementTree as ET
import crossing_lane_validity_v1 as gate

class LaneGateTests(unittest.TestCase):
    def test_polynomial_anchor(self):
        p=ET.fromstring('<width a="3" b="1" c="0" d="0"/>')
        self.assertEqual(gate.poly(p,2),5)
    def test_line_reference(self):
        r=ET.fromstring('<road><planView><geometry s="0" length="5" x="1" y="2" hdg="0"><line/></geometry></planView></road>')
        self.assertEqual(gate.reference_xy(r,3),(4,2))
    def test_right_lane_interval(self):
        r=ET.fromstring('<road><lanes><laneSection s="0"><right><lane id="-1" type="driving"><width sOffset="0" a="3.2" b="0" c="0" d="0"/></lane></right></laneSection></lanes></road>')
        a=gate.lane_ranges(r,5)
        self.assertAlmostEqual(a[-1][0],-3.2)
        self.assertAlmostEqual(a[-1][1],0)
    def test_invalid_geometry_rejected(self):
        r=ET.fromstring('<road><planView><geometry s="0" length="5" x="0" y="0" hdg="0"><spiral/></geometry></planView></road>')
        with self.assertRaises(ValueError):gate.reference_xy(r,2)

if __name__=="__main__":unittest.main()
