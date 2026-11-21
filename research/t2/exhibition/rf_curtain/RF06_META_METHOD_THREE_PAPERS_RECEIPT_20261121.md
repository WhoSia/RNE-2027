# RF06-C — Three further mid-run papers admitted, measurement-to-action validity doctrine

Date: 2026-11-21. During the original 20-item intake, **three more PDFs arrived in Research OS 00_INTAKE** and were triaged separately. Each original was opened (first pages, abstract/key arguments), confirmed peer-reviewed scholarly article, renamed to P&K author/year/title format, moved to 10_PAPERS **preserving original Google Drive file ID**, and post-move parent location verified. A final folder listing of 00_INTAKE showed **zero direct child files**. Thus this turn processed **23 new PDFs (20 sensor/traffic + three meta-methodology)**. Do NOT conflate with user's entirely separate **CIM dataset.zip** download, which was not inspected or moved.

| Paper original, canonical Google Drive PDF | Published source and edition | Concrete research transfer (not a validation result) |
|---|---|---|
| [Kane (2013), *Validating the Interpretations and Uses of Test Scores*, ID 1nbQUgK4kFkjKS4X9Op_q2e5H-Vgm8epM](https://drive.google.com/file/d/1nbQUgK4kFkjKS4X9Op_q2e5H-Vgm8epM/view) | Journal of Educational Measurement 50(1), pp1–73; DOI [10.1111/jedm.12000](https://doi.org/10.1111/jedm.12000) | Validate an *inference and its use*, not the score alone. Measured CSI deviation → occupancy → pocket/downstream cause → signal action → welfare are distinct interpretations needing independently collected evidence; traffic signal use validity does NOT follow automatically from detector classification F1 |
| [Barr, Harman, McMinn, Shahbaz & Yoo (2015), *The Oracle Problem in Software Testing: A Survey*, ID 1GvLHYntPcmuPdjuFmKZdenmBHeAy0SxY](https://drive.google.com/file/d/1GvLHYntPcmuPdjuFmKZdenmBHeAy0SxY/view) | IEEE TSE 41(5), DOI [10.1109/TSE.2014.2372785](https://doi.org/10.1109/TSE.2014.2372785) (online DOI year 2014, journal year 2015) | A test can execute without a trustworthy **oracle** for correct outcomes. RF05's class-encoded synthetic data checks the evaluator, not RF; original physics claims require independent microscopic and real-world observations |
| [Zave & Jackson (1997), *Four Dark Corners of Requirements Engineering*, ID 1PwUeINSkW6vhhuUvYEh9YvGQFBWlWlav](https://drive.google.com/file/d/1PwUeINSkW6vhhuUvYEh9YvGQFBWlWlav/view) | ACM TOSEM 6(1), DOI [10.1145/237432.237434](https://doi.org/10.1145/237432.237434) | Separate *environment/domain assumptions* (vehicles, geometry, legal admissible signal phase) from *machine implementation requirements* (CSI parser, classifier, controller). A toy block-bit is not a verified real road state or lawful actionable phase |

## Explicit inference claim chain

1. **Wireless source**: authorized equipment actually yields CSI, not RSSI dressed as CSI → verify chip, firmware, channel, packet provenance.
2. **Sensor change**: observed channel measurement responds to known staged object → independently labeled lab calibration/ground truth; test no-demand, drift, missing links.
3. **Cause classification**: which of pocket/downstream/both was physically blocked → held-out session × antenna placement, full five-class confusion, unknown/abstain.
4. **Traffic mechanism**: a real left-turn bay or downstream receiving link stops through discharge → validate traffic geometry, route inflow, lane-change and spillover mechanics; source labels alone not enough.
5. **Control utility**: an admissible abstract signal decision improves cost → checkpoint paired counterfactual model *with operational controller constraints*, external data necessary for transport.
6. **Field deployment**: actual public intersection improves safely → outside the scope of student installation; independent highway authority approval, calibration, safety and ethics.

**Anti-shortcut:** `good F1` ≠ cause correctness ≠ observed T2 policy improvement ≠ deployable controller. No result in this turn changes the validity status of the previous PHYS synthetic studies. Distinguish each claim's test oracle and domain conditions.

## Directional project gate

The two tracks continue: (A) broad modality literature harvesting and honest physics-grounded exhibition creativity, (B) exact T2/RF mathematical observability, existing simulator realism and decision-feasibility validation. We should not optimize a synthetic classifier to compensate for missing hardware. The incoming **CIM dataset.zip** (approx 5 GB, downloading elsewhere) remains **UNTOUCHED HOLD**.

Status: P&K three additional PDF moves verified; method arguments reviewed; complete paper-by-paper figure/appendix reading still open. 00 intake root empty at final check. No GitHub Actions, no K047 unsealing.
