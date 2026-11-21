import unittest
import os
from pathlib import Path
from unittest.mock import patch
from p24_dlr_official_signal_codebook import parse_pdf,parse_pdf_text,describe,check
BASE=Path(os.environ.get('P24_SOURCE_DIR','/mnt/data'))
PDF=BASE/'DLR-Urban-Traffic-dataset_v1-3-1_documentation.pdf'
CSV=BASE/'traffic-lights_230924-233000_230924-234500.csv'
class CodebookTests(unittest.TestCase):
 def test_official_pdf_state_codebook(self):
  if not PDF.exists():self.skipTest('source PDF absent')
  records,states=parse_pdf(PDF)
  self.assertEqual(len(records),35)
  self.assertEqual(len(set(x['id'] for x in records)),26)
  self.assertEqual(states[3],'Red light, stop and wait.')
  self.assertEqual(states[5],'Green light.')
  self.assertEqual(states[7],'Yellow light.')
  self.assertEqual(states[9],'Yellow light flashing.')
 def test_exact_real_signal_counts(self):
  if not PDF.exists() or not CSV.exists():self.skipTest('real sources absent')
  x=describe(PDF,CSV)
  self.assertEqual(x['live_signal_ids'],30)
  self.assertEqual(x['live_ids_missing_coordinates'],[10,11,12,13])
  self.assertEqual(x['live_signal_state_readings'],26970)
  self.assertEqual(x['observed_changes_across_live_ids'],869)
  self.assertEqual(x['observed_code_readings'],{'1':604,'3':20924,'4':128,'5':4680,'7':339,'9':295})
 def test_missing_coordinates_are_not_imputed(self):
  if not PDF.exists() or not CSV.exists():self.skipTest('missing raw sources')
  x=describe(PDF,CSV)
  self.assertNotIn(10,{i['id'] for i in x['coordinates']})
  self.assertEqual(x['official_signal_ids_with_coordinates'],26)
 def test_wrong_pdf_sha_refused(self):
  if not PDF.exists():self.skipTest('missing PDF')
  with patch('p24_dlr_official_signal_codebook.SHA',{'official_pdf':'0'*64}):
   with self.assertRaises(ValueError):check(PDF,'official_pdf')
 def test_wrong_version_rejected(self):
  with self.assertRaises(ValueError):parse_pdf_text('Version 1.2.0 Table 3: Traffic light coordinates Table 4: Traffic light states')
 def test_incomplete_pdf_rejected(self):
  with self.assertRaises(ValueError):parse_pdf_text('Version 1.3.1 Table 3: Traffic light coordinates 4.2.3. Table 4: Traffic light states 4.3.')
 def test_coordinate_names_not_assumed_to_be_lane_mapping(self):
  if not PDF.exists() or not CSV.exists():self.skipTest('missing raw')
  x=describe(PDF,CSV)
  self.assertTrue(any('exact controlled lane/turn' in z for z in x['limitations']))
if __name__=='__main__':unittest.main()
