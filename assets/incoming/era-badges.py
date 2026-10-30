"""Split the stacked badge image into two 88x31 badges (stored at 2x) with transparent backgrounds.
Usage: python era-badges.py <source.png> <out_dir>
This is exactly what was done for the design canvas."""
import os, sys
import numpy as np
from PIL import Image, ImageDraw

src, out = sys.argv[1], sys.argv[2]
os.makedirs(out, exist_ok=True)
im = Image.open(src).convert('RGBA')
a = np.array(im)
nonwhite = a[..., :3].min(axis=2) < 235
rows = np.where(nonwhite.any(axis=1))[0]
bands, start, prev = [], None, None
for r in rows:  # contiguous non-white row bands = one badge each
    if start is None: start = r
    elif r != prev + 1: bands.append((start, prev)); start = r
    prev = r
bands.append((start, prev))
names = ['netscape', 'ie']  # top to bottom in the source image
for name, (y0, y1) in zip(names, bands):
    band = a[y0:y1 + 1]
    cols = np.where((band[..., :3].min(axis=2) < 235).any(axis=0))[0]
    crop = im.crop((cols.min(), y0, cols.max() + 1, y1 + 1))
    rgb = Image.new('RGB', crop.size, (255, 255, 255)); rgb.paste(crop, mask=crop.split()[3])
    w, h = rgb.size
    for seed in [(0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1)]:  # flood the outer white only
        if min(rgb.getpixel(seed)) >= 225:
            ImageDraw.floodfill(rgb, seed, (255, 0, 255), thresh=40)
    m = np.array(rgb); c = np.array(crop)
    c[..., 3] = np.where((m[..., 0] == 255) & (m[..., 1] == 0) & (m[..., 2] == 255), 0, 255)
    big = Image.fromarray(c).resize((176, 62), Image.LANCZOS)
    big.putalpha(big.split()[3].point(lambda v: 255 if v >= 128 else 0))
    big.save(os.path.join(out, f'96-badge-{name}.png'))
    print(name, big.size)
