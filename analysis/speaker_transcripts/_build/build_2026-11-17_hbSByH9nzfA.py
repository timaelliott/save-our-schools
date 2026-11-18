#!/usr/bin/env python3
"""Build the speaker-checked transcript of the Nov 17, 2026 Board of Education work session (video hbSByH9nzfA,
BoardBook 777711) from the vendor paragraph export (sources/youtube/vendor_transcripts/2026-11-17_hbSByH9nzfA.paragraphs.json).

Writes, under analysis/speaker_transcripts/:
  2026-11-17_hbSByH9nzfA.txt, turns_/speakers_/corrections_2026-11-17_hbSByH9nzfA.csv,
  2026-11-17_hbSByH9nzfA_transcript.html (artifact page) and _standalone.html (self-hosting copy)
and, into a staging folder given as argv[1] (then brought into sources/ with tools/safe_copy.py), the caption-style copy
  youtube/transcripts/2026-11-17_hbSByH9nzfA.{tsv,txt,meta.json}.

Speaker attribution: the vendor's letter tags (A-Z, AA-AD) were reused for different people (e.g. "C" is the board
manager reading the sign-up list, then the PFSP president, then Director Splitt for the rest of the meeting; "B" is the
board manager once and then CFO Michelle Morrison). Every turn was re-assigned by reading the transcript; DEFAULT/OVR hold
the evidence. Four attributions were confirmed by the repository owner on 2026-11-18 (marked "owner"); the owner also
confirmed the first speaker is Chair Eddie Wang. Run from the repo root.

Privacy: members of the public are labelled "Public commenter N (description)"; adults' own spoken self-introductions stay
in the text. Three student commenters are children: their names are removed word by word (REDACT_WORDS) everywhere.
"""
import csv, json, re, sys, html
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
VID, DATE, MTG = 'hbSByH9nzfA', '2026-11-17', '777711'
RAW = ROOT / f'sources/youtube/vendor_transcripts/{DATE}_{VID}.paragraphs.json'
OUT = ROOT / 'analysis/speaker_transcripts'
STEM = f'{DATE}_{VID}'

PEOPLE = {  # id: (name, role, kind)
    'WANG': ('Eddie Wang', 'Board Chair', 'board'),
    'CM': ('Rashelle Chase-Miller', 'Board Vice-Chair', 'board'),
    'DEP': ('Michelle DePass', 'Board member', 'board'),
    'SPL': ('Christy Splitt', 'Board member; chair, Intergovernmental Affairs Committee', 'board'),
    'ENG': ('Stephanie Engelsman', 'Board member', 'board'),
    'LAF': ('Virginia La Forte', 'Board member', 'board'),
    'SUL': ('Patte Sullivan', 'Board member', 'board'),
    'SAN': ('Rose Sandell', 'Student representative', 'board'),
    'VOTE': ('Board (voice vote)', 'Directors answering a roll of "all in favor"', 'board'),
    'ARM': ('Kimberlee Armstrong', 'Superintendent', 'staff'),
    'FRA': ('Jon Franco', 'Senior Chief of Operations', 'staff'),
    'CAL': ('Margaret Calvert', 'Executive Director, School Planning and Modernization', 'staff'),
    'MOR': ('Michelle Morrison', 'Chief Financial Officer', 'staff'),
    'BUNO': ('Jey Buno', 'Chief of Student Support Services', 'staff'),
    'GOV': ('Ben Gurewitz', 'Senior Manager of Government Relations (surname as in the Jan 27 minutes)', 'staff'),
    'LEGAL': ('Liz Large', 'Contracted senior legal counsel', 'staff'),
    'CLERK': ('Rosanne Powell', 'Senior Board Manager', 'staff'),
    'SEIU': ('Amy Sylvia', 'SEIU Local 140 (custodial and nutrition services); Maplewood nutrition services worker', 'official'),
    'PFSP': ('Elizabeth Held', 'President, Portland Federation of School Professionals (PFSP)', 'official'),
    'PAT': ('Alisha Chavez', 'President, Portland Association of Teachers (PAT); Atkinson K-2 special education teacher', 'official'),
    'STU1': ('Student commenter 1', 'Creston 2nd grader', 'public'),
    'STU2': ('Student commenter 2', 'Lewis 4th grader', 'public'),
    'STU3': ('Student commenter 3', 'Beach 5th grader (introduced by her parent, Public commenter 9)', 'public'),
    'PC1': ('Public commenter 1', 'Former Peninsula student; speaking as a private citizen and neighbor', 'public'),
    'PC2': ('Public commenter 2', 'Mount Tabor MS PTA president, speaking as a parent; supports the recommendation', 'public'),
    'PC3': ('Public commenter 3', 'Sabin parent', 'public'),
    'PC4': ('Public commenter 4', 'Director of advocacy and engagement, Self-Enhancement Inc. (SEI); supports the recommendation', 'public'),
    'PC5': ('Public commenter 5', 'PPS parent', 'public'),
    'PC6': ('Public commenter 6', 'Rose City Park parent (English Scholars and Vietnamese DLI)', 'public'),
    'PC7': ('Public commenter 7', 'Rose City Park Vietnamese DLI kindergarten parent', 'public'),
    'PC8': ('Public commenter 8', 'Creston parent; architect', 'public'),
    'PC9': ('Public commenter 9', 'Beach parent', 'public'),
    'PC10': ('Public commenter 10', 'Irvington and Tubman parent', 'public'),
    'PC11': ('Public commenter 11', 'Consent-agenda comment on the RMC Research contract', 'public'),
    'PC12': ('Public commenter 12', 'Parent; former school enrollment forecaster (consent-agenda comment)', 'public'),
    'PC13': ('Public commenter 13', 'Comment on the legislative agenda', 'public'),
    'PC14': ('Public commenter 14', 'Duniway parent; nurse (comment on the legislative agenda)', 'public'),
    'AUD': ('Audience', 'Calls from the audience', 'other'),
    'UNK': ('Unidentified', 'Speaker not identifiable from the recording', 'other'),
}

