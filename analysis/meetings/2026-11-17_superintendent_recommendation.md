# Superintendent's Rightsizing Recommendation (memo dated Nov 12, posted Nov 13, 2026)

**Bottom line for the Southwest: Maplewood stays open.** Stephenson stays open too. The West (Wells/Lincoln) region has no closures and no attendance-boundary changes. Hayhurst, Rieke, Markham and Capitol Hill are not touched [BB:14695483 p.3](https://meetings.boardbook.org/Documents/DownloadPDF/14695483?org=915#page=3) [BB:14695483 p.27](https://meetings.boardbook.org/Documents/DownloadPDF/14695483?org=915#page=27) [BB:14695483 p.40](https://meetings.boardbook.org/Documents/DownloadPDF/14695483?org=915#page=40).

## Sources and where it was posted

- BoardBook: [MTG:2026-11-17/777711](https://meetings.boardbook.org/Public/Agenda/915?meeting=777711), the Nov 17, 2026 Work Session at Benson HS, item 6 "Superintendent's Recommendation for Rightsizing" (7:30 pm). It has 18 attachments: memo BB:14695483, A–F, H–K and M–R. The memo's attachment list also names **G. Slide Deck 11.17.26 BOE** and **L. 8.70.042-P Dedicated Reserve for Income from Disposition of Surplus Real Properties**. Neither was posted as of 2026-11-14 02:00 UTC [BB:14695483 p.63](https://meetings.boardbook.org/Documents/DownloadPDF/14695483?org=915#page=63). The scheduled refresh first saw the packet on 2026-11-14 (manifest `sources/boardbook/_manifests/_manifest_bb_777711_2026-11-14.json`).
- pps.net: `/rightsize` now redirects to a "Superintendent's Recommendation" page. It links:
  - a full report that is byte-identical to BB:14695483;
  - a two-page summary in six languages;
  - 10 closure reports and 50 school impact reports.

  All are archived under `sources/pps_net/rightsizing/recommendation_2026-11-13/` (manifest `sources/pps_net/_manifests/_manifest_refresh_2026-11-14_0210.json`). PPS has taken down the old scenarios, timeline, what-we-heard, how-could-your-school-be-impacted, PSU-forecast, feeder-pattern and videos pages, which now return 404. They are logged in `sources/_removed_upstream.csv`, and our earlier snapshots are kept.

## What closes, and when

- **10 elementary schools close, phased over two years starting in fall 2027** [BB:14695483 p.2](https://meetings.boardbook.org/Documents/DownloadPDF/14695483?org=915#page=2):
  - **Fall 2027:** Beach, Peninsula, Sabin (North); Buckman, Creston (Southeast); Irvington (Northeast). Irvington's closure works like this: Beverly Cleary K-5 merges into the Irvington building for 2027-28, then the merged school moves to the seismically upgraded Beverly Cleary building in 2028-29 [BB:14695483 p.30](https://meetings.boardbook.org/Documents/DownloadPDF/14695483?org=915#page=30) [BB:14695483 p.33](https://meetings.boardbook.org/Documents/DownloadPDF/14695483?org=915#page=33) [BB:14695483 p.37](https://meetings.boardbook.org/Documents/DownloadPDF/14695483?org=915#page=37).
  - **Fall 2028:** Lewis, Marysville, Woodmere (Southeast); Rose City Park (Northeast) [BB:14695483 p.33](https://meetings.boardbook.org/Documents/DownloadPDF/14695483?org=915#page=33) [BB:14695483 p.37](https://meetings.boardbook.org/Documents/DownloadPDF/14695483?org=915#page=37).
  - The East Sylvan building (Odyssey) also closes in 2028-29, when Odyssey co-locates at Forest Park. PPS does not count it among the 10, but it appears in the Year 2 savings table [BB:14695483 p.28](https://meetings.boardbook.org/Documents/DownloadPDF/14695483?org=915#page=28) [BB:14695483 p.51](https://meetings.boardbook.org/Documents/DownloadPDF/14695483?org=915#page=51).
- **Seven K-8s become K-5:**
  - 2027: Faubion, Vernon, César Chávez, Beverly Cleary, Laurelhurst, Sunnyside.
  - 2028: Bridger.
  - MLC (K-12) becomes K-8 [BB:14695483 p.2](https://meetings.boardbook.org/Documents/DownloadPDF/14695483?org=915#page=2) [PPS:pps_net/rightsizing/recommendation_2026-11-13/summary/final_recommendation_summary.pdf p.2](https://github.com/timaelliott/save-our-schools/blob/main/sources/pps_net/rightsizing/recommendation_2026-11-13/summary/final_recommendation_summary.pdf).
- **Spanish DLI** consolidates from nine elementary sites to four hubs: César Chávez, Rigler, Lent and Ainsworth (West). **Mandarin** goes from three pathways to two [BB:14695483 p.24](https://meetings.boardbook.org/Documents/DownloadPDF/14695483?org=915#page=24).
- **Board timeline** [BB:14695483 p.4](https://meetings.boardbook.org/Documents/DownloadPDF/14695483?org=915#page=4) [BB:14695483 p.62](https://meetings.boardbook.org/Documents/DownloadPDF/14695483?org=915#page=62):

  | Date | Event |
  |---|---|
  | Nov 17 | Presentation to the Board |
  | Nov 19 | Franklin HS listening session |
  | Nov 21 | McDaniel HS info session |
  | Dec 1 | Board discussion |
  | Dec 2 | Teaching, Learning and Enrollment (TLE) Committee review |
  | Dec 3 | Grant HS listening session |
  | **Dec 15** | **Board vote** |

## What changed from Scenarios A and B

A school-by-school table (61 rows, every school changed by the recommendation or by Scenario A or B) is in `analysis/data/recommendation_2026-11-13_vs_scenarios.csv`. Notes on attachments F, N, O, P and R, and on the 2027-28 Southwest staffing model, are in `analysis/meetings/2026-11-17_recommendation_attachments_notes.md`.

Scenario A closed 14 schools and Scenario B closed 11. The recommendation closes 10 [BB:14695483 p.3](https://meetings.boardbook.org/Documents/DownloadPDF/14695483?org=915#page=3). PPS describes it as "changes primarily from Scenario A while applying the magnitude of Scenario B" [BB:14695483 p.23](https://meetings.boardbook.org/Documents/DownloadPDF/14695483?org=915#page=23). The listed changes [BB:14695483 p.3](https://meetings.boardbook.org/Documents/DownloadPDF/14695483?org=915#page=3):

- **Kept open:** Sellwood MS, James John, Maplewood and Stephenson. Both earlier scenarios had closed Maplewood, James John and Sellwood MS; only Scenario A had closed Stephenson (image pages, OCR) [BB:14695483 p.18](https://meetings.boardbook.org/Documents/DownloadPDF/14695483?org=915#page=18) [BB:14695483 p.22](https://meetings.boardbook.org/Documents/DownloadPDF/14695483?org=915#page=22).
- **Delayed:** Lewis, Marysville, Woodmere and Rose City Park now close in fall 2028 instead of fall 2027.
- **Odyssey:** moves to Forest Park, not MLC.
- **Skyline:** stays with Lincoln, not Roosevelt.
- **MLK Jr. Mandarin:** stays in place.
- **Sunnyside:** keeps a lottery environmental-focus component as a K-5.

## Southwest package in detail

### Maplewood

PPS's rationale for keeping it open [BB:14695483 p.27](https://meetings.boardbook.org/Documents/DownloadPDF/14695483?org=915#page=27):
> Enrollment at Maplewood K-5 moved above 300 students this year which is a multi-year upward trend.

> PPS heard from community members concerned about the size of a development in the area that may have a significant impact on the Hayhurst K-5 enrollment.

PPS also says it "will monitor student enrollment at all six K-5 schools in the Ida B. Wells attendance area" [BB:14695483 p.27](https://meetings.boardbook.org/Documents/DownloadPDF/14695483?org=915#page=27).

**Caution flag:** the same memo lists Maplewood among "four schools (James John, Maplewood, Sitton, and Sunrise) with very low enrollment (less than 260 students)" in 2031-32. PPS says it "will monitor closely to ensure students are receiving comparable academic programming" [BB:14695483 p.43](https://meetings.boardbook.org/Documents/DownloadPDF/14695483?org=915#page=43). That fits PSU's status-quo figure of 247 for 2031-32 in the October family guide (`analysis/schools/maplewood.md`). The memo does not say what would trigger another review of Maplewood. For Stephenson it does set a trigger (below).

### Stephenson

Kept open [BB:14695483 p.27](https://meetings.boardbook.org/Documents/DownloadPDF/14695483?org=915#page=27):
> While enrollment at Stephenson has remained below 300 students for the past three years, it has leveled out to around 285 students. PPS will monitor enrollment and if it declines two years in a row a deeper review will be started.

### Markham and Capitol Hill

PPS will watch both schools as Stephenson's neighbors. "Markham has sustained enrollment around 340 students. Capitol Hill's enrollment declined to below 300 students this year." [BB:14695483 p.27](https://meetings.boardbook.org/Documents/DownloadPDF/14695483?org=915#page=27)

### Hayhurst and Rieke

Neither is a receiving school any more. No boundary or program change is listed for either. The West region's only changes are two [BB:14695483 p.40](https://meetings.boardbook.org/Documents/DownloadPDF/14695483?org=915#page=40) [BB:14695483 p.41](https://meetings.boardbook.org/Documents/DownloadPDF/14695483?org=915#page=41):

- MLC becomes K-8 in 2027-28.
- Odyssey moves to Forest Park in 2028-29.

### Projected 2027-28 enrollment

The memo's staffing model gives the same figures for each Southwest school under the status quo and under the recommendation. The FTE is identical too [BB:14695483 p.53](https://meetings.boardbook.org/Documents/DownloadPDF/14695483?org=915#page=53) [BB:14695483 p.54](https://meetings.boardbook.org/Documents/DownloadPDF/14695483?org=915#page=54):

| School | Projected enrollment, 2027-28 | FTE, 2027-28 |
|---|---|---|
| Capitol Hill | 310 | 16.55 |
| Hayhurst | 274 | 15.85 |
| Maplewood | 278 | 16.35 |
| Markham | 312 | 17.55 |
| Rieke | 252 | 15.35 |
| Stephenson | 271 | 14.15 |

PPS calls these "preliminary planning estimates" that will be updated after PSU's revised forecasts in January [BB:14695483 p.51](https://meetings.boardbook.org/Documents/DownloadPDF/14695483?org=915#page=51).

### Regional outcome

In 2031-32, the West stays at 35% of schools above threshold, the same as the status quo [BB:14695483 p.40](https://meetings.boardbook.org/Documents/DownloadPDF/14695483?org=915#page=40). The equity statement says [BB:14695483 p.49](https://meetings.boardbook.org/Documents/DownloadPDF/14695483?org=915#page=49):
> The Ida B. Wells/Lincoln region contributes no closures and has the fewest schools at sustainable enrollment levels.

At the elementary level, 20% of West schools are sustainable, against 50% districtwide. PPS says "we will need to pay close attention to enrollment patterns in the west" [BB:14695483 p.48](https://meetings.boardbook.org/Documents/DownloadPDF/14695483?org=915#page=48). The memo also lists, as an ongoing step, "Initiation of a regional boundary review process, starting on the west side" [BB:14695483 p.1](https://meetings.boardbook.org/Documents/DownloadPDF/14695483?org=915#page=1).

Analysis: Maplewood's reprieve looks conditional rather than final. The district names the West as its weakest region and plans a West-side boundary review first. It also keeps Maplewood on a short list of schools to watch. The next pressure point is likely PSU's January forecast revision and the West boundary review, not this December vote.

### Phase-in, readiness, walkthroughs, capacity, special education and seismic as they bear on the Southwest

- **Phase-in:** nothing in the Southwest is phased, because nothing changes there.
- **Readiness and walkthroughs:** the only West walkthrough the memo describes is at MLC. It found that hosting Odyssey there, "while feasible, presented challenges", including shared classrooms and drop-off limits. That walkthrough is why Odyssey goes to Forest Park instead (capacity 519, against 264 Forest Park and 200 Odyssey students) [BB:14695483 p.28](https://meetings.boardbook.org/Documents/DownloadPDF/14695483?org=915#page=28). Across the plan, PPS says "Each site in the recommendation has a verified amount of space for special education programming" [BB:14695483 p.26](https://meetings.boardbook.org/Documents/DownloadPDF/14695483?org=915#page=26). Implementation includes receiving-school readiness reviews in June–August 2027 [BB:14695483 p.61](https://meetings.boardbook.org/Documents/DownloadPDF/14695483?org=915#page=61).
- **Special education:** under the scenarios, Maplewood's K-2 Intensive Skills Classroom was to move to Markham (`analysis/schools/maplewood.md`). With Maplewood open, no impact report is issued for it, and the memo lists no Southwest special education move. Districtwide, the memo says:
  - there is "no decrease in specialized programming, Learning Center programming, or related services";
  - average Learning Center caseload goes from 26 now to a projected 21 in 2027-28;
  - 9 of 56 K-8 specialized classrooms move;
  - two Communication Behavior (CB) classrooms are added in fall 2027 [BB:14695483 p.25](https://meetings.boardbook.org/Documents/DownloadPDF/14695483?org=915#page=25) [BB:14695483 p.26](https://meetings.boardbook.org/Documents/DownloadPDF/14695483?org=915#page=26).
- **Seismic:** the memo itself never uses the word "seismic". The impact summaries cite seismic work only for Beverly Cleary (summer 2027 and 2028) and Vernon (done summer 2026), and they describe the Rose City Park building as needing "a full seismic overhaul" [BB:14695445 p.157](https://meetings.boardbook.org/Documents/DownloadPDF/14695445?org=915#page=157). Beverly Cleary and Vernon: [BB:14695445 p.13](https://meetings.boardbook.org/Documents/DownloadPDF/14695445?org=915#page=13) [BB:14695445 p.17](https://meetings.boardbook.org/Documents/DownloadPDF/14695445?org=915#page=17) [BB:14695445 p.129](https://meetings.boardbook.org/Documents/DownloadPDF/14695445?org=915#page=129). Nothing ties a Southwest building's seismic status to the decision either way.

## Did PPS publish the per-school ranges and the PSU review of follow shares?

The K-8 modeling guide promised two things before the final proposal [PPS:pps_net/rightsizing/methodology/k8_scenario_modeling_technical_guide_2026-10.pdf p.57](https://github.com/timaelliott/save-our-schools/blob/main/sources/pps_net/rightsizing/methodology/k8_scenario_modeling_technical_guide_2026-10.pdf):

1. PPS would review the follow shares, the 100% transfer rules and the capture-rate assumption with PRC.
2. PPS would produce "a range for each receiving school".

**Neither appears in the packet or on the new pps.net pages, as far as this run can find:**

- **Ranges:** the memo says that for the DLI moves "we lowered our assumption and provided a range of students who may move" [BB:14695483 p.24](https://meetings.boardbook.org/Documents/DownloadPDF/14695483?org=915#page=24). It also says that for James John, "PPS ran the model again to produce a range of enrollment projections rather than a single number" [BB:14695483 p.27](https://meetings.boardbook.org/Documents/DownloadPDF/14695483?org=915#page=27). But the school impact summaries show a single "Recommendation" enrollment row per year, for example César Chávez 414 → 494 [BB:14695445 p.26](https://meetings.boardbook.org/Documents/DownloadPDF/14695445?org=915#page=26). A text search of attachments C, D, F and P, and of the pps.net PDFs, finds no low/high table.
- **PRC review:** no document records one. The new methodology attachment (F) describes the data sets and criteria but says nothing about follow shares or PRC review [BB:14695410 p.2](https://meetings.boardbook.org/Documents/DownloadPDF/14695410?org=915#page=2) [BB:14695410 p.6](https://meetings.boardbook.org/Documents/DownloadPDF/14695410?org=915#page=6).

The slide deck (attachment G) has not been posted yet and may contain the ranges. Check it when it appears.

## Money

- **Savings:** net recurring savings of about $10.2 million across both years, leaving about $7.1 million to reinvest after one-time costs [BB:14695483 p.3](https://meetings.boardbook.org/Documents/DownloadPDF/14695483?org=915#page=3) [BB:14695483 p.51](https://meetings.boardbook.org/Documents/DownloadPDF/14695483?org=915#page=51).
- **Receiving schools:** 15–20 FTE is reserved for receiving schools. None is in the Southwest [BB:14695483 p.55](https://meetings.boardbook.org/Documents/DownloadPDF/14695483?org=915#page=55).
- **Transportation:** bus routes rise from 122 to about 153, roughly +$2.7 million. The DLI hub routes add about $3 million net [BB:14695483 p.56](https://meetings.boardbook.org/Documents/DownloadPDF/14695483?org=915#page=56).
- **Context:** the Nov 17 financial update puts the 2027-28 gap at $65.2 million [BB:14692843 p.12](https://meetings.boardbook.org/Documents/DownloadPDF/14692843?org=915#page=12).
