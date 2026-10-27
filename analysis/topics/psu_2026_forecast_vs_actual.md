# PSU's 2026-27 forecast vs. PPS's official Oct 1, 2026 enrollment

Compiled 2026-10-27, the day PPS posted official Oct 1, 2026 enrollment.

**Sources**
- **Actuals:** PPS "2026-2027 October 1st Enrollment" by grade and program [PPS:pps_net/data-and-reporting/2026-27/enrollment_by_grade_and_program_type.pdf p.1](https://github.com/timaelliott/save-our-schools/blob/main/sources/pps_net/data-and-reporting/2026-27/enrollment_by_grade_and_program_type.pdf).
- **Forecasts:** PSU Population Research Center, *Enrollment Forecasts 2026-27 to 2035-36*, Table 5.5. Its 2025-26 column is the historic count and its 2026-27 column is the one-year-ahead forecast [PPS:pps_net/data-and-reporting/2026-27/psu_prc_enrollment_forecast_2026-27_to_2035-36.pdf p.39](https://www.pps.net/fs/resource-manager/view/8f9d62cd-5056-4cdc-8435-4bcba8ba86b1#page=39).
- **Data file:** every school is in [`../data/psu_2026-27_forecast_vs_oct1_2026_actual.csv`](../data/psu_2026-27_forecast_vs_oct1_2026_actual.csv), which adds each school's Scenario A and B action from `school_impact.csv`.

## District picture

PSU forecast 39,463 students in the 82 schools that appear in both documents. Oct 1 came in at 39,059, 404 below the forecast (−1.0%).

| Level | Schools | PSU forecast | Oct 1 actual | Schools above forecast |
|---|---|---|---|---|
| Elementary (K-5) | 45 | 14,086 | 13,819 | 15 |
| K-8 | 11 | 4,688 | 4,584 | 5 |
| Middle | 15 | 7,280 | 7,373 | 9 |
| High | 9 | 12,828 | 12,686 | 3 |

Elementary enrollment in these schools fell by 507 from 2025-26 to 2026-27.

## Schools proposed for closure

Ten of the 14 schools proposed for closure came in below forecast, and four came in above.

| School | PSU forecast | Oct 1 actual | Actual − forecast | Scenario A | Scenario B |
|---|---|---|---|---|---|
| Creston | 199 | 222 | +23 | close | close |
| **Maplewood** | **288** | **304** | **+16** | close | close |
| Stephenson | 267 | 280 | +13 | close | stays open |
| Irvington | 249 | 259 | +10 | close | close |
| Lewis | 243 | 241 | −2 | close | stays open (receives students) |
| Sellwood MS | 537 | 532 | −5 | close | close |
| Rose City Park | 398 | 393 | −5 | close | stays open |
| Marysville | 294 | 282 | −12 | close | close |
| James John | 361 | 347 | −14 | close | close |
| Woodmere | 222 | 206 | −16 | close | close |
| Beach | 285 | 269 | −16 | close | close |
| Sabin | 258 | 236 | −22 | close | close |
| Buckman | 263 | 239 | −24 | close | close |
| Peninsula | 252 | 220 | −32 | close | close |

## Southwest (Wells cluster) elementaries

| School | Oct 2025 | PSU forecast 2026-27 | Oct 1, 2026 actual | Actual − forecast | Change since last year | Plan (A / B) |
|---|---|---|---|---|---|---|
| **Maplewood** | 287 | 288 | **304** | **+16** | **+17** | close / close |
| Markham | 339 | 325 | 336 | +11 | −3 | receives Stephenson / no change |
| Stephenson | 281 | 267 | 280 | +13 | −1 | close / stays open |
| Hayhurst | 290 | 283 | 286 | +3 | −4 | receives 70% of Maplewood (both) |
| Rieke | 264 | 255 | 254 | −1 | −10 | receives 30% of Maplewood (both) |
| Chapman | 330 | 336 | 319 | −17 | −11 | no change |
| Capitol Hill | 325 | 319 | 291 | −28 | −34 | receives Stephenson / no change |
| Bridlemile | 423 | 413 | 383 | −30 | −40 | no change |
| Ainsworth | 560 | 555 | 527 | −28 | −33 | no change |
| Forest Park | 264 | 259 | 234 | −25 | −30 | no change |

**Analysis:**
- Maplewood is the only Wells-cluster elementary that grew this year (+17). It is now larger than both of the schools that would absorb it, Hayhurst (286) and Rieke (254).
- PPS's Oct 6 rationale chose to keep Rieke and Hayhurst open over Maplewood [YT:zOUH2Jq7Owo@2:22:55](https://www.youtube.com/watch?v=zOUH2Jq7Owo&t=8575s). On this year's count, Maplewood is the biggest of the three.

## Maplewood: every PSU forecast of its 2026-27 enrollment

| PSU edition | Forecast for 2026-27 | Oct 1, 2026 actual | Actual − forecast |
|---|---|---|---|
| 2021-22 | 327 | 304 | −23 |
| 2022-23 | 253 | 304 | +51 |
| 2023-24 | 282 | 304 | +22 |
| 2024-25 | 291 | 304 | +13 |
| 2025-26 | 292 | 304 | +12 |
| 2026-27 | 288 | 304 | +16 |

**Analysis:**
- In each of the five most recent editions, PSU forecast Maplewood below what actually enrolled.
- The 2026-27 edition is the forecast behind PPS's statement that Maplewood was "expected to drop to 247" [PPS:pps_net/rightsizing/school_impact/maplewood.pdf p.3](https://drive.google.com/open?id=1JYIeqmstLm-IlaORhxbO1Wcz9z4Q4beC&usp=drive_copy).
- Earlier forecasts come from `analysis/data/psu_forecast_vs_actual_by_school.csv`, which cites each edition's PDF page.
