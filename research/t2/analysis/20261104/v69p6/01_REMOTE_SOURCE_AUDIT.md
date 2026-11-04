# P6: Bologna–Pasubio remote XML structural audit

Read upstream text through the connected GitHub repository, not raw local files. 8 controllers; cycles (seconds): 218=90, 219=123, 220=90, 230=125, 231=96, 232=90, 233=111, 282=63. Network XML: 491 lane elements, 351 edge elements, 571 connection elements. Each controller's signal-state string length agrees with the network connection's linkIndex set 0..N-1 (N=20,28,6,18,44,13,12,12). Detector XML: 67 text matches, 3 commented, 64 active, all active detector lanes and positions valid, sampling frequency 1800 seconds. Structural validations, not traffic predictions.

Upstream: https://github.com/DLR-TS/sumo-scenarios/tree/main/bologna/pasubio

P6 code, nine tests, JSON evidence, source-blob SHA list: shared-drive ZIP https://drive.google.com/file/d/1IsVCzQsNr-YMuhhqKwyIokJruRZCKi1t/view . No full raw XML snapshot yet. No SUMO run or field validation.
