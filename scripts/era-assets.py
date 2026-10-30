#!/usr/bin/env python3
"""Draw the image assets the 1996, 2001 and 2006 eras need, from the site's own data.

Text that is baked into an image (button labels, 2001 tabs and pixel headings, the 2006 logo, the
hit counter) comes from _data/, so changing a label means editing the YAML and re-running this
script. The 1996 badges are cut out of the stacked source image named in _data/eras.yml.

    python3 scripts/era-assets.py                 # everything, into assets/eras/<year>/
    python3 scripts/era-assets.py --only badges   # just the two 1996 badges
    python3 scripts/era-assets.py --only 2001

Needs Pillow and PyYAML (pip install pillow pyyaml). The generated files are committed, so the Jekyll
build never runs this. See docs/era-assets.md.
"""
import argparse
import math
import sys
import unicodedata
from pathlib import Path

import yaml
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / '_data'
GROUPS = ('shared', '1996', '2001', '2006', 'badges', 'thumbs')

SANS_B = MONO_B = None  # set in main() from --fonts


# ---------- data ----------
def load(name):
    with open(DATA / name, encoding='utf-8') as fh:
        return yaml.safe_load(fh)


def ascii_text(text):
    """Pixel text only has plain letters: Résumé -> Resume."""
    plain = ''.join(c for c in unicodedata.normalize('NFKD', text) if not unicodedata.combining(c))
    plain.encode('ascii')  # fail loudly on anything else
    return plain


def read_labels():
    site, about, nav = load('site.yml'), load('about.yml'), load('navigation.yml')
    eras = {e['slug']: e for e in load('eras.yml')}
    return {
        'name': site['name'],
        'about_heading': about['heading'],
        'nav': [(ascii_text(n['name']).lower(), n['name']) for n in nav],  # ('resume', 'Résumé')
        'labels': site['labels'],
        'resume_button': site['resume']['button'],
        'portfolio_button': site['portfolio']['button'],
        'eras': eras,
        'cases': [c for c in load('casestudies.yml') if c.get('publish')],
        'headshot': site['headshot']['file'],
    }


# ---------- drawing helpers ----------
def hexrgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(len(a)))


def vgrad(w, h, stops):
    """stops: list of (pos 0..1, hex)."""
    im = Image.new('RGB', (w, h))
    d = ImageDraw.Draw(im)
    for y in range(h):
        t = y / max(1, h - 1)
        for i in range(len(stops) - 1):
            p0, c0 = stops[i]
            p1, c1 = stops[i + 1]
            if p0 <= t <= p1:
                c = lerp(hexrgb(c0), hexrgb(c1), 0 if p1 == p0 else (t - p0) / (p1 - p0))
                break
        d.line([(0, y), (w, y)], fill=c)
    return im


def save_gif(im, out, name, transparent=None):
    p = im.convert('P', palette=Image.ADAPTIVE, colors=255)
    kw = {}
    if transparent is not None:
        kw['transparency'] = transparent
    p.save(out / name, **kw)


