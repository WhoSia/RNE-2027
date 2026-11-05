import unittest,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from field_friction_evidence import validate
T={'source':'LTPP_MON_FRICTION','source_record_id':'synthetic-001','metric':'LTPP_SKID_NUMBER','value':35.,'unit':'dimensionless_skid_number','station_or_section':'hypothetical-section','time_utc':None,'device':None,'test_speed_mps':None,'weather':None,'reference_url':'https://infopave.fhwa.dot.gov/Data/TableExport/'}
class T1(unittest.TestCase):
 def test_provenance_not_calibration(self):
  x=validate(T);self.assertIsNone(x['effective_vehicle_tire_mu']);self.assertEqual(len(x['missing_context']),4)
 def test_cannot_call_skid_number_mu(self):
  with self.assertRaises(ValueError):validate({**T,'unit':'device_reported_dimensionless'})
 def test_reject_unknown_metric(self):
  with self.assertRaises(ValueError):validate({**T,'metric':'TIRE_GRIP_MU'})
 def test_reject_nan(self):
  with self.assertRaises(ValueError):validate({**T,'value':float('nan')})
 def test_missing_source(self):
  with self.assertRaises(ValueError):validate({**T,'source_record_id':''})
 def test_wrong_source(self):
  with self.assertRaises(ValueError):validate({**T,'source':'OTHER'})
 def test_timestamp_utc(self):self.assertEqual(validate({**T,'time_utc':'2025-03-01T00:00:00Z'})['missing_context'],['device','test_speed_mps','weather'])
 def test_timezone_rejected(self):
  with self.assertRaises(ValueError):validate({**T,'time_utc':'2025-03-01T09:00:00+09:00'})
if __name__=='__main__':unittest.main()
