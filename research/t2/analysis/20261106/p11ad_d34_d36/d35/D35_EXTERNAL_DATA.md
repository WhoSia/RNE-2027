# D35 — external evidence acquisition and SUMO run gate

- SUMO binary and `netconvert`: not present in this container. The standard package installation was attempted but pip found no matching release from the configured index; **NOT_EXECUTED**.
- Direct GitHub read: real winter road drive CSV at AD-Assurance-Lab/dataset--winter-driving--main (asphalt1) with 933 rows × 40 fields. Source SHA-1 `e7bae3751fae6aedfabd3328ef720ce6a4ca7390`. The data measures speed, location, temperature, friction sensors and driving variables; it **does not** represent signal occupancy/queue measurements. Source data is *not* redistributed; derived summary is preserved, raw license unverified.
- UTD19 official DOI `10.3929/ethz-b-000437802` and metadata/license were independently verified, but raw file was not obtained. 3–5min aggregates cannot independently validate microscopic exact timestamps.
- No real GTFS operating agency feed was downloaded; published illustrative GTFS feed is non-empirical.

**Blocking evidence gates:** matching road length, lane geometry, vehicle class/route, start time, signal legality; verified SUMO binary version and tripinfo raw; independently observed queues or trajectories; train/holdout split across days and sites. Marked as NOT_DONE.
