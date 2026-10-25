#!/usr/bin/env python3
"""Build a speaker-labeled, lightly corrected transcript of a recorded meeting from Whisper-style segments plus
hand-marked speaker turns.

  python3 tools/meeting_transcript.py <raw.json> <turns.csv> <out.txt> <corrections.csv> "<title>" "<audio path>" "<source line>"

raw.json: [{"start": s, "end": s, "text": ...}, ...] (seconds). Any automatic speaker ids in it are ignored: for a
room recording with dozens of voices they are unreliable, so speaker changes are marked by hand instead.
turns.csv: start,label,role,evidence,confidence  (start H:MM:SS; each segment belongs to the last turn starting at or
before it; label is what appears in the transcript)

Words are kept verbatim except:
  - mis-heard names/terms, fixed in [brackets] (RULES);
  - privacy: students' names are replaced by [student's name removed], and other members of the public are shortened
    to first name + [last initial] (PRIVACY). Officials keep their names;
  - speech-recognition junk: the segments listed in DROP (hallucinated loops, repeats, a stray fragment) are left out.
Every change is logged to corrections.csv.
"""
import csv, json, re, sys

RULES = [  # (rule id, regex, replacement)
    ("splitt", r"\bChrist(?:y|ie) Split\b", "[Christy Splitt]"),
    ("splitt", r"\bDirector Split\b", "[Director Splitt]"),
    ("sullivan", r"\bPatty Sullivan\b", "[Patte Sullivan]"),
    ("armstrong", r"\bKimberly Armstrong\b", "[Kimberlee Armstrong]"),
    ("armstrong", r"\bDr\. (?:Archong|Arbsar)\b", "[Dr. Armstrong]"),
    ("franco", r"\bJohn Franco\b", "[Jon Franco]"),
    ("watson", r"\b[Nn]icole [Ww]atson\b", "[Nichole Watson]"),
    ("la-forte", r"\bVirginia LaForte\b", "[Virginia La Forte]"),
    ("la-forte", r"\bLafort\b", "[La Forte]"),
    ("engelsman", r"\b(?:anglesman|Ingelsman)\b", "[Engelsman]"),
    ("rieke", r"\briding Tariki\b", "riding [to Rieke]"),
    ("rieke", r"\b(?:Reiki|Reekie|Riki|Rikki|RICI)\b", "[Rieke]"),
    ("bridlemile", r"\b(?:Bridal Mile|Brattle Mall|Braddle [Mm]ile)\b", "[Bridlemile]"),
    ("mlc", r"\b(?:NLC|nlc|MOC)\b", "[MLC]"),
    ("maplewood", r"\b(?:Mabel Wood|Bigwood)\b", "[Maplewood]"),
    ("maplewood", r"\bdata for a mailman\b", "data for [Maplewood]"),
    ("stevenson", r"\bStephenson\b", "[Stevenson]"),
    ("sellwood", r"\bSelwood\b", "[Sellwood]"),
    ("markham", r"\bMarcom\b", "[Markham]"),
    ("robert-gray", r"\b(?:Rommel Gray|Nama Gray|Rammacray)\b", "[Robert Gray]"),
    ("pps", r"\b(?:PBS|PGS|DPS)\b", "[PPS]"),
    ("pps", r"\bGuant Public Schools\b", "[Portland] Public Schools"),
    ("sunsetting", r"\bsunsiting\b", "[sunsetting]"),
    ("ida-b-wells", r"\bIW Wells\b", "[Ida B. Wells]"),
    ("alpenrose", r"\b(?:Alburo|Elk and Rose)\b", "[Alpenrose]"),
    ("holt-homes", r"\b(?:whole office|whole homes|hold homes)\b", "[Holt Homes]"),
    ("village-table", r"\bvillage people, Rex\b", "[Village Table reps]"),
]
PRIVACY = [
    ("student-name", r"\bSklines\b", "[student's name removed]"),
    ("student-name", r"\bPreston K(?:inney|enny)\b", "[student's name removed]"),
    ("student-name", r"\bPriya (?:Potachetti|Paduchetti)\b", "[student's name removed]"),
    ("student-name", r"\bRoxy Raddett\b", "[student's name removed]"),
    ("student-name", r"\bJacks Bird\b", "[name removed]"),
    ("child-name", r"\bThis is Frankie\b", "This is [my daughter]"),
    ("child-name", r"\bson, Marley\b", "son, [name removed]"),
    ("surname", r"\bSusan Heffernan\b", "Susan [H.]"),
    ("surname", r"\bKathleen Ulrich\b", "Kathleen [U.]"),
    ("surname", r"\bSierra Stringfield-Herryman\b", "Sierra [S.]"),
    ("surname", r"\bHeather Jones\b", "Heather [J.]"),
    ("surname", r"\bJulie Whitaker\b", "Julie [W.]"),
    ("surname", r"\bMiranda Sim(?:enon|inal|inoff)\b", "Miranda [S.]"),
    ("surname", r"\bDrew Gettler\b", "Drew [G.]"),
    ("surname", r"\b(?:Zemecka Fenley|Stan Finley)\b", "[Samantha F.]"),
    ("surname", r"\bSamantha Finlay\b", "Samantha [F.]"),
    ("surname", r"\bSamantha Bennett\b", "Samantha [B.]"),
    ("surname", r"\bShannon Sybil, or Syvelle\b", "Shannon [S.]"),
    ("surname", r"\bShannon Sybil\b", "Shannon [S.]"),
    ("surname", r"\bCarl Snodgrass\b", "Carl [S.]"),
    ("surname", r"\bKristi Upton\b", "Kristi [U.]"),
    ("surname", r"\b(?:Lance Lozano|Len Salzano)\b", "Lance [L.]"),
    ("surname", r"\bTravis Ward\b", "Travis [W.]"),
    ("surname", r"\bAmber,? K(?:inney|enny)\b", "Amber [K.]"),
    ("surname", r"\bChristin[ae] Mede?(?:aris|iros)\b", "Christina [M.]"),
    ("surname", r"\bIbrahim Riyad\b", "Ibrahim [R.]"),
    ("surname", r"\bIbrahim Briana\b", "Ibrahim [B.]"),
]
DROP = {  # (whole seconds of segment start, text) -> reason
    (4844, "We have a great opportunity to join us."): "speech-recognition loop over noise",
    (4847, "We have a great opportunity to join us."): "speech-recognition loop over noise",
    (4850, "We have a great opportunity to join us."): "speech-recognition loop over noise",
    (5808, "So, next time we have a fluke."): "repeat of the lines just before",
    (5813, "I want to do a time check."): "repeat of the lines just before",
    (5814, "We have about 15 more minutes together."): "repeat of the lines just before",
    (7463, "ipts."): "speech-recognition junk after the end",
}


