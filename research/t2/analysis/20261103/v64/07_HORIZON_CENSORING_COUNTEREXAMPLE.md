# T2 v6.4-P1: Fixed-horizon exposure reversal (20261103)

Restricted vehicle time E(H)=sum for b_i<=H of min(f_i,H)-b_i, where birth time b_i and eventual finish f_i. If every generated vehicle finishes before H, this equals eventual total travel time.

Reused 54 guard0 H=155s scenarios and newly ran 54 identical ID/OD scenarios at H=1000s. At H=1000s all 54 selected synthetic scenarios fully cleared.

Paired average profile-minus-uniform (3 demands x 6 seeds):
Later concentrated: H155 -263.250 vehicle-seconds versus H1000 +340.583 vehicle-seconds. **The apparent improvement reverses sign.**
12s platoon: H155 +73.083 vs H1000 -20.917; long-horizon mean is sensitive to chosen seeds.
Late profile: 420 unfinished vehicles summed across 18 short-horizon scenario replicates; zero at long horizon.
Six-seed-cluster exploratory bootstrap 10,000 draws, 3 demands kept grouped:
Late H155 [-366.722,-151.069]; H1000 [47.778,627.556].
Platoon H155 [37.750,98.903]; H1000 [-157.167,88.972].
CIs are about selected synthetic seeds, NOT real-road evidence.

Research gate: pre-register horizon, count generated/completed/censored vehicles and report policy-performance estimand. Never claim congestion benefit from truncated exposure under different arrival times.
Full source/data: https://drive.google.com/file/d/1jiZf9L9IpcWMQJ-lsnSsCYYuO2oewhZt/view
