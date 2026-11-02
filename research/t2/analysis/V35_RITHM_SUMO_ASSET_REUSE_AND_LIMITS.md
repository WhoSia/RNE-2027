# T2 V35 — RITHM SUMO assets that actually transfer (2026-11-02)

## Verified bytes
Original RITHM S02.16 Monaco evidence archive: Drive file 1_7ZLqku4ToJyIU19UnS-St-JMRIf0AQc, 31,028,033 compressed bytes. Parsed 38 tar members and verified SHA256 of all 38 against its 38-entry sidecar manifest; **0 mismatches**. Source scenario MoST commit b29b2f65f1096a9c69a601ec62a724815cb4a43f; SUMO version 1.14.0, simulation step 0.25s, begin 14400/end 50400, seed 42, teleport disabled with time-to-teleport=-1.

## Recomputed XML outcomes (not causal estimates)
Rerouting share 0/30/70/100 percent: tripinfo count 39746/44424/45092/45459; mean completed-trip duration seconds 12956.3379/10673.5479/10073.0009/9362.4999; mean waiting seconds 8664.4182/5693.7425/4886.5922/3630.2152. Unique tripinfo IDs within each scenario, duplicates zero. Different completion counts make naïve means selection-biased; these are descriptive completed-trip summaries, not signal-timing effects. Original source is from another research project and does not validate T2.

## Useful direct components
Tripinfo XML parser; simulation config shape; RITHM SUMO MoST documentation and input route list; four scenario outputs; baseline comparing full-trip completion and waiting-time. The archive does **not** contain all MoST network and route input files, and does not contain an implemented traffic signal optimizer. Do not transplant RITHM governance.

## Cross-project constraint
T2 code and claims remain independent. The first T2-specific SUMO task is a three-junction Korean corridor defined with genuine geometry and calibrated local turning counts, versus current synthetic 3-junction model. Reuse parser and benchmark interface, not Monaco-derived parameter estimates.
