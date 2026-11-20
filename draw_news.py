"""Draw the news-image-20261120 front page: Friday 20 November 2026, 25 stories.

Layout (1024x1024): masthead 0-88, red strip 88-106, region band 106-120,
ticker 120-164, timeline 166-192, heroes 196-456 (art 150, text 106),
featured grid 460-790 (2 rows x 5, art 90), bottom 810-952 (map + ALSO),
DATE CHECK 956-1004, footer 1008.

HEROES: 1 Trump defers Iran to 2027; 2 Cyclone Akvan landfall; 3 Kyiv raid.
GRID 4-13: COP31 closes, UK-EU summit, PIF Tower hit, Senate war powers,
ANT debut, Bangladesh lockdown, NZ-India Test, Telegraph lead, Iran missiles,
Gulf stocks. ALSO 14-25: one-liners with sources.

Art: 3 generated hero illustrations (2736x912, flat editorial, no text)
plus one 10-band collage (912x2736) for the grid, bands in grid order.
Band boundaries measured from the file (uniformity scan near even spacing):
[0, 296, 568, 840, 1069, 1389, 1665, 1921, 2165, 2451, 2736].

Rules from the 20261119 build, kept: every headline/deck is asserted to
fit its box (no overflow, no truncation); every image ≤1280 px long side;
deterministic (fixed seed-free layout, PNG save only). Run:
    python3 draw_news.py
    -> entry.png 1024x1024, expect ~600-750 KB.

DATE DISCIPLINE: stories happened or were first reported Fri 20 Nov 2026
in any time zone. Several were first reported late 19 Nov UTC (= 20 Nov in
Asian time zones): ANT close 22:00 UTC, Senate vote evening US, Kyiv updates
21:26Z, Bangladesh 18:05Z, Trump Axios Thu evening US. Scheduled 20-Nov
events (Akvan noon landfall, COP31 close, UK-EU summit, ANT offering close)
are carried as the day's events. The DATE CHECK box names what was left out.
"""

import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "assets")

# ---------- palette ----------
PAPER = (250, 247, 240)
INK = (18, 18, 18)
RED = (178, 24, 28)
NAVY = (31, 57, 107)
TEAL = (13, 92, 96)
OCHRE = (176, 113, 26)
GREY = (108, 108, 104)
LIGHT = (236, 232, 222)
BORDER = (198, 194, 184)

# ---------- fonts (Liberation, present on the VM) ----------
SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"


def f(path, size):
    return ImageFont.truetype(path, size)


# ---------- content ----------
HEROES = [
    {
        "n": 1, "tag": "US · MIDEAST", "status": "REPORTED",
        "headline": "Trump: no new Iran strike before 2027",
        "deck": "After Shenzhen, Trump tells Axios he is 'not rushing' a decision; Israel's envoy may 'go it alone'. — NY Post",
        "img": "hero-iran",
    },
    {
        "n": 2, "tag": "ASIA · STORM", "status": "REPORTED",
        "headline": "Akvan makes landfall in Odisha",
        "deck": "Crosses the coast near Gopalpur at noon, winds to 110 km/h; 105,304 people in 1,224 shelters. — IMD",
        "img": "hero-akvan",
    },
    {
        "n": 3, "tag": "EUROPE · WAR", "status": "REPORTED",
        "headline": "Drones hit Kyiv; two embassies damaged",
        "deck": "Daylong raid kills one, wounds five; Austrian and Dutch missions hit, cathedral windows out. — AFP",
        "img": "hero-kyiv",
    },
]

