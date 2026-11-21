# RF-CURTAIN — Five physically distinguishable tabletop conditions

This is a **research apparatus design**, not a report of built or
tested Wi-Fi hardware. All measurements, if later attempted, must
use school-approved equipment and an indoor authorized setting.

## Scaled junction layout, schematic only

                        straight flow
             left-turn-pocket entrance          receiving link
                      section P                   section D
   demand ---> [ upstream A ] ---- [ stopline ] ----- [ downstream ]
                     ║   ║                           ║   ║
                     TX  RX                          TX  RX
                    link P                          link D

(Separate RF link geometry is conceptual. Neither link is proven
selective for its named physical region; RSSI/CSI footprints can
overlap through multipath. Two distinct channels/transceivers may
be required depending on the hardware and packet acquisition.)

Two longitudinally separated *radio observation sections*, not
two adjacent lane-imaging pixels. The actual project must verify
whether a change in section P can be distinguished from a change
in D. At a 1m/2.4GHz illustrative link, first-Fresnel midpoint
radius is ~0.177m; the simple 0.70m longitudinal separation
avoids overlap of the two midpoint discs. This does NOT certify
independent CSI signatures.

## Ground-truth labels before RF processing

- no_demand: empty approach and no inbound model car
- free: one or more model cars traverse the observed path freely
- pocket: static model-car obstruction at the pocket entrance,
  downstream clear
- downstream: receiving section blocked, pocket entrance clear
- both: both model sectors blocked

A 'pocket' toy blockage is an imposed condition, not proof that
real drivers would be trapped by a full turn bay. A 'downstream'
toy blockage is not measured road spillback. On prototype version 1,
do not infer route choice or actual stopline discharge from RF data.

For each independently reset trial, record setup-session ID, mounting
placement, class, number/material/position of toy objects, radio
quality/missingness and independent manual truth labels. To avoid
label leakage, commit the trial-condition schedule before looking
at any radio signal features. Do not include person names or
identifiable video. Report uncertain labels as ineligible for
training, not cherry-picked easy cases.

## Non-negotiable controls

1. Static same-material object in two physical zones separately:
   does RF respond to *where*, not merely the total metal volume?
2. Object absent, but apparatus or transmitters moved:
   false occupancy from channel drift.
3. Object held stationary after movement:
   movement detector does not imply stationary congestion detector.
4. Two objects simultaneously:
   does 'both' collapse into 'pocket' or 'downstream'?
5. One link lost:
   does the classifier abstain, or confidently hallucinate a cause?
6. Orientation and reflective-wall change:
   does a new placement destroy the learned pattern?
7. Blind holdout labels and **entire session/placement** exclusion:
   avoid randomly splitting adjacent CSI packets from the same event.

## Low-cost decision path

First inventory institutional equipment; no purchase is required to
run the geometry/code audit. If suitable CSI hardware is unavailable,
there is NO claim of an RF sensor. An existing Wi-Fi RSSI link can
be used solely as a weaker baseline and should not be relabeled CSI.

The apparatus may show an LED/display explaining hypothetical signal
decisions, but never connects to a public traffic controller.
Only classroom models and abstract computer displays are in scope.
