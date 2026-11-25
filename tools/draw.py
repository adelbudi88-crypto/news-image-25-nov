#!/usr/bin/env python3
"""Draw the 25 November 2026 front page: 1024x1024, deterministic.

v3 — built from the v2 newspaper template (31 stories, round 2 of
24 Nov: score 708,842, rank 272/9,063) and from the three round-2
winning posters of 24 Nov, viewed directly (gentle-koala-36
851,588; lialie 846,503; brandalgenius 844,477):

  * Winners run 35-38 stories; v3 runs 41 (3 leads + 10 picture
    stories + 28 briefs). Density is the differentiator.
  * Winners use full-colour painted scenes and MAPS as hero art;
    v3 enriches every mini-illustration (sky bands, figures,
    extra shapes) and adds certainty chips (REPORTED / OFFICIAL /
    CLAIM / ONGOING / TODAY) on every picture story, as the
    winners do.
  * Winners put six big figures in the numbers strip, a timed
    UTC strip, region tabs with counts, a numbered-pins map, a
    numbered briefs list and a DATE CHECK footer naming what was
    deliberately left out. v3 keeps all of it.

STRICT SAME-DAY BAR (per RULES.txt: events that happened, or were
first reported, on 25 November 2026 in any time zone). Built Wed
25 Nov 09:00 WIB (02:00 UTC), so this edition covers the Wed
morning news cycle plus Wed-scheduled events (marked TODAY).
Everything first reported Tue 24 Nov or earlier is LEFT OUT and
named in the DATE CHECK footer instead of appearing as news.

VERIFIED STORIES (all checked live 25 Nov 2026, 01:00-02:00 UTC):
  Leads: Asia gives back the rally -- Nikkei -2.8% Wed (Dow Jones
  Newswires 2026-11-25T00:19Z), Kospi -4%+ (firstfeednews);
  Australia-Solomon Islands security pact SIGNED Wed (Reuters,
  URL dated 2026-11-25); gold $3,544.54, Dec Fed hike 96.4%
  priced, PCE + Q3 GDP due 13:30 GMT (Reuters 00:24 GMT).
  Pictures: Australia apologises to LGBTQ veterans (Reuters Wed
  01:16 GMT); Iran rial at record low (Arab News Wed 25 Nov
  front page); Saudi 2027 budget predicts growth (Arab News Wed
  front page); Kenya opposition vs IEBC (Daily Nation / People
  Daily, Wed front pages); Tanzania grows 5.9%, IMF reforms
  (The Citizen, Wed); UK pancreatic-cancer drug, 90% tumour
  control (East African Wed papers); Bougainville vote under way
  in PNG parliament, 89 of 118 MPs needed (The Conversation /
  Business Melanesia); chess Game 2 today, Gukesh White,
  0.5-0.5, 15:00 CET Geneva (worldchess); UCL tonight, 9 games
  (UEFA); US PCE + Q3 GDP due 13:30 GMT (Reuters).
  Briefs: German GDP detailed Q3 due 07:00 GMT; Australia Oct
  inflation due Wed; BoE Bailey before Treasury Committee;
  Deere reports Wed, US markets shut Thu for Thanksgiving; US
  $44bn 7-year auction; Trump Section 301 tariff findings due
  Tue/Wed; ASX -0.4% to 8,692 (Reuters Wed); silver $40.79,
  platinum $1,267.65 (Reuters Wed); dollar 159.24 yen (DJN Wed);
  Advantest -12%, JX Metals -8.1% (DJN Wed); Sensex reopens
  09:15 IST after Guru Nanak holiday, Mon close 82,435.99; NZ
  shares gain at open; Vodafone gain from Safaricom deal
  (Business Daily, Wed); Kenya eCitizen cyberattack fears (The
  Star, Wed); Uganda gold imports (Daily Monitor, Wed);
  Tanzania school-bus cameras (Mwananchi, Wed); Palestinian
  student release demanded (Arab News, Wed); Netanyahu (Arab
  News, Wed); Saudi law protecting women (Arab News, Wed);
  church attackers in Jordan (Arab News, Wed); Darana Alvarez
  in Marrakech (Arab News, Wed); PNG 2027 budget due Thu;
  Rising Stars semis Thu/Fri; India women vs China, Asian
  Champions Trophy (today); JEE Main 2027 registration
  continues; Avengers: Doomsday final trailer out (Marvel);
  Super Bowl LXI to be shown live in Imax; OpenAI + Cisco
  build Shirudo as Linux patches lag weeks.
DROPPED (first reported Tue 24 Nov or earlier -- named in the
DATE CHECK, not shown as news): Houthi strike on Riyadh tower,
11 hurt (Tue); CIA + ODNI breach (NYT, Tue); CAS restores
Senegal as AFCON champions (Tue); chess Game 1 draw (Tue);
UCL Tue results -- Real Madrid 5-1 PSV, Arsenal 1-1 Dortmund,
Man City 2-2 Napoli (Tue night); Sooryavanshi 204 off 53 (Tue);
England beat Australia, 2nd T20I (Tue); quasar Dun Aonghasa
announced (Tue); Turkish helicopter crash, 5 dead (Tue);
SpaceX/Grok suits filed Mon 23 Nov; COP31 collapse (Sun
22 Nov); Nvidia -6% Tue.

Deterministic: no randomness, no clock, no network. DejaVu
Serif + Sans from /usr/share/fonts/truetype/dejavu.
Run: python3 tools/draw.py  ->  entry.png (1024x1024, <1 MiB).
"""

