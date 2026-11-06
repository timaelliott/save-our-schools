"""Builds rightsizing-record/index.html (public page). Content is defined here; citations resolve via tools/linkify.py.
Run: python3 rightsizing-record/_build/build.py
Source brief: analysis/topics/equity_claims_vs_record.md"""
import sys, re, html, json
import os
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
import linkify as L

VID = {
 'xByUlijpcnE': ('Oct 20, 2026', 'Board work session'),
 '9kX3vnfRlvY': ('Nov 4, 2026', 'Board meeting'),
 'zOUH2Jq7Owo': ('Oct 6, 2026', 'Board meeting'),
 'h_0YMlJnXPk': ('Apr 22, 2026', 'Community engagement session'),
 'kdPfX6KH05c': ('Oct 13, 2026', 'OPB Think Out Loud'),
 'uAf7l-ChjFo': ('Sept 15, 2026', 'Board meeting'),
 '5RMfvT-sAPU': ('Sept 1, 2026', 'Board meeting'),
 'YUCokoJ7-n0': ('June 10, 2025', 'TSCC budget hearing'),
 'zxaXALjzumk': ('Feb 4, 2025', 'Board meeting'),
 'XENAU3DUf5g': ('Mar 18, 2025', 'Board work session'),
 'QIfmGcbkkLE': ('Mar 31, 2026', 'Board work session'),
 'Uxh6Jm_xFYY': ('May 6, 2025', 'Board meeting'),
 'kf21uJr0fcQ': ('Nov 10, 2025', 'Facilities committee'),
 '-NpJZaLR81U': ('Jan 27, 2026', 'Board work session'),
 'XThyXtVtJto': ('Dec 9, 2025', 'Facilities committee'),
 'HGAs0lyZ6kw': ('Sept 9, 2025', 'Board meeting'),
 'AH3wdS1A3sM': ('Apr 14, 2026', 'Board meeting'),
 'SPc05NM0oYs': ('Mar 12, 2026', 'Teaching & Learning committee'),
}
DOC = {
 '14511742': 'PPS rightsizing presentation, Oct 6, 2026',
 '14493920': 'PPS Board Q&A, Oct 1, 2026',
 '14618390': 'PPS Board Q&A, Oct 30, 2026',
 '14615901': 'PPS rightsizing presentation, Nov 4, 2026',
 '14430171': 'PPS decision framework, Sept 15, 2026',
 '3997427': 'SEGC Equity Audit report, Aug 2026',
 '3997428': 'SEGC school-by-school analysis, Aug 2026',
 '3997425': 'PPS rightsizing presentation, Aug 4, 2026',
 '3997426': 'PPS rightsizing memo, Aug 4, 2026',
 '3997273': 'Resolution 7307 (guiding principles), May 26, 2026',
 '3998077': 'Board minutes, Apr 14, 2026',
 '3997157': 'PPS enrollment & utilization table, Apr 2026',
 '14509719': 'Scenario release memo, Oct 5, 2026',
 '14505788': 'District-wide scenarios, Oct 4, 2026',
 '3990267': 'PPS seismic presentation, Mar 2026',
 '3996450': '2020 bond seismic status report, Apr 2025',
 '3991109': 'PPS seismic risk assessment, Sept 2025',
}
def secs(ts):
    h, m, s = map(int, ts.split(':')); return h*3600+m*60+s

def esc(s): return html.escape(s, quote=True)

def src(tag, label=None):
    url = L.url_for(tag)
    if not url: raise SystemExit('no url for ' + tag)
    if label is None:
        if tag.startswith('BB:'):
            m = re.match(r'BB:(\d+)(?: p\.(\S+))?', tag)
            label = DOC[m.group(1)] + (f', p.{m.group(2)}' if m.group(2) else '')
        elif tag.startswith('PPS:'):
            m = re.search(r'school_impact/(\w+)\.pdf(?: p\.(\S+))?', tag)
            name = m.group(1).replace('_', ' ').title().replace('Dr Martin Luther King Jr', 'Dr. Martin Luther King Jr.').replace('Harriet Tubman', 'Harriet Tubman MS').replace('James John', 'James John')
            label = f'PPS family guide: {name}' + (f', p.{m.group(2)}' if m.group(2) else '')
        else:
            label = tag
    return f'<a class="src" href="{esc(url)}" target="_blank" rel="noopener">{esc(label)}</a>'

