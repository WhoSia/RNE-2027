"""WiTraffic (Won, Zhang & Son 2017) motivated 1-D EMD baseline.

This is a documented simplified analogue of the paper's histogram-based
lane comparison, NOT their complete WiTraffic detector, CSI extraction, lane
classifier, speed estimator, original bin metric or field result replication.

Published original stored as Drive PDF:
https://drive.google.com/file/d/1hMMeALKst2WyQUGAw0EorCZG6ddSkdK4/view
Method: normalized per-lane CSI histogram compared by Earth Mover's Distance.
For 1D ordered bin positions the 1-Wasserstein distance is the absolute CDF
difference integrated between bins. No CSI signals are generated here.
"""
from __future__ import annotations

from math import fsum, isfinite


def _check_distribution(hist: tuple[float, ...] | list[float]) -> tuple[float, ...]:
    if len(hist) < 2:
        raise ValueError("at least two bins required")
    if any(not isinstance(x, (float, int)) or isinstance(x, bool)
           or not isfinite(x) or x < 0 for x in hist):
        raise ValueError("histogram mass must be finite and nonnegative")
    total = fsum(hist)
    if not total or not isfinite(total):
        raise ValueError("histogram must have finite positive mass")
    return tuple(float(x / total) for x in hist)


def _check_bins(centers: tuple[float, ...] | list[float], count: int):
    if len(centers) != count:
        raise ValueError("one ordered center per bin required")
    if any(not isinstance(v, (int, float)) or isinstance(v, bool)
           or not isfinite(v) for v in centers):
        raise ValueError("finite numeric bin centers required")
    if any(centers[i] >= centers[i + 1] for i in range(count - 1)):
        raise ValueError("bin centers must strictly increase")


def emd_1d(hist_a, hist_b, *, bin_centers=None) -> float:
    """Exact 1D mass transport for ordered, normalized discrete histograms.

    Physical units are the units of bin_centers. For an equally spaced
    amplitude bin index, the result is in *bin-index units* and is not
    directly an absolute CSI fading amplitude or traffic speed.
    """
    left, right = _check_distribution(hist_a), _check_distribution(hist_b)
    if len(left) != len(right):
        raise ValueError("histogram sizes differ")
    centers = tuple(range(len(left))) if bin_centers is None else tuple(bin_centers)
    _check_bins(centers, len(left))
    cumulative = 0.0
    cost = 0.0
    for i in range(len(left) - 1):
        cumulative += left[i] - right[i]
        cost += abs(cumulative) * (centers[i + 1] - centers[i])
    return cost


def nearest_profile_by_emd(measurement, profiles: dict[str, tuple[float, ...]], *,
                           bin_centers=None) -> dict:
    """Rank frozen, externally acquired class profiles by 1D EMD.

    Does not fit profiles from the measurement itself or infer whether
    the top two scores are separable. Score margin alone is not a
    calibrated confidence probability.
    """
    if not profiles:
        raise ValueError("no profiles")
    if any(not isinstance(k, str) or not k.strip() for k in profiles):
        raise ValueError("invalid profile label")
    scores = {label: emd_1d(measurement, hist, bin_centers=bin_centers)
              for label, hist in profiles.items()}
    ordered = sorted(scores, key=lambda x: (scores[x], x))
    return {"best_label": ordered[0], "distances": scores,
            "best_minus_second_margin": (scores[ordered[1]] - scores[ordered[0]]
                                         if len(ordered) > 1 else None),
            "evidence_status": "MATHEMATICAL_BASELINE_ONLY_NOT_MEASURED_CSI"}
