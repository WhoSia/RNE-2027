import unittest
from d42_second_bin import bin_overlap
class SecondBinTest(unittest.TestCase):
 def test_exact_bin(self):
  self.assertEqual(bin_overlap([(1.2,'v','-1')],[1.])['matched_bins'],1)
 def test_adjacent_bin_no_match(self):
  self.assertEqual(bin_overlap([(1.99,'v','-1')],[2.])['matched_bins'],0)
 def test_multiple_entries(self):
  r=bin_overlap([(1.1,'a','-1'),(1.2,'b','-2')],[1.,1.]);self.assertEqual(r['matched_bins'],2)
 def test_no_double_count(self):
  r=bin_overlap([(1.1,'a','-1'),(1.2,'b','-2')],[1.]);self.assertEqual((r['matched_bins'],r['candidate_excess']),(1,1))
 def test_empty_inputs(self):
  self.assertEqual(bin_overlap([],[])['matched_bins'],0)
 def test_shift_effect(self):
  self.assertEqual(bin_overlap([(1.2,'a','-1')],[2.],1.)['matched_bins'],1)
 def test_boundary_floor(self):
  self.assertEqual(bin_overlap([(0.999,'a','-1')],[1.])['matched_bins'],0)
if __name__=='__main__':unittest.main()
