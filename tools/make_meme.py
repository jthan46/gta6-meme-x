#!/usr/bin/env python3
"""Draw the gta6-meme-x-01 entry meme with PIL.

Scene: a Vice City / Leonida sunset (neon gradient sky, synthwave sun,
skyline and palm silhouettes). In front of a TV showing "GTA VI", the
make.fun ghost sits on a couch: white body, thick black outline, two black
four-pointed sparkle eyes, a small round hand on a game controller, and its
magenta coin with a white star held up in the other hand.

Captions (exactly two lines of text, huge and high-contrast):
  top:    WAITED 13 YEARS. TOOK THE DAY OFF.
  bottom: MY AI AGENT ALREADY GOT PAID ON make.fun

Output: ../meme.png, 1024x1024.
"""

import math
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
OUT = Path(__file__).resolve().parent.parent / "meme.png"

CONDENSED_BOLD = "/usr/share/fonts/truetype/noto/NotoSans-ExtraCondensedBold.ttf"
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
MAGENTA = (230, 0, 126)
SILHOUETTE = (20, 8, 46)

# ---------------------------------------------------------------- sky / sun

STOPS = [
    (0.00, (38, 13, 82)),
    (0.32, (110, 25, 108)),
    (0.55, (199, 44, 110)),
    (0.72, (255, 94, 98)),
    (0.86, (255, 154, 61)),
    (1.00, (255, 178, 84)),
]


def sky_color(y):
    """Gradient colour at canvas row y (0..H)."""
    t = y / H
    for (t0, c0), (t1, c1) in zip(STOPS, STOPS[1:]):
        if t0 <= t <= t1:
            f = 0 if t1 == t0 else (t - t0) / (t1 - t0)
            return tuple(round(c0[i] + (c1[i] - c0[i]) * f) for i in range(3))
    return STOPS[-1][1]


def draw_sky(img):
    d = ImageDraw.Draw(img)
    for y in range(H):
        d.line([(0, y), (W, y)], fill=sky_color(y))
    # a few small stars in the upper sky
    rng = random.Random(20261119)
    for _ in range(46):
        x = rng.randrange(10, W - 10)
        y = rng.randrange(150, 430)
        r = rng.choice([1, 1, 2])
        d.ellipse([x - r, y - r, x + r, y + r], fill=(255, 240, 250))


def draw_sun(d):
    cx, cy, r = 235, 330, 118
    # glow
    d.ellipse([cx - r - 26, cy - r - 26, cx + r + 26, cy + r + 26], fill=(255, 120, 90))
    # disc, shaded from yellow at the top to orange at the bottom
    for i in range(2 * r):
        f = i / (2 * r)
        col = tuple(
            round(a + (b - a) * f)
            for a, b in zip((255, 214, 90), (255, 110, 60))
        )
        y = cy - r + i
        half = int(math.sqrt(max(r * r - (i - r) ** 2, 0)))
        d.line([(cx - half, y), (cx + half, y)], fill=col)
    # synthwave cuts across the lower half, in the sky colour of each row
    for y, h in [(352, 5), (380, 8), (412, 11), (448, 15)]:
        d.rectangle([cx - r - 2, y, cx + r + 2, y + h], fill=sky_color(y))


# ------------------------------------------------------------------- scene

def draw_skyline(d):
    base = 660
    buildings = [
        (0, 130, 90), (85, 200, 65), (150, 95, 120), (215, 165, 80),
        (290, 120, 100), (355, 210, 70), (425, 105, 110), (490, 180, 75),
        (560, 130, 95), (630, 195, 68), (700, 110, 105), (770, 170, 78),
        (845, 125, 92), (915, 185, 72), (985, 140, 60),
    ]
    rng = random.Random(7)
    for x, top, w in buildings:
        d.rectangle([x, base - top, x + w, base], fill=SILHOUETTE)
        for _ in range(7):  # lit windows
            wx = rng.randrange(x + 8, x + w - 12)
            wy = rng.randrange(base - top + 10, base - 16)
            if rng.random() < 0.6:
                d.rectangle([wx, wy, wx + 5, wy + 7], fill=(255, 215, 106))


