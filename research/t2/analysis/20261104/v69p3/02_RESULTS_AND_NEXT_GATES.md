# Independent P3 results and research gates

## Same-policy-space search contrast
For balanced arrivals and buffer capacity 1, coordinate descent started at (6,6,0) and updated upstream main green, downstream main green, then offset. It stopped at (4,4,3). Exhaustive enumeration of the same 27 feasible policies selected (8,8,3). Training objective (vehicle-steps): 8113.3333 vs 7147.6667; training gap 965.6667. Across 24 unused seeds, exhaustive minus coordinate averaged -983.2917 vehicle-steps, exhaustive lower on 24/24. In the other 8 conditions coordinate and exhaustive chose the same policy. This shows a specific starting-point/update-order local trap, **not** general superiority of exhaustive search under larger decision spaces.

## Verification
5/5 standalone unittest tests passed, ZIP CRC pass, ZIP SHA-256 fe49994f73adda80ed6cb4664798ac3650862b786629f357242ccdf254934ee0.
Drive readback: https://drive.google.com/file/d/1KZgbvW4r73W-qmduMnNNxWZ75OqVa9DT/view
paired CSV: https://drive.google.com/file/d/1NKTyDt0sB87d1sxKQ3vCn_TjCrjZYf0o/view
travel lag ablation: https://drive.google.com/file/d/14aLCf2E_YDXicv11cVcG1lFjVQXGZd_S/view

## Next gates
1. Re-run lag/storage falsification protocol on the **archived v6.9-P2** complete code with the physical units preserved; current P3 is separate.
2. Enforce common action space and input budget when comparing local versus joint control.
3. Increase independent training and evaluation dates/scenarios; report policy regret, unfinished queues, and uncertainty by seed group.
4. Preserve the P5/P3 stopline seed943 counterexample as a blocking safety gate, not a cleared bug.
5. Calibrate a simple queue and high-fidelity model against actual observed junction data; validate on held-out date and, where feasible, SUMO.

Researcher status: audit methodology accepted for refinement; no physical model / policy operational promotion.
