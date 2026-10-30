import os, sys, importlib.util
out = sys.argv[1]
# Reuse the helpers from gen.py without re-running it: exec only the definitions we need.
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'era-assets-gen.py')).read()
defs = src.split('# ======================= 1996 =======================')[0]
ns = {'__name__': 'x'}
import sys as _s; _s.argv = ['x', out]
exec(defs, ns)
vgrad, pixel_text, save_gif, ImageDraw = ns['vgrad'], ns['pixel_text'], ns['save_gif'], ns['ImageDraw']
W, H = 358, 44
def tab(label, state, name):
    if state == 'on':
        im = vgrad(W, H, [(0, '#ff8833'), (1, '#cc5200')]); border, ink = '#ff6600', '#ffffff'
    elif state == 'over':
        im = vgrad(W, H, [(0, '#5a5f66'), (1, '#3a3e44')]); border, ink = '#ff6600', '#ffcc66'
    else:
        im = vgrad(W, H, [(0, '#4a4e55'), (1, '#2a2d32')]); border, ink = '#5a5f66', '#e6e6e6'
    d = ImageDraw.Draw(im); d.rectangle([0, 0, W - 1, H - 1], outline=border)
    t = pixel_text(label.upper(), color=ink); im.paste(t, (16, (H - t.height) // 2), t)
    if state == 'on':
        a = pixel_text('>', color=ink); im.paste(a, (W - 16 - a.width, (H - a.height) // 2), a)
    save_gif(im, name)
for key, label in [('about','About'),('work','Work'),('resume','Resume'),('contact','Contact')]:
    for st in ('on','off','over'):
        tab(label, st, f'01m-tab-{key}-{st}.gif')
print(sorted(f for f in os.listdir(out) if f.startswith('01m-')))

# Full-width mobile header background (same diagonal gunmetal as the desktop side panel)
from PIL import Image as _I, ImageDraw as _D
def _lerp(a, b, t): return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))
_hd = _I.new('RGB', (390, 440)); _dd = _D.Draw(_hd)
for y in range(440):
    for x in range(0, 390, 2):
        _dd.line([(x, y), (x + 1, y)], fill=_lerp((0x3a, 0x3e, 0x44), (0x1f, 0x22, 0x26), min(1, (x * 0.35 + y) / 420)))
_hd.save(os.path.join(out, '01m-header.jpg'), quality=88)
