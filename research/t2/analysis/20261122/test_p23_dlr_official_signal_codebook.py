import os, unittest
from pathlib import Path
from p23_dlr_official_signal_codebook import CODES,category,analyze
T=Path(os.environ.get('P23_SIGNAL_CSV','/mnt/data/traffic-lights_230924-233000_230924-234500.csv'))
D=Path(os.environ.get('P23_OFFICIAL_PDF','/mnt/data/DLR-Urban-Traffic-dataset_v1-3-1_documentation.pdf'))
class Tests(unittest.TestCase):
 def test_source_27k_measurements_real_codebook(self):
  if not T.is_file() or not D.is_file():self.skipTest('Source files absent')
  d=analyze(T,D)
  self.assertEqual((d['source_rows'],d['signal_ids'],d['signal_code_changes']),(26970,30,869))
  self.assertEqual(d['by_signal_purpose']['motor_vehicle_signal'],{'3':6105,'4':86,'5':1645,'7':255})
  self.assertEqual(d['by_signal_purpose']['flashing_vru_warning'],{'1':604,'9':295})
  self.assertEqual(d['sampling_intervals_s']['gaps_over_1_5_s'],30)
  self.assertFalse(d['gates']['controlling_signal_to_movement_verified'])
 def test_traffic_code_map(self):
  self.assertEqual(CODES['5'],'green');self.assertEqual(CODES['4'],'red_and_yellow')
  self.assertEqual(CODES['9'],'yellow_flashing');self.assertEqual(CODES['6'],'green_protected_movement')
 def test_signal_groups(self):
  self.assertEqual(category(9),'motor_vehicle_signal')
  self.assertEqual(category(10),'vulnerable_road_user_signal')
  self.assertEqual(category(29),'vulnerable_road_user_signal')
  self.assertEqual(category(30),'flashing_vru_warning')
  with self.assertRaises(ValueError):category(31)
 def test_wrong_doc_rejected(self):
  if not T.is_file():self.skipTest('CSV absent')
  with self.assertRaises((ValueError,FileNotFoundError)):analyze(T,T)
 def test_wrong_signal_csv_rejected(self):
  if not D.is_file():self.skipTest('PDF absent')
  with self.assertRaises((ValueError,FileNotFoundError)):analyze(D,D)
if __name__=='__main__':unittest.main()
