"""XR2 (external review r2): minimal tandem-queue-with-blocking model, written independently of the T2 cell engine.

State is a set of FIFO queues and integer clocks; no cells, no T2 code is imported.

  arrival a_i  --(free travel tau_u)-->  stopline queue  --(upstream phase, headway)-->
  shared downstream store of capacity C  --(min dwell tau_d; downstream green; headway h_d)--> exit

Variants
  M0  calendar only: cost proxy = -(left-green overlap seconds); no queues (the P116 rule).
  M1  movement queues QL, QS (no lane interaction); finite store C; storage carry-over between windows.
  M2  M1 + lane A head-of-line blocking: L and a share of S use lane A FIFO; L must enter a pocket of
      k slots before it can be served, so a waiting L blocks the S vehicles behind it in lane A.

Upstream service (per T2 calendar, but implemented here from its timing description only):
  L phase: one L per 2 s; S phase: one S per 1 s in total (two lanes, one store entry per second).
The store admits a vehicle only if it holds < C vehicles. Exit: one vehicle per h_d s while the
downstream signal is green, FIFO, and only after tau_d s inside the store.
Returns total vehicle-seconds sum(exit_i - a_i) and pooled 'denied seconds' (ticks in which a
stopline-ready vehicle of the active phase was refused by a full store).
"""
import random
from collections import deque


def upstream_phase(t):
    """Upstream calendar used by T2 experiments after the t=84 checkpoint (left-first 6 s override)."""
    if 84 <= t < 120:
        if 87 <= t < 93:
            return "L"
        if 96 <= t < 114:
            return "S"
        return "-"
    x = t % 120
    if x < 35:
        return "L"
    if 38 <= x < 88:
        return "S"
    return "-"


def simulate(tape, *, C, period, phi, variant="M1", tau_u=20, tau_d=None, h_d=2, k_pocket=1,
             b_share=.5, seed=0, horizon=6000, t0=84):
    """tape: tuple of (arrival_second, 'L'|'S'). Downstream green(t)=((t-84+phi)%period)<period//2 for t>=t0;
    before t0 the legacy 60 s clock green(t)=(t%60)<30 applies (as in T2's pre-checkpoint history)."""
    tau_d = C - 1 if tau_d is None else tau_d
    rng = random.Random(seed)
    lane = ["A" if m == "L" or rng.random() >= b_share else "B" for _, m in tape]
    ready = sorted(range(len(tape)), key=lambda i: (tape[i][0] + tau_u, i))  # time vehicle reaches stopline area
    nxt = 0
    QL, QS = deque(), deque()                       # M1 queues
    laneA, laneB, pocket = deque(), deque(), deque()  # M2 queues
    store = deque()                                 # (vehicle, entry_time)
    last_exit = -10**9
    last_up = {"L": -10**9, "S": -10**9}
    exit_t = {}
    denied = 0

    def green(t):
        if t < t0:
            return (t % 60) < 30
        return ((t - t0 + phi) % period) < period // 2

    for t in range(horizon):
        # 1) downstream exit
        if store and green(t) and t - last_exit >= h_d and t - store[0][1] >= tau_d:
            v, _ = store.popleft(); exit_t[v] = t; last_exit = t
        # 2) vehicles reach the stopline area
        while nxt < len(ready) and tape[ready[nxt]][0] + tau_u <= t:
            i = ready[nxt]; nxt += 1
            if variant == "M1":
                (QL if tape[i][1] == "L" else QS).append(i)
            else:
                (laneA if lane[i] == "A" else laneB).append(i)
        # 3) M2: lane A head L moves into pocket if room
        if variant == "M2":
            while laneA and tape[laneA[0]][1] == "L" and len(pocket) < k_pocket:
                pocket.append(laneA.popleft())
        # 4) upstream service into the store
        ph = upstream_phase(t)
        refused = False
        if ph == "L":
            q = QL if variant == "M1" else pocket
            if q and t - last_up["L"] >= 2:
                if len(store) < C:
                    store.append((q.popleft(), t)); last_up["L"] = t
                else:
                    refused = True
        elif ph == "S" and t - last_up["S"] >= 1:
            if variant == "M1":
                cands = [QS] if QS else []
            else:
                cands = [q for q in (laneA, laneB) if q and tape[q[0]][1] == "S"]
                cands.sort(key=lambda q: q[0])  # earliest-arrived head first
            if cands:
                if len(store) < C:
                    store.append((cands[0].popleft(), t)); last_up["S"] = t
                else:
                    refused = True
        denied += refused and t >= t0
        if len(exit_t) == len(tape):
            break
    assert len(exit_t) == len(tape), "model did not clear"
    return sum(exit_t[i] - tape[i][0] for i in range(len(tape))), denied, exit_t


def left_overlap(period, phi, t_end=400):
    return sum(upstream_phase(t) == "L" and ((t - 84 + phi) % period) < period // 2 for t in range(84, t_end))
