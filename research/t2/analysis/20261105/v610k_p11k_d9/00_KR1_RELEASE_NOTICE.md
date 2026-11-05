# T2 K.R1 canonical release (2026-11-05)

**Canonical immutable artifact:** https://drive.google.com/file/d/1swJFopohNOkzeKrEudJvLuQ4UzcyUyko/view

SHA256 `2b785769dded97c92957480336ed3389576c701b39ea29692c5b80ffe4d80536`, 48 archived files, CRC PASS, 150/150 tests; original P2 28/28 separately.

**Correction disclosure:** K initial branch source in `src/road_physics_bridge.py` has an exact planView seam selection problem, caused by selecting the preceding geometry at s precisely equal to the new geometry start. The authoritative K.R1 ZIP repairs this with right-continuous bisect-based piece selection. The regression test was updated in GitHub, but the corresponding GitHub source-file update was blocked by a safety check. Thus the GitHub branch **must not be treated as a runnable K.R1 release** until it matches the ZIP. Use only the Drive K.R1 archive for reproducibility. Original source history remains intact.

No actual field friction measured; OpenDRIVE source friction is application-dependent and not empirical tire grip; no policy run or SUMO run. This is not a real road safety certificate.
