"""Minimal finite-queue T2 counterexample scanner.

This is NOT the spatial traffic model. It tests a precisely defined toy FIFO
model with one arrival per step, pre-discharge bay admission, and one exit per
green movement per step. No lane changing, speed or downstream spillback.

Run: python research/t2/analysis/finite_queue_exhaustive.py
"""
from itertools import product

def simulate(sequence, straight_green, left_green, bay_capacity):
    if bay_capacity < 1:
        raise ValueError("bay_capacity must be positive")
    if not (len(sequence) == len(straight_green) == len(left_green)):
        raise ValueError("input lengths differ")
    shared = []
    bay = 0
    exited = 0
    for ch, sg, lg in zip(sequence, straight_green, left_green):
        if ch not in "SL":
            raise ValueError("invalid movement")
        shared.append(ch)
        if shared and shared[0] == "L" and bay < bay_capacity:
            shared.pop(0)
            bay += 1
        if sg and shared and shared[0] == "S":
            shared.pop(0)
            exited += 1
        if lg and bay:
            bay -= 1
            exited += 1
        assert len(shared) + bay + exited <= len(sequence)
    assert len(shared) + bay + exited == len(sequence)
    return exited

def scan(max_steps=8):
    checked = 0
    for n in range(1, max_steps + 1):
        for seq in product("SL", repeat=n):
            for sg in product((0, 1), repeat=n):
                for lg in product((0, 1), repeat=n):
                    checked += 1
                    low = simulate(seq, sg, lg, 1)
                    high = simulate(seq, sg, lg, 2)
                    if high < low:
                        return {"checked": checked, "counterexample": {
                            "movement": "".join(seq), "sg": sg, "lg": lg,
                            "K1": low, "K2": high}}
    return {"checked": checked, "counterexample": None}

if __name__ == "__main__":
    print(scan())
