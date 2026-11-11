#!/usr/bin/env python3
"""Build the speaker-checked transcript of the Nov 10, 2026 Teaching, Learning, and Enrollment (TLE) Committee meeting
(video V6r7UqxJ53s, BoardBook 776248) from the vendor paragraph export (sources/youtube/vendor_transcripts/
2026-11-10_V6r7UqxJ53s.paragraphs.json).

Writes, under analysis/speaker_transcripts/:
  2026-11-10_V6r7UqxJ53s.txt, turns_/speakers_/corrections_2026-11-10_V6r7UqxJ53s.csv,
  2026-11-10_V6r7UqxJ53s_transcript.html (artifact page) and _standalone.html (self-hosting copy)
and, into a staging folder given as argv[1] (then brought into sources/ with tools/safe_copy.py), the caption-style copy
  youtube/transcripts/2026-11-10_V6r7UqxJ53s.{tsv,txt,meta.json}.

Speaker attribution: the vendor's letter tags were reused for different people (e.g. "E" is the vice-chair's
self-introduction, the board manager reading the sign-up list and then Sabrina Wood for the rest of the meeting; "H" is
the first student commenter, Chief Buno and Vice-Chair Chase-Miller's questions). Every turn was re-assigned by reading
the transcript; DEFAULT/OVR/SPLIT hold the evidence. Run from the repo root.

Privacy: members of the public are labelled "Public commenter N (description)"; adults' own spoken self-introductions stay
in the text. The first commenter is a high-school student (a minor), so his name is redacted everywhere it is spoken.
"""
import csv, json, re, sys, html
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
VID, DATE, MTG = 'V6r7UqxJ53s', '2026-11-10', '776248'
RAW = ROOT / f'sources/youtube/vendor_transcripts/{DATE}_{VID}.paragraphs.json'
OUT = ROOT / 'analysis/speaker_transcripts'
STEM = f'{DATE}_{VID}'

PEOPLE = {  # id: (name, role, kind)
    'LAF': ('Virginia La Forte', 'Board member, Zone 5; TLE Committee chair', 'board'),
    'SPL': ('Christy Splitt', 'Board member, Zone 1; TLE Committee member', 'board'),
    'CM': ('Rashelle Chase-Miller', 'Board Vice-Chair, Zone 4; online', 'board'),
    'COOK': ('Leonie Cook', 'Student representative, McDaniel junior', 'board'),
    'SCH': ('Mel Schuller', 'Student representative, Benson senior', 'board'),
    'ARM': ('Kimberlee Armstrong', 'Superintendent', 'staff'),
    'HOW': ('Kristina Howard', 'Senior Chief of Academics; committee staff liaison', 'staff'),
    'BUNO': ('Jey Buno', 'Chief of Student Support Services; introduced as Chief of Educational Services', 'staff'),
    'WOOD': ('Sabrina Wood', 'Senior Director, Special Education', 'staff'),
    'CHA': ('Dr. Kelli Charles', 'Interim Chief of Accountability, Equity, and Continuous Improvement', 'staff'),
    'FLO': ('Will Flores', 'Director, Multilingual Services / DLI', 'staff'),
    'YEE': ('Angela Yee', 'Assistant Director, Secondary Multilingual Services', 'staff'),
    'PAP': ('Alayna Papaiacovou', 'Assistant Director, K-5 Multilingual Services', 'staff'),
    'CAL': ('Margaret Calvert', 'School Planning & Modernization (rightsizing data modeling)', 'staff'),
    'CLERK': ('Rosanne Powell', 'Board Manager', 'staff'),
    'LEGAL': ('Andrea', 'Senior Legal Counsel; surname not stated', 'staff'),
    'PC1': ('Public commenter 1', 'High-school student; former King Mandarin immersion student', 'public'),
    'PC2': ('Public commenter 2', 'PPS parent', 'public'),
    'PC3': ('Public commenter 3', 'James John DLI parent', 'public'),
    'PC4': ('Public commenter 4', 'James John DLI parent', 'public'),
    'PC5': ('Public commenter 5', 'MLC parent; Special Education PTSA board member', 'public'),
    'PC6': ('Public commenter 6', 'Peninsula parent; special-education occupational therapist', 'public'),
    'PC7': ('Public commenter 7', 'Vietnamese DLI parent', 'public'),
    'PC8': ('Public commenter 8', 'MLK parent', 'public'),
    'PC9': ('Public commenter 9', 'Special Education PTSA president; Franklin and Vestal parent', 'public'),
    'PC10': ('Public commenter 10', 'Atkinson Spanish DLI parent', 'public'),
    'PC11': ('Public commenter 11', 'Virtual commenter on special education', 'public'),
    'UNK': ('Unidentified', 'Speaker not identifiable from the recording', 'other'),
}

