"""Per-home public-school yield (age 5-17) in new 2-4 / 3-4 BR detached and attached homes, tri-county,
for every combination of ACS 1-year surveys, alternative build windows, and the 5-year PUMS files.
Run from repo root: python3 analysis/topics/_build/acs_yield_year_combos.py"""
import csv, io, zipfile, collections, itertools, os, json
SRC = 'sources/census/acs_pums'
PM = set()
for f in ('2010_Census_Tract_to_2010_PUMA.txt', '2020_Census_Tract_to_2020_PUMA.txt'):
    PM |= {x['PUMA5CE'] for x in csv.DictReader(open(f'{SRC}/geo/{f}', encoding='utf-8-sig')) if x['STATEFP'] == '41' and x['COUNTYFP'] in ('051', '067', '005')}

def rows(path):
    z = zipfile.ZipFile(path); n = [n for n in z.namelist() if n.endswith('.csv')][0]
    return csv.DictReader(io.TextIOWrapper(z.open(n), encoding='utf-8'))

def yrblt(r):
    if 'YBL' in r and 'YRBLT' not in r:
        return {'23': 2019, '22': 2018, '21': 2017}.get(r['YBL'])
    v = r['YRBLT']
    return int(v) if v and v.isdigit() and int(v) >= 2011 and v not in ('2010',) else None

def load(hpath, ppath):
    """Return list of new-ish homes: (survey_year, built, bld, bd, wgtp, persons_w, students_w)."""
    H = {}
    for r in rows(hpath):
        if r.get('TYPEHUGQ', r.get('TYPE')) != '1' or r['PUMA'].zfill(5) not in PM: continue
        b = yrblt(r); bd = int(r['BDSP'] or -1)
        if b is None or not 2 <= bd <= 4 or r['BLD'] not in ('02', '03'): continue
        H[r['SERIALNO']] = [int(r['SERIALNO'][:4]), b, r['BLD'], bd, float(r['WGTP']), 0.0, 0.0]
    for r in rows(ppath):
        h = H.get(r['SERIALNO'])
        if not h: continue
        h[5] += float(r['PWGTP'])
        if 5 <= int(r['AGEP']) <= 17 and r['SCH'] == '2': h[6] += float(r['PWGTP'])
    return list(H.values())

def yld(homes, keep):
    sel = [h for h in homes if keep(h)]
    u = sum(h[4] for h in sel); s = sum(h[6] for h in sel); p = sum(h[5] for h in sel)
    return dict(n=len(sel), per_home=round(s / u, 3) if u else None, per_person=round(s / p, 3) if p else None)

one = {y: load(f'{SRC}/{y}/csv_hor.zip', f'{SRC}/{y}/csv_por.zip') for y in (2019, 2021, 2022, 2023, 2024)}
groups = {'detached 2-4BR': lambda h: h[2] == '02', 'attached 2-4BR': lambda h: h[2] == '03',
          'detached 3-4BR': lambda h: h[2] == '02' and h[3] >= 3, 'attached 3-4BR': lambda h: h[2] == '03' and h[3] >= 3}
windows = {'built Y or Y-1': (0, 1), 'built Y only': (0,), 'built Y-1 only': (1,), 'built Y-2..Y': (0, 1, 2)}
out = []
yrs = sorted(one)
for k in range(1, 6):
    for combo in itertools.combinations(yrs, k):
        homes = [h for y in combo for h in one[y]]
        for wn, w in windows.items():
            for gn, g in groups.items():
                d = yld(homes, lambda h: g(h) and (h[0] - h[1]) in w)
                out.append(dict(source='1-year', surveys='+'.join(map(str, combo)), window=wn, group=gn, **d))
for lab in ('2019-2023', '2020-2024'):
    homes = load(f'{SRC}/5yr_{lab}/csv_hor.zip', f'{SRC}/5yr_{lab}/csv_por.zip')
    last = int(lab[-4:])
    for wn, keep in {'built Y or Y-1 (per-record survey year)': lambda h: h[0] - h[1] in (0, 1),
                     f'naive: built {last-1}-{last}, any survey year': lambda h: h[1] in (last - 1, last),
                     'built 2020 or later, any survey year': lambda h: h[1] >= 2020}.items():
        for gn, g in groups.items():
            out.append(dict(source='5-year', surveys=lab, window=wn, group=gn, **yld(homes, lambda h: g(h) and keep(h))))
with open('analysis/data/acs_yield_year_combos.csv', 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(out[0])); w.writeheader(); w.writerows(out)
print(len(out))
