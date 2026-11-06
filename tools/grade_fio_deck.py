#!/usr/bin/env python3
"""Make a 'graded' copy of the Nov 9, 2026 FIO presentation (BoardBook doc 14644366).

The original slides are kept unchanged on the left of each page; red marks (circles, strike-throughs, numbered
markers) are drawn over them, and handwritten-style notes go in a margin on the right. A grade sheet is added as page 1.
Findings and their sources: analysis/meetings/2026-11-09_fio_materials.md.

Usage: python3 tools/grade_fio_deck.py [FONT_DIR]   (FONT_DIR holds Kalam-400.ttf / Kalam-700.ttf; falls back to Helvetica)
Output: analysis/meetings/2026-11-09_fio_presentation_graded.pdf
"""
import glob, os, sys
import pymupdf as fitz

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
SRC = glob.glob(os.path.join(ROOT, 'sources/boardbook/meetings/2026-11-09_776245_*/attachments/14644366_*.pdf'))[0]
OUT = os.path.join(ROOT, 'analysis/meetings/2026-11-09_fio_presentation_graded.pdf')
FONTDIR = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, 'tools/fonts')

RED = (0.80, 0.07, 0.07)
PAPER = (1.0, 0.985, 0.94)
INK = (0.12, 0.12, 0.12)
W0, H = 720, 405
MARGIN = 330
W = W0 + MARGIN

