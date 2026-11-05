import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from road_ir import RoadLane,LaneConnection,RoadIR
from signal_binding import read_programs,inspect_bindings
N=RoadIR((RoadLane('a',10,10),RoadLane('b',10,10)),(LaneConnection('m','a','b','J','straight','J',0),),'synthetic')
class TestBindings(unittest.TestCase):
 def test_simple_pass(self):
  p=read_programs('<additional><tlLogic id="J" programID="x" offset="0"><phase duration="10" state="G"/><phase duration="3" state="y"/></tlLogic></additional>')
  self.assertEqual(inspect_bindings(N,p)['programs'][0]['status'],'PASS')
  self.assertEqual(p[0].cycle_s,13)
 def test_missing_state_link(self):
  p=read_programs('<additional><tlLogic id="J"><phase duration="10" state="GG"/></tlLogic></additional>')
  self.assertEqual(inspect_bindings(N,p)['programs'][0]['unbound_state_indices'],[1])
 def test_missing_program(self):
  self.assertEqual(inspect_bindings(N,())['signal_ids_without_provided_programs'],['J'])
 def test_zero_duration_rejected(self):
  with self.assertRaises(ValueError):read_programs('<additional><tlLogic id="J"><phase duration="0" state="G"/></tlLogic></additional>')
 def test_unequal_state_width(self):
  with self.assertRaises(ValueError):read_programs('<additional><tlLogic id="J"><phase duration="2" state="GG"/><phase duration="2" state="G"/></tlLogic></additional>')
 def test_unknown_signal_color(self):
  with self.assertRaises(ValueError):read_programs('<additional><tlLogic id="J"><phase duration="2" state="X"/></tlLogic></additional>')
 def test_duplicate_program(self):
  with self.assertRaises(ValueError):read_programs('<additional><tlLogic id="J"><phase duration="2" state="G"/></tlLogic><tlLogic id="J"><phase duration="3" state="r"/></tlLogic></additional>')
 def test_not_runtime_confirmed(self):
  self.assertEqual(inspect_bindings(N,())['active_program_at_runtime'],'UNKNOWN')
if __name__=='__main__':unittest.main()
