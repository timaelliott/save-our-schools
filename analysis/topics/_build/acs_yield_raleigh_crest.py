"""Raleigh Crest student-yield check against PSU's explanation of its methods (email from Ethan Sharygin, PSU PRC, 2026-11-12).

Recomputes, from the archived ACS PUMS files, (1) PSU's "~0.10 per single-family detached unit" definition, (2) PSU's
newer "~0.2" definition, (3) last year's 0.45 definition as far as our files allow, and (4) a K-5 yield for Raleigh Crest
by home age and type. 90% margins from the 80 replicate weights (successive-difference formula).
Run from the repo root: python3 analysis/topics/_build/acs_yield_raleigh_crest.py  -> analysis/data/acs_yield_raleigh_crest.csv
"""
import csv, io, zipfile, json
import numpy as np

SRC = 'sources/census/acs_pums'
TRI = ('051', '067', '005')  # Multnomah, Washington, Clackamas
PM, PM_MULT, PM_WASH = set(), set(), set()
for f in ('2010_Census_Tract_to_2010_PUMA.txt', '2020_Census_Tract_to_2020_PUMA.txt'):
    for x in csv.DictReader(open(f'{SRC}/geo/{f}', encoding='utf-8-sig')):
        if x['STATEFP'] == '41' and x['COUNTYFP'] in TRI:
            PM.add(x['PUMA5CE'])
            if x['COUNTYFP'] == '051': PM_MULT.add(x['PUMA5CE'])
            if x['COUNTYFP'] == '067': PM_WASH.add(x['PUMA5CE'])
YBL19 = {f'{c:02d}': 2005 + c - 9 for c in range(9, 24)}  # 2019 file: 09=2005 ... 23=2019 (single years)


def rows(path):
    z = zipfile.ZipFile(path); n = [n for n in z.namelist() if n.endswith('.csv')][0]
    return csv.DictReader(io.TextIOWrapper(z.open(n), encoding='utf-8'))


def built(r):
    """Single build year where the file gives one; 'G2010' for the 2010-2019 group; None if older."""
    if 'YRBLT' not in r:
        return YBL19.get(r['YBL'])
    v = r['YRBLT']
    if v == '2010': return 'G2010'
    return int(v) if v and int(v) >= 2020 else None


def load(tag, hpath, ppath, scale=1.0):
    H = {}
    for r in rows(hpath):
        if r.get('TYPEHUGQ', r.get('TYPE')) != '1' or r['PUMA'].zfill(5) not in PM: continue
        b = built(r)
        if b is None: continue
        w = np.array([float(r['WGTP'])] + [float(r[f'WGTP{i}']) for i in range(1, 81)]) * scale
        val = float(r['VALP']) * float(r['ADJHSG']) / 1e6 / 1e6 if r['VALP'] else None  # $ millions, 2024 dollars
        H[r['SERIALNO']] = dict(src=tag, Y=int(r['SERIALNO'][:4]), b=b, bld=r['BLD'], bd=int(r['BDSP'] or -1),
                                occ=r['TEN'] != '' and r['NP'] not in ('0', ''), ten=r['TEN'], val=val,
                                mult=r['PUMA'].zfill(5) in PM_MULT, wash=r['PUMA'].zfill(5) in PM_WASH, w=w, **{k: np.zeros(81) for k in ('p', 's517', 'k12', 'k5', 'k5all')})
    for r in rows(ppath):
        h = H.get(r['SERIALNO'])
        if not h: continue
        pw = np.array([float(r['PWGTP'])] + [float(r[f'PWGTP{i}']) for i in range(1, 81)]) * scale
        h['p'] += pw
        age, sch, g = int(r['AGEP']), r['SCH'], r['SCHG']
        if 5 <= age <= 17 and sch == '2': h['s517'] += pw
        if g and 2 <= int(g) <= 14 and sch == '2': h['k12'] += pw
        if g and 2 <= int(g) <= 7:
            h['k5all'] += pw
            if sch == '2': h['k5'] += pw
    return list(H.values())


def ratio(sel, num, den='w', occ_only=False):
    sel = [h for h in sel if (h['occ'] or not occ_only)]
    if not sel: return None
    N = sum(h[num] for h in sel); D = sum(h[den] for h in sel)
    r = N / np.where(D == 0, np.nan, D)
    se = np.sqrt(4 / 80 * np.nansum((r[1:] - r[0]) ** 2))
    return dict(n=len(sel), est=round(float(r[0]), 3), moe90=round(float(1.645 * se), 3), units=round(float(D[0])), num=round(float(N[0])))


