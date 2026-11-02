import unittest
from idm_reference import Driver,idm_acceleration,integrate_speed,storage_capacity,receiving_supply
class Tests(unittest.TestCase):
 def test_free_accel(self):self.assertGreater(idm_acceleration(0,100,0,Driver()),0)
 def test_close_following(self):self.assertLess(idm_acceleration(13,2,0,Driver()),0)
 def test_safety_zero_speed(self):self.assertEqual(integrate_speed(1,-100,0.5),0)
 def test_capacity(self):self.assertEqual(storage_capacity(70,4.5,2.5),10)
 def test_supply(self):self.assertEqual(receiving_supply(10,7),3)
 def test_bad_capacity(self):
  with self.assertRaises(ValueError):receiving_supply(2,3)
 def test_bad_params(self):
  with self.assertRaises(ValueError):Driver(time_headway_s=-1)
 def test_invalid_state(self):
  with self.assertRaises(ValueError):idm_acceleration(1,-1,0,Driver())
if __name__=='__main__':unittest.main()
