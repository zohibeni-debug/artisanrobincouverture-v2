# -*- coding: utf-8 -*-
"""Prépare les photos de chantier envoyées par le client (site/photos-originaux/) :
floute les plaques d'immatriculation et l'affiche d'une agence immobilière, aligne les paires avant/après,
range chaque photo dans site/photos-src/<sujet>/ et écrit site/photos_manifest.json.
Usage : python3 tools/prep_photos.py, puis python3 site/photos.py et python3 site/build.py
"""
import glob, json, os, shutil
import cv2
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "site", "photos-originaux")
DST = os.path.join(ROOT, "site", "photos-src")


def load(k):
    return cv2.imread(glob.glob(os.path.join(SRC, k + "-*"))[0], cv2.IMREAD_COLOR)


def blur(im, box, k=31):
    x0, y0, x1, y1 = box
    roi = im[y0:y1, x0:x1]
    small = cv2.resize(roi, (max(1, (x1 - x0) // 10), max(1, (y1 - y0) // 10)), interpolation=cv2.INTER_LINEAR)
    im[y0:y1, x0:x1] = cv2.GaussianBlur(cv2.resize(small, (x1 - x0, y1 - y0), interpolation=cv2.INTER_NEAREST), (k | 1, k | 1), 0)
    return im


def align(src, ref):
    """Recale la photo src sur ref (homographie SIFT) et recadre les deux sur la zone commune."""
    sift = cv2.SIFT_create(6000)
    g1, g2 = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY), cv2.cvtColor(ref, cv2.COLOR_BGR2GRAY)
    k1, d1 = sift.detectAndCompute(g1, None)
    k2, d2 = sift.detectAndCompute(g2, None)
    m = cv2.BFMatcher().knnMatch(d1, d2, k=2)
    good = [a for a, b in m if a.distance < 0.72 * b.distance]
    p1 = np.float32([k1[a.queryIdx].pt for a in good]).reshape(-1, 1, 2)
    p2 = np.float32([k2[a.trainIdx].pt for a in good]).reshape(-1, 1, 2)
    H, mask = cv2.findHomography(p1, p2, cv2.RANSAC, 4.0)
    h, w = ref.shape[:2]
    warped = cv2.warpPerspective(src, H, (w, h))
    valid = cv2.warpPerspective(np.full(src.shape[:2], 255, np.uint8), H, (w, h))
    ys, xs = np.where(valid > 0)
    # plus grand rectangle d'aspect 4:3 entièrement couvert (recherche simple par réduction)
    x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
    for _ in range(400):
        if valid[y0:y1, x0:x1].min() > 0:
            break
        x0 += 3; x1 -= 3; y0 += 2; y1 -= 2
    print(f"  recalage : {int(mask.sum())} points sur {len(good)}, zone {x0},{y0}-{x1},{y1}")
    return warped[y0:y1, x0:x1], ref[y0:y1, x0:x1]


PHOTOS = [
    # clé, dossier, nom, étiquettes, texte alternatif, options
    ("d904e5a8", "equipe", "couvreur-artisan-robin-chantier-pavillon", ["equipe", "tuiles", "chantier"],
     "Couvreur d'Artisan Robin sur une toiture en tuiles, monte-matériaux et camionnette de l'entreprise devant le pavillon", {"hero": True}),
    ("f0ddc527", "echafaudage", "refection-toiture-echafaudage-charpente", ["echafaudage", "charpente", "tuiles"],
     "Réfection de toiture sous échafaudage : charpente et liteaux neufs au faîtage, tuiles terre cuite", {"hero": True, "blur": [(385, 925, 605, 1030)]}),
    ("70d81940", "echafaudage", "refection-toiture-immeuble-echafaudage", ["echafaudage", "tuiles", "chantier"],
     "Réfection de la toiture d'un immeuble d'angle sous échafaudage, filets de protection en rive", {"hero": True}),
    ("ac73055d", "zinc", "gouttiere-descente-zinc-sous-face", ["zinc", "gouttiere"],
     "Gouttière et descente en zinc neuves, coudes façonnés, rive en tuiles et sous-face habillée", {}),
    ("1b9230a5", "gouttiere", "gouttiere-zinc-pignon", ["gouttiere", "zinc"],
     "Gouttière et descente en zinc posées le long d'un pignon, avant l'habillage de la sous-face", {}),
    ("daf5cd3c", "tuiles", "pavillon-toiture-refaite-rives-gouttieres", ["tuiles", "gouttiere", "equipe"],
     "Pavillon après réfection : couverture en tuiles mécaniques, rives et gouttières neuves, camionnette Artisan Robin", {}),
    ("cec69e9f", "chantier", "livraison-tuiles-camion-grue", ["chantier", "tuiles"],
     "Livraison des tuiles par camion-grue directement sur le toit en cours de réfection", {"blur": [(190, 905, 290, 938)]}),
    ("6d1db1db", "chantier", "pose-tuiles-liteaux-neufs", ["chantier", "tuiles", "charpente"],
     "Réfection en cours : tuiles réparties sur les liteaux neufs avant la pose", {"blur": [(245, 1452, 372, 1508)]}),
    ("f5a49f59", "tuiles", "rive-et-tuiles-neuves", ["tuiles", "zinc"],
     "Versant refait en tuiles mécaniques neuves, rive protégée par une bande métallique", {}),
    ("064f6f33", "echafaudage", "maison-echafaudage-versant-bache", ["echafaudage", "urgence", "chantier"],
     "Maison sous échafaudage, versant bâché pendant la réfection de la couverture", {"blur": [(285, 414, 357, 476), (812, 488, 868, 514)]}),
    ("57f3b334", "tuiles", "versant-tuiles-neuves-rive-bois", ["tuiles", "charpente", "cheminee"],
     "Versant refait en tuiles neuves, rive et bandeau en bois neufs, souche de cheminée en brique", {}),
    ("ddb26334", "chantier", "couvreurs-pose-tuiles-pavillon", ["chantier", "tuiles"],
     "Deux couvreurs posent les tuiles neuves sur les liteaux d'un pavillon", {"crop": (0, 0, 1600, 950)}),
    # Pendant / après du même pavillon : points de vue trop différents pour un curseur, publiées séparément
    ("340b4f73", "chantier", "refection-pavillon-cheminee-pendant", ["chantier", "tuiles", "cheminee"],
     "Pendant la réfection : liteaux neufs et pose des tuiles autour de la cheminée", {"crop": (0, 0, 1600, 960)}),
    ("ab2610b4", "tuiles", "refection-pavillon-cheminee-termine", ["tuiles", "cheminee", "equipe"],
     "Le même pavillon après réfection : tuiles neuves, rives et faîtage refaits", {"crop": (0, 0, 1600, 925)}),
]
PAIRS = [
    # (avant, après, nom de la paire, alt avant, alt après, étiquette avant, étiquette après)
    ("c392db33", "d85af613", "depose-pavillon-mitoyen",
     "Pavillon mitoyen avant la dépose : ancienne couverture en tuiles",
     "Même toiture après dépose : écran sous-toiture et liteaux neufs posés", "Avant", "Dépose faite", {"d85af613": [(703, 523, 752, 572)]}),
]

if os.path.exists(DST):
    shutil.rmtree(DST)
os.makedirs(DST)
man = {}
for k, folder, name, tags, alt, opt in PHOTOS:
    im = load(k)
    for b in opt.get("blur", []):
        im = blur(im, b)
    if opt.get("crop"):
        x0, y0, x1, y1 = opt["crop"]
        im = im[y0:y1, x0:x1]
    os.makedirs(os.path.join(DST, folder), exist_ok=True)
    cv2.imwrite(os.path.join(DST, folder, name + ".jpg"), im, [cv2.IMWRITE_JPEG_QUALITY, 93])
    man[name] = {"alt": alt, "tags": tags, "hero": bool(opt.get("hero"))}
    print(name)
for av, ap, name, alt_av, alt_ap, l_av, l_ap, blurs in PAIRS:
    a, b = load(av), load(ap)
    for b_ in blurs.get(ap, []):
        b = blur(b, b_)
    print(name)
    a2, b2 = align(a, b)
    os.makedirs(os.path.join(DST, "avant-apres"), exist_ok=True)
    cv2.imwrite(os.path.join(DST, "avant-apres", name + "-avant.jpg"), a2, [cv2.IMWRITE_JPEG_QUALITY, 93])
    cv2.imwrite(os.path.join(DST, "avant-apres", name + "-apres.jpg"), b2, [cv2.IMWRITE_JPEG_QUALITY, 93])
    man[name + "-avant"] = {"alt": alt_av, "tags": ["avant-apres", "tuiles", "chantier"], "label": l_av}
    man[name + "-apres"] = {"alt": alt_ap, "tags": ["avant-apres", "tuiles", "chantier"], "label": l_ap}
open(os.path.join(DST, ".gitkeep"), "w").close()
json.dump(man, open(os.path.join(ROOT, "site", "photos_manifest.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(len(man), "photos")
