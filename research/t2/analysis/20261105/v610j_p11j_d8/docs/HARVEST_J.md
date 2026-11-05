# J literature Harvest — analysis, not another custody move

All eight D7 source PDFs are now canonical in `10_PAPERS` with unchanged IDs. This research unit does not re-upload or duplicate them.

- **Schwab & Kolbe (2022)**: checks explicit OpenDRIVE lane geometries and topology across 99 datasets; an existing peer-reviewed baseline. We must not advertise 'detected lane seams' as new. Need reproducing their actual dataset/threshold/annotation protocol first.
- **Meek & Walton (1992)**: boundary constraints separate position, orientation and curvature. Current J checks position and orientation only at a declared seam; curvature continuity is not yet certified.
- **Hasan (2014)**: design comfort depends on speed, jerk, banking and related quantities. J's 3D seam geometry cannot certify road safety or driver comfort.
- **Frego (2022)**: arbitrary space-curve torsion is a separate mathematical variable; our 2D spiral plus elevation/roll is not the Frenet–Serret construction investigated there.

## Harvest evidence gap

Our earlier D7 texts were sourced from full PDF-extracted text. In this J run, we did not read or reproduce all internal tables, equations and case-study datasets in the papers. The next literature phase should extract precise experimental thresholds/benchmark dataset provenance and compare the J implementation under matched assumptions.
