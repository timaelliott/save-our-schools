# Which years PSU most likely used for Maplewood's grade progression ratios (2026-27 forecast)

Compiled 2026-11-04. Analysis throughout unless a PSU quotation is cited. Scripts: session scratchpad `win/win.py` (re-runnable from `analysis/data/psu_forecast_vs_actual_by_school.csv`-era inputs: PPS October counts 2016-2025 and PSU's 2026-27 school forecasts).

## What PSU says
- School GPRs: "the individual schools generally rely on longer-run averages with the COVID years removed"; district GPRs "use the prior 3-year averages"; district kindergarten capture converges "toward the pre-COVID 10-year average" [PPS:pps_net/data-and-reporting/2026-27/psu_prc_enrollment_forecast_2026-27_to_2035-36.pdf p.24].
- School kindergarten is "a share of the total district-wide kindergarten enrollment" for most schools [same, p.23]; schools are then reconciled to district totals by "adjusting school-level capture rates at kindergarten and GPRs" [same, p.24].
- The historical dataset runs 2016 to 2025 [same, p.19]. No school-level window length is stated.

## Test 1: which window reproduces PSU across schools
Method: for 15 K-5 schools with no 2016-2025 boundary, program or grade changes and no new affordable housing in PSU Table 2.7, rerun PSU's method from the October 2025 counts with each candidate GPR window (grade-specific averages) and a kindergarten share of district K, fitting one reconciliation factor on K per school; compare to PSU's published 2026-2035 forecast.

| GPR window (year-to-year changes) | Median error across 15 schools (students/yr, RMSE) | Maplewood error | Maplewood avg GPR |
|---|---|---|---|
| 2017→18, 2018→19, 2022→23, 2023→24, 2024→25 | **2.1** | **1.2** | **1.005** |
| same plus 2016→17 | 2.1 | 1.2 | 1.001 |
| 2017-19 plus 2021→22 through 2024→25 | 2.3 | 2.1 | 1.021 |
| 2016-19 only (pre-COVID) | 2.8 | 2.3 | 0.980 |
| Last 3 (2022→23 to 2024→25) | 3.0 | 2.5 | 1.023 |
| Post-COVID 2021→22 to 2024→25 | 4.3 | 4.5 | 1.043 |
| Last year only (2024→25) | 3.9 | 1.1 | 1.005 |

Windows that include 2017-2019 and leave out 2021→22 fit best across schools. The last-year-only window fits Maplewood by coincidence (2024→25 happened to be 1.005) but fits the other schools poorly.

## Test 2: the kindergarten each window would require for Maplewood
PSU forecasts 288 for fall 2026. Grades 1-5 in 2026 are last year's K-4 times the GPRs, so 288 minus that total is the kindergarten PSU must have assumed. Maplewood's K share method (2023-2025 average share × PSU's district K of 2,969) gives about 43.

| GPR window | Grades 1-5 in fall 2026 | Implied fall 2026 K | Share of district K |
|---|---|---|---|
| 2017-19 + 2022-25 | 244.5 | **43.5** | 1.46% |
| Last 3 years | 248.3 | 39.7 | 1.34% |
| Post-COVID 2021-25 | 253.4 | **34.6** | 1.17% |

With post-COVID GPRs, PSU would have to have assumed about 35 kindergartners, fewer than in any year since at least 2016 (range 36-70) and well below Maplewood's recent 1.27%-1.78% shares. With the 2017-19 + 2022-25 window, the implied 43.5 matches the share method almost exactly.

## Conclusion (Analysis)
- It is very likely that PSU's Maplewood GPRs include 2017→18 and 2018→19, the first years after the 2016 boundary change, when Maplewood's classes shrank (0.999 and 0.955). The window that best fits is 2017→18, 2018→19, 2022→23, 2023→24, 2024→25, i.e. data from 2017 through 2025 with 2019-2022 removed, matching PSU's stated dataset and "COVID years removed".
- Those two pre-COVID years pull Maplewood's average from about 1.023 (2022-2025) to about 1.005. Grade-specific: K→1 1.014, 1→2 0.976, 2→3 1.010, 3→4 1.007, 4→5 1.015, held constant for ten years.
- Whether 2016→17 is also included cannot be told apart (fits are identical); PSU's "2016 to 2025" dataset would allow it.
- Limits: the kindergarten share window cannot be identified (the reconciliation factor absorbs it); PSU may also adjust GPRs in reconciliation; PSU says it splits history for boundary changes, but nothing suggests the 2016 phase-in effects on Maplewood's own counts were removed.
