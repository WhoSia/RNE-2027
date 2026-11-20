# Sensor provenance and commitment time
A proposed report has source kind, issuance time, delivery time, target time, error bound and (optional) acquisition cost. A sensor reading of an event occurring **after** the signal commitment cannot be used for that commitment; a forecast about that event can be used only if its inputs are causally available, its issue time is before commitment and the reporting latency ends before commitment.

Time-stamped reports are necessary but not sufficient to establish provenance: the forecast feature pipeline must not read realized future arrivals, future accepted lane changes, or labels assigned retrospectively. A missing provenance audit makes a report *inadmissible*, even with a favorable timestamp.

For two hypothetical sources, compute all four feasible subsets: nothing; structural mode; arrival forecast; both. For each affordable subset use the same robust finite-world regret objective and choose minimum risk + cost. Reject late, retrospective, insufficiently attested or budget-exceeding sources. If all sources fail, the no-information randomized policy is the lawful fallback.

This is a **research-time gate only**. It does not authorize any actual traffic signal intervention, and the two sources do not yet exist as live deployed detectors.
