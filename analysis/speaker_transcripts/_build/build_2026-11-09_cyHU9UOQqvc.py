#!/usr/bin/env python3
"""Build the speaker-checked transcript of the Nov 9, 2026 Facilities Improvement and Oversight (FIO) Committee meeting
(video cyHU9UOQqvc, BoardBook 776245) from the vendor paragraph export (sources/youtube/vendor_transcripts/
2026-11-09_cyHU9UOQqvc.paragraphs.json).

Writes, under analysis/speaker_transcripts/:
  2026-11-09_cyHU9UOQqvc.txt, turns_/speakers_/corrections_2026-11-09_cyHU9UOQqvc.csv,
  2026-11-09_cyHU9UOQqvc_transcript.html (artifact page) and _standalone.html (self-hosting copy)
and, into a staging folder given as argv[1] (then brought into sources/ with tools/safe_copy.py), the caption-style copy
  youtube/transcripts/2026-11-09_cyHU9UOQqvc.{tsv,txt,meta.json}.

Speaker attribution: the vendor's letter tags were reused for different people (e.g. "D" is the student representative,
Director Engelsman and the board manager; "L" is Chief Buno and Chair Wang). Every turn below was re-assigned by reading
the transcript; ASSIGN holds the evidence. Run from the repo root.
"""
import csv, json, re, sys, html
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
VID, DATE, MTG = 'cyHU9UOQqvc', '2026-11-09', '776245'
RAW = ROOT / f'sources/youtube/vendor_transcripts/{DATE}_{VID}.paragraphs.json'
OUT = ROOT / 'analysis/speaker_transcripts'
STEM = f'{DATE}_{VID}'

PEOPLE = {  # id: (name, role, kind)
    'DEP': ('Michelle DePass', 'Board member, Zone 2; FIO Committee chair', 'board'),
    'ENG': ('Stephanie Engelsman', 'Board member, Zone 6; FIO Committee member', 'board'),
    'CM': ('Rashelle Chase-Miller', 'Board Vice-Chair (online)', 'board'),
    'WANG': ('Eddie Wang', 'Board Chair (online)', 'board'),
    'ALM': ('Lila Almeida', 'Student representative (as introduced)', 'board'),
    'ARM': ('Kimberlee Armstrong', 'Superintendent', 'staff'),
    'FRA': ('Jon Franco', 'Senior Chief of Operations', 'staff'),
    'EVE': ('Joanna Evenson', 'Senior Director, RISE (facilities construction projects)', 'staff'),
    'LEA': ('Frank Leavitt', 'Senior Director, Facilities & Maintenance (as introduced)', 'staff'),
    'BUNO': ('Jey Buno', 'Chief of Student Support Services', 'staff'),
    'COON': ('Brandon Coonrod', 'Senior Director, Student Transportation', 'staff'),
    'CLERK': ('Rosanne Powell', 'Board Manager', 'staff'),
    'LEGAL': ('Emily Courtneidge', 'Senior Legal Counsel', 'staff'),
    'EGG': ('Jennifer Eggers', 'Holmes Structural Engineering (seismic consultant)', 'guest'),
    'PC1': ('Public commenter 1', 'Maplewood parent', 'public'),
    'PC2': ('Public commenter 2', 'PPS parent; Lincoln Youth Baseball board member', 'public'),
    'PC3': ('Public commenter 3', 'Cleveland High School baseball/softball board member', 'public'),
    'PC4': ('Public commenter 4', 'Parent; Lincoln Little League Softball president', 'public'),
    'PC5': ('Public commenter 5', 'Forensic architect; Rose City Park parent', 'public'),
    'UNK': ('Unidentified', 'Speaker not identifiable from the recording', 'other'),
}

