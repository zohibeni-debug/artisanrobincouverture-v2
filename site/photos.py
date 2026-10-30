# -*- coding: utf-8 -*-
"""Prépare les photos du site à partir de site/photos-src/.

Rangement conseillé : un dossier par sujet, le nom du dossier sert d'étiquette.
    site/photos-src/tuiles/chantier-lagny-01.jpg
    site/photos-src/zinc/gouttiere-dampmart.jpg
    site/photos-src/avant-apres/refection-thorigny-avant.jpg   (+ ...-apres.jpg : paire avant/après)
Étiquettes reconnues : tuiles, ardoise, zinc, gouttiere, echafaudage, chantier, demoussage, velux,
charpente, urgence, isolation, cheminee, toit-plat, avant-apres, equipe.

site/photos_manifest.json (facultatif) précise, pour une photo (clé = nom de fichier sans extension) :
    {"alt": "...", "tags": ["tuiles", "chantier"], "city": "Lagny-sur-Marne", "hero": true}

Le script produit site/img-out/<clé>-<largeur>.webp (480, 960, 1600 px, sans agrandir) et site/photos.json.
Usage : python3 site/photos.py, puis python3 site/build.py
"""
import json
import os
import re
import shutil
import unicodedata

from PIL import Image, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.environ.get("PHOTOS_SRC") or os.path.join(HERE, "photos-src")
OUT = os.environ.get("IMG_OUT") or os.path.join(HERE, "img-out")
MANIFEST = os.environ.get("PHOTOS_MANIFEST") or os.path.join(HERE, "photos_manifest.json")
JSON_OUT = os.environ.get("PHOTOS_JSON") or os.path.join(HERE, "photos.json")
WIDTHS = [480, 960, 1600]
TAGS = {"tuiles", "ardoise", "zinc", "gouttiere", "echafaudage", "chantier", "demoussage", "velux", "charpente",
        "urgence", "isolation", "cheminee", "toit-plat", "avant-apres", "equipe"}


def slug(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


def main():
    if not os.path.isdir(SRC):
        print("Aucun dossier site/photos-src : rien à faire.")
        return
    man = json.load(open(MANIFEST, encoding="utf-8")) if os.path.exists(MANIFEST) else {}
    if os.path.exists(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)
    meta = {}
    for dp, _, files in sorted(os.walk(SRC)):
        for f in sorted(files):
            if not f.lower().endswith((".jpg", ".jpeg", ".png", ".webp", ".heic")):
                continue
            stem = os.path.splitext(f)[0]
            key = slug(stem)
            folder = slug(os.path.basename(dp)) if dp != SRC else ""
            m = man.get(stem) or man.get(key) or {}
            tags = list(dict.fromkeys(([folder] if folder in TAGS else []) + [t for t in m.get("tags", []) if t in TAGS]))
            if not tags:
                tags = ["chantier"]
            im = ImageOps.exif_transpose(Image.open(os.path.join(dp, f))).convert("RGB")
            W = im.size[0]
            widths = [w for w in WIDTHS if w < W] + [min(W, WIDTHS[-1])]
            for w in widths:
                h = round(im.size[1] * w / W)
                im.resize((w, h), Image.LANCZOS).save(os.path.join(OUT, f"{key}-{w}.webp"), "WEBP", quality=80, method=6)
            pair = None
            if key.endswith("-avant") or key.endswith("-apres"):
                pair = key.rsplit("-", 1)[0]
            meta[key] = {"w": im.size[0], "h": im.size[1], "sizes": widths, "alt": m.get("alt", ""), "tags": tags,
                         "city": m.get("city", ""), "hero": bool(m.get("hero")), "pair": pair, "label": m.get("label", ""),
                         "role": key.rsplit("-", 1)[1] if pair else ""}
            print(f"{key:40} {im.size[0]}x{im.size[1]} {','.join(tags)}")
    json.dump(meta, open(JSON_OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    sans_alt = [k for k, v in meta.items() if not v["alt"]]
    print(f"{len(meta)} photos prêtes.")
    if sans_alt:
        print("Photos sans texte alternatif (à compléter dans photos_manifest.json) :", ", ".join(sans_alt))


if __name__ == "__main__":
    main()
