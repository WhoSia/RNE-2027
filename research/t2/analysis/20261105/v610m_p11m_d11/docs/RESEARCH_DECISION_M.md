# T2 v6.10-M / P11-M / D11 — Research decision (2026-11-05)

**GO, geometric research:** a varying planar lane-center offset `t(s)` requires `t'(s)`, `t''(s)`, reference-line signed curvature `k(s)` and `k'(s)`. Define `a=1-t*k`, `b=t'`, `r_lane'=a*T+b*N`. Then

`k_lane = [a^2*k + a*t'' + 2*(t')^2*k + t*t'*k']/(a^2+(t')^2)^(3/2)`.

This reduces to `k/(1-t*k)` for constant `t` on a regular curve where `1-t*k>0`. It is a local 2D offset-curve identity, not full 3D road curvature, vehicle motion, road grip or safe speed. Cusp/reversal => UNKNOWN, missing lane geometry => UNKNOWN, banked/nonplanar => UNKNOWN.

**Independent mathematical check:** 4 synthetic geometries (arc+variable cubic offset, spiral+variable quadratic offset, line+quadratic offset, arc+constant offset) evaluated using an independent sampled XY central-difference method at h=0.002m. Max discrepancy ~1.6141e-9 1/m. This compares two algorithms applied to the same synthetic geometry, not independent field truth.

**Test gate:** inherited 173 L tests plus 15 new differential geometry tests = 188/188 pass. Original v6.9-P2 regression suite 28/28 pass separately. No policy optimizer run. Source L and K.R1 ZIPs are retained unchanged.

**Field contact:** FHWA LTPP and CPFM catalog remains confirmed; zero instrument measurement rows. NEW: DTU LiRA-CD friction test, official article 23096600, DOI 10.11583/DTU.23096600.v1, publisher API reports two CSV file ids 41205782/41205785 and official MD5s. An HTTP 200 CSV endpoint did not yield accessible file bytes via scrape (binary content); do NOT claim the CSV was downloaded or checksum verified. Road-friction data acquisition gate remains HOLD.

**Priority next:** obtain file bytes via an authenticated/public download path respecting access restrictions and copyright; then SHA256/MD5 compare, inspect units/device/row granularity, split calibration and held-out roads; expand to 3D lane differential geometry and quality-controlled sensor matching. Maintain P12 policy freeze.