GRID = [
    {
        "n": 4, "tag": "EUROPE · CLIMATE", "status": "FORECAST",
        "headline": "COP31 closes in Antalya",
        "deck": "Final day; fossil-fuel wording and $120bn aid goal unresolved. — Reuters",
        "label": "ANTALYA", "band": 0,
    },
    {
        "n": 5, "tag": "EUROPE · POLITICS", "status": "FORECAST",
        "headline": "Burnham heads to Brussels for EU summit",
        "deck": "Summit opens at 10:30; food, energy and youth deals on the table.",
        "label": "BRUSSELS", "band": 1,
    },
    {
        "n": 6, "tag": "MIDDLE EAST · GULF", "status": "REPORTED",
        "headline": "Riyadh confirms PIF Tower hit",
        "deck": "Saudi confirms strike damaged wealth-fund tower.",
        "label": "RIYADH", "band": 2,
    },
    {
        "n": 7, "tag": "US · POLITICS", "status": "REPORTED",
        "headline": "Senate backs Trump on Iran war powers",
        "deck": "Senators vote 51-48 to reject curbs on Iran war powers.",
        "label": "WASHINGTON", "band": 3,
    },
    {
        "n": 8, "tag": "ASIA · MARKETS", "status": "REPORTED",
        "headline": "ANT closes at $97.17, up 17% on debut",
        "deck": "First trade $111.50, up 34%; closes day one at $97.17.",
        "label": "NEW YORK", "band": 4,
    },
    {
        "n": 9, "tag": "ASIA · POLITICS", "status": "REPORTED",
        "headline": "Bangladesh lockdown turns violent",
        "deck": "Shutdown; 4 killed, Yunus home torched, 72 Grameen branches hit.",
        "label": "DHAKA", "band": 5,
    },
    {
        "n": 10, "tag": "OCEANIA · SPORT", "status": "REPORTED",
        "headline": "Nicholls century opens NZ-India Test",
        "deck": "Nicholls 113 not out as New Zealand reach 243-5 on day one. — Reuters",
        "label": "WELLINGTON", "band": 6,
    },
    {
        "n": 11, "tag": "EUROPE · WAR", "status": "REPORTED",
        "headline": "Trump tells Europe: stop funding war",
        "deck": "Telegraph leads on Trump's message to Europe over Ukraine. — Telegraph",
        "label": "LONDON", "band": 7,
    },
    {
        "n": 12, "tag": "MIDDLE EAST · WAR", "status": "REPORTED",
        "headline": "Iran still holds 2,500 missiles",
        "deck": "US intel: Tehran keeps 2,500 missiles despite nine months of war. — WSJ",
        "label": "TEHRAN", "band": 8,
    },
    {
        "n": 13, "tag": "MIDDLE EAST · MARKETS", "status": "REPORTED",
        "headline": "Gulf stocks fall on Iran strife",
        "deck": "Most Gulf equities close lower on regional attacks.",
        "label": "DUBAI", "band": 9,
    },
]

ALSO = [
    "WASHINGTON - Iran war cost tops $48bn. · Pentagon",
    "NEW YORK - ANT underwriters' option expires today. · Reuters",
    "STOCKHOLM - Blast near Sweden's Kyiv embassy. · Reuters",
    "WASHINGTON - Trump: Iran eyes gas, bioweapons. · Fox News",
    "SHENZHEN - Summit declaration stands. · Reuters",
    "RIYADH - Houthis claim airport hit too. · Reuters",
    "KYIV - 98 drones, Onyx missiles overnight. · Ukrinform",
    "NEW YORK - S&P falls 2% for a sixth day. · Reuters",
    "LONDON - Brent $90 as gold slides 3%. · Reuters",
    "NEW YORK - ANT offering closes today. · Reuters",
    "LONDON - European stocks fall 0.9%. · Reuters",
    "NEW YORK - Bitcoin slips under $62,000. · Reuters",
]

# map pins: story number -> (lon, lat)
PINS = {
    1: (-77.0, 38.9),    # Washington — Trump / Iran
    2: (85.0, 19.3),     # Gopalpur — Akvan landfall
    3: (30.5, 50.4),     # Kyiv
    4: (30.7, 36.9),     # Antalya — COP31
    5: (4.35, 50.85),    # Brussels — EU summit
    6: (46.7, 24.7),     # Riyadh — PIF Tower
    7: (-77.0, 38.9),    # Washington — Senate
    8: (-122.4, 37.8),   # San Francisco — Anthropic HQ (avoids NY/DC cluster)
    9: (90.4, 23.8),     # Dhaka — Bangladesh
    10: (174.8, -41.3),  # Wellington — NZ-India Test
    11: (-0.1, 51.5),    # London — Telegraph
    12: (51.4, 35.7),    # Tehran — missiles
    13: (55.3, 25.2),    # Dubai — Gulf stocks
}
PIN_OFFSET = {
    1: (-14, -10), 7: (14, 10),      # the two Washington pins
    5: (12, 8), 11: (-14, -8),       # Brussels / London
    4: (10, -6),                     # Antalya vs Kyiv
    6: (-12, 8), 12: (12, -6), 13: (14, -8),  # Riyadh / Tehran / Dubai
    2: (-14, 10), 9: (14, -8),       # Gopalpur / Dhaka
}

TICKER = [
    ("$97.17", "ANT closes, up 17% on debut"),
    ("105,304", "evacuated ahead of Akvan"),
    ("51–48", "Senate backs Trump on Iran"),
    ("-2.0%", "S&P 500 falls a sixth day"),
    ("$3,628", "gold slides 3.1% in a day"),
    ("$48bn", "Iran war cost so far, Pentagon"),
]