def Q(text, who, role, vid, ts, note=''):
    date, kind = VID[vid]
    s = max(secs(ts) - 3, 0)
    yt = f'https://www.youtube.com/watch?v={vid}&t={secs(ts)}s'
    n = f' <span class="note">{esc(note)}</span>' if note else ''
    return f'''<figure class="quote">
  <blockquote>“{esc(text)}”</blockquote>
  <figcaption><span class="who">{esc(who)}</span><span class="role">{esc(role)}</span><span class="when">{esc(kind)} · {esc(date)} · {ts}</span>{n}
    <span class="actions"><button class="play" data-vid="{vid}" data-start="{s}" aria-label="Play clip of {esc(who)}">▶ Play clip</button><a href="{esc(yt)}" target="_blank" rel="noopener">YouTube ↗</a></span>
  </figcaption>
  <div class="player" hidden></div>
</figure>'''

def R(*items):  # record list; each item is html string
    return '<ul class="record">' + ''.join(f'<li>{i}</li>' for i in items) + '</ul>'

def bars(title, rows, unit='%', maxv=100):
    out = [f'<div class="bars" role="img" aria-label="{esc(title)}"><div class="bars-title">{esc(title)}</div>']
    for label, v, hl in rows:
        out.append(f'<div class="bar-row"><span class="bar-label">{esc(label)}</span><span class="bar-track"><span class="bar{" hl" if hl else ""}" style="width:{v/maxv*100:.1f}%"></span></span><span class="bar-val">{v:.1f}{unit}</span></div>')
    out.append('</div>')
    return ''.join(out)

def F(fid, title, lede, body):
    return f'<article class="finding" id="{fid}"><h3><a class="anchor" href="#{fid}">#</a>{esc(title)}</h3><p class="lede">{lede}</p>{body}</article>'

RS = ('Richard Smith', 'Senior Director, Data & Accountability')
MC = ('Margaret Calvert', 'Executive Director, School Planning & Modernization')
JF = ('Jon Franco', 'Senior Chief of Operations')
KA = ('Kimberlee Armstrong', 'Superintendent')
EW = ('Eddie Wang', 'Board Chair')
MD = ('Michelle DePass', 'Board member')
CM = ('Rashelle Chase-Miller', 'Board member (Vice-Chair from 2026)')
CS = ('Christy Splitt', 'Board member')
VL = ('Virginia La Forte', 'Board member')
SE = ('Stephanie Engelsman', 'Board member')