# Default speaker for each vendor tag (the person who holds that tag for most of the meeting), then per-turn overrides.
DEFAULT = {
    'A': ('DEP', 'h', 'Chair: calls the meeting to order, introduces herself as committee chair (0:30:44) and runs it throughout'),
    'B': ('UNK', 'h', 'vendor tag B is used for several voices'),
    'C': ('ARM', 'm', 'vendor tag C; Armstrong introduces herself with this tag (0:30:32)'),
    'D': ('ENG', 'm', 'vendor tag D; Engelsman introduces herself with this tag (0:30:50); in-person committee member'),
    'E': ('FRA', 'h', 'Franco introduces himself (0:30:55) and leads the staff presentation'),
    'F': ('EVE', 'h', 'Franco hands updates to "Joanna" (0:49:25, 0:56:37); answers on capital projects throughout'),
    'G': ('PC1', 'h', 'public commenter self-identifies (0:32:29)'),
    'H': ('PC2', 'h', 'public commenter self-identifies (0:35:11)'),
    'I': ('UNK', 'h', 'vendor tag I is used for several voices'),
    'J': ('PC3', 'h', 'public commenter self-identifies (0:38:24)'),
    'K': ('PC5', 'h', 'public commenter self-identifies (0:43:22)'),
    'L': ('BUNO', 'h', 'Franco: "I\'m going to have Jay kind of chime in" (1:02:34); answers special-education questions'),
    'M': ('LEA', 'h', 'Franco: "Frank, you want to take this one?" (1:02:09); "Thank you, Frank" (1:16:36)'),
    'N': ('COON', 'h', 'Franco: "Brandon, maybe you could talk real quick about transportation" (1:20:21)'),
    'O': ('EGG', 'h', 'Franco calls up Jennifer Eggers for the seismic portion (1:30:20)'),
}
OVR = {  # raw turn number: (speaker, confidence, evidence)
    0: ('UNK', 'h', 'before the meeting'), 1: ('UNK', 'h', 'before the meeting'),
    4: ('LEGAL', 'h', 'self-introduction: "Emily [Courtneidge], legal counsel"'),
    5: ('ARM', 'h', 'self-introduction: "Kim Armstrong, superintendent"'),
    6: ('ALM', 'h', 'self-introduction: "Lila Almeida, student representative"'),
    8: ('ENG', 'h', 'self-introduction: "Stephanie Engelsman"'),
    11: ('CLERK', 'h', 'chair asks "[Rosanne], do we have ... who do we have signed up"; reply lists online directors and commenters'),
    13: ('CLERK', 'h', 'reads the public-comment sign-up list'),
    19: ('UNK', 'm', 'one-word remark'),
    24: ('PC2', 'm', 'next commenter stepping up; self-identifies two turns later'),
    28: ('PC2', 'm', 'commenter answering the chair before spelling her name'),
    37: ('CLERK', 'h', 'reads the next names on the sign-up list'),
    38: ('UNK', 'm', 'one-word remark'),
    41: ('UNK', 'm', 'commenter at the microphone'),
    44: ('UNK', 'm', 'one-word remark'),
    47: ('PC4', 'h', 'public commenter self-identifies'),
    50: ('UNK', 'm', 'one-word remark during public comment'),
    54: ('CLERK', 'h', 'answers the chair: no more commenters'),
    56: ('UNK', 'm', 'one-word reply'),
    58: ('FRA', 'm', 'one-word reply from the staff table'),
    59: ('ARM', 'm', 'vendor tag C (Armstrong); asks staff for a field update while the community is present'),
    62: ('UNK', 'm', 'one-word reply'),
    66: ('EVE', 'm', 'Powell Park update after Franco asks his team; same voice tag as Evenson'),
    84: ('ARM', 'm', 'vendor tag C (Armstrong)'), 86: ('ARM', 'm', 'vendor tag C (Armstrong)'),
    94: ('ENG', 'm', 'in-person committee member other than the chair; says she will contact Director Splitt about the IGA committee'),
    120: ('ENG', 'm', 'vendor tag D; in-person committee member asking to comment'),
    122: ('ENG', 'm', 'vendor tag D; same voice continues'), 124: ('ENG', 'm', 'vendor tag D; same voice continues'),
    126: ('UNK', 'm', 'interrupted fragment'),
    129: ('UNK', 'm', 'one-word remark'), 134: ('UNK', 'm', 'two-word remark'), 133: ('UNK', 'm', 'one-word remark'),
    147: ('ENG', 'm', 'vendor tag D; in-person committee member'),
    158: ('UNK', 'm', 'two-word remark'),
    164: ('ENG', 'h', 'Franco replies "Thanks, Director Engelsman" (1:23:20) after this exchange'),
    166: ('ENG', 'h', 'Franco replies "Thanks, Director Engelsman" (1:23:20)'),
    170: ('UNK', 'm', 'one-word remark'),
    177: ('ENG', 'm', 'vendor tag D; continues her questions on Markham'), 179: ('ENG', 'm', 'same voice'), 181: ('ENG', 'm', 'same voice'),
    182: ('UNK', 'm', 'one-word remark'),
    183: ('ARM', 'h', 'speaks about the superintendent recommendation and the final packet; vendor tag C'),
    185: ('ARM', 'h', 'continues the same remarks'),
    187: ('ENG', 'm', 'vendor tag D; asks "Ms. Powell" to move a text box'), 189: ('ENG', 'm', 'same voice'),
    188: ('CLERK', 'm', 'answers the request addressed to "Ms. Powell"'),
    206: ('ENG', 'm', 'vendor tag D; says she has questions (asks them at 1:41:17)'), 208: ('ENG', 'm', 'same voice'),
    210: ('UNK', 'm', 'two-word remark'),
    213: ('UNK', 'l', 'reply when the chair asks for questions from online members'),
    215: ('CM', 'h', 'chair: "Is that Director [Chase-Miller]?" reply: "Yeah, that\'s me"'),
    217: ('CM', 'h', 'recognized by the chair (1:38:39)'), 220: ('CM', 'h', 'same speaker, after Buno\'s answer'),
    218: ('ARM', 'm', 'vendor tag C; hands the question to staff'),
    222: ('ENG', 'h', 'in-person director (not the chair: she refers to "Chair DePass") who sent six special-education questions'),
    224: ('UNK', 'm', 'two-word remark'),
    228: ('ENG', 'h', 'same questioner'), 236: ('UNK', 'm', 'one-word remark'), 238: ('ENG', 'h', 'same questioner'),
    240: ('ENG', 'h', 'same questioner'), 242: ('ENG', 'h', 'same questioner'), 244: ('ENG', 'h', 'same questioner'),
    246: ('ENG', 'h', 'same questioner'), 248: ('ENG', 'h', 'same questioner'),
    250: ('ENG', 'h', 'refers to "Chair DePass", so not the chair; continues her questions'),
    252: ('ENG', 'h', 'same questioner'), 254: ('ENG', 'h', 'same questioner'), 256: ('ENG', 'h', 'same questioner'),
    258: ('ENG', 'h', 'same questioner'), 261: ('ENG', 'h', 'same questioner'), 263: ('ENG', 'h', 'same questioner'),
    264: ('ARM', 'm', 'vendor tag C; answers on readiness information for every recommended site'),
    265: ('ENG', 'h', 'same questioner'),
    271: ('WANG', 'h', 'chair calls "Chair [Wang]?" (1:54:16); speaker refers to "Dr. Armstrong"'),
    273: ('WANG', 'h', 'same speaker continues'),
    285: ('UNK', 'm', 'one-word remark'),
    296: ('UNK', 'l', 'aside before the chair\'s reply'),
    298: ('ENG', 'm', 'vendor tag D; committee member suggesting the next agenda'),
    301: ('FRA', 'm', 'vendor tag E'), 303: ('UNK', 'm', 'two-word remark'), 304: ('FRA', 'm', 'vendor tag E; after adjournment'),
}

