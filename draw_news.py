"""Front page for Friday 20 November 2026: 25 stories on one 1024x1024 sheet.

Sections top to bottom: masthead, red band, numbers ticker, day timeline,
three hero stories, a ten-story featured grid, then a world map beside a
twelve-item "also today" column, a date check, and a footer.

The three heroes carry generated art; the grid reuses one tall ten-band
collage, bands taken in story order. Band edges were measured off the
collage file by scanning for uniform stretches near even spacing.

Fit discipline: each headline and deck is wrapped to its box and asserted
to fit — nothing overflows, nothing is cut off. The picture is fully
deterministic: same inputs, same PNG bytes. Usage:
    python3 draw_news.py
which writes entry.png (1024x1024, roughly 600-750 KiB).

Dating rule: a story counts if it happened, or was first reported, on
Friday 20 November 2026 in any time zone. A few items were first reported
late on 19 November UTC, which is already 20 November in Asian zones:
the ANT close at 22:00 UTC, the Senate vote in the US evening, Kyiv
updates at 21:26Z, Bangladesh at 18:05Z, the Trump-Axios call on Thursday
evening US time. Events scheduled for the 20th itself (Akvan's noon
landfall, the COP31 close, the UK-EU summit, the ANT offering close)
are carried as the day's events. The date-check box names what was
kept out as other days' news.
"""

from pathlib import Path

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

ROOT = Path(__file__).resolve().parent
ART_DIR = ROOT / "assets"

PAGE_W, PAGE_H = 1024, 1024

# --- colours ---
COL_PAPER = (250, 247, 240)
COL_INK = (18, 18, 18)
COL_RED = (178, 24, 28)
COL_NAVY = (31, 57, 107)
COL_TEAL = (13, 92, 96)
COL_OCHRE = (176, 113, 26)
COL_GREY = (108, 108, 104)
COL_PALE = (236, 232, 222)
COL_LINE = (198, 194, 184)
COL_BODY = (40, 40, 40)
COL_GRID = (225, 221, 210)
COL_LAND = (214, 208, 192)
COL_WHITE = (255, 255, 255)

# --- typefaces (Liberation, shipped on the machine) ---
FONT_DIR = "/usr/share/fonts/truetype/liberation"
FONT_PATHS = {
    "serif": FONT_DIR + "/LiberationSerif-Regular.ttf",
    "serif_b": FONT_DIR + "/LiberationSerif-Bold.ttf",
    "sans": FONT_DIR + "/LiberationSans-Regular.ttf",
    "sans_b": FONT_DIR + "/LiberationSans-Bold.ttf",
}


def face(kind, size):
    return ImageFont.truetype(FONT_PATHS[kind], size)