P = {}
# ---------------- Principle 1 ----------------
P[1] = [
F('size-not-resources', 'The headline equity number counts students in bigger buildings, not resources.',
  'PPS says every focal student group “gains” under both scenarios. The measure is the share of students in schools above the size threshold, so it rises by design when small schools close. PPS has not said what any student would gain.',
  Q('Doing nothing leaves about half of all students and between 54 and 59% of each focal group in a school that is not sustainable. Both scenarios improve results for every group, and every focal group gains more than students overall.', *MC, 'xByUlijpcnE', '4:08:11') +
  Q("we're not going to necessarily see more", *RS, '9kX3vnfRlvY', '4:40:44', 'Asked whether consolidated schools would be better resourced.') +
  R(f'A “sustainable” school is one above the enrollment threshold, 360 students for K-5. {src("BB:14511742 p.10")}',
    f'PPS’s own written answer: “there is no data supporting that smaller schools have higher test scores. Test scores are better predicted by socio-economic status than school size.” {src("BB:14493920 p.27")}',
    f'“Class size capping is not a part of the rightsizing conversation.” {src("BB:14493920 p.33")}',
    f'Board questions “What specific resources will students gain in the receiving school?” and “Will class sizes get larger, smaller, or remain the same?” were still marked “In process” on Oct 30. {src("BB:14618390 p.37")} {src("BB:14618390 p.38")}')),
F('thresholds', 'The size thresholds behind the closures are called a stopgap by the staff who set them.',
  'Every closure starts from a size floor: 360 students for K-5, 500 for middle schools. Senior staff describe those numbers as temporary and possibly wrong.',
  Q("I do want to say this with this caveat. This is a bridge ... This is not what we would say is ideal state, but it's definitely a bridge.", *JF, 'zOUH2Jq7Owo', '1:38:03', 'Presenting the 360 / 500 / 1,100 thresholds.') +
  Q('I am actually concerned that they\'re low.', *MC, '9kX3vnfRlvY', '4:37:43', 'Asked by Director La Forte whether the 360/500 thresholds are right.') +
  R(f'The 360 and 500 floors come from the state’s Quality Education Model prototype school; the K-8 floor reuses the middle-school number. {src("BB:3997426 p.2")}',
    f'The Board-commissioned SEGC equity audit proposed floors of about 450, 600 and 650. {src("BB:3997427 p.146")}')),
F('savings', 'The savings story changes with the audience, and the net number still does not exist.',
  'Leaders have said closures are “not a cost-saving strategy,” then cited $14 million in savings, while a Board member’s request for net savings stayed unanswered.',
  Q('closing schools is not a cost-saving strategy.', *KA, 'h_0YMlJnXPk', '1:26:04') +
  Q("we are not um exclaiming some you know huge dollar amount from closures and savings because we know that first of all our educators and staff generally move with students", *KA, 'zOUH2Jq7Owo', '3:44:23') +
  Q('we are reducing the expense of the district so that we can get to a point where we no longer have to worry about budget cuts anymore.', *EW, 'kdPfX6KH05c', '0:19:07', 'One minute later in the same interview:') +
  Q("we're not um closing schools to save on the budget.", *EW, 'kdPfX6KH05c', '0:20:08') +
  Q('Scenario A, which models 14 school building closures, estimates approximately $14 million in operational savings.', *KA, 'xByUlijpcnE', '1:14:59') +
  R(f'Ten days later, Director Engelsman’s question “What is the actual net savings to closing Sellwood? What are the net savings to closing any school?” was still “In process.” {src("BB:14618390 p.35")}',
    f'Staff concede closed buildings keep costing money (utilities, security, insurance, repairs) and that “financial estimates will need to account for ongoing and one-time costs when calculating net savings.” {src("BB:14618390 p.39")}',
    f'The SEGC audit warns that districts “often overestimate the savings produced by school closures and underestimate the costs.” {src("BB:3997427 p.147")}')),
F('families-leaving', 'Families leaving the district: a reason to stop a move in 2025, accepted in 2026, and not modeled.',
  'Every family that leaves takes state funding with it. PPS has no grade 1–12 data on how many families a closure drives out, and the last Southeast boundary process saw faster enrollment loss.',
  Q('moving them 11 miles away a student body of 400 we just thought we\'re just going to lose students.', *MD, 'XThyXtVtJto', '0:40:14', 'Explaining why a temporary move for Jefferson High School was rejected.') +
  Q("We're not forcing anybody to stay in our district", *MD, 'uAf7l-ChjFo', '4:00:20') +
  Q('What we don\'t have is a capture rate. The data is not available for a grades one through 12 capture rate ... Is it true that some kids may leave the district if we do right sizing? That is true.', *RS, '9kX3vnfRlvY', '5:01:12') +
  R(f'SEGC audit: SEGC elementary enrollment fell “on average, by 20%” from 2020–21 to 2024–25, “compared to 14% among elementary schools outside SEGC.” {src("BB:3997427 p.6")}')),
]
# ---------------- Principle 2 ----------------
P[2] = [
F('seismic', 'Earthquake money went to schools now proposed to close. High-risk receiving schools have no retrofit plan.',
  'Board members said seismic risk should guide which buildings stay open, and warned about schools serving students of color. The scenarios close recently retrofitted schools and send students to high-risk buildings with no retrofit planned.',
  Q('if we\'re looking at changes to school models do we or even consolidations of schools we want to put investments into schools that could potentially be consolidated.', 'Dan Jung', 'then Chief Operating Officer', 'Uxh6Jm_xFYY', '2:31:54') +
  Q("I'm concerned if we're not thinking about equity um that we're going to end up in a situation where uh the schools that are the schools that kids of color go to are the ones that collapse.", *CM, 'kf21uJr0fcQ', '1:00:44') +
  Q('consolidate into safer schools, closing the more dangerous schools and getting uh more for our money.', *CM, 'kf21uJr0fcQ', '1:07:50') +
  Q("we have a couple of school communities who have basically been told that they're going to get seismic improvements meaning that they won't close.", *MD, '-NpJZaLR81U', '1:35:42') +
  R(f'Closure-list schools with seismic money: a full campus retrofit at Rose City Park (closes in Scenario A) and a targeted retrofit at Beach (closes in both). {src("BB:3990267 p.9")}',
    f'Woodmere (closes in both): roof seismic and masonry work, construction summer 2026. {src("BB:3990267 p.22")}',
    f'Marysville (closes in both): a seismic upgrade budgeted at about $6.75 million for design and construction. {src("BB:3996450 p.1")}',
    f'Receiving schools with high seismic-risk scores and no retrofit planned include Dr. Martin Luther King Jr. (score 9.0; 51.1% poverty, 63.0% underserved racial groups) {src("BB:3991109 p.213")} {src("PPS:pps_net/rightsizing/school_impact/dr_martin_luther_king_jr.pdf p.4")}, Brentwood MS (9.0; 57.5% poverty) {src("BB:3991109 p.214")} {src("PPS:pps_net/rightsizing/school_impact/brentwood.pdf p.4")}, Ockley Green (9.1) {src("BB:3991109 p.229")} and Rieke (9.6) {src("BB:3991109 p.233")}.')),
F('travel', 'Longer trips, and no transportation plan.',
  'The schools proposed to close are the ones children can walk to (see Educational Options). PPS has published no bus routes, ride times or transportation costs.',
  Q("only 12% of the students would live within one and a half miles of Tubman. Has there been any recon? I mean, that tells me that the school is not in the right location for the boundary that's being created.", *VL, '9kX3vnfRlvY', '4:30:10') +
  Q('We have not um incorporated it into this plan.', *MC, '9kX3vnfRlvY', '4:30:34', 'Answering whether relocating Tubman was considered.') +
  R(f'Harriet Tubman MS (50.5% students from underserved racial groups): students living within a mile fall from 23.7% to 12.5% under both scenarios. {src("PPS:pps_net/rightsizing/school_impact/harriet_tubman.pdf p.4")}',
    f'Transportation and ride times “will require further implementation planning.” {src("BB:14509719 p.2")}',
    f'A Board question on “transportation costs, travel-time burdens, and safety considerations” was still “In process” on Oct 30. {src("BB:14618390 p.38")}',
    f'The SEGC audit found “the burden of travel falling hardest on families with the least means.” {src("BB:3997427 p.18")}')),
]
# ---------------- Principle 3 ----------------
P[3] = [
F('walkable', 'The schools proposed to close are the district’s most walkable.',
  'Families ranked “Strong Neighborhood Schools” first among the four principles. The closure list is concentrated in the schools where most students live within a mile.',
  bars('Students living within 1 mile of school (average of each school’s share)', [
    ('Closing in Scenario A', 78.6, True), ('Closing in Scenario B', 80.4, True), ('All other schools (A)', 55.2, False), ('All other schools (B)', 56.0, False)]) +
  R(f'In PPS’s survey, 41% ranked “Strong Neighborhood Schools” first, versus 17% for the Equity Lens. {src("BB:14615901 p.12")}',
    f'Rosa Parks, the highest-poverty receiving school (79.4% poverty; 81.9% underserved racial groups), goes from 100% of students within a mile to 55.2%. {src("PPS:pps_net/rightsizing/school_impact/rosa_parks.pdf p.3")} {src("PPS:pps_net/rightsizing/school_impact/rosa_parks.pdf p.4")}',
    f'Dr. Martin Luther King Jr.: 100% → 64.7%. {src("PPS:pps_net/rightsizing/school_impact/dr_martin_luther_king_jr.pdf p.4")} Scott (51.9% poverty), Scenario A: 91.9% → 46.7%. {src("PPS:pps_net/rightsizing/school_impact/scott.pdf p.4")}',
    'Averages are simple averages of the share printed in each school’s PPS family guide (“No changes” column), for every school with a figure.')),
F('focus-options', 'Focus options kept, neighborhood schools closed, and no reason given for Sunnyside.',
  'PPS’s memo said no focus-option school would close. Sunnyside’s focus option ends, Buckman (an arts focus school) closes, and staff could not say why Sunnyside was picked.',
  Q("I'm just struggling with why we're leaving focus options intact that are primarily in one area of the city and closing neighborhood schools.", *VL, '9kX3vnfRlvY', '4:17:00') +
  Q('so Sunnyside just happened to be one of the ones just arbitrarily because some of them needed to go and some needed to stay.', *CS, 'zOUH2Jq7Owo', '3:36:01', 'Pressing staff after asking why Sunnyside was selected.') +
  Q("So Bridger as an example, the reason why we leave Bridger with the focus option program in this is because Bridger's gone through substantial amount of changes through the Southeast Guiding Coalition process.", *RS, 'zOUH2Jq7Owo', '3:36:11', 'The reply covered Bridger, Winterhaven, ACCESS and Odyssey, but not Sunnyside.') +
  Q("I know it's an arbit somewhat arbitrary of an answer for our Sunnyside friends.", *CS, 'zOUH2Jq7Owo', '3:36:46') +
  R(f'Scenario memo: “No alternative or focus option school closure is proposed.” {src("BB:14509719 p.2")}',
    f'Staff’s own summary of the surveys: “Surveys say that the proposed scenarios over-emphasize choice programs.” {src("BB:14615901 p.13")}')),
F('open-process', '“We have to be open” became a mandate to close, with the number set before the criteria.',
  'In 2025 the Superintendent said the process might close no schools. By April 2026 the Board required closures, and the count rose after Board members called the first range too low.',
  Q("It could be that, you know, it's recommended that no schools are closed and it's more of a reconfiguration of the programs that we have", *KA, 'YUCokoJ7-n0', '0:52:55') +
  Q("in a process like boundaries and school closure, we can't begin with the end in mind. We have to be open.", *KA, 'YUCokoJ7-n0', '0:56:56') +
  R(f'Resolution 7296 (Apr 14, 2026) says rightsizing “will include school and program closures, consolidations, or boundary changes.” A motion to change “will” to “may” failed 2–5. {src("BB:3998077 p.4")}',
    f'On Sept 1, 2026 the Superintendent said she first offered 5 to 12 closures and Board members told her it was too low; the scenarios proposed 11 to 14. <a class="src" href="https://www.youtube.com/watch?v=5RMfvT-sAPU&t=7906s" target="_blank" rel="noopener">Board meeting, Sept 1, 2026, 2:11:46</a> {src("BB:14505788 p.2")}')),
]
# ---------------- Principle 4 ----------------
P[4] = [
F('disabilities', 'Closures fall hardest on students with disabilities.',
  'Students receiving special education are one of PPS’s focal groups. The schools proposed to close have a noticeably higher share of them than the rest of the district.',
  bars('Students receiving special education (average of each school’s share)', [
    ('Closing in Scenario A', 21.6, True), ('Closing in Scenario B', 22.6, True), ('All other schools', 17.9, False)], maxv=30) +
  R(f'Highest among closing schools: Creston 31.0% {src("PPS:pps_net/rightsizing/school_impact/creston.pdf p.4")}, Woodmere 30.4% {src("PPS:pps_net/rightsizing/school_impact/woodmere.pdf p.4")}, Peninsula 30.1% {src("PPS:pps_net/rightsizing/school_impact/peninsula.pdf p.4")}.',
    f'A Board question on how PPS will protect “student belonging, cultural identity, and school-community relationships, especially for racially minoritized students” was still “In process” on Oct 30. {src("BB:14618390 p.38")}')),
F('title-i', 'Title I schools: staff name the pattern, then repeat it.',
  'Six Title I schools close in both scenarios, and receiving schools lose Title I status. A Board member’s question about why was still unanswered on Oct 30.',
  Q("we often disrupt and displace title one schools more than higher [SES] schools. So we're conscious of both pieces.", *MC, '9kX3vnfRlvY', '4:33:58') +
  Q("They could lose the title one funding. That is true. I don't want to say they wouldn't.", *RS, '9kX3vnfRlvY', '4:32:33') +
  R(f'Title I schools closing in both scenarios: Beach, Buckman, James John, Marysville, Peninsula and Woodmere. In Scenario B that is 6 of 11 closures (55%), against 35 of 82 schools district-wide (43%). {src("BB:3997157 p.1")}',
    f'Woodmere: 59.0% poverty, 25.1% multilingual, 30.4% special education. {src("PPS:pps_net/rightsizing/school_impact/woodmere.pdf p.4")} Marysville: 58.3% poverty. {src("PPS:pps_net/rightsizing/school_impact/marysville.pdf p.4")} James John: 54.5% poverty, 63.8% underserved racial groups. {src("PPS:pps_net/rightsizing/school_impact/james_john.pdf p.4")}',
    f'Brentwood MS goes from 57.5% poverty and Title I to 32.1% (A) or 30.6% (B) and no Title I. {src("PPS:pps_net/rightsizing/school_impact/brentwood.pdf p.4")} Markham loses Title I under Scenario A. {src("PPS:pps_net/rightsizing/school_impact/markham.pdf p.4")}',
    f'“Why do we have a list that has close to 50% Title I schools closing?” (Director Engelsman): “In process.” {src("BB:14618390 p.42")}',
    f'The KPI “Number of Title I and CSI/TSI schools impacted” was listed in the framework but never reported. {src("BB:14430171 p.20")}')),
F('segc', 'The schools PPS promised to stabilize after the last boundary process are closing.',
  'The 2021 Southeast Guiding Coalition (SEGC) process moved boundaries and programs across Southeast Portland. Leaders said lessons were learned and hard-hit communities would be protected. Marysville, Lewis and Creston, all SEGC-affected, now close.',
  Q("this was definitely a commitment the district made for five years to those schools and there's some of the lowest income schools ... Harrison Park [Marysville] Lane lent Whitman Vestal um and we'd be totally breaking our promise to those schools that we were going to provide some stabilization for five years", 'Julia Brim-Edwards', 'then Board member', 'zxaXALjzumk', '3:20:51') +
  Q('there were commitments there were promises but ... my priority is to serve uh those who are in the building ... than commitments that were made a couple of years ago with a whole different budget', *KA, 'XENAU3DUf5g', '3:17:24', 'On the same SEGC stabilization staffing.') +
  Q('The [Southeast Guiding Coalition] , I appreciate you mentioning that, will not be the model in which we deploy.', *KA, 'YUCokoJ7-n0', '0:53:58') +
  Q("as a alum of the SEGC process I'm very adamant that equity must be the outcome and not just the intention.", *EW, '5RMfvT-sAPU', '2:23:45') +
  Q("Open seats don't make every school ready. In a community that's been displaced before, where students end up is an equity decision, not just a capacity decision.", *MC, 'uAf7l-ChjFo', '2:51:46') +
  R(f'Marysville closes in both scenarios. {src("BB:3997157 p.1")} It received students displaced by SEGC. {src("BB:3997428 p.39")}',
    f'Lewis, whose projection SEGC cut from 358 to 281, closes in Scenario A. {src("BB:3997428 p.66")} Creston, also part of SEGC {src("BB:3997427 p.87")}, closes in both. {src("BB:14505788 p.2")}',
    f'Staff on the Wells-area routing: “the quantitative model optimizes for building utilization rather than non-measurable social networks.” {src("BB:14618390 p.36")}',
    f'The audit recommended tracking cumulative burden on communities. That measure is not among the KPIs. {src("BB:3997425 p.12")}')),
F('equity-analysis', 'The required equity analysis was not available while the public weighed in, and many affected families were not reached.',
  'The Board required an equity impact analysis for each scenario. Staff said it would arrive with the November recommendation, after the Oct 6–28 engagement window.',
  Q('what it produces is an equity analysis review attached to each scenario, and that will be coming forth as well in the November recommendation.', *JF, 'xByUlijpcnE', '3:58:11') +
  Q("they talked to 16 current [Hayhurst] families and none of those families even knew that this whole thing was happening", *CS, '9kX3vnfRlvY', '4:08:11', 'On a volunteer’s door-knocking at Stephens Creek Crossing, a Home Forward public-housing community moved from Hayhurst to Rieke in Scenario A.') +
  Q("too often in our history you know when we have community engagement it's often the people who can show up that we hear from the most.", *EW, 'HGAs0lyZ6kw', '4:21:34') +
  R(f'Resolution 7307 requires a “standardized equity impact analysis” for each scenario. {src("BB:3997273 p.2")} The September framework promised “An equity analysis review attached to every scenario.” {src("BB:14430171 p.7")}',
    f'The resolution names Black and Native students as focal groups; the KPIs merge them into “historically underserved by race.” {src("BB:3997273 p.2")} {src("BB:14493920 p.33")}',
    f'Survey respondents were 64% White and 74% PPS parents or guardians. {src("BB:14615901 p.9")}')),
F('praised', 'Praised for results one hour, on the closure list the next.',
  'At the Nov 4 meeting, PPS highlighted strong state test results for focal students at several schools that are proposed to close.',
  Q("Markham is joined by [Marysville], Sabin, and Vernon where we've seen notable increases in proficiency for black students. We are seeing exciting results for Latin Latino students at schools such as [Whitman], Maplewood, and [Bridlemile].", 'PPS staff', 'State test (OSAS) results presentation', '9kX3vnfRlvY', '1:53:13') +
  Q("the move to um closure or reconfiguration isn't a reflection of a school doing poorly or quote unquote bad. Um it's more of just us having too many", *KA, '9kX3vnfRlvY', '5:09:19', 'After Director Engelsman noted that Sabin, Marysville and Maplewood were both highlighted and on the closure list.') +
  R(f'Sabin, Marysville and Maplewood close in both scenarios. {src("BB:14505788 p.2")}')),
F('equal-equity', 'One size floor for every school, and every school in, except high schools.',
  'Leaders warned that treating schools the same can be inequitable, and that exempting some schools is inequitable. The plan applies one 360-student floor to every elementary school, and high schools are off the table.',
  Q("in a quest to make things equitable, we move towards making uh things equal, thereby disrupting um equity.", *KA, 'SPc05NM0oYs', '1:14:44') +
  Q('when certain areas or schools are excluded from right-sizing process, it leads to inequitable outcomes.', *EW, 'AH3wdS1A3sM', '0:59:38') +
  Q('not necessarily closing a [high school]', *EW, 'h_0YMlJnXPk', '0:39:36', 'On high schools: the discussion “has more been about like feeder patterns.”') +
  R(f'The 360 floor comes from the state’s prototype school and applies citywide. {src("BB:3997426 p.2")}')),
]