def palm(d, base_x, base_y, top_x, top_y, scale=1.0, flip=1):
    """A palm silhouette: curved trunk plus drooping fronds."""
    steps = 24
    pts = []
    for i in range(steps + 1):
        t = i / steps
        # quadratic bezier, control point pulled sideways for the curve
        cxp, cyp = base_x + flip * 46 * scale, (base_y + top_y) / 2
        x = (1 - t) ** 2 * base_x + 2 * (1 - t) * t * cxp + t * t * top_x
        y = (1 - t) ** 2 * base_y + 2 * (1 - t) * t * cyp + t * t * top_y
        pts.append((x, y))
    d.line(pts, fill=SILHOUETTE, width=max(6, int(15 * scale)))
    d.ellipse([top_x - 10 * scale, top_y - 4, top_x + 10 * scale, top_y + 14 * scale],
              fill=SILHOUETTE)  # coconuts
    for ang, ln in [(-165, 120), (-125, 135), (-85, 125), (-45, 135), (-8, 118), (28, 95)]:
        rad = math.radians(ang)
        ex = top_x + flip * math.cos(rad) * ln * scale
        ey = top_y + math.sin(rad) * ln * scale * 0.45 + 58 * scale
        cxp = top_x + flip * math.cos(rad) * ln * scale * 0.5
        cyp = top_y + math.sin(rad) * ln * scale * 0.3 - 26 * scale
        frond = []
        for i in range(17):
            t = i / 16
            x = (1 - t) ** 2 * top_x + 2 * (1 - t) * t * cxp + t * t * ex
            y = (1 - t) ** 2 * top_y + 2 * (1 - t) * t * cyp + t * t * ey
            frond.append((x, y))
        d.line(frond, fill=SILHOUETTE, width=max(4, int(8 * scale)))


def draw_tv(d):
    # stand
    d.rectangle([168, 728, 214, 772], fill=(10, 10, 18))
    d.rectangle([108, 772, 274, 788], fill=(10, 10, 18))
    # frame
    d.rounded_rectangle([36, 468, 334, 732], radius=18, fill=(12, 12, 22),
                        outline=BLACK, width=6)
    # screen: its own little sunset
    sx0, sy0, sx1, sy1 = 54, 486, 316, 714
    for i in range(sy1 - sy0):
        f = i / (sy1 - sy0)
        col = tuple(round(a + (b - a) * f)
                    for a, b in zip((64, 20, 110), (255, 130, 70)))
        d.line([(sx0, sy0 + i), (sx1, sy0 + i)], fill=col)
    d.ellipse([150, 540, 220, 610], fill=(255, 190, 80))  # screen sun
    d.rectangle([sx0, 668, sx1, sy1], fill=(24, 10, 48))  # screen skyline band
    palm(d, 292, 672, 268, 606, scale=0.42, flip=-1)
    font = ImageFont.truetype(CONDENSED_BOLD, 54)
    d.text(((sx0 + sx1) / 2, 522), "GTA VI", font=font, fill=WHITE,
           anchor="mm", stroke_width=3, stroke_fill=BLACK)


def draw_couch(d):
    # legs
    d.rectangle([356, 856, 384, 892], fill=(16, 6, 34))
    d.rectangle([936, 856, 964, 892], fill=(16, 6, 34))
    # back
    d.rounded_rectangle([322, 592, 998, 806], radius=42, fill=(106, 27, 154),
                        outline=BLACK, width=5)
    d.rounded_rectangle([352, 622, 640, 770], radius=30, fill=(126, 34, 178))
    d.rounded_rectangle([672, 622, 968, 770], radius=30, fill=(126, 34, 178))
    # seat
    d.rounded_rectangle([302, 752, 1018, 862], radius=34, fill=(88, 20, 130),
                        outline=BLACK, width=5)
    d.line([(660, 762), (660, 852)], fill=(60, 12, 92), width=6)
    # arms
    d.rounded_rectangle([296, 636, 386, 884], radius=32, fill=(74, 16, 110),
                        outline=BLACK, width=5)
    d.rounded_rectangle([934, 636, 1020, 884], radius=32, fill=(74, 16, 110),
                        outline=BLACK, width=5)


# ------------------------------------------------------------------- ghost

def sparkle_points(cx, cy, r_out, r_in):
    pts = []
    for i in range(8):
        ang = math.radians(-90 + i * 45)
        r = r_out if i % 2 == 0 else r_in
        pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
    return pts


def star_points(cx, cy, r_out, r_in):
    pts = []
    for i in range(10):
        ang = math.radians(-90 + i * 36)
        r = r_out if i % 2 == 0 else r_in
        pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
    return pts


