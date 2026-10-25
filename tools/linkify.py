#!/usr/bin/env python3
"""Turn citation tags in analysis Markdown into clickable links, keeping the tag text.

  python3 tools/linkify.py analysis/board_closure_stance/rashelle-chase-miller.md [more.md ...] [--check]

[YT:<id>@H:MM:SS]          -> YouTube at that second
[BB:<docId> p.N]           -> BoardBook PDF (#page=N)
[NEWS:<id>]                -> the article URL in sources/news/index.jsonl
[PPS:<path> p.N]           -> the original pps.net / Google Drive URL from sources/pps_net/_manifests (#page=N)
[MTG:<date>/<meetingId>]   -> the BoardBook meeting agenda
[AUDIO:<path>@H:MM:SS]     -> the archived audio on GitHub ([AUDIO:<path>@L<n>] -> line n of the archived transcript)
[LTR:<stem> L<n>]          -> the archived letter on GitHub (#L<n>)

A tag becomes [TAG](url), so the tag text stays searchable. Tags already linked are left alone.
--check prints what would change and any tags it could not resolve, without writing.
"""
import csv, glob, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GH = "https://github.com/timaelliott/save-our-schools/blob/main/"

def _load():
    bb = {}
    for r in csv.DictReader(open(ROOT / "sources/boardbook/attachments_index.csv")):
        if r.get("url"): bb[r["document_id"]] = r["url"]
    mtg = {}
    for r in csv.DictReader(open(ROOT / "sources/boardbook/meetings_index.csv")):
        mtg[r["meeting_id"]] = r.get("agenda_url") or ""
        mu = r.get("minutes_url") or ""
        m = re.search(r"(\d{6,})", mu)
        if m and mu: bb.setdefault(m.group(1), mu)
    news = {}
    for l in open(ROOT / "sources/news/index.jsonl"):
        if l.strip():
            n = json.loads(l); news[n["id"]] = n.get("url", "")
    pps = {}
    for f in glob.glob(str(ROOT / "sources/*/_manifests/*.json")):
        try: d = json.load(open(f))
        except Exception: continue
        items = d if isinstance(d, list) else d.get("files", d.get("items", []))
        for it in items if isinstance(items, list) else []:
            if not isinstance(it, dict): continue
            p = it.get("path") or it.get("save_as") or ""
            u = it.get("orig") or it.get("url") or ""
            if p and u.startswith("http"): pps.setdefault(p, u)
    return bb, mtg, news, pps

BB, MTG, NEWS, PPS = _load()

def secs(t):
    h, m, s = (t.split(":") + ["0", "0"])[:3] if t.count(":") == 2 else ["0"] + t.split(":")
    return int(h) * 3600 + int(m) * 60 + int(s)

def url_for(tag):
    kind, _, body = tag.partition(":")
    if kind == "YT":
        m = re.match(r"([A-Za-z0-9_-]{11})@(\d+:\d\d(?::\d\d)?)", body)
        return m and f"https://www.youtube.com/watch?v={m.group(1)}&t={secs(m.group(2))}s"
    if kind == "BB":
        m = re.match(r"(\d+)(?:\s+p\.(\d+))?", body)
        if not m: return None
        u = BB.get(m.group(1)) or f"https://meetings.boardbook.org/Documents/DownloadPDF/{m.group(1)}?org=915"
        return u + (f"#page={m.group(2)}" if m.group(2) else "")
    if kind == "NEWS":
        return NEWS.get(body.strip()) or None
    if kind == "PPS":
        m = re.match(r"(\S+?)(?:#\S+)?(?:\s+p\.(\d+))?$", body.strip())
        if not m: return None
        p = m.group(1).replace("sources/", "", 1)
        u = PPS.get(p)
        if not u: return GH + "sources/" + p
        return u + (f"#page={m.group(2)}" if m.group(2) and "drive.google" not in u else "")
    if kind == "MTG":
        mid = body.split("/")[-1]
        return MTG.get(mid) or None
    if kind == "AUDIO":
        stem, _, at = body.partition("@")
        if at.startswith("L"):  # transcript-only interview: line in the raw transcript
            return GH + "sources/audio/" + stem + ".transcript.txt#" + at
        ext = ".mp4" if (ROOT / "sources/audio" / (stem + ".mp4")).exists() else ".mp3"
        return GH + "sources/audio/" + stem + ext
    if kind == "LTR":
        m = re.match(r"(\S+)(?:\s+L(\d+))?", body)
        return m and GH + f"sources/correspondence/{m.group(1)}.txt" + (f"#L{m.group(2)}" if m.group(2) else "")
    return None

TAG = re.compile(r"\[((?:YT|BB|NEWS|PPS|MTG|AUDIO|LTR):[^\]\[]+)\](?!\()")

def linkify(text, missing):
    def rep(m):
        u = url_for(m.group(1))
        if not u: missing.append(m.group(1)); return m.group(0)
        return f"[{m.group(1)}]({u})"
    return TAG.sub(rep, text)

if __name__ == "__main__":
    check = "--check" in sys.argv
    for f in [a for a in sys.argv[1:] if not a.startswith("--")]:
        p = Path(f); old = p.read_text(); missing = []
        new = linkify(old, missing)
        n = len(TAG.findall(old)) - len(missing)
        print(f"{f}: {n} tags linked, {len(missing)} unresolved {sorted(set(missing))[:10]}")
        if not check and new != old: p.write_text(new)