def pixel_text(text, size=8, scale=2, color='#ffffff', font=None, track=1):
    """Non-antialiased small text scaled up."""
    f = ImageFont.truetype(font or SANS_B, size)
    widths = [f.getbbox(ch)[2] if ch != ' ' else size // 2 for ch in text]
    w = sum(widths) + track * len(text) + 2
    h = size + 4
    im = Image.new('1', (w, h), 0)
    d = ImageDraw.Draw(im)
    d.fontmode = '1'
    x = 1
    for ch, cw in zip(text, widths):
        d.text((x, 1), ch, font=f, fill=1)
        x += cw + track
    bbox = im.getbbox() or (0, 0, w, h)
    im = im.crop((0, 0, bbox[2] + 1, h))
    im = im.resize((im.width * scale, im.height * scale), Image.NEAREST)
    rgba = Image.new('RGBA', im.size, (0, 0, 0, 0))
    rgba.paste(Image.new('RGBA', im.size, hexrgb(color) + (255,)), mask=im)
    return rgba


def flatten(fg, bg_hex):
    bg = Image.new('RGB', fg.size, hexrgb(bg_hex))
    bg.paste(fg, mask=fg.split()[3])
    return bg


# ======================= 1996 =======================
def make_1996(out, L):
    # Star tile
    tile = Image.new('RGB', (64, 64), hexrgb('#000033'))
    d = ImageDraw.Draw(tile)
    for (x, y, c) in [(5, 9, '#ffffff'), (41, 3, '#ffff99'), (22, 30, '#ffffff'), (55, 37, '#ffffff'),
                      (11, 51, '#ffff99'), (35, 57, '#ffffff'), (60, 18, '#ffffff'), (28, 12, '#9999ff')]:
        d.point((x, y), fill=c)
    d.point((22, 29), fill='#6666cc')
    d.point((22, 31), fill='#6666cc')
    d.point((21, 30), fill='#6666cc')
    d.point((23, 30), fill='#6666cc')
    save_gif(tile, out, '96-stars.gif')

    # Rainbow divider
    rb = Image.new('RGB', (520, 6))
    cols = ['#ff0000', '#ff9900', '#ffff00', '#00cc00', '#0099ff', '#6600cc', '#ff0000']
    for x in range(520):
        t = x / 519 * (len(cols) - 1)
        i = min(int(t), len(cols) - 2)
        c = lerp(hexrgb(cols[i]), hexrgb(cols[i + 1]), t - i)
        ImageDraw.Draw(rb).line([(x, 0), (x, 5)], fill=c)
    save_gif(rb, out, '96-rainbow.gif')

    # Beveled gray buttons
    def bevel_button(text, w, h, name):
        im = Image.new('RGB', (w, h), hexrgb('#c0c0c0'))
        d = ImageDraw.Draw(im)
        for i in range(2):
            d.line([(i, i), (w - 1 - i, i)], fill='#ffffff')
            d.line([(i, i), (i, h - 1 - i)], fill='#ffffff')
            d.line([(i, h - 1 - i), (w - 1 - i, h - 1 - i)], fill='#808080' if i else '#000000')
            d.line([(w - 1 - i, i), (w - 1 - i, h - 1 - i)], fill='#808080' if i else '#000000')
        f = ImageFont.truetype(SANS_B, 14)
        bb = d.textbbox((0, 0), text, font=f)
        d.text(((w - (bb[2] - bb[0])) / 2 - bb[0], (h - (bb[3] - bb[1])) / 2 - bb[1]), text, font=f, fill='#000000')
        save_gif(im, out, name)

    for key, label in L['nav']:
        bevel_button(label, 140, 34, f'96-btn-{key}.gif')
    bevel_button(L['resume_button'], 200, 34, '96-btn-dl-resume.gif')
    bevel_button(L['portfolio_button'], 210, 34, '96-btn-dl-portfolio.gif')

    # Hit counter: the era's year, zero-padded to seven digits
    cnt = Image.new('RGB', (100, 24), hexrgb('#000000'))
    d = ImageDraw.Draw(cnt)
    d.rectangle([0, 0, 99, 23], outline='#808080')
    d.text((7, 2), f"{int(L['eras']['1996']['label']):07d}", font=ImageFont.truetype(MONO_B, 16), fill='#00ff00')
    save_gif(cnt, out, '96-counter.gif')


# ======================= 1996 case-study thumbnails =======================
def make_thumbs(out, L):
    """120 x 90 JPEGs of the approved Phase 1 card images (already 4:3, cropped from the top), one per
    published case study, named after its page: 96-case-amex-value-builder.jpg."""
    for case in L['cases']:
        src = Image.open(ROOT / 'assets' / 'images' / 'wf' / case['card_image']).convert('RGB')
        thumb = src.resize((120, 90), Image.LANCZOS)
        thumb.save(out / f"96-case-{Path(case['link']).stem}.jpg", quality=85)


# ======================= square headshot =======================
def make_headshot(out, L):
    """The headshot is a circle on black. Older eras show it as a square photo. The black outside the
    circle becomes the circle's own background gray: the gray along the circle's edge, averaged over
    +-20 degrees so it is smooth (no streaks), carried straight out to the corners. Where the sweater
    meets the bottom edge, the corners get the sweater's color instead. The photo blends into the fill
    over its last 4px so no ring shows."""
    src = Image.open(ROOT / L['headshot']).convert('RGB')
    w, h = src.size
    px = src.load()
    cx, cy = (w - 1) / 2, (h - 1) / 2
    R = w / 2 - 4  # just inside the antialiased edge, which is mixed with the black

    def lum(c):
        return 0.299 * c[0] + 0.587 * c[1] + 0.114 * c[2]

    # Edge samples per degree: light, low-saturation pixels are background; dark ones may be sweater.
    per = [[] for _ in range(360)]
    dark = []
    for d10 in range(0, 3600, 5):
        a = math.radians(d10 / 10)
        for r in (R - 5, R - 3, R - 1):
            c = px[int(round(cx + r * math.cos(a))), int(round(cy + r * math.sin(a)))]
            if lum(c) > 150 and max(c) - min(c) < 25:
                per[d10 // 10].append(c)
            elif lum(c) < 80 and r == R - 1:
                dark.append((d10 / 10, c))

    # Background gray per degree, smoothed around the circle; gaps borrow the nearest angle.
    edge = []
    for d in range(360):
        acc, wt = [0, 0, 0], 0
        for dd in range(-20, 21):
            k = 21 - abs(dd)
            for c in per[(d + dd) % 360]:
                acc = [acc[i] + c[i] * k for i in range(3)]
                wt += k
        edge.append([v / wt for v in acc] if wt else None)
    for d in range(360):
        for s in range(1, 180):
            if edge[d] is not None:
                break
            edge[d] = edge[(d + s) % 360] or edge[(d - s) % 360]

    # The sweater: the dark run across the bottom edge (y grows downward, so 90 degrees is straight down).
    bottom = [(d, c) for d, c in dark if 20 < d < 160]
    lo, hi = min(d for d, _ in bottom), max(d for d, _ in bottom)
    sweater = sorted((c for _, c in bottom), key=lum)[len(bottom) // 2]

    img = Image.new('RGB', (w, h))
    op = img.load()
    for y in range(h):
        for x in range(w):
            d = math.degrees(math.atan2(y - cy, x - cx)) % 360
            i, f = int(d) % 360, d - int(d)
            gray = [edge[i][k] * (1 - f) + edge[(i + 1) % 360][k] * f for k in range(3)]
            t = min(1, max(0, (d - lo) / 2)) * min(1, max(0, (hi - d) / 2))  # 2-degree shoulder edge
            fill = [gray[k] * (1 - t) + sweater[k] * t for k in range(3)]
            m = min(1, max(0, (R - math.hypot(x - cx, y - cy)) / 4))
            c = px[x, y]
            op[x, y] = tuple(max(0, min(255, int(round(c[k] * m + fill[k] * (1 - m))))) for k in range(3))
    img.save(out / 'headshot-square.jpg', quality=90)


# ======================= badges =======================
def make_badges(out, L):
    """Split the stacked source image into one badge per non-white row band, make the outer white
    transparent, and save each at 176x62 (shown at 88x31)."""
    era = L['eras']['1996']
    badges = era['badges']
    im = Image.open(ROOT / era['badge_source']).convert('RGBA')
    px = im.convert('RGB').load()
    w, h = im.size

    def nonwhite(x, y):
        return min(px[x, y]) < 235

    rows = [y for y in range(h) if any(nonwhite(x, y) for x in range(w))]
    bands, start, prev = [], None, None
    for r in rows:  # contiguous non-white row bands = one badge each
        if start is None:
            start = r
        elif r != prev + 1:
            bands.append((start, prev))
            start = r
        prev = r
    bands.append((start, prev))
    if len(bands) != len(badges):
        sys.exit(f"{era['badge_source']}: found {len(bands)} badge bands, but eras.yml lists {len(badges)} badges")

    for badge, (y0, y1) in zip(badges, bands):
        cols = [x for x in range(w) if any(nonwhite(x, y) for y in range(y0, y1 + 1))]
        crop = im.crop((cols[0], y0, cols[-1] + 1, y1 + 1))
        rgb = Image.new('RGB', crop.size, (255, 255, 255))
        rgb.paste(crop, mask=crop.split()[3])
        cw, ch = rgb.size
        for seed in [(0, 0), (cw - 1, 0), (0, ch - 1), (cw - 1, ch - 1)]:  # flood the outer white only
            if min(rgb.getpixel(seed)) >= 225:
                ImageDraw.floodfill(rgb, seed, (255, 0, 255), thresh=40)
        r, g, b = rgb.split()
        flooded = ImageChops.multiply(
            ImageChops.multiply(r.point(lambda v: 255 if v == 255 else 0), g.point(lambda v: 255 if v == 0 else 0)),
            b.point(lambda v: 255 if v == 255 else 0))
        cutout = crop.convert('RGB')
        cutout.putalpha(ImageChops.invert(flooded))
        big = cutout.resize((176, 62), Image.LANCZOS)
        big.putalpha(big.split()[3].point(lambda v: 255 if v >= 128 else 0))
        big.save(out / f"96-badge-{badge['id']}.png")


# ======================= 2001 =======================
def make_2001(out, L):
    ui = L['eras']['2001']['ui']
    lab = L['labels']

    # Side panel gradient (diagonal-ish: vertical approximation)
    side = Image.new('RGB', (240, 640))
    for y in range(640):
        for x in range(0, 240, 4):
            t = min(1, (x * 0.35 + y) / 520)
            c = lerp(hexrgb('#3a3e44'), hexrgb('#1f2226'), t)
            ImageDraw.Draw(side).line([(x, y), (x + 3, y)], fill=c)
    side.save(out / '01-side.jpg', quality=88)

    # Content top gradient (repeat-x)
    vgrad(4, 240, [(0, '#24272b'), (1, '#1a1c1f')]).save(out / '01-content-bg.jpg', quality=90)

    def tab(label, on, name):
        w, h = 200, 40
        if on:
            im = vgrad(w, h, [(0, '#ff8833'), (1, '#cc5200')])
            border, ink = '#ff6600', '#ffffff'
        else:
            im = vgrad(w, h, [(0, '#4a4e55'), (1, '#2a2d32')])
            border, ink = '#5a5f66', '#e6e6e6'
        d = ImageDraw.Draw(im)
        d.rectangle([0, 0, w - 1, h - 1], outline=border)
        t = pixel_text(label.upper(), color=ink)
        im.paste(t, (14, (h - t.height) // 2), t)
        if on:
            a = pixel_text('>', color=ink)
            im.paste(a, (w - 14 - a.width, (h - a.height) // 2), a)
        save_gif(im, out, name)

    def tab_hover(label, name):
        w, h = 200, 40
        im = vgrad(w, h, [(0, '#5a5f66'), (1, '#3a3e44')])
        d = ImageDraw.Draw(im)
        d.rectangle([0, 0, w - 1, h - 1], outline='#ff6600')
        t = pixel_text(label.upper(), color='#ffcc66')
        im.paste(t, (14, (h - t.height) // 2), t)
        save_gif(im, out, name)

    for key, label in L['nav']:
        text = ascii_text(label)
        tab(text, True, f'01-tab-{key}-on.gif')
        tab(text, False, f'01-tab-{key}-off.gif')
        tab_hover(text, f'01-tab-{key}-over.gif')

    def pix_gif(text, name, color='#ffffff', bg='#1a1c1f', scale=2):
        t = pixel_text(ascii_text(text).upper(), color=color, scale=scale)
        save_gif(flatten(t, bg), out, name)

    nav = dict(L['nav'])
    pix_gif(L['name'], '01-name-intro.gif', bg='#202328', scale=4)
    pix_gif(L['name'], '01-name.gif', bg='#30343a', scale=2)
    pix_gif(ui['loading'], '01-loading.gif', color='#ff9933', bg='#202328')
    pix_gif(L['about_heading'], '01-h-about.gif', bg='#24272b', scale=3)
    pix_gif(lab['case_studies'], '01-h-work.gif', bg='#24272b', scale=3)
    pix_gif(nav['resume'], '01-h-resume.gif', bg='#24272b', scale=3)
    pix_gif(lab['contact'], '01-h-contact.gif', bg='#24272b', scale=3)
    pix_gif(lab['more_work'], '01-h-more.gif', bg='#1f2125', scale=2)
    pix_gif(lab['clients'], '01-h-clients.gif', color='#ff9933', bg='#1f2125', scale=2)

    def boxbtn(text, w, h, on, name):
        text = ascii_text(text).upper()
        w = max(w, pixel_text(text).width + 36)
        if on:
            im = vgrad(w, h, [(0, '#ff8833'), (1, '#cc5200')])
            border, ink = '#ff6600', '#ffffff'
        else:
            im = vgrad(w, h, [(0, '#4a4e55'), (1, '#2a2d32')])
            border, ink = '#5a5f66', '#ffffff'
        d = ImageDraw.Draw(im)
        d.rectangle([0, 0, w - 1, h - 1], outline=border)
        t = pixel_text(text, color=ink)
        im.paste(t, ((w - t.width) // 2, (h - t.height) // 2), t)
        save_gif(im, out, name)

    boxbtn(ui['skip'], 150, 40, False, '01-skip.gif')
    boxbtn(ui['replay'], 150, 36, False, '01-replay.gif')
    boxbtn(L['resume_button'], 260, 44, True, '01-btn-resume.gif')
    boxbtn(L['portfolio_button'], 290, 44, False, '01-btn-portfolio.gif')

    # Animated loader bar (plays once, holds full)
    frames = []
    for i in range(16):
        fr = Image.new('RGB', (324, 14), hexrgb('#202328'))
        d = ImageDraw.Draw(fr)
        d.rectangle([0, 0, 323, 13], outline='#ff6600')
        fill = int(318 * (i / 15))
        if fill > 0:
            bar = Image.new('RGB', (fill, 8))
            for x in range(fill):
                c = lerp(hexrgb('#ff6600'), hexrgb('#ffcc66'), x / 318)
                ImageDraw.Draw(bar).line([(x, 0), (x, 7)], fill=c)
            fr.paste(bar, (3, 3))
        frames.append(fr.convert('P', palette=Image.ADAPTIVE, colors=64))
    frames[0].save(out / '01-loader.gif', save_all=True, append_images=frames[1:],
                   duration=[150] * 15 + [4000], loop=0)

    # Mobile: full-width (358 x 44) tab images and the full-width header background
    def mobile_tab(label, state, name):
        W, H = 358, 44
        if state == 'on':
            im = vgrad(W, H, [(0, '#ff8833'), (1, '#cc5200')])
            border, ink = '#ff6600', '#ffffff'
        elif state == 'over':
            im = vgrad(W, H, [(0, '#5a5f66'), (1, '#3a3e44')])
            border, ink = '#ff6600', '#ffcc66'
        else:
            im = vgrad(W, H, [(0, '#4a4e55'), (1, '#2a2d32')])
            border, ink = '#5a5f66', '#e6e6e6'
        d = ImageDraw.Draw(im)
        d.rectangle([0, 0, W - 1, H - 1], outline=border)
        t = pixel_text(label.upper(), color=ink)
        im.paste(t, (16, (H - t.height) // 2), t)
        if state == 'on':
            a = pixel_text('>', color=ink)
            im.paste(a, (W - 16 - a.width, (H - a.height) // 2), a)
        save_gif(im, out, name)

    for key, label in L['nav']:
        for st in ('on', 'off', 'over'):
            mobile_tab(ascii_text(label), st, f'01m-tab-{key}-{st}.gif')

    hd = Image.new('RGB', (390, 440))
    dd = ImageDraw.Draw(hd)
    for y in range(440):
        for x in range(0, 390, 2):
            dd.line([(x, y), (x + 1, y)], fill=lerp((0x3a, 0x3e, 0x44), (0x1f, 0x22, 0x26), min(1, (x * 0.35 + y) / 420)))
    hd.save(out / '01m-header.jpg', quality=88)


# ======================= 2006 =======================
def make_2006(out, L):
    vgrad(8, 360, [(0, '#cfe3f2'), (1, '#e9f0f5')]).save(out / '06-bg.png')

    def rounded_mask(w, h, r, corners=(1, 1, 1, 1)):
        m = Image.new('L', (w * 4, h * 4), 0)
        ImageDraw.Draw(m).rounded_rectangle([0, 0, w * 4 - 1, h * 4 - 1], radius=r * 4, fill=255,
                                            corners=tuple(bool(c) for c in corners))
        return m.resize((w, h), Image.LANCZOS)

    def gloss(w, h, top, mid, low, bottom, r, name, corners=(1, 1, 1, 1), border=None):
        im = vgrad(w, h, [(0, top), (0.5, mid), (0.51, low), (1, bottom)]).convert('RGBA')
        if border:
            bd = Image.new('RGBA', (w, h), hexrgb(border) + (255,))
            inner = rounded_mask(w - 2, h - 2, max(1, r - 1), corners)
            bd.paste(im.crop((1, 1, w - 1, h - 1)), (1, 1), inner)
            im = bd
        im.putalpha(rounded_mask(w, h, r, corners))
        im.save(out / name)

    # Tabs (sliding doors): wide left piece + right cap
    gloss(400, 44, '#3375b8', '#2a6aa8', '#1d5a96', '#1f5f9e', 10, '06-tab-off-l.png', corners=(1, 0, 0, 0))
    gloss(12, 44, '#3375b8', '#2a6aa8', '#1d5a96', '#1f5f9e', 10, '06-tab-off-r.png', corners=(0, 1, 0, 0))
    gloss(400, 44, '#ffffff', '#ffffff', '#ffffff', '#ffffff', 10, '06-tab-on-l.png', corners=(1, 0, 0, 0))
    gloss(12, 44, '#ffffff', '#ffffff', '#ffffff', '#ffffff', 10, '06-tab-on-r.png', corners=(0, 1, 0, 0))
    # Gloss buttons (fixed width, sidebar)
    gloss(250, 44, '#3375b8', '#2a6aa8', '#1d5a96', '#1f5f9e', 10, '06-btn-blue.png', border='#174a7c')
    gloss(250, 44, '#5a8f2a', '#4f8224', '#437320', '#467a21', 10, '06-btn-green.png', border='#355d18')

    # Sidebar box top (header) and bottom
    def box_top(w, h, name):
        im = vgrad(w, h, [(0, '#f7fafc'), (1, '#dde9f2')]).convert('RGBA')
        d = ImageDraw.Draw(im)
        d.line([(0, h - 1), (w, h - 1)], fill='#d5e2ec')
        border = Image.new('RGBA', (w, h), hexrgb('#d5e2ec') + (255,))
        inner = rounded_mask(w - 2, h - 1, 11, (1, 1, 0, 0))
        border.paste(im.crop((1, 1, w - 1, h)), (1, 1), inner)
        border.putalpha(rounded_mask(w, h, 12, (1, 1, 0, 0)))
        border.save(out / name)

    def box_bottom(w, h, name, fill='#ffffff', line='#d5e2ec'):
        im = Image.new('RGBA', (w, h), hexrgb(line) + (255,))
        inner = rounded_mask(w - 2, h - 1, 11, (0, 0, 1, 1))
        im.paste(Image.new('RGBA', (w - 2, h - 1), hexrgb(fill) + (255,)), (1, 0), inner)
        im.putalpha(rounded_mask(w, h, 12, (0, 0, 1, 1)))
        im.save(out / name)

    box_top(280, 40, '06-box-top.png')
    box_bottom(280, 14, '06-box-bot.png')

    # Main panel bottom with soft shadow
    pb = Image.new('RGBA', (960, 26), (0, 0, 0, 0))
    sh = Image.new('RGBA', (960, 26), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle([4, -20, 955, 18], radius=14, fill=(0, 0, 0, 60))
    sh = sh.filter(ImageFilter.GaussianBlur(4))
    pb.alpha_composite(sh)
    panel = Image.new('RGBA', (960, 16), (255, 255, 255, 255))
    panel.putalpha(rounded_mask(960, 16, 14, (0, 0, 1, 1)))
    pb.alpha_composite(panel, (0, 0))
    pb.save(out / '06-panel-bot.png')
    # Liquid layout: the panel bottom is sliced into left corner, 1px repeating middle, right corner.
    pb.crop((0, 0, 40, 26)).save(out / '06-panel-bot-l.png')
    pb.crop((920, 0, 960, 26)).save(out / '06-panel-bot-r.png')
    pb.crop((480, 0, 481, 26)).save(out / '06-panel-bot-m.png')

    # Logo with baked reflection and beta starburst
    f = ImageFont.truetype(SANS_B, 52)
    text = L['name']
    chars = []
    x = 0
    for ch in text:  # tight tracking (-2px)
        chars.append((ch, x))
        x += f.getlength(ch) - 2
    tw = int(x) + 4
    th = 60
    word = Image.new('RGBA', (tw, th), (0, 0, 0, 0))
    dw = ImageDraw.Draw(word)
    for ch, cx in chars:
        dw.text((cx, 0), ch, font=f, fill=hexrgb('#1d5a96') + (255,))
    wb = word.getbbox()
    word = word.crop((0, wb[1], tw, wb[3]))
    W, H = word.width + 80, word.height + 40 + 20
    logo = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    logo.alpha_composite(word, (0, 20))
    refl = word.transpose(Image.FLIP_TOP_BOTTOM)
    ra = refl.split()[3]  # reflection alpha: original alpha scaled by a fade ramp
    ramp = Image.new('L', refl.size, 0)
    for y in range(refl.height):
        ImageDraw.Draw(ramp).line([(0, y), (refl.width, y)], fill=max(0, int(255 * (1 - y / (refl.height * 0.6)))))
    refl.putalpha(ImageChops.multiply(ra.point(lambda v: v * 50 // 255), ramp))
    logo.alpha_composite(refl, (0, 20 + word.height + 1))
    # beta starburst
    burst = Image.new('RGBA', (64 * 4, 64 * 4), (0, 0, 0, 0))
    db = ImageDraw.Draw(burst)
    pts = []
    for i in range(32):
        ang = math.pi * 2 * i / 32
        rr = 124 if i % 2 == 0 else 104
        pts.append((128 + rr * math.cos(ang), 128 + rr * math.sin(ang)))
    db.polygon(pts, fill=hexrgb('#7ac143') + (255,))
    burst = burst.resize((64, 64), Image.LANCZOS).rotate(-14, resample=Image.BICUBIC)
    bt = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
    ImageDraw.Draw(bt).text((32, 32), L['eras']['2006']['ui']['beta'], font=ImageFont.truetype(SANS_B, 15),
                            fill=hexrgb('#1f3a0d') + (255,), anchor='mm')
    bt = bt.rotate(-14, resample=Image.BICUBIC)
    burst.alpha_composite(bt)
    logo.alpha_composite(burst, (word.width + 8, 0))
    logo.save(out / '06-logo.png')


def main():
    global SANS_B, MONO_B
    ap = argparse.ArgumentParser(description=__doc__.split('\n\n')[0])
    ap.add_argument('--only', choices=GROUPS, action='append',
                    help="draw only this group (repeatable): shared (the square headshot, used by every older "
                         "era), 1996 (includes the badges and thumbnails), 2001 (includes the mobile tabs), "
                         "2006, badges, or thumbs. Default: all.")
    ap.add_argument('--out', type=Path, default=ROOT / 'assets' / 'eras',
                    help='output folder; each era gets its own subfolder (default: assets/eras)')
    ap.add_argument('--fonts', type=Path, default=ROOT / 'scripts' / 'fonts',
                    help='folder with LiberationSans-Bold.ttf and LiberationMono-Bold.ttf '
                         '(default: the copies in scripts/fonts)')
    args = ap.parse_args()
    SANS_B = str(args.fonts / 'LiberationSans-Bold.ttf')
    MONO_B = str(args.fonts / 'LiberationMono-Bold.ttf')
    for f in (SANS_B, MONO_B):
        if not Path(f).is_file():
            sys.exit(f'font not found: {f}')

    want = set(args.only or GROUPS)
    if '1996' in want:
        want |= {'badges', 'thumbs'}  # the 1996 group includes the badges and case-study thumbnails
    L = read_labels()
    steps = [('shared', '.', make_headshot), ('1996', '1996', make_1996), ('badges', '1996', make_badges), ('thumbs', '1996', make_thumbs),
             ('2001', '2001', make_2001), ('2006', '2006', make_2006)]
    for group, folder, fn in steps:
        if group in want:
            out = args.out / folder
            out.mkdir(parents=True, exist_ok=True)
            fn(out, L)
            print(f'{group}: wrote to {out}')


if __name__ == '__main__':
    main()