# Default speaker for each vendor tag (the person who holds that tag for most of the meeting), then per-turn overrides.
DEFAULT = {
    'A': ('LAF', 'h', 'Chair: calls the meeting to order (0:22:22) and runs it throughout; addressed as "Director [La Forte]"'),
    'B': ('COOK', 'm', 'vendor tag B; Cook introduces herself with this tag (0:23:01)'),
    'C': ('SCH', 'h', 'self-introduction: "My name is Mel [Schuller]" (0:23:06)'),
    'D': ('SPL', 'h', 'self-introduction (0:23:12); addressed as "Director [Splitt]" (2:49:25)'),
    'E': ('WOOD', 'h', 'Buno: "I\'ll hand it to, um, Sabrina to get us started" (0:56:23); she then presents (0:57:55)'),
    'F': ('HOW', 'h', 'self-introduction: "I\'m [Kristina] Howard ... Senior Chief of Academics" (0:24:30)'),
    'G': ('ARM', 'h', 'chair welcomes Superintendent Armstrong (0:49:18) and this voice replies; speaks as superintendent throughout'),
    'H': ('BUNO', 'h', 'Howard: "starting with, um, Chief [Jey] Buno" (0:52:49); this voice then begins the presentation (0:55:44)'),
    'I': ('PC9', 'h', 'public commenter self-identifies (0:44:48)'),
    'J': ('PC1', 'h', 'public commenter self-identifies (0:25:00)'),
    'K': ('PAP', 'm', 'K-5 multilingual lead (introduced by Dr. Charles, 2:26:59): speaks of K-5 ELD "as Will was speaking" (2:37:41) and of being an assistant principal at Bridger'),
    'L': ('PC8', 'h', 'public commenter self-identifies (0:41:46)'),
    'M': ('PC2', 'h', 'public commenter self-identifies (0:27:14)'),
    'N': ('UNK', 'm', 'vendor tag N is used for several short remarks'),
    'O': ('PC3', 'h', 'public commenter self-identifies (0:29:46)'),
    'P': ('PC4', 'h', 'public commenter self-identifies (0:32:19)'),
    'Q': ('PC5', 'h', 'public commenter self-identifies (0:35:17)'),
    'R': ('PC6', 'h', 'public commenter self-identifies (0:37:49)'),
    'S': ('PC7', 'h', 'public commenter self-identifies (0:39:45)'),
    'T': ('PC10', 'h', 'public commenter self-identifies (0:47:12)'),
    'U': ('CAL', 'h', 'Armstrong: "Margaret Calvert, who is happy to join and speak to it" (3:04:58); this voice answers "Director [La Forte]" (3:05:27); Papaiacovou later adds "to what Margaret was sharing" (3:16:20)'),
    'V': ('FLO', 'h', 'DLI director introduced by Dr. Charles; Papaiacovou refers to him as "Will" (2:37:41); "As a Latino man myself" (2:40:34)'),
    'W': ('YEE', 'm', 'by elimination: the third presenter Dr. Charles introduced (secondary multilingual lead), distinct voice from Flores and Papaiacovou'),
}
U_ = ('UNK', 'm', 'short remark; voice not identifiable')
OVR = {  # raw turn number: (speaker, confidence, evidence)
    1: ('COOK', 'h', 'self-introduction: "my name is Leonie Cook and I\'m a junior at McDaniel High School"'),
    5: ('CM', 'h', 'self-introduction: "[Rashelle Chase-Miller], uh, board vice chair"'),
    7: ('CLERK', 'h', 'chair: "[Rosanne], who do we have signed up to speak first?"; reads the sign-up list'),
    11: U_, 12: ('PC1', 'm', 'commenter stepping up; spells his name two turns later'),
    13: ('CLERK', 'm', 'asks the commenter to spell his last name, as the board manager does for each speaker'),
    14: U_, 16: U_, 18: U_, 19: U_,
    23: ('CLERK', 'h', 'reads the next names on the sign-up list'),
    24: U_, 25: U_, 29: U_, 32: U_,
    35: ('PC9', 'm', 'mid-comment, between two turns of the same commenter'),
    38: U_, 41: U_, 42: ('UNK', 'm', 'online participant unmuting'),
    43: ('LEGAL', 'h', 'self-introduction: "I\'m Andrea, senior legal counsel"'),
    45: ('CLERK', 'h', 'addresses "Director [La Forte]" and reports the virtual sign-up; the chair then hands the meeting to "[Rosanne]"'),
    46: ('PC11', 'h', 'virtual public commenter self-identifies (0:50:26)'),
    56: U_, 58: U_, 64: U_, 76: U_, 87: U_, 90: U_, 91: U_, 96: U_, 105: U_, 107: U_, 116: U_, 124: U_, 127: U_,
    130: U_,
    132: ('SCH', 'm', 'student representative asked for questions by the chair; the other representative (Cook) asks hers at 2:00:06'),
    134: ('BUNO', 'm', 'one-word remark, vendor tag H'),
    136: U_, 140: U_, 143: U_, 150: U_, 155: U_,
    156: ('CM', 'h', 'chair: "we\'ve got Vice Chair [Chase-Miller] online. She has her hand up" (2:14:11); "I have 4 questions"'),
    159: U_,
    160: ('CM', 'h', 'continues her four questions (second of the vendor turns merged under tag H)'),
    161: U_,
    162: ('CM', 'h', '"And last question" of her four'),
    174: U_, 177: U_,
    180: ('CHA', 'h', 'Howard: "turn it over to Uh, Dr. Charles, who\'s the interim chief equity, accountability ..." (2:26:32); introduces the DLI team'),
    184: U_, 191: U_,
    196: ('CHA', 'm', 'vendor tag N (Dr. Charles); takes the King-to-Boise-Eliot transition question'),
    197: ('CHA', 'm', 'same voice continues'),
    199: U_, 204: U_, 209: U_, 212: U_, 215: U_, 220: U_, 227: U_, 232: U_, 235: U_, 239: U_, 241: U_, 268: U_,
    273: ('CM', 'm', 'reply after the chair asks Director [Chase-Miller] online whether she has questions'),
    275: U_,
}
# Vendor turns holding two or more voices: raw turn -> [(phrase that starts the next part, speaker, confidence, evidence)]
SPLIT = {
    45: [("I'm just doing really terrible job", 'LAF', 'h', 'chair apologizes for running the meeting and hands over to "[Rosanne]"')],
    132: [("Yeah, I think that's a good question.", 'WOOD', 'h', 'answer in "3 layers" (repeated at 1:58:04 under her tag E)')],
    156: [('Yeah, so yeah, to do the projections', 'BUNO', 'm', 'staff answer to the weighted-model question, same vendor tag as Buno'),
          ('Okay, thank you. Um, next question', 'CM', 'h', 'Chase-Miller resumes her list of questions')],
    160: [('Yeah, we are working right now', 'BUNO', 'm', 'staff answer on CRIS accessibility, same vendor tag as Buno')],
}

