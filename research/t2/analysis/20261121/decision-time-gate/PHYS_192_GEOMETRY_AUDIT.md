# Physical lane-change eligibility audit — source-based, not post-hoc selection

The original model has approach cells n=20 and lateral change zone z=floor(70/7)=10. Pocket entry begins at cell x=−k, where k=floor(pocket_length/7). A vehicle may move A→B only if it is a through vehicle, was not already moved longitudinally in the tick, and:
1. −z ≤ x < −k (upstream spatial eligibility);
2. B[x], B[x−1], B[x+1] are empty;
3. the A lane has a plausible immediate obstruction at x+1;
4. the simulator's `allow_lane_changes` switch is enabled.

With 14-m pocket k=2, the potential longitudinal origins are −10,...,−3 (**8 cells**). With 28m k=4, there are **6 cells** (−10,...,−5). With 70m k=10, the range [−10,−10) is empty (**0 cells**). This geometry alone forces `changes_A_to_B==0` for all 70m cases, independent of driver preference or congestion. The initial 192-run fixed grid therefore has no causal variation from permission at 70m.

Observed across 192 runs (counting both phase orders):
- 14m pocket: 1161 successful A→B moves
- 28m pocket: 941 successful A→B moves
- 70m pocket: **0** successful A→B moves.
The 70m cases have identical outcomes whether permission is enabled or not (64 runs in this stratum, paired in the same seed,Bshare,phase order).

**Decision:** do not generalize 0 reversals at 70m to real pocket design. Keep the primary grid sealed, and run a separately marked exploratory sensitivity at a longer lane-change zone (e.g. 100m) while preserving 70m pocket length and checking that eligible cells actually exist. A timed window experiment should not mix this geometry repair with its primary early/late comparison.
