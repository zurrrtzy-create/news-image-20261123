#!/usr/bin/env python3
"""Render 'The World in One Day - Monday 23 November 2026'.

One 1024x1024 newspaper front page, drawn from scratch with Pillow and
real fonts only (Playfair Display for display type, EB Garamond for body,
both SIL OFL in fonts/). No bitmap or pixel-drawn fonts anywhere.
Deterministic: no randomness, no wall clock, no network.
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(HERE, "fonts")
OUT = os.path.join(HERE, "..", "work", "output", "entry.png")

W, H = 1024, 1024
PAPER = (247, 243, 234)
PANEL = (255, 253, 246)
INK = (26, 26, 26)
MUTED = (90, 86, 76)
NAVY = (20, 38, 74)
NAVY2 = (28, 52, 96)
RED = (176, 42, 42)
RED_DK = (140, 28, 28)
GOLD = (201, 162, 39)
LINE = (200, 192, 172)
BLUE = (31, 78, 121)
TEAL = (18, 92, 96)

_cache = {}


def font(name, size, weight=400):
    """name: 'playfair' | 'garamond' | 'garamond-it'. weight via variable axis."""
    key = (name, size, weight)
    if key in _cache:
        return _cache[key]
    path = {
        "playfair": "PlayfairDisplay.ttf",
        "garamond": "EBGaramond.ttf",
        "garamond-it": "EBGaramond-Italic.ttf",
    }[name]
    f = ImageFont.truetype(os.path.join(FONTS, path), size)
    try:
        f.set_variation_by_axes([weight])
    except Exception:
        pass
    _cache[key] = f
    return f


def text_w(draw, s, f):
    return draw.textlength(s, font=f)


def wrap(draw, s, f, max_w):
    """Greedy word wrap; returns list of lines."""
    words = s.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if text_w(draw, t, f) <= max_w or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def fit_lines(draw, s, f, max_w, max_lines, min_size, name, weight):
    """Shrink font until text fits max_lines; returns (lines, font)."""
    size = f.size
    while size > min_size:
        ff = font(name, size, weight)
        lines = wrap(draw, s, ff, max_w)
        if len(lines) <= max_lines:
            return lines, ff
        size -= 1
    ff = font(name, min_size, weight)
    return wrap(draw, s, ff, max_w), ff


def draw_text(draw, xy, s, f, fill=INK, anchor="la"):
    draw.text(xy, s, font=f, fill=fill, anchor=anchor)


def ruled(draw, x0, x1, y, fill=LINE, width=1):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def hline(draw, x0, x1, y, fill, width=2):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img, "RGBA")

# ---------------------------------------------------------------- masthead
d.rectangle([0, 0, W, 66], fill=NAVY)
d.rectangle([0, 66, W, 69], fill=GOLD)
draw_text(d, (512, 6), "THE WORLD IN ONE DAY", font("playfair", 40, 900),
          fill=(250, 247, 238), anchor="ma")
draw_text(d, (512, 50), "MONDAY  23  NOVEMBER  2026    ·    30 STORIES FROM EVERY REGION",
          font("garamond", 15, 600), fill=(212, 196, 140), anchor="ma")

# ---------------------------------------------------------------- subhead
draw_text(d, (512, 76), "WARSHIP SUNK OFF LIBYA  ·  HUANG BACK AT NVIDIA  ·  IRAN VOWS TO DEFY BLOCKADE",
          font("playfair", 19, 800), fill=RED_DK, anchor="ma")
ruled(d, 16, W - 16, 100)

# ---------------------------------------------------------------- stat strip
stats = "NVDA +31%    ·    NASDAQ +6.5%    ·    S&P 500 +4.7%    ·    KOSPI -3.31%    ·    BITCOIN UNDER $61,000    ·    OIL -3.9%    ·    $43.9BN CYBER DEAL"
draw_text(d, (512, 106), stats, font("garamond", 15, 600), fill=INK, anchor="ma")
ruled(d, 16, W - 16, 126)

# ---------------------------------------------------------------- region bar
regions = "EUROPE          MIDDLE EAST          ASIA          AMERICAS          MARKETS          SCIENCE"
draw_text(d, (512, 131), regions, font("garamond", 13, 600), fill=MUTED, anchor="ma")
ruled(d, 16, W - 16, 148)


# ---------------------------------------------------------------- scenes
def night_sea(x, y, w, h):
    """Dark sea at night: stars, moon halo + craters + reflection, layered waves."""
    d.rectangle([x, y, x + w, y + h], fill=(16, 26, 48))
    # stars
    stars = [(0.06, 0.10, 1), (0.12, 0.22, 2), (0.20, 0.08, 1), (0.28, 0.16, 1),
             (0.36, 0.06, 2), (0.44, 0.20, 1), (0.52, 0.10, 1), (0.58, 0.24, 2),
             (0.66, 0.06, 1), (0.74, 0.16, 1), (0.10, 0.34, 1), (0.46, 0.30, 1),
             (0.90, 0.42, 1), (0.30, 0.30, 2), (0.62, 0.34, 1)]
    for (fx, fy, r) in stars:
        sx, sy = x + w * fx, y + h * fy
        d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(220, 226, 240))
    # moon halo + disc + craters (kept inside the scene box)
    d.ellipse([x + w - 112, y, x + w - 44, y + 52], fill=(232, 228, 200, 26))
    d.ellipse([x + w - 106, y, x + w - 50, y + 46], fill=(232, 228, 200, 40))
    d.ellipse([x + w - 104, y + 2, x + w - 52, y + 42], fill=(232, 228, 200, 46))
    d.ellipse([x + w - 96, y + 6, x + w - 60, y + 34], fill=(240, 236, 210))
    d.ellipse([x + w - 88, y + 12, x + w - 82, y + 18], fill=(214, 210, 184))
    d.ellipse([x + w - 76, y + 22, x + w - 71, y + 27], fill=(214, 210, 184))
    # sea
    d.rectangle([x, y + h * 0.62, x + w, y + h], fill=(24, 44, 74))
    # moonlight reflection column under the moon
    mcx = x + w - 78
    for j in range(6):
        yy = y + h * 0.66 + j * 5
        wd = 26 - j * 2
        d.line([(mcx - wd // 2, yy), (mcx + wd // 2, yy)], fill=(210, 205, 170, 110), width=2)
    for j in range(6):
        yy = y + h * 0.68 + j * 9
        d.line([(x + 8 + j * 6, yy), (x + w - 40 - j * 9, yy)], fill=(90, 120, 160, 120), width=2)
        d.line([(x + 30 + j * 22, yy), (x + 52 + j * 22, yy)], fill=(170, 195, 225, 90), width=1)


def explosion(cx, cy, s):
    """Orange blast: glow halo, fireball, drifting smoke plume, sparks, water reflection."""
    d.ellipse([cx - s * 1.25, cy - s * 1.25, cx + s * 1.25, cy + s * 1.25],
              fill=(255, 140, 40, 60))
    # smoke plume rising and drifting left
    for (ox, oy, r, c) in [(-s * 0.55, -s * 0.28, s * 0.34, (120, 120, 120)),
                           (s * 0.5, -s * 0.42, s * 0.30, (105, 105, 105)),
                           (0, -s * 0.62, s * 0.26, (135, 135, 135)),
                           (-s * 0.9, -s * 0.75, s * 0.30, (100, 100, 100)),
                           (-s * 1.25, -s * 1.05, s * 0.24, (88, 88, 88)),
                           (s * 0.85, -s * 0.85, s * 0.22, (118, 118, 118))]:
        d.ellipse([cx + ox - r, cy + oy - r, cx + ox + r, cy + oy + r], fill=c + (215,))
    # fireball layers
    for (r, c) in [(s * 0.62, (235, 120, 30)), (s * 0.45, (245, 170, 60)),
                   (s * 0.28, (255, 220, 120)), (s * 0.14, (255, 244, 190))]:
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=c)
    # sparks
    sparks = [(-1.5, -0.4), (-1.1, 0.9), (-0.6, -1.5), (0.3, -1.7), (1.2, -1.2),
              (1.6, 0.2), (1.3, 1.0), (0.5, 1.5), (-0.9, 1.3), (-1.7, 0.6)]
    for (fx, fy) in sparks:
        sx, sy = cx + fx * s, cy + fy * s
        d.ellipse([sx - 1, sy - 1, sx + 1, sy + 1], fill=(255, 200, 90))
    # orange reflection smear on the water below
    d.ellipse([cx - s * 0.9, cy + s * 1.1, cx + s * 0.9, cy + s * 1.7], fill=(235, 130, 40, 90))


def warship(x, y, w, h, color=(12, 14, 20)):
    """Warship silhouette: hull, deck structures, masts, funnel, gun, portholes."""
    # hull: sloped bow, flat deck, stern
    d.polygon([(x, y + h * 0.55), (x + w, y + h * 0.55), (x + w * 0.86, y + h),
               (x + w * 0.12, y + h)], fill=color)
    # waterline stripe + portholes
    d.line([(x + w * 0.14, y + h * 0.82), (x + w * 0.84, y + h * 0.82)],
           fill=(70, 78, 88), width=1)
    for i in range(7):
        px = x + w * (0.20 + i * 0.10)
        d.ellipse([px - 1, y + h * 0.66 - 1, px + 1, y + h * 0.66 + 1], fill=(150, 165, 185))
    # bow gun turret + barrel
    d.rectangle([x + w * 0.08, y + h * 0.42, x + w * 0.24, y + h * 0.55], fill=color)
    d.line([(x + w * 0.24, y + h * 0.46), (x + w * 0.38, y + h * 0.40)], fill=color, width=3)
    # superstructure blocks
    d.rectangle([x + w * 0.30, y + h * 0.30, x + w * 0.62, y + h * 0.55], fill=color)
    d.rectangle([x + w * 0.36, y + h * 0.16, x + w * 0.56, y + h * 0.30], fill=color)
    # bridge windows (lit)
    for i in range(4):
        wx = x + w * (0.39 + i * 0.05)
        d.rectangle([wx, y + h * 0.20, wx + 3, y + h * 0.26], fill=(255, 214, 120))
    # funnel with smoke
    d.rectangle([x + w * 0.64, y + h * 0.24, x + w * 0.72, y + h * 0.55], fill=color)
    d.ellipse([x + w * 0.66, y + h * 0.10, x + w * 0.72, y + h * 0.22], fill=(90, 90, 90, 200))
    d.ellipse([x + w * 0.68, y + h * 0.02, x + w * 0.73, y + h * 0.12], fill=(80, 80, 80, 170))
    # main mast + yard + radar bar
    d.rectangle([x + w * 0.46, y + h * 0.02, x + w * 0.50, y + h * 0.32], fill=color)
    d.line([(x + w * 0.42, y + h * 0.10), (x + w * 0.54, y + h * 0.10)], fill=color, width=2)
    d.line([(x + w * 0.44, y + h * 0.04), (x + w * 0.56, y + h * 0.06)], fill=color, width=2)
    # stern mast + antenna line to bow mast
    d.line([(x + w * 0.50, y + h * 0.02), (x + w * 0.72, y + h * 0.16)], fill=color, width=2)
    d.rectangle([x + w * 0.78, y + h * 0.30, x + w * 0.81, y + h * 0.55], fill=color)


def helicopter(x, y, s):
    """Ka-27 silhouette: body, tail boom, main + tail rotors, nav light."""
    # main rotor (slight motion blur: two offset lines)
    d.line([(x, y + 2), (x + s, y + 2)], fill=(30, 34, 42), width=2)
    d.line([(x + 2, y + 4), (x + s - 2, y + 4)], fill=(30, 34, 42, 140), width=1)
    # mast + body
    d.line([(x + s * 0.48, y + 2), (x + s * 0.48, y + 8)], fill=(30, 34, 42), width=2)
    d.ellipse([x + s * 0.18, y + 8, x + s * 0.62, y + 20], fill=(30, 34, 42))
    # tail boom + fin + tail rotor
    d.polygon([(x + s * 0.58, y + 11), (x + s * 0.98, y + 8), (x + s * 0.98, y + 13),
               (x + s * 0.60, y + 16)], fill=(30, 34, 42))
    d.line([(x + s * 0.94, y + 2), (x + s * 0.94, y + 16)], fill=(30, 34, 42), width=1)
    # cockpit glint + red nav light
    d.ellipse([x + s * 0.20, y + 10, x + s * 0.28, y + 15], fill=(140, 170, 200))
    d.ellipse([x + s * 0.60, y + 17, x + s * 0.63, y + 20], fill=(255, 60, 50))


def drone_boat(x, y, s):
    d.polygon([(x, y), (x + s, y + s * 0.22), (x + s * 0.82, y + s * 0.5),
               (x + s * 0.12, y + s * 0.5)], fill=(200, 205, 210))
    d.line([(x + s * 0.1, y + s * 0.62), (x + s * 0.9, y + s * 0.62)],
           fill=(200, 210, 225, 160), width=2)
    d.line([(x, y + s * 0.78), (x + s, y + s * 0.78)], fill=(200, 210, 225, 110), width=2)


def chip_scene(x, y, w, h):
    """Trading screen: detailed chip die with pins/traces, candlestick chart."""
    d.rectangle([x, y, x + w, y + h], fill=(10, 26, 18))
    # board grid
    for gy in range(y + 12, y + h, 22):
        d.line([(x, gy), (x + w, gy)], fill=(24, 66, 44, 140), width=1)
    for gx in range(x + 14, x + w, 26):
        d.line([(gx, y), (gx, y + h)], fill=(24, 66, 44, 110), width=1)
    cx, cy, s = x + w * 0.30, y + h * 0.48, 40
    # chip glow + circuit traces fanning out
    d.ellipse([cx - s - 16, cy - s - 16, cx + s + 16, cy + s + 16], fill=(60, 180, 110, 26))
    for (tx, ty, dx, dy) in [(cx - s - 8, cy - 26, -26, -18), (cx - s - 8, cy + 20, -30, 14),
                             (cx + s + 8, cy - 30, 30, -20), (cx + s + 8, cy + 26, 34, 10)]:
        d.line([(tx, ty), (tx + dx, ty), (tx + dx, ty + dy)], fill=(90, 200, 140, 160), width=1)
        d.ellipse([tx + dx - 2, ty + dy - 2, tx + dx + 2, ty + dy + 2], fill=(120, 230, 160))
    # chip package + die
    d.rectangle([cx - s, cy - s, cx + s, cy + s], fill=(16, 84, 48),
                outline=(90, 200, 140), width=2)
    d.rectangle([cx - s * 0.55, cy - s * 0.55, cx + s * 0.55, cy + s * 0.55],
                fill=(22, 110, 62), outline=(140, 230, 170), width=1)
    # transistor blocks on the die
    for i in range(4):
        for j in range(4):
            bx0 = cx - s * 0.44 + i * s * 0.24
            by0 = cy - s * 0.44 + j * s * 0.24
            d.rectangle([bx0, by0, bx0 + s * 0.16, by0 + s * 0.16],
                        fill=(30, 140, 80), outline=(90, 200, 140), width=1)
    # pin-1 marker dot
    d.ellipse([cx - s + 4, cy - s + 4, cx - s + 9, cy - s + 9], fill=(255, 220, 120))
    # pins on all four sides
    for i in range(-2, 3):
        d.line([(cx + i * 18, cy - s), (cx + i * 18, cy - s - 8)], fill=(90, 200, 140), width=3)
        d.line([(cx + i * 18, cy + s), (cx + i * 18, cy + s + 8)], fill=(90, 200, 140), width=3)
        d.line([(cx - s, cy + i * 18), (cx - s - 8, cy + i * 18)], fill=(90, 200, 140), width=3)
        d.line([(cx + s, cy + i * 18), (cx + s + 8, cy + i * 18)], fill=(90, 200, 140), width=3)
    # candlestick chart with axis ticks
    base = y + h * 0.86
    top = y + h * 0.18
    for k in range(5):
        gy = base - k * (base - top) / 4
        d.line([(x + w * 0.52, gy), (x + w * 0.98, gy)], fill=(24, 66, 44, 180), width=1)
        d.line([(x + w * 0.98, gy), (x + w * 0.98 + 4, gy)], fill=(120, 230, 160), width=1)
    d.line([(x + w * 0.52, base), (x + w * 0.98, base)], fill=(90, 200, 140, 200), width=1)
    candles = [(0.55, 0.78, 0.62, 1), (0.60, 0.66, 0.58, 1), (0.65, 0.72, 0.64, 0),
               (0.70, 0.58, 0.50, 1), (0.75, 0.64, 0.56, 0), (0.80, 0.46, 0.40, 1),
               (0.85, 0.52, 0.44, 0), (0.90, 0.30, 0.22, 1)]
    for (fx, o, c, up) in candles:
        px = x + w * fx
        oy = base - o * (base - top)
        cy2 = base - c * (base - top)
        lo = min(oy, cy2) - 6
        hi = max(oy, cy2) + 6
        col = (120, 230, 160) if up else (235, 90, 70)
        d.line([(px, lo), (px, hi)], fill=col, width=1)
        d.rectangle([px - 5, min(oy, cy2), px + 5, max(oy, cy2)], fill=col)
    pts = [(x + w * 0.52, y + h * 0.86), (x + w * 0.64, y + h * 0.70),
           (x + w * 0.72, y + h * 0.76), (x + w * 0.86, y + h * 0.42),
           (x + w * 0.97, y + h * 0.18)]
    d.line(pts, fill=(120, 230, 160), width=4)
    d.polygon([(x + w * 0.97, y + h * 0.18), (x + w * 0.88, y + h * 0.20),
               (x + w * 0.94, y + h * 0.30)], fill=(120, 230, 160))


def tanker_scene(x, y, w, h):
    """Dusk strait: sun glare + reflection, tanker with containers/pipes/rivets, warship."""
    for i in range(h):
        t = i / max(h - 1, 1)
        r = int(64 + (214 - 64) * t)
        g = int(52 + (120 - 52) * t)
        b = int(74 + (60 - 74) * t)
        d.line([(x, y + i), (x + w, y + i)], fill=(r, g, b))
    # thin clouds
    for (cy0, cw0, cx0) in [(0.16, 0.34, 0.05), (0.24, 0.26, 0.44), (0.10, 0.20, 0.30)]:
        cy1 = y + h * cy0
        d.line([(x + w * cx0, cy1), (x + w * (cx0 + cw0), cy1)], fill=(255, 200, 150, 70), width=2)
    # sun halo + disc
    d.ellipse([x + w * 0.64, y + h * 0.02, x + w * 0.90, y + h * 0.40], fill=(255, 214, 140, 60))
    d.ellipse([x + w * 0.68, y + h * 0.08, x + w * 0.86, y + h * 0.34], fill=(255, 214, 140))
    d.ellipse([x + w * 0.72, y + h * 0.13, x + w * 0.82, y + h * 0.29], fill=(255, 232, 180))
    # sea
    d.rectangle([x, y + h * 0.66, x + w, y + h], fill=(28, 52, 78))
    # sun reflection column on the water
    scx = x + w * 0.77
    for j in range(6):
        yy = y + h * 0.70 + j * 5
        wd = 30 - j * 3
        d.line([(scx - wd // 2, yy), (scx + wd // 2, yy)], fill=(255, 190, 110, 120), width=2)
    for j in range(3):
        yy = y + h * 0.72 + j * 10
        d.line([(x + 10 + j * 8, yy), (x + w - 30 - j * 10, yy)], fill=(110, 140, 175, 130), width=2)
        d.line([(x + 40 + j * 30, yy + 4), (x + 66 + j * 30, yy + 4)], fill=(170, 195, 225, 90), width=1)
    # tanker hull with deck pipes and valves
    hx, hy, hw, hh = x + w * 0.06, y + h * 0.52, w * 0.58, h * 0.20
    # accommodation block + funnel at the stern
    d.rectangle([hx + hw * 0.02, hy - h * 0.14, hx + hw * 0.16, hy], fill=(214, 210, 198))
    for i in range(3):
        wx = hx + hw * (0.05 + i * 0.045)
        d.rectangle([wx, hy - h * 0.11, wx + 4, hy - h * 0.07], fill=(40, 60, 90))
    d.rectangle([hx + hw * 0.17, hy - h * 0.12, hx + hw * 0.24, hy], fill=(150, 60, 45))
    d.rectangle([hx + hw * 0.17, hy - h * 0.12, hx + hw * 0.24, hy - h * 0.09], fill=(30, 30, 34))
    # hull
    d.polygon([(hx, hy), (hx + hw, hy), (hx + hw * 0.94, hy + hh), (hx + hw * 0.06, hy + hh)],
              fill=(20, 22, 28))
    # waterline stripe + rivets
    d.line([(hx + hw * 0.06, hy + hh * 0.78), (hx + hw * 0.94, hy + hh * 0.78)],
           fill=(150, 70, 55), width=2)
    for i in range(9):
        px = hx + hw * (0.12 + i * 0.09)
        d.ellipse([px - 1, hy + hh * 0.45 - 1, px + 1, hy + hh * 0.45 + 1], fill=(90, 95, 105))
    # deck pipes + red valves
    for i in range(3):
        px = hx + hw * (0.28 + i * 0.14)
        d.rectangle([px, hy - h * 0.07, px + 5, hy], fill=(120, 120, 125))
        d.ellipse([px - 2, hy - h * 0.10, px + 8, hy - h * 0.06], fill=(170, 60, 50))
    # container stacks toward the bow
    for (ci, col) in [(0, (150, 80, 55)), (1, (40, 110, 105))]:
        cx0 = hx + hw * (0.72 + ci * 0.12)
        for lvl in range(2):
            cy0 = hy - h * 0.07 - lvl * 9
            d.rectangle([cx0, cy0, cx0 + 22, cy0 + 8], fill=col, outline=(20, 22, 28), width=1)
            for rib in range(1, 4):
                d.line([(cx0 + rib * 5, cy0), (cx0 + rib * 5, cy0 + 8)], fill=(0, 0, 0, 60), width=1)
    # bow wave + wake
    d.arc([hx + hw * 0.90, hy + hh - 4, hx + hw + 16, hy + hh + 8], 200, 340, fill=(220, 235, 245, 200), width=2)
    for j in range(3):
        yy = hy + hh + 2 + j * 4
        d.line([(hx - 6 - j * 3, yy), (hx + hw * 0.10, yy)], fill=(200, 220, 240, 110), width=1)
    # grey warship at right with mast, radar, bridge windows
    wx = x + w * 0.72
    d.polygon([(wx, y + h * 0.60), (wx + w * 0.24, y + h * 0.60),
               (wx + w * 0.21, y + h * 0.74), (wx + w * 0.03, y + h * 0.74)],
              fill=(58, 62, 70))
    d.rectangle([wx + w * 0.08, y + h * 0.48, wx + w * 0.16, y + h * 0.60], fill=(58, 62, 70))
    for i in range(3):
        wxx = wx + w * (0.095 + i * 0.02)
        d.rectangle([wxx, y + h * 0.51, wxx + 2, y + h * 0.55], fill=(200, 210, 220))
    d.rectangle([wx + w * 0.11, y + h * 0.38, wx + w * 0.13, y + h * 0.48], fill=(58, 62, 70))
    d.line([(wx + w * 0.09, y + h * 0.40), (wx + w * 0.15, y + h * 0.40)], fill=(58, 62, 70), width=2)
    # distant radar arcs above the warship mast
    for r in (12, 18, 24):
        d.arc([wx + w * 0.12 - r, y + h * 0.38 - r, wx + w * 0.12 + r, y + h * 0.38 + r],
              200, 340, fill=(200, 210, 220, 150), width=1)

# ---------------------------------------------------------------- big stories
BIG = [
    ("LIBYA  ·  7 SEA DRONES", "RUSSIAN WARSHIP SUNK",
     "Zelenskyy confirms Monday: seven sea drones sank the corvette Merkury "
     "at Benghazi; a Ka-27 helicopter was destroyed and the cargo ship Angara hit.",
     "merkury"),
    ("NVIDIA  ·  +31% IN A DAY", "HUANG IS BACK AT NVIDIA",
     "Board reinstates Jensen Huang as CEO 11 days after his ouster; shares "
     "soar 31% - the biggest gain since 2003 - and lift the Nasdaq 6.5%.",
     "nvidia"),
    ("GULF  ·  BLOCKADE", "IRAN VOWS TO DEFY BLOCKADE",
     "Tehran says it will use \u201call means\u201d as 31 laden tankers mass beyond "
     "Hormuz; Trump warns any ship that tests the blockade ends \u201cat the "
     "bottom of the sea\u201d.",
     "iran"),
]
bx = [16, 349, 682]
for i, (kick, head, body, kind) in enumerate(BIG):
    x = bx[i]
    d.rectangle([x, 148, x + 325, 358], fill=PANEL, outline=LINE, width=1)
    if kind == "merkury":
        night_sea(x + 1, 149, 323, 98)
        helicopter(x + 34, 149 + 12, 46)
        warship(x + 60, 149 + 54, 150, 36)
        explosion(x + 195, 149 + 44, 14)
        drone_boat(x + 30, 149 + 80, 34)
        drone_boat(x + 250, 149 + 84, 28)
    elif kind == "nvidia":
        chip_scene(x + 1, 149, 323, 98)
    else:
        tanker_scene(x + 1, 149, 323, 98)
    draw_text(d, (x + 162, 250), kick, font("garamond", 13, 700), fill=RED_DK, anchor="ma")
    hl, hf = fit_lines(d, head, font("playfair", 21, 800), 305, 1, 18, "playfair", 800)
    yy = 266
    for ln in hl:
        draw_text(d, (x + 162, yy), ln, hf, fill=INK, anchor="ma")
        yy += hf.size + 2
    bl = wrap(d, body, font("garamond", 13, 400), 305)
    yy = 266 + len(hl) * (hf.size + 2) + 2
    for ln in bl[:3]:
        draw_text(d, (x + 162, yy), ln, font("garamond", 13, 400), fill=(50, 48, 44), anchor="ma")
        yy += 16

# ---------------------------------------------------------------- numbered stories
NUMBERED = [
    (4, "DYMER TOLL RISES TO 11",
     "Search ends after a Russian drone hit a five-storey block; Kyiv region in mourning.",
     (50.8, 30.3)),
    (5, "NATO MEETS ON POLAND MISSILES",
     "Emergency council in Brussels; AWACS aircraft to deploy after 3 Russian Kh-101s confirmed.",
     (50.3, 22.5)),
    (6, "CROWDSTRIKE BUYS ZSCALER",
     "$43.9bn all-stock deal, the biggest cybersecurity takeover on record.",
     (30.3, -97.7)),
    (7, "KOSPI FALLS 3.31%",
     "AI rout drags Seoul to its lowest since January; stabilisation fund readied.",
     (37.6, 127.0)),
    (8, "UNRWA WORKER KILLED IN GAZA",
     "Israeli strike in Jabalia kills Adel al-Helo at a water well; 3 dead in all.",
     (31.5, 34.5)),
    (9, "UKRAINE HITS PERM REFINERY",
     "Drones strike a Lukoil plant 1,500 km inside Russia; 1 killed, 2 hurt.",
     (58.0, 56.3)),
    (10, "DELTA OUTAGE DRAGS ON",
     "92 more flights cancelled Monday after 2,190 were delayed on Sunday.",
     (33.7, -84.4)),
    (11, "FACTORY FIRE: 24 DEAD",
     "Toll confirmed in Banten, Indonesia; about 30 still missing.",
     (-6.2, 106.3)),
    (12, "INDIA GIVES NEPAL $1.62BN",
     "Flood-rebuilding package agreed as PM Shah visits New Delhi.",
     (28.6, 77.2)),
    (13, "NHS STARTS AI CANCER TRIAL",
     "World\u2019s largest AI breast-screening trial: 700,000 women, 30 sites.",
     (52.2, 0.1)),
    (14, "COP31 AFTERMATH",
     "Erdo\u011fan: failed summit laid groundwork for the next round of talks.",
     (36.9, 30.7)),
    (15, "ANTHROPIC SLIPS 1.4%",
     "Shares fall as the Nasdaq soars, days after its record $81bn IPO.",
     (37.8, -122.4)),
    (16, "JAPAN SHUT, TAIEX UP 2.16%",
     "Tokyo closed for a holiday as Taiwan rebounds from the AI sell-off.",
     (35.7, 139.7)),
    (17, "TRUMP CURBS CONGRESS",
     "Order limits how lawmakers can seek information from federal agencies.",
     (38.9, -77.0)),
    (18, "SKUBAL\u2019S $450M METS DEAL",
     "Nine years, the largest contract ever for a pitcher.",
     (40.7, -74.0)),
]
for idx, (num, head, body, _ll) in enumerate(NUMBERED):
    col, row = idx % 3, idx // 3
    x = 16 + col * 333
    y = 366 + row * 62
    if row:
        ruled(d, x, x + 325, y - 1)
    d.ellipse([x, y + 2, x + 22, y + 24], fill=RED)
    draw_text(d, (x + 11, y + 4), str(num), font("garamond", 13, 700),
              fill=(255, 255, 255), anchor="ma")
    draw_text(d, (x + 30, y + 1), head, font("garamond", 16, 600), fill=INK, anchor="la")
    bl = wrap(d, body, font("garamond", 13, 400), 295)
    yy = y + 21
    for ln in bl[:2]:
        draw_text(d, (x + 30, yy), ln, font("garamond", 13, 400), fill=(50, 48, 44), anchor="la")
        yy += 16

# ---------------------------------------------------------------- also
ALSO = [
    "Bitcoin slides under $61,000 as the AI rout spreads",
    "Seoul readies a ~KRW 10 trillion market stabilisation fund",
    "Won weakens to 1,345.9 per dollar",
    "SK Telecom -7.32% after the Anthropic listing",
    "Zscaler +20%, CrowdStrike -7% on the deal",
    "Nvidia reclaims No. 2 spot behind Apple",
    "Dow jumps 1,448 points (+3%)",
    "Oil falls: WTI -3.9% to $80.20 a barrel",
    "Vance worked the weekend to bring Huang back",
    "Trump traded up to $98m of Nvidia shares",
    "15 Anthropic-linked ETFs begin trading",
    "Tom Jackson, ex-Bronco and ESPN analyst, dies at 75",
]
ruled(d, 16, W - 16, 682)
draw_text(d, (16, 688), "ALSO ON MONDAY", font("garamond", 13, 700), fill=NAVY, anchor="la")
for i, item in enumerate(ALSO):
    col, row = i % 3, i // 3
    x = 16 + col * 333
    y = 708 + row * 15
    d.ellipse([x, y + 4, x + 5, y + 9], fill=RED)
    draw_text(d, (x + 10, y), item, font("garamond", 12, 400), fill=(50, 48, 44), anchor="la")

# ---------------------------------------------------------------- timeline (UTC)
ruled(d, 16, W - 16, 772)
draw_text(d, (16, 778), "MONDAY IN UTC", font("garamond", 13, 700), fill=NAVY, anchor="la")
TL = [
    ("05:23", "Dymer toll reaches 11"),
    ("06:30", "Kospi closes -3.31%"),
    ("11:00", "CrowdStrike buys Zscaler, $43.9bn"),
    ("14:00", "Nvidia brings Huang back"),
    ("15:42", "UNRWA worker killed in Gaza"),
    ("21:00", "Wall Street closes: Nasdaq +6.5%"),
]
tx0, tw = 150, 142
for i, (t, label) in enumerate(TL):
    x = tx0 + i * tw
    d.ellipse([x, 782, x + 7, 789], fill=RED)
    draw_text(d, (x + 12, 778), t, font("garamond", 13, 700), fill=INK, anchor="la")
    ll = wrap(d, label, font("garamond", 12, 400), tw - 14)
    yy = 794
    for ln in ll[:2]:
        draw_text(d, (x + 12, yy), ln, font("garamond", 12, 400), fill=(50, 48, 44), anchor="la")
        yy += 14

# ---------------------------------------------------------------- dotted world map + pins
MAP_X, MAP_Y, MAP_W, MAP_H = 16, 830, 624, 132
BLOBS = [  # (lon, lat, rx, ry) rough continent blobs
    (-100, 48, 28, 14), (-88, 32, 16, 9), (-122, 40, 8, 10), (-152, 64, 14, 7),
    (-42, 73, 8, 6), (-60, -12, 12, 16), (-70, -35, 6, 10),
    (12, 52, 14, 8), (22, 60, 10, 7), (-2, 40, 7, 5), (-2, 54, 3, 4),
    (15, 5, 18, 16), (30, -20, 10, 12),
    (80, 55, 35, 14), (105, 35, 18, 12), (78, 22, 10, 10), (102, 15, 8, 8),
    (139, 37, 7, 8), (115, -2, 16, 5), (134, -25, 14, 8),
]


def to_xy(lat, lon):
    return (MAP_X + (lon + 170) / 360.0 * MAP_W,
            MAP_Y + (75 - lat) / 130.0 * MAP_H)


d.rectangle([MAP_X, MAP_Y, MAP_X + MAP_W, MAP_Y + MAP_H], fill=(232, 238, 244),
            outline=LINE, width=1)
step = 5
gx = MAP_X + 3
while gx < MAP_X + MAP_W - 2:
    gy = MAP_Y + 3
    while gy < MAP_Y + MAP_H - 2:
        lon = (gx - MAP_X) / MAP_W * 360 - 170
        lat = 75 - (gy - MAP_Y) / MAP_H * 130
        land = False
        for (clon, clat, rx, ry) in BLOBS:
            if ((lon - clon) / rx) ** 2 + ((lat - clat) / ry) ** 2 <= 1:
                land = True
                break
        if land:
            d.ellipse([gx - 1, gy - 1, gx + 1, gy + 1], fill=(120, 140, 165))
        gy += step
    gx += step
draw_text(d, (MAP_X + 6, MAP_Y + 4), "WHERE IT HAPPENED", font("garamond", 12, 700),
          fill=NAVY, anchor="la")
for (num, _h, _b, ll) in NUMBERED:
    px, py = to_xy(*ll)
    d.ellipse([px - 7, py - 7, px + 7, py + 7], fill=RED, outline=(255, 255, 255), width=1)
    draw_text(d, (px, py - 6), str(num), font("garamond", 9, 700),
              fill=(255, 255, 255), anchor="ma")

# ---------------------------------------------------------------- date check
DC_X, DC_Y, DC_W, DC_H = 648, 830, 360, 132
d.rectangle([DC_X, DC_Y, DC_X + DC_W, DC_Y + DC_H], fill=PANEL, outline=NAVY, width=2)
d.rectangle([DC_X, DC_Y, DC_X + DC_W, DC_Y + 20], fill=NAVY)
draw_text(d, (DC_X + 10, DC_Y + 3), "DATE CHECK \u2014 NOT 23 NOVEMBER",
          font("garamond", 12, 700), fill=(255, 255, 255), anchor="la")
DC = [
    "COP31 collapses, no deal \u2014 Sun 22 Nov",
    "EU\u2013Indonesia trade deal signed \u2014 Sat 21 Nov",
    "BepiColombo enters Mercury orbit \u2014 Sat 21 Nov",
    "Anthropic\u2019s record $81bn IPO \u2014 trading from Thu 19 Nov",
    "Riemann proof claimed with AI help \u2014 Fri 20 Nov",
    "\u2018El Chapo Isidro\u2019 captured \u2014 Fri 20 Nov",
    "Nigeria boat capsizes, 24 dead \u2014 Fri 20 Nov",
    "Miley Cyrus weds Maxx Morando \u2014 Sat 21 Nov",
]
yy = DC_Y + 24
for item in DC:
    draw_text(d, (DC_X + 10, yy), item, font("garamond", 12, 400), fill=(50, 48, 44), anchor="la")
    yy += 13.5

# ---------------------------------------------------------------- footer
ruled(d, 16, W - 16, 970)
draw_text(d, (16, 975),
          "Sources: Reuters  ·  CNN  ·  Wall Street Journal  ·  AP  ·  Korea JoongAng Daily  ·  NIHR  ·  NHS England  ·  UNRWA  ·  BusinessWire  ·  Morningstar",
          font("garamond", 11, 400), fill=MUTED, anchor="la")
draw_text(d, (16, 990),
          "\u25cf confirmed by two or more outlets      \u25cb reported / single source      ·      All 30 stories dated Monday 23 November 2026.",
          font("garamond", 11, 400), fill=MUTED, anchor="la")
draw_text(d, (16, 1005),
          "Drawn with real fonts \u2014 Playfair Display + EB Garamond (SIL OFL). No AI-drawn text.",
          font("garamond", 11, 400), fill=MUTED, anchor="la")

os.makedirs(os.path.dirname(OUT), exist_ok=True)
img.save(OUT, "PNG")
print("saved", OUT, os.path.getsize(OUT), "bytes")
