# T2 P14 — Finite-queue arrival-clock screen, pre-interpretation scope

2026-11-21. This research unit was executed locally **before** this record was committed. It is a retrospective methods/receipt note, NOT a prospective preregistration.

## Experimental design
- Two abstract queues A,B, capacity two vehicles each, four integer time slots.
- Two arrivals per queue, arrival slots from 0 to 3 allowing simultaneous arrivals: 10 possible multisets per queue, 100 joint worlds.
- Each time slot admits vehicles (up to queue capacity) before one unit of service on the prescribed lane.
- Compare fixed abstract sequences AABB and BBAA, NOT legally admissible traffic signal plans.
- Model cost = sum of post-service queue occupancies + five times discarded excess arrivals + twice terminal queue size. All coefficients are invented.
- Confirm per-world vehicle conservation: total four arrivals = serviced + lost + terminal.
- Strict opposite signs across worlds demonstrate arrival-time dependence under this model, NOT same-observation identification failure (P13 would require identical six-count observation and same action definition).
- Worlds differ in timing and decision-time states; these are not matched intervention checkpoints from PHYS.

## Local execution (Python)
100 total worlds; AABB lower cost in 39, BBAA lower cost in 39, 22 ties.
The complete delta histogram is symmetric: {-11:4,-7:2,-6:10,-5:10,-4:2,-2:2,-1:9,0:22,1:9,2:2,4:2,5:10,6:10,7:2,11:4}.
The smallest-magnitude opposed witnesses:
A arrivals slots (0,2), B slots (1,1): AABB 7, BBAA 8, Δ=-1.
A slots (1,1), B slots (0,2): AABB 8, BBAA 7, Δ=+1.
The signs are small and symmetric. The outcome does not identify an empirical traffic advantage.

Independent local run: `python -m unittest -v` => **13/13 passed**, conservation tests over every world/policy, run <0.1s.
Local source SHA256: `802e1b6de87efebb222136d7be9b2380905061e49d67a245135f1c19851c5cd6`.
Local test SHA256: `01a8b2f73daa8d013dad0b671d0a3506fcfd033f025568068414505cab3f034b`.
These hashes identify the local executed files; they do not claim GitHub-remote byte equality until the files are committed and independently compared.

## Required next gates
1. Preserve code/tests/output on main with exact file identity.
2. Repeat under different loss, holding and terminal-cost weights with predeclared independent evaluation units.
3. Connect only to separately validated PHYS arrival tapes and action constraints, not by reinterpreting abstract AABB/BBAA as real signal timing.
4. Check whether a meaningful strict reversal survives policy feasibility screening and more diverse clocks. Report effective independent arrival histories, not just 100 enumerated worlds.
5. Keep K047 sealed, CIM dataset on HOLD, no GitHub Actions/bot.
