# PPS community meetings (room recordings)

Recordings of PPS-hosted community sessions made by parents attending them, added by contributors. Provenance and
checksums are in `_manifest.json`.

| File | Session | Date | Length | Who spoke |
|---|---|---|---|---|
| `2026-10-24_school-impact-conversation_west-region.mp3` | PPS School Impact Conversation: West Region (Wells and Lincoln clusters), Ida B. Wells High School | 2026-10-24 | 2:04:38 | Superintendent Kimberlee Armstrong, Jon Franco, Margaret Calvert, Nichole Watson; Directors Christy Splitt and Patte Sullivan present; City Councilor Mitch Green; 18 public commenters and 4 student speakers |

## Oct 24, 2026: School Impact Conversation, West Region

- **Audio:** a room recording by a parent attendee (Piet van Zoen), noise-cleaned and mixed down to mono. **Edited for
  privacy:** the nine places a student's or young child's name is said are covered by a 1 kHz tone of the same
  length (times in `_manifest.json`), so the file has the original length and every timestamp is unchanged.
- **Raw transcript** (`.transcript.json`): Whisper large-v3-turbo segments `[{start, end, text, speaker}]`, run locally
  by the contributor. Kept as produced **except** that the same students' and children's names are replaced with
  `[student's name removed]` / `[name removed]`, a deliberate exception to "never edit" for minors' privacy.
  Its `speaker` numbers come from automatic speaker separation and are unreliable (163 ids, far more than the number of speakers): don't use them.
- **Corrected copy:** `analysis/audio_transcripts/2026-10-24_pps-impact-conversation_west-region.txt`, built by
  `python3 tools/meeting_transcript.py` (see its header for the command). Speaker changes are marked by hand, with
  evidence and confidence per turn in `turns_2026-10-24_pps-impact-conversation-west.csv`; name fixes and privacy
  edits are logged in `corrections_2026-10-24_pps-impact-conversation-west.csv`. Members of the public are described,
  not named, and shortened to first name + initial where their names are spoken.
- **Cite** as `[AUDIO:pps_community/2026-10-24_school-impact-conversation_west-region@H:MM:SS]` (turn start).

The words are machine transcription of a room recording (one microphone, crowd noise): check the audio before
quoting anything that matters, especially numbers and names.
