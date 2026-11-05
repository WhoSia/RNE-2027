import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from opendrive_ir import Cubic
from road_integrity import polynomial_range,audit_lane_widths,audit_explicit_junctions,full_audit


def xml(width='a="3.5" b="0" c="0" d="0"', road2_x='10', connected=False):
    link='<junction id="j"><connection id="c" incomingRoad="A" connectingRoad="B" contactPoint="start"><laneLink from="-1" to="-1"/></connection></junction>' if connected else ''
    return f'''<OpenDRIVE><header revMajor="1" revMinor="8"/>
<road id="A" length="10" junction="-1"><planView><geometry s="0" x="0" y="0" hdg="0" length="10"><line/></geometry></planView><elevationProfile><elevation s="0" a="0" b="0" c="0" d="0"/></elevationProfile><lanes><laneSection s="0"><right><lane id="-1" type="driving"><width sOffset="0" {width}/></lane></right></laneSection></lanes></road>
<road id="B" length="10" junction="j"><planView><geometry s="0" x="{road2_x}" y="0" hdg="0" length="10"><line/></geometry></planView><elevationProfile><elevation s="0" a="0" b="0" c="0" d="0"/></elevationProfile><lanes><laneSection s="0"><right><lane id="-1" type="driving"><width sOffset="0" a="3.5" b="0" c="0" d="0"/></lane></right></laneSection></lanes></road>{link}</OpenDRIVE>'''

class TestIntervalProof(unittest.TestCase):
    def test_positive_constant(self):
        self.assertEqual(polynomial_range(Cubic(0,3.5,0,0,0),0,20),(3.5,3.5))
    def test_hidden_negative_interior(self):
        # p(s) = (s-5)^2-1: positive at both endpoints, negative in middle
        z=polynomial_range(Cubic(0,24,-10,1,0),0,10)
        self.assertAlmostEqual(z[0],-1.)
    def test_cubic_stationary_point(self):
        p=Cubic(0,5,-3,0,1)
        lo,hi=polynomial_range(p,0,2)
        self.assertAlmostEqual(lo,3.)
        self.assertAlmostEqual(hi,7.)
    def test_shifted_support_stationarity(self):
        # (s-5)^2-1 minimized at s=5, even when interval starts at s=4.
        self.assertAlmostEqual(polynomial_range(Cubic(0,24,-10,1,0),4,7)[0],-1)
    def test_bad_interval(self):
        with self.assertRaises(ValueError):polynomial_range(Cubic(0,2,0,0,0),1,0)
    def test_full_width_rejects_interior_negative(self):
        f=audit_lane_widths(xml('a="24" b="-10" c="1" d="0"'))
        self.assertTrue(any(q.code=='WIDTH_NONPOSITIVE' for q in f))
    def test_full_width_accepts_constant(self):
        f=audit_lane_widths(xml())
        self.assertTrue(all(q.status=='PASS' for q in f))
    def test_width_piece_jump(self):
        s=xml().replace('/></lane>', '/><width sOffset="5" a="1" b="0" c="0" d="0"/></lane>',1)
        self.assertIn('WIDTH_KNOT_JUMP',[q.code for q in audit_lane_widths(s)])

class TestGeometryLink(unittest.TestCase):
    def test_connected_reference_not_permission(self):
        f=audit_explicit_junctions(xml(connected=True))
        self.assertEqual(f[0].status,'UNKNOWN');self.assertEqual(f[0].code,'LINK_GEOMETRY_ONLY')
    def test_disjoint_roads_are_a_failure(self):
        f=audit_explicit_junctions(xml(road2_x='30',connected=True))
        self.assertEqual(f[0].code,'ROAD_REFERENCE_GAP')
    def test_link_summary_no_vehicle_claim(self):
        x=full_audit(xml(connected=True));self.assertFalse(x['vehicle_simulated']);self.assertGreater(x['unknown_count'],0)

if __name__=='__main__':unittest.main()