# Name and term fixes: (rule, regex, replacement). Applied in order; every change is logged.
RULES = [
    ('courtneidge', r'\bEmily Courtenage\b', '[Emily Courtneidge]'),
    ('franco', r'\bJohn Franco\b', '[Jon Franco]'),
    ('chase-miller', r'\bChase Miller\b', '[Chase-Miller]'),
    ('wang', r'\bChair Wong\b', 'Chair [Wang]'),
    ('splitt', r'\bDirector Split\b', 'Director [Splitt]'),
    ('depass', r'\bDirector DePasquale\b', 'Director [DePass]'),
    ('depass', r'\bthis director to pass\b', 'this [Director DePass]'),
    ('sullivan', r'\bDirector Patty Smith\b', 'Director Patty Smith [likely Patte Sullivan]'),
    ('rosanne', r'\bRoseanne\b', '[Rosanne]'),
    ('leavitt', r'\bFrank Levitt\b', '[Frank Leavitt]'),
    ('buno', r'\bChief Jay Buno\b', 'Chief [Jey Buno]'),
    ('buno', r"\bChief, uh, D'Uno\b", 'Chief, uh, [Buno]'),
    ('buno', r'\bChief Bruno\b', 'Chief [Buno]'),
    ('buno', r'\b(have|what|know,) Jay\b', r'\1 [Jey]'),
    ('holmes', r'\bfrom Home Structures\b', 'from [Holmes] Structures'),
    ('tririga', r'\b(?:TriRega|Truriga)\b', '[TRIRIGA]'),
    ('ida-b-wells', r'\bIdyllwhee Wells\b', '[Ida B.] Wells'),
    ('grice-adair', r'\bGraysidair\b', '[Grice Adair]'),
    ('powell-park', r'\bTurf Pal Park\b', 'Turf [Powell] Park'),
    ('west-sylvan', r'\bWes Sylvan\b', '[West] Sylvan'),
    ('steffek', r'\bMegan Stepek\b', '[Megan Steffek]'),
    ('blancher', r'\bJenna Blanchard\b', '[Jenna Blancher]'),
    ('abernethy', r'\bAbernathy\b', '[Abernethy]'),
    ('arleta', r'\b(?:Arlita|Arletta)\b', '[Arleta]'),
    ('arleta', r'\bour LIDA\b', 'our [Arleta]'),
    ('duniway', r'\bDunaway\b', '[Duniway]'),
    ('rieke', r'\b(?:Reekie|Rickey|Ricci)\b', '[Rieke]'),
    ('rigler', r'\bWriggler\b', '[Rigler]'),
    ('ockley-green', r'\bAkeley Green\b', '[Ockley] Green'),
    ('chavez', r'\bCesar Chavez\b', '[César Chávez]'),
    ('chavez', r'\bVestal, Chavez\b', 'Vestal, [Chávez]'),
    ('whitman', r'\bconcerns about women\b', 'concerns about [Whitman]'),
]
REDACT = []  # (rule, regex, replacement) for children's names; none were spoken in this meeting