def hms(t):
    t = int(t)
    return f"{t // 3600}:{t % 3600 // 60:02d}:{t % 60:02d}"


def secs(s):
    h, m, x = (int(v) for v in s.split(":"))
    return h * 3600 + m * 60 + x


def main(raw, turns_csv, out, corr, title, audio, source):
    segs = json.load(open(raw))
    turns = list(csv.DictReader(open(turns_csv)))
    starts = [secs(t["start"]) for t in turns]
    assert starts == sorted(starts) and starts[0] == 0, "turns must start at 0:00:00 and be in time order"
    log, groups = [], []
    for s in segs:
        text = re.sub(r"\s+", " ", s["text"]).strip()
        key = (int(s["start"]), text)
        if not text:
            continue
        if key in DROP:
            log.append((hms(s["start"]), "asr-junk", text, f"(left out: {DROP[key]})"))
            continue
        for rid, rx, rep in RULES + PRIVACY:
            for m in re.finditer(rx, text):
                log.append((hms(s["start"]), rid, m.group(0), rep))
            text = re.sub(rx, rep, text)
        i = max(j for j, st in enumerate(starts) if st <= s["start"] + 0.5)
        if not groups or groups[-1][0] != i:
            groups.append([i, s["start"], []])
        groups[-1][2].append(text)
    labels = {}
    for t in turns:
        labels.setdefault(t["label"], t)
    with open(out, "w") as f:
        f.write(f"# {title}\n# Audio: {audio}\n# Source: {source}\n")
        f.write("# CORRECTED COPY: words are as transcribed; mis-heard names/terms are fixed in [brackets]; students' names are removed and other\n")
        f.write("# members of the public are shortened to first name + [last initial] (officials keep their names); a few speech-recognition\n")
        f.write("# junk/repeat segments are left out. Every change is logged in corrections_*.csv in this folder.\n")
        f.write("# Speaker changes were marked by hand from the transcript (the automatic speaker ids were unreliable for a room this size);\n")
        f.write("# evidence and confidence per turn in turns_*.csv. Timestamps are turn starts (H:MM:SS into the audio).\n")
        f.write("# Members of the public are described, not named. Speakers:\n")
        for lab, t in labels.items():
            f.write(f"#   {lab}: {t['role']}\n")
        f.write("\n")
        for i, start, texts in groups:
            f.write(f"[{hms(start)}] {turns[i]['label']}: {' '.join(texts)}\n")
    with open(corr, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["file", "timestamp", "rule", "original", "fix"])
        for r in log:
            w.writerow([out.split("/")[-1], *r])
    print(len(segs), "segments ->", len(groups), "turns;", len(log), "changes logged")


if __name__ == "__main__":
    main(*sys.argv[1:8])
