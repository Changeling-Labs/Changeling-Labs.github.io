#!/usr/bin/env python3
"""
Build the hub's brand assets from the source artwork in the Obsidian vault.

There is no logo file to export, so the assets are cropped out of the brand
guide's own renders:

  * chrysalis-mark.png / icon-192.png / icon-512.png
        <- "Pasted image 20261105180143.png" (the asset spec sheet: the mark
           rendered large on a transparency checkerboard)
  * lockup.png
        <- "Pasted image 20261105172334.png" (Corporate Style Guide, the
           horizontal lockup with clear-space guides)

Nothing is redrawn or re-generated: the artwork is keyed off its background
and cleaned of the guide's own hairlines.

Run from the repo root:  python3 tools/make-brand-icons.py
Requires Pillow and read access to the vault.
"""

import os
from pathlib import Path

from PIL import Image, ImageFilter

VAULT = Path(
    "/Users/edmundashdown/Library/CloudStorage/OneDrive-Personal/Documents/Obsidian Vault"
)
SPEC_SHEET = VAULT / "Pasted image 20261105180143.png"   # mark on checkerboard
STYLE_GUIDE = VAULT / "Pasted image 20261105172334.png"  # lockup on white
OUT = Path(__file__).resolve().parent.parent / "icons"

# ── 1. The mark, keyed off the transparency checkerboard ──────────────────
src = Image.open(SPEC_SHEET).convert("RGB")
panel = src.crop((60, 100, 700, 672))    # the large mark panel, caption excluded
W, H = panel.size
px = panel.load()

alpha = Image.new("L", (W, H), 0)
rgb = Image.new("RGB", (W, H), (0, 0, 0))
ap, cp = alpha.load(), rgb.load()
ink = Image.new("L", (W, H), 0)          # blue/cyan ink only
ip = ink.load()

for y in range(H):
    for x in range(W):
        r, g, b = px[x, y]
        mn, spread = min(r, g, b), max(r, g, b) - min(r, g, b)
        a = 255 - mn
        ap[x, y] = a
        if a:                            # white-to-alpha: unpremultiply the blend
            k = 255 / a
            cp[x, y] = (
                max(0, min(255, round((r - (255 - a)) * k))),
                max(0, min(255, round((g - (255 - a)) * k))),
                max(0, min(255, round((b - (255 - a)) * k))),
            )
        if b - r >= 10 and (spread >= 20 or mn <= 175):
            ip[x, y] = 255

near = ink.filter(ImageFilter.MaxFilter(13)).load()
for y in range(H):
    for x in range(W):
        if near[x, y] == 0 or ap[x, y] < 40:
            ap[x, y] = 0                 # drop the checkerboard and its fringe
            cp[x, y] = (0, 0, 0)
        else:
            ap[x, y] = min(255, round((ap[x, y] - 40) * 255 / 215))

mark = Image.merge("RGBA", (*rgb.split(), alpha))


def drop_residue(im, min_sat=70):
    """Remove the guide's grey hairlines: low-saturation specks on the panel edge.

    Real artwork is blue/cyan/navy (mean saturation well above 100); the panel
    border, the mockup's card edge and its dashed clear-space guides all key out
    as near-neutral grey, so they can be dropped on saturation alone.
    """
    w, h = im.size
    band = im.getchannel("A")            # a live band (split() would copy)
    a = band.load()
    R, G, B = (c.load() for c in im.split()[:3])
    seen = [[False] * w for _ in range(h)]
    kill = []
    for y in range(h):
        for x in range(w):
            if a[x, y] > 10 and not seen[y][x]:
                stack, pts = [(x, y)], []
                seen[y][x] = True
                while stack:
                    cx, cy = stack.pop()
                    pts.append((cx, cy))
                    for dx in (-1, 0, 1):
                        for dy in (-1, 0, 1):
                            nx, ny = cx + dx, cy + dy
                            if 0 <= nx < w and 0 <= ny < h and not seen[ny][nx] and a[nx, ny] > 10:
                                seen[ny][nx] = True
                                stack.append((nx, ny))
                sat = sum(max(R[p], G[p], B[p]) - min(R[p], G[p], B[p]) for p in pts) / len(pts)
                if sat < min_sat:
                    kill.extend(pts)
    for x, y in kill:
        a[x, y] = 0
    im.putalpha(band)
    return im


mark = drop_residue(mark).crop(mark.getbbox())

# Web header/footer mark (2x for a 46px slot).
hw = 256
mark.resize((hw, round(hw * mark.height / mark.width)), Image.LANCZOS).save(
    OUT / "chrysalis-mark.png", optimize=True
)


def icon(size):
    """Favicon / PWA icon: the mark on white with 10% clear space."""
    pad = round(size * 0.10)
    m = mark.copy()
    m.thumbnail((size - 2 * pad, size - 2 * pad), Image.LANCZOS)
    c = Image.new("RGB", (size, size), (255, 255, 255))
    c.paste(m, ((size - m.width) // 2, (size - m.height) // 2), m)
    return c


for size in (512, 192):
    icon(size).save(OUT / f"icon-{size}.png", optimize=True)

# ── 2. Horizontal lockup, lifted off the style guide's white page ─────────
g = Image.open(STYLE_GUIDE).convert("RGB")
lock = g.crop((225, 92, 1175, 292))
lw, lh = lock.size
lp = lock.load()
for y in range(lh):
    for x in range(lw):
        r, gg, b = lp[x, y]
        spread = max(r, gg, b) - min(r, gg, b)
        # neutral + light = page or dashed clear-space guides; right label = "30mm"
        if (spread <= 18 and min(r, gg, b) >= 172) or (x >= 855 and y <= 65):
            lp[x, y] = (255, 255, 255)

xs, ys = [], []
for y in range(lh):
    for x in range(lw):
        r, gg, b = lp[x, y]
        if min(r, gg, b) < 200 or (max(r, gg, b) - min(r, gg, b)) > 30:
            xs.append(x)
            ys.append(y)
pad = 14
lock = lock.crop(
    (max(0, min(xs) - pad), max(0, min(ys) - pad), min(lw, max(xs) + 1 + pad), min(lh, max(ys) + 1 + pad))
)
lock.save(OUT / "lockup.png", optimize=True)

for f in ("chrysalis-mark.png", "icon-512.png", "icon-192.png", "lockup.png"):
    print(f"{f:22} {os.path.getsize(OUT / f) // 1024:>4} KB  {Image.open(OUT / f).size}")
