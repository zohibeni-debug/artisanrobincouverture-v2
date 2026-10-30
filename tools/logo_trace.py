# -*- coding: utf-8 -*-
"""Vectorise le logo Artisan Robin (site/brand-src/logo-artisan-robin.png) en groupes SVG.

Sortie : site/logo_parts.json  { groupe: {"color": "red"|"dark"|"gray", "d": "<path>", "box": [x0,y0,x1,y1]} }
Groupes : bars (bandes rouges), roof (chevron noir), shadow (ombre grise), title (ARTISAN ROBIN), tagline.
Coordonnées dans le repère de l'image d'origine (512 x 512).
"""
import json, os
import numpy as np
import potrace
from PIL import Image
from scipy import ndimage

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S = 4  # suréchantillonnage pour des courbes nettes
im = Image.open(os.path.join(ROOT, "site", "brand-src", "logo-artisan-robin.png")).convert("RGB")
im = im.resize((im.width * S, im.height * S), Image.LANCZOS)
a = np.asarray(im).astype(float)
P = {"white": (255, 255, 255), "red": (209, 15, 24), "dark": (31, 31, 31), "gray": (162, 162, 162)}
names = list(P)
d = np.stack([((a - np.array(P[n])) ** 2).sum(2) for n in names])
cls = d.argmin(0)
H, W = cls.shape


def mask(name, y0=0, y1=None, min_size=40, x0=0, x1=512):
    m = cls == names.index(name)
    out = np.zeros_like(m)
    out[y0 * S:(y1 or 512) * S, x0 * S:x1 * S] = m[y0 * S:(y1 or 512) * S, x0 * S:x1 * S]
    lab, n = ndimage.label(out)
    if n:
        sizes = ndimage.sum(out, lab, range(1, n + 1))
        keep = np.isin(lab, [i + 1 for i, s in enumerate(sizes) if s >= min_size * S * S])
        out = keep
    out = ndimage.binary_closing(out, iterations=1)
    return out


def trace(m):
    bm = potrace.Bitmap(~m)
    path = bm.trace(turdsize=8 * S, turnpolicy=potrace.POTRACE_TURNPOLICY_MINORITY, alphamax=1.0, opticurve=True, opttolerance=0.2)
    parts = []
    f = lambda p: f"{p.x / S:.2f} {p.y / S:.2f}"
    for c in path:
        parts.append("M" + f(c.start_point))
        for seg in c.segments:
            if seg.is_corner:
                parts.append("L" + f(seg.c) + "L" + f(seg.end_point))
            else:
                parts.append("C" + f(seg.c1) + " " + f(seg.c2) + " " + f(seg.end_point))
        parts.append("Z")
    ys, xs = np.nonzero(m)
    return "".join(parts), [round(xs.min() / S, 1), round(ys.min() / S, 1), round(xs.max() / S, 1), round(ys.max() / S, 1)]


groups = {
    "bars": ("red", mask("red", 0, 295, 60)),
    "roof": ("dark", mask("dark", 0, 295, 60)),
    "shadow": ("gray", mask("gray", 180, 290, 300, 320, 412)),
    "title": ("dark", mask("dark", 300, 352, 2)),
    "tagline": ("dark", mask("dark", 354, 390, 1)),
}
out = {}
for k, (col, m) in groups.items():
    dd, box = trace(m)
    out[k] = {"color": col, "d": dd, "box": box}
    print(k, col, box, len(dd))
json.dump(out, open(os.path.join(ROOT, "site", "logo_parts.json"), "w"), indent=0)
