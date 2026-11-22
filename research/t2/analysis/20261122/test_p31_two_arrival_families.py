"""P31 tests: arrival-tape invariants and non-universal 6/10 score plateau."""
import copy,unittest
from collections import Counter
from p31_two_arrival_families import experiment,clock,SEED_DEMAND
from p19_receiver_service_opportunity import build_config
from spatial_v10 import arrivals

class ArrivalFamilyTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.result=experiment()
 def test_exact_128_world_grid_eight_tapes(self):
  self.assertEqual(self.result["worlds"],128)
  self.assertEqual(self.result["unique_arrival_tapes"],8)
  self.assertEqual(len(self.result["records"]),128)
 def test_unseen_seeds(self):
  self.assertEqual([a for a,_,_ in SEED_DEMAND],[124,125,126,127])
 def test_route_labels_counts_preserved(self):
  for seed,demand,turn in SEED_DEMAND:
   cfg=build_config(seed,demand,turn,14.,2,0.).base
   orig=arrivals(cfg)
   for family in ("uniform","platoon4"):
    tape=clock(cfg,family)
    self.assertEqual([r for _,r in tape],[r for _,r in orig])
    self.assertEqual(len(tape),len(orig))
    self.assertTrue(all(0<=t<240 for t,_ in tape))
 def test_monotonic_each_clock(self):
  for seed,demand,turn in SEED_DEMAND:
   cfg=build_config(seed,demand,turn,14.,2,0.).base
   for family in ("uniform","platoon4"):
    t=[z[0] for z in clock(cfg,family)]
    self.assertEqual(t,sorted(t))
 def test_invalid_family_fails(self):
  cfg=build_config(124,1650,.5,14.,2,0.).base
  with self.assertRaises(ValueError):clock(cfg,"unregistered")
 def test_price_plateau_is_falsified(self):
  self.assertEqual([r["different_score"] for r in self.result["by_family"]],[1,8])
  self.assertEqual([r["same_score"] for r in self.result["by_family"]],[63,56])
 def test_denial_increment_not_universal(self):
  self.assertEqual([r["denials_other"] for r in self.result["by_family"]],[12,8])
  self.assertEqual([r["denials_4_more"] for r in self.result["by_family"]],[52,56])
 def test_correct_64_worlds_per_family(self):
  self.assertEqual([r["worlds"] for r in self.result["by_family"]],[64,64])
 def test_crossing_audit_matches_when_score_varies(self):
  for r in self.result["records"]:
   for arm in ("six","ten"):
    z=r[arm]
    self.assertGreaterEqual(z["attempts"],z["distinct_rejected_vehicles"])
    self.assertEqual(z["attempts"],z["distinct_rejected_vehicles"]+z["repeat_attempts"])
 def test_all_9_cost_differences_are_negative_189(self):
  differences=[r["ten"]["score"]-r["six"]["score"] for r in self.result["records"]]
  self.assertEqual(Counter(differences),{0:119,-189:9})
 def test_deterministic_rerun(self):
  self.assertEqual(experiment(),self.result)

if __name__=="__main__":unittest.main()
