# -*- coding: utf-8 -*-
"""Aperçu local avec des emplacements photo factices (jamais publié) : montre où vont les photos.
Usage : python3 tools/apercu_photos.py  ->  preview/public (servir ce dossier pour voir le rendu)
"""
import json, os, random, subprocess, sys
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PV = os.path.join(ROOT, "preview")
SRC = os.path.join(PV, "photos-src")
os.makedirs(SRC, exist_ok=True)
LABELS = {"tuiles": "Toiture en tuiles", "ardoise": "Ardoise", "zinc": "Zinguerie", "gouttiere": "Gouttière", "echafaudage": "Échafaudage",
          "chantier": "Chantier", "demoussage": "Démoussage", "velux": "Fenêtre de toit", "charpente": "Charpente", "urgence": "Urgence",
          "isolation": "Isolation", "cheminee": "Cheminée", "toit-plat": "Toit plat", "avant-apres": "Avant / après"}
random.seed(4)
try:
    F = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 46)
    f2 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 30)
except Exception:
    F = f2 = ImageFont.load_default()
man = {}
def make(name, tag, size, hero=False, shade=0):
    W, H = size
    im = Image.new("RGB", (W, H), (46 + shade, 46 + shade, 48 + shade))
    d = ImageDraw.Draw(im)
    for i in range(-H, W, 60):
        d.line([(i, H), (i + H, 0)], fill=(54 + shade, 54 + shade, 57 + shade), width=22)
    cx, cy = W // 2, H // 2 - 30
    d.rounded_rectangle([cx - 70, cy - 45, cx + 70, cy + 50], 14, outline=(209, 15, 24), width=8)
    d.ellipse([cx - 28, cy - 22, cx + 28, cy + 34], outline=(209, 15, 24), width=8)
    d.rectangle([cx - 30, cy - 62, cx + 10, cy - 45], fill=(209, 15, 24))
    t = "EMPLACEMENT PHOTO"
    d.text((cx, cy + 100), t, font=F, fill=(240, 240, 240), anchor="mm")
    d.text((cx, cy + 150), LABELS.get(tag, tag), font=f2, fill=(190, 190, 190), anchor="mm")
    p = os.path.join(SRC, tag); os.makedirs(p, exist_ok=True)
    im.save(os.path.join(p, name + ".jpg"), quality=70)
    man[name] = {"alt": f"Emplacement photo : {LABELS.get(tag, tag)}", "tags": [tag], "hero": hero}
sizes = [(1600, 1200), (1200, 1600), (1600, 900), (1600, 1200), (1600, 1067)]
i = 0
for tag, n in (("tuiles", 6), ("echafaudage", 4), ("chantier", 5), ("zinc", 3), ("gouttiere", 3), ("charpente", 2), ("velux", 2), ("demoussage", 2), ("cheminee", 2), ("urgence", 1), ("isolation", 1), ("ardoise", 1), ("toit-plat", 1)):
    for k in range(n):
        make(f"{tag}-{k + 1}", tag, sizes[i % len(sizes)], hero=(tag in ("echafaudage", "tuiles") and k == 0))
        i += 1
for k in range(2):
    make(f"refection-{k + 1}-avant", "avant-apres", (1600, 1200), shade=-12)
    make(f"refection-{k + 1}-apres", "avant-apres", (1600, 1200), shade=14)
json.dump(man, open(os.path.join(PV, "manifest.json"), "w"), ensure_ascii=False)
env = dict(os.environ, PHOTOS_SRC=SRC, IMG_OUT=os.path.join(PV, "img-out"), PHOTOS_MANIFEST=os.path.join(PV, "manifest.json"),
           PHOTOS_JSON=os.path.join(PV, "photos.json"), PUBLIC_DIR=os.path.join(PV, "public"))
subprocess.run([sys.executable, os.path.join(ROOT, "site", "photos.py")], env=env, check=True, stdout=subprocess.DEVNULL)
subprocess.run([sys.executable, os.path.join(ROOT, "site", "build.py")], env=env, check=True)