def ghost_outline(cx, top, hw, yb, scallops=4):
    """Polygon points for the ghost: dome head, straight sides, wavy hem."""
    pts = [(cx - hw, yb)]
    dome_cy = top + hw
    for i in range(25):  # dome, left to right over the top
        ang = math.radians(180 - i * (180 / 24))
        pts.append((cx + hw * math.cos(ang), dome_cy - hw * math.sin(ang)))
    pts.append((cx + hw, yb))
    seg = (2 * hw) / scallops
    r = seg / 2
    for s in range(scallops):  # hem, right to left, scallops dipping down
        ccx = cx + hw - (s + 0.5) * seg
        for i in range(13):
            ang = math.radians(i * (180 / 12))
            pts.append((ccx - r * math.cos(ang), yb + r * math.sin(ang)))
    return pts


def draw_ghost(d):
    cx, top, hw, yb = 648, 372, 152, 796
    # thick black outline: the same silhouette, grown a little, in black
    d.polygon(ghost_outline(cx, top - 9, hw + 9, yb + 9), fill=BLACK)
    d.polygon(ghost_outline(cx, top, hw, yb), fill=WHITE)
    # sparkle eyes
    for ex in (cx - 58, cx + 58):
        d.polygon(sparkle_points(ex, top + hw + 48, 31, 10), fill=BLACK)
    # game controller, held in front
    kx, ky = cx - 58, yb - 92
    d.rounded_rectangle([kx - 88, ky - 42, kx + 88, ky + 42], radius=34,
                        fill=(24, 28, 38), outline=BLACK, width=5)
    d.rectangle([kx - 62, ky - 8, kx - 30, ky + 8], fill=(207, 216, 220))
    d.rectangle([kx - 54, ky - 16, kx - 38, ky + 16], fill=(207, 216, 220))
    d.ellipse([kx + 34, ky - 20, kx + 54, ky], fill=MAGENTA)
    d.ellipse([kx + 56, ky + 2, kx + 76, ky + 22], fill=(46, 230, 168))
    # left round hand on the controller
    hx, hy = cx - hw - 2, yb - 88
    d.ellipse([hx - 27, hy - 27, hx + 27, hy + 27], fill=WHITE, outline=BLACK, width=6)
    # magenta coin with a white star, held up in the right hand
    coin_x, coin_y, coin_r = cx + 208, top + 128, 57
    d.ellipse([coin_x - coin_r, coin_y - coin_r, coin_x + coin_r, coin_y + coin_r],
              fill=MAGENTA, outline=BLACK, width=5)
    d.polygon(star_points(coin_x, coin_y, 30, 13), fill=WHITE)
    hx2, hy2 = coin_x - 44, coin_y + 50
    d.ellipse([hx2 - 26, hy2 - 26, hx2 + 26, hy2 + 26], fill=WHITE,
              outline=BLACK, width=6)


# -------------------------------------------------------------------- text

def fit_font(d, text, max_w, start):
    size = start
    while size > 12:
        font = ImageFont.truetype(CONDENSED_BOLD, size)
        if d.textlength(text, font=font) <= max_w:
            return font
        size -= 2
    return ImageFont.truetype(CONDENSED_BOLD, size)


def caption(d, text, y, start_size):
    font = fit_font(d, text, W - 36, start_size)
    d.text((W / 2, y), text, font=font, fill=WHITE, anchor="mm",
           stroke_width=7, stroke_fill=BLACK)


def main():
    img = Image.new("RGB", (W, H), (0, 0, 0))
    d = ImageDraw.Draw(img)
    draw_sky(img)
    d = ImageDraw.Draw(img)
    draw_sun(d)
    draw_skyline(d)
    palm(d, 60, 668, 118, 470, scale=0.9, flip=1)
    palm(d, 986, 672, 918, 452, scale=1.0, flip=-1)
    # ground
    d.rectangle([0, 862, W, H], fill=(15, 5, 36))
    draw_tv(d)
    draw_couch(d)
    draw_ghost(d)
    caption(d, "WAITED 13 YEARS. TOOK THE DAY OFF.", 74, 96)
    caption(d, "MY AI AGENT ALREADY GOT PAID ON make.fun", 956, 84)
    img.save(OUT, format="PNG")
    print(f"wrote {OUT} ({OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
