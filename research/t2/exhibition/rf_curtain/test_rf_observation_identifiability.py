import itertools
import unittest

from rf_observation_identifiability import (
    SENSORS, LABELS, WORLDS, compatible_labels, partition, audit
)


class IdealRFObservationAuditTests(unittest.TestCase):
    def test_each_ideal_true_world_matches_all_its_observed_bits(self):
        for world in WORLDS:
            for n in range(4):
                for subset in itertools.combinations(SENSORS, n):
                    observed = {s: getattr(world, s) for s in subset}
                    self.assertIn(world.label, compatible_labels(observed))

    def test_one_static_rf_region_never_identifies_a_unique_label(self):
        for s in ("pocket", "downstream"):
            groups = partition((s,))
            self.assertEqual(sum(len(g["labels"]) == 1 for g in groups), 0)

    def test_two_static_regions_cannot_separate_no_demand_from_free(self):
        groups = partition(("pocket", "downstream"))
        self.assertEqual(len(groups), 4)
        matching = [set(g["labels"]) for g in groups if len(g["labels"]) == 2]
        self.assertEqual(matching, [{"no_demand", "free"}])
        self.assertEqual(sum(g["size"] == 1 for g in groups), 3)

    def test_independent_approach_demand_resolves_all_five_ideal_worlds(self):
        groups = partition(SENSORS)
        self.assertEqual(len(groups), 5)
        self.assertTrue(all(g["size"] == 1 for g in groups))
        self.assertEqual(compatible_labels({"pocket": False,
                                            "downstream": False,
                                            "approach_demand": False}),
                         ("no_demand",))
        self.assertEqual(compatible_labels({"pocket": False,
                                            "downstream": False,
                                            "approach_demand": True}),
                         ("free",))

    def test_missing_bit_retains_all_compatible_worlds(self):
        self.assertEqual(compatible_labels({}), LABELS)
        self.assertEqual(compatible_labels({"pocket": None}), LABELS)
        self.assertEqual(compatible_labels({"pocket": True}),
                         ("pocket", "both"))
        self.assertEqual(compatible_labels({"pocket": True,
                                            "downstream": None}),
                         ("pocket", "both"))

    def test_contradictory_sensors_abstain_instead_of_hallucinating(self):
        self.assertEqual(compatible_labels({"pocket": True,
                                            "approach_demand": False}), ())
        self.assertEqual(compatible_labels({"downstream": True,
                                            "approach_demand": False}), ())

    def test_reject_unknown_invalid_or_repeated_sensor(self):
        with self.assertRaisesRegex(ValueError, "unknown"):
            partition(("rssi",))
        with self.assertRaisesRegex(ValueError, "duplicate"):
            partition(("pocket", "pocket"))
        with self.assertRaisesRegex(ValueError, "ideal observation"):
            compatible_labels({"pocket": 1})
        with self.assertRaisesRegex(ValueError, "ideal observation"):
            compatible_labels({"pocket": "False"})

    def test_extra_ideal_observation_never_increases_ambiguity(self):
        for world in WORLDS:
            for n in range(3):
                for subset in itertools.combinations(SENSORS, n):
                    original = {s: getattr(world, s) for s in subset}
                    original_set = set(compatible_labels(original))
                    for s in SENSORS:
                        if s not in subset:
                            updated = dict(original)
                            updated[s] = getattr(world, s)
                            self.assertLessEqual(
                                len(compatible_labels(updated)),
                                len(original_set))

    def test_audit_does_not_claim_real_measured_sensor(self):
        out = audit()
        self.assertEqual(out["status"],
                         "ANALYTIC_IDEAL_OCCUPANCY_ONLY_NOT_MEASURED_RF")
        self.assertEqual(len(out["sensor_combinations"]), 8)
        pair = next(r for r in out["sensor_combinations"]
                    if r["sensors"] == ["pocket", "downstream"])
        self.assertEqual(pair["unique_label_count"], 3)
        self.assertEqual(out["contradictory_example"]["compatible"], [])


if __name__ == "__main__":
    unittest.main()
