# T2 v6.9-P5b — horizon 630 versus 1200 seconds

Ran an additional 256 synthetic simulations on the same five-junction networks and eight heldout seeds, using four fixed policies × two demand profiles × two link capacities × two horizons. At 630s balanced with 18m link storage had only 0–2 of 8 completed per policy; upstream_peak with 18m had 0/8 per policy. With 1200s, all eight seeds completed for all four policies in every demand/storage cell.

In this limited sample priority_wave remained lowest average vehicle-seconds out of four at both horizons. Thus finite horizon censoring was substantively present but no rank inversion was found in this selected 4-plan comparison. We do not claim censoring never changes policy rankings or any real-road superiority. The raw CSV, summary, code and report have immutable separate derivative archive https://drive.google.com/file/d/1xEq85oCDHb_YZ6JBmSsiX3uiIaAlPqN0/view . No SUMO execution or real field validation.