# Name and term fixes: (rule, regex, replacement). Applied in order; every change is logged.
RULES = [
    ('la-forte', r'\b(?:LaForte|LaFort|LaFord)\b', '[La Forte]'),
    ('splitt', r'\bChristy Split\b', 'Christy [Splitt]'),
    ('splitt', r'\bDirector Splitz\b', 'Director [Splitt]'),
    ('splitt', r'\bDirector Split\b', 'Director [Splitt]'),
    ('chase-miller', r'\bRochelle Chase Miller\b', '[Rashelle Chase-Miller]'),
    ('chase-miller', r'\bChase Miller\b', '[Chase-Miller]'),
    ('schuller', r'\bMel Schuler\b', 'Mel [Schuller]'),
    ('rosanne', r'\b(?:Roseanne|Rosanna)\b', '[Rosanne]'),
    ('howard', r'\bChristina\b', '[Kristina]'),
    ('howard', r'\bmaking Kristen nervous\b', 'making [Kristina] nervous'),
    ('buno', r'\bJay\b', '[Jey]'),
    ('papaiacovou', r'\bElena Papea-Cobu\b', '[Alayna Papaiacovou]'),
    ('van-buecken', r'\bBeth Van Beuken\b', 'Beth [Van Buecken]'),
    ('soong', r'\bPatrick Sung\b', 'Patrick [Soong]'),
    ('septsa', r'\bSEPSA\b', '[SEPTSA]'),
    ('stephenson', r'\bStevenson\b', '[Stephenson]'),
    ('sitton', r"\bSittin'", '[Sitton]'),
    ('arleta', r'\bArlita\b', '[Arleta]'),
    ('arleta', r'\bour (?:Lita|Leda)\b', 'our [Arleta]'),
    ('duniway', r'\bDunaway\b', '[Duniway]'),
    ('beverly-cleary', r'\bBeverly,? [Cc]learly\b|\bBeverly Clear\b|\bBev Cleary\b', '[Beverly Cleary]'),
    ('sabin', r'\bSabine\b', '[Sabin]'),
    ('chavez', r'\bCesar Chavez\b', '[César Chávez]'),
    ('chavez', r'\bChavez\b', '[Chávez]'),
    ('boise-eliot', r'\bBoise Elliott\b', '[Boise-Eliot]'),
    ('lent', r'\b(?:LENT|Lentz|Lint)\b', '[Lent]'),
    ('rigler', r'\bWrigley\b', '[Rigler]'),
    ('james-john', r"\bJames Johns'", "[James John's]"),
    ('rosa-parks', r'\bRosa Park have\b', '[Rosa Parks] have'),
    ('west-linn-wilsonville', r'\bWest Wind-Lilsonville\b', '[West Linn-Wilsonville]'),
    ('guiding-coalition', r'\bSoutheast Gotting Coalition\b', 'Southeast [Guiding] Coalition'),
    ('cris', r'\bColumbia Regional Inclusive Service Program\b', 'Columbia Regional Inclusive [Services] Program'),
]
REDACT = []  # (rule, regex, replacement): text rules unused here; the student's name is removed word by word below
# The first public commenter is a high-school student: his name is replaced by vendor word start time (ms), so the name
# itself appears in no derived file, script or correction log. None = drop the word.
REDACT_WORDS = {1443564: '[student name],', 1444206: None, 1496759: '[student name]',
                1501227: '我叫[student name]，十一名九，年级十二生。Hello,', 1506155: '[student name].', 1506641: None}

