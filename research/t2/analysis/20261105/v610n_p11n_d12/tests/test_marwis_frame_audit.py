import unittest,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from marwis_frame_audit import audit_csv_text
HEADER='timestamp_sec,marwis_friction,marwis_road_condition,marwis_surface_temp_c,marwis_water_film_height\n'
class T(unittest.TestCase):
 def test_repeated_frames_not_independent(self):
  z=audit_csv_text(HEADER+'1,.3,snow,-3,1\n2,.3,snow,-3,1\n3,.3,snow,-3,1\n4,.2,ice,-3,1\n','test-origin')
  self.assertEqual((z['frame_rows'],z['consecutive_sensor_constant_blocks'],z['between_row_sensor_value_changes']),(4,2,1))
  self.assertIsNone(z['effective_independent_measurement_count'])
 def test_missing_sensor_not_zero(self):
  z=audit_csv_text(HEADER+'1,,snow,-3,1\n2,.2,ice,-3,1\n','test-origin')
  self.assertEqual(z['instrument_value_rows'],1)
 def test_clock_backward_rejected(self):
  with self.assertRaises(ValueError):audit_csv_text(HEADER+'2,.2,snow,-3,1\n1,.3,ice,-3,1\n','r')
 def test_missing_source_rejected(self):
  with self.assertRaises(ValueError):audit_csv_text(HEADER+'1,.2,snow,-3,1\n','')
 def test_bad_nan_rejected(self):
  with self.assertRaises(ValueError):audit_csv_text(HEADER+'1,nan,snow,-3,1\n','r')
 def test_empty_rejected(self):
  with self.assertRaises(ValueError):audit_csv_text(HEADER,'r')
 def test_missing_schema_rejected(self):
  with self.assertRaises(ValueError):audit_csv_text('time,mu\n1,.2\n','r')
if __name__=='__main__':unittest.main()
