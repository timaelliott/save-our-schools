# "Six Years of PSU projections" sheet: what it adds

## About the sheet

**Source.** A Google Sheet titled "Six Years of PSU projections", supplied by the repository owner on 2026-11-10 and archived as `sources/psu_prc/forecast_history_sheet/six_years_of_psu_projections_2026-11-10.xlsx`, with tab CSVs and `_manifest.json`. The sheet doesn't name its publisher. It matches the six-year forecast-history tool PPS staff announced on Nov 4 [YT:9kX3vnfRlvY@3:48:51](https://www.youtube.com/watch?v=9kX3vnfRlvY&t=13731s), but that isn't confirmed.

**Contents.** Two tabs:
- "6 years of PSU forecasts": every school's PSU forecasts and actuals from the 2021-22 through 2026-27 report editions (Report_Year 2021-2026), including October 2026 actuals.
- "Historical enrollment": PPS October enrollment by school, 1996-97 to 2025-26.

**Check against our own PSU table.** Our `analysis/data/psu_forecast_vs_actual_by_school.csv` was transcribed from the PSU PDFs. Of the 1,420 school-edition-year forecasts the two have in common, 1,410 match exactly. The 10 that don't:
- Beverly Cleary in the 2022-23 edition, where the sheet runs about 95 lower (perhaps one campus or program left out);
- five Bridger rows that read 0 in the sheet.

The sheet also adds horizons and editions our table lacks.

## Maplewood across PSU editions

