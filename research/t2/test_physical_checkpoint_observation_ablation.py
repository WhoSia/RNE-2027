"""Contract tests for PHYS-05 observation features and no test-fold target leakage."""
import unittest
from physical_checkpoint_observation_ablation import features, predict, experiment


def toy_row(seed, capacity, pocket, share, delta):
    positions = {"outside_A": 0, "outside_B": 1,
                 "approach_A": 2, "approach_B": 3,
                 "pocket_vehicles": 1, "receiver_vehicles": 1,
                 "approach_A_positions": (-2, -1),
                 "approach_B_positions": (-3, -2, -1),
                 "pocket_positions": (-1,),
                 "receiver_occupied_cells": (0,)}
    return {"seed": seed, "capacity": capacity, "pocket_m": pocket,
            "b_share": share, "delta_p60": delta, "decision_observation": positions}


def fixture():
    return [toy_row(seed, capacity, pocket, share, (seed - 3) * 12)
            for capacity in (2,4,8) for seed in range(8)
            for pocket in (14.,28.,70.) for share in (0.,.5)]


class ObservationAblationTests(unittest.TestCase):
    def test_dimensions_and_consistent_scaling(self):
        x = fixture()[0]
        self.assertEqual(len(features(x, "geometry")), 3)
        self.assertEqual(len(features(x, "counts")), 9)
        self.assertEqual(len(features(x, "positions")), 67)

    def test_future_labels_cannot_enter_test_seed_prediction(self):
        rows = fixture()
        train = [r for r in rows if r["seed"] != 0]
        test = next(r for r in rows if r["seed"] == 0)
        old = {k: predict(train, test, k)
               for k in ("geometry", "counts", "positions")}
        test["delta_p60"] = 999999
        self.assertEqual(old, {k: predict(train, test, k)
                               for k in ("geometry", "counts", "positions")})

    def test_cross_validation_folds_do_not_share_seeds(self):
        output = experiment(fixture())
        self.assertEqual(len(output["out_of_fold_predictions"]), 144)
        for seed in range(8):
            heldout = [r for r in output["out_of_fold_predictions"]
                       if r["seed"] == seed]
            self.assertEqual(len(heldout), 18)

    def test_geometry_features_ignore_observation(self):
        row = toy_row(0, 4, 14., .5, -12)
        baseline = features(row, "geometry")
        row["decision_observation"]["outside_A"] = 999
        self.assertEqual(baseline, features(row, "geometry"))


if __name__ == "__main__":
    unittest.main()
