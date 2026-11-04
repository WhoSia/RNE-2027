# T2 v6.9-P9 — Time-grid convergence and SUMO validation gate
Date: 2026-11-04. Original P2 source SHA256 ZIP: 99e5b8173bfa1e6e002193785cae5124e2df14c335b2a14ce7e0696b601c823e. Source unmodified.

Research question: will the selected traffic signal policy change when step size is refined, and can numerical simulation outputs be trusted as inputs to an optimization claim?

Design: 4 predeclared synthetic demand profiles x two network storage settings (18m / 60m) x 2 independent evaluation seeds (211, 223) x 27 fixed candidate plans x two step sizes (.5 and .25s) x one full-completion horizon (1200s) = 864 original P2 simulation runs. Source arrival IDs, types, and timestamps are matched within each block. No field data or SUMO simulation used.

Evidence: source code, checksum manifest, tests, exact CSVs and diagnosis in shared Drive folder https://drive.google.com/drive/folders/1QrR6L77H28vwda1ujFERnuIr449hneaL . ZIP SHA256 3f5dbf4d81756208e1a5c46e4906a32b95fe50ac0a61e4f142ba39097c2139bd.

The official SUMO 1.28.0 installer is available from https://eclipse.dev/sumo/docs/Downloads.html but this sandbox has no SUMO binary or network route to original Pasubio files. Independent SUMO-run count remains ZERO.