**Forecast for fall 2026 (Oct 2026 actual: 304 [PPS:psu_prc/forecast_history_sheet/six_years_of_psu_projections_2026-11-10.xlsx#6 years of PSU forecasts!R11967])**

| PSU edition | 2021-22 | 2022-23 | 2023-24 | 2024-25 | 2025-26 | 2026-27 |
|---|---|---|---|---|---|---|
| Forecast | 327 | 253 | 282 | 291 | 292 | 288 [PPS:psu_prc/forecast_history_sheet/six_years_of_psu_projections_2026-11-10.xlsx#6 years of PSU forecasts!R7112] |

**Forecast for 2031-32, the year PPS tests against the 360 K-5 floor**

| School | 2022-23 | 2023-24 | 2024-25 | 2025-26 | 2026-27 | Change from 2025-26 to 2026-27 |
|---|---|---|---|---|---|---|
| Maplewood | 257 [PPS:psu_prc/forecast_history_sheet/six_years_of_psu_projections_2026-11-10.xlsx#6 years of PSU forecasts!R7137] | 270 [PPS:psu_prc/forecast_history_sheet/six_years_of_psu_projections_2026-11-10.xlsx#6 years of PSU forecasts!R7138] | 298 [PPS:psu_prc/forecast_history_sheet/six_years_of_psu_projections_2026-11-10.xlsx#6 years of PSU forecasts!R7139] | 291 [PPS:psu_prc/forecast_history_sheet/six_years_of_psu_projections_2026-11-10.xlsx#6 years of PSU forecasts!R7140] | **247** [PPS:psu_prc/forecast_history_sheet/six_years_of_psu_projections_2026-11-10.xlsx#6 years of PSU forecasts!R7141] | **−15%** |
| Hayhurst | 304 | 295 | 285 | 266 [PPS:psu_prc/forecast_history_sheet/six_years_of_psu_projections_2026-11-10.xlsx#6 years of PSU forecasts!R4683] | 266 [PPS:psu_prc/forecast_history_sheet/six_years_of_psu_projections_2026-11-10.xlsx#6 years of PSU forecasts!R4684] | 0% |
| Rieke | 279 | 246 | 239 | 261 [PPS:psu_prc/forecast_history_sheet/six_years_of_psu_projections_2026-11-10.xlsx#6 years of PSU forecasts!R8928] | **311** [PPS:psu_prc/forecast_history_sheet/six_years_of_psu_projections_2026-11-10.xlsx#6 years of PSU forecasts!R8929] | **+19%** |
| Markham | 391 | 436 | 332 | 314 | 347 | +11% |
| Stephenson | 295 | 273 | 287 | 235 | 261 | +11% |
| Capitol Hill | 297 | 326 | 345 | 279 | 311 | +11% |

Analysis:
- **The newest edition is the most pessimistic yet for Maplewood.** The 2026-27 edition, the one behind the rightsizing scenarios, cut Maplewood's 2031-32 forecast from 291 to 247. Among 48 elementary schools, only MLC (−31%) had a larger cut; Creston's was the same size. In the same edition, PSU raised Rieke's 2031-32 forecast by 19% and Markham, Stephenson and Capitol Hill's by about 11% each, and left Hayhurst's unchanged.
- **That edition is already off for Maplewood in its first year.** It forecast 288 for fall 2026; Maplewood enrolled 304. Every edition since 2022-23 has under-forecast Maplewood's fall 2026 enrollment. The 2022-23 edition missed by 51 students.
- **The floor test turns on these numbers.** Under the PPS modeling guide, Maplewood (247), Hayhurst (266) and Rieke (311) all fall below the 360 floor in 2031-32. Merging Maplewood into the other two lifts both above it (`analysis/topics/k8_scenario_modeling_guide.md`). With the previous edition's forecasts (Maplewood 291, Rieke 261, Hayhurst 266), Maplewood would not have been the smallest of the three. Rieke would have been.
- **This doesn't prove the cut is wrong.** PSU revises forecasts for many reasons. But the one-year swing happened in the edition that decided which of the three schools closes, and it runs against Maplewood's observed growth, the highest grade progression of 38 comparable schools (`analysis/data/k5_growth_gpr_2021_2026.csv`). That makes it a fair question for PSU and PPS: what changed in Maplewood's inputs between the 2025-26 and 2026-27 editions?

## PSU changed its school-level method between the two editions

| | 2025-26 edition | 2026-27 edition |
|---|---|---|
| Enrollment data used | "Data from 2018 through 2024" [PPS:pps_net/data-and-reporting/2025-26/psu_prc_enrollment_forecast_2025-26_to_2034-35.pdf p.24](https://www.pps.net/fs/resource-manager/view/e54facfd-a9b6-4637-9080-719dff12e382#page=24) | "Data from 2017 through 2025" [PPS:pps_net/data-and-reporting/2026-27/psu_prc_enrollment_forecast_2026-27_to_2035-36.pdf p.24](https://www.pps.net/fs/resource-manager/view/8f9d62cd-5056-4cdc-8435-4bcba8ba86b1#page=24) |
| School kindergarten intake | "a share of the applicable high school cluster forecast enrollment", reconciled to the cluster and then the district [PPS:pps_net/data-and-reporting/2025-26/psu_prc_enrollment_forecast_2025-26_to_2034-35.pdf p.23](https://www.pps.net/fs/resource-manager/view/e54facfd-a9b6-4637-9080-719dff12e382#page=23) | "a share of the total district-wide kindergarten enrollment" (local trends for some schools), reconciled directly to district totals [PPS:pps_net/data-and-reporting/2026-27/psu_prc_enrollment_forecast_2026-27_to_2035-36.pdf p.23](https://www.pps.net/fs/resource-manager/view/8f9d62cd-5056-4cdc-8435-4bcba8ba86b1#page=23) |
| School GPRs | capture rates and GPRs "projected based on an assumption of gradual convergence back to the pre-COVID 5-year average" [PPS:pps_net/data-and-reporting/2025-26/psu_prc_enrollment_forecast_2025-26_to_2034-35.pdf p.25](https://www.pps.net/fs/resource-manager/view/e54facfd-a9b6-4637-9080-719dff12e382#page=24) | "individual schools generally rely on longer-run averages with the COVID years removed" [PPS:pps_net/data-and-reporting/2026-27/psu_prc_enrollment_forecast_2026-27_to_2035-36.pdf p.24](https://www.pps.net/fs/resource-manager/view/8f9d62cd-5056-4cdc-8435-4bcba8ba86b1#page=24) |
| District GPRs | "weighted average of the last 3 post-COVID years, where the most recent year is assigned twice the weight" [PPS:pps_net/data-and-reporting/2025-26/psu_prc_enrollment_forecast_2025-26_to_2034-35.pdf p.34](https://www.pps.net/fs/resource-manager/view/e54facfd-a9b6-4637-9080-719dff12e382#page=31) | "the district-wide GPRs use the prior 3-year averages" [PPS:pps_net/data-and-reporting/2026-27/psu_prc_enrollment_forecast_2026-27_to_2035-36.pdf p.24](https://www.pps.net/fs/resource-manager/view/8f9d62cd-5056-4cdc-8435-4bcba8ba86b1#page=24) |

Analysis:
- Three things changed in the edition that cut Maplewood's 2031-32 forecast by 15% and raised Rieke's by 19%: the high-school-cluster step was dropped, the kindergarten-share basis changed, and the school GPR averaging changed.
- The published reports don't give school-level inputs, so the effect of each change can't be separated. Our earlier fit (`analysis/topics/psu_maplewood_gpr_window.md`) suggests the 2026-27 Maplewood GPRs average about 1.005, against an observed 1.040 for 2021-2026.
- **Questions for PSU:** Maplewood's GPRs and kindergarten share in each edition, and which years each average used.
