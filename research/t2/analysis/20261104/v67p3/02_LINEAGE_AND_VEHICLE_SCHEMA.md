# P3 source and vehicle contract provenance

The full Drive reproducibility archive preserves historical source P1a network_v67.py and P1b network_v67_p1.py in separate legacy folders. P3 network_v67_p3.py is a deterministic transformation of the P1b code using build_p3.py; P1a sources are never overwritten.

VehicleSpec remains P1b physics: car 4.5m long, 1.8m wide, 2m gap, accel1.5m/s2, brake3m/s2, headway1.3s; truck 11m long, 2.5m wide, 3m gap, accel0.95m/s2, brake2.2m/s2, headway1.9s. Both class-dependent footprints and headways influence IDM, geometric SAT, connector clearance and downstream receiving storage.

Historical P1a has different truck length and IDM/timeline/admission semantics. A-vs-P3 traffic output is not an isolated single-factor physical comparison. B-vs-P3 with no WALK is the clean regression check.