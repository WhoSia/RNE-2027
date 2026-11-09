# D42 — 2026-11-10 topology × time alignment audit (HOLD)

## Actual source and execution
- DLR UT v1.3.1, UTC 2023-09-24 12:00–12:15.
- Publisher OpenDRIVE map SHA-256 `256115a13cd29cb1d36cbbf110a4dbfa104ec2bdb680e3af1505a53f4ded30c4`, source Drive `1j6xu3ngbh1dO75_eCdrgBWVgytRAzGtg`.
- Publisher 32-movement, 900-second traffic volume SHA-256 `98e4e0a593702188c2d134cef1346cbc7501067c9ad421ddb9e72a1e6d9d1d15`, source `1L89cdXpt5qJ1hPS8w00C4pyzg-oxAqUB`.
- Prior D42 derived 684-event lane strip candidate CSV SHA-256 `40ed7bcdcf57faf2abfc4af397a04a091435e73830eba0659961ec6f212788bd`, source `1R9P7J2NKP0-MuZv0WLIz-RkxRpNFW__f`.
- A new self-contained ZIP includes the **exact locally executed Python implementation** `d42_topology_gate.py`, `d42_temporal_gate.py`, their tests, JSON results, CSVs and manifest; **20/20 tests passed** on the listed source inputs. ZIP SHA-256 `5b236164f3a0d206a999f117911a6f0a57f0afd18a086f929d422285d7d6469c`: https://drive.google.com/file/d/1pSS-IR3r1XU5pu48N-_B4kAmYM7e0ggz/view

## Validated map structure
Junction ID 300000 has 16 `connection` records. All connecting roads identify a matching incoming-road predecessor and one outgoing-road successor; **44 laneLinks** resolve to valid source and connector lane IDs. Four incoming approach roads and four outgoing roads form 4×4 origin-destination road pairs, via 16 internal connectors. This is the connectivity of the map, **not 32 empirically validated signal-controlled movements**.

Inferred cardinal approach mapping from road geometry: East=100000; South=179000; West=201000; North=280000. The map's four outgoing roads are 101000,180000,200000,279000. Cardinal assignment is an inference from physical approach position and heading, not a publisher lane/movement mapping.

## Apparent comparison and its limitations
After excluding the **exit** road 101000 (128 events) and **internal** junction roads 300013/300018 (110 events) from the 684 candidate gate crossings, 446 **approach candidates** remain; each is assigned to a distinct local track ID within the 15-minute file, but IDs are not verified unique physical vehicles. Approach candidate counts East 116, South 133, West 121, North 76.

Aggregating *publisher metadata* columns by origin label gives East 113, South 129, West 119, North 75, sum 436. Differences +3,+4,+2,+1 = +10. They cannot be used as an overall error-rate denominator because geometry, signal-head mapping, permitted turns, vehicle identity and publisher specific stopline definition remain unresolved.

A chronological one-to-one *within-approach* matching of candidate crossing epoch timestamps with publisher per-second count timestamps using a **declared ±1.0 second tolerance** yields East 113, South 126, West 118, North 75; total 432/436 publisher count entries matched. **14 candidates remain unmatched and 4 publisher count entries unmatched**. This pairing does not know individual vehicle IDs, can match adjacent different vehicles, and is NOT 432 verified common objects. Sensitivity checks: ±0.5s gives only 283 matches; uniformly shifting all candidates +1s gives 245 matches, +5s gives 165 matches. The apparent timing agreement strongly suggests a related time/crossing convention but does not certify exact events. The traffic-volume metadata are themselves derived from the same DLR trajectories, so this is an **internal consistency audit**, not independent external validation.

## Gate
Status remains **HOLD**. Required: finite lane-specific stopline geometry, connection lane routing, 30 head IDs mapped to 32 origin→destination lane movements, censored/ambiguous tracks, and independent held-out time-window comparison. No matched SUMO execution or real-world policy-effect claim.

## Derived artifacts
- Per-approach counts: https://drive.google.com/file/d/1k2QNA6WtQLjsIkULvlzVJYU-x_l1jtQO/view
- Per-approach time matching and shifted negative controls: https://drive.google.com/file/d/19bvpAJppltMnLK5IJ0RJhGuNInRa8CgB/view
- Unmatched candidates/publisher event table: https://drive.google.com/file/d/1jeE_tGjZvgFxQwoaAaINAVNK-h8yEGrj/view
- R&E 20261110 reasoning log: https://docs.google.com/document/d/1fkzetvDIyGTho0wyccceYvFhUvB5ZPtPAMhjmJK9DH8/edit

*Exact executable code is in the byte-sealed release ZIP; this Markdown file is the GitHub source-of-evidence pointer, not a claim the Python sources have been separately mirrored to GitHub.*
