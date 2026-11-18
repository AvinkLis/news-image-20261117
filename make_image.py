#!/usr/bin/env python3
"""Draw the entry image: the world news of Tuesday 17 November 2026 in one frame.

A newspaper front page, drawn with PIL primitives only (no photos, no network):
a lead story with a drawn scene of the Kerch Bridge strike, four secondary
stories with flat icons, and a bottom strip of three more. The AI judge has no
news feed, so every story carries its own headline and a one-line explanation.

Run:  python3 make_image.py   ->  writes entry.png beside this file (1024x1024)
"""

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (246, 241, 229)
INK = (32, 36, 43)
RED = (179, 35, 42)
NAVY = (31, 58, 95)
STEEL = (61, 106, 150)
WATER = (127, 168, 201)
SMOKE = (120, 118, 112)
GOLD = (176, 132, 42)
LIGHT_LINE = (198, 190, 170)

FD = "/usr/share/fonts/truetype/dejavu/"
SERIF_B = FD + "DejaVuSerif-Bold.ttf"
SERIF = FD + "DejaVuSerif.ttf"
SANS_B = FD + "DejaVuSans-Bold.ttf"
SANS = FD + "DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        trial = (cur + " " + w_).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, xy, text, fnt, fill, max_w, leading=1.18, align="left"):
    x, y = xy
    lines = wrap(draw, text, fnt, max_w)
    asc, desc = fnt.getmetrics()
    step = int((asc + desc) * leading)
    for ln in lines:
        lx = x
        if align == "center":
            lx = x + (max_w - draw.textlength(ln, font=fnt)) / 2
        draw.text((lx, y), ln, font=fnt, fill=fill)
        y += step
    return y


def rule(draw, y, x0=36, x1=W - 36, fill=INK, width=3):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


# ---------------------------------------------------------------- icons ----

def draw_bridge_scene(draw, box):
    """Kerch Bridge: two towers, a deck, the middle span fallen into the sea."""
    x0, y0, x1, y1 = box
    sea_y = y0 + int((y1 - y0) * 0.62)
    deck_y = y0 + int((y1 - y0) * 0.34)
    # sky fire glow behind the broken span
    draw.ellipse([x0 + 330, y0 + 2, x0 + 560, y0 + 118], fill=(233, 178, 120))
    draw.ellipse([x0 + 370, y0 + 16, x0 + 520, y0 + 96], fill=(240, 205, 150))
    # sea
    draw.rectangle([x0, sea_y, x1, y1], fill=WATER)
    for i in range(3):
        yy = sea_y + 12 + i * 15
        draw.line([(x0 + 20 + (i % 3) * 40, yy), (x0 + 130 + (i % 3) * 40, yy)], fill=STEEL, width=3)
        draw.line([(x1 - 190 + (i % 2) * 30, yy), (x1 - 80 + (i % 2) * 30, yy)], fill=STEEL, width=3)
    # towers (kept below the deck line above the scene)
    for tx in (x0 + 150, x1 - 190):
        draw.rectangle([tx, deck_y - 64, tx + 26, sea_y + 26], fill=NAVY)
    # standing deck, left and right of the gap
    draw.rectangle([x0 + 10, deck_y, x0 + 400, deck_y + 14], fill=NAVY)
    draw.rectangle([x0 + 545, deck_y, x1 - 10, deck_y + 14], fill=NAVY)
    # cables
    for tx in (x0 + 163, x1 - 177):
        draw.line([(tx, deck_y - 64), (tx - 120, deck_y)], fill=NAVY, width=3)
        draw.line([(tx, deck_y - 64), (tx + 120, deck_y)], fill=NAVY, width=3)
    # the fallen span, tilted into the water
    draw.polygon([(x0 + 405, deck_y + 4), (x0 + 545, deck_y + 46),
                  (x0 + 540, deck_y + 62), (x0 + 402, deck_y + 20)], fill=RED)
    draw.polygon([(x0 + 440, sea_y + 26), (x0 + 520, sea_y + 44),
                  (x0 + 515, sea_y + 58), (x0 + 438, sea_y + 40)], fill=RED)
    # splash + smoke
    for dx in (430, 470, 505):
        draw.line([(x0 + dx, sea_y + 4), (x0 + dx - 8, sea_y - 22)], fill=(240, 248, 252), width=4)
    for i, (cx, cy, r) in enumerate([(455, 60, 30), (492, 38, 40), (535, 52, 33)]):
        draw.ellipse([x0 + cx - r, y0 + cy - r, x0 + cx + r, y0 + cy + r], fill=SMOKE)
    # missile streak
    draw.line([(x0 + 90, y0 + 6), (x0 + 415, deck_y - 26)], fill=RED, width=4)
    draw.ellipse([x0 + 408, deck_y - 33, x0 + 424, deck_y - 17], fill=RED)


