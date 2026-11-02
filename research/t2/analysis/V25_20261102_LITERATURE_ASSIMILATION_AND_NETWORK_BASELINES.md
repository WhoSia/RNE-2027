# T2 — 20261102 literature assimilation, Research OS canonical custody

## Intake processed
Five verified articles originally in Research OS 00_INTAKE were renamed to short author (year) — title filenames and moved without file-ID changes to 10_PAPERS: Varaiya (2013); Harth, Langer & Bogenberger (2022); Xiong et al. (2026, EPUB); Ma et al. (2021); Hallmark et al. (2010). Not all 00_INTAKE items are articles: existing hold/duplicate files and a philosophy EPUB must remain pending independent handling.

## Native detailed reading record
https://docs.google.com/document/d/1zaUc5dScw47gwm49UjxGF94dbtxWFa9h7igd6fvlzXU/edit
Folder: 20261102 김우준의 사유 https://drive.google.com/drive/folders/1fOdKyyYSme3T9RGEJb4SQJ2N3P3xmHCe

## Source-derived findings
- Varaiya (2013), DOI 10.1016/j.trc.2013.08.014: max-pressure guarantees stability under specified store-and-forward point queue assumptions and admissible demand; explicitly acknowledges infinite link storage restriction and finite-link blocking / de-facto red.
- Harth et al. (2022), DOI 10.52825/scp.v2i.120: SUMO calibration against actual detector and signal observations; 75 mapped intersections, 18 requiring manual map repairs; 210/529 detectors manually reassigned; green-share median error 1.6–1.9%; demand median absolute count error 13–18% accounting for clearing period.
- Ma et al. (2021), DOI 10.3390/app11062584: publicly available geographic population data drive SUMO ActivityGen; transport hot spots around stations/hospitals are not accurately captured by population alone.
- Hallmark et al. (2010), DOI 10.3141/2182-18: two corridor VISSIM cases; roundabout does not demonstrate strong corridor benefit over optimized signals with turn-lanes in studied settings; platoon dispersion can matter; avoid generalizing beyond scenarios.
- Xiong et al. (2026), DOI 10.1049/itr2.70296: mechanism-based survey of multi-agent signal coordination; reward/information/policy/temporal coupling categories, local-vs-global and spillback failure modes. EPUB source retained, no PDF fabricated.

## Scientific next steps
Question: When and why can a locally optimized signal policy worsen a finite-storage corridor network? Establish exact 2-3 junction benchmark with conserved OD vehicle paths, link-level receiving constraints, fixed arrival streams and movement-level logs. Compare fixed-time, offset coordination and max pressure. Separately validate simulator with independent SUMO and observed data before real-world optimization claims.

## Pending
Taglieri et al. (2024) roundabout network comparison, DOI 10.1177/03611981231192093: NOT in verified 2026-11-02 five-item intake. Keep as missing/hold, not counted ingested.

No GitHub Actions, no github-actions[bot].