# Each finding: page -> dict(points, marks=[(kind, rect, label)], notes=[(label, text)])
# kind: 'oval' circles a rect; 'strike' draws a line through it; 'box' draws a rectangle.
F = {
 5: dict(points=4, marks=[('oval', (150, 300, 632, 327), 1)],
     notes=[(1, 'Not the 21 biggest increases. Missing: Harrison Park +215, Tubman +151, Lent +147, Rieke +117, Roseway Heights +116. '
                'Included: Capitol Hill +68, Ockley Green +110. (Peak vs. no-change projection, PPS family guides.)')]),
 6: dict(points=0, marks=[('oval', (474, 291, 630, 311), 1), ('oval', (90, 160, 216, 213), 2), ('oval', (90, 267, 216, 290), 2)],
     notes=[(1, 'Noted: special-ed rooms count 12 students.'),
            (2, 'Noted: 24 / 27 / 30 per room by size; one art/music room comes out at K-5. We use these rules to check p.19 and p.26.')]),
 13: dict(points=2, marks=[('oval', (10, 145, 118, 170), 1)],
      notes=[(1, 'Capitol Hill was 375 in PPS\'s April 2026 table. At 375, the 387 peak is 103%. The +42 is not explained.')]),
 16: dict(points=2, marks=[('oval', (10, 145, 118, 170), 1), ('oval', (10, 188, 150, 210), 2), ('oval', (10, 230, 175, 252), 3)],
      notes=[(1, 'Was 525 in April. At 525 the peak is 104%.'), (2, 'Peak 544...'), (3, '...is more than the most students Duniway has ever had (512).')]),
 17: dict(points=2, marks=[('oval', (14, 303, 120, 320), 1)],
      notes=[(1, '7 special-ed rooms here, but PPS\'s capacity model sets aside only 3. Capacity (623) was not reduced, so it is too high. Peak 669 is already 107%.')]),
 19: dict(points=9,
      marks=[('oval', (10, 230, 185, 252), 1), ('strike', (15, 241, 40, 241), None),
             ('oval', (10, 145, 118, 170), 2), ('oval', (14, 303, 120, 330), 3),
             ('oval', (10, 188, 150, 210), 4), ('oval', (100, 52, 203, 86), 5), ('oval', (474, 369, 560, 386), 6)],
      notes=[(1, 'Wrong. PPS\'s own capacity model lists Hayhurst at 396 in 2019-20. The 640 adds Odyssey (244), which moved to East Sylvan in 2016. '
                 'Most ever in this building: 499 in fall 2015.'),
             (2, '525 matches PPS\'s Nov 2 model: 20 rooms x 27 + 2 x 30 + gym 30 = 630, minus 5 set-aside rooms = 525. But the model takes the gym '
                 'out at 27, not 30, and leaves 15 seats in each special-ed room (its rule says 12). By its own rules: 516.'),
             (3, 'The model sets aside 2 special-ed rooms + a Learning Center, not 7. If 7 is right, capacity is about 468.'),
             (4, '469 = 89% of 525, 91% of 516. In 2016, PPS\'s figures put a K-5-only Hayhurst at about 464 seats (327 students = 70.6%).'),
             (5, '"Ready"? In 2016 PPS called 499 students here "Over-Crowding" (101.8%) and moved a whole program out.'),
             (6, 'This box says 4 special-ed rooms; the left panel says 7. Which is it?')]),
 20: dict(points=2, marks=[('oval', (10, 188, 150, 210), 1), ('oval', (14, 303, 120, 320), 2), ('oval', (474, 368, 560, 385), 3)],
      notes=[(1, '747 / 711 = 105%.'), (2, '5 special-ed rooms here...'), (3, '...3 here, and 1 in PPS\'s capacity model.')]),
 21: dict(points=3, marks=[('oval', (10, 145, 118, 170), 1), ('oval', (576, 337, 700, 356), 2)],
      notes=[(1, 'Was 510 in April. At 510 the 554 peak is 109%. Peak is also above the most ever enrolled (456).'),
             (2, 'Maplewood\'s Intensive Skills students would move into a building rated "Not Yet Ready."')]),
 22: dict(points=1, marks=[],
      notes=[(None, 'Hidden text from other slides sits under pages 22-29 (e.g. "561 students", "456 students in 2017-2018"). '
                    'It is invisible here but is what screen readers and copy-paste pick up.')]),
 26: dict(points=4, marks=[('oval', (10, 145, 118, 170), 1), ('oval', (14, 303, 120, 320), 2), ('oval', (530, 362, 690, 381), 3)],
      notes=[(1, 'Was 633 in April. Now 499: the change is not explained.'),
             (2, '3 special-ed rooms counted...'),
             (3, '...but 6-7 needed for the program. At about 15 seats per extra room (p.6), capacity is ~440-455, so the 487 peak is ~107-111%.')]),
 27: dict(points=5, marks=[('oval', (10, 145, 118, 170), 1), ('oval', (10, 188, 150, 210), 2), ('oval', (92, 50, 194, 84), 3)],
      notes=[(1, 'Was 496 in April.'), (2, '465 / 419 = 111%.'), (3, 'Over capacity at peak, yet rated "Ready." George at 107% is "Not Yet Ready."')]),
 28: dict(points=2, marks=[('oval', (10, 145, 118, 170), 1), ('oval', (10, 230, 175, 252), 2)],
      notes=[(1, 'Was 465 in April. At 465 the 507 peak is 109%.'), (2, 'Peak 507 is above the most Vestal has ever had (451).')]),
 29: dict(points=5, marks=[('oval', (10, 188, 150, 210), 1), ('oval', (106, 50, 209, 84), 2), ('oval', (14, 303, 120, 320), 3), ('oval', (478, 370, 560, 389), 4)],
      notes=[(1, '466 / 416 = 112%.'), (2, 'Over capacity at peak, yet rated "Ready."'),
             (3, '1 special-ed room counted...'), (4, '...4-5 needed with Woodmere. Capacity would drop further.')]),
 30: dict(points=2, marks=[('oval', (60, 246, 442, 273), 1)],
      notes=[(1, 'Main floor only. Hosford\'s basement classrooms are "inaccessible or difficult" (p.20); Gray\'s route is "indirect and difficult" (p.18); '
                 'many receiving schools have no elevator.')]),
 31: dict(points=3, marks=[('oval', (66, 278, 112, 300), 1), ('oval', (455, 174, 499, 196), 1)],
      notes=[(1, 'Rieke gets seismic money in both scenarios but has no readiness profile, even though it takes 30% of Maplewood plus the '
                 'Stephens Creek Crossing area and has the highest seismic score of any receiving school (9.6).')]),
 33: dict(points=8, marks=[('box', (431, 203, 474, 219), 1), ('box', (519, 203, 562, 219), 1), ('box', (474, 203, 518, 219), 2),
                           ('oval', (575, 125, 700, 152), 3), ('box', (321, 150, 368, 166), 4)],
      notes=[(1, 'Normalized: Scenario B 33.6% vs. status quo 33.5%. B is slightly WORSE than doing nothing.'),
             (2, 'Scenario A improves on doing nothing by 1.0 point (234 students).'),
             (3, 'The "reduction" is measured from 2025. Most of it (-2,926 students) comes from bond retrofits that happen under the status quo too.'),
             (4, 'Left table: Scenario B total (25,031) is larger than status quo (24,646). It compares 2025-26 with 2031-32 enrollment.')]),
}