# --- the 25 stories: heroes first, then the featured ten ---
# kind: "hero" (big art, top row) or "grid" (collage band).
# band: index into BAND_EDGES for grid stories. place: map label.
STORIES = [
    {"rank": 1, "kind": "hero", "section": "US · MIDEAST", "status": "REPORTED",
     "head": "Trump rules out any new Iran strike before 2027",
     "deck": "After Shenzhen, Trump tells Axios he is 'not rushing' a decision, while Israel's envoy warns it may 'go it alone'. — NY Post",
     "art": "hero-iran"},
    {"rank": 2, "kind": "hero", "section": "ASIA · STORM", "status": "REPORTED",
     "head": "Akvan comes ashore in Odisha at noon",
     "deck": "The cyclone crosses near Gopalpur with winds to 110 km/h; 105,304 people wait it out in 1,224 shelters. — IMD",
     "art": "hero-akvan"},
    {"rank": 3, "kind": "hero", "section": "EUROPE · WAR", "status": "REPORTED",
     "head": "Kyiv raid damages two embassies",
     "deck": "A daylong drone attack kills one and wounds five; Austrian and Dutch missions are hit and a cathedral loses windows. — AFP",
     "art": "hero-kyiv"},
    {"rank": 4, "kind": "grid", "section": "EUROPE · CLIMATE", "status": "FORECAST",
     "head": "COP31 wraps up in Antalya",
     "deck": "Last day; fossil-fuel wording and the $120bn aid goal still open. — Reuters",
     "place": "ANTALYA", "band": 0},
    {"rank": 5, "kind": "grid", "section": "EUROPE · POLITICS", "status": "FORECAST",
     "head": "Burnham flies to Brussels for EU summit",
     "deck": "Summit opens at 10:30; food, energy and youth deals on the table.",
     "place": "BRUSSELS", "band": 1},
    {"rank": 6, "kind": "grid", "section": "MIDDLE EAST · GULF", "status": "REPORTED",
     "head": "Riyadh confirms its PIF Tower was hit",
     "deck": "Saudi Arabia confirms a strike damaged the wealth-fund tower.",
     "place": "RIYADH", "band": 2},
    {"rank": 7, "kind": "grid", "section": "US · POLITICS", "status": "REPORTED",
     "head": "Senate sides with Trump on Iran war powers",
     "deck": "Senators vote 51–48 against limits on Iran war powers.",
     "place": "WASHINGTON", "band": 3},
    {"rank": 8, "kind": "grid", "section": "ASIA · MARKETS", "status": "REPORTED",
     "head": "ANT ends debut day at $97.17, up 17%",
     "deck": "First trade $111.50, up 34%; the stock settles at $97.17 on day one.",
     "place": "NEW YORK", "band": 4},
    {"rank": 9, "kind": "grid", "section": "ASIA · POLITICS", "status": "REPORTED",
     "head": "Bangladesh shutdown turns violent",
     "deck": "Four killed; Yunus's home torched, 72 Grameen branches hit.",
     "place": "DHAKA", "band": 5},
    {"rank": 10, "kind": "grid", "section": "OCEANIA · SPORT", "status": "REPORTED",
     "head": "Nicholls ton opens the NZ–India Test",
     "deck": "Nicholls 113 not out; New Zealand close day one on 243–5. — Reuters",
     "place": "WELLINGTON", "band": 6},
    {"rank": 11, "kind": "grid", "section": "EUROPE · WAR", "status": "REPORTED",
     "head": "Trump to Europe: stop bankrolling the war",
     "deck": "Telegraph leads with Trump's message to Europe on Ukraine.",
     "place": "LONDON", "band": 7},
    {"rank": 12, "kind": "grid", "section": "MIDDLE EAST · WAR", "status": "REPORTED",
     "head": "Iran still holds 2,500 missiles",
     "deck": "US intel: Tehran keeps 2,500 missiles after nine months of war. — WSJ",
     "place": "TEHRAN", "band": 8},
    {"rank": 13, "kind": "grid", "section": "MIDDLE EAST · MARKETS", "status": "REPORTED",
     "head": "Gulf shares slide on Iran strife",
     "deck": "Most Gulf markets end lower as regional attacks weigh.",
     "place": "DUBAI", "band": 9},
]

# --- the other twelve, one line each ---
ALSO_LINES = [
    "WASHINGTON — Iran war cost passes $48bn. · Pentagon",
    "NEW YORK — ANT underwriters' option runs out today. · Reuters",
    "STOCKHOLM — Blast by Sweden's Kyiv embassy. · Reuters",
    "WASHINGTON — Trump: Iran seeks gas, bioweapons. · Fox News",
    "SHENZHEN — Summit declaration holds. · Reuters",
    "RIYADH — Houthis claim an airport hit as well. · Reuters",
    "KYIV — 98 drones and Onyx missiles overnight. · Ukrinform",
    "NEW YORK — S&P down 2% for a sixth straight day. · Reuters",
    "LONDON — Brent $90 while gold drops 3%. · Reuters",
    "NEW YORK — ANT offering ends today. · Reuters",
    "LONDON — European shares off 0.9%. · Reuters",
    "NEW YORK — Bitcoin dips below $62,000. · Reuters",
]

