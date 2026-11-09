"""Build analysis/topics/maplewood_claims_check.html.

Recomputes every figure from repo data:
- K-5 growth and grade progression (GPR), Oct 2021 -> Oct 2026, from PPS "Enrollment by Grade and Program Type"
  PDFs (parsed with pdfplumber), excluding schools with boundary/configuration changes since 2021 and focus/charter programs.
- PSU 2026-27 first-year forecast miss from analysis/data/psu_forecast_vs_actual_by_school.csv.
- PSU's 2031-32 projection from analysis/data/school_impact.csv (status quo).
- Peak projected utilization under Scenarios A/B: max(proj 2027-28..2031-32) / functional capacity (Nov 2 utilization model).
- Poverty / underserved shares of closing schools from analysis/data/school_impact.csv.
Run from the repo root: python3 analysis/topics/_build/build_maplewood_claims.py
"""
import csv, json, re, sys, html, collections, os
import pdfplumber

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
import linkify as L

def P(*a): return os.path.join(ROOT, *a)
GH = 'https://timaelliott.github.io/save-our-schools/'
GHB = 'https://github.com/timaelliott/save-our-schools/blob/main/'

# ------------------------------------------------------------------ 1. enrollment by grade
FILES = {2021: 'sources/pps_net/data-archives/2021-22/enrollment_by_grade_and_program_type.pdf',
         2022: 'sources/pps_net/data-and-reporting/2022-23/enrollment_by_grade_and_program_type.pdf',
         2023: 'sources/pps_net/data-and-reporting/2023-24/enrollment_by_grade_and_program_type.pdf',
         2024: 'sources/pps_net/data-and-reporting/2024-25/enrollment_by_grade_and_program_type.pdf',
         2025: 'sources/pps_net/data-and-reporting/2025-26/enrollment_by_grade_and_program_type.pdf',
         2026: 'sources/pps_net/data-and-reporting/2026-27/enrollment_by_grade_and_program_type.pdf'}