SUMMARY = [
 ('p.19', 'Hayhurst: "640" is wrong (396; building max 499 in 2015); 7 special-ed rooms vs 4 on the same page and 3 in the model; model rules give 516', 9),
 ('p.33', 'Seismic: Scenario B is worse than the status quo on 9.0+ buildings; the "reduction" is mostly bond retrofits', 8),
 ('p.27', 'Sitton rated "Ready" at 111% of capacity', 5),
 ('p.29', 'Whitman rated "Ready" at 112% of capacity; 1 vs 4-5 special-ed rooms', 5),
 ('p.5', '"21 buildings with the highest increase" leaves out Harrison Park, Tubman, Lent, Rieke, Roseway Heights', 4),
 ('p.26', 'Rosa Parks: 3 special-ed rooms counted vs 6-7 needed; capacity cut from 633 to 499 unexplained', 4),
 ('p.21', 'Markham: capacity raised 510 -> 561; Maplewood ISC students into a "Not Yet Ready" building', 3),
 ('p.31', 'Rieke gets seismic money but no readiness profile', 3),
 ('p.13 / 16 / 28', 'Capacity raised since April at Capitol Hill, Duniway, Vestal (over 100% under April figures)', 6),
 ('p.17 / 20', 'George, Hosford: more special-ed rooms than the capacity model sets aside', 4),
 ('p.30', '"All campuses ADA accessible to the main floor" understates access problems', 2),
 ('p.22-29', 'Hidden leftover text from other slides', 1),
]

def fonts(page):
    try:
        page.insert_font(fontname='kalb', fontfile=os.path.join(FONTDIR, 'Kalam-700.ttf'))
        page.insert_font(fontname='kalr', fontfile=os.path.join(FONTDIR, 'Kalam-400.ttf'))
        return 'kalb', 'kalr'
    except Exception:
        return 'hebo', 'helv'

_FONTS = {}
def _font(fn):
    key = {'kalb': 'Kalam-700.ttf', 'kalr': 'Kalam-400.ttf'}.get(fn)
    if fn not in _FONTS:
        _FONTS[fn] = fitz.Font(fontfile=os.path.join(FONTDIR, key)) if key else fitz.Font(fn)
    return _FONTS[fn]

def ctext(page, cx, cy, text, fn, size, color):
    """Single line of text centered on (cx, cy); Kalam's tall line box makes insert_textbox drop short labels."""
    f = _font(fn)
    w = f.text_length(text, fontsize=size)
    page.insert_text((cx - w / 2, cy + size * 0.33), text, fontname=fn, fontsize=size, color=color)

def marker(page, x, y, label, fb):
    r = 7.5
    page.draw_circle((x, y), r, color=RED, fill=RED)
    ctext(page, x, y, str(label), fb, 9.5, (1, 1, 1))

