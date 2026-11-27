"""External-review solver for the H08 shared-FIFO persistent-observation model.
Written after reading h08d_reference.py: same model definition (service budget 2, FIFO admission up to 2,
head-of-line blocking, iid fair binary arrival, free counts / head / full observation, four stages), but
generalised to per-pocket capacity and an arbitrary initial-state support. Exact Fractions. Parity with the
team's published H08D numbers is checked in ext_parity.py before any new claim is made."""
from fractions import Fraction as Q
from functools import lru_cache
from collections import Counter, defaultdict
from itertools import product
from math import gcd

A = (0, 1)
BUDGET = 2

def words(n):
    return [w for k in range(n + 1) for w in product(A, repeat=k)]

def gcd_norm(c):
    g = 0
    for v in c.values():
        g = gcd(g, v)
    return tuple(sorted((x, v // g) for x, v in c.items()))

def mass(b):
    return sum(v for _, v in b)

def obs(x, m):
    s, l, w = x
    if m == 0:
        return (s, l, w.count(0), w.count(1))
    if m == 1:
        return w[:1]
    return w

def split(b, m):
    d = defaultdict(Counter)
    for x, n in b:
        d[obs(x, m)][x] += n
    return {k: (sum(c.values()), gcd_norm(c)) for k, c in d.items()}

class Model:
    def __init__(self, caps=(2, 2), c=Q(1, 16), h=4):
        self.caps, self.c, self.h = caps, Q(c), h
        self.price = (Q(0), self.c / 4, self.c)

        @lru_cache(None)
        def step(x, a):
            q = list(x[:2]); w = list(x[2])
            for _ in range(BUDGET):
                if q[a]:
                    q[a] -= 1
            for _ in range(BUDGET):
                if not w or q[w[0]] == caps[w[0]]:
                    break
                q[w.pop(0)] += 1
            cost = sum(q) + len(w)
            return cost, tuple((q[0], q[1], tuple(w + [i])) for i in A)
        self.step = step

        @lru_cache(None)
        def fullq(x, h, a):
            r, ch = step(x, a)
            if h == 1:
                return Q(r)
            return Q(r) + sum(Q(1, 2) * min(fullq(y, h - 1, i) for i in A) for y in ch)
        self.fullq = fullq

    def solve(self, policy):
        step, price = self.step, self.price
        modes_of = {'free': (0,), 'head': (1,), 'full': (2,), 'adaptive': (0, 1, 2)}[policy]

        @lru_cache(None)
        def sense(b, h):
            vals = []
            for m in modes_of:
                v = (Q(0), price[m], Q(m == 1), Q(m == 2))
                parts = [(mass(b), b)] if m == 0 else list(split(b, m).values())
                for n, bb in parts:
                    u = control(bb, h)
                    v = tuple(x + Q(n, mass(b)) * y for x, y in zip(v, u))
                vals.append(v)
            return min(vals, key=lambda t: t[0] + t[1])

        @lru_cache(None)
        def control(b, h):
            n = mass(b)
            best = None
            for a in A:
                nxt = Counter(); imm = 0
                for x, m in b:
                    r, ch = step(x, a); imm += m * r
                    for y in ch:
                        nxt[y] += m
                v = (Q(imm, n), Q(0), Q(0), Q(0))
                if h > 1:
                    for k, (m2, bb) in split(tuple(nxt.items()), 0).items():
                        u = sense(bb, h - 1)
                        v = tuple(x + Q(m2, 2 * n) * y for x, y in zip(v, u))
                if best is None or v[0] + v[1] < best[0] + best[1]:
                    best = v
            return best
        return sense, control

    def class_values(self, support, policy):
        """Return {free-observation class: (n_worlds, (traffic,sensing,head,full))}."""
        sense, _ = self.solve(policy)
        out = {}
        b0 = tuple((x, 1) for x in support)
        for k, (n, bb) in split(b0, 0).items():
            out[k] = (n, sense(bb, self.h))
        return out
