# P9 result scope and external validation gate

These are original T2 2-junction mesoscopic model calculations, not physical measurements. The fixed plan grid permits stable argmin even with strongly grid-sensitive policy scores. Real-world reliability requires physical reference models and measured lane flows, queue sizes and detector positions.

P10 plan:
1. Trace first differing connector admission/release events for same arrival stream on dt .25 vs .05; compare queue front IDs and phase-boundary events.
2. Explicitly define and unit-test ordering of simultaneous link receipt, connector release, source arrival, downstream discharge and phase transitions. Consider event-time rather than tick-order execution.
3. Add dt sweeps on training-only and heldout outcomes; test winner margin versus numerical score uncertainty (with conservative bounds).
4. Obtain complete immutable SUMO Bologna–Pasubio raw files, install exact SUMO version and run paired conditions. Without lane/phase and vehicle correspondence the numeric comparison is invalid.
5. Independently validate with observed traffic data (Jinju, NGSIM, Utah SPaT) rather than treating SUMO as truth.

No external signal-controller interaction. No original-byte modification. GitHub-Actions[bot] author/contributor prohibited.