SEGS = [  # id, title, start seconds
    ('pre', 'Before the meeting', 0),
    ('open', 'Call to order and introductions', 1798),
    ('pc', 'Public comment', 1904),
    ('follow', 'Follow-up: Powell Park and West Sylvan fields', 2758),
    ('wins', 'Departmental wins', 3230),
    ('process', 'Readiness process and functional capacity', 3729),
    ('sites', 'School-by-school readiness (21 receiving sites)', 4241),
    ('ada', 'ADA and accessibility', 5369),
    ('seismic', 'Seismic funds under Scenarios A and B', 5420),
    ('qa', 'Next steps and committee questions', 5840),
    ('close', 'Next agenda and adjournment', 7254),
]
TAGS = {
    'sped': ('Special education', r'special ed|SPED|learning center|focus classroom|sensory|regulation space|IEP|SES|ISC|deaf|hard of hearing'),
    'capacity': ('Space & capacity', r'capacity|classrooms?\b|square f|modular|portable|utilization|walkthrough|walked'),
    'seismic': ('Seismic', r'seismic|unreinforced|URM|retrofit|building part'),
    'transport': ('Transportation & traffic', r'bus(es|ing)?\b|transportation|traffic|Safe Routes|parking'),
    'nutrition': ('Kitchens & nutrition', r'nutrition|oven|warming cabinet|kitchen|cafeteria|dishwasher'),
    'fields': ('Athletic fields', r'Powell Park|West\]? Sylvan|turf|softball|baseball|athletic|field'),
    'data': ('Data accuracy & LRFP', r'long-range facilit|LRFP|typo|inconsistent|discrepanc|inaccura|accurate'),
    'access': ('Accessibility', r'accessib|elevator|ADA\b|wheelchair'),
    'bond': ('Bond & funding', r'\bbond\b|grant|funding|funds|deferred maintenance'),
    'process': ('Process & recommendation', r'recommendation|readiness factor|engagement|November 17|the 17th|final packet|phase-in'),
}
SCHOOLS = ['Abernethy', 'Arleta', 'Atkinson', 'Beach', 'Beverly Cleary', 'Boise', 'Brentwood', 'Capitol Hill', 'Chávez', 'Chief Joseph',
           'Creston', 'Duniway', 'George', 'Glencoe', 'Hayhurst', 'Hosford', 'Kelly', 'Lincoln', 'Maplewood', 'Markham', 'Marysville',
           'MLC', 'Mount Tabor', 'Ockley', 'Rieke', 'Rigler', 'Rosa Parks', 'Rose City Park', 'Sitton', 'Vestal', 'West Sylvan',
           'Whitman', 'Woodmere', 'Ainsworth', 'Richmond', 'Cleveland', 'Wells', 'Vernon']