# --- the day in numbers ---
TICKER_ITEMS = [
    ("$97.17", "ANT ends debut up 17%"),
    ("105,304", "moved to shelter before Akvan"),
    ("51–48", "Senate backs Trump on Iran"),
    ("-2.0%", "S&P 500 down a sixth day"),
    ("$3,628", "gold off 3.1% in a day"),
    ("$48bn", "Iran war cost to date, Pentagon"),
]

# --- the day in hours ---
TIMELINE_ITEMS = [
    ("10:30", "BRUSSELS", "EU–UK summit begins"),
    ("12:00", "GOPALPUR", "Akvan comes ashore"),
    ("13:25", "BRUSSELS", "Summit news conference"),
    ("TODAY", "ANTALYA", "COP31 wraps up"),
    ("TODAY", "NEW YORK", "ANT offering ends"),
    ("THU PM", "WASHINGTON", "Trump defers Iran call"),
]

# --- map marks: (story, longitude, latitude, nudge x, nudge y) ---
MAP_MARKS = [
    (1, -77.0, 38.9, -14, -10),   # Washington: Trump and Iran
    (2, 85.0, 19.3, -14, 10),     # Gopalpur: Akvan landfall
    (3, 30.5, 50.4, 0, 0),        # Kyiv
    (4, 30.7, 36.9, 10, -6),      # Antalya: COP31, kept clear of Kyiv
    (5, 4.35, 50.85, 12, 8),      # Brussels: EU summit
    (6, 46.7, 24.7, -12, 8),      # Riyadh: PIF Tower
    (7, -77.0, 38.9, 14, 10),     # Washington: the Senate vote
    (8, -122.4, 37.8, 0, 0),      # San Francisco: Anthropic HQ, clear of NY/DC
    (9, 90.4, 23.8, 14, -8),      # Dhaka: Bangladesh
    (10, 174.8, -41.3, 0, 0),     # Wellington: NZ–India Test
    (11, -0.1, 51.5, -14, -8),    # London: Telegraph
    (12, 51.4, 35.7, 12, -6),     # Tehran: missiles
    (13, 55.3, 25.2, 14, -8),     # Dubai: Gulf shares
]

# --- date check: what this page counts, and what it leaves out ---
DATE_LINES = [
    ("DATE CHECK — Each story on this page happened, or was first reported, on Friday 20 November 2026.", True),
    ("19 NOVEMBER, NOT THE 20TH — Gaza tank raid ends; ICJ finds Myanmar guilty; Suneung exam; Indonesia asset law; Australia jobless 4.9%; Han term voided.", False),
    ("18 NOVEMBER — Fiji disaster declared; IAEA: N. Korea expands Yongbyon; Google launches Gemini 4 Neon; Modi meets William & Kate.", False),
    ("17 NOVEMBER AND BEFORE — COP31 D-8 framework (Tue); Equinor cyberattack (Tue); Vance 'no forever war' (Mon); Amazon $7bn (Tue).", False),
]

FOOTER_TEXT = (
    "Each story on this page happened, or was first reported, on Friday 20 November 2026. "
    "Claims carry attribution, not stated as fact. Sources: Reuters, AP, AFP, IMD, IAEA, "
    "Ukrinform, CNBC, NY Post, Axios, Fox News, Consilium, Pentagon, WSJ, Telegraph. "
    "Artwork generated; layout original."
)

# --- art files ---
ART_FILES = [
    ("hero-iran", "media-generation-hero-iran-0-de047e34-2b0e-491b-a852-f8b514f06582.png"),
    ("hero-akvan", "media-generation-hero-akvan-0-33d33542-6dd1-4457-a13d-1571bf030f8b.png"),
    ("hero-kyiv", "media-generation-hero-kyiv-0-84acd919-7b37-4400-9a55-d83397a65a99.png"),
]
ART = dict(ART_FILES)
STRIP_FILE = "media-generation-grid-collage-0-541ac79a-6691-4dbc-9eb2-8f151d4637d5.png"
BAND_EDGES = [0, 296, 568, 840, 1069, 1389, 1665, 1921, 2165, 2451, 2736]
STRIP_LEFT, STRIP_RIGHT = 8, 904