SEGS = [  # id, title, start seconds
    ('pre', 'Before the meeting', 0),
    ('open', 'Call to order and introductions', 1342),
    ('pc', 'Public comment', 1418),
    ('sup', 'Superintendent and counsel', 2958),
    ('sped', 'Special education: framing and data', 3155),
    ('land', 'Special education program landscape', 4169),
    ('moves', 'Program moves by scenario (incl. Maplewood ISC)', 4983),
    ('dc', 'Direct-certification figures questioned', 6421),
    ('neuro', 'Neurodiversity, OSAS and transitions', 6562),
    ('qsped', 'Committee questions on special education', 7003),
    ('dli', 'Dual language immersion follow-up', 8768),
    ('qdli', 'Committee questions on DLI', 10165),
    ('close', 'Closing remarks and adjournment', 12100),
]
TAGS = {
    'sped': ('Special education', r'special ed|SPED|\bIEP|\bISC\b|\bCB\b|\bSES\b|learning center|focus (?:classroom|program)|sensory|regulation|paras?\b|paraeducator|case manager|disabilit|CRIS|deaf'),
    'dli': ('DLI & multilingual', r'\bDLI\b|dual lang|immersion|Mandarin|Spanish|Vietnamese|Japanese|Russian|bilingual|\bELD\b|multilingual|whole[- ]school model|whole language'),
    'space': ('Space & facilities', r'capacity|classrooms?\b|square f|facilit|\bspace\b|building'),
    'equity': ('Equity & segregation', r'equit|segregat|Latino|Black students|direct certification|\bDC\b|poverty|historically|students of color'),
    'access': ('Distance, transport & health', r'\bbus|transportation|commute|distance|walk|drive|freeway|air quality|diesel'),
    'budget': ('Budget & funding', r'budget|cost|million|funding|underfund|encroach|legislat|governor'),
    'outcomes': ('Outcomes data', r'OSAS|proficien|achievement|absentee|outcomes'),
    'process': ('Process & recommendation', r'recommendation|engagement|implementation plan|timeline|November 1[278]|\bvote|scenario'),
}
SCHOOLS = ['Astor', 'Atkinson', 'Beaumont', 'Benson', 'Beverly Cleary', 'Boise-Eliot', 'Bridger', 'Buckman', 'Capitol Hill', 'Chávez',
           'Creston', 'Duniway', 'Franklin', 'Glencoe', 'Hayhurst', 'Hosford', 'Irvington', 'James John', 'Jefferson', 'Kellogg',
           'Kelly', 'King', 'Lent', 'Lewis', 'Maplewood', 'Markham', 'Marysville', 'MLC', 'Mount Tabor', 'Peninsula', 'Rigler',
           'Rosa Parks', 'Rose City Park', 'Sabin', 'Scott', 'Sitton', 'Stephenson', 'Sunnyside', 'Tubman', 'Vernon', 'Vestal',
           'Whitman', 'Woodmere', 'Woodstock', 'Arleta']