UNANSWERED = [
 ('Engelsman', 'What is the actual net savings to closing Sellwood? What are the net savings to closing any school?', 'BB:14618390 p.35'),
 ('Engelsman', 'Why do we have a list that has close to 50% Title I schools closing?', 'BB:14618390 p.42'),
 ('Chase-Miller', 'What specific resources will students gain in the receiving school?', 'BB:14618390 p.37'),
 ('Chase-Miller', 'Will class sizes get larger, smaller, or remain the same?', 'BB:14618390 p.38'),
 ('Chase-Miller', 'What transportation costs, travel-time burdens, and safety considerations will be created by the change of potential consolidations or closures?', 'BB:14618390 p.38'),
 ('Chase-Miller', 'How will PPS protect student belonging, cultural identity, and school-community relationships, especially for racially minoritized students?', 'BB:14618390 p.38'),
 ('Chase-Miller', 'What will PPS do if projected savings do not translate into school-level improvements?', 'BB:14618390 p.39'),
]

PRINC = [
 (1, 'well-resourced', 'Well-Resourced Schools', 'Sustainable, well-resourced schools that provide consistent access to strong academic programming across PPS.'),
 (2, 'safe-healthy', 'Safe and Healthy Learning Environments', 'Aligning school facilities and learning environments to support student safety, wellness, and long-term sustainability.'),
 (3, 'educational-options', 'Educational Options', 'Maintaining a strong network of neighborhood schools (while providing a balance of educational options) that are sustainable and well-resourced.'),
 (4, 'equity-lens', 'PPS Equity Lens', 'Using the PPS Equity Lens to guide decision-making and center students most impacted by inequities.'),
]

