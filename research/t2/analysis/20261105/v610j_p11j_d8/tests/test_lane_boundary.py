import unittest,sys,math
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from lane_boundary import lane_boundaries,audit_boundary_seams,sample_lane_strip
from opendrive_lateral import parse_lateral


def xml(*, b_x=10., b_y=0., b_z=0., b_heading=0., b_width=3.5, b_roll=0.,
        a_width=3.5, include_elev=True):
    def road(id,x,y,z,hdg,w,roll):
        elev=f'<elevationProfile><elevation s="0" a="{z}" b="0" c="0" d="0"/></elevationProfile>' if include_elev else ''
        return f'<road id="{id}" length="10" junction="-1"><planView><geometry s="0" x="{x}" y="{y}" hdg="{hdg}" length="10"><line/></geometry></planView>{elev}<lateralProfile><superelevation s="0" a="{roll}" b="0" c="0" d="0"/></lateralProfile><lanes><laneSection s="0"><right><lane id="-1" type="driving"><width sOffset="0" a="{w}" b="0" c="0" d="0"/></lane></right></laneSection></lanes></road>'
    return f'<OpenDRIVE><header revMajor="1" revMinor="8"/>{road("A",0,0,0,0,a_width,0)}{road("B",b_x,b_y,b_z,b_heading,b_width,b_roll)}<junction id="j"><connection incomingRoad="A" connectingRoad="B" contactPoint="start"><laneLink from="-1" to="-1"/></connection></junction></OpenDRIVE>'

class BoundaryTest(unittest.TestCase):
    def test_right_lane_edges_and_center(self):
        s=xml();net,c=parse_lateral(s);b=lane_boundaries(net.roads[0],c['A'],0,-1)
        self.assertEqual(b.inner_xyz_m,(0,0,0))
        self.assertAlmostEqual(b.outer_xyz_m[1],-3.5)
        self.assertAlmostEqual(b.center_xyz_m[1],-1.75)
    def test_rising_roll_creates_height(self):
        s=xml(b_roll=.1);net,c=parse_lateral(s)
        b=lane_boundaries(net.roads[1],c['B'],0,-1)
        self.assertAlmostEqual(b.outer_xyz_m[2],-3.5*math.sin(.1))
    def test_matching_geometry_still_unknown(self):
        v=audit_boundary_seams(xml());self.assertEqual(v['findings'][0]['status'],'UNKNOWN')
        self.assertFalse(v['findings'][0]['legal_permission_verified'])
    def test_disconnected_declared_link_fails(self):
        v=audit_boundary_seams(xml(b_x=12));self.assertIn('BOUNDARY_GAP',v['findings'][0]['code'])
    def test_vertical_separation_not_hidden_by_xy(self):
        v=audit_boundary_seams(xml(b_z=2));self.assertIn('VERTICAL_GAP',v['findings'][0]['code'])
    def test_heading_kink(self):
        # Endpoint B starts at same reference location but has sharply different direction.
        v=audit_boundary_seams(xml(b_heading=.4));self.assertIn('HEADING_KINK',v['findings'][0]['code'])
    def test_width_mismatch(self):
        v=audit_boundary_seams(xml(b_width=2.5));self.assertIn('WIDTH_MISMATCH',v['findings'][0]['code'])
    def test_roll_changes_lane_surface(self):
        v=audit_boundary_seams(xml(b_roll=.3));self.assertIn('BOUNDARY_GAP',v['findings'][0]['code'])
    def test_source_missing_elevation_fails_closed(self):
        v=audit_boundary_seams(xml(include_elev=False));self.assertEqual(v['findings'][0]['status'],'UNKNOWN')
    def test_negative_width_blocks_strip(self):
        s=xml(a_width=-1.0)
        v=audit_boundary_seams(s);self.assertEqual(v['status'],'BLOCKED_BAD_WIDTH')
        with self.assertRaises(ValueError):sample_lane_strip(s,'A',-1)
    def test_sampled_strip_has_two_equal_length_edges(self):
        v=sample_lane_strip(xml(),'A',-1,n=11);self.assertEqual(len(v['inner_xyz_m']),11)
        self.assertEqual(len(v['outer_xyz_m']),11);self.assertFalse(v['exact_3d_surface_certified'])
    def test_reject_invalid_thresholds(self):
        with self.assertRaises(ValueError):audit_boundary_seams(xml(),edge_tol_m=-1)
    def test_reject_excessive_strip_samples(self):
        with self.assertRaises(ValueError):sample_lane_strip(xml(),'A',-1,n=100001)
    def test_separate_source_and_destination_width(self):
        a=audit_boundary_seams(xml(a_width=3.5,b_width=3.5))
        b=audit_boundary_seams(xml(a_width=3.5,b_width=3.6))
        self.assertEqual(a['findings'][0]['status'],'UNKNOWN');self.assertEqual(b['findings'][0]['status'],'UNKNOWN')

if __name__=='__main__':unittest.main()
