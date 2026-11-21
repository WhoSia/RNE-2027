"""RF04 math-only OpenCSI-style known-quiet scalar calibration.

Inspired by Khamaisi, Sigg & Rodrigues (2026), OpenCSI arXiv 2607.26665v2,
Drive PDF 1rqlZxB_wmDxYrpF6o28KeLJwE17qcSyw.
Only Welford quiet baseline and z=abs(x-mu)/s are transferred. This is NOT
OpenCSI source code, CSI parser, maturity/reliability method, detector
validation, or traffic sensor. Input samples are assumed externally verified
quiet; contamination defeats the assumption.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import isfinite, sqrt


def _finite_number(value: float, field: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (float, int)):
        raise ValueError(f"{field} must be numeric")
    if not isfinite(value):
        raise ValueError(f"{field} must be finite")
    return float(value)


@dataclass
class QuietBaseline:
    min_samples: int = 3
    sigma_floor: float = 1e-9
    n: int = 0
    mean: float = 0.0
    m2: float = 0.0
    frozen: bool = False

    def __post_init__(self):
        if type(self.min_samples) is not int or self.min_samples < 3:
            raise ValueError("min_samples must be integer >=3")
        if _finite_number(self.sigma_floor, "sigma_floor") <= 0:
            raise ValueError("sigma_floor must be positive")

    def ingest_known_quiet(self, amplitude: float) -> None:
        if self.frozen:
            raise ValueError("calibration frozen: no scoring-time leakage")
        value = _finite_number(amplitude, "amplitude")
        self.n += 1
        delta = value - self.mean
        self.mean += delta / self.n
        self.m2 += delta * (value - self.mean)

    def freeze(self) -> None:
        self.frozen = True

    def score(self, amplitude: float, *, threshold: float = 3.0) -> dict:
        value = _finite_number(amplitude, "amplitude")
        cutoff = _finite_number(threshold, "threshold")
        if cutoff <= 0:
            raise ValueError("threshold must be positive")
        if not self.frozen:
            return {"status": "ABSTAIN_NOT_FROZEN", "z": None, "flagged": None}
        if self.n < self.min_samples:
            return {"status": "ABSTAIN_TOO_FEW_QUIET", "z": None, "flagged": None}
        sigma = sqrt(max(self.m2 / (self.n - 1), 0.0))
        if sigma <= self.sigma_floor:
            return {"status": "ABSTAIN_ZERO_VARIANCE", "z": None, "flagged": None}
        z = abs(value - self.mean) / sigma
        if not isfinite(z):
            return {"status": "ABSTAIN_NONFINITE_SCORE", "z": None, "flagged": None}
        return {"status": "SCALAR_DEVIATION_ONLY", "z": z,
                "flagged": z >= cutoff}


def compare_two_zones(calibrators: dict, amplitudes: dict,
                      *, threshold: float = 3.0) -> dict:
    """Only report two separately calibrated deviations, NEVER a blockage cause."""
    zones = ("pocket", "downstream")
    if set(calibrators) != set(zones) or set(amplitudes) != set(zones):
        raise ValueError("exact pocket/downstream zones required")
    if any(amplitudes[name] is None for name in zones):
        return {"status": "ABSTAIN_MISSING_LINK", "zones": None,
                "cause": None}
    reports = {name: calibrators[name].score(amplitudes[name],
                                             threshold=threshold)
               for name in zones}
    if any(x["status"] != "SCALAR_DEVIATION_ONLY" for x in reports.values()):
        return {"status": "ABSTAIN_UNRELIABLE_CALIBRATION", "zones": reports,
                "cause": None}
    return {"status": "TWO_SCALAR_DEVIATIONS_NOT_CAUSAL_CLASSIFICATION",
            "zones": reports, "cause": None}


def preregistered_fixture_audit() -> dict:
    """Generate only the five locked arithmetic examples; no measured CSI."""
    def score(quiet, reading):
        calibrator = QuietBaseline()
        for x in quiet:
            calibrator.ingest_known_quiet(x)
        calibrator.freeze()
        return calibrator.score(reading)
    base = [9., 10., 11., 10., 10.]
    return {
        "evidence": "SYNTHETIC_MATH_ONLY_NOT_RF_DATA",
        "original": score(base, 13.),
        "affine_gain": score([2*x+7 for x in base], 2*13+7),
        "higher_quiet_variance": score([8., 10., 12., 10., 10.], 13.),
        "occupied_bootstrap_contamination": score([12., 13., 14., 13., 13.], 13.),
        "quiet_drift": score(base, 14.),
        "zero_variance": score([10.]*5, 13.)
    }


if __name__ == "__main__":
    import json
    print(json.dumps(preregistered_fixture_audit(), sort_keys=True, indent=2))
