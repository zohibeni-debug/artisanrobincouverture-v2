# -*- coding: utf-8 -*-
"""Communes de la zone d'intervention autour de Thorigny-sur-Marne.

Données : data/communes_base.json (INSEE et Etalab « découpage administratif » pour les codes, populations
et intercommunalités ; GeoNames pour les coordonnées) et data/communes_notes_A.json / _B.json
(bâti, patrimoine, risques, quartiers : recherches documentées, sources dans les fichiers).
"""
import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(HERE, "data")
COMMUNES = json.load(open(os.path.join(D, "communes_base.json"), encoding="utf-8"))
NOTES = {}
for f in ("communes_notes_A.json", "communes_notes_B.json"):
    p = os.path.join(D, f)
    if os.path.exists(p):
        for n in json.load(open(p, encoding="utf-8")):
            old = NOTES.get(n["slug"])
            if not old or len(n.get("bati") or "") > len(old.get("bati") or ""):
                NOTES[n["slug"]] = n
for c in COMMUNES:
    n = NOTES.get(c["slug"], {})
    c["bati"] = (n.get("bati") or "").strip()
    c["patrimoine"] = (n.get("patrimoine") or "").strip()
    c["risques"] = (n.get("risques") or "").strip()
    c["quartiers"] = [q for q in (n.get("quartiers") or []) if q][:6]
    c["reperes"] = [r for r in (n.get("reperes") or []) if r][:4]
    c["sources"] = n.get("sources") or []
    c["dist_label"] = f"{c['dist']:.1f}".replace(".", ",")

BY_SLUG = {c["slug"]: c for c in COMMUNES}
CENTER = (48.88689, 2.71806)  # Thorigny-sur-Marne
GROUPS = list(dict.fromkeys(c["group"] for c in COMMUNES))

VOWELS = "AEIOUYÉÈÊÂÎ"


def a_(name):
    """« à Lagny-sur-Marne », « au Pin »."""
    if name.startswith("Le "):
        return "au " + name[3:]
    if name.startswith("Les "):
        return "aux " + name[4:]
    return "à " + name


def de_(name):
    """« de Lagny-sur-Marne », « d'Esbly », « du Pin »."""
    if name.startswith("Le "):
        return "du " + name[3:]
    if name.startswith("Les "):
        return "des " + name[4:]
    if name[0].upper() in VOWELS:
        return "d'" + name
    return "de " + name


def direction(b):
    names = ["nord", "nord-est", "est", "sud-est", "sud", "sud-ouest", "ouest", "nord-ouest"]
    return names[int((b + 22.5) % 360 // 45)]


def dist(c1, c2):
    R = 6371
    p1, p2 = math.radians(c1["lat"]), math.radians(c2["lat"])
    dp, dl = p2 - p1, math.radians(c2["lon"] - c1["lon"])
    x = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * R * math.asin(math.sqrt(x))


def neighbours(c, n=6):
    others = [o for o in COMMUNES if o["slug"] != c["slug"]]
    return sorted(others, key=lambda o: dist(c, o))[:n]


def pop_label(p):
    if not p:
        return ""
    if p >= 10000:
        return f"{round(p / 1000):d} 000 habitants".replace("000 000", "000")
    return f"{p:,} habitants".replace(",", " ")