SCHOOL_RE = {'Chávez': r'Ch[aá]vez', 'Chief Joseph': r'Chief Jo(seph|e)\b', 'Mount Tabor': r'Mount Tabor|Mt\.? Tabor',
             'Ockley': r'Ockley', 'George': r'\bGeorge\b', 'Boise': r'\bBoise\b', 'Beach': r'\b[Bb]each\b(?! funding)|Beach seismic',
             'Wells': r'Ida B\.\] Wells|Wells\b', 'Lincoln': r'\bLincoln\b', 'Kelly': r'\bKelly\b'}

KEYS = [  # raw turn, label, quote (as it reads after corrections)
    (21, 'Maplewood parent: Hayhurst and Rieke "could run out of space"', 'If Maplewood closes, Hayhurst and [Rieke] could run out of space.'),
    (49, 'Commenter: Vestal listed with 18 accessible ground-floor classrooms', 'Vestal is listed as having 18 accessible ground floor classrooms when there are only 10.'),
    (94, 'Engelsman: bring Powell Park parties to the IGA committee', 'it sounds like every time I hear, um, an update it\'s someone else isn\'t doing something'),
    (122, 'Engelsman: Woodmere roofing work is not a "win"', "I don't consider that necessarily a departmental win"),
    (123, 'Franco: "over a billion dollars in deferred maintenance"', 'We have over a billion dollars in deferred maintenance.'),
    (132, 'Franco: walkthroughs of 21 buildings after the scenarios', 'did in-person walkthroughs with principals and other staff of 21 buildings.'),
    (132, 'Franco: special education rooms "set aside" from functional capacity', "they're set aside from the general instructional functional capacity"),
    (159, 'George rated not yet ready (PE space)', 'So we did list this, list this as not yet ready to receive.'),
    (160, 'Hayhurst historic peak corrected to 499', "the largest historic enrollment was not 650, it's actually 499 because Odyssey was in a sense counted with Hayhurst."),
    (162, 'Franco: Hayhurst "is ready" from a facilities perspective', 'But we feel, uh, Hayhurst from a facilities perspective is ready.'),
    (166, 'Engelsman: Hosford classroom count differs from the LRFP', 'on the long-range facility plan, Hosford has 32 classrooms'),
    (168, 'Markham rated not yet ready (transportation)', 'so Markham is another one we have, we have outlined this as not yet ready.'),
    (171, 'Coonrod: Markham traffic would back up', 'the increase in numbers would make it so we would be backing up down Capitol'),
    (183, 'Armstrong: readiness factors decide the recommendation list', "there are several readiness factors that have to be met either for '27-'28 or for '28-'29."),
    (201, 'Eggers: Scenario A seismic money moves to receiving schools', 'There are seismic funds for Rose City Park park and beach that will be reallocated'),
    (204, 'Eggers: 45% of students in building parts rated 9.0+', "it's 45% for building parts greater than 9.0"),
    (219, 'Buno: special-ed space use had not been published', 'specific space usage'),
    (239, 'Buno: special-ed students counted in both capacities', 'So students are included in both counts.'),
    (243, 'Evenson: the LRFP counts the gym as a classroom', 'I think in the long-range facility plan, the gymnasium is counted as a classroom.'),
    (245, 'Evenson: smaller flex rooms left out of classroom counts', 'and so we did not count them in our classroom counts.'),
    (255, 'Franco: Atkinson not walked because projections are below capacity', "they weren't prioritized to do a walkthrough."),
    (262, 'Franco: other walkthroughs only after the Nov 17 recommendation', "we won't have time to do the walkthroughs before the materials"),
]


