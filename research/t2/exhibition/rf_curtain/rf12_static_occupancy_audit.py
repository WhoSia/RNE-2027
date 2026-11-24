"""RF12: deterministic, explicitly artificial counterexamples for CSI features.

No hardware capture, no RF wave propagation model, no measured accuracy.
Do not infer traffic state from these hypothetical scalar channels.
"""
from __future__ import annotations
from dataclasses import dataclass
from math import fsum, isfinite, sqrt
from typing import Iterable


@dataclass(frozen=True)
class TrialFeatures:
    amplitude_mean: float
    temporal_dispersion: float
    packet_count: int


def features(amplitudes: Iterable[float]) -> TrialFeatures:
    """Summarize frame-level scalar magnitudes in a single window.

    Equal to RF10's temporal aggregation if the input numbers are the
    per-packet mean-subcarrier amplitudes (not radio packets themselves).
    """
    x = tuple(amplitudes)
    if len(x) < 2 or any(isinstance(v, bool) or not isinstance(v, (int,float))
                         or not isfinite(v) or v < 0 for v in x):
        raise ValueError('at least two finite nonnegative scalar amplitudes')
    mean = fsum(x) / len(x)
    var = fsum((v - mean)**2 for v in x) / len(x)
    return TrialFeatures(mean, sqrt(var), len(x))


def compare_to_frozen_empty(trial: TrialFeatures, empty: TrialFeatures) -> dict:
    """A fixed same-domain empty reference is an *assumption*, not a fact.

    The empty baseline must be acquired before, independent of test labels.
    Using a target session's labelled samples during fitting breaks a strict
    zero-shot setup. Score is only a signed mean shift, not a class label.
    """
    if trial.packet_count < 2 or empty.packet_count < 2:
        raise ValueError('insufficient packets')
    return {'signed_mean_shift': trial.amplitude_mean - empty.amplitude_mean,
            'absolute_mean_shift': abs(trial.amplitude_mean - empty.amplitude_mean),
            'temporal_dispersion': trial.temporal_dispersion,
            'evidence_status': 'SYNTHETIC_SCALAR_FEATURE_ANALOGUE_NOT_MEASURED_CSI'}


def counterexamples() -> dict:
    """Three chosen worlds: no difference, static shift, and environment drift.

    `drift` and `static` are intentionally observationally equivalent in
    a single scalar channel. No classifier can identify cause from it alone.
    """
    empty = features([10.,10.,10.,10.])
    static = features([15.,15.,15.,15.])
    drift = features([15.,15.,15.,15.])
    moving = features([10.,12.,14.,16.])
    p0=compare_to_frozen_empty(empty,empty)
    p1=compare_to_frozen_empty(static,empty)
    p2=compare_to_frozen_empty(drift,empty)
    p3=compare_to_frozen_empty(moving,empty)
    assert p0['temporal_dispersion']==p1['temporal_dispersion']==p2['temporal_dispersion']==0
    assert p1['absolute_mean_shift']==p2['absolute_mean_shift']==5
    assert p3['temporal_dispersion'] > 0
    return {'status':'RF12_CONSTRUCTIVE_NON_IDENTIFIABILITY_COUNTEREXAMPLE',
            'radio_measurements':0,'worlds':{'empty':p0,'static_object':p1,
                'environment_drift':p2,'moving_object':p3},
            'verdict':'Temporal dispersion is insufficient for static occupancy. '
                'Frozen empty contrast separates an imposed static shift from '
                'empty in this artificial example, but not from identical drift. '
                'Therefore class identification requires controls, multiple '
                'paths or additional independently verified observations.'}


if __name__=='__main__':
    import json
    print(json.dumps(counterexamples(),ensure_ascii=False,indent=2))
