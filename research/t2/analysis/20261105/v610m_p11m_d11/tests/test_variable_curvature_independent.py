"""Independent sampled-XY finite-difference witness, not reused symbolic formula."""
import unittest,sys,math
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from variable_lane_curvature import lane_curvature_variable
from test_variable_lane_curvature import xml
from opendrive_lateral import parse_lateral

class IndependentXY(unittest.TestCase):
 def _numeric(self,x,s,h=.002):
  n,c=parse_lateral(x);r=n.roads[0];cs=c['a'];
  def at(q):
   p=r.reference_at(q); t=cs.offset(q)-2. # fixed right-lane width 4m
   return p['x_m']-t*math.sin(p['hdg_rad']),p['y_m']+t*math.cos(p['hdg_rad'])
  l=at(s-h);m=at(s);u=at(s+h)
  dx=(u[0]-l[0])/(2*h);dy=(u[1]-l[1])/(2*h)
  dxx=(u[0]-2*m[0]+l[0])/(h*h);dyy=(u[1]-2*m[1]+l[1])/(h*h)
  return (dx*dyy-dy*dxx)/math.hypot(dx,dy)**3
 def test_circle_variable_cubic(self):
  x=xml(offset='<laneOffset s="0" a="0.2" b=".03" c=".001" d="-.00002"/>')
  self.assertAlmostEqual(lane_curvature_variable(x,'a',-1,9)['k_lane_inv_m'],self._numeric(x,9),delta=2e-7)
 def test_spiral_variable(self):
  x=xml(kind='<spiral curvStart=".01" curvEnd=".07"/>',offset='<laneOffset s="0" a="0.2" b=".02" c=".002" d="0"/>')
  self.assertAlmostEqual(lane_curvature_variable(x,'a',-1,8)['k_lane_inv_m'],self._numeric(x,8),delta=2e-7)
 def test_line_variable_quad(self):
  x=xml(kind='<line/>',offset='<laneOffset s="0" a="0" b="0" c=".01" d="0"/>')
  self.assertAlmostEqual(lane_curvature_variable(x,'a',-1,7)['k_lane_inv_m'],self._numeric(x,7),delta=2e-7)
if __name__=='__main__':unittest.main()
