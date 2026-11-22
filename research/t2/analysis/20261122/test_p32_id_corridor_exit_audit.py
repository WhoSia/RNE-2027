"""P32 tests: every output record, hostile frame tamper and frozen P30/P31 parity."""
import copy,json,os,unittest
from pathlib import Path
from collections import Counter
from p32_id_corridor_exit_audit import analyse,corridor_ledger,comparison
from p25_p26_physical_followups import worlds,action
from dual_lane_v11 import run

WORK=Path(os.environ.get("P32_INPUT_ROOT","/mnt/data/p30_work/results"))


class CorridorIDTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
    cls.p30=json.loads((WORK/"p30_results.json").read_text())
    cls.p31=json.loads((WORK/"p31_results.json").read_text())
    cls.new=analyse(cls.p30,cls.p31)
    _,cls.cfg,cls.tape=next(worlds())
    cp=run(cls.cfg,cls.tape,checkpoint_at=84,trace=True)
    cls.a=run(cls.cfg,cls.tape,resume_from=cp,trace=True,phase_overrides=action(6))
    cls.b=run(cls.cfg,cls.tape,resume_from=cp,trace=True,phase_overrides=action(10))

 def test_all_historic_worlds_recovered(self):
    self.assertEqual(self.new["worlds"],192)
    self.assertEqual(self.new["unique_arrival_tapes"],12)
    self.assertEqual([z["worlds"] for z in self.new["by_cohort"]],[64,128])

 def test_explicit_falsification_of_aggregate_equivalence(self):
    a,b=self.new["by_cohort"]
    self.assertEqual((a["score_equal_but_crossing_or_exit_history_changed"],
                      b["score_equal_but_crossing_or_exit_history_changed"]),(16,32))
    self.assertEqual((a["aggregate_exact_but_individual_history_changed"],
                      b["aggregate_exact_but_individual_history_changed"]),(16,31))
    self.assertEqual((a["identical_full_vehicle_event_histories"],
                      b["identical_full_vehicle_event_histories"]),(48,87))

 def test_prior_bad_baseline_score_field_detected_in_all_rows(self):
    self.assertEqual(self.new["archived_P31_baseline_score_wrong_label_rows"],128)
    for row in self.new["records"]:
        if row["cohort"]=="P31":
            self.assertNotEqual(row["baseline_true_score"],row["baseline_remaining"])

 def test_full_source_replay_matches_persisted_result(self):
    baseline=json.loads((WORK/"p32_results.json").read_text())
    self.assertEqual(self.new,baseline)

 def test_receiver_exit_conservation(self):
    crossed,departed=corridor_ledger(self.a,self.tape)
    self.assertEqual(len(crossed),self.a["exit_S"]+self.a["exit_L"])
    self.assertEqual(len(departed),self.a["network_out_S"]+self.a["network_out_L"])
    self.assertEqual(len(departed)+self.a["remaining"],len(self.tape))

 def test_no_extra_network_departure_claim(self):
    corrupt=copy.deepcopy(self.a)
    corrupt["network_out_S"]+=1
    with self.assertRaises(AssertionError):corridor_ledger(corrupt,self.tape)

 def test_wrong_receiver_vehicle_movement_fails(self):
    corrupt=copy.deepcopy(self.a)
    f=next(f for f in corrupt["frames"] if f["receiver"])
    cells=list(f["receiver"])
    cell,vid,move=cells[0]
    cells[0]=(cell,vid,"L" if move=="S" else "S")
    f["receiver"]=tuple(cells)
    with self.assertRaises(AssertionError):corridor_ledger(corrupt,self.tape)

 def test_duplicate_receiver_vehicle_fails(self):
    corrupt=copy.deepcopy(self.a)
    f=next(f for f in corrupt["frames"] if f["receiver"])
    f["receiver"]=tuple(f["receiver"])+(f["receiver"][0],)
    with self.assertRaises(AssertionError):corridor_ledger(corrupt,self.tape)

 def test_forged_premature_departure_fails(self):
    corrupt=copy.deepcopy(self.a)
    f=next(f for f in corrupt["frames"] if f["receiver"])
    f["receiver"]=tuple()
    with self.assertRaises(AssertionError):corridor_ledger(corrupt,self.tape)

 def test_incomplete_frame_history_fails(self):
    corrupt=copy.deepcopy(self.a)
    corrupt["frames"]=corrupt["frames"][:-1]
    with self.assertRaises(AssertionError):corridor_ledger(corrupt,self.tape)

 def test_cross_pair_is_id_comparable(self):
    r=comparison(self.a,self.b,self.tape)
    self.assertTrue(r["fully_matching_aggregate"])
    self.assertEqual(r["score_delta"],0)
    self.assertTrue(r["common_completed_corridor_ids"]>=0)


if __name__=="__main__":unittest.main()
