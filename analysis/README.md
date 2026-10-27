# analysis/: index and how-to

Everything here is derived from `sources/` and cites back to it. The citation formats (`[BB:…]`, `[YT:…]`, `[MTG:…]`, `[PPS:…](https://github.com/timaelliott/save-our-schools/blob/main/sources/…)`, `[NEWS:…]`) and quoting rules are in `../CLAUDE.md`. Compiled 2026-10-11.

**Start here:**
- `BRIEFING.md` is the decision briefing for the Dec 15, 2026 closure vote.
- `timeline.md` is the master chronology.
- Then go to the topic, school or person file you need.

## Top-level files

| File | What it is | Use it for |
|---|---|---|
| `BRIEFING.md` | Capstone briefing: bottom line, Scenario A vs B, decision path, PPS's rationale, weak points, Board stances, next steps, top 15 sources, gaps | First read for anyone engaging with the decision |
| `topics/septsa_rightsizing_report.md` | SEPTSA (Special Education PTSA) Oct 20, 2026 report: disability impacts of Scenarios A/B, 12 information requests, cross-checks against PPS data |
| `topics/safe_structures_letter_2026-10-20.md` | Safe Structures PPS Oct 20, 2026 letter on seismic risk under Scenarios A/B (the group's estimates of students in URM and Holmes 9+ schools, closures at retrofitted schools, five questions), checked against Holmes data |
| `topics/2016_boundary_changes.md` | The 2016 West Side boundary/program changes (Res. 5256/5266): justification, PSU forecasts used by staff, Maplewood forecast vs actual |
| `topics/2005_closures.md` | The March 14, 2005 closure votes (Smith, Edwards, Richmond): resolutions, which PSU forecast they cited (March 2004 edition), the Smith case, savings claimed |
| `refresh_2026-10-18.md` | What the 2026-10-18 refresh added (BoardBook Oct 20 packet, Oct 13 committee and OPB/TV transcripts, news, pps.net FAQ rewrite, new dashboard, April engagement decks) and key findings |
| `refresh_2026-10-22.md` | What the 2026-10-22 refresh added: re-posted Board Q&A document, edited Oct 20 video, FAQ additions, Scenario A/B feeder charts, Phase I engagement summaries, Oregonian/WW/KPTV/KATU/KOIN/KGW stories (Splitt's "Scenario D", Engelsman's changes, Kotek letter) |
| `refresh_2026-10-25.md` | What the 2026-10-25 refresh added: Oct 20 Superintendent's Report slides (scenario budget table), Oct 27 committee agendas, September committee minutes, calendar changes (Nov 18 listening session moved; December events dropped), KPI/Methodology translations, BAC Q4 (Oct 28) packet with a rightsizing item, 12 news records |
| `refresh_2026-10-27.md` | What the 2026-10-27 refresh added: Oct 13–19 What We Heard recap, FAQ change, Oct 13 IGA minutes, Audit Committee attachments, Oregonian seismic story and letters, OPB/Tribune/KOIN stories, unverified Signal-photo commentary; scenarios page and its 30 PDFs unchanged |
| `topics/sw_k5_enrollment.html` | Standalone page: SW (Wells-cluster) K-5 enrollment 2007-08 to 2026-27 by school, cluster total, change since 2019-20; data in `data/sw_wells_k5_enrollment_2007-2026.csv` |
| `timeline.md` | Master timeline, Jan 2023 – Oct 2026 plus scheduled dates. One line per event; the 30 key events are bold | "When did X happen?" or "what came before Y?" |
| `timeline_from_news.md` | Timeline as reported by news outlets (Sept 2024 – Oct 2026), with per-outlet figures | News framing; items not in primary documents. Verify before relying on them |
| `_verification_report.md` | Independent fact-check: method, pass rates, 20 discrepancies, 25 corrections applied | Know which errors were fixed and how reliable each area is |
| `_transcript_analysis_instructions.md` | Instructions given to the meeting-analysis agents | How `meetings/` and the quote batches were produced |
| `README.md` | This index | — |
| `transcripts_corrected/` | All meeting transcripts with caption mis-hearings of names fixed in [brackets], plus `corrections.csv` | Reading and quoting transcripts (search and `tools/window.py` use these) |
| `speaker_transcripts/` | Speaker-labeled transcripts with every speaker re-checked (evidence and confidence per turn). First: the Oct 20, 2026 work session ([`2026-10-20_xByUlijpcnE.txt`](speaker_transcripts/2026-10-20_xByUlijpcnE.txt)) | Who said what at a meeting; checking an attribution |
| `_published_pages.md` | Shareable pages built from the archive, with links | Republishing |

## topics/: cross-cutting syntheses

| File | Contents |
|---|---|
| `rightsizing.md` | The 2026 rightsizing process end to end: origin, Res. 7296 and 7307, engagement, the Oct 5–6 scenarios by region, equity, transportation, facilities, how proposals changed, related Jefferson and SEGC work, Board positions in documents |
| `rightsizing_criteria_and_principles.md` | Policy factors, guiding principles (draft vs adopted), workplan, the "well-resourced school" definition, thresholds (360/500/1,100) and their basis, the KPI framework, and the criteria actually applied |
| `segc_equity_audit.md` | Digest of PPS's commissioned SEGC equity audit (Green & Hanson, June 2026, [BB:3997427](https://meetings.boardbook.org/Documents/DownloadPDF/3997427?org=915)): projection misses and the call for ranges, QEM and "well-resourced" floors (450/600/650, not closure thresholds), closure savings research, family and staff impacts, trust, cumulative disruption, and its pre-decision recommendations |
| `hayhurst_to_rieke_boundary_shift.md` | The Hayhurst → Rieke boundary shift in Scenarios A/B: housing units in the moved area (incl. Stephens Creek Crossing), bottom-up K-5 estimate, and a cross-check against PPS's own projections |
| `feeder_patterns_2026-10.md` | PPS's Scenario A/B feeder-pattern charts (posted 2026-10-22), how to read them, and where they disagree with the school impact pages or with themselves |
| `odyssey_move_to_mlc.md` | Odyssey's move from East Sylvan to MLC: where its students live, how its draw falls with drive distance, and estimated returns to Southwest neighborhood schools (incl. Hayhurst) |
| `topics/psu_2026_forecast_vs_actual.md` | PSU's 2026-27 forecast vs PPS's official Oct 1, 2026 enrollment: district totals, closure-list schools, Wells-cluster elementaries, and every PSU forecast of Maplewood's 2026-27 enrollment (data: `data/psu_2026-27_forecast_vs_oct1_2026_actual.csv`) |
| `phase1_engagement_2026_spring.md` | The ten Phase I (spring 2026) engagement summaries PPS posted in October: per-session results, participation counts, the After-Action Review, and how PPS's October characterizations compare with the documents |
| `rightsizing_open_questions.md` | Numbers that don't reconcile, internal contradictions, promised items not delivered, unexplained selections, missing documents |
| `bond_and_seismic.md` | The 2025 bond (Measure 26-259), high school cost history, program management (Procedeo), Holmes seismic scores, first seismic tranche, and every intersection with closures |
| `bond_seismic_open_questions.md` | Conflicting bond and seismic figures and archive gaps |
| `budget_and_enrollment.md` | Ten-year enrollment, forecasts and their vintages, under-enrolled schools, 2025-26 and 2026-27 budgets, reserves, per-pupil cost evidence, savings (none published), counter-evidence |
| `budget_enrollment_open_questions.md` | Conflicting enrollment and budget figures; data gaps |

## data/: structured tables (CSV; every row carries a source)

| File | Grain | Notes |
|---|---|---|
| `school_impact.csv` | school × scenario (StatusQuo/A/B), 82 schools | From the PPS per-school family guides (Oct 2026). Includes action, destinations, 2027-28 to 2031-32 projections, size goal met, demographics, 2025-26 enrollment and capacity, seismic score, $/student. **Use this for per-school questions.** |
| `rightsizing_scenarios.csv` | school × scenario | Earlier build from the memo, deck and regional summaries; corrected against the family guides (`schools/_discrepancies.md` Part 2) |
| `school_metrics.csv` | school × metric (long format) | 2025-26 enrollment, capacity, utilization, Title I, etc. |
| `enrollment_2026-27_sept_by_school.csv` / `enrollment_2026-27_sept_by_grade.csv` | school; school × program × grade | Fall 2026 K-8 counts from the Sept 2026 staffing workbook (`sources/staffing/`), with the spring projection, Oct 2025 count, family-guide 2027-28 status quo and staffing counts for all schools |
| `enrollment_history_and_forecast.csv` | year × level/school × measure | ACFR history 2015-16 to 2024-25, school reports, PPS projections (Apr 2025, Apr 2026), PRC forecasts, ADM, capture, charters |
| `psu_forecast_vs_actual_by_school.csv` | school × PSU edition × horizon (1–10 yrs) | Every PSU PRC school forecast (2003-04 to 2007-08 editions in `sources/psu_prc/`; 2008-09 to 2026-27 from pps.net) matched to the actual in the next report's history columns; 2026-27 actuals are the Sept 22, 2026 counts. Flags grade-span changes and COVID years. Parser for the older reports: `tools/psu_forecasts/` |
| `psu_district_forecast_vs_actual.csv` | PSU edition × horizon (1–10 yrs) | District-wide K-12 forecast from each PSU PRC edition 2001-02 to 2026-27 (medium/middle series; "Current Trends" for 2001-02 and 2002-03), with the actual October count from the next report's history columns, % error, and the source file and PDF page |
| `k5_seismic_retrofit_costs_closures.csv` | K-5 school building | Holmes complete and masonry-only retrofit estimates (2023 $), Scenario A/B closure status, documented past seismic spending (mostly roof+seismic projects), earlier work without dollar figures, KGW-reported figures, planned 2025-bond retrofits, with citations |
| `k5_prior_seismic_work.csv` | past seismic project | Each past seismic or roof-plus-seismic project at current K-5 schools (2012/2017/2020 bonds, SRGP, pre-2012 work from the Holmes report), amount, amount type, seismic share and citation |
| `psu_elementary_2030_2031_forecast_by_edition.csv` | elementary school | 2030-31 and 2031-32 forecasts in PSU's 2025-26 and 2026-27 editions, year-over-year change, typical annual change, revision between editions, PDF pages. Note: the Barbur Apartments affordable housing moved from Maplewood's zone (2025-26 ed.) to Rieke's (2026-27 ed.) [PPS:pps_net/data-and-reporting/2025-26/psu_prc_enrollment_forecast_2025-26_to_2034-35.pdf p.18](https://www.pps.net/fs/resource-manager/view/e54facfd-a9b6-4637-9080-719dff12e382#page=18) [PPS:pps_net/data-and-reporting/2026-27/psu_prc_enrollment_forecast_2026-27_to_2035-36.pdf p.18](https://www.pps.net/fs/resource-manager/view/8f9d62cd-5056-4cdc-8435-4bcba8ba86b1#page=18) |
| `hayhurst_to_rieke_shift_parcels.csv` / `hayhurst_to_rieke_shift_k5_estimate.csv` / `hayhurst_to_rieke_shift_area.geojson` | parcel; component; study polygon | Assessor parcels in the area moved from Hayhurst to Rieke, with unit estimates (low/high) and notes; the K-5 yield arithmetic; built by `tools/hayhurst_rieke_shift.py` from `sources/gis/portlandmaps/hayhurst_rieke_shift/` |
| `feeder_patterns_2026-10.csv` | scenario × school statement | Each statement on PPS's Scenario A/B feeder charts (change, destination/source, %, citation) |
| `odyssey_move_sw_estimate.csv` / `school_drive_distances_odyssey.csv` | neighborhood; school | Odyssey students by home neighborhood (Oct 2024/2025), drive distances to East Sylvan and MLC (OSRM), low/central/high estimates of students leaving Odyssey and returning to neighborhood schools |
| `video_time_offsets.csv` | meeting × segment | Offsets between a meeting's unedited livestream and BoardBook's edited upload (Oct 20, 2026: xByUlijpcnE vs SHPKPJyRfX0) |
| `budget_figures.csv` | fiscal year × item | Budget totals, reductions, FTE, reserves, PERS, ratings, per-pupil figures |
| `bond_projects.csv` | project | 2025/2020/2017 bond projects, budgets, schedules, rightsizing relevance |
| `seismic_facilities.csv` | campus (Holmes v2.0) | Risk scores, building parts, retrofit plans, joined to the scenarios |

## schools/: one page per school

- `schools/README.md` lists all 82 schools by high school region. It gives 2025-26 enrollment, the 2031-32 status-quo projection and the A and B actions and projections, with links.
- `schools/<slug>.md` covers one school: proposal under A and B, receiving and sending schools, projections, demographics, building and seismic notes, and citations to the family guide.
- `schools/_discrepancies.md` lists conflicts between the family guides and earlier analysis (D01–D26) and logs every CSV correction.

## people/: Board members and senior staff

- `people/README.md` has the roster, one-line stances, and the Board stance matrix as of Oct 2026, with an Analysis vote signal.
- `people/<slug>.md` profiles each person: roles, positions by topic, a dated "how their thinking changed" section, a voting table and key quotes. There are 27 profiles, covering 7 current directors, 4 former directors, 3 student reps and 13 senior staff.
- `people/quotes_all.jsonl` holds all 1,443 verified transcript quotes. Each record has the person, date, video and timestamp, the quote, a paraphrase, stance, topics, `confidence` and `attribution_evidence`.
- `people/positions_timeline.csv` has one row per high- or medium-confidence policy quote and per key vote.
- `people/quotes/`, `_quotes_from_news.jsonl` and `_roster_from_web.md` are input batches and notes. The batch files keep pre-verification confidence values for 4 records; `quotes_all.jsonl` is authoritative.

## meetings/: per-meeting summaries

`meetings/<YYYY-MM-DD>_<videoId>.md` covers 107 meetings, Jan 2025 – Oct 2026 (latest: [`2026-10-20_xByUlijpcnE.md`](meetings/2026-10-20_xByUlijpcnE.md), the Oct 20 work session, from a speaker-labeled vendor transcript). Each file has:
- attendance, key documents, a summary, and a **Decisions & votes** table built from minutes or video roll calls;
- sections on rightsizing, bond, seismic, facilities, and budget and enrollment;
- public comment themes, notable quotes and a topics index with timestamps.

The file name's video ID matches `sources/youtube/transcripts/<date>_<videoId>.tsv`.

## How to answer common questions

| Question | Where to go |
|---|---|
| What did X say about Y? | `python3 tools/search.py "Y" --kind quote --person "X"`, then read `people/<x>.md`. Open the `[YT:…]` link to hear the context. Only use `high`/`medium` quotes, and state medium confidence. For raw captions: `--kind transcript`. |
| How has X's position changed? | `people/<x>.md`, "How their thinking changed"; `people/positions_timeline.csv` filtered by person. |
| How will the Board vote? | `people/README.md`, "Where each board member stands"; `BRIEFING.md` (f). The vote signals are Analysis, not member statements. |
| What happens to school Z? | `schools/<z>.md`, then `data/school_impact.csv` (rows for Z), then the family guide `[PPS:pps_net/rightsizing/school_impact/<z>.pdf p.3–4]`. |
| Which schools close / convert / receive students? | `BRIEFING.md` (b); `schools/README.md`; filter `data/school_impact.csv` on `proposed_action`. |
| Why was school Z chosen? | The family guide's "Why is PPS considering this?" (p.3) via `schools/<z>.md`; `meetings/2026-10-06_zOUH2Jq7Owo.md` (staff school-by-school rationale, about 2:16–2:50 in the video); `topics/rightsizing.md` §4.3. |
| How was a vote decided? | `meetings/<date>_*.md`, Decisions & votes; the voting tables in `people/*.md`; minutes text at `sources/boardbook/meetings/<folder>/minutes_*.pdf.txt` (prefer `.ocr.txt` when present). |
| What did PPS promise and not deliver? | `topics/rightsizing_open_questions.md` §C; `BRIEFING.md` (e). |
| Where does a number come from or why do two numbers differ? | The relevant `topics/*.md` section and its `*_open_questions.md`; the `source` column in `data/*.csv`; `python3 tools/search.py '"exact figure"' --kind boardbook`. |
| Bond or seismic money at a school? | `topics/bond_and_seismic.md` §7; `data/seismic_facilities.csv`; `data/bond_projects.csv`; `schools/<z>.md`. |
| Enrollment history or forecast for a school or level? | `data/enrollment_history_and_forecast.csv`; `data/school_impact.csv` (2027–32 projections); `topics/budget_and_enrollment.md` §2. |
| Budget and savings? | `topics/budget_and_enrollment.md` §3–4 (no savings estimate exists; §4.4 has illustrative arithmetic); `data/budget_figures.csv`. |
| What happened at meeting M? | `meetings/<date>_<videoId>.md`; the agenda and attachments in `sources/boardbook/meetings/<date>_<id>_*/meeting.json`. |
| What did the press report? | `python3 tools/search.py "…" --kind news`; `timeline_from_news.md`. Treat news-only facts as unverified. |
| What is coming up and how to weigh in? | `BRIEFING.md` (g); `timeline.md`, "Scheduled". |

Search tips:
- The engine is FTS5. Put phrases in double quotes. Quote anything containing a dot (for example `'"6.10.030"'`), or the query fails.
- Date filters are `--from 2026-01-01 --to 2026-12-31`.
- Run `python3 tools/search.py --rebuild` after adding files. The index at `.cache/search.sqlite` does not pick up new analysis files automatically.

## Known stale statements in older files (superseded; not edited)

These files predate later additions to the archive. Prefer the newer source shown.

| File / location | Stale statement | Current state |
|---|---|---|
| `topics/rightsizing.md` §1, §4.4; `topics/budget_enrollment_open_questions.md` B2 | Per-school 2031-32 projections "not in the released documents" | Published in the Oct 2026 family guides; see `data/school_impact.csv` and `schools/_discrepancies.md` D18 |
| `_verification_report.md` §1 | "Per-school impact PDFs are not in the archive" | All 82 were fetched 2026-10-11 into `sources/pps_net/rightsizing/school_impact/` |
| `topics/rightsizing.md` §3.2; `topics/rightsizing_open_questions.md` B12, E30 | Final adopted text of Res. 7296 not in the archive; amendment outcome ambiguous | Adopted text is at [BB:3998077 p.13](https://meetings.boardbook.org/Documents/DownloadPDF/3998077?org=915#page=13). The video confirms the guardrail amendment failed 3–4 [YT:AH3wdS1A3sM@2:13:13](https://www.youtube.com/watch?v=AH3wdS1A3sM&t=7993s) |
| `topics/rightsizing_criteria_and_principles.md` §3 intro | "No vote tally is in the archive" for Res. 7307 | Passed 7–0 [BB:3998080 p.3](https://meetings.boardbook.org/Documents/DownloadPDF/3998080?org=915#page=3) |
| `topics/rightsizing_open_questions.md` §F; headers of `bond_and_seismic.md` and `budget_and_enrollment.md`; `bond_seismic_open_questions.md` B14 | No transcripts, pps.net or news in the archive | All three are now archived. Most "check against video" items are answered in `meetings/*.md` |
| `bond_seismic_open_questions.md` B2 | No tally for Res. 7382 | Recommendation-level roll calls from video are in `meetings/2026-09-29_SPwXuNlwP_U.md` |
| `topics/rightsizing.md` §6.3 | Spanish DLI hubs list | Incomplete. Kellogg keeps SE middle-grades Spanish; Ainsworth and West Sylvan keep West-side DLI (`schools/_discrepancies.md` D22) |
| `meetings/2026-10-06_zOUH2Jq7Owo.md` | HS threshold "1,000" | A caption artifact ("is,00"); documents say 1,100 [BB:14511742 p.10](https://meetings.boardbook.org/Documents/DownloadPDF/14511742?org=915#page=10) |
| `timeline_from_news.md` 2026-10-07 | Woodmere roof "2020 bond" (KATU) | PPS lists it as 2017-bond roof and seismic work [BB:3990267 p.22](https://meetings.boardbook.org/Documents/DownloadPDF/3990267?org=915#page=22) |
