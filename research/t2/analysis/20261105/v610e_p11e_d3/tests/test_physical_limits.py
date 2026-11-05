import unittest,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from physical_limits import RoadLimits,VehicleEnvelope,audit
V=VehicleEnvelope('v',4.1,2.4,12.,18.)
class TestLimits(unittest.TestCase):
 def test_missing_limits_unknown(self):
  self.assertEqual(audit(V,RoadLimits('bridge',provenance='sign'))['status'],'UNKNOWN')
 def test_height_denied(self):
  a=audit(V,RoadLimits('bridge',max_height_m=4.,provenance='sign'))
  self.assertEqual(a['status'],'DENY');self.assertEqual(a['violated'],['height_m'])
 def test_all_explicit_pass(self):
  r=RoadLimits('bridge',4.2,2.5,12.,18.,'sign')
  self.assertEqual(audit(V,r)['status'],'PASS_DECLARED_ONLY')
 def test_mass_limit(self):
  r=RoadLimits('bridge',max_gross_mass_t=15.,provenance='sign')
  self.assertEqual(audit(V,r)['violated'],['gross_mass_t'])
 def test_width_limit(self):
  r=RoadLimits('bridge',max_width_m=2.3,provenance='sign')
  self.assertEqual(audit(V,r)['status'],'DENY')
 def test_invalid_limit(self):
  with self.assertRaises(ValueError):RoadLimits('bridge',-2,provenance='sign')
 def test_missing_evidence(self):
  with self.assertRaises(ValueError):RoadLimits('bridge',max_height_m=4.)
 def test_invalid_vehicle(self):
  with self.assertRaises(ValueError):VehicleEnvelope('bad',0,2.,2.,1.)
if __name__=='__main__':unittest.main()