# Default speaker for each vendor tag (the person who holds that tag for most of the meeting), then per-turn overrides.
DEFAULT = {
    'A': ('WANG', 'h', 'chair: opens the meeting, calls speakers and votes throughout; first speaker confirmed as Wang by the repository owner'),
    'B': ('MOR', 'h', 'Armstrong invites "Chief Financial Officer, Michelle Morrison" (1:22:17); this voice presents the financial update'),
    'C': ('SPL', 'h', 'chair: "Director [Splitt] moves" (1:07:25) after this voice; presents the legislative-agenda amendment; addressed as Director [Splitt] (2:27:03)'),
    'D': ('STU1', 'h', 'student commenter self-identifies (0:04:41)'),
    'E': ('STU2', 'h', 'student commenter self-identifies (0:05:30)'),
    'F': ('PC1', 'h', 'public commenter self-identifies (0:08:03)'),
    'G': ('PC2', 'h', 'public commenter self-identifies (0:10:22)'),
    'H': ('PC14', 'h', 'public commenter self-identifies (1:18:27)'),
    'I': ('PC3', 'h', 'public commenter self-identifies (0:13:49)'),
    'J': ('PC4', 'h', 'public commenter self-identifies (0:16:41)'),
    'K': ('PC5', 'h', 'public commenter self-identifies (0:20:27)'),
    'L': ('PC6', 'h', 'public commenter self-identifies (0:22:30)'),
    'M': ('PC7', 'h', 'public commenter self-identifies (0:25:37)'),
    'N': ('PC8', 'h', 'public commenter self-identifies (0:27:56)'),
    'O': ('PAT', 'h', 'self-identifies as PAT president (0:43:03)'),
    'P': ('LEGAL', 'h', 'chair: "I\'ll let Liz chime in" (4:07:17) and this voice answers on outside counsel; same voice advises on the amendment process (3:54:37)'),
    'Q': ('PC10', 'h', 'public commenter self-identifies (0:33:11)'),
    'R': ('ENG', 'h', 'Armstrong: "Director Engelsman, that you\'re hoping to see" (3:27:16) in reply to this voice; Intergovernmental Affairs member'),
    'S': ('GOV', 'h', 'self-introduction as Senior Manager of Government Relations (1:03:00)'),
    'T': ('SEIU', 'h', 'self-identifies for SEIU Local 140 (0:36:11)'),
    'U': ('CM', 'h', 'Armstrong: "the frame that um Director [Chase-Miller] put forth" (2:59:10) after this voice\'s process question; asks as the only remaining director'),
    'V': ('ARM', 'h', 'chair hands items to "Superintendent Armstrong" and this voice introduces them; speaks as superintendent throughout'),
    'W': ('DEP', 'h', 'chair: "Director DePass seconds" (0:53:54) after this voice; Armstrong: "Thank you for that question, Director DePass" (2:01:22)'),
    'X': ('PC11', 'h', 'public commenter self-identifies (0:54:33)'),
    'Y': ('PC12', 'h', 'public commenter self-identifies (0:56:24)'),
    'Z': ('CAL', 'h', 'Franco: "with me today is Margaret Calvert ... Margaret is going to uh walk us through ... the memo" (2:09:10); this voice then presents'),
    'AA': ('FRA', 'h', 'self-introduction: "My name is [Jon] Franco ... Senior Chief of Operations" (2:09:10)'),
    'AB': ('SUL', 'h', 'chair: "Director Sullivan seconds" (1:07:25) after this voice; called on as Director Sullivan (2:47:44)'),
    'AC': ('LAF', 'h', 'chair: "Director [La Forte] seconds" (1:08:30) after this voice; called on first in the financial questions (1:41:55)'),
    'AD': ('PC13', 'h', 'public commenter self-identifies (1:15:47)'),
}
U_ = ('UNK', 'm', 'short remark; voice not identifiable')
AUD_ = ('AUD', 'h', 'shout from the audience during the meeting')
VOTE_ = ('VOTE', 'm', 'answer to the chair\'s "All in favor"')
SAN_ = ('SAN', 'm', 'answer when the chair asks "Student representative?"')
CLERK_ = ('CLERK', 'h', 'board manager, addressed by the chair as "Ms. [Powell]"; reads the sign-up list')
OVR = {  # raw turn number: (speaker, confidence, evidence)
    4: ('CLERK', 'h', 'answers the chair\'s "Ms. Powell, can you call up the students"'),
    5: CLERK_, 7: ('STU1', 'm', 'continues the Creston student\'s comment ("[Creston] is the only school with STEAM days")'),
    10: ('STU2', 'h', 'self-identifies as a Lewis 4th grader'),
    13: CLERK_, 28: CLERK_, 30: U_, 46: U_, 50: CLERK_, 52: CLERK_, 54: U_, 60: CLERK_, 62: CLERK_,
    68: CLERK_, 69: ('PC9', 'h', 'self-identifies (0:30:43)'), 70: ('PC9', 'h', '"My daughter ... asked if she might speak"'),
    71: ('STU3', 'h', '"I\'m a 5th grader at Beach", introduced by Public commenter 9'),
    75: ('CLERK', 'm', 'closing thanks at the clerk\'s table'), 78: AUD_,
    80: ('PFSP', 'm', 'greeting immediately before the PFSP president\'s self-introduction'),
    81: ('PFSP', 'h', 'self-introduction: "My name is Elizabeth Held ... president of PFSP"'),
    82: ('PFSP', 'h', 'mid-sentence continuation of the PFSP list of unknowns'), 83: ('PFSP', 'h', 'continues'), 84: ('PFSP', 'h', 'continues'),
    86: ('PAT', 'h', 'self-introduction as PAT president'), 87: U_, 92: ('PAT', 'h', 'continuation of the PAT president\'s sentence'),
    101: ('CLERK', 'h', 'answers the chair\'s "Ms. Powell, are there any changes to consent agenda?"'),
    103: ('SPL', 'h', 'chair: "Director [Splitt] moves"'), 106: CLERK_, 107: CLERK_, 112: U_,
    116: ('ENG', 'm', 'director asking staff about the RMC contract; vendor tag R (Engelsman) throughout'),
    120: ('ENG', 'm', 'continues the RMC question'), 121: ('CLERK', 'm', 'clerk\'s table: "Someone\'s coming up right now"'),
    123: ('ENG', 'm', 'continues the RMC question to Chief Buno'),
    124: ('BUNO', 'h', 'owner confirmed: Chief Buno answers (Armstrong: "We have Chief Buno coming up", 1:01:20)'),
    125: ('ENG', 'm', 'continues'), 126: ('BUNO', 'h', 'owner confirmed: Buno answers the grant question'),
    127: ('ENG', 'm', 'continues'), 128: U_, 130: VOTE_, 132: SAN_, 138: U_,
    140: ('GOV', 'm', 'closing thanks right after the government-relations presentation'),
    167: U_, 170: ('CLERK', 'h', '"We have public comment" (reminds the chair)'), 172: CLERK_,
    177: ('PC14', 'm', 'two words inside Public commenter 14\'s comment'), 179: U_,
    183: ('LEGAL', 'h', 'owner confirmed: legal counsel Liz Large reminds the chair of the amendment'),
    187: ('LEGAL', 'h', 'owner confirmed: legal counsel'),
    190: VOTE_, 192: SAN_, 194: VOTE_, 196: SAN_, 212: U_, 217: U_,
    222: ('LAF', 'm', 'reply to the chair calling on Director La Forte, who then asks her questions'),
    228: ('MOR', 'm', 'acknowledgement during La Forte\'s question to the CFO'), 234: U_, 242: U_, 249: U_,
    252: U_, 255: ('SPL', 'm', 'end of Splitt\'s question ("Does that make sense?")'),
    268: ('MOR', 'm', 'agreement during Sullivan\'s remark to the CFO'), 275: U_, 276: U_, 287: U_,
    293: ('SAN', 'm', 'answer to the chair\'s "Student rep? All good?"'), 295: U_, 299: U_, 300: U_, 303: U_, 309: U_,
    311: U_, 313: U_, 319: U_, 329: U_,
    341: ('CAL', 'm', 'confirms Calvert\'s answer on Buckman lottery students'), 344: U_, 345: U_, 352: U_, 360: U_,
    365: ('ENG', 'm', 'vendor tag R; short question to Splitt'), 375: U_, 382: U_, 383: U_, 385: U_, 389: U_,
    404: AUD_, 408: U_,
    414: ('WANG', 'm', 'begins "I don\'t have-"; the chair completes "I have the answer for that tonight"'),
    420: U_, 429: U_, 437: U_, 440: U_, 453: U_, 458: U_, 459: AUD_, 463: AUD_, 465: U_, 467: U_, 476: U_, 479: U_,
    481: U_, 482: U_, 484: U_, 487: U_, 490: U_, 493: U_, 497: U_,
    501: ('CAL', 'm', 'false start of Calvert\'s "I\'m hearing-" (repeated in her next turn)'), 506: U_,
    512: ('FRA', 'm', 'answer to Engelsman\'s readiness question about Glencoe and CRIS, addressed to Franco\'s facilities walkthroughs'),
    516: U_, 518: U_, 520: U_, 521: U_,
    523: ('SAN', 'h', 'owner confirmed: student representative Rose Sandell asks her question'),
    524: ('SAN', 'h', 'owner confirmed: Sandell continues'), 525: ('SAN', 'h', 'owner confirmed: Sandell continues'),
    528: U_, 530: U_, 534: U_, 551: ('SPL', 'm', 'vendor tag C (Splitt)'), 554: U_, 563: U_,
    568: ('SPL', 'h', 'owner confirmed: Splitt notes the Dec 8 executive-session hold'),
    578: ('SPL', 'm', 'vendor tag C (Splitt)'), 580: U_, 583: ('SUL', 'm', 'vendor tag AB'), 587: U_, 592: U_, 602: U_,
}
SPLIT = {}