# --- drawing helpers ---
def fit_text(pen, text, font, max_w, limit=None):
    parts = text.split()
    rows, current = [], ""
    for word in parts:
        candidate = (current + " " + word).strip()
        if pen.textlength(candidate, font=font) <= max_w:
            current = candidate
        else:
            if current:
                rows.append(current)
            current = word
    if current:
        rows.append(current)
    if limit is not None:
        assert len(rows) <= limit, f"does not fit in {limit}: {text!r} -> {rows}"
    return rows


def crop_fill(pic, tw, th):
    sw, sh = pic.size
    if sw / sh > tw / th:
        nw = int(sh * tw / th)
        x0 = (sw - nw) // 2
        box = (x0, 0, x0 + nw, sh)
    else:
        nh = int(sw * th / tw)
        y0 = (sh - nh) // 2
        box = (0, y0, sw, y0 + nh)
    return pic.crop(box).resize((tw, th), Image.LANCZOS)


def centered(pen, y, text, font, fill, cx=512):
    pen.text((cx, y), text, font=font, fill=fill, anchor="ma")


def status_colour(status):
    return COL_TEAL if status == "REPORTED" else COL_OCHRE


# --- coarse land outlines, drawn from a plain world map ---
LANDMASSES = [
    [(-168, 66), (-150, 70), (-130, 71), (-115, 72), (-100, 73), (-90, 74),
     (-80, 73), (-75, 70), (-65, 62), (-55, 52), (-60, 46), (-70, 42),
     (-76, 35), (-81, 30), (-84, 28), (-90, 21), (-97, 16), (-104, 19),
     (-112, 26), (-122, 38), (-124, 48), (-140, 60), (-158, 58), (-168, 62)],
    [(-79, 9), (-76, 3), (-72, -4), (-64, -10), (-52, -4), (-41, -6),
     (-35, -9), (-39, -17), (-42, -24), (-49, -29), (-58, -35), (-65, -41),
     (-70, -50), (-74, -52), (-71, -30), (-70, -18), (-77, -12), (-81, -4), (-80, 4)],
    [(-10, 36), (-9, 43), (-2, 48), (2, 51), (8, 55), (10, 58),
     (18, 56), (21, 60), (25, 64), (30, 70), (35, 68), (40, 60),
     (32, 55), (28, 50), (28, 45), (24, 40), (20, 38), (14, 38),
     (8, 39), (0, 36), (-6, 36)],
    [(-17, 15), (-15, 22), (-10, 30), (-5, 35), (0, 36), (10, 37),
     (20, 32), (30, 31), (35, 28), (40, 20), (44, 12), (50, 10),
     (48, 0), (42, -8), (40, -18), (36, -26), (32, -32), (26, -34),
     (19, -35), (15, -27), (12, -18), (11, -6), (8, 4), (0, 5),
     (-8, 5), (-14, 8), (-17, 12)],
    [(40, 70), (55, 72), (70, 73), (90, 75), (110, 76), (130, 72),
     (150, 70), (170, 66), (178, 65), (170, 60), (162, 56), (156, 52),
     (142, 50), (135, 43), (128, 38), (122, 32), (120, 24), (110, 20),
     (105, 10), (100, 8), (95, 14), (90, 22), (86, 20), (80, 10),
     (76, 8), (72, 20), (66, 25), (60, 25), (54, 28), (50, 30),
     (45, 30), (40, 36), (36, 36)],
    [(113, -22), (114, -30), (115, -35), (120, -34), (126, -32), (132, -32),
     (136, -35), (140, -38), (146, -39), (150, -37), (153, -32), (150, -24),
     (146, -19), (142, -14), (140, -17), (136, -12), (132, -12), (130, -13),
     (126, -14), (122, -17), (118, -20)],
]


