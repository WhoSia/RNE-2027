# P147 prereg — finite latent-state observation contract

A minimal logical model of one green movement, NOT a calibrated traffic model.
Enumerate all eight triples (demand, pocket_block, downstream_block), each binary.
Discharge = demand AND NOT pocket_block AND NOT downstream_block.
Cause labels: no_demand overrides both blockage flags; when demand exists, free/pocket/downstream/both correspond to the flags.
Test every subset of ideal binary observations (discharge, demand, pocket_block, downstream_block). Report observation equivalence classes, ambiguous classes, worst class count, and exact label identifiability. No probability or physical sensing claim.
In particular test whether discharge + both blockage flags is enough without demand; whether demand + both flags is enough without discharge.
No Wi-Fi observation equated with an ideal flag. This is a logic benchmark for future sensor design. 