SCHOOL_RE = {'Chávez': r'Ch[aá]vez', 'King': r'\bKing\b|\bMLK\b', 'Kelly': r"\bKelly's SES|\bKelly\b(?! right here)(?!'s point)",
             'Beverly Cleary': r'Beverly Cleary|\bBCS\b', 'Mount Tabor': r'Mount Tabor|Mt\.? Tabor', 'Lent': r'\bLent\b',
             'Rose City Park': r'Rose City', 'Tubman': r'Tubman', 'Boise-Eliot': r'Boise', 'Scott': r'\bScott\b(?! [A-Z])'}

KEYS = [  # raw turn (or "turn.part" for split turns), label, quote (as it reads after corrections)
    (26, 'Commenter: flexible learning spaces have "no minimum size requirement and no capacity limit"', 'have no minimum size requirement and no capacity limit'),
    (36, 'Commenter: special-education virtual engagement set for Nov 18', 'engagement on November 18th at 6 PM'),
    (48, 'Howard: leaving special-ed moves out of the regional overviews "was a misstep"', 'and this was a misstep.'),
    (79, 'Wood: "one sensory space for hundreds of students is not optimal"', 'one sensory space for hundreds of students is not optimal'),
    (85, 'Buno: Maplewood ISC classroom came from Markham in the ice storm and would "reconnect at Markham"', 'Right now, our ISC classroom at Maplewood actually used to be at Markham'),
    (85, 'Buno: Hayhurst not considered because it already houses a focus program', "The reason Hayhurst isn't considered is because Hayhurst currently houses a focus classroom program already."),
    (110, 'Buno: Stephenson CB classroom moves with the neighborhood to Capitol Hill', 'It is a 3-5 CB classroom at [Stephenson]. They will move with the neighborhood to Capitol Hill.'),
    (113, 'Splitt: Hayhurst direct-certification figure is "off by half"', "Hayhurst is like off by half. We're almost always right around 30"),
    (125, 'Buno: the same 14.8 figure appears for several schools', 'I see 14.8, 14.8, 14.8.'),
    (152, 'Splitt: would support "a significantly smaller number of mergers"; worries about losing sensory and QMHP space', 'I would support a significantly smaller number of mergers and changes'),
    (168, 'Buno: special ed encroaches on the general fund by about $70M; high-cost disability fund $55M vs. $63M submitted', 'encroach into the general fund by $70-something million, $70 million.'),
    (176, 'Armstrong: special-education detail "will be in the final recommendation"', 'it will be in the final recommendation.'),
    (201, "Yee: implementation plan with the superintendent's recommendation will ask families their fall plans", "The implementation plan to be submitted with the superintendent's recommendation will include a process and timeline for impacted families to indicate their plans for the fall."),
    (202, 'Yee: Chávez staffing "will come with the recommendation"', 'it will come with the recommendation'),
    (210, 'Splitt: what would be the harm in taking a year for DLI engagement?', 'taking a year to have more engagement'),
    (211, 'Armstrong: DLI "5 numbers: 4, 2, 1, 1, and 1"', 'keep in mind 5 numbers: 4, 2, 1, 1, and 1.'),
    (213, 'Armstrong: four Spanish DLI whole-school sites, with first choice for current DLI families', "there's 4 locations where we will have the support needed to continue dual language immersion"),
    (218, 'Armstrong: feedback "changed my thinking on some things"', "It's It's changed my thinking on some things."),
    (225, 'Armstrong: closing schools "isn\'t a significant cost savings"; program consolidation is', "closing schools isn't a significant cost savings"),
    (229, 'La Forte: Lent "backs up to a freeway"; take it out of the building inventory', 'it backs up to a freeway'),
    (237, 'La Forte: diesel-pollution studies near Lent', 'lots of studies done in that neighborhood about the diesel pollution'),
    (250, 'Armstrong: co-located DLI programs "will be dismantled"', 'Those programs will be dismantled.'),
    (258, 'Papaiacovou: Black students in MLK immersion 8% proficient in ELA, 0% in math (2025-26)', 'our Black students in the immersion program at MLK, um, 8%'),
    (267, 'La Forte: "this narrative that we have too many schools" is not true', "this narrative that we have too many schools really for a city our size, I don't think that it's true."),
    (271, 'La Forte: "definitely not 14 and it\'s definitely not 11"', "it's definitely not 14 and it's definitely not 11."),
]


