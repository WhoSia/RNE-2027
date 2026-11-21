# RF08 — First-party ESP-CSI minimum laboratory demonstration gate

Date: 2026-11-21. Literature/code documentation review, **not an executed device study**.

## Technical source
Espressif `esp-csi` official README and get-started documentation:
- https://github.com/espressif/esp-csi
- https://github.com/espressif/esp-csi/blob/master/examples/get-started/README.md
- https://github.com/espressif/esp-csi/tree/master/examples/get-started/csi_recv

Espressif documents several compatible ESP32 family devices and a send/receive example that plots CSI subcarrier values in real time. The exact SoC, IDF version, toolchain, antenna configuration and licensed RF environment still need a **physical inventory** before claiming compatibility. Do not infer the exact user's hardware model.

## Exhibit-science claim ladder
1. Hardware returns CSI bytes from **team-owned lab communications** (not RSSI relabelled as CSI).
2. Frozen baseline packets and CSI subcarrier traces are plotted.
3. Independent labelled tabletop object motion versus empty contrast measured across repeated sessions.
4. Independent labelled *stationary occupancy* versus empty contrast measured across unseen placement.
5. Opposite traffic source classes (pocket vs downstream) under frozen holdout.
6. Only after success: empirical confusion matrix into T2 abstract observer interface.

Levels 1-3 **do not prove** 4-6. A graphic resembling an image is not a calibrated camera image.

## Lab gate
- Supervisor signoff, owned hardware, school network permission and isolated/private setup.
- Ground truth comes from manual placement labels, never from the same CSI features being evaluated.
- Freeze training/validation/holdout partitions by placement and session; do not tune hyperparameters on holdout.
- Report time delay, signal dropouts, false occupancy, per-class precision/recall and abstention.
- Compare cheaper optical/physical marker control at the **same task**; if it wins, preserve the negative result.
- No extra hardware purchase until available inventory is known.

No third-party device capture, bystander tracking, unauthorized networks, real road-side installation, or active traffic-signal connections. The separately downloaded ~5GB CIM dataset.zip stays on HOLD.
