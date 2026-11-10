# PPS K-8 scenario modeling technical guide (Oct 2026): what it says, and what it means for the Southwest package

Source: "K–8 Rightsizing & Consolidation Scenario Modeling | Technical Documentation", 62 pages. It is linked from the rightsize scenarios page and was archived on 2026-11-10 at `sources/pps_net/rightsizing/methodology/k8_scenario_modeling_technical_guide_2026-10.pdf`. The guide does not name any school except in worked examples.

## What the guide says

- **Two models.** An enrollment model applies each scenario's rules to PSU's forecast through 2035-36. A demographic model places each current student under each scenario. Both read the same boundary work [PPS:pps_net/rightsizing/methodology/k8_scenario_modeling_technical_guide_2026-10.pdf p.2](https://github.com/timaelliott/save-our-schools/blob/main/sources/pps_net/rightsizing/methodology/k8_scenario_modeling_technical_guide_2026-10.pdf).
- **Floor and ceiling tests.** Each school is tested against two limits [PPS:pps_net/rightsizing/methodology/k8_scenario_modeling_technical_guide_2026-10.pdf p.54](https://github.com/timaelliott/save-our-schools/blob/main/sources/pps_net/rightsizing/methodology/k8_scenario_modeling_technical_guide_2026-10.pdf):
  - an enrollment floor, tested on 2031-32: **K-5 360**, K-8 500, middle school 500, high school 1,100;
  - functional capacity, tested in every year from 2027-28 through 2035-36.
- **Exceptions to the floor.** "Floors are minimum student enrollments, not targets. A school may sit below its floor or above its capacity only temporarily, or where a scenario deliberately limits how many schools close" [PPS:pps_net/rightsizing/methodology/k8_scenario_modeling_technical_guide_2026-10.pdf p.54](https://github.com/timaelliott/save-our-schools/blob/main/sources/pps_net/rightsizing/methodology/k8_scenario_modeling_technical_guide_2026-10.pdf).
- **Scenario numbers are not the staffing forecast.** After adoption, PSU produces a fresh forecast from October 2026 enrollment and the adopted changes [PPS:pps_net/rightsizing/methodology/k8_scenario_modeling_technical_guide_2026-10.pdf p.4](https://github.com/timaelliott/save-our-schools/blob/main/sources/pps_net/rightsizing/methodology/k8_scenario_modeling_technical_guide_2026-10.pdf).
- **Planning judgments, not measurements** [PPS:pps_net/rightsizing/methodology/k8_scenario_modeling_technical_guide_2026-10.pdf p.56](https://github.com/timaelliott/save-our-schools/blob/main/sources/pps_net/rightsizing/methodology/k8_scenario_modeling_technical_guide_2026-10.pdf):
  - At ten closing schools, 66-90% of transfer students are assumed to follow; at nine, all of them.
  - 80% of immersion students are assumed to follow a moved program.
  - Families keep their current capture rate at the receiving school.
  - No extra families leave PPS because of a closure. The guide calls this "an upper-bound stress test on a receiving school's functional capacity".
- **Boundary timing.** "Boundary changes between two schools that both stay open apply to incoming students only" [PPS:pps_net/rightsizing/methodology/k8_scenario_modeling_technical_guide_2026-10.pdf p.56](https://github.com/timaelliott/save-our-schools/blob/main/sources/pps_net/rightsizing/methodology/k8_scenario_modeling_technical_guide_2026-10.pdf).
- **New housing.** The residency table covers where students live over the three years since 2023-24. "It does not include housing that is planned but not yet built", and when a scenario splits a school's forecast, "Students expected from new housing are split as if they lived where current students do" [PPS:pps_net/rightsizing/methodology/k8_scenario_modeling_technical_guide_2026-10.pdf p.57](https://github.com/timaelliott/save-our-schools/blob/main/sources/pps_net/rightsizing/methodology/k8_scenario_modeling_technical_guide_2026-10.pdf).
- **Old geography.** Census blocks use 2010 geography, and walking distances come from a 2016 list [PPS:pps_net/rightsizing/methodology/k8_scenario_modeling_technical_guide_2026-10.pdf p.57](https://github.com/timaelliott/save-our-schools/blob/main/sources/pps_net/rightsizing/methodology/k8_scenario_modeling_technical_guide_2026-10.pdf).
- **Commitments before the recommendation:**
  - "PPS will review the follow shares, the 100 percent transfer rules and the capture-rate assumption with PRC before the Superintendent's final proposal to the Board" [PPS:pps_net/rightsizing/methodology/k8_scenario_modeling_technical_guide_2026-10.pdf p.57](https://github.com/timaelliott/save-our-schools/blob/main/sources/pps_net/rightsizing/methodology/k8_scenario_modeling_technical_guide_2026-10.pdf).
  - "PPS will publish the range for every receiving school and every year through 2031-2032 for the scenario the Superintendent recommends" [PPS:pps_net/rightsizing/methodology/k8_scenario_modeling_technical_guide_2026-10.pdf p.58](https://github.com/timaelliott/save-our-schools/blob/main/sources/pps_net/rightsizing/methodology/k8_scenario_modeling_technical_guide_2026-10.pdf).

## Analysis: the floor test and the Southwest package

| School | PSU status quo, 2031-32 | Scenarios A and B, 2031-32 |
|---|---|---|
| Maplewood | 247 | closed |
| Hayhurst | 266 | 410 |
| Rieke | 311 | 432 |

All figures are from the family guides, compiled in `analysis/data/school_impact.csv`.

- **Why this package exists.** All three schools fall below the 360 K-5 floor on PSU's numbers. Merging Maplewood into the other two lifts both above it. That is the clearest statement yet of the logic behind the package. Maplewood is the smallest of the three in 2031-32.
- **The floor is not applied uniformly.** In Scenario A, nine other neighborhood K-5/K-8 programs stay open below their floor in 2031-32 (Skyline 177, Sunrise 254, Forest Park 258, Clark 272, Grout 280, Woodlawn 289, Glencoe 317, Vernon 323, Chapman 333). In Scenario B, 30 schools stay open below their floor, including three Southwest K-5s: Stephenson 261, Capitol Hill 311 and Markham 347. The guide allows this "where a scenario deliberately limits how many schools close" [PPS:pps_net/rightsizing/methodology/k8_scenario_modeling_technical_guide_2026-10.pdf p.54](https://github.com/timaelliott/save-our-schools/blob/main/sources/pps_net/rightsizing/methodology/k8_scenario_modeling_technical_guide_2026-10.pdf). So a sub-floor projection alone does not require Maplewood's closure.
- **Maplewood's 247 depends on PSU's forecast.** PSU projects Maplewood shrinking about 14% by 2031-32, while Maplewood's observed 2021-2026 grade progression is the highest of 38 comparable schools (`analysis/data/k5_growth_gpr_2021_2026.csv`). A forecast closer to its recent progression would raise the 2031-32 figure. On any plausible path it would still sit below 360 (Maplewood had 304 K-5 students in Oct 2026).
- **New housing doesn't help Hayhurst's case.** Students from new housing are allocated by where current students live, and housing not yet built is not in the residency table. Raleigh Crest/Alpenrose, which PSU says it has not modeled, is therefore missing from Hayhurst's projection twice over. Its students would add to a receiving school the guide already tests near its ceiling.
- **The capacity test is only as good as the capacity figure.** Markham's 2.0 ISC classrooms in the Nov 10 special-education deck [BB:14663333 p.19](https://meetings.boardbook.org/Documents/DownloadPDF/14663333?org=915#page=19) would lower its functional capacity to about 550 against a Scenario A peak of 554 (`analysis/meetings/2026-11-10_tle_materials.md`, finding 5). That fails the guide's every-year capacity test.
- **Things to check when the recommendation is posted.** Whether PPS publishes the promised per-school ranges, and whether the follow shares and capture-rate assumptions were reviewed with PSU. Both were promised before the final proposal.
