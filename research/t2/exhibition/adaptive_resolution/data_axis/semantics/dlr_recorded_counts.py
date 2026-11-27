"""DLR UT v1.3.1 §5.1 (p20): sparse routes, trajectory-covered seconds.
Only recorded counts; this adapter never grants decision-time availability.
"""
from dataclasses import dataclass
from data_contract import Window

@dataclass(frozen=True)
class RecordedCounts:
    window: Window
    known_routes: frozenset[str]

    def __post_init__(self):
        if not set(self.window.headers) <= self.known_routes:
            raise ValueError('route universe excludes supplied header')

    def bins(self, width, movement):
        if movement not in self.known_routes:
            return [dict(r, explicit_seconds=None, implicit_zero_seconds=None) for r in self.window.bins(width, movement)]
        present = movement in self.window.headers
        rows = self.window.bins(width, movement if present else None)
        return [dict(r, observed_count=r['observed_count'] if present or not r['coverage_seconds'] else 0,
                     explicit_seconds=r['coverage_seconds'] if present else 0,
                     implicit_zero_seconds=0 if present else r['coverage_seconds']) for r in rows]


def verified_collection(windows, expected_digests):
    """Exact audited publisher collection only; source identity by verified digest set.
    known routes are the union of supplied headers, not the full intersection map.
    """
    windows = tuple(windows)
    expected = frozenset(expected_digests)
    if not expected or len(windows) != len(expected) or {w.digest for w in windows} != expected:
        raise ValueError('unverified collection')
    if any(w.seconds != 900 or w.available_at is not None for w in windows):
        raise ValueError('expected historical 15-minute windows with unknown availability')
    if len({w.start for w in windows}) != len(windows):
        raise ValueError('duplicate window')
    routes = frozenset(k for w in windows for k in w.headers)
    return tuple(RecordedCounts(w, routes) for w in windows)
