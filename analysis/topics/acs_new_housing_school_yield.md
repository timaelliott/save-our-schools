# Public-school students in newly built 2-4 bedroom homes (ACS PUMS, Portland tri-county)

**Question.** In Multnomah, Washington and Clackamas counties, how many public-school children aged 5-17 live in newly built 2-4 bedroom homes?

## Data and method

**Source.** ACS 1-year Public Use Microdata Sample (PUMS), Oregon housing and person files for survey years 2019, 2021, 2022, 2023 and 2024. The originals are archived in `sources/census/acs_pums/`, with the URL, fetch time and checksum in `_manifest.json`.
- The Census Bureau released no standard 1-year file for 2020; its experimental 2020 file isn't distributed with the other years.
- PUMS areas (PUMAs) are assigned to counties with the Census tract-to-PUMA files. Every PUMA in these counties sits inside one county, so the county totals are exact.

**Definitions.**
- **Newly built:** structure first built in the survey year or the year before. For example, the 2024 survey counts homes built in 2023-24, and the 2019 survey homes built in 2018-19.
- **Units:** housing units with 2-4 bedrooms, including vacant units.
- **Students:** residents aged 5-17 enrolled in public school (ACS `SCH=2`). This includes charter schools and any district, not just PPS.

**Margins of error.** 90% margins come from the ACS's 80 replicate weights. Code: `analysis/topics/_build/acs_new_housing_school_yield.py` (run it with `WINDOW=3` for the three-year version).

**Outputs.**
- `analysis/data/acs_new_housing_school_yield.csv` (two-year window)
- `analysis/data/acs_new_housing_school_yield_3yr.csv` (three-year window)

**Sample size.** This is the main limitation. Across all five surveys only 192 newly built 2-4 bedroom homes fall in the sample (two-year window), so single-year and county-level figures are rough.

## Results: two-year window, five surveys pooled (students per unit ± 90% margin)

| Group | Sampled homes | Est. units | Public students 5-17 | Students per unit | Students per occupied unit |
|---|---|---|---|---|---|
| All new 2-4 BR homes | 192 | 23,622 | 5,769 | **0.24 ± 0.11** | 0.29 |
| 2 bedrooms | 49 | 6,934 | 272 | 0.04 ± 0.05 | 0.05 |
| 3 bedrooms | 76 | 8,446 | 1,577 | 0.19 ± 0.10 | 0.22 |
| 4 bedrooms | 67 | 8,242 | 3,920 | 0.48 ± 0.24 | 0.54 |
| Single-family detached, all 2-4 BR | 127 | 15,612 | 5,031 | 0.32 ± 0.15 | 0.36 |
| Single-family detached, 3-4 BR | 112 | 13,446 | 4,759 | **0.35 ± 0.18** | |
| Single-family detached, 4 BR | 63 | 7,731 | 3,804 | **0.49 ± 0.25** | |
| Townhome (attached) | 25 | 2,702 | 486 | 0.18 ± 0.18 | 0.20 |
| 5+ unit apartment building | 25 | 3,998 | 0 | 0.00 (no sampled children) | |
| Owner-occupied | 141 | 15,365 | 5,334 | 0.35 ± 0.15 | |
| Renter-occupied | 36 | 4,867 | 435 | 0.09 ± 0.10 | |
| Washington County | 71 | 8,566 | 3,147 | 0.37 ± 0.22 | 0.40 |
| Clackamas County | 61 | 7,582 | 1,405 | 0.19 ± 0.15 | 0.25 |
| Multnomah County | 60 | 7,474 | 1,217 | 0.16 ± 0.10 | 0.19 |

## By survey year (all new 2-4 BR homes, all three counties)

| Survey | Built | Sampled homes | Est. units | Public students 5-17 | Students per unit |
|---|---|---|---|---|---|
| 2019 | 2018-19 | 41 | 4,372 ± 1,446 | 1,239 ± 1,005 | 0.28 ± 0.21 |
| 2021 | 2020-21 | 41 | 3,580 ± 967 | 1,547 ± 1,119 | 0.43 ± 0.27 |
| 2022 | 2021-22 | 39 | 4,975 ± 1,275 | 749 ± 570 | 0.15 ± 0.12 |
| 2023 | 2022-23 | 31 | 3,866 ± 1,271 | 869 ± 711 | 0.23 ± 0.17 |
| 2024 | 2023-24 | 40 | 6,829 ± 2,204 | 1,365 ± 1,572 | 0.20 ± 0.23 |

Year-to-year swings are within the margins of error; none of the changes is statistically meaningful.

## Three-year window (more sample)

The 2021 file groups 2010-2019 together, so the three-year window adds nothing for 2021. For the other surveys it adds one more build year.

- All new 2-4 BR homes: 0.29 ± 0.08 (340 sampled homes).
- Single-family detached, 3-4 BR: 0.36 ± 0.13.
- Single-family detached, 4 BR: 0.44 ± 0.16.
- Townhomes: 0.23 ± 0.15.
- Apartments, 2 BR: 0.07 ± 0.07.

## How this compares with PSU's own figures

PSU ran a version of this analysis for its 2026-27 PPS forecast. Its Table 2.6 says: "Pooled sample of Multnomah, Washington, and Clackamas counties; (a) buildings less than 5 years old and students age 5–17 in any public school" [PPS:pps_net/data-and-reporting/2026-27/psu_prc_enrollment_forecast_2026-27_to_2035-36.pdf p.16](https://www.pps.net/fs/resource-manager/view/8f9d62cd-5056-4cdc-8435-4bcba8ba86b1#page=16). PSU's yields per unit:

| Housing type | Yield per unit |
|---|---|
| Single family | 0.45 |
| Multi-family, studio/1-BR | 0.04 |
| Multi-family, 2-BR | 0.26 |
| Multi-family, 3+ BR | 0.72 |
| Affordable multi-family, 3+ BR | 0.91 |

PSU's earlier figures:
- The 2014-15 report: 0.47 "in homes built since 2003 on lots larger than 2,750 square feet" [PPS:pps_net/data-archives/2014-15/psu_prc_enrollment_forecast_2014-15.pdf p.8](https://www.pps.net/fs/resource-manager/view/7b6aeb58-e420-4c8a-81ba-3a8d6a075262#page=8).
- The 2007-08 report: "newer multiple family homes of 0.09 per unit" [PPS:psu_prc/psu_prc_enrollment_forecast_2007-08_base_oct2006.pdf.txt L2356].

Analysis:
1. This replication uses a stricter age cutoff (two years instead of PSU's five). It puts new detached 3-4 bedroom homes at about 0.35 public-school students per home (0.36 with three years of builds) and 4-bedroom homes at 0.44-0.49. Both overlap PSU's 0.45 single-family rate within the margin of error.
2. The 0.09 figure is PSU's rate for newer multi-family homes. It is about a quarter of the detached-home rate found here, and a fifth of PSU's own current single-family rate.
3. The apartment figures here (2 BR about 0.07 with three years of builds) come in below PSU's 0.26 for 2-bedroom multi-family. The apartment sample is small (49 sampled units).
4. These homes are measured within two years of construction, so households that move in before having school-age children aren't counted yet. Yields usually rise as a subdivision ages, so treat these as a floor.
5. Renters and Multnomah County show lower yields, but both are dominated by small units and apartments.
