# -*- coding: utf-8 -*-
"""Dessins SVG : carte des communes et visuels de remplacement quand une photo manque."""
import html
import math

import communes as CM

RED, INK, GRAY = "#d10f18", "#161616", "#a3a3a3"


def _xy(lat, lon, scale, cx, cy):
    kx = 111.32 * math.cos(math.radians(CM.CENTER[0]))
    x = (lon - CM.CENTER[1]) * kx * scale + cx
    y = -(lat - CM.CENTER[0]) * 110.57 * scale + cy
    return x, y


def zone_map(current=None, links=True, cls="map", title="Carte des communes"):
    W, H = 640, 600
    cx, cy, s = W / 2 - 10, H / 2 + 10, 22.5  # px par km
    out = [f'<svg class="{cls}" viewBox="0 0 {W} {H}" role="img" aria-label="{html.escape(title)}">']
    out.append(f'<rect width="{W}" height="{H}" fill="none"/>')
    for r, lab in ((5, "5 km"), (10, "10 km")):
        out.append(f'<circle cx="{cx}" cy="{cy}" r="{r * s}" fill="none" stroke="currentColor" stroke-opacity=".18" stroke-dasharray="3 5"/>')
        out.append(f'<text x="{cx + r * s * .7071 + 4:.0f}" y="{cy - r * s * .7071 - 4:.0f}" class="map-km">{lab}</text>')
    big = {"Thorigny-sur-Marne", "Lagny-sur-Marne", "Chelles", "Torcy", "Bussy-Saint-Georges", "Montévrain", "Chessy", "Serris",
           "Claye-Souilly", "Villeparisis", "Noisiel", "Vaires-sur-Marne", "Esbly", "Pomponne", "Dampmart", "Champs-sur-Marne",
           "Noisy-le-Grand", "Mitry-Mory", "Lognes", "Saint-Thibault-des-Vignes", "Annet-sur-Marne", "Coupvray", "Magny-le-Hongre"}
    labels = []
    for c in sorted(CM.COMMUNES, key=lambda c: -c["dist"]):
        x, y = _xy(c["lat"], c["lon"], s, cx, cy)
        if not (8 < x < W - 8 and 8 < y < H - 8):
            continue
        main = c["slug"] == "thorigny-sur-marne"
        here = current and c["slug"] == current["slug"]
        r = 7 if main or here else (4.5 if (c["pop"] or 0) > 10000 else 3.4)
        cl = "map-dot" + (" is-main" if main else "") + (" is-here" if here else "")
        dot = f'<circle class="{cl}" cx="{x:.1f}" cy="{y:.1f}" r="{r}"/>'
        name = html.escape(c["name"])
        if links and not here:
            href = "/" if main else f"/zone/couvreur-{c['slug']}"
            out.append(f'<a href="{href}" class="map-a"><title>Couvreur {html.escape(CM.a_(c["name"]))}</title>{dot}</a>')
        else:
            out.append(dot)
        if c["name"] in big or here:
            labels.append((x, y, name, main or here))
    boxes = []
    prio = sorted(labels, key=lambda l: (not l[3], -(next((c["pop"] or 0) for c in CM.COMMUNES if html.escape(c["name"]) == l[2]))))
    for x, y, name, strong in prio:
        wtxt = len(html.unescape(name)) * (8.4 if strong else 6.6)
        for anchor, dx, dy in (("start", 9, 4), ("end", -9, 4), ("start", 7, -9), ("start", 7, 16), ("end", -7, -9), ("end", -7, 16)):
            x0 = x + dx if anchor == "start" else x + dx - wtxt
            if x0 < 2 or x0 + wtxt > W - 2:
                continue
            bb = (x0 - 2, y + dy - 12, x0 + wtxt + 2, y + dy + 3)
            if all(bb[2] < o[0] or bb[0] > o[2] or bb[3] < o[1] or bb[1] > o[3] for o in boxes):
                boxes.append(bb)
                out.append(f'<text x="{x + dx:.1f}" y="{y + dy:.1f}" text-anchor="{anchor}" class="map-l{" is-strong" if strong else ""}">{name}</text>')
                break
    out.append("</svg>")
    return "".join(out)


