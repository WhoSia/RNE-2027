from fractions import Fraction as Q
from ext_fifo_solver import *
sup = [(s, l, w) for s in range(3) for l in range(3) for w in words(4)]
M = Model(caps=(2, 2), c=Q(1, 16), h=4)
tot = {}
for pol in ('free', 'head', 'full', 'adaptive'):
    cv = M.class_values(sup, pol)
    N = len(sup); v = [Q(0)] * 4
    for k, (n, vv) in cv.items():
        v = [a + Q(n, N) * b for a, b in zip(v, vv)]
    tot[pol] = v
    print(pol, 'traffic', v[0], 'sensing', v[1], 'head', v[2], 'full', v[3], 'objective', float(v[0] + v[1]))
assert tot['free'][0] == Q(3031, 279)
assert tot['full'][0] == Q(1004, 93)
assert tot['adaptive'][0] == Q(1004, 93) and tot['adaptive'][1] == Q(1, 279)
assert tot['adaptive'][2] == Q(32, 279) and tot['adaptive'][3] == Q(8, 279)
print('PARITY_WITH_H08D_PUBLISHED_NUMBERS: PASS')
