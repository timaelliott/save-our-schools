"""Public-school students (age 5-17) living in newly built 2-4 bedroom homes, Multnomah/Washington/Clackamas counties.

Source: ACS 1-year PUMS, Oregon, survey years 2019, 2021, 2022, 2023, 2024 (no standard 2020 1-year file exists).
"Newly built" = structure first built in the survey year or the year before (YBL/YRBLT).
Units: housing units (not group quarters) with 2-4 bedrooms, weighted with WGTP. Vacant units are counted in "all units".
Students: persons aged 5-17 enrolled in public school (SCH=2), weighted with PWGTP.
Standard errors: ACS successive-difference replication, SE = sqrt(4/80 * sum_r (X_r - X)^2) with the 80 replicate weights.
Run from the repo root: python3 analysis/topics/_build/acs_new_housing_school_yield.py
"""
import csv, io, math, os, zipfile, collections, json

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
SRC = os.path.join(ROOT, 'sources', 'census', 'acs_pums')
YEARS = [2019, 2021, 2022, 2023, 2024]
R = 80

def county_map(year):
    f = '2010_Census_Tract_to_2010_PUMA.txt' if year < 2022 else '2020_Census_Tract_to_2020_PUMA.txt'
    m = {}
    for x in csv.DictReader(open(os.path.join(SRC, 'geo', f), encoding='utf-8-sig')):
        if x['STATEFP'] == '41' and x['COUNTYFP'] in ('051', '067', '005'):
            m[x['PUMA5CE']] = {'051': 'Multnomah', '067': 'Washington', '005': 'Clackamas'}[x['COUNTYFP']]
    return m

def rows(year, kind):
    z = zipfile.ZipFile(os.path.join(SRC, str(year), f'csv_{kind}.zip'))
    name = [n for n in z.namelist() if n.endswith('.csv')][0]
    return csv.DictReader(io.TextIOWrapper(z.open(name), encoding='utf-8'))

def bld_group(b):
    b = int(b or 0)
    return {1: 'Mobile home', 2: 'Single-family detached', 3: 'Single-family attached (townhome)',
            4: '2-4 unit building', 5: '2-4 unit building'}.get(b, '5+ unit apartment building' if 6 <= b <= 9 else 'Other')

WINDOW = int(os.environ.get('WINDOW', '2'))  # years: 2 = survey year and the year before

def new_built(year, r):
    if year == 2019:
        return r['YBL'] in [str(23 - i) for i in range(WINDOW)]  # 23 = 2019, 22 = 2018, 21 = 2017
    return r['YRBLT'] in [str(year - i) for i in range(WINDOW)]

class Acc:
    """Weighted total with 80 replicates."""
    def __init__(self): self.v = [0.0] * (R + 1); self.n = 0
    def add(self, r, w):
        self.v[0] += float(r[w]); self.n += 1
        for i in range(1, R + 1): self.v[i] += float(r[f'{w}{i}'])

def se(vals):
    return math.sqrt(4 / R * sum((vals[i] - vals[0]) ** 2 for i in range(1, R + 1)))

units = collections.defaultdict(Acc); occ = collections.defaultdict(Acc); stud = collections.defaultdict(Acc); kids = collections.defaultdict(Acc)
for y in YEARS:
    cm = county_map(y)
    hh = {}
    for r in rows(y, 'hor'):
        if r.get('TYPEHUGQ', r.get('TYPE')) != '1': continue
        p = r['PUMA'].zfill(5)
        if p not in cm or not new_built(y, r): continue
        bd = int(r['BDSP'] or -1)
        if not 2 <= bd <= 4: continue
        info = (cm[p], bd, bld_group(r['BLD']), 'Owner' if r['TEN'] in ('1', '2') else ('Renter' if r['TEN'] in ('3', '4') else 'Vacant'))
        hh[r['SERIALNO']] = info
        for key in [(y,) + k for k in [('All 3 counties', 'All', 'All', 'All'), (info[0], 'All', 'All', 'All'), ('All 3 counties', info[1], 'All', 'All'),
                                         ('All 3 counties', 'All', info[2], 'All'), ('All 3 counties', 'All', 'All', info[3]), ('All 3 counties', info[1], info[2], 'All'), ('All 3 counties', '3-4', info[2], 'All') if info[1] >= 3 else ('All 3 counties', '2', info[2], 'All')]]:
            for kk in (key, ('2019-2024 pooled',) + key[1:]):
                units[kk].add(r, 'WGTP')
                if int(r['NP'] or 0) > 0: occ[kk].add(r, 'WGTP')
    for r in rows(y, 'por'):
        info = hh.get(r['SERIALNO'])
        if not info: continue
        a = int(r['AGEP'])
        if not 5 <= a <= 17: continue
        for key in [(y,) + k for k in [('All 3 counties', 'All', 'All', 'All'), (info[0], 'All', 'All', 'All'), ('All 3 counties', info[1], 'All', 'All'),
                                         ('All 3 counties', 'All', info[2], 'All'), ('All 3 counties', 'All', 'All', info[3]), ('All 3 counties', info[1], info[2], 'All'), ('All 3 counties', '3-4', info[2], 'All') if info[1] >= 3 else ('All 3 counties', '2', info[2], 'All')]]:
            for kk in (key, ('2019-2024 pooled',) + key[1:]):
                kids[kk].add(r, 'PWGTP')
                if r['SCH'] == '2': stud[kk].add(r, 'PWGTP')

out = []
for k in sorted(units, key=lambda k: tuple(str(x) for x in k)):
    if k[2] == '2': continue  # duplicate of the integer 2-bedroom rows
    u, o, s, c = units[k], occ[k], stud.get(k, Acc()), kids.get(k, Acc())
    ratio = [s.v[i] / u.v[i] if u.v[i] else 0 for i in range(R + 1)]
    ratio_o = [s.v[i] / o.v[i] if o.v[i] else 0 for i in range(R + 1)]
    out.append(dict(survey_year=k[0], county=k[1], bedrooms=k[2], structure=k[3], tenure=k[4],
                    sample_units=u.n, units=round(u.v[0]), units_moe90=round(1.645 * se(u.v)),
                    occupied_units=round(o.v[0]), children_5_17=round(c.v[0]), public_students_5_17=round(s.v[0]),
                    students_moe90=round(1.645 * se(s.v)), sample_students=s.n,
                    students_per_unit=round(ratio[0], 3), per_unit_moe90=round(1.645 * se(ratio), 3),
                    students_per_occupied_unit=round(ratio_o[0], 3), per_occupied_moe90=round(1.645 * se(ratio_o), 3)))
os.makedirs(os.path.join(ROOT, 'analysis', 'data'), exist_ok=True)
with open(os.path.join(ROOT, 'analysis', 'data', 'acs_new_housing_school_yield.csv' if WINDOW == 2 else f'acs_new_housing_school_yield_{WINDOW}yr.csv'), 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(out[0])); w.writeheader(); w.writerows(out)
for d in out:
    if d['county'] == 'All 3 counties' and d['bedrooms'] == 'All' and d['structure'] == 'All' and d['tenure'] == 'All' or d['survey_year'] == '2019-2024 pooled':
        print({k: d[k] for k in ('survey_year', 'county', 'bedrooms', 'structure', 'tenure', 'sample_units', 'units', 'public_students_5_17', 'students_per_unit', 'per_unit_moe90', 'students_per_occupied_unit')})
