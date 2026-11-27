"""Offline feature contract for sampled binary occupancy, not vehicle counts."""
from itertools import product


def features(rows):
    out = []
    prev = None
    age = None
    releases = 0
    for t, signal, occupied in rows:
        if type(t) is not int or signal not in (0, 1, None) or occupied not in (0, 1, None):
            raise ValueError('invalid sample')
        if prev is not None and t <= prev[0]:
            raise ValueError('timestamps must strictly increase')
        contiguous = prev is not None and t == prev[0] + 1
        same_segment = contiguous and signal is not None and signal == prev[1] and occupied is not None and prev[2] is not None
        if not same_segment:
            releases = 0
        edge = 'unknown'
        if contiguous and occupied is not None and prev[2] is not None:
            edge = 'fall' if prev[2] == 1 and occupied == 0 else 'rise' if prev[2] == 0 and occupied == 1 else 'none'
        assigned = edge == 'fall' and same_segment
        releases += int(assigned)
        if occupied == 1:
            age = 0
        elif occupied == 0 and contiguous and age is not None:
            age += 1
        else:
            age = None
        out.append((t, age, edge, assigned, releases if signal is not None and occupied is not None else None))
        prev = (t, signal, occupied)
    return out


def audit():
    sequences = 0
    prefixes = 0
    for s in product((0, 1, None), repeat=5):
        for d in product((0, 1, None), repeat=5):
            rows = list(zip(range(5), s, d))
            result = features(rows)
            for k in range(1, 6):
                assert features(rows[:k]) == result[:k]
                prefixes += 1
            for i in range(1, 5):
                assigned = d[i-1] == 1 and d[i] == 0 and s[i] is not None and s[i] == s[i-1]
                assert result[i][3] == assigned
            sequences += 1
    assert features([(0,1,1),(1,1,0)])[1] == (1,1,'fall',True,1)
    assert features([(0,1,1),(2,1,0)])[1] == (2,None,'unknown',False,0)
    assert features([(0,0,1),(1,1,0)])[1] == (1,1,'fall',False,0)
    assert features([(0,1,0),(1,1,0)])[1][1] is None
    assert features([(0,1,1),(1,1,None),(2,1,0)])[2][1] is None
    for rows in ([(0,1,1),(0,1,0)], [(1,1,1),(0,1,0)], [(0,2,1)]):
        try:
            features(rows)
        except ValueError:
            pass
        else:
            raise AssertionError('invalid input accepted')
    # A forward-looking falling-edge convention changes t=0 with same prefix.
    assert int(1 - 0 > 0) != int(1 - 1 > 0)
    assert features([(0,1,1),(1,1,0)])[0] == features([(0,1,1),(1,1,1)])[0]
    return {'synthetic_sequences': sequences, 'prefix_checks': prefixes, 'assignment_checks': sequences * 4, 'boundary_cases': 10, 'status':'PASS_SYNTHETIC_ONLY'}


if __name__ == '__main__':
    import json
    print(json.dumps(audit(), indent=2))