COLS = ['PK', 'KG', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', 'Total']
G = ['KG', '01', '02', '03', '04', '05']

def parse(path):
    rows = []
    with pdfplumber.open(P(path)) as pdf:
        for page in pdf.pages:
            words = page.extract_words()
            kg = [w for w in words if w['text'] == 'KG']
            if not kg: continue
            top = min(w['top'] for w in kg)
            xs = {w['text']: (w['x0'] + w['x1']) / 2 for w in words if w['text'] in COLS and abs(w['top'] - top) < 3}
            lines = collections.defaultdict(list)
            for w in words:
                if w['top'] > top + 3: lines[round(w['top'])].append(w)
            for t in sorted(lines):
                ws = sorted(lines[t], key=lambda w: w['x0'])
                name = ' '.join(w['text'] for w in ws if not re.fullmatch(r'[\d,]+', w['text']) and w['x1'] < xs['PK'] - 5)
                vals = {}
                for w in ws:
                    if re.fullmatch(r'[\d,]+', w['text']) and w['x0'] > xs['PK'] - 40:
                        cx = (w['x0'] + w['x1']) / 2
                        vals[min(xs, key=lambda k: abs(xs[k] - cx))] = int(w['text'].replace(',', ''))
                if vals: rows.append((name, vals))
    totals = {n[:-6].strip() for n, v in rows if n.endswith(' Total')}
    out, ingroup = {}, False
    for n, v in rows:
        if n.endswith(' Total'):
            out[n[:-6].strip()] = v; ingroup = False; continue
        if any(n == t or n.startswith(t + ' ') for t in totals): ingroup = True; continue
        if ingroup: continue
        out[n] = v
    for n, v in out.items():
        assert sum(x for c, x in v.items() if c != 'Total') == v.get('Total', sum(v.values())), (path, n)
    if 'Lee' in out: out['Sunrise'] = out.pop('Lee')
    return out

E = {y: parse(f) for y, f in FILES.items()}

BOUNDARY = ['Arleta', 'Atkinson', 'Bridger', 'Bridger Creative Science', 'Creative Science', 'Clark', 'Creston', 'Glencoe',
            'Vestal', 'Lent', 'Lewis', 'Marysville', 'Whitman', 'Woodmere', 'Woodstock']
NOT_NBHD = ['Alt. Programs', 'Arthur Academy', 'Emerson School', 'Kairos PDX', 'Le Monde', 'Portland Village School',
            'Metro. Learning Center', 'Odyssey', 'Online Learning Academy', 'PPS Pioneer Programs', 'Public Charter Schools',
            'Special Education Instruction', 'Special Services', 'District', 'Elementary Schools', 'Sunnyside Environmental',
            'Winterhaven', 'Richmond', 'Rigler']
growth = []
for n in E[2026]:
    if n in BOUNDARY or n in NOT_NBHD or 'KG' not in E[2026][n]: continue
    if not all(n in E[y] for y in E): continue
    k5 = {y: sum(E[y][n].get(g, 0) for g in G) for y in E}
    num = sum(sum(E[y + 1][n].get(G[i + 1], 0) for i in range(5)) for y in range(2021, 2026))
    den = sum(sum(E[y][n].get(G[i], 0) for i in range(5)) for y in range(2021, 2026))
    growth.append(dict(school=n, chg=k5[2026] - k5[2021],
                       pct=100 * (k5[2026] - k5[2021]) / k5[2021], gpr=num / den, **{f'k5_{y}': k5[y] for y in E}))
assert len(growth) == 38, len(growth)
by_gpr = sorted(growth, key=lambda d: -d['gpr'])
by_pct = sorted(growth, key=lambda d: -d['pct'])
rank = lambda lst, n: [i for i, d in enumerate(lst, 1) if d['school'] == n][0]
MW = [d for d in growth if d['school'] == 'Maplewood'][0]
with open(P('analysis/data/k5_growth_gpr_2021_2026.csv'), 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=['school', 'k5_2021', 'k5_2022', 'k5_2023', 'k5_2024', 'k5_2025', 'k5_2026', 'chg', 'pct', 'gpr', 'gpr_rank', 'growth_rank'])
    w.writeheader()
    for d in by_gpr:
        w.writerow({**{k: d[k] for k in ['school', 'k5_2021', 'k5_2022', 'k5_2023', 'k5_2024', 'k5_2025', 'k5_2026', 'chg']},
                    'pct': round(d['pct'], 1), 'gpr': round(d['gpr'], 3), 'gpr_rank': rank(by_gpr, d['school']), 'growth_rank': rank(by_pct, d['school'])})

# ------------------------------------------------------------------ 2. PSU forecast
psu = list(csv.DictReader(open(P('analysis/data/psu_forecast_vs_actual_by_school.csv'))))
pnames = {x['school'] for x in psu}
palias = {'Sunrise': 'Lee'}
def pm(n):
    a = palias.get(n, n)
    return a if a in pnames else [x for x in pnames if n.lower() in x.lower()][0]
inc = [d['school'] for d in growth]
miss = []
for x in psu:
    if x['vintage'] == '2026-27' and x['target_year'] == '2026-27':
        for n in inc:
            if pm(n) == x['school']:
                miss.append(dict(school=n, forecast=int(x['forecast']), actual=int(x['actual']), err=int(x['actual']) - int(x['forecast']),
                                 pct=-float(x['pct_error'])))
miss.sort(key=lambda d: -d['pct'])
assert len(miss) == 38
avg5 = []
for n in inc:
    e = [float(x['pct_error']) for x in psu if x['school'] == pm(n) and x['target_year'] == '2026-27' and x['vintage'] in ('2022-23', '2023-24', '2024-25', '2025-26', '2026-27')]
    if len(e) == 5: avg5.append((-sum(e) / 5, n))
avg5.sort(reverse=True)

si = list(csv.DictReader(open(P('analysis/data/school_impact.csv'))))
SQ = {d['school']: d for d in si if d['scenario'] == 'StatusQuo'}
salias = {'MLK Jr': 'Dr. Martin Luther King Jr.', 'Sunrise': 'Sunrise (formerly Lee)'}
decl = []
for d in growth:
    s = SQ.get(salias.get(d['school'], d['school']))
    if not s or s['current_grades'] not in ('K-5', 'PK-5'): continue
    p = float(s['proj_enr_2031_32'])
    decl.append(dict(school=d['school'], base=d['k5_2025'], proj=p, pct=100 * (p - d['k5_2025']) / d['k5_2025']))
decl.sort(key=lambda d: d['pct'])

# ------------------------------------------------------------------ 3. peak utilization
um = list(csv.reader(open(P('sources/pps_net/rightsizing/utilization_model/tab_DISTRICT_UTILIZATION_v1.csv'))))
ix = {k: i for i, k in enumerate(um[0])}
FC = {r[ix['Site']].strip().upper(): float(r[ix['Functional Capacity']]) for r in um[1:]
      if len(r) > 30 and r[ix['Functional Capacity']].replace('.', '', 1).isdigit()}
ualias = {'SUNRISE (FORMERLY LEE)': 'LEE', 'DR. MARTIN LUTHER KING JR.': 'MLK JR', 'BRENTWOOD MS (FORMERLY LANE)': 'LANE'}
def peak(sc):
    out = []
    for d in si:
        if d['scenario'] != sc: continue
        p = [float(d[f'proj_enr_{y}']) for y in ('2027_28', '2028_29', '2029_30', '2030_31', '2031_32') if d[f'proj_enr_{y}']]
        if not p: continue
        k = d['school'].strip().upper(); k = ualias.get(k, k).replace(' MS', '')
        c = FC.get(k)
        if not c: continue
        out.append(dict(school=d['school'], peak=max(p), fc=c, util=100 * max(p) / c, action=d['proposed_action']))
    return sorted(out, key=lambda d: -d['util'])
PA, PB = peak('A'), peak('B')

# ------------------------------------------------------------------ 4. equity
pc = lambda x: float(x.strip('%'))
def closures(sc):
    out = []
    for d in si:
        if d['scenario'] == sc and 'close' in d['proposed_action'].lower() and SQ[d['school']]['school_type'] != 'MS':
            s = SQ[d['school']]
            out.append(dict(school=d['school'], pov=pc(s['poverty_pct']), race=pc(s['underserved_race_pct']), sped=pc(s['sped_pct']),
                            ml=pc(s['multilingual_pct']), ti=s['title_I_2025_26'], enr=int(s['enrollment_2025_26'])))
    return sorted(out, key=lambda d: d['pov'])
CA, CB = closures('A'), closures('B')
assert all(d['school'] != 'Sellwood MS' for d in CA)
SHIFT = {n: (SQ[n], [d for d in si if d['school'] == n and d['scenario'] == 'A'][0]) for n in ('Hayhurst', 'Rieke', 'Markham')}

# ------------------------------------------------------------------ helpers
esc = html.escape
def link(url, text): return f'<a href="{esc(url)}" target="_blank" rel="noopener">{esc(text)}</a>'
def cite(tag, text=None):
    u = tag if tag.startswith('http') else L.url_for(tag)
    if not u and tag.startswith('PPS:'):
        u = GH + 'sources/' + tag[4:].split('#')[0].split(' ')[0]
    assert u, tag
    return f'<a class="cite" href="{esc(u)}" target="_blank" rel="noopener">{esc(text or tag)}</a>'

def hbars(rows, label, value, fmt, hi, vmin=None, vmax=None, ref=None, reflabel=None, extra=None, aria=''):
    """Horizontal emphasis bar chart as inline SVG. hi(row) -> 'hi'|'hi2'|''. Bars grow from `ref` when the axis
    does not start at zero (so a ratio chart is drawn as distance from 1.000, never a truncated bar)."""
    extra = extra or {}
    n = len(rows); bh = 20; gap = 6; top = 22 if reflabel else 6; lw = 120; rw = 150 if extra.get('ghost') else 56; W = 560
    H = top + n * (bh + gap) + 22
    vals = [value(r) for r in rows]
    lo = vmin if vmin is not None else 0
    hiv = vmax if vmax is not None else max(vals) * 1.05
    x = lambda v: lw + (W - lw - rw) * (v - lo) / (hiv - lo)
    base = ref if (ref is not None and lo > 0) else max(lo, 0)
    tf = extra.get('tickfmt', fmt)
    s = [f'<svg viewBox="0 0 {W} {H}" width="100%" role="img" aria-label="{esc(aria)}">']
    for t in extra.get('ticks', []):
        s.append(f'<line x1="{x(t):.1f}" x2="{x(t):.1f}" y1="{top-2}" y2="{H-20}" class="grid"/>'
                 f'<text x="{x(t):.1f}" y="{H-6}" class="tick" text-anchor="middle">{esc(tf(t))}</text>')
    if ref is not None:
        s.append(f'<line x1="{x(ref):.1f}" x2="{x(ref):.1f}" y1="{top-4}" y2="{H-20}" class="ref"/>')
        if reflabel:
            s.append(f'<text x="{x(ref):.1f}" y="{top-9}" class="reflab" text-anchor="middle">{esc(reflabel)}</text>')
    for i, r in enumerate(rows):
        y = top + i * (bh + gap); v = value(r); cls = hi(r)
        x0, x1 = x(base), x(v)
        bx, bw = min(x0, x1), max(2, abs(x1 - x0))
        tipv = fmt(v)
        g = extra.get('ghost', {}).get(label(r))
        ghost = ''
        vx = x1 + 6
        if g:
            gv, gl = g
            ghost = (f'<rect x="{x1:.1f}" y="{y+0.75}" width="{x(gv)-x1:.1f}" height="{bh-1.5}" rx="4" class="ghost"/>')
            vx = x(gv) + 6
            tipv += f' (≈{fmt(gv)} {gl})'
        lab_val = fmt(v) + (f' → ≈{fmt(g[0])} {g[1]}' if g else '')
        s.append(f'<g class="row {cls}" data-tip="{esc(label(r))}: {esc(tipv)}">'
                 f'<rect x="0" y="{y-2}" width="{W}" height="{bh+4}" class="hit"/>'
                 f'<text x="{lw-8}" y="{y+bh/2+4.5}" class="lab" text-anchor="end">{esc(label(r))}</text>'
                 f'<rect x="{bx:.1f}" y="{y}" width="{bw:.1f}" height="{bh}" rx="4" class="bar"/>{ghost}'
                 f'<text x="{vx:.1f}" y="{y+bh/2+4.5}" class="val">{esc(lab_val)}</text></g>')
    s.append('</svg>')
    return ''.join(s)

def table(head, rows, cls=''):
    h = ''.join(f'<th>{esc(c)}</th>' for c in head)
    b = ''.join('<tr class="' + ('mw' if r[0].startswith('Maplewood') else '') + '">' + ''.join(f'<td>{c}</td>' for c in r) + '</tr>' for r in rows)
    return f'<div class="tbl"><table class="{cls}"><thead><tr>{h}</tr></thead><tbody>{b}</tbody></table></div>'

# ------------------------------------------------------------------ figures
gr_rank, pct_rank = rank(by_gpr, 'Maplewood'), rank(by_pct, 'Maplewood')
miss_rank = [i for i, d in enumerate(miss, 1) if d['school'] == 'Maplewood'][0]
avg_rank = [i for i, (a, n) in enumerate(avg5, 1) if n == 'Maplewood'][0]
decl_rank = [i for i, d in enumerate(decl, 1) if d['school'] == 'Maplewood'][0]
MWm = [d for d in miss if d['school'] == 'Maplewood'][0]
MWd = [d for d in decl if d['school'] == 'Maplewood'][0]
pa = {d['school']: (i, d) for i, d in enumerate(PA, 1)}
pb = {d['school']: (i, d) for i, d in enumerate(PB, 1)}
ca_rank = [i for i, d in enumerate(CA, 1) if d['school'] == 'Maplewood'][0]
cb_rank = [i for i, d in enumerate(CB, 1) if d['school'] == 'Maplewood'][0]
car = sorted(CA, key=lambda d: d['race']); car_rank = [i for i, d in enumerate(car, 1) if d['school'] == 'Maplewood'][0]
HAY_ROOM = 487  # midpoint of 486-489: capacity with Hayhurst's actual special-ed room use (see hayhurst room analysis)
hay_peak = pa['Hayhurst'][1]['peak']

chart1 = hbars(by_gpr[:12], lambda r: r['school'], lambda r: r['gpr'], lambda v: f'{v:.3f}',
               lambda r: 'hi' if r['school'] == 'Maplewood' else '', vmin=0.995, vmax=1.045, ref=1.0, reflabel='1.00 = classes hold steady',
               extra={'ticks': [1.0, 1.02, 1.04], 'tickfmt': lambda v: f'{v:.2f}'}, aria='Grade progression ratio, top 12 of 38 elementary schools; Maplewood first at 1.040')
chart2 = hbars(miss[:10], lambda r: r['school'], lambda r: r['pct'], lambda v: f'{v:.1f}%',
               lambda r: 'hi' if r['school'] == 'Maplewood' else '', vmin=0, vmax=8,
               extra={'ticks': [0, 2, 4, 6], 'tickfmt': lambda v: f'{v:.0f}%'}, aria='PSU fall 2026 forecast miss, top 10 of 38; Maplewood 4th at 5.3%')
chart3 = hbars(PA[:14], lambda r: r['school'], lambda r: r['util'], lambda v: f'{v:.0f}%',
               lambda r: 'hi' if r['school'] in ('Hayhurst', 'Rieke') else ('hi2' if r['school'] == 'Markham' else ''),
               vmin=0, vmax=120, ref=100, reflabel='100% of capacity', extra={'ticks': [0, 50, 100], 'ghost': {'Hayhurst': (100 * hay_peak / HAY_ROOM, 'real rooms')}},
               aria='Peak projected utilization in Scenario A, top 14 of 51 schools; Rieke 12th at 93%, Hayhurst 14th at 90%')
chart4 = hbars(CA, lambda r: r['school'], lambda r: r['pov'], lambda v: f'{v:.1f}%',
               lambda r: 'hi' if r['school'] == 'Maplewood' else '', vmin=0, vmax=66, extra={'ticks': [0, 20, 40, 60], 'tickfmt': lambda v: f'{v:.0f}%'},
               aria='Share of students in poverty at the 13 elementary schools closing in Scenario A; Maplewood second lowest at 19.5%')

T1 = table(['School', 'K-5 Oct 2021', 'K-5 Oct 2026', 'Change', 'GPR 2021-26', 'GPR rank'],
           [[d['school'], d['k5_2021'], d['k5_2026'], f"{d['pct']:+.1f}%", f"{d['gpr']:.3f}", rank(by_gpr, d['school'])] for d in by_gpr[:10]] +
           ([] if gr_rank <= 10 else [['Maplewood', MW['k5_2021'], MW['k5_2026'], f"{MW['pct']:+.1f}%", f"{MW['gpr']:.3f}", gr_rank]]))
T1b = table(['School (top 10 by K-5 growth)', 'K-5 Oct 2021', 'K-5 Oct 2026', 'Change', 'Growth rank'],
            [[d['school'], d['k5_2021'], d['k5_2026'], f"{d['pct']:+.1f}%", rank(by_pct, d['school'])] for d in by_pct[:10]])
T2 = table(['School', 'PSU forecast, fall 2026', 'Actual, Oct 1 2026', 'Students missed', 'Miss as % of actual'],
           [[d['school'], d['forecast'], d['actual'], f"{d['err']:+d}", f"{d['pct']:.1f}%"] for d in miss[:8]])
T2b = table(['School (steepest PSU-projected K-5 decline)', 'Actual Oct 2025', "PSU's 2031-32", 'Change'],
            [[d['school'], d['base'], int(d['proj']), f"{d['pct']:+.1f}%"] for d in decl[:6]])
T3 = table(['School', 'Peak projected enrollment (2027-32)', 'PPS functional capacity', 'Peak / capacity', 'Rank in A'],
           [[d['school'], int(d['peak']), int(d['fc']), f"{d['util']:.0f}%", i] for i, d in enumerate(PA[:14], 1)])
T4 = table(['School closing in Scenario A', 'Poverty', 'Underserved race/ethnicity', 'Special ed', 'Multilingual', 'Title I'],
           [[d['school'], f"{d['pov']:.1f}%", f"{d['race']:.1f}%", f"{d['sped']:.1f}%", f"{d['ml']:.1f}%", 'Yes' if d['ti'] == 'Y' else 'No'] for d in CA])
hz, hzA = SHIFT['Hayhurst']; rk, rkA = SHIFT['Rieke']

GPAGES = {y: GH + f for y, f in FILES.items()}
enr_links = ' · '.join(link(GPAGES[y], f'{y}-{str(y+1)[2:]}') for y in FILES)

claims = [
 dict(id='growth', claim='“Maplewood has among the highest growth and GPR”', verdict='Holds', vcls='ok',
      finding=f'Maplewood has the <strong>highest grade progression ratio</strong> of {len(growth)} comparable PPS elementary schools since 2021 '
              f'({MW["gpr"]:.3f}), and the <strong>{pct_rank}th-highest K-5 growth</strong> ({MW["pct"]:+.1f}%, {MW["k5_2021"]} → {MW["k5_2026"]}).',
      chart=chart1, cap=f'Grade progression ratio, Oct 2021 → Oct 2026. Top 12 of {len(growth)} schools.'),
 dict(id='forecast', claim='“Maplewood has the biggest forecast error from PSU”', verdict='Overstated', vcls='warn',
      finding=f'Not the biggest. PSU under-forecast Maplewood this fall by {MWm["err"]} students ({MWm["pct"]:.1f}%), the '
              f'<strong>{miss_rank}th-largest miss</strong> of {len(miss)}. PSU still projects it to <strong>shrink {abs(MWd["pct"]):.0f}% by 2031-32</strong>, '
              f'the {decl_rank}rd-steepest decline of {len(decl)} K-5 schools, while it has the highest GPR.',
      chart=chart2, cap=f'How far PSU’s fall 2026 forecast fell short of the Oct 1 count. Top 10 of {len(miss)} schools.'),
 dict(id='overcrowding', claim='“Closing it will create two of the most overcrowded schools”', verdict='Not by PPS’s numbers', vcls='bad',
      finding=f'Using PPS’s own capacities, Scenario A puts <strong>Rieke at {pa["Rieke"][1]["util"]:.0f}%</strong> ({pa["Rieke"][0]}th of {len(PA)}) and '
              f'<strong>Hayhurst at {pa["Hayhurst"][1]["util"]:.0f}%</strong> ({pa["Hayhurst"][0]}th). Full, but not the fullest. '
              f'Corrected for the special-ed rooms Hayhurst actually uses, Hayhurst is about <strong>{100*hay_peak/HAY_ROOM:.0f}%</strong>.',
      chart=chart3, cap=f'Peak projected enrollment ÷ PPS functional capacity, Scenario A. Top 14 of {len(PA)} schools. Markham (lighter) receives Maplewood’s K-2 Intensive Skills class. Dashed: Hayhurst with the special-ed rooms it actually uses.'),
 dict(id='equity', claim='“Closing it has the least impact on equity measures”', verdict='Holds, with a caveat', vcls='ok',
      finding=f'Maplewood has the <strong>{ca_rank}nd-lowest poverty rate</strong> of the {len(CA)} elementary schools PPS would close in Scenario A '
              f'({[d for d in CA if d["school"]=="Maplewood"][0]["pov"]:.1f}%) and the lowest of {len(CB)} in Scenario B. It is not Title I. '
              f'The caveat: the Southwest package moves Hayhurst’s poverty rate from {hz["poverty_pct"]} to {hzA["poverty_pct"]} and Rieke’s from {rk["poverty_pct"]} to {rkA["poverty_pct"]}.',
      chart=chart4, cap=f'Students in poverty, the {len(CA)} elementary schools closing in Scenario A (2025-26).'),
]

panels = '\n'.join(f'''
  <article class="panel" id="{c['id']}">
    <header><p class="claim">{c['claim']}</p><p class="verdict {c['vcls']}"><span class="dot" aria-hidden="true"></span>{c['verdict']}</p></header>
    <p class="finding">{c['finding']}</p>
    <figure>{c['chart']}<figcaption>{c['cap']}</figcaption></figure>
  </article>''' for c in claims)

corrected = (f'Since 2021, Maplewood’s classes have grown grade to grade faster than any other comparable PPS elementary school. '
             f'PSU under-forecast it this fall and still projects it to shrink {abs(MWd["pct"]):.0f}% by 2031-32. '
             f'Closing it sends its students to Rieke and Hayhurst, which PPS projects at {pa["Rieke"][1]["util"]:.0f}% and {pa["Hayhurst"][1]["util"]:.0f}% full, '
             f'and Hayhurst’s real figure is closer to {100*hay_peak/HAY_ROOM:.0f}%. Its students are among the least likely to be low-income of any school on the closure list, '
             f'so closing it does little for PPS’s equity goals.')

work = f'''
<section class="work" id="work">
  <h2>The work</h2>

  <h3 id="w-growth">1. Growth and grade progression since 2021</h3>
  <p><strong>Data.</strong> PPS “Enrollment by Grade and Program Type,” October counts for 2021-22 through 2026-27 ({enr_links}). All programs at a school are combined (for example, Ainsworth’s Spanish Immersion and neighborhood program). For K-8 schools only grades K-5 are used.</p>
  <p><strong>Which schools.</strong> {len(growth)} neighborhood elementary and K-8 schools. Left out:</p>
  <ul>
    <li><strong>Boundary or grade changes since 2021:</strong> the Southeast Guiding Coalition changes effective 2023-24 and the 2021-22 K-5 reconfigurations ({', '.join(sorted(set(BOUNDARY) - {'Creative Science'}))}), per the footnotes to PPS’s {link(GH + 'sources/pps_net/data-and-reporting/2025-26/10yr_enrollment_history_detail.pdf', '10-year enrollment history')}.</li>
    <li><strong>Focus, immersion-only, charter and special programs:</strong> Odyssey, Sunnyside Environmental, Winterhaven, Richmond, Rigler, MLC, charters, and special services.</li>
  </ul>
  <p><strong>Grade progression ratio (GPR).</strong> For each school, the number of students in grades 1-5 one October divided by the number in grades K-4 the October before, pooled over the five year-to-year steps from 2021→22 through 2025→26. Above 1.000 means classes grow as they move up; below 1.000 means they shrink. This is the same quantity PSU uses to roll each class forward.</p>
  {T1}
  {T1b}
  <p class="note">Full results for all {len(growth)} schools: {link(GHB + 'analysis/data/k5_growth_gpr_2021_2026.csv', 'k5_growth_gpr_2021_2026.csv')}. Fall 2021 was a pandemic low for most schools, so “since 2021” growth flatters every school about equally; the GPR is less sensitive to the starting year.</p>

  <h3 id="w-forecast">2. PSU forecast error</h3>
  <p><strong>This fall.</strong> PSU’s 2026-27 forecast (the one behind the rightsizing scenarios) compared with the Oct 1, 2026 count, for the same {len(miss)} schools {cite('PPS:pps_net/data-and-reporting/2026-27/psu_prc_enrollment_forecast_2026-27_to_2035-36.pdf p.39', 'PSU 2026-27 forecast, p.39')}.</p>
  {T2}
  <p>Averaged over PSU’s last five editions’ forecasts for fall 2026 (2022-23 through 2026-27), Maplewood is under-forecast by {[a for a, n in avg5 if n == 'Maplewood'][0]:.1f}%, <strong>{avg_rank}th</strong> of {len(avg5)}. The largest five-edition misses were {', '.join(f'{n} ({a:.1f}%)' for a, n in avg5[:3])}. Before 2022, PSU over-forecast Maplewood: its 2021-22 edition expected 327 students this fall.</p>
  <p><strong>The direction of the forecast.</strong> PSU projects Maplewood at {int(MWd['proj'])} K-5 students in 2031-32, down {abs(MWd['pct']):.1f}% from {MWd['base']} in fall 2025 {cite('PPS:pps_net/rightsizing/school_impact/maplewood.pdf p.3', 'Maplewood family guide p.3')}. Among {len(decl)} K-5 schools in the comparison set:</p>
  {T2b}
  <p class="note">Our separate analysis of PSU’s method finds its Maplewood GPRs likely average about 1.005, because they include 2017-2019, the years right after the 2016 boundary change; Maplewood’s pooled 2021-2026 GPR is {MW['gpr']:.3f}. See {link(GHB + 'analysis/topics/psu_maplewood_gpr_window.md', 'PSU’s likely GPR window for Maplewood')}.</p>

  <h3 id="w-overcrowding">3. Overcrowding at the receiving schools</h3>
  <p><strong>Method.</strong> For every school in each scenario’s family guide, the highest projected enrollment from 2027-28 to 2031-32 divided by its functional capacity in PPS’s Nov 2 utilization model {cite('PPS:pps_net/rightsizing/utilization_model/static_v1_public_utilization_model_2026-11-02.xlsx#DISTRICT UTILIZATION v1!R40', 'utilization model')}. Scenario A, top 14 of {len(PA)}:</p>
  {T3}
  <p>In Scenario B, Rieke is {pb['Rieke'][0]}th ({pb['Rieke'][1]['util']:.0f}%) and Hayhurst {pb['Hayhurst'][0]}th ({pb['Hayhurst'][1]['util']:.0f}%) of {len(PB)}. Maplewood’s K-2 Intensive Skills class goes to Markham, {pa['Markham'][1]['util']:.0f}% full at peak in Scenario A ({pa['Markham'][0]}th) and rated “Not Yet Ready / Significant Barriers” on PPS’s Nov 9 readiness profile {cite('BB:14644366 p.21', 'FIO deck p.21')}.</p>
  <p><strong>Why Hayhurst’s real figure is higher.</strong> PPS’s 525 seats assume 2 special-ed rooms and 18 homerooms. Hayhurst’s own Nov 9 profile lists 7 special-education classrooms, and its special-ed box lists 4 rooms {cite('BB:14644366 p.19', 'FIO deck p.19')}. Director Splitt said the SCES program “takes up four classrooms” {cite('YT:9kX3vnfRlvY@4:01:52', 'Nov 4, 4:01:52')}. With those rooms counted, capacity is 486-489, and a peak of {int(hay_peak)} is about {100*hay_peak/HAY_ROOM:.0f}%. In 2015-16, PPS’s own profile flagged this same 22-classroom building as having “little or no room left for growth” at 23 students per classroom; {int(hay_peak)} students is {hay_peak/22:.1f} per classroom {cite(GH + 'sources/pps_net/boundaries_2016/wayback_2017/2015-16_School_Profiles.pdf#page=212', '2015-16 profile p.212')}.</p>

  <h3 id="w-equity">4. Equity measures</h3>
  <p><strong>Method.</strong> 2025-26 student demographics from each school’s family guide {cite('PPS:pps_net/rightsizing/school_impact/maplewood.pdf p.3', 'Maplewood guide')}, for the elementary schools PPS would close (Sellwood Middle School left out).</p>
  {T4}
  <p>On underserved race/ethnicity, Maplewood ({[d for d in CA if d['school']=='Maplewood'][0]['race']:.1f}%) is {car_rank}nd-lowest of {len(CA)}. In Scenario B, Maplewood has the lowest poverty rate of the {len(CB)} elementary closures.</p>
  <p><strong>The caveat.</strong> The Southwest package does change equity measures at the receiving schools, mostly because part of Hayhurst’s boundary moves to Rieke:</p>
  {table(['School', 'Poverty, no changes', 'Poverty, Scenario A', 'Underserved race, no changes', 'Underserved race, Scenario A'],
         [[n, SHIFT[n][0]['poverty_pct'], SHIFT[n][1]['poverty_pct'], SHIFT[n][0]['underserved_race_pct'], SHIFT[n][1]['underserved_race_pct']] for n in ('Hayhurst', 'Rieke', 'Markham')])}
  <p class="note">So “least impact” is fair for Maplewood’s own students; it is not true of the package as a whole. A better wording: closing Maplewood does the least for PPS’s equity goals.</p>
</section>'''

page = f'''<title>Maplewood Claims Check</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Libre+Franklin:wght@400;600;700;800&family=Source+Serif+4:opsz,wght@8..60,400;8..60,600&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>
/* Layout: a fact-check sheet. The corrected sentence up top, four claim panels in a 2x2 grid, the full work below. */
:root {{
  --paper: #f6f7f4; --sheet: #fcfcfb; --ink: #0b0b0b; --ink2: #52514e; --muted: #898781; --rule: #e1e0d9; --axis: #c3c2b7;
  --accent: #2a78d6; --accent2: #9dc0ea; --deemph: #d6d4cc; --leaf-soft: #e6eef7;
  --ok: #006300; --ok-soft: #e3f0e3; --warn: #8a5a00; --warn-soft: #f6ecd6; --bad: #a3261f; --bad-soft: #f6e1df;
  --display: "Libre Franklin", "Helvetica Neue", Arial, sans-serif;
  --body: "Source Serif 4", Georgia, serif;
  --mono: "IBM Plex Mono", ui-monospace, Menlo, monospace;
}}
@media (prefers-color-scheme: dark) {{ :root:not([data-theme="light"]) {{
  --paper: #0d0d0d; --sheet: #1a1a19; --ink: #f0efec; --ink2: #c3c2b7; --muted: #898781; --rule: #2c2c2a; --axis: #383835;
  --accent: #3987e5; --accent2: #2c5486; --deemph: #3b3b38; --leaf-soft: #1c2735;
  --ok: #0ca30c; --ok-soft: #142614; --warn: #e0b04a; --warn-soft: #2e2614; --bad: #ee7a72; --bad-soft: #321a18; color-scheme: dark; }} }}
:root[data-theme="dark"] {{
  --paper: #0d0d0d; --sheet: #1a1a19; --ink: #f0efec; --ink2: #c3c2b7; --muted: #898781; --rule: #2c2c2a; --axis: #383835;
  --accent: #3987e5; --accent2: #2c5486; --deemph: #3b3b38; --leaf-soft: #1c2735;
  --ok: #0ca30c; --ok-soft: #142614; --warn: #e0b04a; --warn-soft: #2e2614; --bad: #ee7a72; --bad-soft: #321a18; color-scheme: dark; }}
body {{ background: var(--paper); color: var(--ink); font-family: var(--body); font-size: 17px; line-height: 1.55; }}
.wrap {{ max-width: 1080px; margin: 0 auto; padding-block: 36px 64px; padding-left: max(16px, env(safe-area-inset-left, 0px)); padding-right: max(16px, env(safe-area-inset-right, 0px)); display: grid; gap: 28px; }}
a {{ color: var(--accent); }}
a:focus-visible {{ outline: 2px solid var(--accent); outline-offset: 2px; }}
h1, h2, h3, .claim, .verdict, .eyebrow, th {{ font-family: var(--display); }}
.eyebrow {{ margin: 0; font-size: 0.78rem; letter-spacing: 0.08em; text-transform: uppercase; color: var(--ink2); font-weight: 600; }}
h1 {{ margin: 4px 0 0; font-size: clamp(1.9rem, 4.5vw, 2.7rem); line-height: 1.08; font-weight: 800; text-wrap: balance; }}
.lede {{ margin: 0; max-width: 68ch; color: var(--ink2); }}
.orig, .fixed {{ margin: 0; padding: 14px 18px; max-width: 80ch; }}
.orig {{ border-left: 3px solid var(--axis); color: var(--ink2); font-style: italic; }}
.fixed {{ background: var(--leaf-soft); border-left: 3px solid var(--accent); }}
.fixed b, .orig b {{ font-family: var(--display); font-style: normal; font-size: 0.75rem; letter-spacing: 0.08em; text-transform: uppercase; display: block; margin-bottom: 4px; color: var(--ink2); }}
.grid2 {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 480px), 1fr)); gap: 16px; }}
.panel {{ background: var(--sheet); border: 1px solid var(--rule); padding: 18px 20px 14px; display: grid; gap: 10px; align-content: start; min-width: 0; }}
.panel header {{ display: flex; flex-wrap: wrap; justify-content: space-between; gap: 8px 12px; align-items: baseline; }}
.claim {{ margin: 0; font-weight: 700; font-size: 1.02rem; text-wrap: balance; max-width: 34ch; }}
.verdict {{ margin: 0; font-size: 0.78rem; font-weight: 700; padding: 3px 10px 3px 8px; border-radius: 999px; display: inline-flex; gap: 6px; align-items: center; white-space: nowrap; }}
.verdict .dot {{ width: 8px; height: 8px; border-radius: 50%; background: currentColor; }}
.verdict.ok {{ color: var(--ok); background: var(--ok-soft); }}
.verdict.warn {{ color: var(--warn); background: var(--warn-soft); }}
.verdict.bad {{ color: var(--bad); background: var(--bad-soft); }}
.finding {{ margin: 0; font-size: 0.97rem; }}
figure {{ margin: 0; display: grid; gap: 4px; }}
figcaption {{ font-family: var(--display); font-size: 0.75rem; color: var(--muted); }}
svg text {{ font-family: var(--display); }}
svg .lab {{ font-size: 12px; fill: var(--ink2); }}
svg .val {{ font-size: 11.5px; fill: var(--ink2); font-variant-numeric: tabular-nums; }}
svg .tick {{ font-size: 10.5px; fill: var(--muted); font-variant-numeric: tabular-nums; }}
svg .reflab {{ font-size: 10.5px; fill: var(--muted); }}
svg .grid {{ stroke: var(--rule); stroke-width: 1; }}
svg .ref {{ stroke: var(--axis); stroke-width: 1.5; stroke-dasharray: 3 3; }}
svg .bar {{ fill: var(--deemph); }}
svg .hit {{ fill: transparent; }}
svg .row.hi .bar {{ fill: var(--accent); }}
svg .row.hi2 .bar {{ fill: var(--accent2); }}
svg .row.hi .lab, svg .row.hi .val {{ fill: var(--ink); font-weight: 700; }}
svg .ghost {{ fill: none; stroke: var(--accent); stroke-width: 1.5; stroke-dasharray: 3 2; }}
svg .row:hover .bar {{ opacity: 0.85; }}
#tip {{ position: fixed; pointer-events: none; background: var(--ink); color: var(--paper); font-family: var(--display); font-size: 12px; padding: 4px 8px; border-radius: 4px; z-index: 5; }}
.work {{ background: var(--sheet); border: 1px solid var(--rule); padding: 24px clamp(16px, 4vw, 36px); display: grid; gap: 12px; min-width: 0; }}
.work h2 {{ margin: 0; font-size: 1.5rem; }}
.work h3 {{ margin: 18px 0 0; font-size: 1.1rem; }}
.work p, .work ul {{ margin: 0; max-width: 78ch; }}
.work ul {{ padding-left: 1.2em; display: grid; gap: 4px; }}
.note {{ font-size: 0.92rem; color: var(--ink2); }}
.tbl {{ overflow-x: auto; }}
table {{ border-collapse: collapse; font-size: 0.88rem; font-variant-numeric: tabular-nums; min-width: 420px; }}
th {{ text-align: left; font-size: 0.75rem; font-weight: 600; color: var(--ink2); padding: 6px 12px 6px 0; border-bottom: 1px solid var(--axis); vertical-align: bottom; }}
td {{ padding: 5px 12px 5px 0; border-bottom: 1px solid var(--rule); }}
tr.mw td {{ font-weight: 700; color: var(--ink); }}
tr.mw td:first-child {{ box-shadow: inset 3px 0 0 var(--accent); padding-left: 8px; }}
.cite {{ font-family: var(--mono); font-size: 0.74rem; color: var(--ink2); }}
footer.src {{ font-size: 0.85rem; color: var(--ink2); max-width: 80ch; display: grid; gap: 6px; }}
footer.src p {{ margin: 0; }}
@media (prefers-reduced-motion: reduce) {{ * {{ transition: none !important; }} }}
</style>

<div class="wrap">
  <header style="display:grid;gap:12px">
    <p class="eyebrow">Fact check · data as of Oct 1, 2026</p>
    <h1>Four claims about Maplewood, checked against PPS’s own data</h1>
    <p class="orig"><b>The claim as written</b>So across PPS Maplewood has among the highest growth / GPR, biggest forecast error from PSU, closing it will create two of the most overcrowded schools, and closing it has the least impact on equity measures.</p>
    <p class="fixed"><b>What the data supports</b>{corrected}</p>
  </header>

  <section class="grid2" aria-label="The four claims">{panels}
  </section>
{work}
  <footer class="src">
    <p><strong>Sources.</strong> PPS October enrollment by grade (2021-22 to 2026-27); PSU Population Research Center enrollment forecasts (2017-18 to 2026-27 editions); PPS rightsizing family guides (October 2026); PPS Static V1 utilization model (Nov 2, 2026); PPS Nov 9, 2026 facilities committee readiness profiles; PPS 2015-16 school profiles. All archived at {link('https://github.com/timaelliott/save-our-schools', 'github.com/timaelliott/save-our-schools')}. Every figure on this page is recomputed by {link(GHB + 'analysis/topics/_build/build_maplewood_claims.py', 'build_maplewood_claims.py')}.</p>
  </footer>
</div>
<div id="tip" hidden></div>
<script>
(function () {{
  var tip = document.getElementById('tip');
  document.querySelectorAll('svg .row').forEach(function (g) {{
    g.addEventListener('pointermove', function (e) {{
      tip.textContent = g.getAttribute('data-tip'); tip.hidden = false;
      var x = Math.min(e.clientX + 12, window.innerWidth - tip.offsetWidth - 8);
      tip.style.left = x + 'px'; tip.style.top = (e.clientY - 30) + 'px';
    }});
    g.addEventListener('pointerleave', function () {{ tip.hidden = true; }});
  }});
}})();
</script>
'''
open(P('analysis/topics/maplewood_claims_check.html'), 'w').write(page)
print('ok', len(page), 'gpr rank', gr_rank, 'growth rank', pct_rank, 'miss rank', miss_rank, 'avg5', avg_rank, 'decl', decl_rank,
      'A ranks', pa['Rieke'][0], pa['Hayhurst'][0], 'B', pb['Rieke'][0], pb['Hayhurst'][0], 'pov', ca_rank, cb_rank, 'race', car_rank)