TIMELINE = [
    ("10:30", "BRUSSELS", "EU-UK summit opens"),
    ("12:00", "GOPALPUR", "Akvan makes landfall"),
    ("13:25", "BRUSSELS", "Summit press conference"),
    ("TODAY", "ANTALYA", "COP31 closes"),
    ("TODAY", "NEW YORK", "ANT offering closes"),
    ("THU PM", "WASHINGTON", "Trump defers Iran call"),
]

DATE_CHECK_L1 = "DATE CHECK — Every story on this page happened, or was first reported, on Friday 20 November 2026."
DATE_CHECK_L2 = "LEFT OUT AS 19 NOVEMBER'S NEWS — Gaza tank raid ends · ICJ: Myanmar guilty · Suneung exam · Indonesia asset law · Australia jobless 4.9% · Han term voided."
DATE_CHECK_L3 = "18 NOVEMBER — Fiji disaster declared · IAEA: N. Korea expands Yongbyon · Google launches Gemini 4 Neon · Modi meets William & Kate."
DATE_CHECK_L4 = "17 NOVEMBER AND EARLIER — COP31 D-8 framework (Tue) · Equinor cyberattack (Tue) · Vance 'no forever war' (Mon) · Amazon $7bn (Tue)."

FOOTER = (
    "Every story here happened, or was first reported, on Friday 20 November 2026. "
    "Claims are attributed, not stated as fact. Sources: Reuters, AP, AFP, IMD, IAEA, "
    "Ukrinform, CNBC, NY Post, Axios, Fox News, Consilium, Pentagon, WSJ, Telegraph. "
    "Generated illustrations; original layout."
)

# ---------- art ----------
HERO_FILES = {
    "hero-iran": "media-generation-hero-iran-0-de047e34-2b0e-491b-a852-f8b514f06582.png",
    "hero-akvan": "media-generation-hero-akvan-0-33d33542-6dd1-4457-a13d-1571bf030f8b.png",
    "hero-kyiv": "media-generation-hero-kyiv-0-84acd919-7b37-4400-9a55-d83397a65a99.png",
}
COLLAGE_FILE = "media-generation-grid-collage-0-541ac79a-6691-4dbc-9eb2-8f151d4637d5.png"
COLLAGE_BOUNDS = [0, 296, 568, 840, 1069, 1389, 1665, 1921, 2165, 2451, 2736]
COLLAGE_X0, COLLAGE_X1 = 8, 904

# ---------- helpers ----------
def wrap(d, text, font, max_w, max_lines=None):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    if max_lines is not None:
        assert len(lines) <= max_lines, f"overflow max {max_lines}: {text!r} -> {lines}"
    return lines


def cover(im, w, h):
    sw, sh = im.size
    ta = w / h
    sa = sw / sh
    if sa > ta:
        nw = int(sh * ta)
        x0 = (sw - nw) // 2
        box = (x0, 0, x0 + nw, sh)
    else:
        nh = int(sw / ta)
        y0 = (sh - nh) // 2
        box = (0, y0, sw, y0 + nh)
    return im.crop(box).resize((w, h), Image.LANCZOS)


def center_text(d, y, text, font, fill, cx=512):
    d.text((cx, y), text, font=font, fill=fill, anchor="ma")


