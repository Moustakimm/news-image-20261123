#!/usr/bin/env python3
"""Draw 'The World Today - 23 November 2026' - a dense one-page newspaper
summing up Monday 23 November 2026. Deterministic: same bytes every run.
Built from a story slate verified against Reuters/AP/Al Jazeera/CNN/BBC/
Yonhap/AFP/WSJ/Morningstar on 23-24 November 2026. Output: entry.png 1024x1024.
"""
import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
FD = "/usr/share/fonts/truetype"
SERIF = FD + "/liberation/LiberationSerif-Bold.ttf"
SERIF_R = FD + "/liberation/LiberationSerif-Regular.ttf"
SANS = FD + "/liberation/LiberationSans-Regular.ttf"
SANS_B = FD + "/liberation/LiberationSans-Bold.ttf"

# palette
INK = (18, 22, 34)
PAPER = (250, 246, 236)
NAVY = (14, 30, 62)
NAVY2 = (22, 46, 92)
RED = (196, 30, 30)
RED_D = (150, 20, 20)
GOLD = (212, 158, 32)
TEAL = (0, 118, 118)
SKY = (140, 192, 222)
SEA = (28, 88, 138)
SEA_D = (16, 58, 96)
SAND = (233, 211, 160)
GREY = (120, 124, 132)
LGREY = (226, 228, 232)
WHITE = (255, 255, 255)
CREAM = (255, 250, 230)
ORANGE = (238, 120, 20)
YELLOW = (250, 200, 40)

def F(size, bold=False, serif=False):
    if serif:
        return ImageFont.truetype(SERIF if bold else SERIF_R, size)
    return ImageFont.truetype(SANS_B if bold else SANS, size)

