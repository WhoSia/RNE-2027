import sys, unittest, math
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from opendrive_ir import parse_xodr

def sample(kind='line', second=False):
    g='<line/>' if kind=='line' else '<arc curvature="0.1"/>' if kind=='arc' else '<spiral curvStart="0" curvEnd="0.1"/>'
    more='''<road id="2" length="10" junction="1"><planView><geometry s="0" x="10" y="0" hdg="0" length="10"><line/></geometry></planView><elevationProfile><elevation s="0" a="0" b="0" c="0" d="0"/></elevationProfile><lanes><laneSection s="0"><right><lane id="-1" type="driving"><width sOffset="0" a="3.5" b="0" c="0" d="0"/></lane></right></laneSection></lanes></road>''' if second else ''
    j='''<junction id="1"><connection id="1" incomingRoad="1" connectingRoad="2" contactPoint="start"><laneLink from="-1" to="-1"/></connection></junction>''' if second else ''
    return f'''<OpenDRIVE><header revMajor="1" revMinor="8"/><road id="1" length="10" junction="-1"><planView><geometry s="0" x="0" y="0" hdg="0" length="10">{g}</geometry></planView><elevationProfile><elevation s="0" a="0" b="0.1" c="0" d="0"/></elevationProfile><lanes><laneSection s="0"><right><lane id="-1" type="driving"><width sOffset="0" a="3.5" b="0" c="0" d="0"/></lane></right></laneSection></lanes></road>{more}{j}</OpenDRIVE>'''

class TestOpenDrive(unittest.TestCase):
    def test_line_elevation(self):
        r=parse_xodr(sample()).roads[0];p=r.reference_at(7)
        self.assertAlmostEqual(p['x_m'],7);self.assertAlmostEqual(p['y_m'],0);self.assertAlmostEqual(p['z_m'],.7)
    def test_arc(self):
        p=parse_xodr(sample('arc')).roads[0].reference_at(10)
        self.assertAlmostEqual(p['x_m'],math.sin(1)/.1);self.assertAlmostEqual(p['y_m'],(1-math.cos(1))/.1)
    def test_lane_width(self):
        r=parse_xodr(sample()).roads[0]
        self.assertAlmostEqual(r.lane_at(5,-1).width_at(5),3.5)
    def test_junction_explicit_not_legal(self):
        a=parse_xodr(sample(second=True));self.assertEqual(len(a.junction_links),1)
        self.assertIn('connection_orientation_not_certified',' '.join(a.unresolved))
    def test_unsupported_spiral_rejected(self):
        with self.assertRaises(ValueError):parse_xodr(sample('spiral'))
    def test_bad_reference(self):
        with self.assertRaises(ValueError):parse_xodr(sample().replace('incomingRoad="1"','incomingRoad="4"') .replace('</OpenDRIVE>','<junction id="1"><connection id="1" incomingRoad="4" connectingRoad="1" contactPoint="start"><laneLink from="-1" to="-1"/></connection></junction></OpenDRIVE>'))
    def test_gap_rejected(self):
        with self.assertRaises(ValueError):parse_xodr(sample().replace('length="10"><line/>','length="9"><line/>'))
    def test_xxe_rejected(self):
        with self.assertRaises(ValueError):parse_xodr('<!DOCTYPE OpenDRIVE [<!ENTITY x SYSTEM "file:///etc/passwd">]>'+sample())
    def test_negative_width_flagged(self):
        r=parse_xodr(sample().replace('a="3.5"','a="-3.5"')).roads[0];self.assertIsNone(r.lane_at(0,-1).width_at(0))
    def test_beyond_road(self):
        with self.assertRaises(ValueError):parse_xodr(sample()).roads[0].reference_at(11)
    def test_missing_elevation_unknown(self):
        import re
        t=re.sub(r'<elevationProfile>.*?</elevationProfile>','',sample())
        a=parse_xodr(t);self.assertIsNone(a.roads[0].reference_at(5)['z_m'])
    def test_two_road_coverage(self):self.assertEqual(parse_xodr(sample(second=True)).summary()['roads'],2)

if __name__=='__main__':unittest.main()

class TestDiscontinuousFragments(unittest.TestCase):
    def test_spatial_discontinuity(self):
        s=sample().replace('length="10"><line/>','length="5"><line/></geometry><geometry s="5" x="100" y="0" hdg="0" length="5"><line/>')
        with self.assertRaisesRegex(ValueError,'discontinuous'):parse_xodr(s)
    def test_heading_discontinuity(self):
        s=sample().replace('length="10"><line/>','length="5"><line/></geometry><geometry s="5" x="5" y="0" hdg="1" length="5"><line/>')
        with self.assertRaisesRegex(ValueError,'discontinuous'):parse_xodr(s)
    def test_continuous_segments(self):
        s=sample().replace('length="10"><line/>','length="5"><line/></geometry><geometry s="5" x="5" y="0" hdg="0" length="5"><line/>')
        self.assertAlmostEqual(parse_xodr(s).roads[0].reference_at(9)['x_m'],9.)
    def test_unsupported_does_not_create_false_connectivity(self):
        with self.assertRaises(ValueError):parse_xodr(sample('spiral'),reject_unsupported_geometry=False)