# Name and term fixes: (rule, regex, replacement). Applied in order; every change is logged.
RULES = [
    ('wang', r'\bWong\b', '[Wang]'),
    ('splitt', r'\bDirector (?:Split|Slipp)\b', 'Director [Splitt]'),
    ('la-forte', r'\b(?:LaFort|LaFour)\b', '[La Forte]'),
    ('engelsman', r'\bInglesman\b', '[Engelsman]'),
    ('chase-miller', r'\bChase Miller\b', '[Chase-Miller]'),
    ('armstrong', r'\bAramshaw\b', '[Armstrong]'),
    ('armstrong', r'\bKimberly Armstrong\b', '[Kimberlee] Armstrong'),
    ('franco', r'\bJohn Franco\b', '[Jon] Franco'),
    ('franco', r'\bDr\. Frankel\b', 'Dr. [Franco]'),
    ('sandell', r'\bZandell\b', '[Sandell]'),
    ('powell', r'\bMs\. Fowl\b', 'Ms. [Powell]'),
    ('rosanne', r'\bRoseanne\b', '[Rosanne]'),
    ('morrison', r'\bMichelle Morris\b', 'Michelle [Morrison]'),
    ('gurewitz', r'\bBen (?:Gurrut|Gerwitz)\b', 'Ben [Gurewitz]'),
    ('alisha-chavez', r'\bAlicia Chavez\b', '[Alisha] Chavez'),
    ('chavez', r'\bCesar Chavez\b', '[César Chávez]'),
    ('chavez', r'(?<!Alisha\] )\bChavez\b', '[Chávez]'),
    ('duniway', r'\bDunaway\b', '[Duniway]'),
    ('abernethy', r'\bAbernathy\b', '[Abernethy]'),
    ('stephenson', r'\bStevenson\b', '[Stephenson]'),
    ('creston', r'\bQuesten\b', '[Creston]'),
    ('ockley-green', r'\bOakleigh\b', '[Ockley]'),
    ('faubion', r'\bPhoebian\b', '[Faubion]'),
    ('glencoe', r'\bGlen Coe\b', '[Glencoe]'),
    ('sitton', r'\bSeton\b', '[Sitton]'),
    ('cris', r'\bChris\b(?!tmas)', '[CRIS]'),
    ('title-i', r'\bTidal\b', '[Title I]'),
    ('segc', r'\bSCGC\b|\bSEG\b', '[SEGC]'),
    ('sei', r'\bSCI supports\b', '[SEI] supports'),
    ('tle', r'\bTLA\b', '[TLE]'),
    ('weidler', r'\bWidler\b', '[Weidler]'),
]
REDACT = []
# Three student commenters are children: their names are replaced by vendor word start time (ms), so the names themselves
# appear in no derived file, script or correction log. None = drop the word.
REDACT_WORDS = {246916: '[student name],', 247816: None, 248717: '[student name],', 250160: None,
                251490: '[student name].', 251961: None, 283036: '[student name],', 283446: None,
                331928: '[student name],', 332243: None, 1847420: '[student name]'}

