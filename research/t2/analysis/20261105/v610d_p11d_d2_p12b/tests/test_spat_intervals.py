import unittest,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from spat_intervals import edges
class IntervalTests(unittest.TestCase):
 def test_bracket_not_exact(self):
  a=[{'intersection_id':'5502','tmstp_utc':'2025-03-01T00:00:08.156','signalgroup2':'G','signalgroup4':'R'},
     {'intersection_id':'5502','tmstp_utc':'2025-03-01T00:00:08.259','signalgroup2':'Y','signalgroup4':'R'}]
  e=edges(a);self.assertEqual(len(e),1);self.assertAlmostEqual(e[0]['time_uncertainty_s'],.103)
 def test_absent_signal_not_assumed_red(self):
  a=[{'intersection_id':'5502','tmstp_utc':'2025-03-01T00:00:00','signalgroup2':'G'},
     {'intersection_id':'5502','tmstp_utc':'2025-03-01T00:00:01','signalgroup2':'R','signalgroup4':'G'}]
  self.assertEqual(edges(a),[])
 def test_mixed_intersections_rejected(self):
  a=[{'intersection_id':str(i),'tmstp_utc':f'2025-03-01T00:00:0{i}','signalgroup2':'R'} for i in (1,2)]
  with self.assertRaises(ValueError):edges(a)
 def test_unordered_rejected(self):
  a=[{'intersection_id':'1','tmstp_utc':f'2025-03-01T00:00:0{i}','signalgroup2':'R'} for i in (2,1)]
  with self.assertRaises(ValueError):edges(a)
if __name__=='__main__':unittest.main()
