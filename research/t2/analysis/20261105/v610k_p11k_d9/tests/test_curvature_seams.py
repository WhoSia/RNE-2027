import unittest,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from curvature_seams import audit_curvature
X='''<OpenDRIVE><road id="r" length="20"><planView><geometry s="0" x="0" y="0" hdg="0" length="10"><line/></geometry><geometry s="10" x="10" y="0" hdg="0" length="10"><arc curvature="{curvature}"/></geometry></planView><elevationProfile><elevation s="0" a="0" b="0" c="0" d="0"/></elevationProfile></road></OpenDRIVE>'''
class TestCurvature(unittest.TestCase):
 def test_jump(self):self.assertEqual(audit_curvature(X.format(curvature=.01))['findings'][0]['status'],'G2_CURVATURE_JUMP')
 def test_smooth(self):self.assertEqual(audit_curvature(X.format(curvature=0))['findings'][0]['status'],'G2_CURVATURE_CONTINUOUS')
 def test_no_cert(self):self.assertFalse(audit_curvature(X.format(curvature=0))['traffic_safety_certified'])
 def test_tolerance(self):self.assertEqual(audit_curvature(X.format(curvature=.01),tolerance_inv_m=.02)['findings'][0]['status'],'G2_CURVATURE_CONTINUOUS')
if __name__=='__main__':unittest.main()