def wrap(text, font, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if font.getlength(t) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def text(d, xy, s, font, fill=INK, anchor="la"):
    d.text(xy, s, font=font, fill=fill, anchor=anchor)

def para(d, x, y, max_w, lines, font, fill=INK, leading=None):
    """Draw wrapped lines, return y after last line."""
    lh = leading or int(font.size * 1.22)
    for ln in lines:
        d.text((x, y), ln, font=font, fill=fill)
        y += lh
    return y

def trunc(s, font, max_w):
    if font.getlength(s) <= max_w:
        return s
    while s and font.getlength(s + "...") > max_w:
        s = s[:-1]
    return s + "..."

def rrect(d, box, fill, outline=None, r=4, width=1):
    d.rounded_rectangle(box, radius=r, fill=fill, outline=outline, width=width)

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# ---------------------------------------------------------------- masthead
d.rectangle([0, 0, W, 102], fill=NAVY)
d.rectangle([0, 102, W, 106], fill=RED)
text(d, (16, 10), "THE WORLD TODAY", F(19, bold=True), fill=GOLD)
text(d, (16, 30), "23 NOVEMBER 2026", F(56, bold=True, serif=True), fill=WHITE)
text(d, (1016, 14), "MONDAY", F(22, bold=True), fill=WHITE, anchor="ra")
text(d, (1016, 42), "ONE DAY  •  ONE PAGE", F(14, bold=True), fill=(200, 210, 230), anchor="ra")
text(d, (1016, 62), "ALL THE NEWS THAT FITS", F(14, bold=True), fill=(200, 210, 230), anchor="ra")
d.line([16, 96, 420, 96], fill=GOLD, width=2)

# ---------------------------------------------------------------- helpers for scenes
def sea(d, x, y, w, h, base=SEA):
    d.rectangle([x, y, x + w, y + h], fill=base)
    for i in range(5):
        yy = y + 8 + i * (h // 5)
        d.line([x + 6, yy, x + w - 6, yy], fill=(90, 160, 200), width=2)

def flames(d, cx, y, s=1.0):
    for (dx, w, h, col) in [(-16, 18, 34, ORANGE), (0, 22, 44, YELLOW),
                            (16, 16, 30, ORANGE), (6, 12, 24, (255, 230, 120))]:
        d.polygon([(cx + dx * s - w * s / 2, y), (cx + dx * s, y - h * s),
                   (cx + dx * s + w * s / 2, y)], fill=col)

def smoke(d, cx, y, n=3, r=9):
    for i in range(n):
        d.ellipse([cx - r + i * 10 - 12, y - i * 12 - r, cx + r + i * 10 - 12,
                   y - i * 12 + r], fill=(200, 200, 200))
        d.ellipse([cx - r + i * 10 - 4, y - i * 12 - r, cx + r + i * 10 - 4,
                   y - i * 12 + r], fill=(170, 170, 170))

def ship(d, x, y, w, h, hull=(40, 44, 54), deck=RED):
    d.polygon([(x, y), (x + w, y), (x + w - 12, y + h), (x + 12, y + h)], fill=hull)
    d.rectangle([x + 8, y - 14, x + w - 8, y], fill=deck)
    d.rectangle([x + w * 0.30, y - 30, x + w * 0.52, y - 14], fill=WHITE)
    d.rectangle([x + w * 0.58, y - 26, x + w * 0.72, y - 14], fill=(70, 76, 88))
    d.line([x + w * 0.62, y - 44, x + w * 0.62, y - 26], fill=INK, width=3)

# ---------------------------------------------------------------- lead 1: COP31 hall
def lead1(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(30, 52, 84))
    d.rectangle([x, y + h - 26, x + w, y + h], fill=(18, 34, 60))
    # rows of desks with flags
    for row in range(3):
        yy = y + 18 + row * 26
        for i in range(9):
            xx = x + 12 + i * 34
            d.rectangle([xx, yy, xx + 26, yy + 12], fill=(70, 92, 130))
            d.rectangle([xx + 10, yy - 10, xx + 12, yy], fill=(200, 200, 200))
            col = [(196, 30, 30), (255, 255, 255), (0, 118, 118), GOLD,
                   (60, 90, 160)][(i + row) % 5]
            d.rectangle([xx + 12, yy - 10, xx + 22, yy - 2], fill=col)
    # gavel block + cracked globe
    d.ellipse([x + w - 78, y + 8, x + w - 18, y + 68], fill=TEAL)
    d.arc([x + w - 70, y + 16, x + w - 26, y + 60], 20, 200, fill=WHITE, width=3)
    d.arc([x + w - 66, y + 22, x + w - 30, y + 54], 200, 340, fill=WHITE, width=2)
    # NO DEAL stamp
    st = Image.new("RGBA", (190, 56), (0, 0, 0, 0))
    sd = ImageDraw.Draw(st)
    sd.rectangle([2, 2, 188, 54], outline=RED, width=5)
    sd.text((95, 28), "NO DEAL", font=F(30, bold=True), fill=RED, anchor="mm")
    st = st.rotate(10, expand=True, resample=Image.BICUBIC)
    img.paste(st, (x + w // 2 - 105, y + h - 78), st)

# ---------------------------------------------------------------- lead 2: Hormuz tanker
def lead2(x, y, w, h):
    d.rectangle([x, y, x + w, y + 52], fill=(250, 190, 110))
    d.ellipse([x + w - 70, y + 6, x + w - 18, y + 58], fill=(255, 220, 120))
    sea(d, x, y + 52, w, h - 52)
    ship(d, x + 40, y + 92, 210, 26)
    flames(d, x + 120, y + 78, 1.1)
    flames(d, x + 210, y + 78, 0.8)
    smoke(d, x + 150, y + 62, 4, 10)
    # mine in the water
    mx, my = x + w - 52, y + h - 22
    d.ellipse([mx - 10, my - 10, mx + 10, my + 10], fill=INK)
    for a in range(0, 360, 45):
        r = math.radians(a)
        d.line([mx + 10 * math.cos(r), my + 10 * math.sin(r),
                mx + 17 * math.cos(r), my + 17 * math.sin(r)], fill=INK, width=3)
    d.line([x + 14, y + 118, x + 60, y + 118], fill=(200, 220, 235), width=2)
    d.line([x + 250, y + 122, x + 300, y + 122], fill=(200, 220, 235), width=2)

# ---------------------------------------------------------------- lead 3: Merkury sinking
def lead3(x, y, w, h):
    d.rectangle([x, y, x + w, y + 46], fill=(38, 44, 60))
    d.ellipse([x + 18, y + 8, x + 52, y + 42], fill=(220, 220, 210))
    sea(d, x, y + 46, w, h - 46, base=SEA_D)
    # listing warship
    hull = [(x + 60, y + 96), (x + 250, y + 70), (x + 262, y + 88),
            (x + 120, y + 112), (x + 66, y + 112)]
    d.polygon(hull, fill=(90, 96, 108))
    d.rectangle([x + 150, y + 52, x + 210, y + 72], fill=(70, 76, 88))
    d.line([x + 180, y + 30, x + 180, y + 52], fill=(200, 200, 200), width=3)
    flames(d, x + 200, y + 66, 1.2)
    smoke(d, x + 210, y + 48, 3, 9)
    # sea drones approaching
    for (dx, dy) in [(40, 118), (90, 124), (290, 118)]:
        d.polygon([(x + dx, y + dy), (x + dx + 26, y + dy),
                   (x + dx + 20, y + dy + 7), (x + dx + 6, y + dy + 7)],
                  fill=(20, 22, 30))
        d.line([x + dx - 14, y + dy + 9, x + dx + 34, y + dy + 9],
               fill=(160, 200, 225), width=2)
    d.ellipse([x + 250, y + 100, x + 300, y + 116], fill=(120, 160, 190))

LEADS = [
    ("CLIMATE  •  ANTALYA, TURKEY", "COP31 COLLAPSES — NO DEAL",
     "After the longest COP on record, the EU and 130 nations reject a final text "
     "that never mentions fossil fuels. Disputes pass to COP32 in Ethiopia.", lead1),
    ("WAR AT SEA  •  STRAIT OF HORMUZ", "TANKERS HIT IN HORMUZ AS IRAN STRIKES BAHRAIN",
     "Tankers struck in the Strait as Iran fires on US bases in Bahrain and a "
     "civilian site burns. Tehran vows to use \u201call means\u201d against the blockade.", lead2),
    ("UKRAINE  •  BENGHAZI, LIBYA", "UKRAINE SINKS RUSSIAN WARSHIP IN LIBYA",
     "Seven sea drones sink the corvette Merkury in Benghazi harbour and hit the "
     "cargo ship Angara. A day earlier, a Russian freighter was hit in the Baltic.", lead3),
]

LX = [8, 348, 688]
LW = 328
for (kicker, head, deck, scene), x in zip(LEADS, LX):
    y = 112
    text(d, (x, y), kicker, F(11, bold=True), fill=RED)
    y += 18
    scene(x, y, LW, 132)
    d.rectangle([x, y, x + LW, y + 132], outline=INK, width=1)
    y += 140
    hl = wrap(head, F(19, bold=True), LW)
    y = para(d, x, y, LW, hl, F(19, bold=True), leading=21)
    y += 3
    dl = wrap(deck, F(12), LW)[:3]
    para(d, x, y, LW, dl, F(12), leading=15)

# ---------------------------------------------------------------- section bar
d.rectangle([8, 374, 668, 396], fill=RED)
text(d, (16, 379), "THE DAY IN BRIEF", F(13, bold=True), fill=WHITE)
d.rectangle([676, 374, 1016, 396], fill=NAVY)
text(d, (684, 379), "WHERE IT HAPPENED", F(13, bold=True), fill=WHITE)

# ---------------------------------------------------------------- medium icons (46x46 flat pictograms)
def icon_bg(d, x, y, col):
    rrect(d, [x, y, x + 46, y + 46], fill=col, r=6)

def ic_rubble(d, x, y):
    icon_bg(d, x, y, (70, 76, 88))
    d.polygon([(x + 6, y + 40), (x + 20, y + 22), (x + 34, y + 40)], fill=(150, 156, 168))
    d.rectangle([x + 22, y + 14, x + 40, y + 40], fill=(120, 126, 138))
    d.polygon([(x + 22, y + 14), (x + 31, y + 6), (x + 40, y + 14)], fill=(150, 156, 168))
    d.ellipse([x + 12, y + 8, x + 22, y + 18], fill=YELLOW)

def ic_chart(d, x, y):
    icon_bg(d, x, y, WHITE)
    d.rectangle([x, y, x + 46, y + 46], outline=RED, width=2)
    for i, h in enumerate([10, 18, 14, 26, 34]):
        d.rectangle([x + 6 + i * 8, y + 40 - h, x + 11 + i * 8, y + 40], fill=RED)
    d.line([x + 4, y + 8, x + 42, y + 34], fill=INK, width=3)
    d.polygon([(x + 42, y + 34), (x + 34, y + 30), (x + 38, y + 40)], fill=INK)

def ic_capitol(d, x, y):
    icon_bg(d, x, y, NAVY2)
    d.rectangle([x + 8, y + 30, x + 38, y + 40], fill=WHITE)
    d.rectangle([x + 12, y + 24, x + 34, y + 30], fill=WHITE)
    d.pieslice([x + 14, y + 10, x + 32, y + 28], 180, 360, fill=WHITE)
    d.rectangle([x + 21, y + 4, x + 25, y + 12], fill=WHITE)

def ic_cuffs(d, x, y):
    icon_bg(d, x, y, (40, 90, 60))
    d.ellipse([x + 6, y + 14, x + 20, y + 28], outline=WHITE, width=3)
    d.ellipse([x + 26, y + 14, x + 40, y + 28], outline=WHITE, width=3)
    d.line([x + 20, y + 21, x + 26, y + 21], fill=WHITE, width=3)
    d.polygon([(x + 23, y + 32), (x + 25, y + 37), (x + 30, y + 37),
               (x + 26, y + 40), (x + 28, y + 45), (x + 23, y + 42),
               (x + 18, y + 45), (x + 20, y + 40), (x + 16, y + 37),
               (x + 21, y + 37)], fill=GOLD)

def ic_plane(d, x, y):
    icon_bg(d, x, y, SKY)
    d.polygon([(x + 6, y + 26), (x + 34, y + 14), (x + 40, y + 16),
               (x + 16, y + 28), (x + 10, y + 32)], fill=WHITE)
    d.polygon([(x + 18, y + 20), (x + 26, y + 12), (x + 30, y + 14),
               (x + 24, y + 22)], fill=WHITE)
    d.line([x + 30, y + 30, x + 42, y + 42], fill=RED, width=4)
    d.line([x + 42, y + 30, x + 30, y + 42], fill=RED, width=4)

def ic_missile(d, x, y):
    icon_bg(d, x, y, (90, 40, 40))
    d.polygon([(x + 10, y + 34), (x + 30, y + 10), (x + 36, y + 14),
               (x + 18, y + 38)], fill=(200, 200, 200))
    d.polygon([(x + 10, y + 34), (x + 16, y + 28), (x + 12, y + 40)], fill=RED)
    d.arc([x + 26, y + 26, x + 42, y + 42], 270, 90, fill=YELLOW, width=2)
    d.arc([x + 20, y + 20, x + 42, y + 42], 270, 90, fill=YELLOW, width=2)

def ic_boat(d, x, y):
    icon_bg(d, x, y, SEA)
    d.polygon([(x + 8, y + 22), (x + 38, y + 22), (x + 32, y + 30),
               (x + 14, y + 30)], fill=(120, 70, 30))
    d.line([x + 4, y + 36, x + 42, y + 36], fill=WHITE, width=2)
    d.line([x + 8, y + 41, x + 38, y + 41], fill=WHITE, width=2)

def ic_gaza(d, x, y):
    icon_bg(d, x, y, (150, 120, 60))
    d.rectangle([x + 8, y + 18, x + 22, y + 40], fill=(90, 80, 70))
    d.rectangle([x + 26, y + 26, x + 38, y + 40], fill=(110, 100, 88))
    smoke(d, x + 30, y + 16, 2, 5)

def ic_sudan(d, x, y):
    icon_bg(d, x, y, (120, 70, 30))
    d.rectangle([x + 8, y + 28, x + 20, y + 40], fill=(80, 60, 40))
    d.polygon([(x + 8, y + 28), (x + 14, y + 20), (x + 20, y + 28)], fill=(100, 70, 45))
    d.rectangle([x + 26, y + 30, x + 38, y + 40], fill=(80, 60, 40))
    smoke(d, x + 32, y + 24, 3, 6)

def ic_jets(d, x, y):
    icon_bg(d, x, y, (40, 60, 90))
    for (dx, dy) in [(8, 10), (24, 20)]:
        d.polygon([(x + dx, y + dy + 8), (x + dx + 14, y + dy),
                   (x + dx + 12, y + dy + 10)], fill=WHITE)
    d.ellipse([x + 30, y + 6, x + 40, y + 16], outline=YELLOW, width=2)
    d.line([x + 35, y + 16, x + 35, y + 22], fill=YELLOW, width=2)

def ic_ship(d, x, y):
    icon_bg(d, x, y, SEA_D)
    ship(d, x + 4, y + 28, 38, 8, hull=(200, 200, 200), deck=ORANGE)
    flames(d, x + 24, y + 26, 0.55)
    smoke(d, x + 28, y + 20, 2, 5)

MEDIUMS = [
    ("DYMER, UKRAINE", "BOY, 7, PULLED ALIVE AFTER 14 HOURS",
     "Russian strike kills 11 near Kyiv; boy survives.", ic_rubble),
    ("MARKETS", "KOSPI DIVES 3.31% AS AI ROUT SPREADS",
     "Seoul's worst close since Jan; Nasdaq fell 5.3%.", ic_chart),
    ("WASHINGTON", "DEMOCRATS TAKE 258 SEATS, MOST SINCE 1992",
     "Recount flips a seat by 330 votes; Foxx concedes.", ic_capitol),
    ("MEXICO", "\u2018EL CHAPO ISIDRO\u2019 CAPTURED IN SINALOA",
     "Cartel boss seized; 11 dead, four of them soldiers.", ic_cuffs),
    ("BELGIUM", "STRIKE GROUNDS 429 BRUSSELS FLIGHTS",
     "Air traffic control joins a national day of action.", ic_plane),
    ("POLAND", "CRASHED OBJECTS WERE RUSSIAN MISSILES",
     "Three fallen objects were Kh-101 cruise missiles.", ic_missile),
    ("NIGERIA", "BOAT OF MOURNERS CAPSIZES, 24 DEAD",
     "Funeral boat sinks in Bayelsa State; 24 rescued.", ic_boat),
    ("GAZA", "SIX KILLED, 33 WOUNDED IN 24 HOURS",
     "Health officials report the toll as the truce frays.", ic_gaza),
    ("SUDAN", "DRONES STRIKE HOMES ACROSS KHARTOUM",
     "Children killed; a humanitarian building also hit.", ic_sudan),
    ("TAIWAN", "TAIWAN COUNTS 24 CHINESE AIRCRAFT",
     "17 cross the median line; 11 warships also tracked.", ic_jets),
]

MX, MY0, MCW, MCH, MGAP = 8, 404, 326, 50, 8
for i, (kick, head, deck, fn) in enumerate(MEDIUMS):
    col, row = i % 2, i // 2
    x = MX + col * (MCW + MGAP)
    y = MY0 + row * (MCH + MGAP)
    fn(d, x, y)
    tx = x + 52
    tw = MCW - 52
    text(d, (tx, y - 1), kick, F(9, bold=True), fill=RED)
    hl = wrap(head, F(12, bold=True), tw)
    yy = para(d, tx, y + 11, tw, hl[:2], F(12, bold=True), leading=14)
    text(d, (tx, yy + 1), trunc(deck, F(10), tw), F(10), fill=(60, 64, 74))

# ---------------------------------------------------------------- world map
MAPX, MAPY, MAPW, MAPH = 676, 404, 340, 176
d.rectangle([MAPX, MAPY, MAPX + MAPW, MAPY + MAPH], fill=(196, 222, 238))
d.rectangle([MAPX, MAPY, MAPX + MAPW, MAPY + MAPH], outline=INK, width=1)

def proj(lon, lat):
    return (MAPX + 6 + (lon + 180) / 360.0 * (MAPW - 12),
            MAPY + 6 + (90 - lat) / 180.0 * (MAPH - 12))

CONTINENTS = [
    [(-168, 66), (-140, 70), (-125, 72), (-110, 68), (-95, 69), (-85, 66),
     (-80, 73), (-65, 60), (-55, 47), (-70, 42), (-75, 35), (-80, 32),
     (-85, 29), (-90, 21), (-95, 19), (-105, 20), (-115, 28), (-125, 40),
     (-125, 49), (-140, 60), (-165, 60)],
    [(-80, 10), (-70, 12), (-60, 8), (-50, 0), (-40, -5), (-35, -8),
     (-40, -20), (-48, -28), (-58, -38), (-65, -45), (-70, -52), (-73, -40),
     (-73, -20), (-80, -5), (-80, 5)],
    [(-17, 15), (-10, 30), (0, 36), (10, 37), (20, 32), (32, 31), (35, 28),
     (40, 15), (48, 11), (51, 12), (44, 0), (40, -10), (35, -20), (30, -30),
     (20, -35), (15, -30), (12, -18), (9, -1), (9, 4), (-8, 4), (-13, 8), (-17, 12)],
    [(-10, 36), (-9, 43), (-2, 48), (0, 50), (5, 53), (8, 57), (10, 59),
     (18, 56), (21, 55), (24, 59), (28, 60), (30, 62), (25, 65), (20, 70),
     (15, 68), (5, 60), (-5, 58), (-10, 54), (-10, 44), (-9, 38)],
    [(30, 62), (40, 68), (55, 70), (70, 72), (90, 75), (110, 76), (130, 72),
     (150, 70), (170, 66), (178, 65), (170, 60), (162, 56), (158, 52),
     (142, 50), (140, 40), (135, 35), (127, 33), (122, 30), (120, 25),
     (110, 20), (105, 10), (100, 8), (95, 15), (90, 22), (85, 20), (80, 8),
     (77, 8), (72, 20), (66, 25), (60, 25), (55, 26), (50, 29), (48, 30),
     (44, 29), (40, 31), (36, 36), (30, 36)],
    [(113, -22), (114, -30), (115, -35), (124, -33), (130, -32), (137, -35),
     (140, -38), (147, -39), (150, -37), (153, -32), (153, -27), (146, -19),
     (142, -11), (136, -12), (132, -11), (126, -14), (122, -17), (118, -20)],
]
for poly in CONTINENTS:
    d.polygon([proj(lo, la) for lo, la in poly], fill=(120, 170, 110),
              outline=(70, 120, 70))

PINS = [  # (lon, lat, label, lead?) - lead pins nudged apart for legibility
    (31.5, 39.0, "ANTALYA", True),
    (57.5, 24.5, "HORMUZ", True),
    (18.0, 30.0, "BENGHAZI", True),
    (30.5, 50.5, "", False), (127.0, 37.5, "", False), (-79.0, 35.8, "", False),
    (-107.0, 24.0, "", False), (4.4, 50.8, "", False), (6.3, 4.9, "", False),
    (34.5, 31.5, "", False), (32.5, 15.6, "", False), (121.0, 23.7, "", False),
    (24.0, 59.5, "", False), (50.6, 26.2, "", False),
]
for n, (lo, la, lab, lead) in enumerate(PINS, 1):
    px, py = proj(lo, la)
    if lead:
        d.ellipse([px - 7, py - 7, px + 7, py + 7], fill=RED, outline=WHITE, width=2)
        d.text((px, py), str(n), font=F(8, bold=True), fill=WHITE, anchor="mm")
    else:
        d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=GOLD, outline=INK, width=1)
d.rectangle([MAPX + 8, MAPY + MAPH - 22, MAPX + 132, MAPY + MAPH - 6],
            fill=(255, 255, 255))
d.text((MAPX + 12, MAPY + MAPH - 20), "1 ANTALYA  2 HORMUZ  3 BENGHAZI",
       font=F(9, bold=True), fill=RED_D)

# ---------------------------------------------------------------- date check box
DX, DY, DW, DH = 676, 588, 340, 98
d.rectangle([DX, DY, DX + DW, DY + DH], fill=CREAM, outline=RED, width=2)
text(d, (DX + 10, DY + 6), "DATE CHECK — MONDAY 23 NOVEMBER 2026", F(11, bold=True), fill=RED_D)
checks = [
    "COP31 collapsed Sun 22 Nov; row passes to COP32.",
    "Merkury sunk Sun 22 Nov; Kyiv confirmed Mon 23 Nov.",
    "Kospi fell 3.31% Mon 23 Nov; worst since January.",
    "Every story is 23 Nov news, or confirmed that day.",
]
yy = DY + 26
for c in checks:
    d.text((DX + 10, yy), "\u2022", font=F(11, bold=True), fill=RED)
    yy = para(d, DX + 22, yy, DW - 32, wrap(c, F(11), DW - 32), F(11), leading=14)
    yy += 2

# ---------------------------------------------------------------- numbered list
d.rectangle([8, 694, 1016, 716], fill=NAVY)
text(d, (16, 699), "THE REST OF THE DAY — IN 31 NUMBERS", F(13, bold=True), fill=WHITE)
text(d, (1008, 699), "WORLD  •  BUSINESS  •  SCIENCE  •  CULTURE", F(11, bold=True),
     fill=(200, 210, 230), anchor="ra")

ITEMS = [
    "World court: Myanmar committed genocide against the Rohingya",
    "Houthi missile damages Riyadh's tallest tower",
    "Israeli forces cross the Yellow Line in central Gaza",
    "Iran war enters month nine; US Senate blocks war resolution",
    "White House fires cyber chief Sean Cairncross",
    "Voyager 1 phones home from a light-day away",
    "Gas blast in Georgia collapses a block of flats; 3-6 dead",
    "Kenya frees its last Ebola patient; WHO pleads for Congo team",
    "Denmark approves the US-Greenland security deal",
    "US and Venezuela sign a military cooperation deal",
    "A Van Gogh sells for a record $190.4m",
    "Hippo Fiona dies days after swallowing a visitor's hat",
    "Scientists grow potatoes in moon soil",
    "Bukele registers for a third term in El Salvador",
    "Iran inflation hits 76.8%; Argentina's rises to 2.2%",
    "US flight chaos ignites a fight over air-traffic funding",
    "Spain's Vox goes mainstream; PP leads before Sunday's vote",
    "NHS launches the largest AI breast-cancer trial",
    "EU signs a trade deal with Indonesia",
    "Bitcoin bounces 3% off two-year lows",
    "Deal averts a strike at America's busiest ports",
    "Trump wants a Ukraine peace deal by early January",
    "Trump signals Iran strikes could resume after New Year",
    "Strike on Vyshneve kills three, wounds 13",
    "NATO council meets in Brussels over Poland missiles",
    "US federal funding runs out on 11 December",
    "Brent crude holds at $92.10 a barrel",
    "COP31 agrees a just-transition package after all",
    "90+ countries sign COP31's electrification pledge",
    "Qatari delegation visits Tehran to mediate",
    "Iran says it shot down a US drone over Qeshm",
]
assert len(ITEMS) == 31, len(ITEMS)
COLW = 328
COLX = [8, 348, 688]
n_per_col = [11, 10, 10]
idx = 0
for c, (cx, n) in enumerate(zip(COLX, n_per_col)):
    y = 722
    for k in range(n):
        item = ITEMS[idx]
        idx += 1
        num = f"{idx}."
        d.text((cx, y), num, font=F(10, bold=True), fill=RED)
        nw = F(10, bold=True).getlength(num) + 5
        lines = wrap(item, F(10), COLW - nw)[:2]
        y = para(d, cx + nw, y, COLW - nw, lines, F(10), leading=12)
        y += 6

# ---------------------------------------------------------------- footer / sources
d.rectangle([0, 990, W, 1024], fill=NAVY)
text(d, (512, 996),
     "Sources: Reuters  •  AP  •  Al Jazeera  •  CNN  •  BBC  •  Yonhap  •  AFP  •  WSJ  •  Morningstar  •  Chosun Biz",
     F(10), fill=(210, 218, 232), anchor="ma")
text(d, (512, 1010),
     "All stories verified 23-24 November 2026  •  The World Today  •  One day, one page",
     F(10), fill=(160, 170, 190), anchor="ma")

img.save("entry.png", optimize=True)
print("saved entry.png")