def paint_masthead(pen):
    centered(pen, 4, "THE WORLD TODAY", face("serif_b", 54), COL_INK)
    centered(pen, 64, "FRIDAY, 20 NOVEMBER 2026  ·  25 STORIES  ·  6 CONTINENTS",
             face("sans_b", 19), COL_INK)
    pen.line([(8, 86), (1016, 86)], fill=COL_INK, width=2)
    pen.rectangle([0, 88, 1024, 106], fill=COL_RED)
    centered(pen, 90, "IRAN  ·  AKVAN  ·  KYIV  ·  COP31  ·  ANT DEBUT  —  THE DAY IN 25 STORIES",
             face("sans_b", 13), COL_WHITE)
    centered(pen, 107, "A M E R I C A S      E U R O P E      M I D D L E   E A S T      A F R I C A      A S I A      O C E A N I A",
             face("sans", 11), COL_GREY)


def paint_ticker(pen):
    for i, (val, txt) in enumerate(TICKER_ITEMS):
        x = 8 + (i % 3) * 336
        y = 122 + (i // 3) * 21
        pen.text((x, y), val, font=face("sans_b", 16), fill=COL_RED)
        vw = pen.textlength(val, font=face("sans_b", 16))
        pen.text((x + vw + 6, y + 2), txt, font=face("sans", 12), fill=COL_INK)
    pen.line([(8, 166), (1016, 166)], fill=COL_LINE, width=1)


def paint_timeline(pen):
    for i, (t, place, ev) in enumerate(TIMELINE_ITEMS):
        x = 8 + i * 168
        pen.text((x, 170), t, font=face("sans_b", 12), fill=COL_RED)
        tw = pen.textlength(t, font=face("sans_b", 12))
        pen.text((x + tw + 5, 171), place, font=face("sans_b", 10), fill=COL_GREY)
        for j, ln in enumerate(fit_text(pen, ev, face("sans", 11), 160, 2)):
            pen.text((x, 184 + j * 12), ln, font=face("sans", 11), fill=COL_INK)
    pen.line([(8, 194), (1016, 194)], fill=COL_INK, width=1)


def paint_heroes(page, pen):
    heroes = [s for s in STORIES if s["kind"] == "hero"]
    for k, s in enumerate(heroes):
        x = 8 + k * 340
        w = 328
        art = Image.open(ART_DIR / ART[s["art"]])
        page.paste(crop_fill(art, w, 150), (x, 196))
        pen.rectangle([x, 196, x + w, 346], outline=COL_INK, width=1)
        pen.text((x, 350), s["section"], font=face("sans_b", 11), fill=COL_NAVY)
        pen.text((x + w, 350), s["status"], font=face("sans_b", 11),
                 fill=status_colour(s["status"]), anchor="ra")
        for j, ln in enumerate(fit_text(pen, s["head"], face("serif_b", 20), w, 2)):
            pen.text((x, 366 + j * 23), ln, font=face("serif_b", 20), fill=COL_INK)
        for j, ln in enumerate(fit_text(pen, s["deck"], face("sans", 12), w, 3)):
            pen.text((x, 412 + j * 14), ln, font=face("sans", 12), fill=COL_BODY)


def paint_grid(page, pen):
    pen.text((8, 462), "FEATURED — TEN MORE FROM THE DAY", font=face("sans_b", 13), fill=COL_INK)
    pen.line([(8, 480), (1016, 480)], fill=COL_RED, width=2)
    strip = Image.open(ART_DIR / STRIP_FILE)
    grid = [s for s in STORIES if s["kind"] == "grid"]
    for k, s in enumerate(grid):
        col, row = k % 5, k // 5
        x = 8 + col * 206
        y = 484 + row * 158
        top, bottom = BAND_EDGES[s["band"]], BAND_EDGES[s["band"] + 1]
        band = strip.crop((STRIP_LEFT, top, STRIP_RIGHT, bottom))
        page.paste(crop_fill(band, 192, 84), (x, y))
        pen.rectangle([x, y, x + 192, y + 84], outline=COL_INK, width=1)
        pen.text((x, y + 88), s["place"], font=face("sans_b", 10), fill=COL_GREY)
        pen.text((x + 192, y + 88), s["status"], font=face("sans_b", 10),
                 fill=status_colour(s["status"]), anchor="ra")
        for j, ln in enumerate(fit_text(pen, s["head"], face("serif_b", 15), 192, 2)):
            pen.text((x, y + 100 + j * 16), ln, font=face("serif_b", 15), fill=COL_INK)
        for j, ln in enumerate(fit_text(pen, s["deck"], face("sans", 11), 192, 2)):
            pen.text((x, y + 132 + j * 11), ln, font=face("sans", 11), fill=COL_BODY)
    pen.line([(8, 804), (1016, 804)], fill=COL_INK, width=1)


def paint_bottom(pen):
    pen.rectangle([8, 810, 508, 952], outline=COL_LINE, width=1)
    pen.text((16, 814), "WHERE IT HAPPENED — 13 STORIES, ONE MAP",
             font=face("sans_b", 11), fill=COL_INK)
    mx0, my0, mw, mh = 14, 830, 488, 118
    for lon in range(-180, 181, 60):
        gx = mx0 + (lon + 180) / 360 * mw
        pen.line([(gx, my0), (gx, my0 + mh)], fill=COL_GRID, width=1)
    for lat in (-60, -30, 0, 30, 60):
        gy = my0 + (90 - lat) / 180 * mh
        pen.line([(mx0, gy), (mx0 + mw, gy)], fill=COL_GRID, width=1)

    def project(lon, lat):
        return (mx0 + (lon + 180) / 360 * mw, my0 + (90 - lat) / 180 * mh)

    for poly in LANDMASSES:
        pen.polygon([project(lon, lat) for lon, lat in poly],
                    fill=COL_LAND, outline=COL_LINE)
    for n, lon, lat, ox, oy in MAP_MARKS:
        px, py = project(lon, lat)
        px, py = px + ox, py + oy
        pen.ellipse([px - 7, py - 7, px + 7, py + 7], fill=COL_RED,
                    outline=COL_WHITE, width=1)
        pen.text((px, py - 5), str(n), font=face("sans_b", 9),
                 fill=COL_WHITE, anchor="ma")
    pen.rectangle([516, 810, 1016, 952], outline=COL_LINE, width=1)
    pen.text((524, 814), "ALSO TODAY — 12 MORE", font=face("sans_b", 11), fill=COL_INK)
    for j, line in enumerate(ALSO_LINES):
        pen.text((524, 830 + j * 10), line, font=face("sans", 10), fill=COL_INK)


def paint_datecheck(pen):
    pen.rectangle([8, 956, 1016, 1004], outline=COL_RED, width=1)
    for j, (line, bold) in enumerate(DATE_LINES):
        kind = "sans_b" if bold else "sans"
        pen.text((16, 958 + j * 12), line, font=face(kind, 11), fill=COL_INK)


def paint_footer(pen):
    centered(pen, 1009,
             "Sources: Reuters, AP, AFP, IMD, CNBC, NY Post, Axios, WSJ, Telegraph  ·  Generated illustrations; original layout",
             face("sans", 10), COL_GREY)


def build_page():
    page = Image.new("RGB", (PAGE_W, PAGE_H), COL_PAPER)
    pen = ImageDraw.Draw(page)
    paint_masthead(pen)
    paint_ticker(pen)
    paint_timeline(pen)
    paint_heroes(page, pen)
    paint_grid(page, pen)
    paint_bottom(pen)
    paint_datecheck(pen)
    paint_footer(pen)
    target = ROOT / "entry.png"
    page.save(target, optimize=True)
    nbytes = target.stat().st_size
    print(f"entry.png: {page.size[0]}x{page.size[1]} {nbytes} bytes ({nbytes / 1024:.1f} KiB)")
    assert page.size == (PAGE_W, PAGE_H)
    assert nbytes <= 1024 * 1024, "entry.png over the 1 MiB gate"
    return target


if __name__ == "__main__":  # draw it
    build_page()
