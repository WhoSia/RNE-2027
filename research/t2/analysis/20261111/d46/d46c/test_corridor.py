import unittest
from corridor import run

class FiniteStorageGate(unittest.TestCase):
 def test_zero_space_blocks(self):
  from corridor import State,advance
  x=advance(State(4,2,6),0,5,1,2)
  self.assertEqual((x.transfer,x.exit_flow,x.state.downstream),(0,1,1))
 def test_freed_space_next_tick(self):
  from corridor import State,advance
  x=advance(State(4,2,6),0,5,1,2)
  y=advance(x.state,0,5,1,2)
  self.assertEqual(y.transfer,1)
 def test_arrival_not_transferred_same_tick(self):
  from corridor import State,advance
  x=advance(State(0,0),5,5,5,5)
  self.assertEqual((x.transfer,x.state.upstream),(0,5))
 def test_transfer_not_exited_same_tick(self):
  from corridor import State,advance
  x=advance(State(5,0,5),0,5,5,5)
  self.assertEqual((x.exit_flow,x.state.downstream),(0,5))
 def test_full_sequence_conservation(self):
  seq=run([2]*30,[4]*30,[1]*30,3)
  self.assertTrue(any(x.blocked>0 for x in seq))
  for x in seq:
   self.assertAlmostEqual(x.end_conservation_error,0)
   self.assertLessEqual(x.state.downstream,3)
 def test_zero_arrivals(self):
  from corridor import State
  self.assertEqual(run([0],[2],[2],5)[0].state,State(0,0,0,0))
 def test_invalid_negative(self):
  from corridor import State,advance
  with self.assertRaises(ValueError):advance(State(0,0),-1,1,1,3)
 def test_bad_storage(self):
  from corridor import State,advance
  with self.assertRaises(ValueError):advance(State(0,5,5),0,1,1,3)
 def test_nonfinite(self):
  from corridor import State,advance
  with self.assertRaises(ValueError):advance(State(0,0),float('inf'),1,1,3)
 def test_bad_schedule(self):
  with self.assertRaises(ValueError):run([1],[1,2],[1],3)
 def test_initial_conservation(self):
  from corridor import State,advance
  with self.assertRaises(ValueError):advance(State(5,1,2),0,1,1,3)
 def test_transfer_only_if_queued(self):
  from corridor import State,advance
  self.assertEqual(advance(State(1,0,1),0,10,0,10).transfer,1)
 def test_exit_only_if_present(self):
  from corridor import State,advance
  self.assertEqual(advance(State(1,0,1),0,0,10,2).exit_flow,0)
 def test_blocked_nonnegative(self):
  from corridor import State,advance
  self.assertEqual(advance(State(5,2,7),0,0,5,2).blocked,0)
 def test_occupancy_never_negative(self):
  seq=run([3]+[0]*20,[2]*21,[10]*21,5)
  self.assertTrue(all(x.state.upstream>=0 and x.state.downstream>=0 for x in seq))
if __name__=='__main__':unittest.main()
