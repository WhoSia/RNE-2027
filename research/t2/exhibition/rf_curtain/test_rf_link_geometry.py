import math
import unittest
from rf_link_geometry import first_fresnel_radius_m,Link,pairwise_midpoint_gate,exhibition_geometry_audit

class GeometryContracts(unittest.TestCase):
    def test_midpoint_formula(self):
        x=first_fresnel_radius_m(2.4,1)
        self.assertAlmostEqual(x, math.sqrt(299792458/(2.4e9)/4))
        self.assertAlmostEqual(first_fresnel_radius_m(2.4,2,.5),
                               first_fresnel_radius_m(2.4,2,1.5))
    def test_longer_link_lower_frequency_broader_zone(self):
        self.assertGreater(first_fresnel_radius_m(2.4,2),first_fresnel_radius_m(2.4,1))
        self.assertGreater(first_fresnel_radius_m(2.4,1),first_fresnel_radius_m(5,1))
    def test_invalid_inputs(self):
        for f,L,d in ((0,1,None),(2.4,0,None),(-1,1,None),(2.4,1,0),
                      (2.4,1,1),(2.4,1,-.1),(2.4,1,1.1),
                      (math.inf,1,None),(2.4,math.nan,None)):
            with self.subTest(f=f,L=L,d=d),self.assertRaises(ValueError):
                first_fresnel_radius_m(f,L,d)
    def test_tabletop_midpoint_heuristic_discourages_lane_resolution(self):
        x=exhibition_geometry_audit()
        self.assertFalse(x['section_pair']['overlap_heuristic'])
        self.assertTrue(x['adjacent_scaled_lane_pair']['overlap_heuristic'])
        self.assertEqual(x['status'],'ANALYTIC_GEOMETRY_NOT_MEASURED_WIFI')
    def test_boundary_contact_is_not_promoted_to_separation_proof(self):
        a=Link('a',0,0,1)
        b=Link('b',2*a.radius_m,0,1)
        o=pairwise_midpoint_gate(a,b)
        self.assertTrue(o['boundary_contact'])
        self.assertFalse(o['overlap_heuristic'])
        self.assertIn('HEURISTIC',o['meaning'])

if __name__=='__main__': unittest.main()
