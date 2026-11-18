"""Lift the acacia tree out of the Facebook profile logo into a transparent PNG.

Run from the project root:  python -I tools/build_logo.py
Reads _source/fb/logo.jpg, writes _source/gen/tree.png (black tree, alpha from darkness).
"""
import os
from PIL import Image, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src = Image.open(os.path.join(ROOT, "_source", "fb", "logo.jpg")).convert("L")
# tree sits inside the ring, between the curved name (top) and "Marloth Park" (bottom)
box = (140, 212, 580, 505)
crop = src.crop(box)
# dark pixels are the tree; the grey ground shadow (~150-200) is dropped
alpha = crop.point(lambda v: 0 if v > 120 else (255 if v < 60 else int((120 - v) * 255 / 60)))
alpha = alpha.filter(ImageFilter.MedianFilter(3))
# keep only the largest connected shape (drops bits of the curved lettering)
w, h = alpha.size
px = alpha.load()
seen = bytearray(w * h)
best = []
for sy in range(h):
    for sx in range(w):
        if px[sx, sy] < 40 or seen[sy * w + sx]:
            continue
        comp, stack = [], [(sx, sy)]
        seen[sy * w + sx] = 1
        while stack:
            x, y = stack.pop()
            comp.append((x, y))
            for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                if 0 <= nx < w and 0 <= ny < h and not seen[ny * w + nx] and px[nx, ny] >= 40:
                    seen[ny * w + nx] = 1
                    stack.append((nx, ny))
        if len(comp) > len(best):
            best = comp
keep = Image.new("L", alpha.size, 0)
kp = keep.load()
for x, y in best:
    kp[x, y] = 255
keep = keep.filter(ImageFilter.MaxFilter(5))
alpha = Image.composite(alpha, Image.new("L", alpha.size, 0), keep)
tree = Image.new("RGBA", crop.size, (0, 0, 0, 0))
tree.putalpha(alpha)
tree = tree.crop(alpha.getbbox())
out = os.path.join(ROOT, "_source", "gen", "tree.png")
tree.save(out)
print(tree.size)
