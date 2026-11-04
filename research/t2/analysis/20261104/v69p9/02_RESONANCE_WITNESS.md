# P9 60-second phase-scale temporal resonance witness

Original P2; demand upstream_peak, storage 18m, heldout seed 223, plan (24,24,24), horizon 1200s, all 63 generated vehicles complete under every step size.

dt(s): 0.5=>20965.5; 0.4=>19686.8; 0.25=>19661.5; 0.2=>19680.0; 0.125=>20960.75; 0.1=>20966.3; 0.0625=>20963.625; 0.05=>20963.4 vehicle-seconds.

Compared to dt 0.05, dt 0.25 has 27/63 per-ID completion timestamps differing by >=50 seconds (maximum ~60.5 s). dt 0.1's max completion timestamp deviation is ~0.05 s. Thus smaller dt is not sufficient to guarantee monotone convergence in this discrete event model, and 0.25 cannot be treated as truth.

Additional witness downstream_side_peak, storage 18m, seed 211, plan (24,30,24): dt 0.5=9814.5 veh-s, .25=10994.5, .125=10995.375, .05=10997.2. Suspected cause includes queue propagation at signal phase boundaries and connector clearance timing. The exact causal mechanism is NOT YET proven; compare earliest differing events and add deterministic event-order tests.
