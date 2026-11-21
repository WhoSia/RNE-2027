# RF-CURTAIN — Dimensioned RF feasibility and first-Fresnel-zone gate

Date: 2026-11-21. **The following are wave-geometry calculations, NOT measured Wi-Fi detection results.**

For a link with endpoints separated by d and a point at distances d1 and
d2=d-d1, the approximate first-Fresnel-zone radius is
`r_1 = sqrt(lambda*d1*d2/(d1+d2))`, with `lambda=c/f`.
At the midpoint: `r_1 = 0.5*sqrt(lambda*d)`.
References:
- https://www.tegola.org.uk/howto/fresnel.html
- https://industrialwirelessio.com/tools/fresnel-zone-calculator/
- https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-guides/wifi-driver/wifi-vendor-features.html

With 2.4 GHz RF and a 1m transmitter–receiver link, the midpoint radius
is approximately **0.177m**; for 5 GHz it is approximately **0.122m**.
For a 4m link it increases to ~**0.354m** (2.4GHz). These scales are
not tiny compared with a reduced tabletop intersection.

## Critical disconfirming check

At 1:20 scale, two 3.5m-wide real-world lanes have tabletop center
spacing **0.175m**. Two nominal 2.4GHz/1m links centered on adjacent
lanes have midpoint first-zone radius sum **0.354m**, larger than that
center spacing. Their simple midpoint discs overlap.

**Therefore reject the naive exhibition claim that a pair of ordinary
2.4GHz tabletop Wi-Fi links automatically resolves two adjacent lanes.**
First-zone disc separation is a weak geometric plausibility heuristic
and is neither necessary nor sufficient for actual CSI discrimination;
multipath can cause correlated observations even when discs do not
overlap.

## Geometry-specific fallback

Place two **longitudinal** sensing sections, one at the pocket entrance
and another near the downstream receiving boundary, e.g. illustrative
centerlines 0.70m apart in a controlled tabletop, rather than promising
fine separation of side-by-side lanes. For two 1m/2.4GHz links,
midpoint disc radii sum to ~0.354m: the two midpoint discs do not
overlap in this illustrative arrangement.

This only reduces geometric ambiguity; vehicles near both sections,
antenna patterns, metal surfaces, multipath and changes in orientation
may still invalidate independent diagnosis. Measurement must prove
a physically distinguishable signature. No target detection threshold
is inferred from the Fresnel radius.

## Failure gates that terminate the radio claim

- No CSI-capable *owned* hardware or usable labeled vehicle RF dataset:
  restrict work to geometry and evidence review. Ordinary RSSI is a
  baseline, not CSI equivalence.
- Static obstruction cannot be discriminated from baseline drift
  under a new session/placement: do not promote 'detects traffic jam'.
- Out-of-placement class-level precision/recall fails the locked
  pilot: reject generalizable cause-of-blockage inference.
- A third-party device identifier or unconsented person data is needed:
  reject that acquisition design.
- A toy model vehicle blocks an RF path but not the equivalent scaled
  vehicle geometry: do not claim size-invariant physical transfer.
- Never put student-installed sensor equipment at a live
  intersection or wire into a public controller.

## Reproducible computation

`rf_link_geometry.py` and its unit tests are a small standalone
Fresnel geometry audit, not an RF propagation simulator.
Both actual RF calibration and synchronized ground-truth trials remain
**UNEXECUTED**.