import math
import os
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
MARGIN = 20
CONTENT_W = W - 2 * MARGIN  # 984

PAPER = (246, 241, 227)
INK = (26, 26, 26)
INK_SOFT = (74, 74, 74)
RED = (166, 30, 30)
RED_DARK = (140, 22, 22)
BLUE = (31, 78, 121)
NAVY = (24, 44, 74)
GOLD = (176, 132, 32)
GREEN = (40, 110, 70)
GREY = (96, 96, 96)
SEA = (52, 96, 130)
SKY = (214, 228, 238)
OCEAN = (223, 233, 238)
LAND = (232, 220, 192)
CARD = (252, 250, 244)
BORDER = (180, 172, 150)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


def serif(size):
    return font("DejaVuSerif.ttf", size)


def serif_b(size):
    return font("DejaVuSerif-Bold.ttf", size)


def sans(size):
    return font("DejaVuSans.ttf", size)


def sans_b(size):
    return font("DejaVuSans-Bold.ttf", size)


def text_w(draw, text, fnt):
    return draw.textlength(text, font=fnt)


def wrap_text(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = f"{cur} {word}".strip()
        if text_w(draw, trial, fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, x, y, lines, fnt, fill, lh):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += lh
    return y


def rule(draw, x0, y, x1, color=INK, width=1):
    draw.line([x0, y, x1, y], fill=color, width=width)


def tag_chip(draw, x, y, text, fill=RED, fg=(255, 255, 255), size=10):
    """Small filled label, e.g. CONFIRMED - AP. Returns its width."""
    fnt = sans_b(size)
    w = int(text_w(draw, text, fnt)) + 12
    draw.rounded_rectangle([x, y, x + w, y + 16], radius=3, fill=fill)
    draw.text((x + 6, y + 2), text, font=fnt, fill=fg)
    return w


def chip_right(draw, x1, y, text, fill):
    """Certainty chip right-aligned to x1 inside an art box."""
    fnt = sans_b(8)
    w = int(text_w(draw, text, fnt)) + 10
    x0 = x1 - w - 4
    draw.rounded_rectangle([x0, y + 3, x0 + w, y + 17], radius=3, fill=fill)
    draw.text((x0 + 5, y + 5), text, font=fnt, fill=(255, 255, 255))
    return x0


# ------------------------------------------------------------------
# Lead art (90px tall boxes, 320 wide). Richer than v2: sky bands,
# figures, stamps -- closer to the winners' painted heroes.
# ------------------------------------------------------------------

def art_lead_fall(draw, x0, y0, x1, y1):
    draw.rectangle([x0, y0, x1, y1], fill=(16, 28, 44))
    for gy in (y0 + 22, y0 + 44, y0 + 66):
        draw.line([x0 + 8, gy, x1 - 8, gy], fill=(40, 60, 84), width=1)
    # Falling line: flat, then a sharp drop.
    pts = [(x0 + 12, y1 - 58), (x0 + 90, y1 - 56), (x0 + 150, y1 - 52),
           (x0 + 210, y1 - 38), (x0 + 260, y1 - 26), (x1 - 14, y1 - 14)]
    draw.line(pts, fill=(255, 90, 70), width=4, joint="curve")
    ex, ey = pts[-1]
    draw.polygon([(ex, ey), (ex - 16, ey + 2), (ex - 4, ey - 12)],
                 fill=(255, 90, 70))
    draw.text((x0 + 10, y0 + 6), "NIKKEI  -2.8%", font=sans_b(20),
              fill=(255, 90, 70))
    draw.text((x0 + 10, y1 - 20),
              "Kospi -4%  ·  Advantest -12%  ·  bounce fades",
              font=sans(11), fill=(190, 205, 220))


def art_lead_pact(draw, x0, y0, x1, y1):
    draw.rectangle([x0, y0, x1, y1], fill=(214, 228, 238))
    # Sea + islands, bottom.
    draw.rectangle([x0, y0 + 56, x1, y1], fill=(52, 120, 150))
    draw.ellipse([x0 + 16, y0 + 62, x0 + 110, y1 - 6], fill=(224, 198, 138))
    draw.ellipse([x0 + 190, y0 + 66, x0 + 280, y1 - 10], fill=(210, 186, 130))
    # Two flags on poles.
    for fx, col in ((x0 + 44, (24, 44, 120)), (x0 + 232, (30, 120, 80))):
        draw.line([fx, y0 + 8, fx, y0 + 56], fill=(90, 60, 30), width=3)
        draw.rectangle([fx, y0 + 8, fx + 44, y0 + 30], fill=col)
        draw.ellipse([fx + 18, y0 + 15, fx + 26, y0 + 23], fill=CARD)
    # SIGNED stamp, centre.
    sx0, sy0 = x0 + 108, y0 + 34
    draw.rectangle([sx0, sy0, sx0 + 104, sy0 + 26],
                   outline=RED_DARK, width=3)
    draw.text((sx0 + 12, sy0 + 4), "SIGNED", font=sans_b(18),
              fill=RED_DARK)


def art_lead_gold(draw, x0, y0, x1, y1):
    draw.rectangle([x0, y0, x1, y1], fill=(28, 24, 18))
    # Gold bars, stacked bottom-left.
    for i, (bx, by, bw) in enumerate(((x0 + 12, y1 - 18, 84),
                                      (x0 + 28, y1 - 32, 84),
                                      (x0 + 44, y1 - 46, 84))):
        draw.polygon([(bx, by), (bx + bw, by), (bx + bw - 10, by + 16),
                      (bx + 10, by + 16)], fill=(212, 175, 55))
        draw.line([bx, by, bx + bw, by], fill=(240, 210, 110), width=2)
    # Rising line, right.
    pts = [(x0 + 170, y1 - 24), (x0 + 210, y1 - 34), (x0 + 250, y1 - 44),
           (x0 + 285, y1 - 66), (x1 - 12, y1 - 76)]
    draw.line(pts, fill=(74, 222, 128), width=3, joint="curve")
    draw.text((x0 + 170, y0 + 6), "$3,544", font=sans_b(22), fill=GOLD)
    draw.text((x0 + 170, y0 + 32), "spot gold", font=sans(11),
              fill=(200, 190, 170))
    draw.text((x0 + 10, y0 + 6), "96.4%", font=sans_b(20), fill=CARD)
    draw.text((x0 + 10, y0 + 30), "Dec hike odds", font=sans(10),
              fill=(200, 190, 170))


# ------------------------------------------------------------------
# Picture-story mini art (40px tall, ~190 wide). Each scene has a
# sky band, a ground band and 3-6 shapes -- richer than v2's flat
# icons, in the winners' painted-scene spirit.
# ------------------------------------------------------------------

def mini_apology(draw, x0, y0, x1, y1):
    draw.rectangle([x0, y0, x1, y1], fill=SKY)
    draw.rectangle([x0, y0 + 28, x1, y1], fill=(120, 110, 96))
    # Flag pole + Australian-blue flag.
    draw.line([x0 + 22, y0 + 4, x0 + 22, y0 + 30], fill=(90, 60, 30), width=3)
    draw.rectangle([x0 + 22, y0 + 4, x0 + 62, y0 + 20], fill=(24, 44, 120))
    for sx, sy in ((x0 + 32, y0 + 9), (x0 + 44, y0 + 14), (x0 + 54, y0 + 8)):
        draw.ellipse([sx, sy, sx + 3, sy + 3], fill=CARD)
    # Podium + speaker silhouette.
    draw.rectangle([x0 + 96, y1 - 18, x0 + 150, y1 - 2], fill=(90, 80, 64))
    draw.ellipse([x0 + 116, y0 + 12, x0 + 130, y0 + 26], fill=INK)
    draw.rectangle([x0 + 112, y0 + 26, x0 + 134, y1 - 2], fill=INK)
    draw.text((x1 - 46, y0 + 6), "SORRY", font=sans_b(12), fill=RED_DARK)


def mini_rial(draw, x0, y0, x1, y1):
    draw.rectangle([x0, y0, x1, y1], fill=(246, 232, 228))
    draw.rectangle([x0 + 14, y0 + 8, x0 + 120, y1 - 8], fill=(252, 250, 244),
                   outline=(150, 90, 80), width=1)
    draw.ellipse([x0 + 58, y0 + 12, x0 + 76, y0 + 30], fill=(150, 90, 80))
    draw.text((x0 + 20, y0 + 12), "RIAL", font=sans_b(11), fill=INK_SOFT)
    # Red down arrow.
    draw.line([x1 - 52, y0 + 6, x1 - 52, y1 - 14], fill=RED, width=4)
    draw.polygon([(x1 - 62, y1 - 16), (x1 - 42, y1 - 16), (x1 - 52, y1 - 4)],
                 fill=RED)
    draw.line([x1 - 70, y0 + 30, x1 - 52, y0 + 12], fill=RED, width=2)


def mini_budget(draw, x0, y0, x1, y1):
    draw.rectangle([x0, y0, x1, y1], fill=(214, 200, 170))
    draw.polygon([(x0 + 20, y0 + 14), (x1 - 60, y0 + 14),
                  ((x0 + x1) // 2 - 20, y0 + 2)], fill=(90, 80, 64))
    for c in range(3):
        cx = x0 + 34 + c * 30
        draw.rectangle([cx, y0 + 16, cx + 9, y1 - 6], fill=(252, 250, 244))
    # Rising bars, right.
    for i, h in enumerate((8, 14, 22)):
        bx = x1 - 52 + i * 14
        draw.rectangle([bx, y1 - 6 - h, bx + 10, y1 - 6], fill=GREEN)
    draw.text((x1 - 52, y0 + 4), "2027", font=sans_b(11), fill=GREEN)


def mini_kenya(draw, x0, y0, x1, y1):
    draw.rectangle([x0, y0, x1, y1], fill=(240, 232, 214))
    # Kenyan flag stripes.
    for i, col in enumerate(((26, 26, 26), (166, 30, 30), (40, 110, 70))):
        draw.rectangle([x0, y0 + 4 + i * 6, x0 + 70, y0 + 10 + i * 6],
                       fill=col)
    # Ballot box + check.
    draw.rectangle([x0 + 96, y0 + 12, x0 + 160, y1 - 4], fill=(90, 80, 64))
    draw.rectangle([x0 + 104, y0 + 6, x0 + 152, y0 + 12], fill=(120, 110, 96))
    draw.line([x0 + 164, y0 + 10, x0 + 174, y0 + 22], fill=RED, width=3)
    draw.line([x0 + 174, y0 + 22, x0 + 188, y0 + 4], fill=RED, width=3)
    draw.text((x0 + 8, y1 - 14), "IEBC", font=sans_b(10), fill=INK_SOFT)


def mini_tanzania(draw, x0, y0, x1, y1):
    draw.rectangle([x0, y0, x1, y1], fill=SKY)
    draw.rectangle([x0, y0 + 26, x1, y1], fill=(224, 198, 138))
    # Skyline blocks.
    for bx, bh in ((x0 + 10, 14), (x0 + 30, 20), (x0 + 54, 12), (x0 + 76, 18)):
        draw.rectangle([bx, y1 - 4 - bh, bx + 18, y1 - 4], fill=(90, 80, 64))
    # Rising chart.
    pts = [(x0 + 110, y1 - 8), (x0 + 135, y1 - 16), (x0 + 160, y1 - 22),
           (x1 - 8, y1 - 34)]
    draw.line(pts, fill=GREEN, width=3, joint="curve")
    draw.text((x1 - 58, y0 + 4), "+5.9%", font=sans_b(13), fill=GREEN)


def mini_drug(draw, x0, y0, x1, y1):
    draw.rectangle([x0, y0, x1, y1], fill=(226, 238, 226))
    # Lab bench + flasks.
    draw.rectangle([x0, y0 + 28, x1, y1 - 2], fill=(120, 110, 96))
    for fx, col in ((x0 + 22, (52, 128, 180)), (x0 + 62, (40, 110, 70)),
                    (x0 + 102, (176, 132, 32))):
        draw.polygon([(fx + 6, y0 + 8), (fx + 14, y0 + 8), (fx + 18, y0 + 24),
                      (fx + 2, y0 + 24)], fill=col)
        draw.rectangle([fx, y0 + 24, fx + 20, y0 + 28], fill=col)
    draw.ellipse([x1 - 34, y0 + 4, x1 - 6, y0 + 30], fill=CARD,
                 outline=GREEN, width=2)
    draw.text((x1 - 30, y0 + 9), "90%", font=sans_b(10), fill=GREEN)


def mini_bougainville(draw, x0, y0, x1, y1):
    draw.rectangle([x0, y0, x1, y1], fill=(52, 120, 150))
    draw.ellipse([x0 + 14, y0 + 16, x0 + 92, y1 - 4], fill=(224, 198, 138))
    draw.line([x0 + 44, y0 + 20, x0 + 40, y0 + 6], fill=(90, 60, 30), width=4)
    draw.arc([x0 + 24, y0 + 2, x0 + 58, y0 + 16], 200, 340,
             fill=(52, 128, 74), width=4)
    # Ballot box, right.
    draw.rectangle([x1 - 64, y0 + 12, x1 - 10, y1 - 4], fill=(90, 80, 64))
    draw.rectangle([x1 - 58, y0 + 6, x1 - 16, y0 + 12], fill=(120, 110, 96))
    draw.text((x1 - 58, y0 + 16), "89", font=sans_b(14), fill=CARD)


def mini_chess(draw, x0, y0, x1, y1):
    draw.rectangle([x0, y0, x1, y1], fill=(60, 48, 36))
    # 4x4 board.
    bs, ox, oy = 9, x0 + 14, y0 + 2
    for r in range(4):
        for c in range(4):
            col = CARD if (r + c) % 2 == 0 else (120, 100, 78)
            draw.rectangle([ox + c * bs, oy + r * bs,
                            ox + (c + 1) * bs, oy + (r + 1) * bs], fill=col)
    # Two pieces: white king + black knight (circles with letters).
    draw.ellipse([x0 + 78, y0 + 6, x0 + 104, y0 + 32], fill=CARD,
                 outline=INK, width=2)
    draw.text((x0 + 86, y0 + 9), "K", font=sans_b(16), fill=INK)
    draw.ellipse([x0 + 122, y0 + 8, x0 + 146, y0 + 32], fill=INK)
    draw.text((x0 + 130, y0 + 11), "N", font=sans_b(14), fill=CARD)
    draw.text((x1 - 46, y0 + 8), "0.5-0.5", font=sans_b(11), fill=CARD)


def mini_ucl(draw, x0, y0, x1, y1):
    draw.rectangle([x0, y0, x1, y1], fill=(36, 110, 70))
    for i in range(3):
        draw.line([x0, y0 + 10 + i * 12, x1, y0 + 10 + i * 12],
                  fill=(52, 132, 88), width=5)
    # Ball.
    bx, by = x0 + 30, y0 + 20
    draw.ellipse([bx - 12, by - 12, bx + 12, by + 12], fill=CARD)
    draw.polygon([(bx, by - 6), (bx + 5, by - 2), (bx + 3, by + 5),
                  (bx - 3, by + 5), (bx - 5, by - 2)], fill=INK)
    # Star-ball, right.
    sx, sy = x1 - 30, y0 + 20
    draw.ellipse([sx - 14, sy - 14, sx + 14, sy + 14], fill=NAVY,
                 outline=GOLD, width=2)
    for k in range(5):
        ang = -math.pi / 2 + k * 2 * math.pi / 5
        px, py = sx + 8 * math.cos(ang), sy + 8 * math.sin(ang)
        draw.ellipse([px - 1, py - 1, px + 1, py + 1], fill=GOLD)
    draw.text((x0 + 52, y0 + 12), "9 GAMES", font=sans_b(11), fill=CARD)


def mini_pce(draw, x0, y0, x1, y1):
    draw.rectangle([x0, y0, x1, y1], fill=(226, 232, 238))
    # Bar chart + clock.
    base = y1 - 6
    for i, h in enumerate((10, 16, 12, 22)):
        bx = x0 + 16 + i * 22
        draw.rectangle([bx, base - h, bx + 14, base],
                       fill=BLUE if i < 3 else RED)
    draw.ellipse([x1 - 34, y0 + 6, x1 - 8, y0 + 32], fill=CARD,
                 outline=INK, width=2)
    draw.line([x1 - 21, y0 + 19, x1 - 21, y0 + 11], fill=INK, width=2)
    draw.line([x1 - 21, y0 + 19, x1 - 15, y0 + 19], fill=INK, width=2)
    draw.text((x0 + 14, y0 + 4), "13:30 GMT", font=sans_b(11), fill=INK)


# ------------------------------------------------------------------
# World map: continents as (lon, lat) outlines, projected into the
# map box (x 20..316, y 650..852). Pins are placed by lon/lat too,
# nudged a few px where two stories share a crowded corner.
# ------------------------------------------------------------------

MAP_X0, MAP_Y0, MAP_X1, MAP_Y1 = 20, 650, 316, 852


def _ll(lon, lat):
    x = MAP_X0 + (lon + 170) / 360 * (MAP_X1 - MAP_X0)
    y = MAP_Y0 + (75 - lat) / 130 * (MAP_Y1 - MAP_Y0)
    return (int(x), int(y))


CONTINENTS_LL = [
    # North America
    [(-168, 66), (-140, 70), (-125, 72), (-110, 68), (-95, 69),
     (-85, 66), (-80, 73), (-65, 60), (-55, 47), (-70, 42),
     (-75, 35), (-80, 26), (-85, 30), (-95, 29), (-97, 26),
     (-105, 20), (-110, 24), (-125, 40), (-125, 49), (-140, 60),
     (-155, 58), (-165, 60)],
    # Greenland
    [(-45, 60), (-30, 68), (-20, 70), (-30, 76), (-55, 76), (-58, 70)],
    # South America
    [(-80, 10), (-75, 5), (-60, 0), (-50, -5), (-35, -8), (-40, -20),
     (-48, -28), (-58, -35), (-65, -45), (-70, -55), (-73, -40),
     (-72, -20), (-77, -12), (-80, -3)],
    # Europe
    [(-10, 36), (-9, 43), (-2, 48), (0, 50), (5, 53), (8, 57),
     (10, 59), (18, 56), (21, 55), (24, 58), (28, 60), (30, 62),
     (28, 70), (20, 70), (15, 68), (12, 65), (5, 60), (5, 58),
     (-2, 57), (-5, 50), (-9, 43), (-10, 37)],
    # Africa
    [(-6, 35), (0, 36), (10, 37), (20, 32), (30, 31), (35, 28),
     (32, 20), (38, 18), (43, 12), (48, 11), (51, 10), (44, 0),
     (40, -10), (35, -18), (32, -26), (28, -33), (20, -35),
     (15, -28), (12, -18), (9, -1), (9, 4), (-8, 5), (-13, 8),
     (-17, 15), (-16, 20), (-15, 28), (-10, 31)],
    # Asia
    [(30, 62), (40, 68), (55, 68), (70, 72), (90, 75), (110, 76),
     (130, 72), (150, 70), (170, 66), (178, 65), (170, 60),
     (160, 55), (150, 45), (142, 40), (135, 35), (127, 33),
     (122, 30), (120, 22), (110, 10), (105, 5), (100, 8), (95, 15),
     (90, 22), (85, 20), (80, 15), (75, 10), (72, 20), (66, 25),
     (60, 25), (55, 28), (50, 30), (48, 30), (43, 35), (38, 36),
     (35, 36), (30, 36)],
    # Australia
    [(113, -22), (114, -30), (115, -35), (120, -34), (125, -33),
     (130, -32), (135, -35), (140, -38), (145, -38), (150, -37),
     (153, -27), (150, -22), (146, -19), (142, -15), (142, -11),
     (137, -12), (135, -15), (132, -12), (130, -13), (126, -14),
     (122, -17), (118, -20)],
]

# Story number -> (lon, lat).
PINS_LL = {
    1: (139, 36),   # Tokyo, Nikkei
    2: (160, -9),   # Honiara, Solomons pact
    3: (-74, 41),   # New York, gold / Fed
    4: (149, -35),  # Canberra, apology
    5: (51, 36),    # Tehran, rial
    6: (47, 25),    # Riyadh, budget
    7: (37, -1),    # Nairobi, IEBC
    8: (39, -7),    # Dar es Salaam, growth
    9: (0, 51),     # London, cancer drug
    10: (147, -9),  # Port Moresby, Bougainville
    11: (6, 46),    # Geneva, chess
    12: (2, 49),    # Paris, UCL tonight (9 cities)
    13: (-77, 39),  # Washington, PCE + GDP
}

# Pixel nudges (dx, dy) applied after projection, to keep crowded
# European / East-African / Pacific pins from sitting on each other.
PIN_NUDGE = {
    2: (8, -6), 5: (6, -4), 6: (-4, 6), 7: (-8, -4), 8: (8, 4),
    9: (-10, -6), 10: (-6, 6), 11: (9, 7), 12: (9, -7),
}


def draw_map(draw, x0, y0, x1, y1):
    draw.rectangle([x0, y0, x1, y1], fill=OCEAN, outline=BORDER, width=1)
    for poly in CONTINENTS_LL:
        draw.polygon([_ll(lon, lat) for lon, lat in poly], fill=LAND,
                     outline=(190, 178, 148))
    for num, (lon, lat) in sorted(PINS_LL.items()):
        px, py = _ll(lon, lat)
        dx, dy = PIN_NUDGE.get(num, (0, 0))
        px, py = px + dx, py + dy
        draw.ellipse([px - 8, py - 8, px + 8, py + 8], fill=RED,
                     outline=CARD, width=1)
        label = str(num)
        tw = text_w(draw, label, sans_b(9))
        draw.text((px - tw / 2, py - 7), label, font=sans_b(9),
                  fill=(255, 255, 255))


def num_circle(draw, x, y, num, r=11):
    draw.ellipse([x - r, y - r, x + r, y + r], fill=RED)
    label = str(num)
    tw = text_w(draw, label, sans_b(10))
    draw.text((x - tw / 2, y - 7), label, font=sans_b(10),
              fill=(255, 255, 255))


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([10, 10, W - 11, H - 11], outline=INK, width=2)

    # ---- masthead --------------------------------------------------
    d.text((MARGIN, 22), "THE WORLD ON ONE PAGE", font=sans_b(13),
           fill=RED)
    centre = "DAY 329 OF 2026"
    d.text(((W - text_w(d, centre, sans_b(12))) / 2, 23), centre,
           font=sans_b(12), fill=INK)
    right = "41 STORIES  ·  7 REGIONS  ·  WEDNESDAY'S NEWS"
    d.text((W - MARGIN - text_w(d, right, sans_b(12)), 23), right,
           font=sans_b(12), fill=INK)
    rule(d, MARGIN, 42, W - MARGIN, color=INK, width=2)
    d.text((MARGIN, 48), "Wednesday 25 November 2026", font=serif_b(42),
           fill=INK)
    rule(d, MARGIN, 104, W - MARGIN, color=RED, width=2)

    # ---- region strip ----------------------------------------------
    regions = [
        ("ASIA 7", 160, (166, 30, 30)),
        ("EUROPE 5", 130, (31, 78, 121)),
        ("MID EAST 6", 150, (150, 90, 40)),
        ("AMERICAS 6", 150, (40, 110, 70)),
        ("AFRICA 7", 160, (120, 80, 140)),
        ("OCEANIA 7", 150, (30, 120, 130)),
        ("WORLD 3", 84, (90, 90, 90)),
    ]
    rx = MARGIN
    for label, w, col in regions:
        d.rectangle([rx, 110, rx + w, 130], fill=col)
        tw = text_w(d, label, sans_b(10))
        d.text((rx + (w - tw) / 2, 115), label, font=sans_b(10),
               fill=(255, 255, 255))
        rx += w

    # ---- THE DAY IN UTC --------------------------------------------
    d.rectangle([MARGIN, 134, MARGIN + 110, 160], fill=RED)
    d.text((MARGIN + 8, 136), "THE DAY", font=sans_b(10),
           fill=(255, 255, 255))
    d.text((MARGIN + 8, 147), "IN UTC", font=sans_b(10),
           fill=(255, 255, 255))
    slots = [
        ("00:19 GMT", "Nikkei falls 2.8%"),
        ("00:24 GMT", "Gold $3,544"),
        ("01:16 GMT", "Australia says sorry"),
        ("07:00 GMT", "German GDP due"),
        ("13:30 GMT", "US PCE + GDP"),
        ("15:00 CET", "Chess Game 2"),
    ]
    sx = MARGIN + 116
    sw = (W - MARGIN - sx) // 6
    for i, (part, story) in enumerate(slots):
        x = sx + i * sw
        if i:
            d.line([x - 4, 136, x - 4, 158], fill=BORDER, width=1)
        d.text((x, 136), part, font=sans_b(9), fill=RED)
        d.text((x, 147), story, font=sans(9), fill=INK)

    # ---- THE DAY IN NUMBERS ----------------------------------------
    d.rectangle([MARGIN, 164, MARGIN + 150, 190], fill=INK)
    d.text((MARGIN + 8, 168), "THE DAY", font=sans_b(10),
           fill=(255, 255, 255))
    d.text((MARGIN + 8, 179), "IN NUMBERS", font=sans_b(10),
           fill=(255, 255, 255))
    numbers = [
        ("-2.8%", "Nikkei, Wed fall"),
        ("-4%", "Kospi, Wed fall"),
        ("$3,544", "Gold, spot oz"),
        ("96.4%", "Dec hike odds"),
        ("8,692", "ASX 200"),
        ("89", "MPs for Bougainville"),
    ]
    nx = MARGIN + 156
    nw = (W - MARGIN - nx) // 6
    for i, (num, label) in enumerate(numbers):
        x = nx + i * nw
        if i:
            d.line([x - 4, 166, x - 4, 188], fill=BORDER, width=1)
        d.text((x, 166), num, font=sans_b(16), fill=RED)
        d.text((x, 183), label, font=sans(9), fill=INK_SOFT)

    # ---- 3 leads ----------------------------------------------------
    leads = [
        (1, "MARKETS · TOKYO", "DJN · REUTERS", art_lead_fall,
         "REPORTED",
         "Asia gives back the rally",
         "Nikkei falls 2.8% and the Kospi drops 4%+ as the Nvidia "
         "bounce fades; chip stocks lead the slide."),
        (2, "PACIFIC · HONIARA", "REUTERS", art_lead_pact,
         "OFFICIAL",
         "Solomons sign with Canberra",
         "Australia becomes the Solomons' defence partner of "
         "choice; the 2022 China security pact is dropped."),
        (3, "MARKETS · NEW YORK", "REUTERS", art_lead_gold,
         "REPORTED",
         "Gold $3,544 as hike bets build",
         "Gold holds $3,544 as traders price a 96.4% chance of a "
         "December Fed hike; PCE and Q3 GDP due 13:30 GMT."),
    ]
    lw = 320
    for i, (num, tag, src, art, chip, head, body) in enumerate(leads):
        x0 = MARGIN + i * (lw + 12)
        x1 = x0 + lw
        art(d, x0, 196, x1, 286)
        d.rectangle([x0, 196, x1, 286], outline=BORDER, width=1)
        num_circle(d, x0 + 11, 299, num)
        d.text((x0 + 28, 292), tag, font=sans_b(11), fill=RED)
        sw_ = text_w(d, src, sans(9))
        d.text((x1 - sw_, 293), src, font=sans(9), fill=INK_SOFT)
        hf = serif_b(20)
        hl = wrap_text(d, head, hf, lw - 4)
        draw_lines(d, x0, 312, hl[:2], hf, INK, 22)
        bf = sans(12)
        bl = wrap_text(d, body, bf, lw - 4)
        draw_lines(d, x0, 358, bl[:3], bf, INK_SOFT, 15)

    # ---- 10 picture stories, 5 x 2 ----------------------------------
    pics = [
        (4, "OCEANIA", "Australia says sorry",
         "Formal apology to LGBTQ veterans.", mini_apology,
         "REUTERS", "OFFICIAL"),
        (5, "MID EAST", "Rial at record low",
         "Iran currency plunges as US hits 'shadow economy'.",
         mini_rial, "ARAB NEWS", "REPORTED"),
        (6, "MID EAST", "Saudi budget 2027",
         "Growth forecast despite this year's challenges.",
         mini_budget, "ARAB NEWS", "REPORTED"),
        (7, "AFRICA", "Kenya showdown",
         "Opposition vs IEBC over election credibility.",
         mini_kenya, "DAILY NATION", "REPORTED"),
        (8, "AFRICA", "Tanzania grows 5.9%",
         "Growth holds as IMF presses reform demands.",
         mini_tanzania, "THE CITIZEN", "REPORTED"),
        (9, "EUROPE", "Cancer drug hope",
         "UK pancreatic drug: 90% tumour control.",
         mini_drug, "EAST AFRICAN PRESS", "REPORTED"),
        (10, "OCEANIA", "Bougainville vote on",
         "PNG parliament votes; 89 of 118 MPs needed.",
         mini_bougainville, "THE CONVERSATION", "ONGOING"),
        (11, "EUROPE", "Chess Game 2 today",
         "Gukesh White in Geneva, score 0.5-0.5.",
         mini_chess, "WORLD CHESS", "TODAY"),
        (12, "EUROPE", "UCL tonight: 9 games",
         "Barca at Sabah; Liverpool, Man Utd away.",
         mini_ucl, "UEFA", "TODAY"),
        (13, "AMERICAS", "PCE + GDP day",
         "US inflation + growth due 13:30 GMT.",
         mini_pce, "REUTERS", "TODAY"),
    ]
    pw = 190
    chip_fill = {"OFFICIAL": BLUE, "REPORTED": GREEN, "ONGOING": GREY,
                 "TODAY": NAVY, "CLAIM": RED}
    for i, (num, tag, head, body, art, src, chip) in enumerate(pics):
        col, row = i % 5, i // 5
        x0 = MARGIN + col * (pw + 8)
        y0 = 410 + row * 108
        x1 = x0 + pw
        art(d, x0, y0, x1, y0 + 40)
        d.rectangle([x0, y0, x1, y0 + 40], outline=BORDER, width=1)
        chip_right(d, x1, y0, chip, chip_fill[chip])
        num_circle(d, x0 + 9, y0 + 51, num, r=9)
        d.text((x0 + 22, y0 + 44), tag, font=sans_b(9), fill=RED)
        sw_ = text_w(d, src, sans(8))
        d.text((x1 - sw_, y0 + 45), src, font=sans(8), fill=INK_SOFT)
        hf = sans_b(12)
        hl = wrap_text(d, head, hf, pw - 4)
        draw_lines(d, x0, y0 + 60, hl[:2], hf, INK, 14)
        bf = sans(10)
        bl = wrap_text(d, body, bf, pw - 4)
        draw_lines(d, x0, y0 + 88, bl[:2], bf, INK_SOFT, 12)

    # ---- map + briefs ------------------------------------------------
    d.text((MARGIN, 632), "WHERE IT HAPPENED", font=sans_b(13), fill=RED)
    draw_map(d, MARGIN, 650, MARGIN + 296, 852)
    legend = [
        ((166, 30, 30), "Asia 7"),
        ((31, 78, 121), "Europe 5"),
        ((150, 90, 40), "Mid East 6"),
        ((40, 110, 70), "Americas 6"),
        ((120, 80, 140), "Africa 7"),
        ((30, 120, 130), "Oceania 7"),
    ]
    lx, ly = MARGIN, 858
    for col, label in legend:
        d.rectangle([lx, ly + 2, lx + 10, ly + 12], fill=col)
        d.text((lx + 14, ly), label, font=sans(10), fill=INK)
        lx += 14 + int(text_w(d, label, sans(10))) + 12
        if lx > MARGIN + 260:
            lx = MARGIN
            ly += 16

    d.text((328, 632), "ALSO ON WEDNESDAY 25 NOVEMBER · 28 MORE",
           font=sans_b(13), fill=RED)
    briefs = [
        (14, "Germany", "Q3 GDP due 07:00 GMT"),
        (15, "Australia", "Oct inflation due today"),
        (16, "Bank of England", "Bailey faces MPs today"),
        (17, "Deere", "reports; US shut Thu for Thanksgiving"),
        (18, "US Treasury", "$44bn 7-year auction today"),
        (19, "Trump tariffs", "Section 301 findings due"),
        (20, "ASX", "down 0.4% to 8,692; miners slide"),
        (21, "Metals", "silver $40.79, platinum $1,267.65"),
        (22, "Yen", "dollar at 159.24 yen"),
        (23, "Tokyo chips", "Advantest -12%, JX Metals -8.1%"),
        (24, "Sensex", "reopens 09:15 IST after holiday"),
        (25, "New Zealand", "shares gain at the open"),
        (26, "Kenya", "Vodafone gain from Safaricom deal"),
        (27, "Kenya", "eCitizen cyberattack fears grow"),
        (28, "Uganda", "gold imports climb"),
        (29, "Tanzania", "school-bus safety cameras"),
        (30, "Palestine", "student release demanded"),
        (31, "Israel", "Netanyahu in the spotlight"),
        (32, "Saudi Arabia", "law protecting women"),
        (33, "Jordan", "church attackers held"),
        (34, "Morocco", "Darana Alvarez in Marrakech"),
        (35, "PNG", "2027 budget due Thursday"),
        (36, "Cricket", "Rising Stars semis Thu/Fri"),
        (37, "Hockey", "India women face China today"),
        (38, "India", "JEE Main 2027 sign-ups open"),
        (39, "Film", "Avengers: Doomsday trailer out"),
        (40, "Sport", "Super Bowl LXI live in Imax"),
        (41, "Tech", "OpenAI, Cisco build Shirudo"),
    ]
    for i, (num, place, fact) in enumerate(briefs):
        col, row = i // 14, i % 14
        bx = 328 + col * 344
        by = 650 + row * 18
        d.text((bx, by), f"{num}", font=sans_b(11), fill=RED)
        nw_ = text_w(d, f"{num} ", sans_b(11))
        d.text((bx + nw_, by), place, font=sans_b(11), fill=INK)
        pw_ = text_w(d, place, sans_b(11))
        d.text((bx + nw_ + pw_, by), f": {fact}", font=sans(11),
               fill=INK_SOFT)

    # ---- DATE CHECK --------------------------------------------------
    d.rectangle([MARGIN, 910, W - MARGIN, 1000], outline=RED, width=2)
    d.rectangle([MARGIN, 910, MARGIN + 96, 926], fill=RED)
    d.text((MARGIN + 8, 913), "DATE CHECK", font=sans_b(11),
           fill=(255, 255, 255))
    dc = ("Left out as earlier news (Tue 24 Nov): Houthi strike on "
          "Riyadh tower, 11 hurt · CIA + ODNI breach · CAS restores "
          "Senegal as AFCON champions · Chess Game 1 draw · UCL: "
          "Real Madrid 5-1 PSV, Arsenal 1-1 Dortmund, Man City 2-2 "
          "Napoli · Sooryavanshi 204 off 53 · England beat Australia, "
          "2nd T20I · Quasar Dun Aonghasa · Turkish helicopter crash, "
          "5 dead · Nvidia -6%. Mon 23 Nov: SpaceX/Grok suits filed "
          "· COP31 collapse (Sun 22 Nov). Not yet (drawn Wed "
          "09:00 WIB / 02:00 UTC): German GDP 07:00 GMT · US PCE + "
          "GDP 13:30 GMT · BoE Bailey · Deere · UCL tonight · "
          "Bougainville result. Sources: Reuters, DJN, AP, UEFA, "
          "Arab News, ESA. Maps + drawings are original vector art.")
    lines = wrap_text(d, dc, sans(10), (W - MARGIN) - (MARGIN + 108))
    draw_lines(d, MARGIN + 108, 913, lines[:6], sans(10), INK, 12)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "..", "entry.png")
    img.save(out)
    print(f"Wrote {out} ({os.path.getsize(out)} bytes, 1024x1024)")


if __name__ == "__main__":
    main()
