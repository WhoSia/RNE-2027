# P125 prereg — exact cumulative-departure identity and independent reconstruction from P124

Freeze P124_RESULT.json as the sole input; NO new T2 simulation or fitting. This is an exact numerical identity, known in queueing theory (cumulative input-output curves), NOT a novel theorem.

Let A(t) be cumulative common arrivals through tick t, D_pi(t) cumulative final exits under policy pi, N_pi(t)=A(t)-D_pi(t), and define total post-tick vehicle-seconds over t=84..4799. Since identical predecision vehicles and the same arrival tape, N_a-N_b = D_b-D_a every t. Hence J_a-J_b = sum_t [D_b(t)-D_a(t)], and for full clearing also sum_i(e_a(i)-e_b(i)). Prove by conservation only, no Markov or independence assumptions.

Reconstruct D_b-D_a for the same period30 phi0 versus phi1 using solely P124's `vehicle_exit_deltas` (unchanged IDs cancel). Assert that its five preregistered windows equal P124's five frame-zone window totals [0,-1,-49,-257,-425], overall -732, and cumulative contrast max difference -3 at first recorded tick 204 (tie handling documented). Check first divergence at t114. Report NO causal attribution beyond ID-specific event chronology; arrivals fixed, signal calendars differ, storage fixed. This result is tautological under conservation but is a useful executable integrity gate that prevents false overlap-driven narratives.