def hms(s):
    s = int(s)
    return f'{s // 3600}:{s % 3600 // 60:02d}:{s % 60:02d}'


def build_turns():
    d = json.load(open(RAW))
    words = []
    for p in d['paragraphs']:
        for w in p['words']:
            if w['start'] in REDACT_WORDS:
                if REDACT_WORDS[w['start']] is None: continue
                w = dict(w, text=REDACT_WORDS[w['start']], redacted=True)
            words.append(w)
    assert sum(1 for w in words if w.get('redacted')) == sum(1 for v in REDACT_WORDS.values() if v), 'redaction word times moved'
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


def split_words(i, t):
    """Return [(part id, words, (speaker, conf, evidence))] for raw turn i."""
    first = OVR.get(i) or DEFAULT[t['tag']]
    if i not in SPLIT:
        return [(i, t['w'], first)]
    ws, parts, cut = t['w'], [], [0]
    joined = ' '.join(w['text'] for w in ws)
    for phrase, *_ in SPLIT[i]:
        pos = joined.find(phrase)
        assert pos >= 0 and (pos == 0 or joined[pos - 1] == ' '), (i, phrase)
        cut.append(len(joined[:pos].split()))
    cut.append(len(ws))
    who = [first] + [tuple(s[1:]) for s in SPLIT[i]]
    for j in range(len(who)):
        parts.append((i if j == 0 else f'{i}.{j}', ws[cut[j]:cut[j + 1]], who[j]))
    return parts


