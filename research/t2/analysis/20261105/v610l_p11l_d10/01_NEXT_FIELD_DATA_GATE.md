# T2 D11 external-field acquisition gate

1. **FHWA InfoMaterials CPFM:** locate selectable 2026 friction/texture dataset, retrieve raw CSV/XLSX plus original URL, download timestamp, byte SHA256 and license. Determine instrument/measurement mode, position, speed, date, wetness and quality flags. The catalog confirms the dataset, **not yet a successful download**. https://infomaterials.fhwa.dot.gov/data
2. **FHWA LTPP MON_FRICTION:** acquire actual rows using InfoPave export/SDR, note Skid Number test definition and potential missing tire/device metadata; no direct equation SN -> effective tire mu. https://infopave.fhwa.dot.gov/Data/TableExport/
3. **Source-lane junction geometry:** acquire a byte-faithful original .xodr, independently parse and compare external esmini/SUMO geometry before empirical claims. Existing esmini source only inspected remotely.
4. **Utah SPaT:** expand observation duration, map signal groups to junction connections and join geo/UTC with suitable BSM records; do not infer friction or vehicle delays from SPaT alone.
5. **Calibration:** reserve held-out roads/sites/days, quantify instrument uncertainty and missingness. Only calibrate compatible target quantities after original record schemas verified.

Policy P12 stays frozen. No field-safety speed or traction guidance.
