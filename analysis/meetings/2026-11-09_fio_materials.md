# FIO Committee, 2026-11-09: school readiness profiles and seismic reallocation (pre-meeting materials)

- **Status:** written 2026-11-06 from the materials posted before the meeting. No video yet.
- **BoardBook:** meeting 776245 [MTG:2026-11-09/776245](https://meetings.boardbook.org/Public/Agenda/915?meeting=776245). Agenda item 4, "Rightsizing Update: Facilities School Readiness."
- **Document:** FIO Presentation 11.09.26, 36 pages [BB:14644366](https://meetings.boardbook.org/Documents/DownloadPDF/14644366?org=915). Structured data from the 21 profiles: `analysis/data/fio_readiness_profiles_2026-11-09.csv`.
- **Also fetched in this refresh (2026-11-06):** TLE Committee Nov 10 (special education and DLI; no attachments yet) [MTG:2026-11-10/776248](https://meetings.boardbook.org/Public/Agenda/915?meeting=776248); Intergovernmental Affairs Nov 10 (draft 2027 legislative agenda) [MTG:2026-11-10/776737](https://meetings.boardbook.org/Public/Agenda/915?meeting=776737); new Nov 4 attachments (OSAS memos and presentation, "Preliminary Findings: What We Heard," committee reports); Oct 27 Audit Committee minutes and attachments.

## What the deck says

- **Process.** PPS assessed readiness using functional capacity, current utilization and work-order counts, Tririga room data, June principal reviews of floor plans, and in-person walkthroughs "with principals of 21 buildings set to experience the highest number of student increase" [BB:14644366 p.5](https://meetings.boardbook.org/Documents/DownloadPDF/14644366?org=915#page=5).
- **Capacity rules** [BB:14644366 p.6](https://meetings.boardbook.org/Documents/DownloadPDF/14644366?org=915#page=6):
  - classrooms of 500–800 sq ft count 24 students, 801–1,000 count 27, larger count 30;
  - special education classrooms "are set aside from general instructional functional capacity," and "Capacity in these rooms is 12 students";
  - K-5/K-8 calculations exclude gyms and "one or two Art/Music rooms, based on enrollment."
- **21 Campus Readiness Profiles** [BB:14644366 p.9–29](https://meetings.boardbook.org/Documents/DownloadPDF/14644366?org=915#page=9). 18 are rated "Ready/Minor Adjustments," Hosford "Conditionally Ready," George and Markham "Not Yet Ready/Significant Barriers." Most "urgent improvements" are kitchen equipment ($3,100–$83,000).
- **ADA:** "All PPS campuses are ADA accessible to the main floor" [BB:14644366 p.30](https://meetings.boardbook.org/Documents/DownloadPDF/14644366?org=915#page=30). Several receiving schools have no elevator.
- **Seismic reallocation (new)** [BB:14644366 p.31](https://meetings.boardbook.org/Documents/DownloadPDF/14644366?org=915#page=31):
  - Scenario A moves Rose City Park and Beach retrofit money to Abernethy, Arleta, Brentwood, Duniway, Hosford, Markham, Rigler, Rieke (Building Parts A, B and C) and Whitman.
  - Scenario B moves Beach money to Duniway and Rieke.
  - PPS is "Applying for SRGP grant for Rieke (Building Parts B and C)."
- **Seismic outcome claims** [BB:14644366 p.32–33](https://meetings.boardbook.org/Documents/DownloadPDF/14644366?org=915#page=32): district seismic risk score 5.45 (2025) → 5.30 status quo, 5.04 (A), 5.09 (B). "Both scenarios show a reduction in the proportion of students attending schools with building parts rated 9.0+ and schools with URM buildings."

## Mathematical flaws and inconsistencies

**1. Hayhurst's 525 cannot be reproduced from the profile's own room counts.**
- The profile lists **7 special education classrooms and 15 classrooms** [BB:14644366 p.19](https://meetings.boardbook.org/Documents/DownloadPDF/14644366?org=915#page=19). The utilization model has 22 classrooms at Hayhurst (20 rated 27 students, 2 rated 30), with only 2 special education rooms and 1 Learning Center set aside, giving 525 [PPS:pps_net/rightsizing/utilization_model/tab_DISTRICT_UTILIZATION_v1.csv](https://github.com/timaelliott/save-our-schools/blob/main/sources/pps_net/rightsizing/utilization_model/tab_DISTRICT_UTILIZATION_v1.csv) [PPS:pps_net/rightsizing/utilization_model/tab_CLASSROOM_LIST_v1.csv](https://github.com/timaelliott/save-our-schools/blob/main/sources/pps_net/rightsizing/utilization_model/tab_CLASSROOM_LIST_v1.csv).
- Analysis: applying the deck's own rules (p.6) to the profile's 7 + 15 rooms: one Art/Music room comes out of the 15, leaving 14 general rooms (12 × 27 + 2 × 30 = 384), plus 7 special education rooms × 12 = 84. That is **468**, or **456** if the Learning Center is set aside as the model does. The projected peak is **469** (in 2027). Hayhurst would be at 100–103% of capacity, not 89%.
- The profile also contradicts itself: the capacity box says 7 special education classrooms, the Special Education box says "4 Classrooms Total" (one Learning Center, two Social Emotional Skills rooms, one sensory space). Even with 4, the capacity works out to about 489, not 525.
- **Largest historic enrollment "640 students in 2019-2020" is wrong.** PPS's own utilization model lists Hayhurst's 2019-20 enrollment as **396** [PPS:pps_net/rightsizing/utilization_model/tab_DISTRICT_UTILIZATION_v1.csv](https://github.com/timaelliott/save-our-schools/blob/main/sources/pps_net/rightsizing/utilization_model/tab_DISTRICT_UTILIZATION_v1.csv); the 640 adds Odyssey K-8 (244), which had moved to East Sylvan in 2016 [PPS:pps_net/data-archives/2019-20/enrollment_by_grade_and_program_type.pdf p.2](https://github.com/timaelliott/save-our-schools/blob/main/sources/pps_net/data-archives/2019-20/enrollment_by_grade_and_program_type.pdf). The most students ever in the Hayhurst building in PPS's records is **499, in fall 2015** (277 Hayhurst K-5 + 222 Odyssey), which PPS then rated "Over-Crowding" at 101.8% [PPS:pps_net/data-archives/2019-20/enrollment_history_detail_2019-20.pdf p.1](https://www.pps.net/fs/resource-manager/view/c58980d2-9a82-4e6b-b98d-eca7cd80c53d#page=1) [PPS:pps_net/boundaries_2016/dbrac/Quadrant_KPIs_SuptRecommendationsWest.pdf p.3](https://github.com/timaelliott/save-our-schools/blob/main/sources/pps_net/boundaries_2016/dbrac/Quadrant_KPIs_SuptRecommendationsWest.pdf). The other profiles that cite a 2019-20 peak match the model (Arleta 526, Duniway 512); only Hayhurst does not.

**2. Two schools rated "Ready" would be over capacity at peak.**
- Whitman: peak 466 (2032) against functional capacity 416, **112%**, rated "Ready/Minor Adjustments" [BB:14644366 p.29](https://meetings.boardbook.org/Documents/DownloadPDF/14644366?org=915#page=29).
- Sitton: peak 465 (2029) against 419, **111%**, rated "Ready/Minor Adjustments" [BB:14644366 p.27](https://meetings.boardbook.org/Documents/DownloadPDF/14644366?org=915#page=27).
- By contrast George (107%) is "Not Yet Ready" and Hosford (105%) "Conditionally Ready" [BB:14644366 p.17](https://meetings.boardbook.org/Documents/DownloadPDF/14644366?org=915#page=17) [BB:14644366 p.20](https://meetings.boardbook.org/Documents/DownloadPDF/14644366?org=915#page=20). The rating does not follow utilization.

**3. Special education room counts disagree within profiles, and capacity was not updated.**
- In 9 of 21 profiles the capacity box and the Special Education box give different room counts. Largest gaps: Rosa Parks 3 vs "Approximately 6-7 Classrooms" [BB:14644366 p.26](https://meetings.boardbook.org/Documents/DownloadPDF/14644366?org=915#page=26); Whitman 1 vs "4-5 Classrooms Total" [BB:14644366 p.29](https://meetings.boardbook.org/Documents/DownloadPDF/14644366?org=915#page=29); Hayhurst 7 vs 4 [BB:14644366 p.19](https://meetings.boardbook.org/Documents/DownloadPDF/14644366?org=915#page=19); Hosford 5 vs 3 [BB:14644366 p.20](https://meetings.boardbook.org/Documents/DownloadPDF/14644366?org=915#page=20).
- Every functional capacity in the 21 profiles equals the Static V1 utilization model (posted Nov 2) exactly, including Brentwood, which the model still lists as "LANE" (763). The walkthroughs did not change any capacity number, although the profiles list more special education rooms than the model sets aside at Hayhurst (7 vs 3), George (7 vs 3), Hosford (5 vs 1), Gray (3 vs 1) and Arleta (4 vs 2).
- Analysis: each room moved from general use to special education lowers capacity by about 12–15 seats under the p.6 rules. Rosa Parks (peak 487 vs 499) and Whitman (already 112%) are the most sensitive.

**4. Capacities changed since April 2026, and the changes matter at four receiving schools.**
- Compared with PPS's April 2026 enrollment and utilization table [BB:3997157 p.1](https://meetings.boardbook.org/Documents/DownloadPDF/3997157?org=915#page=1), functional capacity rose at Markham (510 → 561), Vestal (465 → 516), Capitol Hill (375 → 417) and Duniway (525 → 552). With the April figures their peaks would be 109%, 109%, 103% and 104% of capacity; with the new figures they are 99%, 98%, 93% and 99%.
- Capacity fell at Rosa Parks (633 → 499), Sitton (496 → 419), Boise-Eliot/Humboldt (632 → 586), Rigler (654 → 621), Chávez (589 → 564) and Whitman (442 → 416).
- The deck does not explain the changes.

**5. Many receiving schools would exceed the most students they have ever enrolled.** Peak above "largest historic enrollment" on the profile: Markham (554 vs 456), Vestal (507 vs 451), George (669 vs 588), Hosford (747 vs 676), Duniway (544 vs 512), Arleta (552 vs 526), Sitton (465 vs 449). Hayhurst belongs on this list (469 vs 396) once the Odyssey students are removed from its "640."

**6. The "21 buildings with the highest increase" list leaves out large increases.**
- Analysis: comparing each Scenario A family guide's peak with its no-change peak, Harrison Park (+215), Harriet Tubman (+151), Lent (+147, DLI moves in), Rieke (+117) and Roseway Heights (+116) are not profiled, while Capitol Hill (+68), Ockley Green (+110) and Gray (+124) are (`data/school_impact.csv`). PPS may have used a different measure; the deck does not say.
- Rieke receives 30% of Maplewood and the Stephens Creek Crossing area from Hayhurst, has the highest seismic score among receiving schools (9.6) [BB:3991109 p.233](https://meetings.boardbook.org/Documents/DownloadPDF/3991109?org=915#page=233), and gets seismic money in both scenarios, but has no readiness profile.

**7. The seismic claim for Scenario B is not supported by the deck's own table.**
- Normalized table [BB:14644366 p.33](https://meetings.boardbook.org/Documents/DownloadPDF/14644366?org=915#page=33): students at campuses with a building part rated 9.0+ are **8,249 (33.5%) under the status quo, 8,015 (32.5%) under A and 8,285 (33.6%) under B.** Scenario B is slightly worse than doing nothing.
- The "reduction" in the slide is measured from 2025 values (11,175). Most of it (−2,926 students) comes from 2025 bond retrofits that happen under the status quo too. Scenario A adds a further −234 students (1.0 point).
- URM is a real difference: 19.6% (status quo) → 11.1% (A) and 15.9% (B).
- The unnormalized table compares status-quo 2025-26 enrollment with 2031-32 scenario enrollment; its Scenario B total (25,031) exceeds the status quo (24,646) and A (24,541), and footnote 5 says B "may be overstated."

**8. Hidden template text.** The PDF carries leftover text layers from other schools under several profiles (e.g. "561 students" and "456 students in 2017-2018" under MLC and later pages) [BB:14644366 p.22–29](https://meetings.boardbook.org/Documents/DownloadPDF/14644366?org=915#page=22). They are not visible on the slides but show up in text extraction and screen readers.

## New information
- Rieke seismic upgrades (Building Parts A, B and C) in both scenarios, with an SRGP grant application [BB:14644366 p.31](https://meetings.boardbook.org/Documents/DownloadPDF/14644366?org=915#page=31).
- Hayhurst transportation: "City review and expansion required. On property adjustments required and able to accommodate" [BB:14644366 p.19](https://meetings.boardbook.org/Documents/DownloadPDF/14644366?org=915#page=19).
- Markham "Not Yet Ready": "Space constraints. Limited street frontage"; Maplewood's Intensive Skills Classroom students "will return to Markham" [BB:14644366 p.21](https://meetings.boardbook.org/Documents/DownloadPDF/14644366?org=915#page=21).
- George needs a $750K covered PE structure (Summer 2028) [BB:14644366 p.17](https://meetings.boardbook.org/Documents/DownloadPDF/14644366?org=915#page=17).
- Bond: Ida B. Wells land-use approval received; Beverly Cleary retrofit in for permit; Richmond, Ainsworth and Kelly retrofit RFPs before mid-December [BB:14644366 p.3](https://meetings.boardbook.org/Documents/DownloadPDF/14644366?org=915#page=3).

## Deck vs. the Static V1 utilization model (posted Nov 2)
- Functional capacity: identical for all 21 schools.
- Room counts (deck special education + classrooms vs. model classrooms + modulars) match at Hayhurst (22), Rosa Parks (26), Whitman (24), Capitol Hill (19), Chávez (31), Chief Joseph (19), Duniway (25) and Gray (26), and differ at Boise-Eliot/Humboldt (28 vs 34), Ockley Green (39 vs 34), Vestal (32 vs 26), Mt. Tabor (35 vs 31), Sitton (26 vs 24), George (33 vs 31), Markham (24 vs 26), Hosford (33 vs 32), Arleta (30 vs 29), Rigler (28 vs 29) and Abernethy (22 vs 21).
- Special education rooms: the model sets aside fewer than the deck counts at Hayhurst (3 incl. Learning Center vs 7), George (3 vs 7), Hosford (1 vs 5), Gray (1 vs 3) and Arleta (2 vs 4). Capacity was not reduced to match.
- Title I adjustment: the model cuts capacity 5% at Title I schools (Arleta, Markham, Rigler, Rosa Parks, Sitton, Vestal, Whitman; 10% at Boise-Eliot/Humboldt and Chávez) [PPS:pps_net/rightsizing/utilization_model/tab_GENERAL_NOTES.csv](https://github.com/timaelliott/save-our-schools/blob/main/sources/pps_net/rightsizing/utilization_model/tab_GENERAL_NOTES.csv). Markham is expected to lose Title I under Scenario A, which would raise its modeled capacity again.
