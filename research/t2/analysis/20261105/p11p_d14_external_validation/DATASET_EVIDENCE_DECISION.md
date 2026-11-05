# P11-P / D14 — external evidence acquisition and validation gates
2026-11-05. Source-discovery snapshot. No new raw source bytes yet.

## Confirmed source portals
KR Jinju lane-level actuated-signal traffic counts: https://www.data.go.kr/data/15152135/fileData.do
KR Jinju link traffic API: https://bigdata.gyeongnam.go.kr/
KR national UTIC signal *plans*: https://www.utic.go.kr/guide/utisRefSig.do
KR Seoul historic lane counts: https://www.data.go.kr/data/15056899/openapi.do
US NGSIM highway and signalized intersections: https://data.transportation.gov/Automobiles/Next-Generation-Simulation-NGSIM-Vehicle-Trajector/8ect-6jqj/data
Germany inD intersection tracks + OpenDRIVE maps: https://levelxdata.com/ind-dataset/
Greece pNEUMA trajectories: https://open-traffic.epfl.ch/
Multiple nations INTERACTION: https://interaction-dataset.com/about/
US Argoverse2: https://www.argoverse.org/av2.html
US Waymo Open: https://www.waymo.com/open/about/
ASAM OpenDRIVE: https://www.asam.net/standards/detail/opendrive/
Michigan MARWIS: https://github.com/AD-Assurance-Lab/dataset--winter-driving--main
Denmark LiRA-CD: https://doi.org/10.11583/dtu.23096600.v1

## Ranking by *falsifiability*, not feature count
Tier I (immediate): Jinju lane counts (traffic count/queue) + NGSIM signalized intersections (car-following/turn trajectories) + inD tracks/maps (geometry). Execute independent fixed splits and baselines.
Tier II: UTIC program/map metadata to define controllers (not observed phase transitions); Seoul independent counts.
Tier III: pNEUMA, INTERACTION, Argoverse, Waymo for rare interactions; MARWIS/LiRA-CD for sensor clocks only.

## Acceptance test per dataset
Official provenance; file byte SHA256; license; raw unit definitions; UTC/local timestamp mapping; map CRS; missingness; train/dev/test split by day/site/recording; strong baseline; independent source; failure witness; versioned receipt.
Do not conflate occupancy, departures and latent arrivals. Nominal signal plans are not live signal-state logs. Images/frames are not independent friction measurements.
No SUMO or genuine policy experiment reported for D14; optimizer remains frozen.
