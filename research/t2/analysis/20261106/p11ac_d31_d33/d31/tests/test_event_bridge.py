import unittest,sys,json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from event_bridge import Event,from_micro,validate_event_clock,capacity_witness
from micro_world import Road,Vehicle,run

P10=Path(__file__).resolve().parents[1]/'references/p10_replay.json'
class EventBridgeTests(unittest.TestCase):
 def test_micro_event_schema(self):
  o=run({'A':Road('A',30,1,10)},[Vehicle('x',('A',),0)],horizon_s=30)
  events=from_micro(o)
  self.assertTrue(any(e.action=='finish' for e in events))
  self.assertGreaterEqual(len(events),2)
 def test_forged_backwards_trace_rejected(self):
  with self.assertRaises(ValueError):validate_event_clock([Event(3,'1','enter','A'),Event(2,'2','exit','A')])
 def test_p10_original_witness(self):
  src=json.loads(P10.read_text())
  trace={'source_case':src['case'],'mechanism':src['mechanism'],'runs':src['grid']}
  out={x['dt_s']:x for x in capacity_witness(trace)}
  self.assertEqual(out[0.5]['retroactive_seconds'],0.5)
  self.assertEqual(out[0.25]['retroactive_seconds'],0.)
  self.assertGreater(out[0.05]['retroactive_seconds'],0.)
 def test_independent_cases_not_generalized(self):
  src=json.loads(P10.read_text());src['case']['vehicle_8']=9
  with self.assertRaises(ValueError):capacity_witness({'source_case':src['case'],'mechanism':src['mechanism'],'runs':src['grid']})

if __name__=='__main__':unittest.main()
