# T2 G1 V5 — Research Director Admission Decision

## Advancement in a science-fair-first four-week program

**2026-11-13 / Week 1 site selection and real-data gate / DFS + BFS**

1. A real documentation discovery resolves what numeric states mean: DLR-UT v1.3.1 Figure 1 and Tables 3–4. This is not a new algorithm and should not be advertised as one. Grouped motorized signal heads, their reported positions and code definitions are public source metadata. We independently parsed and compared to two real signals CSV windows and prior seven center/front crossing candidates.
2. Crucial negative: published per-movement volumes are derived **from the same trajectories**, not independent labels. A publisher-count reproduction is an excellent benchmark of semantic/algorithmic reproducibility, but not accuracy against independent reality.
3. A literature backbone is in place: known left-turn blockage/spillback (Zhang/Tong 2008); heavy traffic delay (Yin 2011); signal-setting sensitivity (Wei 2021); calibration order (Harth 2022); field validation of spillback control (Han 2024); micro car-following (Krauß 1998). We shall replicate known baselines before new comparative design, explicitly checking each study's actual assumptions, design and boundary conditions.
4. 1 Hz sample-level state fractions are observations, not accurate cycle-time control plans. The head's physical location and road approach are documented, but the exact lane and directional movement actuated by that head remains unresolved. A temporal match is not a legal or causal signal compliance test. None of the 18:00–18:30 same-day holdout has been inspected.
5. The existing 12 V5 regression tests plus the independent previous 18 V4 source regression tests were executed in the same local environment (separate runs), both passed. This is software reproducibility, not traffic physics validation.

## Numerical evidence

- 35 documented coordinates for 26 distinct head IDs, with nonmotorized heads 10–13 absent from coordinate table (visible in Figure 1).
- Night 23:30–23:45 UTC: 899 observations/head; daytime 12:30–12:45 UTC: 895 observations/head. At night, head 2's 899 recorded samples are red (code 3). At midday 34 of 895 are green (code 5), so the observed sample fraction is 3.799%.
- 7 candidate road/object pairs with center and inferred front timestamps from V4; two heads per road approach; 28 signal-time brackets: 26 stable, 2 across a `red_yellow (4)→green (5)` change for candidate head 4 on the same object.
- Four road-end StVO 294 marking candidates and 30 traffic signal heads are distinct identifier systems. Figures in this package use *source-supplied UTM coordinates*, not invented street locations.

## Week-1 next gates and stop decisions

- **DFS**: determine whether DLR documentation Figure 1's specific lines and colors can be converted to a *movement-permission matrix*, with manual independent review. Do not assign left-turn lane based on proximity alone. Reconstruct one documented signal-cycle phase from 1Hz codes and compare fixed-time baseline of Harth et al. 2022. Freeze definitions before any holdout.
- **BFS**: seek Seoul `CROSS_ID` to C-ITS `itstId` joining evidence and actual same-day records; then seek CityArtery's raw sample files via licensed public access. Prioritize established DLR data until other source has a better empirical chain.
- **ABSTAIN**: do not claim better real-world signal policies, actual violation counts, independent GT or new scholarship for already established pocket spillback mechanisms.

## Custody

DLR-UT v1.3.1 canonical documentation Drive ID `1gUqUJEAGtXw06RjQCLbBoJ0k-pcee5Uq`. Original DLR raw and prior V4 kept unchanged. V5 independently produced standalone Python and derived tables, test summary and figures. No GitHub Actions usage; upload only authored code and textual evidence to GitHub. Notebook/meaning in 20261113 research-log Doc; reproducibility ZIP in Drive evidence shelf.
