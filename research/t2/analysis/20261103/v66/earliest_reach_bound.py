"""T2 v6.6-P0 — idealized minimum time to stop line.

Research-only analytic bound. Does not include leading vehicles, signal safety,
pedestrians, receiving supply, or acceleration followed by braking.
"""
from math import sqrt, isfinite

def earliest_reach_time(distance: float, speed: float, accel: float, speed_cap: float) -> float:
    values=(distance,speed,accel,speed_cap)
    if any(not isfinite(x) for x in values): raise ValueError("nonfinite input")
    if distance<0 or speed<0 or accel<=0 or speed_cap<=0: raise ValueError("invalid input")
    if distance==0: return 0.0
    if speed>=speed_cap:
        # Optimistic time at current speed; the approach speed already exceeds cap
        # and this is NOT a feasibility certification.
        return distance/speed
    t_acc=(speed_cap-speed)/accel
    d_acc=(speed+speed_cap)*t_acc/2
    if distance<=d_acc:
        return (sqrt(speed**2+2*accel*distance)-speed)/accel
    return t_acc+(distance-d_acc)/speed_cap