def main(stage):
    d, words, raw = build_turns()
    corr, rows = [], []
    for i, t in enumerate(raw):
        for pid, ws, (sp, conf, ev) in split_words(i, t):
            ts = hms(ws[0]['start'] / 1000)
            text = fix(' '.join(w['text'] for w in ws), ts, corr)
            for w in ws:
                if w.get('redacted'):
                    corr.append(dict(file=f'{STEM}.txt', timestamp=hms(w['start'] / 1000), rule='redact-minor', original='[withheld]', fix=w['text']))
            rows.append(dict(i=pid, s=ws[0]['start'] / 1000, e=ws[-1]['end'] / 1000, p=sp, c=conf, ev=ev, tag=t['tag'], x=text, w=ws))
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
    hdr = (f'# 2026-11-10 Board of Education Teaching, Learning, and Enrollment Committee: speaker-checked transcript\n'
           f'# Video: https://www.youtube.com/watch?v={VID}  (BoardBook meeting {MTG})\n'
           f'# Source: vendor speech-to-text paragraph export (sources/youtube/vendor_transcripts/{STEM}.paragraphs.json), supplied by the\n'
           f'#   repository owner 2026-11-10. Speakers re-assigned by reading the transcript (evidence: turns_{STEM}.csv).\n'
           f'# Format: [H:MM:SS] Name (role) {{confidence if not high}}: words. Fixes in [brackets] (corrections_{STEM}.csv).\n'
           f'# Members of the public are labelled by number; a student commenter\'s name is redacted.\n\n')
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

    # caption-style copy for tools/window.py and search (staged into sources/); the student's name is redacted here too
    cap = Path(stage) / 'youtube/transcripts'; cap.mkdir(parents=True, exist_ok=True)
    lines_tsv, chunk = [], []
    for wd in words:
        chunk.append(wd)
        if len(chunk) >= 12 or wd['text'][-1:] in '.?!' and len(chunk) >= 5:
            lines_tsv.append((chunk[0]['start'], chunk[-1]['end'] - chunk[0]['start'], ' '.join(x['text'] for x in chunk))); chunk = []
    if chunk: lines_tsv.append((chunk[0]['start'], chunk[-1]['end'] - chunk[0]['start'], ' '.join(x['text'] for x in chunk)))

    (cap / f'{STEM}.tsv').write_text('start_ms\tduration_ms\ttext\n' + '\n'.join(f'{a}\t{b}\t{t}' for a, b, t in lines_tsv) + '\n')
    title = '2026-11-10  Board of Education’s Teaching, Learning, and Enrollment Committee'
    (cap / f'{STEM}.txt').write_text(
        f'# {title}\n# Video: https://www.youtube.com/watch?v={VID}\n'
        f'# Source: NOT YouTube captions. Word-level speech-to-text export (sources/youtube/vendor_transcripts/{STEM}.paragraphs.json),\n'
        f'#   supplied by the repository owner 2026-11-10; the vendor\'s words regrouped into caption-length lines (a student commenter\'s\n'
        f'#   name redacted). Speaker-labeled copy: analysis/speaker_transcripts/{STEM}.txt\n# BoardBook meeting(s): {DATE}|{MTG}\n'
        f'# Link to a moment: https://www.youtube.com/watch?v={VID}&t=<seconds>s\n\n'
        + '\n'.join(f'[{hms(a / 1000)}] {t}' for a, b, t in lines_tsv) + '\n')
    (cap / f'{STEM}.meta.json').write_text(json.dumps({
        'id': VID, 'fetched_at': '2026-11-11T05:20:00Z',
        'meta': {'videoId': VID, 'title': title, 'lengthSeconds': str(round(d['audio_duration'])), 'author': 'PPS Board of Education', 'uploadDate': DATE},
        'meetings': f'{DATE}|{MTG}', 'caption_kind': 'vendor_stt', 'caption_lang': 'en', 'n_lines': len(lines_tsv),
        'fetch_method': f'Word-level speech-to-text paragraph export with automatic speaker tags (paragraphs.json, model {d.get("speech_model_used")}), supplied by the repository owner 2026-11-10; raw file archived at sources/youtube/vendor_transcripts/{STEM}.paragraphs.json. Title from YouTube oEmbed 2026-11-10; length = the export\'s audio_duration. A student commenter\'s name is redacted in this copy.',
        'url': f'https://www.youtube.com/watch?v={VID}', 'boardbook_meetings': [[DATE, MTG]]}, indent=1, ensure_ascii=False))

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
        if k in keyd:
            keyd[k] = (keyd[k][0] + '; ' + label, keyd[k][1], keyd[k][2])  # two key moments in one turn: keep the first quote
        else:
            keyd[k] = (label, q, qs)
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
        ('<title>Oct 20 Board Work Session Transcript</title>', '<title>Nov 10 TLE Committee Transcript</title>'),
        ('<h1>Work Session, October 20, 2026: full transcript</h1>', '<h1>Teaching, Learning, and Enrollment Committee, November 10, 2026: full transcript</h1>'),
        ('Benson High School auditorium. Agenda: public comment, Cleveland-at-Marshall transportation, the bond performance audit, the rightsizing update (KPIs and equity analysis of Scenarios A and B), the Division 22 report and the consent agenda.',
         'Committee chair Virginia La Forte with Director Splitt and student representatives Leonie Cook and Mel Schuller; Vice-Chair Chase-Miller joined online and Superintendent Armstrong attended. Agenda: public comment (DLI consolidation, special education), the rightsizing special-education presentation (where programs move under Scenarios A and B, including the Maplewood ISC classroom), and the dual language immersion follow-up. Members of the public are labelled by number; a student commenter\'s name is redacted.'),
        ('xByUlijpcnE', VID),
        ('<b>6:57</b> video', '<b>3:25</b> video'),
        ('oct20-filters', 'nov10-tle-filters'),
        ('placeholder="Search the transcript (e.g. Maplewood, DLI, 223 FTE)"', 'placeholder="Search the transcript (e.g. Maplewood, ISC, Lent, sensory)"'),
        ('<span style="--c:var(--guest)">Guests (auditors, TriMet, committees)</span><span style="--c:var(--official)">Elected and union officials</span>', ''),
    ]
    for a, b in reps:
        assert a in page, a[:60]
        page = page.replace(a, b)
    (OUT / f'{STEM}_transcript.html').write_text(page)
    st = (OUT / '2026-10-20_xByUlijpcnE_transcript_standalone.html').read_text()
    head = st[:st.find('<title>')]
    head = head.replace('October 20, 2026 Portland Public Schools Board of Education work session', 'November 10, 2026 Portland Public Schools Teaching, Learning, and Enrollment Committee meeting')
    body = page.replace('<meta name="claude:viewport-fit-sides" content="cover">\n', '').replace('<header class="top">', '</head>\n<body>\n<header class="top">', 1)
    (OUT / f'{STEM}_transcript_standalone.html').write_text(head + body.rstrip() + '\n</body>\n</html>\n')
    print('turns', len(turns), 'raw', len(raw), 'corrections', len(corr), 'keys', len(keyd))


if __name__ == '__main__':
    main(sys.argv[1])
