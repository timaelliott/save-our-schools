# Speaker-labeled meeting transcripts

Meetings where we have a transcript with speaker separation (not plain YouTube captions), with **every speaker
checked by reading the transcript**.

| Meeting | Transcript | Source |
|---|---|---|
| 2026-10-20 Board work session (BoardBook 772442), video [xByUlijpcnE](https://www.youtube.com/watch?v=xByUlijpcnE) | [`2026-10-20_xByUlijpcnE.txt`](2026-10-20_xByUlijpcnE.txt) | Vendor word-level export, supplied by the repository owner 2026-10-21 ([raw](../../sources/youtube/vendor_transcripts/2026-10-20_xByUlijpcnE.timestamps.json)) |
| 2026-11-09 Facilities Improvement and Oversight Committee (BoardBook 776245), video [cyHU9UOQqvc](https://www.youtube.com/watch?v=cyHU9UOQqvc) | [`2026-11-09_cyHU9UOQqvc.txt`](2026-11-09_cyHU9UOQqvc.txt) | Vendor paragraph export, supplied by the repository owner 2026-11-09 ([raw](../../sources/youtube/vendor_transcripts/2026-11-09_cyHU9UOQqvc.paragraphs.json)); build script `_build/build_2026-11-09_cyHU9UOQqvc.py` |

Files per meeting:
- `<date>_<videoId>.txt`: one line per speaker turn, `[H:MM:SS] Name (role) {confidence if not high}: words`. Words are as
  transcribed; mis-heard names are fixed in [brackets]; children's names are replaced with [student name].
- `turns_<date>_<videoId>.csv`: every turn with start/end, speaker, confidence, the evidence for the attribution, and the
  vendor's original tag and turn numbers, so each re-assignment can be checked.
- `speakers_<date>_<videoId>.csv`: everyone who speaks, with turn and word counts.
- `corrections_<date>_<videoId>.csv`: every bracketed fix and redaction.

**Why the re-check matters (2026-10-20):** the vendor tagged six speakers by name and the rest by letter. The letters were
reused for different people: "H" is a public commenter, the board manager, Director Splitt and Christina Howard at
different times. Some named tags were wrong:
- a retired teacher's public comment was tagged "Kimberlee Armstrong";
- CFO Michelle Morrison was tagged "Stephanie Engelsman";
- the board manager calling speakers was tagged "Virginia La Forte".

Directors Splitt and Sullivan had no named tag. They were identified from the chair's recognitions and from staff
addressing them by name. Quotes for `analysis/people/` were taken only from turns marked high, unless the quote says
otherwise.

Citations use the video: `[YT:xByUlijpcnE@H:MM:SS]`. `tools/merge_quotes.py` and `tools/window.py` read the caption-style
copy in `sources/youtube/transcripts/2026-10-20_xByUlijpcnE.txt`, which has the same words without speaker tags.

**Re-check notes (2026-11-09 FIO committee):** the export's speakers are letters A–O, and several were reused for different people:
- "D" is the student representative's self-introduction, then Director Engelsman for most of the meeting, and the board manager reading the public-comment list.
- "L" is Chief Buno, and also Chair Wang when the chair called on him online.
- "B" is legal counsel at the introductions, then a public commenter.
Engelsman is identified from her self-introduction, Franco's "Thanks, Director Engelsman", and her reference to "Chair DePass". Chase-Miller is identified from the chair's question "Is that Director [Chase-Miller]?". The meeting summary is in `analysis/meetings/2026-11-09_fio_meeting.md`.
