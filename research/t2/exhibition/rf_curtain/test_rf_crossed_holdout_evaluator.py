"""RF05 crossed holdout contracts on synthetic rows; NOT actual CSI results."""
import copy
import unittest

from rf_crossed_holdout_evaluator import (
    TRAIN_CELLS, TEST_CELLS, UNUSED_RESERVE, evaluate_crossed
)
from rf_pilot_evaluator import LABELS, MODELS


def fixture():
    rows = []
    for session in ("S1", "S2", "S3"):
        for place in ("P1", "P2"):
            for index, label in enumerate(LABELS):
                for reset in range(10):
                    rows.append({
                        "trial_id": f"{session}-{place}-{label}-{reset}",
                        "session_id": session,
                        "placement_id": place,
                        "trial_origin": "synthetic_test_fixture",
                        "ground_truth_source": "synthetic_test_fixture",
                        "label": label, "quality": "ok",
                        "rssi_1_dbm": "-52.0", "rssi_2_dbm": "-58.0",
                        "csi_1_amp_dispersion": str(10.0 + index*10.0 + .001*reset),
                        "csi_2_amp_dispersion": str(15.0 + index*15.0 + .001*reset)
                    })
    return rows


def shift(rows, predicate, amount):
    new = copy.deepcopy(rows)
    for row in new:
        if predicate(row):
            row["csi_1_amp_dispersion"] = str(
                float(row["csi_1_amp_dispersion"]) + amount)
            row["csi_2_amp_dispersion"] = str(
                float(row["csi_2_amp_dispersion"]) + amount)
    return new


class RF05CrossedHoldoutTests(unittest.TestCase):
    def test_all_six_cells_present_and_three_test_holdouts_locked(self):
        out = evaluate_crossed(fixture())
        self.assertEqual(out["train_cells"], [["S1", "P1"], ["S2", "P1"]])
        self.assertEqual(out["train_n"], 100)
        self.assertEqual(out["unused_cell"], ["S1", "P2"])
        self.assertEqual(out["unused_n"], 50)
        self.assertEqual(set(out["test_cells"]), set(TEST_CELLS))
        self.assertTrue(all(out["test_reports"][k]["n"] == 50
                            for k in TEST_CELLS))
        self.assertEqual(out["primary_gate"], "NOT_APPLICABLE_SYNTHETIC_FIXTURE")

    def test_source_classifier_is_fit_to_train_only(self):
        out = evaluate_crossed(fixture())
        self.assertEqual(out["test_reports"]["joint"]["models"]["csi_both"]["macro_f1"], 1.0)
        self.assertEqual(out["test_reports"]["session_only"]["models"]["csi_both"]["macro_f1"], 1.0)
        self.assertLess(out["test_reports"]["joint"]["models"]["rssi_one"]["macro_f1"], 1.0)

    def test_placement_shift_fails_where_placement_unseen(self):
        baseline = evaluate_crossed(fixture())
        shifted = evaluate_crossed(shift(fixture(), lambda r: r["placement_id"] == "P2", 2000))
        self.assertEqual(baseline["test_reports"]["session_only"]["models"]["csi_both"]["macro_f1"],
                         shifted["test_reports"]["session_only"]["models"]["csi_both"]["macro_f1"])
        for name in ("placement_only", "joint"):
            self.assertLess(shifted["test_reports"][name]["models"]["csi_both"]["macro_f1"], 1.0)

    def test_session_shift_fails_where_session_unseen(self):
        shifted = evaluate_crossed(shift(fixture(), lambda r: r["session_id"] == "S3", 2000))
        self.assertEqual(shifted["test_reports"]["placement_only"]["models"]["csi_both"]["macro_f1"], 1.0)
        for name in ("session_only", "joint"):
            self.assertLess(shifted["test_reports"][name]["models"]["csi_both"]["macro_f1"], 1.0)

    def test_missing_csi_preserved_as_abstention_and_recall_loss(self):
        rows = fixture()
        for row in rows:
            if (row["session_id"], row["placement_id"], row["label"], row["trial_id"].endswith("-0")) == (
                "S3", "P2", "both", True):
                row["csi_1_amp_dispersion"] = ""
        out = evaluate_crossed(rows)
        joint = out["test_reports"]["joint"]["models"]["csi_both"]
        self.assertEqual(joint["abstain_rate"], 1 / 50)
        self.assertEqual(joint["per_class"]["both"]["recall"], .9)
        self.assertEqual(joint["test_n"], 50)
        self.assertEqual(out["primary_gate"], "NOT_APPLICABLE_SYNTHETIC_FIXTURE")

    def test_missing_cell_or_missing_label_is_invalid_not_ignored(self):
        rows = fixture()
        with self.assertRaisesRegex(ValueError, "independently reset"):
            evaluate_crossed([r for r in rows if not (
                r["placement_id"] == "P2" and r["session_id"] == "S1")])
        with self.assertRaisesRegex(ValueError, "independently reset"):
            evaluate_crossed([r for r in rows if not (
                r["placement_id"] == "P2" and r["session_id"] == "S3"
                and r["label"] == "downstream")])

    def test_extra_cell_and_mixed_provenance_rejected(self):
        rows = fixture()
        a = copy.deepcopy(rows)
        a[0]["session_id"] = "S4"
        with self.assertRaisesRegex(ValueError, "unexpected"):
            evaluate_crossed(a)
        a = copy.deepcopy(rows)
        a[0]["trial_origin"] = "measured_authorized_lab"
        a[0]["ground_truth_source"] = "manual_model_state"
        with self.assertRaisesRegex(ValueError, "mixed"):
            evaluate_crossed(a)

    def test_measured_status_is_not_independent_provenance_verification(self):
        rows = fixture()
        for row in rows:
            row["trial_origin"] = "measured_authorized_lab"
            row["ground_truth_source"] = "manual_model_state"
        result = evaluate_crossed(rows)
        self.assertEqual(result["status"], "LAB_TRIAL_ANALYSIS_REQUIRES_INDEPENDENT_SOURCE_AUDIT")
        self.assertEqual(result["primary_gate"], "PASS_PROVISIONAL_REQUIRES_SOURCE_AUDIT")

    def test_no_heldout_label_is_a_feature(self):
        self.assertEqual(set(TRAIN_CELLS), {("S1", "P1"), ("S2", "P1")})
        self.assertEqual(UNUSED_RESERVE, ("S1", "P2"))
        for fields in MODELS.values():
            self.assertFalse({"label", "placement_id", "session_id", "trial_id"} & set(fields))


if __name__ == "__main__":
    unittest.main()
