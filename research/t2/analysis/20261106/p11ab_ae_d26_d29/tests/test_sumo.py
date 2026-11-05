import unittest,tempfile
from pathlib import Path
from src.sumo_export import write_sumo_fixture
class SumoInputTest(unittest.TestCase):
 def test_export_well_formed_inputs_not_executed(self):
  with tempfile.TemporaryDirectory() as d:
   result=write_sumo_fixture(d)
   self.assertTrue(Path(d,'corridor.sumocfg').is_file())
   self.assertEqual(len(list(Path(d).glob('*.xml'))),3)
   self.assertIn('sumo',result['run_command'])
if __name__=='__main__':unittest.main()