def build():
    nav = ''.join(f'<a href="#{slug}"><span class="pn">{n}</span>{esc(name)}</a>' for n, slug, name, _ in PRINC)
    secs_html = []
    for n, slug, name, text in PRINC:
        toc = ''.join(f'<li><a href="#{re.search(r"id=\"([^\"]+)\"", f).group(1)}">{esc(re.search(r"</a>(.*?)</h3>", f).group(1))}</a></li>' for f in P[n])
        secs_html.append(f'''<section class="principle p{n}" id="{slug}">
  <header class="ph"><div class="pnum">Guiding principle {n}</div><h2>{esc(name)}</h2>
    <p class="ptext">“{esc(text)}” {src("BB:14615901 p.5", "PPS, Nov 4, 2026")}</p>
    <ol class="ptoc">{html.unescape(toc)}</ol></header>
  {''.join(P[n])}
</section>''')
    unans = ''.join(f'<li><q>{esc(q)}</q> <span class="by">— Director {esc(w)}</span> {src(t)}</li>' for w, q, t in UNANSWERED)
    return TEMPLATE.replace('{{NAV}}', nav).replace('{{SECTIONS}}', '\n'.join(secs_html)).replace('{{UNANSWERED}}', unans) \
      .replace('{{SRC_Q30}}', src('BB:14618390', 'PPS Board Q&A, Oct 30, 2026')) \
      .replace('{{SRC_TIMELINE}}', src('BB:14615901 p.21')) \
      .replace('{{SRC_TITLE_I}}', src('BB:14618390 p.42')) \
      .replace('{{SRC_SMITH}}', '<a class="src" href="https://www.youtube.com/watch?v=uAf7l-ChjFo&t=10814s" target="_blank" rel="noopener">Board meeting, Sept 15, 2026, 3:00:14</a>') \
      .replace('{{SRC_REVISE}}', src('BB:14615901 p.17')) \
      .replace('{{Q_TRADEOFF}}', Q("the trade-offs are actually to our most marginalized communities more.", *RS, '9kX3vnfRlvY', '4:40:21', 'On spreading the $65 million in cuts across all schools instead of consolidating.')) \
      .replace('{{Q_IFNOT}}', Q("The question I don't hear enough coming from community is if not this then what?", *RS, '9kX3vnfRlvY', '5:00:35'))

TEMPLATE = open(os.path.join(ROOT, 'rightsizing-record', '_build', 'template.html')).read()
out = build()
open(os.path.join(ROOT, 'rightsizing-record', 'index.html'), 'w').write(out)
print('ok', len(out))