def tile(kind, uid, label="", cls="tile"):
    """Visuel dessiné aux couleurs de la marque, utilisé tant qu'une photo n'est pas disponible."""
    p = f"t{uid}"
    W, H = 800, 600
    if kind in ("ardoise",):
        pat = (f'<pattern id="{p}" width="60" height="44" patternUnits="userSpaceOnUse">'
               f'<rect width="60" height="44" fill="#2a2c30"/><path d="M0 22h60M30 0v22M0 22v22M60 22v22" stroke="#1b1c1f" stroke-width="3"/>'
               f'<rect x="2" y="2" width="26" height="18" rx="2" fill="#34373c"/><rect x="32" y="2" width="26" height="18" rx="2" fill="#30333a"/>'
               f'<rect x="-13" y="24" width="26" height="18" rx="2" fill="#2f3237"/><rect x="17" y="24" width="26" height="18" rx="2" fill="#383b41"/><rect x="47" y="24" width="26" height="18" rx="2" fill="#2f3237"/></pattern>')
    elif kind in ("zinc", "toit-plat", "gouttiere"):
        pat = (f'<pattern id="{p}" width="70" height="70" patternUnits="userSpaceOnUse">'
               f'<rect width="70" height="70" fill="#8d9196"/><rect width="35" height="70" fill="#979b a0" opacity="0"/>'
               f'<rect x="0" width="4" height="70" fill="#c9ccd0"/><rect x="4" width="3" height="70" fill="#6c7075"/></pattern>').replace("#979b a0", "#979ba0")
    elif kind in ("charpente", "isolation"):
        pat = (f'<pattern id="{p}" width="120" height="120" patternUnits="userSpaceOnUse">'
               f'<rect width="120" height="120" fill="#e9dcc6"/><rect x="0" y="0" width="16" height="120" fill="#c79a5e"/><rect x="60" y="0" width="16" height="120" fill="#c79a5e"/>'
               f'<path d="M0 30h120M0 90h120" stroke="#b78a4f" stroke-width="10"/></pattern>')
    else:  # tuiles
        pat = (f'<pattern id="{p}" width="56" height="40" patternUnits="userSpaceOnUse">'
               f'<rect width="56" height="40" fill="#7d2a1d"/>'
               f'<path d="M0 30 q14 -18 28 0 q14 -18 28 0 v10 h-56z" fill="#a33a26"/><path d="M0 30 q14 -18 28 0 q14 -18 28 0" fill="none" stroke="#5e1f15" stroke-width="3"/>'
               f'<path d="M14 21v-21M42 21v-21" stroke="#8e3121" stroke-width="2"/></pattern>')
    lab = f'<title>{html.escape(label)}</title>' if label else ""
    role = 'role="img"' if label else 'aria-hidden="true"'
    return (f'<svg class="{cls}" viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMid slice" {role}>{lab}<defs>{pat}'
            f'<linearGradient id="g{p}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#000" stop-opacity=".05"/><stop offset="1" stop-color="#000" stop-opacity=".55"/></linearGradient></defs>'
            f'<rect width="{W}" height="{H}" fill="url(#{p})" transform="rotate(-8 400 300) scale(1.25) translate(-80 -60)"/>'
            f'<rect width="{W}" height="{H}" fill="url(#g{p})"/>'
            f'<g transform="translate(560 410) scale(.55)" opacity=".92"><path d="M0 140 L120 20 L240 140" fill="none" stroke="#fff" stroke-width="34" stroke-linejoin="miter"/>'
            f'<rect x="-210" y="40" width="150" height="22" fill="{RED}" transform="skewX(-30)"/><rect x="-210" y="78" width="150" height="22" fill="{RED}" transform="skewX(-30)"/><rect x="-210" y="116" width="150" height="22" fill="{RED}" transform="skewX(-30)"/></g>'
            f'</svg>')
