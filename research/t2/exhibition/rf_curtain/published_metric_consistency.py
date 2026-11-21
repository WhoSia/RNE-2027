"""Audit *reported* per-class precision, recall and F1 in CSI papers.

This checks arithmetic only, NOT original labels/training/sensor fidelity,
and cannot infer which reported metric is mistaken.

Source currently audited: Shahid et al. (QPAIN 2025), Bi-LSTM Table I
Drive original ID 1w2zgRKFFuWl3CsPBec7xHQkqi_7eNIcc.
Recorded example: 'Leguna-type' precision .67 recall .57 F1 .24.
"""
import math


def harmonic_f1(precision: float, recall: float) -> float:
    for v in (precision, recall):
        if isinstance(v, bool) or not isinstance(v, (float, int)):
            raise ValueError("precision/recall must be numeric")
        if not math.isfinite(v) or not 0 <= v <= 1:
            raise ValueError("precision/recall must be finite in [0,1]")
    if precision + recall == 0:
        return 0.0
    return 2 * precision * recall / (precision + recall)


def check_reported_row(label: str, precision: float, recall: float,
                       reported_f1: float, *, rounding_tolerance: float = 0.02) -> dict:
    if isinstance(reported_f1, bool) or not isinstance(reported_f1, (int, float)) or not math.isfinite(reported_f1) or not 0 <= reported_f1 <= 1:
        raise ValueError("invalid reported F1")
    if not isinstance(label, str) or not label.strip():
        raise ValueError("invalid class label")
    if isinstance(rounding_tolerance, bool) or not isinstance(rounding_tolerance, (int, float)) or not math.isfinite(rounding_tolerance) or not 0 <= rounding_tolerance <= 1:
        raise ValueError("invalid tolerance")
    inferred = harmonic_f1(precision, recall)
    mismatch = abs(inferred - reported_f1)
    return {
        "label": label, "reported_precision": precision, "reported_recall": recall,
        "reported_f1": reported_f1, "harmonic_f1": inferred,
        "absolute_discrepancy": mismatch,
        "flagged": mismatch > rounding_tolerance,
        "evidence_status": "ORIGINAL_TABLE_TEXT_ARITHMETIC_ONLY_NOT_RF_REPLICATION"
    }


def shahid_2025_reported_bilstm_leguna() -> dict:
    return check_reported_row("Leguna-type", 0.67, 0.57, 0.24)
