"""P30 tests: rejects trace tampering and confirms ID-based unique-denial result."""
import copy,json,os,unittest
from pathlib import Path
from dual_lane_v11 import run
from p25_p26_physical_followups import worlds,action
from p30_unique_vehicle_event_audit import analyse,audit_trace

REF=Path(os.environ.get("P30_REFERENCE","/mnt/data/p30_work/results/p25_p26_results.json"))
class P30Tests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
    cls.reference=json.loads(REF.read_text(encoding="utf8"))
    cls.output=analyse(cls.reference)
 def test_full_cohort_reproduces_prior_scores(self):
    self.assertEqual(self.output["worlds"],64)
    self.assertEqual(self.output["unique_full_arrival_tapes"],4)
    self.assertEqual(self.output["same_score_worlds"],64)
 def test_denials_not_one_to_one_unique_cars(self):
    h=self.output["difference_histogram_10_minus_6"]
    self.assertEqual(h["attempts"],{"4":64})
    self.assertEqual(h["distinct_rejected_vehicles"],{"0":30,"1":34})
    self.assertEqual(h["repeat_attempts"],{"3":34,"4":30})
 def test_equal_counts_do_not_imply_id_equal(self):
    h=self.output["difference_histogram_10_minus_6"]
    self.assertEqual(h["observed_crossing_count"],{"0":64})
    self.assertEqual(h["score"],{"0":64})
    self.assertEqual(h["remaining"],{"0":64})
 def test_censoring_not_imputed_as_completed(self):
    h=self.output["difference_histogram_10_minus_6"]
    self.assertEqual(h["rejected_censored_at_240"],{"0":64})
    self.assertEqual(h["rejected_then_crossed"],{"0":30,"1":34})
 def test_trace_rejects_invalid_vehicle_id(self):
    _,cfg,tape=next(worlds());r=run(cfg,tape,trace=True)
    broken=copy.deepcopy(r)
    broken["service_events"][0]["vehicle_id"]=len(tape)
    with self.assertRaises(AssertionError):audit_trace(broken,tape)
 def test_trace_rejects_duplicate_crossing(self):
    _,cfg,tape=next(worlds());r=run(cfg,tape,trace=True)
    broken=copy.deepcopy(r)
    e=next(e for e in r["service_events"] if e["reason"]=="stopline_cross")
    broken["service_events"].append(dict(e))
    with self.assertRaises(AssertionError):audit_trace(broken,tape)
 def test_trace_rejects_missing_denial(self):
    _,cfg,tape=next(worlds());r=run(cfg,tape,trace=True)
    broken=copy.deepcopy(r)
    broken["service_events"]=[e for i,e in enumerate(r["service_events"])
          if i!=next(j for j,z in enumerate(r["service_events"]) if z["reason"]!="stopline_cross")]
    with self.assertRaises(AssertionError):audit_trace(broken,tape)
 def test_trace_rejects_route_mutation(self):
    _,cfg,tape=next(worlds());r=run(cfg,tape,trace=True)
    broken=copy.deepcopy(r)
    broken["service_events"][0]["movement"]="S" if broken["service_events"][0]["movement"]=="L" else "L"
    with self.assertRaises(AssertionError):audit_trace(broken,tape)
 def test_deterministic_result(self):
    self.assertEqual(self.output,analyse(self.reference))

if __name__=="__main__":unittest.main()
