# -*- coding: utf-8 -*-
"""Logo Artisan Robin en SVG, à partir de site/logo_parts.json (voir tools/logo_trace.py).

Variantes : "stacked" (logo complet), "mark" (bandes et toit seuls), "horizontal" (toit à gauche, nom à droite).
Thèmes : "color" (fond clair), "light" (fond sombre : noir remplacé par blanc).
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
PARTS = json.load(open(os.path.join(HERE, "logo_parts.json")))
COLORS = {
    "color": {"red": "#d10f18", "dark": "#1c1c1c", "gray": "#a3a3a3"},
    "light": {"red": "#e3141d", "dark": "#ffffff", "gray": "#6d6d6d"},
}


def _paths(names, theme, extra=""):
    c = COLORS[theme]
    return "".join(f'<path class="lg-{n}" fill="{c[PARTS[n]["color"]]}" fill-rule="evenodd" d="{PARTS[n]["d"]}"{extra}/>' for n in names)


def svg(variant="stacked", theme="color", title="Artisan Robin, charpentier couvreur zingueur", cls="", animated=False):
    t = f"<title>{title}</title>" if title else ""
    a = ' aria-hidden="true"' if not title else ' role="img"'
    k = f' class="{cls}"' if cls else ""
    if variant == "mark":
        x0, y0, x1, y1 = 70, 124, 448, 287
        body = _paths(["bars", "shadow", "roof"], theme)
    elif variant == "horizontal":
        # Marque réduite à gauche, textes à droite
        mx0, my0, mx1, my1 = 70, 124, 448, 287
        s = 0.42
        mw, mh = (mx1 - mx0) * s, (my1 - my0) * s
        tx0, ty0, tx1, ty1 = 66, 306, 452, 378
        tw, th = tx1 - tx0, ty1 - ty0
        ts = mh / th
        gap = 14
        body = (f'<g transform="translate({-mx0 * s:.2f} {-my0 * s:.2f}) scale({s})">{_paths(["bars", "shadow", "roof"], theme)}</g>'
                f'<g transform="translate({mw + gap - tx0 * ts:.2f} {-ty0 * ts:.2f}) scale({ts:.4f})">{_paths(["title", "tagline"], theme)}</g>')
        W, Hh = mw + gap + tw * ts, mh
        return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W:.1f} {Hh:.1f}"{k}{a}>{t}{body}</svg>'
    else:
        x0, y0, x1, y1 = 62, 120, 456, 380
        body = _paths(["bars", "shadow", "roof", "title", "tagline"], theme)
    if animated:
        body = f'<g class="lg-anim">{body}</g>'
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0} {y0} {x1 - x0} {y1 - y0}"{k}{a}>{t}{body}</svg>'


def favicon():
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="49 -5 420 420">'
            '<rect x="49" y="-5" width="420" height="420" rx="64" fill="#fff"/>'
            f'{_paths(["bars", "shadow", "roof"], "color")}</svg>')