ONE = {y: load(f'1yr{y}', f'{SRC}/{y}/csv_hor.zip', f'{SRC}/{y}/csv_por.zip') for y in (2019, 2021, 2022, 2023, 2024)}
FIVE = load('5yr2020-24', f'{SRC}/5yr_2020-2024/csv_hor.zip', f'{SRC}/5yr_2020-2024/csv_por.zip')
SFD = lambda h: h['bld'] == '02'
ATT = lambda h: h['bld'] == '03'
age = lambda h: h['Y'] - h['b'] if isinstance(h['b'], int) else None
out = []


def add(section, spec, sel, num, den='w', occ_only=False, note=''):
    d = ratio(sel, num, den, occ_only)
    if d: out.append(dict(section=section, spec=spec, numerator=num, per='occupied unit' if occ_only else ('person' if den == 'p' else 'unit incl. vacant'), note=note, **d))
    return d


# ---- 1. PSU's "~0.10": 2020-24, built 0-2 years before the survey, SFD, all bedrooms, units incl. vacant, age 5-17 public
S = 'A. PSU ~0.10 definition'
win02 = lambda h: age(h) is not None and 0 <= age(h) <= 2
add(S, '5-yr 2020-24 file, built 0-2 yrs before each record\'s survey year (2020-21 surveys: only 2020+ builds identifiable)', [h for h in FIVE if SFD(h) and win02(h)], 's517')
add(S, 'same, surveys 2022-24 only (window fully identifiable)', [h for h in FIVE if SFD(h) and win02(h) and h['Y'] >= 2022], 's517')
pool1 = [h for y in (2021, 2022, 2023, 2024) for h in ONE[y]]
add(S, '1-yr 2021-24 files pooled, built 0-2 yrs before survey', [h for h in pool1 if SFD(h) and win02(h)], 's517')
for y in range(2020, 2025):
    add(S, f'5-yr file, survey year {y} only', [h for h in FIVE if SFD(h) and win02(h) and h['Y'] == y], 's517')
add(S, 'same as first row, per resident instead of per unit', [h for h in FIVE if SFD(h) and win02(h)], 's517', den='p')
add(S, 'same as first row, per occupied unit', [h for h in FIVE if SFD(h) and win02(h)], 's517', occ_only=True)
# Mixed-period check: 5-yr weights give a period AVERAGE; a denominator summed over the five survey years is 5x larger.
selA = [h for h in FIVE if SFD(h) and win02(h)]
nA = sum(h['s517'][0] for h in selA); dA = sum(h['w'][0] for h in selA)
out.append(dict(section=S, spec='5-yr numerator / denominator summed over the 5 survey years (= 5 x period average)', numerator='s517',
                per='unit, summed over years', note='mixed periods', n=len(selA), est=round(nA / (5 * dA), 3), moe90='', units=round(5 * dA), num=round(nA)))
d1 = sum(h['w'][0] for y in (2021, 2022, 2023, 2024) for h in ONE[y] if SFD(h) and win02(h))
out.append(dict(section=S, spec='5-yr numerator / sum of 1-yr ACS counts of 0-2-yr-old SFD units, surveys 2021-24', numerator='s517',
                per='unit, summed over years', note='mixed periods', n='', est=round(nA / d1, 3), moe90='', units=round(d1), num=round(nA)))
add(S, 'same as first row, grades K-5 only', selA, 'k5')
for a in (0, 1, 2):
    add(S, f'5-yr file, homes exactly {a} yr old at survey', [h for h in FIVE if SFD(h) and age(h) == a], 's517')

# ---- 2. PSU's newer "~0.2": public K-12 in SFD built 2020-24 (any survey year), / inventory of SFD built 2020-24
S = 'B. PSU ~0.2 definition'
b2024 = lambda h: isinstance(h['b'], int) and 2020 <= h['b'] <= 2024
d_c = add(S, 'numerator and denominator both from the 5-yr 2020-24 file (consistent period average)', [h for h in FIVE if SFD(h) and b2024(h)], 'k12')
inv = sum(h['w'][0] for h in ONE[2024] if SFD(h) and b2024(h))
num5 = sum(h['k12'][0] for h in FIVE if SFD(h) and b2024(h))
out.append(dict(section=S, spec='5-yr period-average numerator / end-2024 stock of SFD built 2020-24 (2024 1-yr ACS, proxy for the regional housing inventory)',
                numerator='k12', per='unit in end-2024 inventory', note='mixed periods', n='', est=round(num5 / inv, 3), moe90='', units=round(inv), num=round(num5)))
