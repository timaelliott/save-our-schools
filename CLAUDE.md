# Working conventions for this repository (for Claude agents)

Purpose: source archive + analysis of Portland Public Schools (PPS), focused on the **2026 rightsizing /
school-closure proposals**. Supporting topics: 2025 bond & seismic retrofits, enrollment, budget, facilities,
and how board members and senior staff think and change positions over time. Routine procedural business
(contract approvals, minutes adoption, ceremonial items) can be noted briefly or skipped.

## Start here
- **Answering questions** about PPS closures, schools, people or meetings: follow `.claude/skills/pps-research/SKILL.md`.
  Everything needed is already in the repo, so don't browse or fetch.
- **Collecting or refreshing sources** (new meetings, minutes, transcripts): follow `RUNBOOK.md`.
- **Shareable pages** built from the archive: `analysis/_published_pages.md`.

## Rules
1. `sources/` is primary material. Never edit files there except to ADD new source files plus their
   provenance (URL + fetch date in a manifest or front matter). Do not paraphrase into sources/.
   **Always keep originals.** PPS edits and deletes posted documents. Never overwrite or delete an archived file:
   bring refreshed material in with `python3 tools/safe_copy.py <staging-dir>`, which moves any changed file to
   `<dir>/_prior/` and logs it in `sources/_versions_log.csv`. Save every new document the first time it's seen,
   even if it looks minor. After each refresh run `tools/check_upstream.py --log` (from a machine that can reach
   BoardBook/Drive) and record disappearances in `sources/_removed_upstream.csv`.
2. `analysis/` is derived. Every factual claim carries a citation:
   - BoardBook doc: `[BB:<docId> p.<page>]` (page = PDF page; text files separate pages with \f)
   - Video: `[YT:<videoId>@H:MM:SS]` (timestamp from the transcript line)
   - Audio: `[AUDIO:<path under sources/audio/ without .mp3>@H:MM:SS]` (turn start in `analysis/audio_transcripts/`); transcript-only interviews (no audio): `[AUDIO:<path without .transcript.txt>@L<line>]` (line in the raw transcript)
   - Meeting: `[MTG:<YYYY-MM-DD>/<meetingId>]`
   - pps.net / bond.pps.net files: `[PPS:<path under sources/>]` or full URL
   - Spreadsheet cells: `[PPS:<path under sources/>#<tab>!R<row>]` (row as in the xlsx; tab name as in the xlsx)
   - News: `[NEWS:<id from sources/news/index.jsonl>]`
   - Correspondence (letters to the Board): `[LTR:<file stem under sources/correspondence/> L<line>]`
   - Community-organization documents (PTAs, parent groups): `[COMM:<path under sources/community/> p.<page>]`; these are advocacy sources, so label their figures as the group's estimates
3. Quotes must be verbatim from the source text. Transcripts are auto-captions: fix nothing inside the
   quote except obvious caption artifacts, and mark any repair with [brackets]. Keep each quote short and
   relevant (1–3 sentences). Never invent or "smooth" a quote.
4. Speaker attribution for transcript quotes must state evidence and confidence:
   `confidence: high` (named by chair/self-identified immediately before, or unambiguous role),
   `medium` (strong contextual inference), `low` (guess; avoid using low-confidence quotes in syntheses).
5. Distinguish clearly between what PPS documents state, what people said, and your own inference
   (label inference as "Analysis:").
6. Helper agents spawned by a controlling session: do NOT run git commit/push (the controller commits), and write only
   to the paths your task assigns you. A session working directly for the user commits only when asked.
7. Prefer structured outputs (CSV/JSONL) alongside readable Markdown so things can be searched and joined.
8. News articles are copyrighted: store metadata, a summary in your own words, and at most short quotes
   (< 25 words each) with attribution; never full article text.

## Key indexes
- `sources/boardbook/meetings_index.csv`: every meeting since 2025-01-01
- `sources/boardbook/attachments_index.csv`: every agenda/supplemental attachment with tags and local paths
- `sources/boardbook/meetings/<date>_<id>_<slug>/meeting.json`: agenda items + attachments per meeting
- `sources/youtube/transcripts/`: per-video raw auto-captions (primary source; never edit)
- `analysis/transcripts_corrected/`: same transcripts with caption name mis-hearings fixed in [brackets]; read and
  quote from these (`tools/caption_fixes.py` regenerates them; `corrections.csv` logs every change)
- `sources/audio/` + `analysis/audio_transcripts/`: radio interviews and parent recordings of PPS community meetings (`pps_community/`), with speaker-labeled corrected transcripts
- `sources/correspondence/`: letters/emails to the Board from public officials, verbatim, with `_manifest.json`
- `sources/staffing/`: PPS staffing/enrollment workbooks (Sept 2026 "Board Request": fall 2026 K-8 counts by school and grade) with tab CSVs
- PDF text: `<file>.pdf.txt` next to each PDF (pages separated by form feed \f). Scanned PDFs also have
  `<file>.pdf.ocr.txt` (tesseract OCR of image-only pages; may contain recognition errors; verify against the PDF)
- pps.net / bond.pps.net archives: `sources/pps_net/`, `sources/bond/` with `_manifests/` (URL, final URL, fetch time)
- People: `analysis/people/README.md`, `analysis/people/quotes_all.jsonl`, per-person profiles
- Search: `python3 tools/search.py "query"` (full-text over sources + analysis)
- Data tables: `analysis/data/*.csv` (`school_impact.csv` for per-school scenario facts); director stances: `analysis/board_closure_stance/`
- Context and page lookup: `python3 tools/window.py <videoId> <H:MM:SS>`; `python3 tools/doc.py <docId> [page] [--grep re]`
- Clickable citations: `python3 tools/linkify.py <file.md>` turns citation tags into links (YouTube at the timestamp, BoardBook/pps.net PDFs at the page, news URLs), keeping the tag text
- Quote merging (new batches only): `python3 tools/merge_quotes.py analysis/people/quotes/<batch>.jsonl [--write]`