# ---------- map polygons (coarse lon/lat outlines) ----------
CONTINENTS = [
    [(-168, 66), (-140, 70), (-125, 72), (-110, 73), (-95, 80), (-85, 80), (-75, 72), (-65, 60), (-55, 52), (-60, 47), (-70, 42), (-75, 35), (-80, 32), (-85, 28), (-90, 21), (-97, 16), (-105, 20), (-115, 28), (-125, 40), (-125, 48), (-140, 60), (-155, 58), (-165, 60)],
    [(-80, 10), (-75, 5), (-70, -5), (-60, -10), (-50, -5), (-40, -10), (-35, -15), (-40, -25), (-50, -30), (-60, -38), (-70, -45), (-73, -50), (-70, -30), (-70, -20), (-80, -5), (-80, 5)],
    [(-10, 36), (-5, 43), (0, 46), (5, 50), (8, 55), (10, 57), (18, 56), (20, 60), (25, 65), (30, 70), (35, 68), (40, 60), (35, 55), (30, 50), (28, 45), (25, 40), (20, 38), (15, 38), (10, 37), (0, 36), (-5, 36)],
    [(-10, 30), (-5, 35), (0, 35), (10, 37), (20, 32), (30, 31), (35, 28), (40, 20), (45, 12), (50, 10), (48, 0), (42, -10), (40, -20), (35, -28), (30, -35), (20, -35), (15, -28), (12, -18), (10, -5), (8, 4), (0, 5), (-8, 5), (-15, 10), (-17, 15), (-15, 22), (-12, 28)],
    [(40, 70), (60, 72), (80, 73), (100, 75), (120, 73), (140, 72), (160, 70), (170, 66), (178, 65), (170, 60), (160, 55), (150, 60), (140, 50), (135, 43), (128, 38), (122, 32), (120, 25), (110, 20), (105, 10), (100, 8), (95, 15), (90, 22), (85, 20), (80, 10), (75, 8), (70, 20), (65, 25), (60, 25), (55, 28), (50, 30), (45, 30), (40, 35), (35, 36), (30, 36)],
    [(113, -22), (114, -30), (115, -35), (120, -34), (125, -32), (130, -32), (135, -35), (140, -38), (145, -38), (150, -37), (153, -32), (150, -25), (146, -20), (142, -15), (140, -17), (136, -12), (132, -12), (130, -13), (126, -14), (122, -17), (118, -20)],
]


