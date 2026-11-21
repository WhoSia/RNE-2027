# RF07 — The viral 'Wi-Fi camera' source audit and a defensible exhibition translation

Date 2026-11-21. Search-level primary-code review only: no clone, no source-code execution, no firmware flashing, no hardware observations. These links identify public repositories, **not validated accuracy claims**.

## Open source chain
1. Espressif official reference: https://github.com/espressif/esp-csi — vendor-backed CSI application examples, including Wi-Fi sensing/presence workflows. This is the recommended first source for API/hardware scope, not a full camera reconstruction claim.
2. WiFi DensePose ecosystem: https://github.com/syntax-syndicate/wifi-densepose — ambitious visual output and proxy-ground-truth claims. Its README states a low camera-free pose PCK@20 number (~2.5% in a particular proxy-labelled evaluation) and notes camera-ground-truth work remains open. The figure is not a universal benchmark for Wi-Fi sensing. Animated 3D interfaces cannot substitute for held-out labels.
3. Another ESP32 lab data example: https://github.com/Tahmid-Mahmud-Fahim/esp32-based-presence-and-motion-detection-using-wifi-csi — reports open 2-transmitter/receiver-layout experimental captures. Its data labels are human motion, not traffic causal blockage; verify permissions and split before any use.
4. https://github.com/collabray/wisense — Python ESP32 CSI classification implementation; requires independent reproduction and provenance review.

## What is feasible to claim?
| Output | Evidence required |
|---|---|
| RSSI time-series display | RSSI readings only; cannot rename them CSI |
| CSI amplitude over subcarriers | Capability of owned hardware, own frame capture, repeatability |
| Tabletop movement detected | Independent synchronized truth and unseen-session error |
| Stationary obstruction diagnosed | Occupancy comparisons with empty state and position heldouts |
| Camera-like 3D object representation | Spatial independent ground truth, localization error and unseen layouts; NO current evidence |
| Change in real traffic signal performance | Realistic controller/action set, calibrated model and deployment approval; NOT allowed in this study |

## Strongest proposed demo
Transparent model intersection with two physically separated observation zones, cars manually labelled in fixed positions, an honest three-panel display: *actual recorded signal*; *uncertainty/UNRESOLVED*; *independent truth*. A 'Wi-Fi image' or voxel rendering should not be presented as a measured map unless calibrated against coordinates.

## Compliance
Test only with authorized school equipment and own transmissions under supervisor approval. Do not study passersby, monitor unrelated devices, collect MAC addresses or suggest that walls nullify consent. No public-road placement and no road signal actuation.