SEGS = [  # id, title, start seconds
    ('open', 'Call to order and meeting rules', 0),
    ('stu', 'Student and public comment', 245),
    ('union', 'Comments from union partners', 2134),
    ('consent', 'Consent agenda (RMC contract question)', 3179),
    ('legis', '2027 legislative agenda (Res. 7400, amended)', 3741),
    ('fin', 'Financial update ($65.2M gap, PERS)', 4917),
    ('pres', 'Rightsizing recommendation: orientation to the binder', 7364),
    ('qspl', 'Board questions: Splitt and Sullivan', 8823),
    ('proc', 'How the board will handle amendments', 10427),
    ('qwang', 'Questions: Wang', 11825),
    ('qeng', 'Questions and process concerns: Engelsman', 12070),
    ('qdep', 'Comments: DePass and Sandell', 13256),
    ('qlaf', 'La Forte; amendment timeline set', 13756),
    ('close', 'Future agenda items and adjournment', 14688),
]
TAGS = {
    'amend': ('Amendments & process', r'amendment|December (?:1st|2nd|3rd|8th|15th)|the 15th|the 30th|\bvote\b|timeline|listening session|vet|no surprises|special meeting'),
    'budget': ('Budget & PERS', r'budget|PERS|deficit|\$\d|million|reserve|contingency|fund balance|pension|Stability Fund'),
    'dli': ('DLI & multilingual', r'\bDLI\b|dual lang|immersion|Mandarin|Spanish|Vietnamese|Japanese|Russian|hub model|multilingual'),
    'sped': ('Special education', r'special ed|\bIEP|\bSCS\b|\bSES\b|focus (?:classroom|program)|disabilit|\bCRIS\b|deaf|hard of hearing'),
    'space': ('Space & facilities', r'capacity|classrooms?\b|floor plan|gymnasium|facilit|\bspace\b|building|walk-?through|retrofit'),
    'staffing': ('Staffing & class size', r'staffing|\bFTE\b|class size|blends?\b|merger|administrators of color|counselor|librar'),
    'equity': ('Equity & focal students', r'equit|Title (?:One|I)|poverty|focal|students of color|administrators of color|east side|west side|affluent'),
    'access': ('Transportation', r'\bbus|transportation|commute|route|walk(?:ing|able)?\b'),
    'legis': ('Legislative agenda', r'legislat|Salem|governor|lobby|unfunded mandate'),
}
SCHOOLS = ['Abernethy', 'Atkinson', 'Beach', 'Beverly Cleary', 'Brentwood', 'Buckman', 'Chávez', 'Chief Joseph', 'Clark', 'Creston',
           'Duniway', 'Faubion', 'Forest Park', 'Glencoe', 'Irvington', 'James John', 'Kelly', 'King', 'Lent', 'Lewis', 'Lincoln',
           'Maplewood', 'Marysville', 'MLC', 'Mount Tabor', 'Ockley Green', 'Odyssey', 'Peninsula', 'Richmond', 'Rigler',
           'Rosa Parks', 'Rose City Park', 'Sabin', 'Scott', 'Sellwood', 'Sitton', 'Skyline', 'Smith', 'Stephenson', 'Sunnyside',
           'Tubman', 'Vestal', 'Whitman', 'Woodmere', 'Woodstock']