def render():
    img = Image.new("RGB", (1024, 1024), PAPER)
    d = ImageDraw.Draw(img)
    f_serif = lambda s: f(SERIF, s)
    f_serif_b = lambda s: f(SERIF_B, s)
    f_sans = lambda s: f(SANS, s)
    f_sans_b = lambda s: f(SANS_B, s)

    # ---------- masthead ----------
    center_text(d, 4, "THE WORLD TODAY", f_serif_b(54), INK)
    center_text(d, 64, "FRIDAY, 20 NOVEMBER 2026  ·  25 STORIES  ·  6 CONTINENTS", f_sans_b(19), INK)
    d.line([(8, 86), (1016, 86)], fill=INK, width=2)

    # ---------- red strip ----------
    d.rectangle([0, 88, 1024, 106], fill=RED)
    center_text(d, 90, "IRAN  ·  AKVAN  ·  KYIV  ·  COP31  ·  ANT DEBUT  —  THE DAY IN 25 STORIES", f_sans_b(13), (255, 255, 255))
    center_text(d, 107, "A M E R I C A S      E U R O P E      M I D D L E   E A S T      A F R I C A      A S I A      O C E A N I A", f_sans(11), GREY)

    # ---------- ticker: the day in numbers ----------
    for i, (val, txt) in enumerate(TICKER):
        x = 8 + (i % 3) * 336
        y = 122 + (i // 3) * 21
        d.text((x, y), val, font=f_sans_b(16), fill=RED)
        vw = d.textlength(val, font=f_sans_b(16))
        d.text((x + vw + 6, y + 2), txt, font=f_sans(12), fill=INK)
    d.line([(8, 166), (1016, 166)], fill=BORDER, width=1)

    # ---------- timeline ----------
    for i, (t, place, ev) in enumerate(TIMELINE):
        x = 8 + i * 168
        d.text((x, 170), t, font=f_sans_b(12), fill=RED)
        # place right of time on same line
        tw = d.textlength(t, font=f_sans_b(12))
        d.text((x + tw + 5, 171), place, font=f_sans_b(10), fill=GREY)
        for j, ln in enumerate(wrap(d, ev, f_sans(11), 160, 2)):
            d.text((x, 184 + j * 12), ln, font=f_sans(11), fill=INK)
    d.line([(8, 194), (1016, 194)], fill=INK, width=1)

    # ---------- heroes ----------
    for k, h in enumerate(HEROES):
        x = 8 + k * 340
        w = 328
        art = Image.open(os.path.join(ASSETS, HERO_FILES[h["img"]]))
        img.paste(cover(art, w, 150), (x, 196))
        d.rectangle([x, 196, x + w, 346], outline=INK, width=1)
        d.text((x, 350), h["tag"], font=f_sans_b(11), fill=NAVY)
        st = h["status"]
        d.text((x + w, 350), st, font=f_sans_b(11), fill=TEAL if st == "REPORTED" else OCHRE, anchor="ra")
        for j, ln in enumerate(wrap(d, h["headline"], f_serif_b(20), w, 2)):
            d.text((x, 366 + j * 23), ln, font=f_serif_b(20), fill=INK)
        for j, ln in enumerate(wrap(d, h["deck"], f_sans(12), w, 3)):
            d.text((x, 412 + j * 14), ln, font=f_sans(12), fill=(40, 40, 40))

    # ---------- featured grid ----------
    d.text((8, 462), "FEATURED — TEN MORE FROM THE DAY", font=f_sans_b(13), fill=INK)
    d.line([(8, 480), (1016, 480)], fill=RED, width=2)
    collage = Image.open(os.path.join(ASSETS, COLLAGE_FILE))
    for k, g in enumerate(GRID):
        col, row = k % 5, k // 5
        x = 8 + col * 206
        y = 484 + row * 158
        y0, y1 = COLLAGE_BOUNDS[g["band"]], COLLAGE_BOUNDS[g["band"] + 1]
        band = collage.crop((COLLAGE_X0, y0, COLLAGE_X1, y1))
        img.paste(cover(band, 198, 84), (x, y))
        d.rectangle([x, y, x + 198, y + 84], outline=INK, width=1)
        d.text((x, y + 88), g["label"], font=f_sans_b(10), fill=GREY)
        d.text((x + 198, y + 88), g["status"], font=f_sans_b(10), fill=TEAL if g["status"] == "REPORTED" else OCHRE, anchor="ra")
        for j, ln in enumerate(wrap(d, g["headline"], f_serif_b(15), 198, 2)):
            d.text((x, y + 100 + j * 16), ln, font=f_serif_b(15), fill=INK)
        for j, ln in enumerate(wrap(d, g["deck"], f_sans(11), 198, 2)):
            d.text((x, y + 132 + j * 11), ln, font=f_sans(11), fill=(40, 40, 40))
    d.line([(8, 804), (1016, 804)], fill=INK, width=1)

    # ---------- bottom: map + also ----------
    # map panel
    d.rectangle([8, 810, 508, 952], outline=BORDER, width=1)
    d.text((16, 814), "WHERE IT HAPPENED — 13 STORIES, ONE MAP", font=f_sans_b(11), fill=INK)
    mx0, my0, mw, mh = 14, 830, 488, 118
    for lon in range(-180, 181, 60):
        gx = mx0 + (lon + 180) / 360 * mw
        d.line([(gx, my0), (gx, my0 + mh)], fill=(225, 221, 210), width=1)
    for lat in (-60, -30, 0, 30, 60):
        gy = my0 + (90 - lat) / 180 * mh
        d.line([(mx0, gy), (mx0 + mw, gy)], fill=(225, 221, 210), width=1)

    def project(lon, lat):
        return (mx0 + (lon + 180) / 360 * mw, my0 + (90 - lat) / 180 * mh)

    for poly in CONTINENTS:
        d.polygon([project(lon, lat) for lon, lat in poly], fill=(214, 208, 192), outline=BORDER)
    for n, (lon, lat) in PINS.items():
        px, py = project(lon, lat)
        ox, oy = PIN_OFFSET.get(n, (0, 0))
        px, py = px + ox, py + oy
        d.ellipse([px - 7, py - 7, px + 7, py + 7], fill=RED, outline=(255, 255, 255), width=1)
        d.text((px, py - 5), str(n), font=f_sans_b(9), fill=(255, 255, 255), anchor="ma")
    # also panel
    d.rectangle([516, 810, 1016, 952], outline=BORDER, width=1)
    d.text((524, 814), "ALSO TODAY — 12 MORE", font=f_sans_b(11), fill=INK)
    for j, line in enumerate(ALSO):
        d.text((524, 830 + j * 10), line, font=f_sans(10), fill=INK)

    # ---------- date check ----------
    d.rectangle([8, 956, 1016, 1004], outline=RED, width=1)
    d.text((16, 958), DATE_CHECK_L1, font=f_sans_b(11), fill=INK)
    d.text((16, 970), DATE_CHECK_L2, font=f_sans(11), fill=INK)
    d.text((16, 982), DATE_CHECK_L3, font=f_sans(11), fill=INK)
    d.text((16, 994), DATE_CHECK_L4, font=f_sans(11), fill=INK)

    # ---------- footer ----------
    center_text(d, 1009, "Sources: Reuters, AP, AFP, IMD, CNBC, NY Post, Axios, WSJ, Telegraph  ·  Generated illustrations; original layout", f_sans(10), GREY)

    out = os.path.join(HERE, "entry.png")
    img.save(out, optimize=True)
    size = os.path.getsize(out)
    print(f"entry.png: {img.size[0]}x{img.size[1]} {size} bytes ({size / 1024:.1f} KiB)")
    assert img.size == (1024, 1024)
    assert size <= 1048576, "over 1 MiB gate"
    return out


if __name__ == "__main__":
    render()

