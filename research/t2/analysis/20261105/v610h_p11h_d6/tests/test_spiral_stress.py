"""Independent numerical quadrature test. SciPy is a test dependency, not runtime."""
import math,sys,unittest
from pathlib import Path
from scipy.integrate import quad
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from opendrive_ir import Geometry,_simpson_clothoid

class TestSpiralStress(unittest.TestCase):
 def test_80_cases_against_independent_adaptive_quadrature(self):
  worst=0.
  for k0 in (-.2,-.02,0.,.05,.2):
   for k1 in (-.2,0.,.01,.2):
    for length in (5.,20.,50.,100.):
     g=Geometry(0.,0.,0.,0.,length,'spiral',k0,k1)
     x,y,heading=_simpson_clothoid(g,length)
     slope=(k1-k0)/length
     xr=quad(lambda s:math.cos(k0*s+.5*slope*s*s),0,length,epsabs=1e-11)[0]
     yr=quad(lambda s:math.sin(k0*s+.5*slope*s*s),0,length,epsabs=1e-11)[0]
     worst=max(worst,abs(x-xr),abs(y-yr))
     self.assertAlmostEqual(heading,length*(k0+k1)/2,places=12)
  self.assertLess(worst,1e-6)
 def test_negative_curvature(self):
  g=Geometry(0.,0.,0.,0.,40.,'spiral',0.,-.1)
  x,y,_=_simpson_clothoid(g,40)
  self.assertLess(y,0)
 def test_missing_final_curvature(self):
  with self.assertRaises(ValueError):Geometry(0.,0.,0.,0.,10.,'spiral',0.,None)
if __name__=='__main__':unittest.main()
