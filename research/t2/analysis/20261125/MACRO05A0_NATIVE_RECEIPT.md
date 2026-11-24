# Independent native audit
Python 3.13.5, 108 runs, 256 snapshots. Local source git blob efe67dc41c1e7565b9a46317371b61181ab59fe9, local JSON blob 30d801bb0dd8d49584ca909d43dbab8c547222fb. Remote source exact match. Native totals, grid differences and snapshot sign counts match JS. Native audit does not rerun 18 JS empty/ring controls or compare each trajectory.
```json
{
  "totals": [
    7428,
    7219,
    7116
  ],
  "diffs": [
    {
      "signed": 312,
      "absolute": 312,
      "maxAbs": 18,
      "positive": 26,
      "negative": 0,
      "tie": 10
    },
    {
      "signed": 103,
      "absolute": 103,
      "maxAbs": 6,
      "positive": 26,
      "negative": 0,
      "tie": 10
    }
  ],
  "snap": [
    [
      190,
      15,
      51
    ],
    [
      160,
      96,
      0
    ]
  ]
}
```