def draw_ship(draw, cx, cy, s=1.0):
    hull = [(cx - 52 * s, cy + 6 * s), (cx + 52 * s, cy + 6 * s),
            (cx + 38 * s, cy + 24 * s), (cx - 38 * s, cy + 24 * s)]
    draw.polygon(hull, fill=NAVY)
    draw.rectangle([cx - 30 * s, cy - 12 * s, cx + 6 * s, cy + 6 * s], fill=STEEL)
    draw.rectangle([cx + 12 * s, cy - 22 * s, cx + 24 * s, cy + 6 * s], fill=STEEL)
    # naval mine beside the ship
    draw.ellipse([cx + 58 * s, cy + 8 * s, cx + 82 * s, cy + 32 * s], fill=RED)
    for a in range(0, 360, 60):
        import math
        ex = cx + 70 * s + 15 * s * math.cos(math.radians(a))
        ey = cy + 20 * s + 15 * s * math.sin(math.radians(a))
        draw.line([(cx + 70 * s, cy + 20 * s), (ex, ey)], fill=RED, width=3)


def draw_plane(draw, cx, cy, s=1.0):
    # side-profile airliner: fuselage, swept wing, tail fin
    draw.polygon([(cx - 58 * s, cy + 2 * s), (cx + 40 * s, cy - 8 * s),
                  (cx + 58 * s, cy - 2 * s), (cx + 40 * s, cy + 8 * s),
                  (cx - 58 * s, cy + 10 * s)], fill=NAVY)
    draw.polygon([(cx - 6 * s, cy + 6 * s), (cx + 16 * s, cy + 27 * s),
                  (cx + 2 * s, cy + 28 * s), (cx - 20 * s, cy + 8 * s)], fill=STEEL)
    draw.polygon([(cx - 58 * s, cy + 2 * s), (cx - 46 * s, cy - 17 * s),
                  (cx - 35 * s, cy - 15 * s), (cx - 41 * s, cy + 4 * s)], fill=RED)
    for i in range(4):
        wx = cx + (6 + i * 11) * s
        draw.ellipse([wx, cy - 4 * s, wx + 5 * s, cy + 1 * s], fill=PAPER)


def draw_rocket(draw, cx, cy, s=1.0):
    draw.polygon([(cx, cy - 52 * s), (cx + 15 * s, cy - 18 * s),
                  (cx + 15 * s, cy + 22 * s), (cx - 15 * s, cy + 22 * s),
                  (cx - 15 * s, cy - 18 * s)], fill=STEEL)
    draw.ellipse([cx - 7 * s, cy - 30 * s, cx + 7 * s, cy - 16 * s], fill=PAPER)
    draw.polygon([(cx - 15 * s, cy + 8 * s), (cx - 30 * s, cy + 30 * s),
                  (cx - 15 * s, cy + 30 * s)], fill=RED)
    draw.polygon([(cx + 15 * s, cy + 8 * s), (cx + 30 * s, cy + 30 * s),
                  (cx + 15 * s, cy + 30 * s)], fill=RED)
    # broken-off satellite panel + flame sputter
    draw.rectangle([cx + 30 * s, cy - 44 * s, cx + 58 * s, cy - 30 * s], fill=GOLD)
    draw.polygon([(cx - 9 * s, cy + 22 * s), (cx, cy + 46 * s), (cx + 9 * s, cy + 22 * s)],
                 fill=(233, 140, 60))


def draw_bank(draw, cx, cy, s=1.0):
    draw.polygon([(cx - 52 * s, cy - 26 * s), (cx, cy - 48 * s), (cx + 52 * s, cy - 26 * s)], fill=NAVY)
    for i in range(4):
        x = cx - 39 * s + i * 26 * s
        draw.rectangle([x, cy - 20 * s, x + 10 * s, cy + 22 * s], fill=STEEL)
    draw.rectangle([cx - 54 * s, cy + 24 * s, cx + 54 * s, cy + 32 * s], fill=NAVY)
    # bug: a red X over the door
    draw.line([(cx - 9 * s, cy - 2 * s), (cx + 9 * s, cy + 16 * s)], fill=RED, width=4)
    draw.line([(cx + 9 * s, cy - 2 * s), (cx - 9 * s, cy + 16 * s)], fill=RED, width=4)


