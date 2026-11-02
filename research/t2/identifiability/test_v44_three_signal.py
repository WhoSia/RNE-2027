import unittest
from v44_three_signal import World,simulate,optimum
class Tests(unittest.TestCase):
 def test_conservation(self):
  for g in range(6):
   r=simulate(World(2,2,1,3,2),g,50)
   self.assertEqual(r['generated'],r['completed']+r['remaining'])
 def test_three_active_signals(self):
  self.assertEqual(simulate(World(arrivals_main=0,arrivals_side=1),0,50)['completed'],150)
 def test_no_negative(self):
  for g in range(6):self.assertGreaterEqual(simulate(World(),g)['remaining'],0)
 def test_storage(self):
  for capacity in (1,2,4):simulate(World(storage=capacity,arrivals_main=4),2,100)
 def test_deterministic(self):self.assertEqual(simulate(World(),3),simulate(World(),3))
 def test_ambiguity(self):
  a,b=World(2,2,1,2,0),World(2,2,1,2,2)
  self.assertEqual(simulate(a,5,50)['completed'],simulate(b,5,50)['completed'])
  self.assertFalse(set(optimum(a)[0]) & set(optimum(b)[0]))
 def test_bad_split(self):
  with self.assertRaises(ValueError):simulate(World(),6)
if __name__=='__main__':unittest.main()
