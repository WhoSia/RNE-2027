import math,sys,unittest
from pathlib import Path
from scipy.special import fresnel
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from opendrive_ir import parse_xodr
from opendrive_lateral import parse_lateral

R='''<OpenDRIVE><header revMajor="1" revMinor="8"/><road id="1" length="20" junction="-1"><planView><geometry s="0" x="0" y="0" hdg="0" length="20"><spiral curvStart="0" curvEnd="0.1"/></geometry></planView><elevationProfile><elevation s="0" a="3" b="0" c="0" d="0"/></elevationProfile><lateralProfile><superelevation s="0" a="0.1" b="0" c="0" d="0"/></lateralProfile><lanes><laneOffset s="0" a="0.5" b="0" c="0" d="0"/><laneSection s="0"><left><lane id="1" type="driving"><width sOffset="0" a="3.5" b="0" c="0" d="0"/></lane></left><right><lane id="-1" type="driving"><width sOffset="0" a="3" b="0" c="0" d="0"/></lane></right></laneSection></lanes></road></OpenDRIVE>'''

class TestSpiralAndLateral(unittest.TestCase):
 def test_spiral_fresnel_independent(self):
  p=parse_xodr(R).roads[0].reference_at(20)
  slope=.1/20
  u=20*math.sqrt(slope/math.pi)
  S,C=fresnel(u)
  f=math.sqrt(math.pi/slope)
  self.assertAlmostEqual(p['x_m'],f*C,places=5)
  self.assertAlmostEqual(p['y_m'],f*S,places=5)
  self.assertAlmostEqual(p['hdg_rad'],1.,places=10)
 def test_roll_and_offset(self):
  net,sec=parse_lateral(R); road=net.roads[0]
  p=sec['1'].lane_center(road,0,-1)
  self.assertEqual(p['status'],'COMPUTED_CONDITIONAL')
  self.assertAlmostEqual(p['t_m'],-1.,places=7)
  self.assertAlmostEqual(p['y_m'],-math.cos(.1),places=7)
  self.assertAlmostEqual(p['z_m'],3-math.sin(.1),places=7)
 def test_left_lane(self):
  net,sec=parse_lateral(R)
  self.assertAlmostEqual(sec['1'].lane_center(net.roads[0],0,1)['t_m'],2.25)
 def test_no_elevation(self):
  x=R.replace('<elevationProfile><elevation s="0" a="3" b="0" c="0" d="0"/></elevationProfile>','')
  net,sec=parse_lateral(x)
  self.assertEqual(sec['1'].lane_center(net.roads[0],0,1)['status'],'UNKNOWN_GEOMETRY')
 def test_negative_width_unknown(self):
  x=R.replace('a="3.5"','a="-3.5"')
  net,sec=parse_lateral(x)
  self.assertEqual(sec['1'].lane_center(net.roads[0],0,1)['status'],'UNKNOWN_GEOMETRY')
 def test_reject_unsupported_levelled_lane(self):
  x=R.replace('id="1" type="driving"','id="1" type="driving" level="true"')
  with self.assertRaises(ValueError):parse_lateral(x)
 def test_invalid_superelevation_rejected(self):
  x=R.replace('superelevation s="0"','superelevation s="-1"')
  with self.assertRaises(ValueError):parse_lateral(x)
 def test_zero_spiral_equivalent_straight(self):
  x=R.replace('curvEnd="0.1"','curvEnd="0"')
  p=parse_xodr(x).roads[0].reference_at(20)
  self.assertAlmostEqual(p['x_m'],20,places=7);self.assertAlmostEqual(p['y_m'],0,places=7)
 def test_policy_contract_nonexecuting(self):
  sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'policy_idea'))
  from variable_contract import FutureDecisionVariables
  self.assertFalse(FutureDecisionVariables().report()['simulation_or_controller_run'])
if __name__=='__main__':unittest.main()