def grade_page(out, src, pno, spec):
    page = out.new_page(width=W, height=H)
    page.show_pdf_page(fitz.Rect(0, 0, W0, H), src, pno)
    fb, fr = fonts(page)
    page.draw_rect(fitz.Rect(W0, 0, W, H), color=None, fill=PAPER)
    page.draw_line((W0, 0), (W0, H), color=RED, width=1.2)
    if spec is None:
        return
    pts = spec['points']
    # deduction badge
    if pts:
        page.draw_circle((W - 34, 32), 22, color=RED, width=2.2)
        ctext(page, W - 34, 32, f'-{pts}', fb, 18, RED)
    else:
        ctext(page, W - 34, 32, 'OK', fb, 18, RED)
    seen = set()
    for kind, rect, label in spec['marks']:
        r = fitz.Rect(*rect)
        if kind == 'oval':
            page.draw_oval(r, color=RED, width=1.8)
        elif kind == 'box':
            page.draw_rect(r, color=RED, width=1.8)
        elif kind == 'strike':
            page.draw_line((r.x0 - 2, r.y0), (r.x1 + 2, r.y1), color=RED, width=2.2)
        if label is not None and (label, round(r.x0)) not in seen:
            seen.add((label, round(r.x0)))
            marker(page, r.x1 + 2, r.y0 + 1, label, fb)
    y = 62
    x0, x1 = W0 + 14, W - 12
    for label, text in spec['notes']:
        tx0 = x0
        if label is not None:
            marker(page, x0 + 7, y + 8, label, fb)
            tx0 = x0 + 20
        box = fitz.Rect(tx0, y, x1, H - 8)
        rc = page.insert_textbox(box, text, fontname=fr, fontsize=10.5, color=RED, lineheight=1.15)
        used = (H - 8 - y) - rc if rc >= 0 else (H - 8 - y)
        y += used + 9

def grade_sheet(out, total):
    page = out.new_page(width=W, height=H)
    fb, fr = fonts(page)
    page.draw_rect(page.rect, color=None, fill=PAPER)
    page.insert_textbox(fitz.Rect(40, 26, 700, 60), 'FIO Committee Presentation, Nov 9, 2026: graded copy', fontname='hebo', fontsize=19, color=INK)
    page.insert_textbox(fitz.Rect(40, 56, 700, 92),
        'Original PPS slides (BoardBook document 14644366), unchanged. Red marks and margin notes check the slides against PPS\'s own '
        'rules (p.6), its Nov 2 capacity model, its April 2026 enrollment and utilization table, the family guides, and 2015-16 enrollment records.',
        fontname='helv', fontsize=9.5, color=INK)
    score = 100 - total
    page.draw_circle((W - 110, 110), 62, color=RED, width=3)
    ctext(page, W - 110, 100, f'{score}', fb, 50, RED)
    ctext(page, W - 110, 140, '/ 100', fb, 17, RED)
    page.insert_textbox(fitz.Rect(W - 230, 178, W - 10, 240), 'Please show your work. The capacity numbers on these slides do not follow from the room counts on the same slides.',
                        fontname=fr, fontsize=11.5, color=RED, align=1)
    y = 100
    for pg, text, pts in SUMMARY:
        page.insert_textbox(fitz.Rect(40, y, 120, y + 30), pg, fontname='hebo', fontsize=9.5, color=INK)
        rc = page.insert_textbox(fitz.Rect(120, y, 740, y + 30), text, fontname='helv', fontsize=9.5, color=INK)
        page.insert_text((750, y + 10), f'-{pts}', fontname=fb, fontsize=13, color=RED)
        y += 21
    page.insert_textbox(fitz.Rect(40, H - 46, W - 40, H - 10),
        'Sources and full analysis: github.com/timaelliott/save-our-schools, analysis/meetings/2026-11-09_fio_materials.md. '
        'Prepared Nov 6, 2026 from PPS public records.', fontname='helv', fontsize=8.5, color=(0.35, 0.35, 0.35))

def main():
    src = fitz.open(SRC)
    out = fitz.open()
    total = sum(p for _, _, p in SUMMARY)
    grade_sheet(out, total)
    for pno in range(src.page_count):
        grade_page(out, src, pno, F.get(pno + 1))
    out.set_metadata({'title': 'FIO Presentation 11.09.26 (graded copy)', 'author': 'save-our-schools research archive',
                      'subject': 'PPS FIO Committee presentation, Nov 9, 2026, with corrections'})
    out.save(OUT, garbage=3, deflate=True)
    print(OUT, out.page_count, 'pages; score', 100 - total)

if __name__ == '__main__':
    main()