def hms(s):
    s = int(s)
    return f'{s // 3600}:{s % 3600 // 60:02d}:{s % 60:02d}'


def build_turns():
    d = json.load(open(RAW))
    words = [w for p in d['paragraphs'] for w in p['words']]
    turns = []
    for w in words:
        if turns and turns[-1]['tag'] == w['speaker'] and w['start'] - turns[-1]['end'] < 4000:
            turns[-1]['w'].append(w); turns[-1]['end'] = w['end']
        else:
            turns.append(dict(tag=w['speaker'], start=w['start'], end=w['end'], w=[w]))
    return d, words, turns


def fix(text, ts, corr):
    for rule, rx, rep in REDACT + RULES:
        def sub(m):
            new = m.expand(rep)
            corr.append(dict(file=f'{STEM}.txt', timestamp=ts, rule=rule, original=m.group(0), fix=new))
            return new
        text = re.sub(rx, sub, text)
    return text


def main(stage):
    d, words, raw = build_turns()
    corr, rows = [], []
    for i, t in enumerate(raw):
        sp, conf, ev = OVR.get(i) or DEFAULT[t['tag']]
        ts = hms(t['start'] / 1000)
        text = fix(' '.join(w['text'] for w in t['w']), ts, corr)
        rows.append(dict(i=i, s=t['start'] / 1000, e=t['end'] / 1000, p=sp, c=conf, ev=ev, tag=t['tag'], x=text, w=t['w']))
    # merge consecutive turns by the same assigned speaker
    turns = []
    for r in rows:
        if turns and turns[-1]['p'] == r['p'] and r['s'] - turns[-1]['e'] < 4:
            T = turns[-1]; T['x'] += ' ' + r['x']; T['e'] = r['e']; T['w'] += r['w']; T['raw'].append(r['i']); T['tags'].add(r['tag'])
            T['c'] = min(T['c'], r['c'], key='lmh'.index)
        else:
            turns.append(dict(s=r['s'], e=r['e'], p=r['p'], c=r['c'], ev=r['ev'], x=r['x'], w=list(r['w']), raw=[r['i']], tags={r['tag']}))
    rawpos = {i: k for k, T in enumerate(turns) for i in T['raw']}

    # text file
    hdr = (f'# 2026-11-09 Board of Education Facilities Improvement and Oversight Committee: speaker-checked transcript\n'
           f'# Video: https://www.youtube.com/watch?v={VID}  (BoardBook meeting {MTG})\n'
           f'# Source: vendor speech-to-text paragraph export (sources/youtube/vendor_transcripts/{STEM}.paragraphs.json), supplied by the\n'
           f'#   repository owner 2026-11-09. Speakers re-assigned by reading the transcript (evidence: turns_{STEM}.csv).\n'
           f'# Format: [H:MM:SS] Name (role) {{confidence if not high}}: words. Fixes in [brackets] (corrections_{STEM}.csv).\n\n')
    lines = []
    for T in turns:
        n, r, k = PEOPLE[T['p']]
        c = '' if T['c'] == 'h' else (' {medium}' if T['c'] == 'm' else ' {low}')
        lines.append(f"[{hms(T['s'])}] {n} ({r}){c}: {T['x']}")
    (OUT / f'{STEM}.txt').write_text(hdr + '\n'.join(lines) + '\n')

    with open(OUT / f'turns_{STEM}.csv', 'w', newline='') as f:
        w = csv.writer(f); w.writerow(['start', 'end', 'seconds', 'speaker', 'role', 'confidence', 'evidence', 'vendor_tag', 'vendor_turns'])
        for T in turns:
            w.writerow([hms(T['s']), hms(T['e']), int(T['s']), PEOPLE[T['p']][0], PEOPLE[T['p']][1], {'h': 'high', 'm': 'medium', 'l': 'low'}[T['c']],
                        T['ev'], '+'.join(sorted(T['tags'])), ' '.join(map(str, T['raw']))])
    with open(OUT / f'speakers_{STEM}.csv', 'w', newline='') as f:
        w = csv.writer(f); w.writerow(['id', 'label', 'role', 'kind', 'turns', 'words', 'first_turn'])
        for pid, (n, r, k) in PEOPLE.items():
            ts = [T for T in turns if T['p'] == pid]
            if ts: w.writerow([pid, n, r, k, len(ts), sum(len(T['x'].split()) for T in ts), hms(ts[0]['s'])])
    with open(OUT / f'corrections_{STEM}.csv', 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=['file', 'timestamp', 'rule', 'original', 'fix']); w.writeheader(); w.writerows(corr)

    # caption-style copy for tools/window.py and search (staged into sources/)
    cap = Path(stage) / 'youtube/transcripts'; cap.mkdir(parents=True, exist_ok=True)
    lines_tsv, chunk = [], []
    for wd in words:
        chunk.append(wd)
        if len(chunk) >= 12 or wd['text'][-1:] in '.?!' and len(chunk) >= 5:
            lines_tsv.append((chunk[0]['start'], chunk[-1]['end'] - chunk[0]['start'], ' '.join(x['text'] for x in chunk))); chunk = []
    if chunk: lines_tsv.append((chunk[0]['start'], chunk[-1]['end'] - chunk[0]['start'], ' '.join(x['text'] for x in chunk)))
    (cap / f'{STEM}.tsv').write_text('start_ms\tduration_ms\ttext\n' + '\n'.join(f'{a}\t{b}\t{t}' for a, b, t in lines_tsv) + '\n')
    title = '2026-11-09  Board of Education’s Facilities Improvement and Oversight Committee'
    (cap / f'{STEM}.txt').write_text(
        f'# {title}\n# Video: https://www.youtube.com/watch?v={VID}\n'
        f'# Source: NOT YouTube captions. Word-level speech-to-text export (sources/youtube/vendor_transcripts/{STEM}.paragraphs.json),\n'
        f'#   supplied by the repository owner 2026-11-09; the vendor\'s words regrouped into caption-length lines. Speaker-labeled copy:\n'
        f'#   analysis/speaker_transcripts/{STEM}.txt\n# BoardBook meeting(s): {DATE}|{MTG}\n'
        f'# Link to a moment: https://www.youtube.com/watch?v={VID}&t=<seconds>s\n\n'
        + '\n'.join(f'[{hms(a / 1000)}] {t}' for a, b, t in lines_tsv) + '\n')
    (cap / f'{STEM}.meta.json').write_text(json.dumps({
        'id': VID, 'fetched_at': '2026-11-10T03:30:00Z',
        'meta': {'videoId': VID, 'title': title, 'lengthSeconds': str(round(d['audio_duration'])), 'author': 'PPS Board of Education', 'uploadDate': DATE},
        'meetings': f'{DATE}|{MTG}', 'caption_kind': 'vendor_stt', 'caption_lang': 'en', 'n_lines': len(lines_tsv),
        'fetch_method': f'Word-level speech-to-text paragraph export with automatic speaker tags (paragraphs.json, model {d.get("speech_model_used")}), supplied by the repository owner 2026-11-09; raw file archived at sources/youtube/vendor_transcripts/{STEM}.paragraphs.json. Title from YouTube oEmbed 2026-11-10; length = the export\'s audio_duration.',
        'url': f'https://www.youtube.com/watch?v={VID}', 'boardbook_meetings': [[DATE, MTG]]}, indent=1))

    # html page data
    def seg_of(s):
        g = SEGS[0][0]
        for sid, _, st in SEGS:
            if s >= st: g = sid
        return g
    keyd = {}
    for ri, label, q in KEYS:
        k = rawpos[ri]; T = turns[k]
        pos = T['x'].find(q)
        assert pos >= 0, (ri, q)
        widx = len(T['x'][:pos].split())
        qs = int(T['w'][min(widx, len(T['w']) - 1)]['start'] / 1000)
        if k in keyd: label = keyd[k][0] + '; ' + label  # two key moments in one turn: keep the first quote, join labels
        keyd.setdefault(k, (label, q, qs)); keyd[k] = (label, keyd[k][1], keyd[k][2])
    out = []
    for k, T in enumerate(turns):
        tg = [t for t, (lab, rx) in TAGS.items() if re.search(rx, T['x'], re.I)]
        sc = [s for s in SCHOOLS if re.search(SCHOOL_RE.get(s, r'\b' + re.escape(s) + r'\b'), T['x'])]
        r = dict(s=int(T['s']), p=T['p'], c=T['c'], g=seg_of(T['s']), x=T['x'], tg=tg, sc=sc, k='')
        if k in keyd: r.update(k=keyd[k][0], q=keyd[k][1], qs=keyd[k][2])
        out.append(r)
    data = dict(people={p: dict(n=n, r=r, k=kk) for p, (n, r, kk) in PEOPLE.items()},
                segs=[[a, b, c] for a, b, c in SEGS], tags={k: v[0] for k, v in TAGS.items()}, rows=out)
    tpl = (OUT / '2026-10-20_xByUlijpcnE_transcript.html').read_text()
    i = tpl.find('<script id="data"'); j = tpl.find('</script>', i)
    page = tpl[:i] + '<script id="data" type="application/json">' + json.dumps(data, ensure_ascii=False).replace('</', '<\\/') + tpl[j:]
    reps = [
        ('<title>Oct 20 Board Work Session Transcript</title>', '<title>Nov 9 Facilities Committee Transcript</title>'),
        ('<h1>Work Session, October 20, 2026: full transcript</h1>', '<h1>Facilities Improvement and Oversight Committee, November 9, 2026: full transcript</h1>'),
        ('Benson High School auditorium. Agenda: public comment, Cleveland-at-Marshall transportation, the bond performance audit, the rightsizing update (KPIs and equity analysis of Scenarios A and B), the Division 22 report and the consent agenda.',
         'Committee chair Michelle DePass with Director Engelsman and the student representative; Chair Wang and Vice-Chair Chase-Miller joined online. Agenda: public comment (Maplewood/Hayhurst capacity, athletic fields, facilities data accuracy), departmental wins, and the rightsizing school-readiness review: how functional capacity is set, walkthroughs of 21 receiving schools, and seismic funds under Scenarios A and B.'),
        ('xByUlijpcnE', VID),
        ('<b>6:57</b> video', '<b>2:03</b> video'),
        ('oct20-filters', 'nov9-fio-filters'),
        ('placeholder="Search the transcript (e.g. Maplewood, DLI, 223 FTE)"', 'placeholder="Search the transcript (e.g. Hayhurst, special ed, walkthrough)"'),
        ('<span style="--c:var(--guest)">Guests (auditors, TriMet, committees)</span><span style="--c:var(--official)">Elected and union officials</span>',
         '<span style="--c:var(--guest)">Consultant (seismic engineer)</span>'),
    ]
    for a, b in reps:
        assert a in page, a[:60]
        page = page.replace(a, b)
    (OUT / f'{STEM}_transcript.html').write_text(page)
    st = (OUT / '2026-10-20_xByUlijpcnE_transcript_standalone.html').read_text()
    head = st[:st.find('<title>')]
    head = head.replace('October 20, 2026 Portland Public Schools Board of Education work session', 'November 9, 2026 Portland Public Schools Facilities Improvement and Oversight Committee meeting')
    body = page.replace('<meta name="claude:viewport-fit-sides" content="cover">\n', '').replace('<header class="top">', '</head>\n<body>\n<header class="top">', 1)
    (OUT / f'{STEM}_transcript_standalone.html').write_text(head + body.rstrip() + '\n</body>\n</html>\n')
    print('turns', len(turns), 'raw', len(raw), 'corrections', len(corr), 'keys', len(keyd))


if __name__ == '__main__':
    main(sys.argv[1])
