import unittest
from src.micro_network import Link,Network,Demand

class LateralTests(unittest.TestCase):
 def test_empty_adjacent_lane_change_is_logged(self):
  network=Network([Link('L',35,8),Link('R',35,8)],dt_s=.5,lateral_neighbors={'L':('R',)})
  result=network.run([Demand('car',0,('L',))],40,lane_change_requests={'car':(1,'R')})
  self.assertEqual(len(result.lane_changes),1)
  self.assertEqual(result.lane_changes[0][1:],('car','L','R'))
  self.assertIn('car',result.completed_s)
 def test_occupied_adjacent_lane_blocks_change_until_clear(self):
  network=Network([Link('L',40,6),Link('R',40,12)],dt_s=.5,lateral_neighbors={'L':('R',)})
  result=network.run([Demand('car',0,('L',),acceleration_mps2=0.5),Demand('occupied',0,('R',),acceleration_mps2=8,desired_speed_mps=12)],70,
                  lane_change_requests={'car':(0,'R')})
  self.assertEqual(len(result.lane_changes),1)
  self.assertGreater(result.lane_changes[0][0],0)
 def test_nonadjacent_raises(self):
  network=Network([Link('L',20),Link('R',20)])
  with self.assertRaises(ValueError):
   network.run([Demand('car',0,('L',))],20,lane_change_requests={'car':(0,'R')})
 def test_different_length_reference_rejected(self):
  with self.assertRaises(ValueError):
   Network([Link('L',20),Link('R',10)],lateral_neighbors={'L':('R',)})
if __name__=='__main__':unittest.main()
