import unittest,sys,math
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from lane_3d_differential import derivatives_3d,lane_3d_at,convergence_diagnostic

D=math.sqrt(5)
def helix(s):return (2*math.cos(s/D),2*math.sin(s/D),s/D)
def road(elev='b="0"',roll='',k='.02',offset=''):
    return f'<OpenDRIVE><road id="r" length="25"><planView><geometry s="0" x="0" y="0" hdg="0" length="25"><arc curvature="{k}"/></geometry></planView><elevationProfile><elevation s="0" a="0" {elev} c="0" d="0"/></elevationProfile><lateralProfile>{roll}</lateralProfile><lanes>{offset}<laneSection s="0"><right><lane id="-1" type="driving"><width sOffset="0" a="4" b="0" c="0" d="0"/></lane></right></laneSection></lanes></road></OpenDRIVE>'
class Differential3D(unittest.TestCase):
    def test_helix_curvature(self):self.assertAlmostEqual(derivatives_3d(helix,3,.025)['curvature_inv_m'],2/5,delta=3e-7)
    def test_helix_torsion(self):self.assertAlmostEqual(derivatives_3d(helix,3,.025)['torsion_inv_m'],1/5,delta=3e-5)
    def test_mirrored_helix_torsion(self):self.assertAlmostEqual(derivatives_3d(lambda s:(helix(s)[0],-helix(s)[1],helix(s)[2]),3,.025)['torsion_inv_m'],-1/5,delta=3e-5)
    def test_flat_circle_torsion_zero(self):self.assertAlmostEqual(derivatives_3d(lambda s:(math.cos(s),math.sin(s),0),2,.03)['torsion_inv_m'],0,delta=1e-8)
    def test_line_torsion_undefined(self):self.assertEqual(derivatives_3d(lambda s:(s,0,0),3)['status'],'CURVATURE_ONLY')
    def test_missing_road(self):
        with self.assertRaises(ValueError):lane_3d_at(road(),'missing',-1,5)
    def test_planar_lane_curvature(self):self.assertAlmostEqual(lane_3d_at(road(),'r',-1,5)['curvature_inv_m'],.02/1.04,delta=1e-6)
    def test_banked_lane_conditional(self):
        r=lane_3d_at(road(roll='<superelevation s="0" a=".1" b=".01" c="0" d="0"/>'),'r',-1,5)
        self.assertEqual(r['status'],'SAMPLED_3D_DIFFERENTIAL_GEOMETRY_ONLY');self.assertFalse(r['field_validated'])
    def test_grade_supported(self):self.assertEqual(lane_3d_at(road(elev='b=".03"'),'r',-1,5)['status'],'SAMPLED_3D_DIFFERENTIAL_GEOMETRY_ONLY')
    def test_near_boundary_unknown(self):self.assertEqual(lane_3d_at(road(),'r',-1,.01)['reason'],'STENCIL_OUTSIDE_ROAD')
    def test_source_knot_unknown(self):
        x=road(offset='<laneOffset s="0" a="0" b="0" c="0" d="0"/><laneOffset s="6" a="0" b="0" c="0" d="0"/>')
        self.assertEqual(lane_3d_at(x,'r',-1,6.02,.025)['reason'],'FINITE_DIFFERENCE_CROSSES_SOURCE_KNOT')
    def test_stencil_on_knot_unknown(self):self.assertEqual(lane_3d_at(road(),'r',-1,0.1,.05)['reason'],'FINITE_DIFFERENCE_CROSSES_SOURCE_KNOT')
    def test_no_safety_speed(self):self.assertIsNone(lane_3d_at(road(),'r',-1,5)['safe_speed_mps'])

class Convergence(unittest.TestCase):
    def test_helix_refinement_curvature(self):
        z=convergence_diagnostic(helix,2,.05)
        self.assertFalse(z['certified_error_bound'])
        self.assertLess(z['curvature_abs_difference_inv_m'],1e-7)
    def test_helix_refinement_torsion(self):
        self.assertLess(convergence_diagnostic(helix,2,.05)['torsion_abs_difference_inv_m'],3e-5)
    def test_line_torsion_not_inferred(self):
        self.assertIsNone(convergence_diagnostic(lambda t:(t,0.,0.),2,.05)['torsion_abs_difference_inv_m'])

if __name__=='__main__':unittest.main()
