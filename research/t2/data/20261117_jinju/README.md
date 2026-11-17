# Jinju actuated-signal lane-count public sample

Provider metadata: https://www.data.go.kr/data/15152135/fileData.do

Public download linked by the portal:
https://www.data.go.kr/cmm/cmm/fileDownload.do?atchFileId=FILE_000000003523838&fileDetailSn=1

Raw SHA-256: `0df7079720916706f2de64c8b0cb3d671c69bd39df901b0516a56de5b21ed412`.

The file has 10,000 CP949 rows and 74 location labels. It delivers exactly
1,000 rows per start date over 2025-11-01 to 2025-11-10. 9,127 rows start between
00:00 and 00:59 as written in the file. Nine dates have no starts at or after
01:00. The broad catalogue dates therefore do not describe this file's useful
daypart coverage. Elapsed end minus start varies from zero to 21,425 seconds.
Retain the recorded interval rather than treating it as a regular bin.

The six per-lane observation counts follow the provider order (through, left,
right, U-turn, residual, waiting), followed by a seven-element vehicle class
vector in a separate column. Do not sum the last two slots as passing volume.
The meaning of the clock and the location/direction/lane/controller crosswalk
must be confirmed before phase-resolved replay. There are 10 excess exact
parsed rows and 231 excess rows on the site-label/start/end key. Preserve
nonidentical collisions and require additional identifiers to resolve them.

## Count-compatible demonstration

Select a lane record with through=1, left=1, and all other movement/queue
slots zero, exactly a 14-second recorded elapsed interval, class and flow
counts agreeing, and a site/time key that occurs once. Prefer the site with
the most source rows among eligible records, then earliest start, then lane
index. This deterministic rule selects a small count example before signal
outcomes are computed.

For illustration, interpret only the selected pair of counts as a hypothetical
input of one through and one left arrival. Enumerate independent arrival ticks
within a synthetic 14-tick window starting at tick 0, 8 or 26; enumerate both
arrival orders for same-tick ties. Evaluate the protected leading and lagging
plans on every sequence. The window length and counts use the sample; the
arrival interpretation, within-window order and signal clock are synthetic.
The result is an identifiability demonstration conditional on those assumptions,
without a calibrated or estimated signal effect for that site.

Compatible sequences distinguish aggregate counts from unknown event times.
For real observations, request full day coverage, approach or camera IDs,
physical lane geometry and actual signal transition logs. If counts are
departures, measure arrivals separately or model their compatible set.