add(S, 'consistent 5-yr version, grades K-5 only', [h for h in FIVE if SFD(h) and b2024(h)], 'k5')
add(S, '2024 survey only: K-12 public in SFD built 2020-24 / SFD built 2020-24 (both end-of-period)', [h for h in ONE[2024] if SFD(h) and b2024(h)], 'k12')

# ---- 3. Last year's 0.45: buildings < 5 years old, SFD + mobile homes, per occupied unit, Portland-area geography
S = 'C. Last year\'s 0.45 definition (approximation)'
lt5 = lambda h: age(h) is not None and 0 <= age(h) <= 4
pool = [h for y in (2019, 2022, 2023, 2024) for h in ONE[y]]  # 1-yr files where a 0-4 year window is identifiable
for geo, gf in (('tri-county', lambda h: True), ('Multnomah PUMAs (City of Portland approx.)', lambda h: h['mult'])):
    add(S, f'1-yr 2019+2022-24, {geo}, SFD + mobile, < 5 yrs old', [h for h in pool if h['bld'] in ('01', '02') and lt5(h) and gf(h)], 's517', occ_only=True)
    add(S, f'1-yr 2019+2022-24, {geo}, SFD, < 5 yrs old, per unit incl. vacant', [h for h in pool if SFD(h) and lt5(h) and gf(h)], 's517')

# ---- 4. Raleigh Crest: K-5 public students per unit by home age, detached 3+ BR and attached
S = 'D. K-5 public yield by home age (1-yr 2019, 2022-24; tri-county)'
pool = [h for y in (2019, 2022, 2023, 2024) for h in ONE[y]]
BUCKETS = {'0-1': (0, 1), '2-4': (2, 4), '0-4': (0, 4), '5-9': (5, 9), '10-14': (10, 14)}
for gname, g in (('detached 3+ BR', lambda h: SFD(h) and h['bd'] >= 3), ('detached all', SFD),
                 ('attached (townhouse) all', ATT), ('attached 3+ BR', lambda h: ATT(h) and h['bd'] >= 3)):
    for bn, (lo, hi) in BUCKETS.items():
        sel = [h for h in pool if g(h) and age(h) is not None and lo <= age(h) <= hi]
        add(S, f'{gname}, age {bn}', sel, 'k5')
        if gname.startswith('detached 3+') or gname.startswith('attached (town'):
            add(S, f'{gname}, age {bn}', sel, 'k5', occ_only=True)
            add(S, f'{gname}, age {bn} (any school K-5, for public share)', sel, 'k5all')
for gname, g in (('detached 3+ BR', lambda h: SFD(h) and h['bd'] >= 3), ('attached (townhouse) all', ATT)):
    add(S, f'{gname}, age 0-4, Washington County only', [h for h in pool if g(h) and h['wash'] and age(h) is not None and 0 <= age(h) <= 4], 'k5')
    add(S, f'{gname}, age 0-4, owner-occupied', [h for h in pool if g(h) and h['ten'] in ('1', '2') and age(h) is not None and 0 <= age(h) <= 4], 'k5', occ_only=True)
    add(S, f'{gname}, age 0-4, K-12', [h for h in pool if g(h) and age(h) is not None and 0 <= age(h) <= 4], 'k12')
# value test: owner-occupied new detached homes worth >= $700K (2024 dollars) vs below
S = 'E. Value test (owner-occupied detached 3+ BR, age 0-9, K-5 public per occupied unit)'
for vn, vf in (('< $700K', lambda v: v < 0.7), ('>= $700K', lambda v: v >= 0.7), ('$700K-$1.5M', lambda v: 0.7 <= v <= 1.5)):
    add(S, vn, [h for h in pool if SFD(h) and h['bd'] >= 3 and h['ten'] in ('1', '2') and h['val'] is not None and vf(h['val'])
                and age(h) is not None and 0 <= age(h) <= 9], 'k5', occ_only=True)

with open('analysis/data/acs_yield_raleigh_crest.csv', 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(out[0])); w.writeheader(); w.writerows(out)
for o in out:
    print(f"{o['section'][:2]} {o['spec'][:105]:<105} {o['numerator']:>5} /{o['per'][:10]:<10} n={o['n']!s:>4} {o['est']!s:>6} ±{o['moe90']!s:<6}")
