# T2 P11 — strict causal scheduler, optimization reliability
1. Write a minimal analytical queue/link/signal test for the exact threshold at 47.1625 seconds, with immutable timestamped event specifications. Distinguish physical clearance from mere stage order.
2. Test a coherent event-driven or tick-end state transition engine with causal dependencies: downstream receipt at t_end cannot be consumed at t_start; connector release not reused retroactively; queue and link updates require strict monotone event time.
3. Measure numerical convergence over several decreasing dt, policy objective and vehicle-specific event times; do not mistake a finite stable sequence for proof. Compare all 27 plans, not just the witness, with a margin/uncertainty gate.
4. Actual SUMO external replication and real-world calibration remain open, separate evidence requirements. A simulation optimum has no established field credibility yet.
5. Preserve original ZIP and extracted bytes; store differences and computed artifacts in 40_DERIVED. Research commits manual and no GitHub-Actions[bot] contributor.