# ----------------------------------------------------------------- page ----

def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # masthead
    rule(d, 22, fill=RED, width=5)
    rule(d, 32, width=2)
    text_block(d, (36, 44), "THE DAILY PICTURE", font(SERIF_B, 66), INK, W - 72, align="center")
    text_block(d, (36, 128),
               "Tuesday 17 November 2026  ·  The whole world's news, in one image",
               font(SANS_B, 21), NAVY, W - 72, align="center")
    rule(d, 168, width=4)
    rule(d, 176, width=1)

    # lead story — fixed vertical budget so nothing below can overflow
    text_block(d, (36, 188), "LEAD STORY — EUROPE AT WAR", font(SANS_B, 20), RED, 700)
    text_block(d, (36, 214),
               "UKRAINE BLOWS A GAP IN THE CRIMEA BRIDGE",
               font(SERIF_B, 47), INK, W - 72)
    text_block(d, (36, 338),
               "Kyiv's strike collapses a span of the Kerch road bridge, Russia's lifeline "
               "to occupied Crimea. Moscow answers within hours by striking Kyiv's bridges.",
               font(SERIF, 21), INK, W - 72)
    draw_bridge_scene(d, (36, 414, W - 36, 546))
    text_block(d, (36, 554),
               "The Kerch Bridge after the strike: one road span in the sea. "
               "Zelenskyy hails an \u201cunprecedented operation\u201d.",
               font(SANS, 17), NAVY, W - 72, align="center")
    rule(d, 584, width=2)

    # secondary grid, 2 x 2 — short deks, measured to fit their cells
    gy = 596
    cells = [
        (draw_ship, "TANKERS HIT MINES IN THE STRAIT OF HORMUZ",
         "Iran's Guards say two tankers struck mines and caught fire. Drones target "
         "a U.S. radar in Bahrain."),
        (draw_plane, "TRUMP LANDS IN MANILA FOR ASEAN SUMMIT",
         "First stop of a three-day Asia swing ending in China — one table with "
         "Xi Jinping and Vladimir Putin."),
        (draw_rocket, "VULCAN ROCKET FAILS — 40 SATELLITES LOST",
         "ULA's Vulcan breaks up minutes after liftoff from Cape Canaveral, "
         "destroying 40 Amazon Leo internet satellites."),
        (draw_bank, "JPMORGAN'S BIG OUTAGE WAS A BUG, NOT HACKERS",
         "America's largest bank blames a software fault, not hackers, for "
         "Monday's app and Zelle meltdown."),
    ]
    cell_w, cell_h = (W - 72 - 24) // 2, 126
    for i, (icon, head, dek) in enumerate(cells):
        cx0 = 36 + (i % 2) * (cell_w + 24)
        cy0 = gy + (i // 2) * (cell_h + 8)
        icon(d, cx0 + 50, cy0 + 56, 0.8)
        text_block(d, (cx0 + 124, cy0), head, font(SANS_B, 20), INK, cell_w - 130)
        text_block(d, (cx0 + 124, cy0 + 52), dek, font(SANS, 16), INK, cell_w - 130)
    gy2 = gy + 2 * cell_h + 8
    rule(d, gy2 + 4, width=2)

    # bottom strip: three minis
    minis = [
        ("GENEVA", "128 nations open talks on banning \u201ckiller robots\u201d — weapons "
                    "that pick their own targets."),
        ("TOKYO", "Japan scrambles fighter jets and protests after Russian aircraft "
                  "breach its airspace."),
        ("WASHINGTON", "Pentagon fails its money audit for the 9th straight year. "
                       "Nvidia posts first earnings since Huang's exit."),
    ]
    mw = (W - 72 - 32) // 3
    for i, (kick, body) in enumerate(minis):
        mx = 36 + i * (mw + 16)
        text_block(d, (mx, gy2 + 14), kick, font(SANS_B, 19), RED, mw)
        text_block(d, (mx, gy2 + 42), body, font(SANS, 16), INK, mw)

    # footer
    rule(d, H - 46, width=4)
    text_block(d, (36, H - 34),
               "ALSO TODAY — West presses Israel to open Gaza aid crossings · "
               "UK sanctions settlement firms",
               font(SANS_B, 16), NAVY, W - 72, align="center")

    img.save("entry.png", optimize=True)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
