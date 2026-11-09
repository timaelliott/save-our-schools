import csv, io, os, zipfile, collections, math, sys
sys.path.insert(0,'analysis/topics/_build')
SRC='sources/census/acs_pums'; R=80
def cmap(y):
    f='2010_Census_Tract_to_2010_PUMA.txt' if y<2022 else '2020_Census_Tract_to_2020_PUMA.txt'
    return {x['PUMA5CE'] for x in csv.DictReader(open(f'{SRC}/geo/{f}',encoding='utf-8-sig')) if x['STATEFP']=='41' and x['COUNTYFP'] in ('051','067','005')}
def rows(y,k):
    z=zipfile.ZipFile(f'{SRC}/{y}/csv_{k}.zip'); n=[n for n in z.namelist() if n.endswith('.csv')][0]
    return csv.DictReader(io.TextIOWrapper(z.open(n),encoding='utf-8'))
def built(y,r,ages):
    if y==2019: return r['YBL'] in [str(23-a) for a in ages]
    return r['YRBLT'] in [str(y-a) for a in ages]
cases={'ours: built Y or Y-1':(0,1),'built Y-1 or Y-2 (excl. survey yr)':(1,2),'built Y, Y-1, Y-2':(0,1,2)}
for label,ages in cases.items():
    T=collections.defaultdict(lambda: collections.Counter())
    for y in (2019,2021,2022,2023,2024):
        if y==2021 and 2 in ages and label!='ours: built Y or Y-1': pass
        pm=cmap(y); H={}
        for r in rows(y,'hor'):
            if r.get('TYPEHUGQ',r.get('TYPE'))!='1' or r['PUMA'].zfill(5) not in pm or not built(y,r,ages): continue
            bd=int(r['BDSP'] or -1)
            if not 2<=bd<=4 or r['BLD'] not in ('02','03'): continue
            for g in [('det' if r['BLD']=='02' else 'att','2-4'), ('det' if r['BLD']=='02' else 'att','3-4')] if bd>=3 else [('det' if r['BLD']=='02' else 'att','2-4')]:
                T[g]['units']+=float(r['WGTP']); T[g]['n']+=1
                if int(r['NP'])>0: T[g]['occ']+=float(r['WGTP'])
            H[r['SERIALNO']]=(r['BLD'],bd,float(r['WGTP']))
        for r in rows(y,'por'):
            h=H.get(r['SERIALNO'])
            if not h: continue
            gs=[('det' if h[0]=='02' else 'att','2-4')]+([('det' if h[0]=='02' else 'att','3-4')] if h[1]>=3 else [])
            a=int(r['AGEP']); stu = 5<=a<=17 and r['SCH']=='2'
            for g in gs:
                T[g]['persons']+=float(r['PWGTP']); T[g]['wgtp_over_persons']+=h[2]
                if stu: T[g]['stud']+=float(r['PWGTP']); T[g]['stud_n']+=1
    print('==',label)
    for g,c in sorted(T.items()):
        print(f"  {g}: n={c['n']} students/unit={c['stud']/c['units']:.3f}  students/occupied={c['stud']/c['occ']:.3f}  students/PERSONS={c['stud']/c['persons']:.3f}  students/sum(WGTP over person rows)={c['stud']/c['wgtp_over_persons']:.3f}  avg hh size={c['persons']/c['occ']:.2f}")
