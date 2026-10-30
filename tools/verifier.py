# -*- coding: utf-8 -*-
"""Contrôles du site généré : liens internes, balises, données structurées, anciennes adresses (pages ou redirections 301)."""
import json, os, re, sys
from html.parser import HTMLParser
from collections import Counter, defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUB = os.environ.get("PUBLIC_DIR") or os.path.join(ROOT, "public")
sys.path.insert(0, os.path.join(ROOT, "site"))
import content as C  # noqa: E402

OLD = ["/", "/a-propos", "/tarifs", "/blog", "/contact", "/realisations", "/zones", "/couverture", "/temoignages", "/mentions-legales", "/politique-de-confidentialite"]
OLD += ["/couverture/" + s for s in "pose-toiture reparation-entretien zinguerie-gouttieres isolation-toiture urgence-bachage charpente demoussage-nettoyage velux-fenetres-toit etancheite-toiture demoussage-nettoyage-toiture ramonage-cheminee bardage-facade amenagement-combles faitage-refection-cheminee".split()]
OLD += ["/blog/" + s for s in json.load(open(os.path.join(ROOT, "site", "data", "blog_list.json")))]
OLD += ["/zone/couvreur-" + s for s in C.OLD_ZONES]


class P(HTMLParser):
    def __init__(s):
        super().__init__(); s.links = []; s.ids = []; s.h1 = 0; s.title = ""; s.desc = None; s.canon = None; s.imgs_noalt = 0; s.ld = []; s._t = False; s._ld = False; s.text = []; s._main = 0; s._skip = 0; s.robots = ""

    def handle_starttag(s, t, a):
        a = dict(a)
        if "id" in a: s.ids.append(a["id"])
        if t == "a" and a.get("href"): s.links.append(a["href"])
        if t == "h1": s.h1 += 1
        if t == "title" and not s._skip and not s.title: s._t = True
        if t == "meta" and a.get("name") == "description": s.desc = a.get("content")
        if t == "meta" and a.get("name") == "robots": s.robots = a.get("content")
        if t == "link" and a.get("rel") == "canonical": s.canon = a.get("href")
        if t == "img" and "alt" not in a: s.imgs_noalt += 1
        if t == "img":
            s.links.append(a.get("src", ""))
            for part in (a.get("srcset") or "").split(","):
                if part.strip(): s.links.append(part.strip().split(" ")[0])
        if t == "link" and a.get("href", "").startswith("/"): s.links.append(a["href"])
        if t == "script" and a.get("src"): s.links.append(a["src"])
        if t == "script" and a.get("type") == "application/ld+json": s._ld = True; s.ld.append("")
        if t == "main": s._main += 1
        if t in ("script", "style", "svg"): s._skip += 1

    def handle_endtag(s, t):
        if t == "title": s._t = False
        if t == "script": s._ld = False
        if t in ("script", "style", "svg"): s._skip = max(0, s._skip - 1)

    def handle_data(s, d):
        if s._t: s.title += d
        if s._ld: s.ld[-1] += d
        elif s._main and not s._skip: s.text.append(d)


pages = {}
for dp, dn, fn in os.walk(PUB):
    for f in fn:
        if f.endswith(".html"):
            rel = "/" + os.path.relpath(os.path.join(dp, f), PUB)
            rel = rel[:-len("/index.html")] if rel.endswith("/index.html") else rel
            rel = rel or "/"
            if rel == "/index.html": rel = "/"
            p = P(); p.feed(open(os.path.join(dp, f), encoding="utf-8").read()); pages[rel] = p

redirects = {}
for line in open(os.path.join(PUB, "_redirects"), encoding="utf-8"):
    line = line.strip()
    if line and not line.startswith("#"):
        a, b, code = line.split()
        redirects[a] = b


def exists(path):
    path = path.split("#")[0].split("?")[0]
    if not path or path == "/": return True
    if path.endswith("/"): return False  # le site n'utilise pas de barre finale
    full = os.path.join(PUB, path.lstrip("/"))
    return os.path.isfile(full) or os.path.isfile(os.path.join(full, "index.html")) or os.path.isfile(full + ".html")


errors = []
titles, descs = Counter(), Counter()
inbound = defaultdict(int)
words = {}
for rel, p in sorted(pages.items()):
    if p.h1 != 1: errors.append(f"{rel}: {p.h1} h1")
    dup = [i for i, n in Counter(p.ids).items() if n > 1]
    if dup: errors.append(f"{rel}: ids en double {dup}")
    if p.imgs_noalt: errors.append(f"{rel}: {p.imgs_noalt} images sans alt")
    for l in p.links:
        if l.startswith("/") and not l.startswith("//"):
            if not exists(l): errors.append(f"{rel}: lien cassé {l}")
            else: inbound[l.split("#")[0]] += 1
    for j in p.ld:
        try: json.loads(j)
        except Exception as e: errors.append(f"{rel}: JSON-LD invalide {e}")
    if rel != "/404.html":
        titles[p.title] += 1; descs[p.desc] += 1
        if len(p.title) > 65: errors.append(f"{rel}: titre long ({len(p.title)}) {p.title}")
        if not p.desc or len(p.desc) > 165 or len(p.desc) < 90: errors.append(f"{rel}: description {len(p.desc or '')} car.")
        want = "https://artisanrobincouverture.fr" + rel
        if p.canon != want: errors.append(f"{rel}: canonical {p.canon}")
    words[rel] = len(re.findall(r"\w+", " ".join(p.text)))
for t, n in titles.items():
    if n > 1: errors.append(f"titre en double x{n}: {t}")
for d, n in descs.items():
    if n > 1: errors.append(f"description en double x{n}: {d}")
miss = []
for u in OLD:
    if u in pages: continue
    if u in redirects:
        if not exists(redirects[u]): errors.append(f"redirection vers une page absente : {u} -> {redirects[u]}")
        continue
    miss.append(u)
for u in miss: errors.append(f"ancienne adresse ni page ni redirection : {u}")
orph = [r for r in pages if r not in ("/404.html", "/") and inbound.get(r, 0) == 0]
sm = open(os.path.join(PUB, "sitemap.xml")).read()
print(f"{len(pages)} fichiers HTML, {len(OLD)} adresses de l'ancien site contrôlées ({sum(1 for u in OLD if u in pages)} pages, {sum(1 for u in OLD if u in redirects)} redirections), {sm.count('<loc>')} URL dans le sitemap")
print("pages sans lien entrant :", orph)
groups = defaultdict(list)
for r, n in words.items():
    groups["commune" if r.startswith("/zone/") else ("article" if r.startswith("/blog/") else ("service" if r.startswith("/couverture/") else "autres"))].append(n)
for k, v in groups.items(): print(f"mots {k:8} moyenne {sum(v) // len(v)} min {min(v)} max {max(v)}")
print("ERREURS :", len(errors))
for e in errors[:60]: print(" -", e)
sys.exit(1 if errors else 0)
