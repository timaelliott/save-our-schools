#!/usr/bin/env python3
"""Hourly BoardBook ID probe: runs tools/boardbook_id_probe.php over the IDs just past the newest known PPS document and
reports every ID that answers 200 (a document viewable under PPS org 915), with its title from the WebViewer page.

Window: starts after the highest PPS document ID we know (attachments_index.csv + earlier probe hits, never below
14695005). BoardBook IDs are shared by all its customers and grow ~500/hour, so the window is 10,000 IDs plus 600 per
hour since that start was first used (capped at 40,000), so it keeps reaching the newest uploads even over a weekend.

State: analysis/_watch/boardbook_probe_state.json (start, when it was first used, every 200 hit ever seen).
Prints a JSON summary; "new_hits" lists 200s not reported before and not already in attachments_index.csv.
Run from the repo root: python3 tools/boardbook_probe_run.py [--concurrency 10]
"""
import csv, json, re, subprocess, sys, html, time, urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / 'analysis/_watch/boardbook_probe_state.json'
FLOOR, BASE, PER_HOUR, CAP = 14695005, 10_000, 600, 40_000
VIEW = 'https://meetings.boardbook.org/Documents/WebViewer/915?file='


def main():
    conc = int(sys.argv[sys.argv.index('--concurrency') + 1]) if '--concurrency' in sys.argv else 10
    now = datetime.now(timezone.utc)
    st = json.loads(STATE.read_text()) if STATE.exists() else {'start': None, 'start_first_used': None, 'hits': {}}
    known = {int(r['document_id']) for r in csv.DictReader(open(ROOT / 'sources/boardbook/attachments_index.csv'))
             if r['document_id'].isdigit()}
    start = max([FLOOR - 1, *[k for k in known if k < 20_000_000], *map(int, st['hits'])]) + 1
    if start != st['start']:
        st['start'], st['start_first_used'] = start, now.isoformat(timespec='seconds')
    hours = (now - datetime.fromisoformat(st['start_first_used'])).total_seconds() / 3600
    count = min(CAP, BASE + int(PER_HOUR * hours))
    t0 = time.time()
    out = subprocess.run(['php', str(ROOT / 'tools/boardbook_id_probe.php'), str(start), str(count), str(conc)],
                         capture_output=True, text=True, timeout=1800)
    rows = [l.split(',') for l in out.stdout.split()]
    codes = {}
    for _, c in rows: codes[c] = codes.get(c, 0) + 1
    new = []
    for i, c in rows:
        if c != '200' or i in st['hits']: continue
        try:
            page = urllib.request.urlopen(VIEW + i, timeout=20).read().decode('utf-8', 'replace')
            m = re.search(r'<title>(.*?)</title>', page, re.S)
            title = re.sub(r'\s+', ' ', html.unescape(m.group(1))).replace(' - BoardBook Premier', '').strip() if m else ''
        except Exception as e:
            title = f'(title not read: {e})'
        hit = dict(first_seen=now.isoformat(timespec='seconds'), title=title, url=VIEW + i, already_archived=int(i) in known)
        st['hits'][i] = hit
        if not hit['already_archived']: new.append(dict(id=int(i), **hit))
    st['last_run'] = dict(at=now.isoformat(timespec='seconds'), start=start, count=count, seconds=round(time.time() - t0),
                          codes=codes, curl_errors=len(out.stderr.strip().splitlines()) if out.stderr.strip() else 0)
    STATE.parent.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps(st, indent=1, ensure_ascii=False) + '\n')
    print(json.dumps(dict(start=start, end=start + count - 1, codes=codes, new_hits=new,
                          all_200=[int(i) for i, c in rows if c == '200']), indent=1, ensure_ascii=False))


if __name__ == '__main__':
    main()