SCHOOL_RE = {'Chávez': r'Ch[aá]vez(?! president)(?!, president)', 'King': r'\bKing\b|\bMLK\b', 'Chief Joseph': r'Chief Jo', 'Mount Tabor': r'Mount Tabor|Mt\.? Tabor',
             'Rose City Park': r'Rose City|\bRCP\b', 'Tubman': r'Tubman', 'Scott': r'\bScott\b', 'Ockley Green': r'Ockley',
             'Smith': r'\bSmith\b(?! is here)(?! coming)', 'Lincoln': r'\bLincoln\b', 'Clark': r'\bClark\b(?! uh who)|\bClark uh who'}

KEYS = [  # raw turn, label, quote (as it reads after corrections)
    (20, 'Mt. Tabor PTA president supports the recommendation: "the state is not coming to save us"', 'And the state is not coming to save us.'),
    (56, 'Rose City Park parent: apply the same formula and keep RCP\'s seismic retrofit funded', "keep RCP's retrofit funded"),
    (79, 'SEIU: closed schools like Smith still need daily checks; "10 more empty buildings"', 'It does not make sense to add 10 more empty buildings to the list.'),
    (81, 'PFSP president: "we don\'t know what real well-resourced schools mean"', "we don't know what real well-resourced schools mean"),
    (90, 'PAT president: "You don\'t build the plane while children are on board"', "You don't build the plane while children are on board"),
    (111, 'Former forecaster: 45 of 82 schools missed by more than 3%; the model assumes no families leave', 'The current model assumption of no loss of families is wholly unrealistic.'),
    (169, 'Legislative agenda amended (Splitt) and adopted 7-0', 'the board will now vote on Resolution 7400'),
    (218, 'Morrison: rightsizing is not a way to close the budget gap', 'We have to close that gap whether there are any changes or not.'),
    (220, 'Armstrong: about $200M reduced over six years; "we are at an emergency state"', 'So we are at an emergency state.'),
    (274, 'Armstrong: closing buildings makes little difference to the deficit; FTE is reinvested', "I don't think that you would see much a difference"),
    (302, 'Armstrong: memo financial table corrected after a Chase-Miller question; change log to be posted', "We did, we caught the error, and we've updated that in Board Book."),
    (312, 'Calvert: rightsizing savings are minimal and do not count toward the $65M', 'this is not uh contributing to the reduction of the $65 million'),
    (314, 'Calvert: formal student enrollment verification in January', 'formal student enrollment verification'),
    (339, 'Calvert: Buckman lottery students move to Sunnyside as a group', 'Buckman Lottery students would move to Sunnyside as a group.'),
    (361, 'Calvert: correction, Lewis students go to Duniway and then Sellwood (not Brentwood)', 'to show that Lewis goes to [Duniway] and they go to Sellwood.'),
    (378, 'Splitt: is DLI "over-serving affluent white families"? Asks for floor plans', 'if we are over-serving affluent white families in our DLI programs'),
    (379, 'Franco: floor plans not published for school-safety reasons; offers walkthrough detail', 'just from a school safety perspective'),
    (390, 'Sullivan: making César Chávez a hub creates problems for its English program moving to Rosa Parks', 'in trying to make [César Chávez] better'),
    (402, 'Armstrong: three possible outcomes: approve, amend and approve, or defer', "there'll either be an affirmative vote"),
    (443, 'Calvert: about 48 hours to model one change', 'takes to run a full analysis is about 48 hours'),
    (448, 'Wang: SEGC boundary modeling took the contractor over a week', 'took over a week to model those'),
    (454, 'Wang: individual directors cannot direct staff time to model amendments', "individual board members don't have any power"),
    (513, 'Engelsman: assumed PPS would use outside experts; "B felt very much just like A light"', 'B felt very much just like A light.'),
    (515, 'Armstrong: "I stand behind my team"; the decision is now the board\'s', 'I stand behind my team and their work'),
    (517, 'Engelsman: learned of up to 20 closures from the news after the August 7-0 vote', 'to go from 5 to 10 to 20 overnight'),
    (522, 'DePass: SEGC audit lessons; 3 of the 5 first-year closures are led by principals of color', 'So of the 5 schools.'),
    (524, 'Sandell: why are most closures on the east side?', 'why most of the schools on the list are on the east side'),
    (526, 'Calvert: west-side changes would have split elementary attendance areas; west-side boundaries to be reviewed', 'both both of the changes on the west side for the elementary included splits'),
    (527, 'Armstrong: Splitt\'s Scenario D called for a regional boundary review; west-side growth pockets', 'one of those did call for a regional boundary uh review'),
    (535, 'La Forte: "still struggling with the hub model"; plans boundary-exception amendments', "I'm really still struggling with, with the hub model"),
    (544, 'Wang: submit amendments to the board manager by Nov 30', 'submit that to [Rosanne] by the 30th'),
    (579, 'Agreed plan: amendments by Nov 30, discussion Dec 1, possible meeting Dec 8, vote Dec 15', 'submit amendment amendments by the 30th'),
    (603, 'Splitt: add the board to the Signal fact-finding (DePass suggestion); counsel to propose a structure', 'add the board to the fact-finding'),
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
    hdr = (f'# 2026-11-17 Board of Education work session: speaker-checked transcript\n'
           f'# Video: https://www.youtube.com/watch?v={VID}  (BoardBook meeting {MTG})\n'
           f'# Source: vendor speech-to-text paragraph export (sources/youtube/vendor_transcripts/{STEM}.paragraphs.json), supplied by the\n'
           f'#   repository owner 2026-11-18. Speakers re-assigned by reading the transcript (evidence: turns_{STEM}.csv).\n'
           f'# Format: [H:MM:SS] Name (role) {{confidence if not high}}: words. Fixes in [brackets] (corrections_{STEM}.csv).\n'
           f'# Members of the public are labelled by number; the names of three child commenters are redacted.\n\n')
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

    # caption-style copy for tools/window.py and search (staged into sources/); the children's names are redacted here too
    cap = Path(stage) / 'youtube/transcripts'; cap.mkdir(parents=True, exist_ok=True)
    lines_tsv, chunk = [], []
    for wd in words:
        chunk.append(wd)
        if len(chunk) >= 12 or wd['text'][-1:] in '.?!' and len(chunk) >= 5:
            lines_tsv.append((chunk[0]['start'], chunk[-1]['end'] - chunk[0]['start'], ' '.join(x['text'] for x in chunk))); chunk = []
    if chunk: lines_tsv.append((chunk[0]['start'], chunk[-1]['end'] - chunk[0]['start'], ' '.join(x['text'] for x in chunk)))

    (cap / f'{STEM}.tsv').write_text('start_ms\tduration_ms\ttext\n' + '\n'.join(f'{a}\t{b}\t{t}' for a, b, t in lines_tsv) + '\n')
    title = '2026-11-17 Board of Education Work Session'
    (cap / f'{STEM}.txt').write_text(
        f'# {title}\n# Video: https://www.youtube.com/watch?v={VID}\n'
        f'# Source: NOT YouTube captions. Word-level speech-to-text export (sources/youtube/vendor_transcripts/{STEM}.paragraphs.json),\n'
        f'#   supplied by the repository owner 2026-11-18; the vendor\'s words regrouped into caption-length lines (child commenters\'\n'
        f'#   names redacted). Speaker-labeled copy: analysis/speaker_transcripts/{STEM}.txt\n# BoardBook meeting(s): {DATE}|{MTG}\n'
        f'# Link to a moment: https://www.youtube.com/watch?v={VID}&t=<seconds>s\n\n'
        + '\n'.join(f'[{hms(a / 1000)}] {t}' for a, b, t in lines_tsv) + '\n')
    (cap / f'{STEM}.meta.json').write_text(json.dumps({
        'id': VID, 'fetched_at': '2026-11-18T17:00:00Z',
        'meta': {'videoId': VID, 'title': title, 'lengthSeconds': str(round(d['audio_duration'])), 'author': 'PPS Board of Education', 'uploadDate': DATE},
        'meetings': f'{DATE}|{MTG}', 'caption_kind': 'vendor_stt', 'caption_lang': 'en', 'n_lines': len(lines_tsv),
        'fetch_method': f'Word-level speech-to-text paragraph export with automatic speaker tags (paragraphs.json, model {d.get("speech_model_used")}), supplied by the repository owner 2026-11-18; raw file archived at sources/youtube/vendor_transcripts/{STEM}.paragraphs.json. Title from YouTube oEmbed 2026-11-18; length = the export\'s audio_duration. Child commenters\' names are redacted in this copy.',
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
        ('<title>Oct 20 Board Work Session Transcript</title>', '<title>Nov 17 Board Work Session Transcript</title>'),
        ('<h1>Work Session, October 20, 2026: full transcript</h1>', '<h1>Work Session, November 17, 2026: full transcript</h1>'),
        ('Benson High School auditorium. Agenda: public comment, Cleveland-at-Marshall transportation, the bond performance audit, the rightsizing update (KPIs and equity analysis of Scenarios A and B), the Division 22 report and the consent agenda.',
         'Benson High School auditorium. Agenda: student and public comment, union partners, the consent agenda, the 2027 legislative agenda (Res. 7400), the financial update, and the first board session on Superintendent Armstrong\'s Nov 13 rightsizing recommendation, including how directors will bring amendments before the Dec 15 vote. Members of the public are labelled by number; child commenters\' names are redacted.'),
        ('xByUlijpcnE', VID),
        ('<b>6:57</b> video', '<b>4:08</b> video'),
        ('oct20-filters', 'nov17-ws-filters'),
        ('placeholder="Search the transcript (e.g. Maplewood, DLI, 223 FTE)"', 'placeholder="Search the transcript (e.g. amendment, hub model, PERS, Beach)"'),
        ('<span style="--c:var(--guest)">Guests (auditors, TriMet, committees)</span>', ''),
    ]
    for a, b in reps:
        assert a in page, a[:60]
        page = page.replace(a, b)
    (OUT / f'{STEM}_transcript.html').write_text(page)
    st = (OUT / '2026-10-20_xByUlijpcnE_transcript_standalone.html').read_text()
    head = st[:st.find('<title>')]
    head = head.replace('October 20, 2026 Portland Public Schools Board of Education work session', 'November 17, 2026 Portland Public Schools Board of Education work session')
    body = page.replace('<meta name="claude:viewport-fit-sides" content="cover">\n', '').replace('<header class="top">', '</head>\n<body>\n<header class="top">', 1)
    (OUT / f'{STEM}_transcript_standalone.html').write_text(head + body.rstrip() + '\n</body>\n</html>\n')
    print('turns', len(turns), 'raw', len(raw), 'corrections', len(corr), 'keys', len(keyd))


if __name__ == '__main__':
    main(sys.argv[1])
