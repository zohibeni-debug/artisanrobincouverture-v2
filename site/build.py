# -*- coding: utf-8 -*-
"""Générateur du site artisanrobincouverture.fr (ARTISAN ROBIN COUVERTURE, Thorigny-sur-Marne et alentour).

Usage : python3 site/build.py
Produit public/ : pages HTML complètes (lisibles sans JavaScript), plan du site, robots, redirections, en-têtes.
Les adresses des pages sont celles de l'ancien site, sans barre finale (/couverture/pose-toiture).
"""
import base64
import glob
import hashlib
import html
import json
import os
import re
import shutil
from datetime import date

import art
import communes as CM
import content as C
import logo as LG
import services as SV

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "site")
PUBLIC = os.environ.get("PUBLIC_DIR") or os.path.join(ROOT, "public")
IMG_OUT = os.environ.get("IMG_OUT") or os.path.join(SITE, "img-out")
PHOTOS_FILE = os.environ.get("PHOTOS_JSON") or os.path.join(SITE, "photos.json")
PHOTOS = json.load(open(PHOTOS_FILE, encoding="utf-8")) if os.path.exists(PHOTOS_FILE) else {}
TODAY = date.today().isoformat()
URL = C.SITE_URL
B = C.BUSINESS
PAGES = []
ASSETS = {}

BLOG = []
for f in sorted(glob.glob(os.path.join(SITE, "data", "blog", "*.json"))):
    BLOG.append(json.load(open(f, encoding="utf-8")))
BLOG_ORDER = json.load(open(os.path.join(SITE, "data", "blog_list.json"), encoding="utf-8"))
BLOG.sort(key=lambda a: BLOG_ORDER.index(a["slug"]) if a["slug"] in BLOG_ORDER else 99)
BLOG_BY = {a["slug"]: a for a in BLOG}
ZONES = [c for c in CM.COMMUNES if c["slug"] != "thorigny-sur-marne"]
THORIGNY = CM.BY_SLUG["thorigny-sur-marne"]

# ---------------------------------------------------------------------------
# Outils texte
# ---------------------------------------------------------------------------


def esc(s):
    return html.escape(str(s), quote=True)


def nw(s):
    """Empêche la coupure d'un nom composé (Thorigny-sur-Marne) en fin de ligne."""
    parts = re.split(r"(<[^>]+>)", s)
    return "".join(p if p.startswith("<") else re.sub(r"([^\s<>]+-[^\s<>]+)", r'<span class="nw">\1</span>', p) for p in parts)


def fr(text):
    """Typographie française hors balises : espaces insécables."""
    parts = re.split(r"(<[^>]+>)", text)
    out = []
    in_script = False
    for p in parts:
        if p.startswith("<"):
            if p.startswith("<script"):
                in_script = True
            elif p.startswith("</script"):
                in_script = False
            out.append(p)
            continue
        if in_script:
            out.append(p)
            continue
        p = re.sub(r" ([?!;])", "\u00a0\\1", p)
        p = re.sub(r" :(?=\s|$)", "\u00a0:", p)
        p = p.replace("« ", "«\u00a0").replace(" »", "\u00a0»")
        p = re.sub(r"(\d) (km|m²|m|cm|mm|h|%|€|°|ans|semaines|jours|heures|habitants|€/m²|€/ml|avis|chantiers|min)(?=[\s.,;:)/]|$)", "\\1\u00a0\\2", p)
        p = re.sub(r"(\d) (\d{3})\b", "\\1\u202f\\2", p)
        p = re.sub(r"\b(n°|7 j/7|24 h)", lambda m: m.group(1).replace(" ", "\u00a0"), p)
        out.append(p)
    return "".join(out)


def num(v):
    return f"{int(v):,}".replace(",", "\u202f")


def P(key, short=False):
    a, b, u, _ = C.PRIX[key]
    return f"{num(a)} à {num(b)} {u}"


def P_from(key):
    a, b, u, _ = C.PRIX[key]
    return f"dès {num(a)} {u}"


def price_table(keys, highlight=None):
    rows = "".join(
        f'<tr{" class=is-on" if k == highlight else ""}><th scope="row">{esc(C.PRIX[k][3])}</th><td>{P(k)}</td></tr>' for k in keys)
    return (f'<div class="tbl-wrap"><table class="tbl"><thead><tr><th scope="col">Travaux</th><th scope="col">Prix indicatif 2026</th></tr></thead>'
            f'<tbody>{rows}</tbody></table></div><p class="note">Fourchettes constatées en Île-de-France, fourniture et pose. Le prix ferme est fixé après la visite gratuite. <a href="/tarifs">Tous nos tarifs</a></p>')


def fill(text):
    text = re.sub(r"\[\[p:([a-z_]+)\]\]", lambda m: P(m.group(1)), text)
    text = re.sub(r"\[\[table:([a-z_,]+)\]\]", lambda m: price_table(m.group(1).split(",")), text)
    return text


def jsonld(obj):
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/") + "</script>"


def write(rel, data, binary=False):
    path = os.path.join(PUBLIC, rel.lstrip("/"))
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb" if binary else "w", **({} if binary else {"encoding": "utf-8"})) as f:
        f.write(data)


def h(s):
    return hashlib.sha1(s.encode()).hexdigest()


def pick(seed, n):
    return int(h(seed)[:8], 16) % n if n else 0


def sid(t):
    return re.sub(r"[^a-z0-9]+", "-", t.lower().encode("ascii", "ignore").decode())[:48].strip("-") or "s"


EARLY_JS = "document.documentElement.classList.add('js')"
EARLY_JS_HASH = "sha256-" + base64.b64encode(hashlib.sha256(EARLY_JS.encode()).digest()).decode()

ICONS = {
    "tel": '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M6.6 3.5h2.8l1.4 4.2-2 1.5a12 12 0 0 0 6 6l1.5-2 4.2 1.4v2.8a2 2 0 0 1-2.2 2A17 17 0 0 1 4.6 5.7a2 2 0 0 1 2-2.2z" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linejoin="round"/></svg>',
    "check": '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12.5l4.2 4.2L19 7" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    "pin": '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 21s-6.5-6.2-6.5-11a6.5 6.5 0 0 1 13 0c0 4.8-6.5 11-6.5 11z" fill="none" stroke="currentColor" stroke-width="1.9"/><circle cx="12" cy="10" r="2.4" fill="none" stroke="currentColor" stroke-width="1.9"/></svg>',
    "mail": '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><rect x="3.5" y="5.5" width="17" height="13" rx="2" fill="none" stroke="currentColor" stroke-width="1.9"/><path d="M4 7l8 6 8-6" fill="none" stroke="currentColor" stroke-width="1.9"/></svg>',
    "menu": '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>',
    "close": '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>',
    "chev": '<svg class="ico chev" viewBox="0 0 24 24" aria-hidden="true"><path d="M7 10l5 5 5-5" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    "arrow": '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    "star": '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3.2l2.7 5.6 6.1.8-4.5 4.2 1.1 6.1L12 17l-5.4 2.9 1.1-6.1-4.5-4.2 6.1-.8z" fill="currentColor"/></svg>',
    "shield": '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3l7.5 3v5.5c0 4.6-3.2 8.3-7.5 9.5-4.3-1.2-7.5-4.9-7.5-9.5V6z" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linejoin="round"/><path d="M8.5 12l2.4 2.4 4.6-4.8" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    "clock": '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="8.5" fill="none" stroke="currentColor" stroke-width="1.9"/><path d="M12 7.5V12l3 2" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round"/></svg>',
    "bolt": '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M13 2.5L5 13.5h6l-1 8 8-11h-6z" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linejoin="round"/></svg>',
    "zoom": '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><circle cx="10.5" cy="10.5" r="6" fill="none" stroke="currentColor" stroke-width="2"/><path d="M15 15l5 5M8 10.5h5M10.5 8v5" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>',
}
STRIPES = '<span class="stripes" aria-hidden="true"><i></i><i></i><i></i></span>'

# ---------------------------------------------------------------------------
# Photos
# ---------------------------------------------------------------------------
POOL = sorted(k for k in PHOTOS if not k.startswith("logo"))
TAG_ALT = {"tuiles": "Toiture en tuiles", "ardoise": "Couverture en ardoise", "zinc": "Travaux de zinguerie", "gouttiere": "Pose de gouttière",
           "echafaudage": "Chantier de couverture sur échafaudage", "chantier": "Chantier de couverture", "demoussage": "Démoussage de toiture",
           "velux": "Fenêtre de toit posée", "charpente": "Charpente bois", "urgence": "Intervention d'urgence sur toiture", "isolation": "Isolation de toiture",
           "cheminee": "Cheminée et faîtage", "toit-plat": "Étanchéité de toit plat", "avant-apres": "Toiture avant et après travaux", "equipe": "L'équipe Artisan Robin"}


def alt_of(k):
    m = PHOTOS[k]
    if m.get("alt"):
        return m["alt"]
    base = TAG_ALT.get(m["tags"][0], "Chantier de couverture")
    return base + (f" à {m['city']}" if m.get("city") else ", Artisan Robin")


def pick_photos(tags, n, seed="", exclude=(), roles=("", "apres")):
    cands = [k for k in POOL if k not in exclude and PHOTOS[k].get("role", "") in roles]
    if not cands:
        return []
    tags = list(tags or [])
    def score(k):
        t = PHOTOS[k]["tags"]
        s = sum(3 if x == (tags[0] if tags else None) else 1 for x in t if x in tags)
        return (-s, h(seed + k))
    return sorted(cands, key=score)[:n]


def img(key, alt=None, sizes="100vw", cls="", eager=False):
    m = PHOTOS[key]
    widths = m["sizes"]
    w = widths[-1]
    hh = round(m["h"] * w / m["w"])
    srcset = ", ".join(f"/assets/img/{key}-{x}.webp {x}w" for x in widths)
    src = f"/assets/img/{key}-{widths[min(1, len(widths) - 1)]}.webp"
    a = [f'src="{src}"', f'srcset="{srcset}"', f'sizes="{sizes}"', f'width="{w}"', f'height="{hh}"', f'alt="{esc(alt if alt is not None else alt_of(key))}"']
    a.append('fetchpriority="high"' if eager else 'loading="lazy"')
    a.append('decoding="async"')
    if cls:
        a.append(f'class="{cls}"')
    return "<img " + " ".join(a) + ">"


def big_src(key):
    return f"/assets/img/{key}-{PHOTOS[key]['sizes'][-1]}.webp"


def lb(key, sizes, cls="pz", cap=None):
    """Photo cliquable qui s'ouvre en grand (visionneuse)."""
    alt = alt_of(key)
    c = cap if cap is not None else alt
    return (f'<a class="{cls}" href="{big_src(key)}" data-lb data-cap="{esc(c)}">{img(key, alt, sizes)}'
            f'<span class="ph-zoom" aria-hidden="true">{ICONS["zoom"]}</span></a>')


def visual(tags, uid, label, sizes="(min-width: 960px) 50vw, 100vw", eager=False, seed=""):
    ks = pick_photos(tags, 1, seed or uid)
    if ks:
        return f'<figure class="visual">{img(ks[0], None, sizes, eager=eager)}</figure>', ks[0]
    return f'<figure class="visual visual-art">{art.tile(tags[0] if tags else "tuiles", uid, label=label)}</figure>', None


def thumb(tags, uid, label, sizes="(min-width: 960px) 25vw, 50vw", seed="", exclude=()):
    ks = pick_photos(tags, 1, seed or uid, exclude)
    if ks:
        return img(ks[0], None, sizes), ks[0]
    return art.tile(tags[0] if tags else "tuiles", uid, label=label), None


def gallery(tags, n, seed, title=None, exclude=(), cls="gal", hid="gal-t", intro=""):
    ks = pick_photos(tags, n, seed, exclude)
    if len(ks) < 3:
        return ""
    items = "".join(f"<li>{lb(k, '(min-width: 960px) 30vw, 50vw')}</li>" for k in ks)
    head = f'<div class="sec-head">{STRIPES}<h2 id="{hid}">{esc(title)}</h2>{f"<p>{intro}</p>" if intro else ""}</div>' if title else ""
    return f'<section class="sec sec-gal" aria-labelledby="{hid}"><div class="wrap">{head}<ul class="{cls} gal-{min(len(ks), 8)}">{items}</ul></div></section>'


def reel(seed="reel"):
    ks = pick_photos([], 18, seed)
    if len(ks) < 6:
        return ""
    lis = "".join(f'<li>{img(k, alt_of(k), "320px")}</li>' for k in ks)
    return f'<div class="reel" aria-label="Photos de nos chantiers"><div class="reel-in"><ul>{lis}</ul><ul aria-hidden="true">{lis}</ul></div></div>'


def pairs():
    out = {}
    for k, m in PHOTOS.items():
        if m.get("pair"):
            out.setdefault(m["pair"], {})[m["role"]] = k
    return [(p, v["avant"], v["apres"]) for p, v in sorted(out.items()) if "avant" in v and "apres" in v]


def before_after(av, ap, label):
    return f"""<figure class="ba" data-ba style="--pos:50%">
<div class="ba-img ba-after">{img(ap, alt_of(ap), "(min-width: 960px) 60vw, 100vw")}</div>
<div class="ba-img ba-before" aria-hidden="true">{img(av, alt_of(av), "(min-width: 960px) 60vw, 100vw")}</div>
<span class="ba-tag ba-tag-b">Avant</span><span class="ba-tag ba-tag-a">Après</span>
<input type="range" min="0" max="100" value="50" aria-label="{esc(label)} : faites glisser pour comparer avant et après">
<figcaption>{esc(label)}</figcaption></figure>"""


# ---------------------------------------------------------------------------
# Données structurées
# ---------------------------------------------------------------------------
ORG_ID = URL + "/#entreprise"


def org_schema():
    o = {
        "@context": "https://schema.org",
        "@type": "RoofingContractor",
        "@id": ORG_ID,
        "name": B["name"],
        "alternateName": "Artisan Robin",
        "description": "Charpentier, couvreur et zingueur à Thorigny-sur-Marne et dans les communes autour : réfection et réparation de toiture, zinguerie, isolation, charpente, urgences 7 j/7.",
        "url": URL + "/",
        "image": URL + "/assets/og-image.jpg",
        "logo": URL + "/assets/logo.png",
        "telephone": B["phone_e164"],
        "email": B["email"],
        "priceRange": "€€",
        "address": {"@type": "PostalAddress", "streetAddress": B["street"], "postalCode": B["postcode"],
                    "addressLocality": B["city"], "addressRegion": "Île-de-France", "addressCountry": "FR"},
        "geo": {"@type": "GeoCoordinates", "latitude": B["lat"], "longitude": B["lon"]},
        "openingHoursSpecification": [{"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], "opens": "00:00", "closes": "23:59"}],
        "areaServed": [{"@type": "City", "name": c["name"]} for c in CM.COMMUNES],
        "founder": {"@type": "Person", "name": B["manager"]},
        "knowsAbout": [s["name"] for s in SV.SERVICES],
        "sameAs": [B["twitter"]],
        "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Travaux de couverture, charpente et zinguerie",
                            "itemListElement": [{"@type": "Offer", "itemOffered": {"@type": "Service", "name": s["name"], "url": f"{URL}/couverture/{s['slug']}"}} for s in SV.SERVICES]},
    }
    if C.A_CONFIRMER["siret"]:
        o["identifier"] = {"@type": "PropertyValue", "propertyID": "SIRET", "value": C.A_CONFIRMER["siret"]}
    return o


def website_schema():
    return {"@context": "https://schema.org", "@type": "WebSite", "@id": URL + "/#site", "url": URL + "/",
            "name": "Artisan Robin Couverture", "inLanguage": "fr-FR", "publisher": {"@id": ORG_ID}}


def crumbs_schema(items):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList",
            "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": URL + p} for i, (n, p) in enumerate(items)]}


def faq_schema(faq):
    return {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub("<[^>]+>", "", fill(a))}} for q, a in faq]}


def service_schema(name, desc, path, keys=None, area=None):
    o = {"@context": "https://schema.org", "@type": "Service", "name": name, "serviceType": name, "url": URL + path,
         "description": desc, "provider": {"@id": ORG_ID},
         "areaServed": area or [{"@type": "City", "name": c["name"]} for c in CM.COMMUNES[:20]]}
    if keys:
        k = keys[0]
        a, b, u, _ = C.PRIX[k]
        unit = {"€/m²": "MTK", "€/ml": "MTR"}.get(u)
        spec = {"@type": "PriceSpecification", "minPrice": a, "maxPrice": b, "priceCurrency": "EUR"}
        if unit:
            spec = {"@type": "UnitPriceSpecification", "minPrice": a, "maxPrice": b, "priceCurrency": "EUR", "unitCode": unit}
        o["offers"] = {"@type": "Offer", "priceCurrency": "EUR", "priceSpecification": spec}
    return o


def article_schema(a, path, image):
    return {"@context": "https://schema.org", "@type": "BlogPosting", "headline": a["h1"], "description": a["desc"],
            "url": URL + path, "inLanguage": "fr-FR", "dateModified": TODAY, "datePublished": "2025-06-01",
            "author": {"@type": "Person", "name": B["manager"], "jobTitle": "Couvreur-zingueur, gérant d'Artisan Robin", "worksFor": {"@id": ORG_ID}},
            "publisher": {"@id": ORG_ID}, "image": image, "mainEntityOfPage": URL + path, "articleSection": a["category"]}


# ---------------------------------------------------------------------------
# Gabarit commun
# ---------------------------------------------------------------------------


def tel_btn(cls="btn btn-red", label=None):
    label = label or B["phone"]
    return f'<a class="{cls}" href="tel:{B["phone_e164"]}">{ICONS["tel"]}<span>{esc(label)}</span></a>'


def devis_btn(cls="btn btn-line", label="Devis gratuit", href="#devis"):
    return f'<a class="{cls}" href="{href}"><span>{esc(label)}</span>{ICONS["arrow"]}</a>'


def rating(cls="rating"):
    return (f'<span class="{cls}"><span class="stars" aria-hidden="true">{ICONS["star"] * 5}</span>'
            f'<span><strong>{B["google_rating"]}/5</strong> sur Google, {B["google_count"]} avis</span></span>')


def header(current):
    svc = "".join(
        f'<li><a href="/couverture/{s["slug"]}"{" aria-current=page" if current == s["slug"] else ""}><span>{esc(s["nav"])}</span><small>{esc(s["short"])}</small></a></li>'
        for s in SV.SERVICES)

    def link(path, label, key):
        here = ' aria-current="page"' if current == key else ""
        return f'<li><a href="{path}"{here}>{label}</a></li>'

    on = " is-current" if current in SV.BY_SLUG or current == "couverture" else ""
    return f"""<a class="skip" href="#contenu">Aller au contenu</a>
<div class="topbar"><div class="wrap topbar-in">
<p class="tb-urg"><span class="dot" aria-hidden="true"></span>Urgence toiture 7 j/7 : <a href="tel:{B['phone_e164']}">{B['phone']}</a></p>
<p class="tb-mid">{ICONS['clock']}Devis gratuit sous 24 h · Thorigny-sur-Marne et alentour</p>
<p class="tb-rate">{ICONS['star']}<strong>{B['google_rating']}/5</strong> · {B['google_count']} avis Google</p>
</div></div>
<header class="hd" data-header>
  <div class="wrap hd-in">
    <a class="brand" href="/" aria-label="Artisan Robin, charpentier couvreur zingueur, accueil"><img class="brand-svg" src="/assets/logo-h.svg" width="340" height="43" alt="Artisan Robin, charpentier couvreur zingueur"></a>
    <nav class="nav" id="nav" aria-label="Navigation principale">
      <ul class="nav-list">
        <li class="has-sub{on}"><details class="sub"><summary>Couverture{ICONS['chev']}</summary>
          <div class="mega"><ul class="mega-list">{svc}</ul>
          <div class="mega-side"><p class="mega-k">Une fuite ?</p><p>Mise hors d'eau 7 j/7, bâche arrimée, photos pour l'assurance.</p>{tel_btn('btn btn-red')}<a class="more" href="/couverture">Toutes nos prestations</a></div></div>
        </details></li>
        {link('/realisations', 'Réalisations', 'realisations')}
        {link('/tarifs', 'Tarifs', 'tarifs')}
        {link('/zones', 'Zones', 'zones')}
        {link('/blog', 'Conseils', 'blog')}
        {link('/a-propos', 'À propos', 'a-propos')}
        {link('/contact', 'Contact', 'contact')}
      </ul>
      <div class="nav-foot">{tel_btn('btn btn-red')}<a class="btn btn-line" href="/contact#devis"><span>Devis gratuit</span></a></div>
    </nav>
    {tel_btn('btn btn-red hd-tel')}
    <button class="menu-btn" type="button" aria-controls="nav" aria-expanded="false" aria-label="Ouvrir le menu">{ICONS['menu']}{ICONS['close']}</button>
  </div>
</header>"""


def footer(cls=""):
    svc = "".join(f'<li><a href="/couverture/{s["slug"]}">{esc(s["nav"])}</a></li>' for s in SV.SERVICES)
    top = sorted([c for c in ZONES if (c["pop"] or 0) >= 5000], key=lambda c: c["dist"])[:14]
    zon = '<li><a href="/">Thorigny-sur-Marne</a></li>' + "".join(f'<li><a href="/zone/couvreur-{c["slug"]}">{esc(c["name"])}</a></li>' for c in top)
    return f"""<footer class="ft">
  <div class="ft-stripe" aria-hidden="true"></div>
  <div class="wrap ft-grid">
    <div class="ft-id">
      <a href="/" aria-label="Artisan Robin, accueil"><img class="ft-logo" src="/assets/logo-light.svg" width="200" height="132" alt="Artisan Robin, charpentier couvreur zingueur" loading="lazy"></a>
      <p>Charpentier, couvreur et zingueur à Thorigny-sur-Marne et dans un rayon de 15 km : réfection, réparation, zinguerie, isolation, charpente. Urgences 7 jours sur 7.</p>
      <address>
        <p>{ICONS['tel']}<span><a href="tel:{B['phone_e164']}">{B['phone']}</a>, 7 j/7</span></p>
        <p>{ICONS['mail']}<span><a href="mailto:{B['email']}">{B['email']}</a></span></p>
        <p>{ICONS['pin']}<span>{esc(B['name'])}<br>{esc(B['street'])}, {B['postcode']} {B['city']}</span></p>
      </address>
      {rating('rating rating-light')}
    </div>
    <nav class="ft-nav" aria-label="Nos prestations"><h2>Couverture</h2><ul>{svc}</ul></nav>
    <nav class="ft-nav" aria-label="Communes"><h2>Communes</h2><ul>{zon}<li><a href="/zones">Toutes les communes</a></li></ul></nav>
    <nav class="ft-nav" aria-label="Informations"><h2>Infos</h2><ul>
      <li><a href="/realisations">Réalisations</a></li><li><a href="/tarifs">Tarifs</a></li><li><a href="/temoignages">Avis clients</a></li>
      <li><a href="/blog">Conseils toiture</a></li><li><a href="/a-propos">À propos</a></li><li><a href="/contact">Contact et devis</a></li>
      <li><a href="/mentions-legales">Mentions légales</a></li><li><a href="/politique-de-confidentialite">Confidentialité</a></li></ul></nav>
  </div>
  <div class="wrap ft-legal">
    <p>© {date.today().year} {esc(B['name'])} · Charpentier, couvreur, zingueur</p>
    <p><a href="https://allositeweb.com/" rel="noopener">Site réalisé par ALLOSITEWEB</a></p>
  </div>
</footer>
<div class="callbar" data-callbar>{tel_btn('btn btn-red', 'Appeler')}<a class="btn btn-white" href="{'/contact#devis' if cls in ('p-legal', 'p-404') else '#devis'}"><span>Devis gratuit</span></a></div>
<div class="lb" data-lightbox hidden><button class="lb-x" type="button" aria-label="Fermer">{ICONS['close']}</button><button class="lb-p" type="button" aria-label="Photo précédente">{ICONS['arrow']}</button><figure><img alt=""><figcaption></figcaption></figure><button class="lb-n" type="button" aria-label="Photo suivante">{ICONS['arrow']}</button></div>"""


def page(path, title, desc, body, crumbs=None, schema=None, current=None, robots="index,follow", priority="0.6", cls="", og_image=None, extra_head=""):
    canonical = URL + path
    crumbs_html = ""
    schemas = [website_schema(), org_schema()] if path == "/" else []
    if crumbs:
        items = [("Accueil", "/")] + crumbs
        lis = []
        for i, (n, p) in enumerate(items):
            lis.append(f'<li aria-current="page">{esc(n)}</li>' if i == len(items) - 1 else f'<li><a href="{p}">{esc(n)}</a></li>')
        crumbs_html = f'<nav class="crumbs" aria-label="Fil d\'Ariane"><ol class="wrap">{"".join(lis)}</ol></nav>'
        schemas.append(crumbs_schema(items))
    schemas += schema or []
    ld = "".join(jsonld(s) for s in schemas)
    og = og_image or URL + "/assets/og-image.jpg"
    doc = f"""<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="{'article' if path.startswith('/blog/') else 'website'}">
<meta property="og:locale" content="fr_FR">
<meta property="og:site_name" content="Artisan Robin Couverture">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{og}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#141414">
<meta name="geo.region" content="FR-77">
<meta name="geo.placename" content="Thorigny-sur-Marne">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/favicon.ico" sizes="32x32">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="preload" href="{ASSETS['font_h']}" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{ASSETS['font_b']}" as="font" type="font/woff2" crossorigin>{extra_head}
<link rel="stylesheet" href="{ASSETS['css']}">
<script>{EARLY_JS}</script>
<script src="{ASSETS['js']}" defer></script>
{ld}
</head>
<body class="{cls}">
{header(current)}
<main id="contenu">
{crumbs_html}
{re.sub(r"<h1([^>]*)>(.*?)</h1>", lambda m: "<h1" + m.group(1) + ">" + nw(m.group(2)) + "</h1>", fr(body.replace('href="/zone/couvreur-thorigny-sur-marne"', 'href="/"')), flags=re.S)}
</main>
{fr(footer(cls))}
</body>
</html>
"""
    rel = path if path.endswith(".html") else ("/index.html" if path == "/" else path + "/index.html")
    write(rel, doc)
    if robots.startswith("index"):
        PAGES.append((path, priority))


# ---------------------------------------------------------------------------
# Composants
# ---------------------------------------------------------------------------


def ticks(items, cls="ticks"):
    return f'<ul class="{cls}">' + "".join(f'<li>{ICONS["check"]}<span>{esc(x)}</span></li>' for x in items) + "</ul>"


def steps_html():
    lis = "".join(f'<li><span class="st-n">{i + 1:02d}</span><h3>{esc(t)}</h3><p>{esc(d)}</p></li>' for i, (t, d) in enumerate(C.STEPS))
    return f'<ol class="steps">{lis}</ol>'


def faq_html(faq, title="Questions fréquentes", hid="faq"):
    items = "".join(f'<details class="qa"><summary>{esc(q)}</summary><p>{fill(esc(a))}</p></details>' for q, a in faq)
    return f'<section class="sec sec-faq" aria-labelledby="{hid}"><div class="wrap narrow"><h2 id="{hid}">{title}</h2>{items}</div></section>'


def trust_band():
    return f"""<section class="band" aria-label="Nos engagements"><div class="wrap band-in">
<div><strong>{B['years']} ans</strong><span>de métier sur les toits</span></div>
<div><strong>{B['jobs']}+</strong><span>chantiers réalisés</span></div>
<div><strong>{B['google_rating']}/5</strong><span>{B['google_count']} avis Google</span></div>
<div><strong>24 h</strong><span>pour recevoir votre devis</span></div>
<div><strong>7 j/7</strong><span>pour les urgences</span></div>
<div><strong>10 ans</strong><span>garantie décennale</span></div>
</div></section>"""


def form_html(commune=None, type_default=None, compact=False, fid="devis-form"):
    opts = "".join(f'<option{" selected" if t == type_default else ""}>{esc(t)}</option>' for t in C.WORK_TYPES)
    dl = "".join(f'<option value="{esc(c["name"])}">' for c in sorted(CM.COMMUNES, key=lambda c: c["name"]))
    val = f' value="{esc(commune)}"' if commune else ""
    p = fid
    mail = "" if compact else f'<div class="f-row"><label for="{p}-mail">Email <small>(facultatif)</small></label><input id="{p}-mail" name="email" type="email" autocomplete="email" maxlength="120"></div>'
    msg_lab = "Votre projet <small>(facultatif)</small>" if compact else "Votre projet"
    rappel = "" if compact else f'''<fieldset class="f-row f-radio"><legend>Rappel de préférence</legend>
<label><input type="radio" name="rappel" value="Matin"> Matin</label><label><input type="radio" name="rappel" value="Après-midi"> Après-midi</label><label><input type="radio" name="rappel" value="Indifférent" checked> Indifférent</label></fieldset>'''
    return f"""<form class="form{' form-compact' if compact else ''}" data-devis novalidate>
<div class="f-two"><div class="f-row"><label for="{p}-nom">Nom</label><input id="{p}-nom" name="nom" autocomplete="name" required maxlength="80"></div>
<div class="f-row"><label for="{p}-tel">Téléphone</label><input id="{p}-tel" name="telephone" type="tel" autocomplete="tel" required pattern="[+0-9 .()\\-]{{8,20}}" maxlength="20"></div></div>
{mail}
<div class="f-two">
<div class="f-row"><label for="{p}-commune">Commune</label><input id="{p}-commune" name="commune" list="{p}-cl" required maxlength="80" autocomplete="address-level2"{val}><datalist id="{p}-cl">{dl}</datalist></div>
<div class="f-row"><label for="{p}-type">Travaux</label><select id="{p}-type" name="type" required><option value="">Choisir…</option>{opts}</select></div>
</div>
<div class="f-row"><label for="{p}-msg">{msg_lab}</label><textarea id="{p}-msg" name="message" rows="{2 if compact else 4}" maxlength="3000"{'' if compact else ' required'} placeholder="Fuite, tuiles cassées, réfection, surface approximative…"></textarea></div>
{rappel}
<div class="f-hp" aria-hidden="true"><label for="{p}-site">Site web</label><input id="{p}-site" name="site_web" tabindex="-1" autocomplete="off"></div>
<label class="f-ok"><input type="checkbox" name="consentement" required> <span>J'accepte que mes coordonnées servent uniquement à traiter ma demande. <a href="/politique-de-confidentialite">Confidentialité</a></span></label>
<button class="btn btn-red btn-big" type="submit"><span>Recevoir mon devis gratuit</span>{ICONS['arrow']}</button>
<div class="form-status" role="status"></div>
</form>"""


def form_section(commune=None, title="Votre devis gratuit sous 24 heures", type_default=None):
    ks = pick_photos(["chantier", "echafaudage", "tuiles"], 1, "form" + (commune or "") + (type_default or ""))
    bg = f'<div class="devis-bg" aria-hidden="true">{img(ks[0], "", "100vw")}</div>' if ks else ""
    return f"""<section class="sec sec-devis" id="devis" aria-labelledby="devis-t">{bg}
<div class="wrap devis-grid">
<div class="devis-txt">
{STRIPES}
<h2 id="devis-t">{esc(title)}</h2>
<p>Décrivez votre toit en quelques mots. On vous rappelle pour convenir d'une visite gratuite, puis vous recevez un devis détaillé, poste par poste, sous 24 heures.</p>
{ticks(["Visite et devis gratuits, sans engagement", "Photos de votre toiture à l'appui", "Attestation de garantie décennale jointe", "Urgence ? Appelez, on décroche 7 j/7"])}
<p class="devis-tel">{tel_btn('btn btn-red btn-big')}</p>
</div>
<div class="devis-card">{form_html(commune, type_default)}</div>
</div></section>"""


def aside_card(price=None, head=None):
    p = f'<p class="ac-price"><small>Prix indicatif</small><strong>{esc(price)}</strong></p>' if price else ""
    if head:
        p = f'<p class="ac-price"><strong>{esc(head)}</strong></p>'
    return f"""<aside class="aside-card" aria-label="Votre devis">{STRIPES}{p}
{ticks(["Visite et devis gratuits", "Devis détaillé sous 24 h", "Garantie décennale", "Urgences 7 j/7"])}
{tel_btn('btn btn-red')}
<a class="btn btn-line" href="#devis"><span>Demander un devis</span></a>
{rating()}
</aside>"""


def svc_cards(slugs=None, cls="cards", seed="c"):
    lis = []
    used = []
    for i, s in enumerate([SV.BY_SLUG[x] for x in slugs] if slugs else SV.SERVICES):
        vis, k = thumb(s["tags"], f"{seed}{i}", s["name"], "(min-width: 1100px) 24vw, (min-width: 700px) 45vw, 90vw", seed=seed + s["slug"], exclude=used)
        if k:
            used.append(k)
        lis.append(f'<li class="card"><a href="/couverture/{s["slug"]}"><span class="card-img">{vis}</span>'
                   f'<span class="card-body"><span class="card-t">{esc(s["name"])}</span><span class="card-d">{esc(s["short"])}</span>'
                   f'<span class="card-p">{esc(P_from(s["prices"][0]))}</span></span></a></li>')
    if not slugs:
        lis.append(f'<li class="card card-cta"><a href="tel:{B["phone_e164"]}"><span class="card-body"><span class="card-k">Une fuite, une tuile envolée ?</span>'
                   f'<span class="card-t">Urgence toiture 7 j/7</span><span class="card-d">Bâche arrimée, maison hors d\'eau, photos pour l\'assurance.</span>'
                   f'<span class="btn btn-white">{ICONS["tel"]}<span>{B["phone"]}</span></span></span></a></li>')
    return f'<ul class="{cls}">{"".join(lis)}</ul>'


def testimonials(n=12):
    cards = "".join(
        f'<li class="tm"><span class="stars" aria-hidden="true">{ICONS["star"] * 5}</span><blockquote><p>« {esc(q)} »</p></blockquote>'
        f'<p class="tm-sum">{esc(s)}</p><p class="tm-who"><strong>{esc(n_)}</strong><span>{esc(city)} · {esc(sv)}</span><small>Avis Google, {esc(d)}</small></p></li>'
        for n_, city, sv, d, q, s in C.TESTIMONIALS[:n])
    return f'<div class="tms" data-tms><ul class="tms-track">{cards}</ul><div class="tms-nav"><button type="button" class="tms-p" aria-label="Avis précédents">{ICONS["arrow"]}</button><button type="button" class="tms-n" aria-label="Avis suivants">{ICONS["arrow"]}</button></div></div>'


def commune_chips(cs):
    return '<ul class="chips">' + "".join(
        f'<li><a href="{"/" if c["slug"] == "thorigny-sur-marne" else "/zone/couvreur-" + c["slug"]}">{esc(c["name"])} <small>{c["dist_label"]} km</small></a></li>' for c in cs) + "</ul>"


def zones_groups(full=False):
    out = []
    for g in CM.GROUPS:
        cs = sorted([c for c in CM.COMMUNES if c["group"] == g], key=lambda c: c["dist"])
        lis = "".join(f'<li><a href="{"/" if c["slug"] == "thorigny-sur-marne" else "/zone/couvreur-" + c["slug"]}">{esc(c["name"])}</a> <small>{c["dist_label"]} km</small></li>' for c in cs)
        gid = "zg-" + h(g)[:6]
        if full:
            prof = C.GROUP_PROFILES[g]
            out.append(f'<section class="zg" aria-labelledby="{gid}"><h2 id="{gid}">{esc(g)}</h2><p>{esc(prof["habitat"][0])}</p><ul class="zg-list">{lis}</ul></section>')
        else:
            out.append(f'<details class="zg-d"><summary>{esc(g)} <small>{len(cs)} communes</small></summary><ul class="zg-list">{lis}</ul></details>')
    return "".join(out)


def sections_html(sections):
    out = []
    for t, body in sections:
        i = sid(t)
        out.append(f'<section class="art-sec" aria-labelledby="{i}"><h2 id="{i}">{esc(t)}</h2>{fill(body.strip())}</section>')
    return "".join(out)


# ---------------------------------------------------------------------------
# Pages
# ---------------------------------------------------------------------------


def hero_media(seed="home"):
    hero = [k for k in POOL if PHOTOS[k].get("hero")] or pick_photos(["echafaudage", "tuiles", "chantier"], 5, seed)
    hero = hero[:5]
    if not hero:
        return f'<div class="hero-media hero-art" aria-hidden="true">{art.tile("tuiles", "hero")}</div>', None
    slides = "".join(f'<div class="hs{" is-on" if i == 0 else ""}">{img(k, "", "100vw", eager=(i == 0))}</div>' for i, k in enumerate(hero))
    return f'<div class="hero-media" data-slides aria-hidden="true">{slides}</div>', hero[0]


def build_home():
    media, first = hero_media()
    T = THORIGNY
    metiers = []
    for i, (t, d, href, tags) in enumerate(C.METIERS):
        vis, _ = thumb(tags, f"m{i}", t, "(min-width: 960px) 33vw, 100vw", seed="metier" + t)
        metiers.append(f'<li class="mt"><a href="{href}"><span class="mt-img">{vis}</span><span class="mt-body"><span class="mt-k">0{i + 1}</span><span class="mt-t">{esc(t)}</span><span class="mt-d">{esc(d)}</span><span class="more">En savoir plus</span></span></a></li>')
    prs = pairs()
    ba = ""
    if prs:
        p, av, ap = prs[0]
        others = "".join(f"<li>{before_after(a, b, alt_of(b))}</li>" for _, a, b in prs[1:3]) if len(prs) >= 3 else ""
        ba = f"""<section class="sec sec-dark" aria-labelledby="ba-t"><div class="wrap ba-grid">
<div class="ba-txt">{STRIPES}<h2 id="ba-t">Avant, après</h2><p>Faites glisser le curseur : la même toiture, avant notre passage et une fois le chantier terminé.</p><a class="btn btn-white" href="/realisations"><span>Toutes nos réalisations</span>{ICONS['arrow']}</a></div>
{before_after(av, ap, alt_of(ap))}</div>{f'<div class="wrap"><ul class="ba-more">{others}</ul></div>' if others else ''}</section>"""
    gal = gallery([], 10, "home-gal", "Nos chantiers en photos", exclude=([first] if first else []), cls="gal gal-masonry", hid="chantiers-t",
                  intro='Réfections, réparations, zinguerie, charpente : quelques-uns de nos chantiers. <a href="/realisations">Voir toutes les réalisations</a>')
    quart = ", ".join(T["quartiers"][:5])
    thor_vis, _ = visual(["tuiles", "chantier"], "thor", "Toiture à Thorigny-sur-Marne", seed="thorigny")
    key_prices = ["refection_tuiles_meca", "remaniement", "reparation", "demoussage_hydrofuge", "gouttiere_zinc", "velux_remplacement"]
    body = f"""
<section class="hero" aria-labelledby="hero-t">
{media}
<div class="hero-shade" aria-hidden="true"></div>
<div class="wrap hero-grid">
<div class="hero-txt">
<p class="kicker">{STRIPES}Charpentier · Couvreur · Zingueur</p>
<h1 id="hero-t">Couvreur à Thorigny-sur-Marne</h1>
<p class="lead">Réfection et réparation de toiture, zinguerie, charpente, isolation et urgences 7 j/7, à Thorigny-sur-Marne et dans les communes autour. On monte voir votre toit, et vous avez votre devis sous 24 heures.</p>
<div class="cta-row">{tel_btn('btn btn-red btn-big')}{devis_btn('btn btn-white btn-big', 'Devis gratuit', '#devis-hero')}</div>
<ul class="hero-trust"><li>{ICONS['star']}<span><strong>{B['google_rating']}/5</strong> · {B['google_count']} avis Google</span></li><li>{ICONS['shield']}<span>Garantie décennale</span></li><li>{ICONS['bolt']}<span>Urgences 7 j/7</span></li></ul>
</div>
<div class="hero-card" id="devis-hero">
<p class="hc-k">{STRIPES}Devis gratuit</p>
<h2>Réponse sous 24 heures</h2>
{form_html(compact=True, fid="hero-form")}
</div>
</div>
</section>
{trust_band()}
{reel()}
<section class="sec" aria-labelledby="metiers-t"><div class="wrap">
<div class="sec-head">{STRIPES}<h2 id="metiers-t">Trois métiers, un seul artisan pour tout le toit</h2><p>Comme sur notre logo : charpentier, couvreur, zingueur. Un seul interlocuteur, de la charpente à la dernière gouttière.</p></div>
<ul class="metiers">{''.join(metiers)}</ul>
</div></section>
<section class="sec sec-mist" aria-labelledby="svc-t"><div class="wrap">
<div class="sec-head sec-head-row"><div>{STRIPES}<h2 id="svc-t">Nos travaux de couverture</h2><p>Treize prestations, chacune avec sa page : quand la choisir, comment on la réalise, combien elle coûte.</p></div><a class="more" href="/couverture">Toutes les prestations</a></div>
{svc_cards(seed="home")}
</div></section>
{ba}
{gal}
<section class="sec" aria-labelledby="thor-t"><div class="wrap split">
<div class="split-txt">{STRIPES}
<h2 id="thor-t">Les toits de Thorigny-sur-Marne, on les connaît</h2>
{''.join(f"<p>{esc(x)}</p>" for x in C.THORIGNY_HOME)}
<div class="cta-row">{tel_btn()}<a class="more" href="/zones">Les communes autour de Thorigny</a></div>
</div>
<div class="split-vis">{thor_vis}</div>
</div></section>
<section class="sec sec-dark" aria-labelledby="etapes-t"><div class="wrap">
<div class="sec-head">{STRIPES}<h2 id="etapes-t">Comment se passe un chantier avec nous</h2><p>Du premier appel à la réception, vous savez toujours ce qui se passe et ce que ça coûte.</p></div>
{steps_html()}
</div></section>
<section class="sec" aria-labelledby="prix-t"><div class="wrap split split-rev">
<div class="split-txt">{STRIPES}<h2 id="prix-t">Des prix clairs, avant même la visite</h2>
<p>Les fourchettes qu'on constate en Île-de-France en 2026, fourniture et pose. Le prix ferme dépend de votre toit : surface, pente, accès, état de la charpente. Il est fixé après la visite gratuite.</p>
<a class="btn btn-ink" href="/tarifs"><span>Tous nos tarifs</span>{ICONS['arrow']}</a></div>
<div>{price_table(key_prices)}</div>
</div></section>
<section class="sec sec-mist" aria-labelledby="zones-t"><div class="wrap zones-grid">
<div class="zones-txt">{STRIPES}
<h2 id="zones-t">{len(ZONES)} communes autour de Thorigny-sur-Marne</h2>
<p>De Dampmart et Lagny-sur-Marne, à deux kilomètres, jusqu'à Chelles, Claye-Souilly, Bussy-Saint-Georges et le Val d'Europe : la vallée de la Marne, Marne-la-Vallée et les villages briards.</p>
{zones_groups()}
<p><a class="more" href="/zones">Toutes les zones d'intervention</a></p>
</div>
<div class="zones-map">{art.zone_map(cls="map", links=True, title="Carte des communes où nous intervenons autour de Thorigny-sur-Marne")}</div>
</div></section>
<section class="sec" aria-labelledby="avis-t"><div class="wrap">
<div class="sec-head sec-head-row"><div>{STRIPES}<h2 id="avis-t">Ce que disent nos clients</h2><p>{B['google_rating']}/5 sur Google, {B['google_count']} avis. Quelques extraits :</p></div><a class="more" href="/temoignages">Tous les avis</a></div>
{testimonials()}
</div></section>
{faq_html(C.HOME_FAQ)}
{form_section()}
"""
    pre = f'\n<link rel="preload" as="image" imagesrcset="{", ".join(f"/assets/img/{first}-{x}.webp {x}w" for x in PHOTOS[first]["sizes"])}" imagesizes="100vw">' if first else ""
    page("/", "Couvreur Thorigny-sur-Marne (77400) | Artisan Robin, 7 j/7",
         "Couvreur, charpentier et zingueur à Thorigny-sur-Marne et alentour : réfection, réparation, gouttières, isolation, urgences 7 j/7. 4,9/5 sur Google, devis sous 24 h.",
         body, schema=[faq_schema(C.HOME_FAQ), service_schema("Couvreur à Thorigny-sur-Marne", "Travaux de couverture, charpente et zinguerie à Thorigny-sur-Marne et alentour.", "/", ["refection_tuiles_meca"], [{"@type": "City", "name": "Thorigny-sur-Marne"}])],
         priority="1.0", cls="p-home", extra_head=pre)


def build_service(s):
    path = f"/couverture/{s['slug']}"
    vis, k0 = visual(s["tags"], "v" + s["slug"], s["name"], eager=True, seed="svc" + s["slug"])
    related = "".join(f'<li><a href="/couverture/{r}"><span>{esc(SV.BY_SLUG[r]["name"])}</span><small>{esc(SV.BY_SLUG[r]["short"])}</small></a></li>' for r in s["related"])
    arts = [a for a in BLOG if s["slug"] in a.get("services", [])][:3]
    arts_html = "".join(f'<li><a href="/blog/{a["slug"]}"><span>{esc(a["h1"])}</span><small>{esc(a["category"])}</small></a></li>' for a in arts)
    near = sorted(CM.COMMUNES, key=lambda c: c["dist"])[:16]
    gal = gallery(s["tags"], 8, "g" + s["slug"], f"{s['name']} : nos chantiers en photos", exclude=([k0] if k0 else []), hid="gal-t")
    body = f"""
<section class="ph">
<div class="wrap ph-grid">
<div class="ph-txt">
<p class="kicker">{STRIPES}Couverture</p>
<h1>{esc(s['h1'])}</h1>
<p class="lead">{esc(s['lead'])}</p>
{ticks(s['points'])}
<div class="cta-row">{tel_btn()}{devis_btn()}</div>
</div>
{vis}
</div>
</section>
<div class="wrap body-grid">
<article class="art">{sections_html(s['sections'])}</article>
<div class="aside-col">{aside_card(P(s['prices'][0]))}
<nav class="related" aria-label="Prestations liées"><h2>À voir aussi</h2><ul>{related}</ul>{f'<h2>Conseils</h2><ul>{arts_html}</ul>' if arts_html else ''}</nav></div>
</div>
{gal}
{faq_html(s['faq'])}
<section class="sec sec-mist sec-near" aria-labelledby="near-t"><div class="wrap">
<h2 id="near-t">{esc(s['name'])} autour de Thorigny-sur-Marne</h2>
<p>Nous intervenons à Thorigny-sur-Marne et dans {len(ZONES)} communes à moins de 15 km. Les plus proches :</p>
{commune_chips(near)}
<p><a class="more" href="/zones">Toutes les communes</a></p>
</div></section>
{form_section(type_default=s['type'])}
"""
    sch = [service_schema(s["name"], s["desc"], path, s["prices"]), faq_schema(s["faq"])]
    page(path, s["title"], s["desc"], body, crumbs=[("Couverture", "/couverture"), (s["name"], path)], schema=sch, current=s["slug"], priority="0.9", cls="p-service")


def build_couverture():
    body = f"""
<section class="ph ph-plain"><div class="wrap narrow-l">
<p class="kicker">{STRIPES}Charpentier · Couvreur · Zingueur</p>
<h1>Nos travaux de couverture à Thorigny-sur-Marne</h1>
<p class="lead">De la réparation d'une tuile à la réfection complète, de la gouttière à la charpente : toutes nos prestations, avec leurs prix indicatifs. Chaque page détaille la méthode, les matériaux et les questions qu'on nous pose le plus.</p>
<div class="cta-row">{tel_btn()}{devis_btn()}</div>
</div></section>
<section class="sec sec-tight"><div class="wrap">{svc_cards(seed="hub")}</div></section>
{trust_band()}
{gallery([], 8, "hub-gal", "Sur nos chantiers", hid="hub-gal-t")}
<section class="sec" aria-labelledby="etapes-t"><div class="wrap">
<div class="sec-head">{STRIPES}<h2 id="etapes-t">Notre méthode, quel que soit le chantier</h2></div>
{steps_html()}</div></section>
{form_section()}
"""
    page("/couverture", "Travaux de couverture à Thorigny-sur-Marne | Artisan Robin",
         "Toutes nos prestations de couverture, charpente et zinguerie à Thorigny-sur-Marne : réfection, réparation, gouttières, isolation, Velux, démoussage. Prix indicatifs.",
         body, crumbs=[("Couverture", "/couverture")], current="couverture", priority="0.8", cls="p-hub")


def build_zone(c):
    name = c["name"]
    a, de = CM.a_(name), CM.de_(name)
    cp = c["cp"][0]
    prof = C.GROUP_PROFILES[c["group"]]
    V = lambda key, opts: opts[pick(c["slug"] + key, len(opts))]
    habitat = V("hab", prof["habitat"])
    dirp = CM.direction((c["bearing"] + 180) % 360)
    dist = c["dist_label"]
    path = f"/zone/couvreur-{c['slug']}"
    E = esc
    lead = V("lead", [
        f"Réfection, réparation, gouttières, charpente, isolation et urgences 7 j/7 {E(a)} ({cp}). Notre secteur est centré sur Thorigny-sur-Marne, à {dist} km : on se déplace vite, et la visite comme le devis sont gratuits.",
        f"Artisan Robin intervient {E(a)} ({cp}) pour tous les travaux de toiture : fuite, tuiles cassées, réfection complète, zinguerie, démoussage, fenêtres de toit. Devis détaillé sous 24 heures après la visite.",
        f"Charpentier, couvreur et zingueur, nous travaillons {E(a)} ({cp}) et dans tout le secteur de Thorigny-sur-Marne, à {dist} km. Une fuite ? On met la maison hors d'eau 7 jours sur 7.",
    ])
    facts = [("Code postal", ", ".join(c["cp"])), ("Département", f"{c['dept_name']} ({c['dept']})"),
             ("Population", (num(c["pop"]) + " habitants") if c["pop"] else ""), ("Intercommunalité", c["epci"]),
             ("Depuis Thorigny", f"{dist} km")]
    facts_html = "".join(f"<div><dt>{E(k)}</dt><dd>{E(v)}</dd></div>" for k, v in facts if v)
    S0, kp, ex_desc = prof["example"]
    surf = S0 + (pick(c["slug"] + "s", 5) - 2) * 10
    lo, hi = C.PRIX[kp][0] * surf, C.PRIX[kp][1] * surf
    budget = f"{num(round(lo, -2))} à {num(round(hi, -2))} €"
    works = "".join(f'<li><a href="/couverture/{w}"><span class="dv-n">{E(SV.BY_SLUG[w]["name"])}</span><span class="dv-d">{E(SV.BY_SLUG[w]["short"])}</span><span class="dv-p">{E(P_from(SV.BY_SLUG[w]["prices"][0]))}</span></a></li>' for w in prof["works"])
    roofs = ticks(prof["roofs"], "ticks ticks-2")
    bati_local = f"<p>{E(c['bati'])}</p>" if c["bati"] else ""
    demarches = []
    if c["patrimoine"]:
        demarches.append(f"<p>{E(c['patrimoine'])}</p><p>Dans le périmètre d'un monument historique, les travaux de toiture visibles passent par une déclaration préalable soumise à l'avis de l'architecte des Bâtiments de France : matériau, teinte, faîtage scellé ou lucarnes peuvent être imposés. On prépare avec vous les pièces du dossier.</p>")
    else:
        demarches.append(f"<p>Refaire une toiture à l'identique {E(a)} ne demande en général pas d'autorisation. Changer de matériau ou de teinte, créer une fenêtre de toit ou une lucarne impose une déclaration préalable en mairie, et le PLU peut fixer les matériaux autorisés. Le service urbanisme de la mairie {E(de)} vous le confirme ; on vous fournit les pièces techniques.</p>")
    demarches.append("<p>Si l'échafaudage doit empiéter sur le trottoir, une autorisation d'occupation du domaine public se demande quelques semaines avant le chantier.</p>")
    risk = f'<section class="art-sec" aria-labelledby="risques"><h2 id="risques">Ce qu\'il faut savoir {E(a)}</h2><p>{E(c["risques"])}</p><p>Ces contraintes concernent surtout les fondations et les murs, mais elles comptent aussi pour le toit : fissures qui tirent sur la charpente, gouttières et descentes à raccorder correctement pour ne pas détremper le pied des murs. On en tient compte dans le diagnostic.</p></section>' if c["risques"] else ""
    quart = f'<p class="small">Quartiers et lieux-dits où nous intervenons : {E(", ".join(c["quartiers"]))}.</p>' if c["quartiers"] else ""
    neigh = CM.neighbours(c, 8)
    nn = [n["name"] for n in neigh[:3]]
    faq = [
        (f"Intervenez-vous en urgence {a} ?", f"Oui, 7 jours sur 7. {name} est à {dist} km de Thorigny-sur-Marne, au cœur de notre secteur : on bâche le toit pour mettre la maison hors d'eau, puis on chiffre la réparation."),
        (f"Combien coûte une réfection de toiture {a} ?", f"Le prix dépend du toit, pas de la commune. Pour {ex_desc} d'environ {surf} m², comptez {budget.replace(chr(8239), ' ')} fourniture et pose. Le prix ferme est fixé après la visite gratuite."),
        (f"Faut-il une autorisation pour refaire sa toiture {a} ?",
         ("Oui dans le périmètre d'un monument historique, avec l'avis de l'architecte des Bâtiments de France. Ailleurs, une déclaration préalable est nécessaire si vous changez de matériau, de teinte ou créez une ouverture."
          if c["patrimoine"] else
          "À l'identique, en général non. Une déclaration préalable est nécessaire si vous changez de matériau ou de teinte, ou si vous créez une fenêtre de toit ou une lucarne.")),
        ("Le devis est-il gratuit ?", "Oui : la visite et le devis sont gratuits et sans engagement. Vous recevez un devis détaillé, poste par poste, sous 24 heures."),
    ]
    used = []
    strip = pick_photos(c.get("tags") or prof_tags(c["group"]), 4, "z" + c["slug"])
    strip_html = ""
    if len(strip) >= 3:
        strip_html = '<ul class="strip">' + "".join(f"<li>{lb(k, '(min-width: 960px) 25vw, 50vw')}</li>" for k in strip) + "</ul>"
        used = strip
    vis, _ = visual(prof_tags(c["group"]), "z" + c["slug"], f"Toiture {a}", eager=True, seed="zv" + c["slug"])
    body = f"""
<section class="ph ph-zone">
<div class="wrap ph-grid">
<div class="ph-txt">
<p class="kicker">{STRIPES}{E(prof['short'])} · {E(c['dept_name'])}</p>
<h1>Couvreur {E(a)} ({cp})</h1>
<p class="lead">{lead}</p>
<div class="cta-row">{tel_btn()}{devis_btn()}</div>
<dl class="facts">{facts_html}</dl>
</div>
{vis}
</div>
</section>
<div class="wrap body-grid">
<article class="art">
<section class="art-sec" aria-labelledby="bati"><h2 id="bati">Les toitures {E(de)}</h2>{bati_local}<p>{E(habitat)}</p>{roofs}{quart}</section>
<section class="art-sec" aria-labelledby="travaux"><h2 id="travaux">Nos travaux de toiture {E(a)}</h2>
<p>{V("tr", ["Les demandes qui reviennent le plus souvent dans ce secteur, avec nos prix indicatifs :", f"Ce que l'on nous demande le plus {E(a)} et alentour :", "Les travaux les plus fréquents sur ce type de bâti :"])}</p>
<ol class="devis-list">{works}</ol>
<p>Et bien sûr : <a href="/couverture/urgence-bachage">urgence et bâchage</a>, <a href="/couverture/velux-fenetres-toit">fenêtres de toit</a>, <a href="/couverture/charpente">charpente</a>, <a href="/couverture/isolation-toiture">isolation</a>.</p></section>
{strip_html}
<section class="art-sec" aria-labelledby="budget"><h2 id="budget">Exemple de budget {E(a)}</h2>
<p>Pour {E(ex_desc)}, sur environ {surf} m² de toiture, le budget se situe entre <strong>{budget}</strong>, fourniture et pose ({P(kp)}). Il varie avec la pente, l'accès pour l'échafaudage, l'état de la charpente et le nombre de cheminées ou de fenêtres de toit. Le devis ferme est établi après une visite gratuite.</p>
<p><a class="more" href="/tarifs">Tous nos tarifs</a></p></section>
<section class="art-sec" aria-labelledby="demarches"><h2 id="demarches">Démarches avant des travaux de toiture {E(a)}</h2>{''.join(demarches)}</section>
{risk}
</article>
<div class="aside-col">{aside_card(head=f"Devis gratuit {a}")}
<figure class="mini-map">{art.zone_map(current=c, cls="map map-mini", links=False, title=f"Position {de} par rapport à Thorigny-sur-Marne")}<figcaption>{E(name)} et Thorigny-sur-Marne, cercles à 5 et 10 km</figcaption></figure></div>
</div>
{faq_html(faq)}
<section class="sec sec-mist sec-near" aria-labelledby="near-t"><div class="wrap">
<h2 id="near-t">Couvreur près {E(de)}</h2>
<p>Autour {E(de)}, nous intervenons aussi {E(CM.a_(nn[0]))}, {E(CM.a_(nn[1]))} et {E(CM.a_(nn[2]))}. Les communes les plus proches :</p>
{commune_chips(neigh)}
<p><a class="more" href="/zones">Toutes les communes de notre zone</a></p>
</div></section>
{form_section(commune=name)}
"""
    title = f"Couvreur {a} ({cp}) | Artisan Robin, devis 24 h"
    if len(title) > 62:
        title = f"Couvreur {a} ({cp}) | Artisan Robin"
    if len(title) > 62:
        title = f"Couvreur {a} ({cp})"
    desc = f"Couvreur {a} ({cp}) : réfection, réparation, fuite, gouttières, charpente, démoussage. Artisan à {dist} km, urgences 7 j/7, devis gratuit sous 24 h."
    if len(desc) > 160:
        desc = f"Couvreur {a} ({cp}) : réfection, réparation, fuite, gouttières, démoussage. Urgences 7 j/7, devis gratuit sous 24 h."
    area = {"@type": "City", "name": name, "address": {"@type": "PostalAddress", "postalCode": cp, "addressLocality": name, "addressCountry": "FR"}}
    sch = [service_schema(f"Couvreur {a}", desc, path, [prof["example"][1]], area), faq_schema(faq)]
    page(path, title, desc, body, crumbs=[("Zones d'intervention", "/zones"), (name, path)], schema=sch, priority="0.7", cls="p-zone")


def prof_tags(group):
    return {"Vallée de la Marne, de Thorigny à Esbly": ["tuiles", "demoussage", "gouttiere"],
            "Villages de la Gondoire et de la Brie": ["tuiles", "charpente", "cheminee"],
            "Marne-la-Vallée et Val d'Europe": ["tuiles", "velux", "toit-plat"],
            "Chelles, Vaires et la Marne aval": ["tuiles", "echafaudage", "cheminee"],
            "Plaine de France : Claye, Villeparisis, Mitry": ["tuiles", "urgence", "gouttiere"]}.get(group, ["tuiles"])


def build_zones():
    body = f"""
<section class="ph ph-plain"><div class="wrap ph-grid ph-zones">
<div class="ph-txt"><p class="kicker">{STRIPES}Zones d'intervention</p>
<h1>Couvreur à Thorigny-sur-Marne et dans {len(ZONES)} communes autour</h1>
<p class="lead">Notre secteur couvre un rayon d'environ 15 km autour de Thorigny-sur-Marne : la vallée de la Marne de Chelles à Esbly, Marne-la-Vallée et le Val d'Europe, les villages de la Gondoire et de la Brie, et la Plaine de France jusqu'à Claye-Souilly et Mitry-Mory.</p>
<div class="cta-row">{tel_btn()}{devis_btn()}</div></div>
<div class="zones-map">{art.zone_map(cls="map map-big", links=True, title="Carte des communes où nous intervenons")}</div>
</div></section>
<section class="sec sec-tight"><div class="wrap zg-grid">{zones_groups(full=True)}</div></section>
{form_section()}
"""
    page("/zones", "Zones d'intervention : couvreur autour de Thorigny-sur-Marne",
         f"Les {len(CM.COMMUNES)} communes où Artisan Robin intervient autour de Thorigny-sur-Marne : Lagny, Pomponne, Dampmart, Chelles, Torcy, Bussy, Val d'Europe, Claye-Souilly.",
         body, crumbs=[("Zones d'intervention", "/zones")], current="zones", priority="0.8", cls="p-zones")


def build_tarifs():
    blocks = []
    for t, keys in C.TARIFS:
        blocks.append(f'<section class="art-sec" aria-labelledby="{sid(t)}"><h2 id="{sid(t)}">{esc(t)}</h2>{price_table(keys)}</section>')
    m2 = [k for k, v in C.PRIX.items() if v[2] == "€/m²" and k not in ("amenagement_combles",)]
    opts = "".join(f'<option value="{k}" data-min="{C.PRIX[k][0]}" data-max="{C.PRIX[k][1]}"{" selected" if k == "refection_tuiles_meca" else ""}>{esc(C.PRIX[k][3])}</option>' for k in m2)
    a, b = C.PRIX["refection_tuiles_meca"][:2]
    est = f"""<form class="estim" data-estim onsubmit="return false">
<div class="estim-in">
<label class="f-row" for="est-type"><span>Travaux</span></label><select id="est-type" name="type">{opts}</select>
<label class="range" for="est-surf"><span>Surface de toiture</span><output data-surf>110 m²</output></label>
<input id="est-surf" type="range" name="surface" min="20" max="300" step="5" value="110">
<p class="hint">Pas de mesure ? Surface au sol de la maison × 1,2 à 1,4 selon la pente donne un ordre de grandeur.</p>
</div>
<div class="estim-out" aria-live="polite"><p>Budget indicatif</p><p class="estim-val" data-out>{num(110 * a)} € à {num(110 * b)} €</p>
<p class="small">Fourniture et pose, avant visite. Le devis ferme suit le diagnostic sur place.</p>
<a class="btn btn-red" href="#devis"><span>Faire chiffrer ma toiture</span></a></div>
</form>"""
    src = "".join(f'<li><a href="{u}" rel="noopener">{esc(t)}</a></li>' for t, u in C.TARIF_SOURCES)
    faq = [("Le devis est-il payant ?", "Non. La visite et le devis sont gratuits et sans engagement."),
           ("Pourquoi des fourchettes et pas un prix fixe ?", "Parce que deux toits de même surface n'ont ni la même pente, ni le même accès, ni le même état de charpente. Le prix ferme est fixé après la visite."),
           ("L'échafaudage est-il compris ?", "Il figure sur le devis comme un poste à part, pour que vous puissiez comparer les offres ligne par ligne."),
           ("Quelle TVA s'applique ?", "10 % pour la plupart des travaux de rénovation sur un logement de plus de deux ans, 5,5 % pour les travaux d'amélioration énergétique éligibles, comme l'isolation.")]
    body = f"""
<section class="ph ph-plain"><div class="wrap narrow-l">
<p class="kicker">{STRIPES}Tarifs 2026</p>
<h1>Prix des travaux de toiture à Thorigny-sur-Marne</h1>
<p class="lead">Nos fourchettes de prix 2026, fourniture et pose, pour toutes les prestations de couverture, zinguerie, charpente et isolation. Elles vous donnent un ordre de grandeur avant la visite ; le prix ferme est fixé après, poste par poste.</p>
</div></section>
<section class="sec sec-tight"><div class="wrap estim-wrap"><h2>Estimez votre budget</h2>{est}</div></section>
<div class="wrap body-grid">
<article class="art">{''.join(blocks)}
<section class="art-sec" aria-labelledby="facteurs"><h2 id="facteurs">Ce qui fait varier le prix</h2>
<ul><li><strong>La surface réelle</strong> de toiture, qui dépasse toujours la surface au sol.</li><li><strong>La pente et la hauteur</strong> : plus le toit est raide et haut, plus la sécurité coûte.</li><li><strong>L'accès</strong> : échafaudage sur rue, jardin étroit, mitoyenneté.</li><li><strong>L'état de la charpente</strong> découvert à la dépose.</li><li><strong>Les points singuliers</strong> : cheminées, noues, lucarnes, fenêtres de toit.</li><li><strong>Le matériau</strong> et les contraintes du PLU ou de l'architecte des Bâtiments de France.</li></ul></section>
<section class="art-sec" aria-labelledby="sources"><h2 id="sources">Sources des fourchettes</h2><p>Fourchettes établies à partir de nos chantiers et recoupées avec les comparateurs de prix publiés en 2026 :</p><ul>{src}</ul></section>
</article>
<div class="aside-col">{aside_card(head="Devis gratuit sous 24 h")}</div>
</div>
{faq_html(faq)}
{form_section()}
"""
    page("/tarifs", "Prix couvreur 2026 à Thorigny-sur-Marne : tarifs toiture",
         "Prix 2026 des travaux de toiture à Thorigny-sur-Marne : réfection au m², réparation, démoussage, gouttière zinc, Velux, isolation. Simulateur et devis gratuit.",
         body, crumbs=[("Tarifs", "/tarifs")], current="tarifs", priority="0.8", cls="p-tarifs", schema=[faq_schema(faq)])


def build_realisations():
    tags_present = []
    for k in POOL:
        for t in PHOTOS[k]["tags"]:
            if t not in tags_present:
                tags_present.append(t)
    LABEL = {"tuiles": "Tuiles", "ardoise": "Ardoise", "zinc": "Zinc", "gouttiere": "Gouttières", "echafaudage": "Échafaudage", "chantier": "Chantiers",
             "demoussage": "Démoussage", "velux": "Fenêtres de toit", "charpente": "Charpente", "urgence": "Urgences", "isolation": "Isolation",
             "cheminee": "Cheminées", "toit-plat": "Toits plats", "avant-apres": "Avant / après", "equipe": "L'équipe"}
    filters = '<button type="button" aria-pressed="true" data-f="*">Toutes <small>' + str(len(POOL)) + '</small></button>' + "".join(
        f'<button type="button" aria-pressed="false" data-f="{t}">{LABEL.get(t, t)} <small>{sum(1 for k in POOL if t in PHOTOS[k]["tags"])}</small></button>' for t in tags_present)
    items = "".join(f'<li data-tags="{" ".join(PHOTOS[k]["tags"])}">{lb(k, "(min-width: 1100px) 25vw, (min-width: 700px) 33vw, 50vw")}</li>' for k in sorted(POOL, key=lambda k: h("r" + k)))
    prs = pairs()
    ba = "".join(f"<li>{before_after(a, b, alt_of(b))}</li>" for _, a, b in prs)
    if POOL:
        main = f"""<section class="sec sec-tight"><div class="wrap">
<div class="filters" role="group" aria-label="Filtrer les photos">{filters}</div>
<ul class="gal gal-masonry gal-all" data-gal>{items}</ul></div></section>"""
    else:
        main = f'<section class="sec sec-tight"><div class="wrap">{svc_cards(seed="real")}</div></section>'
    ba_sec = f'<section class="sec sec-dark" aria-labelledby="ba-t"><div class="wrap"><div class="sec-head">{STRIPES}<h2 id="ba-t">Avant, après</h2><p>Faites glisser le curseur pour comparer.</p></div><ul class="ba-list">{ba}</ul></div></section>' if ba else ""
    body = f"""
<section class="ph ph-plain"><div class="wrap narrow-l">
<p class="kicker">{STRIPES}Réalisations</p>
<h1>Nos chantiers de couverture en photos</h1>
<p class="lead">Réfections complètes, réparations, zinguerie, charpente, fenêtres de toit, démoussage : nos chantiers à Thorigny-sur-Marne, dans la vallée de la Marne et en Île-de-France. Cliquez sur une photo pour l'agrandir.</p>
<div class="cta-row">{tel_btn()}{devis_btn()}</div>
</div></section>
{main}
{ba_sec}
{trust_band()}
{form_section(title="Votre toit est le prochain ?")}
"""
    page("/realisations", "Réalisations : nos chantiers de toiture en photos | Artisan Robin",
         "Photos de nos chantiers de couverture, zinguerie et charpente à Thorigny-sur-Marne et alentour : réfections, réparations, gouttières, avant/après.",
         body, crumbs=[("Réalisations", "/realisations")], current="realisations", priority="0.8", cls="p-real")


def build_temoignages():
    body = f"""
<section class="ph ph-plain"><div class="wrap narrow-l">
<p class="kicker">{STRIPES}Avis clients</p>
<h1>Avis clients : {B['google_rating']}/5 sur Google</h1>
<p class="lead">{B['google_count']} clients ont donné leur avis sur Google. Voici des extraits de ceux que nous avons reçus après leurs chantiers : urgences, réfections, zinguerie, isolation, fenêtres de toit.</p>
{rating('rating rating-big')}
</div></section>
<section class="sec sec-tight"><div class="wrap"><ul class="tm-grid">{''.join(f'<li class="tm"><span class="stars" aria-hidden="true">{ICONS["star"] * 5}</span><blockquote><p>« {esc(q)} »</p></blockquote><p class="tm-sum">{esc(s)}</p><p class="tm-who"><strong>{esc(n)}</strong><span>{esc(city)} · {esc(sv)}</span><small>Avis Google, {esc(d)}</small></p></li>' for n, city, sv, d, q, s in C.TESTIMONIALS)}</ul></div></section>
{gallery([], 8, "avis-gal", "Leurs chantiers ressemblaient à ça", hid="avis-gal-t")}
{form_section(title="À votre tour")}
"""
    page("/temoignages", "Avis clients Artisan Robin : 4,9/5 sur Google (68 avis)",
         "Avis de nos clients sur Google : urgences après tempête, réfections, gouttières, isolation, Velux. 4,9/5 sur 68 avis. Couvreur à Thorigny-sur-Marne.",
         body, crumbs=[("Avis clients", "/temoignages")], current="temoignages", priority="0.6", cls="p-avis")


def build_apropos():
    vis, _ = visual(["equipe", "chantier", "echafaudage"], "ap", "Artisan Robin sur un chantier", eager=True, seed="apropos")
    vals = [("Un artisan, pas un centre d'appels", "Vous parlez à celui qui monte sur le toit. Le diagnostic, le devis et le chantier sont faits par la même équipe."),
            ("Des devis lisibles", "Chaque poste a sa ligne : échafaudage, dépose, fournitures, main-d'œuvre, évacuation. Vous pouvez comparer."),
            ("La bonne réparation", "On ne vend pas une réfection quand une réparation suffit. Photos à l'appui, on vous montre ce qu'on a vu."),
            ("Réactifs", "Devis sous 24 heures, urgences 7 jours sur 7, bâche posée le jour même quand c'est possible."),
            ("Un chantier propre", "Protections, bâche chaque soir quand le toit est ouvert, déchets évacués, jardin rendu propre."),
            ("Assurés", "Garantie décennale et responsabilité civile : l'attestation est jointe au devis.")]
    vals_html = "".join(f'<li><h3>{esc(t)}</h3><p>{esc(d)}</p></li>' for t, d in vals)
    body = f"""
<section class="ph">
<div class="wrap ph-grid">
<div class="ph-txt">
<p class="kicker">{STRIPES}À propos</p>
<h1>Artisan Robin, charpentier couvreur zingueur</h1>
<p class="lead">ARTISAN ROBIN COUVERTURE est une entreprise artisanale familiale de Seine-et-Marne, dirigée par {B['manager']}. Plus de {B['years']} ans de métier et plus de {B['jobs']} chantiers de couverture, de charpente et de zinguerie, aujourd'hui centrés sur Thorigny-sur-Marne et les communes autour.</p>
<div class="cta-row">{tel_btn()}{devis_btn()}</div>
</div>
{vis}
</div>
</section>
{trust_band()}
<section class="sec" aria-labelledby="val-t"><div class="wrap">
<div class="sec-head">{STRIPES}<h2 id="val-t">Notre façon de travailler</h2></div>
<ul class="values">{vals_html}</ul></div></section>
<section class="sec sec-mist" aria-labelledby="mt-t"><div class="wrap">
<div class="sec-head">{STRIPES}<h2 id="mt-t">Trois métiers du toit</h2><p>Un seul interlocuteur de la charpente à la gouttière : moins d'intermédiaires, des responsabilités claires.</p></div>
{svc_cards(["pose-toiture", "charpente", "zinguerie-gouttieres", "reparation-entretien"], seed="ap")}
</div></section>
{gallery([], 8, "ap-gal", "Sur nos chantiers", hid="ap-gal-t")}
<section class="sec" aria-labelledby="avis-t"><div class="wrap">
<div class="sec-head sec-head-row"><div>{STRIPES}<h2 id="avis-t">Ils nous ont confié leur toit</h2></div><a class="more" href="/temoignages">Tous les avis</a></div>
{testimonials(6)}</div></section>
{form_section()}
"""
    page("/a-propos", "À propos : Artisan Robin, couvreur en Seine-et-Marne",
         "ARTISAN ROBIN COUVERTURE : entreprise artisanale familiale de charpente, couverture et zinguerie, plus de 15 ans de métier, centrée sur Thorigny-sur-Marne.",
         body, crumbs=[("À propos", "/a-propos")], current="a-propos", priority="0.6", cls="p-about")


def build_contact():
    maps = "https://www.google.com/maps/search/?api=1&query=" + "Artisan+Robin+Couverture+22+avenue+Augustin+Pilardeau+77290+Mitry-Mory"
    body = f"""
<section class="ph ph-plain"><div class="wrap ph-grid">
<div class="ph-txt"><p class="kicker">{STRIPES}Contact</p><h1>Contact et devis gratuit</h1>
<p class="lead">Appelez-nous ou décrivez votre projet : on vous rappelle pour convenir d'une visite gratuite, et vous recevez un devis détaillé sous 24 heures. Une fuite ? Appelez directement, 7 jours sur 7.</p></div>
<div class="contact-card">
<p class="cc-l">Téléphone, 7 j/7</p><p class="cc-tel"><a href="tel:{B['phone_e164']}">{B['phone']}</a></p>
<p class="cc-l">Email</p><p><a href="mailto:{B['email']}">{B['email']}</a></p>
<p class="cc-l">Secteur</p><p>Thorigny-sur-Marne et {len(ZONES)} communes autour</p>
<p class="cc-l">Siège</p><p>{esc(B['name'])}<br>{esc(B['street'])}<br>{B['postcode']} {B['city']}</p>
<p><a class="more" href="{maps}" rel="noopener">Voir sur Google Maps</a></p>
</div>
</div></section>
{form_section(title="Votre demande de devis")}
"""
    page("/contact", "Contact et devis couvreur | Artisan Robin, Thorigny-sur-Marne",
         "Contactez Artisan Robin, couvreur à Thorigny-sur-Marne : 07 64 07 31 49, 7 j/7. Demande de devis gratuit en ligne, réponse sous 24 h.",
         body, crumbs=[("Contact", "/contact")], current="contact", priority="0.7", cls="p-contact",
         schema=[{"@context": "https://schema.org", "@type": "ContactPage", "url": URL + "/contact", "about": {"@id": ORG_ID}}])


def build_blog_index():
    cats = list(dict.fromkeys(a["category"] for a in BLOG))
    filters = '<button type="button" aria-pressed="true" data-f="*">Tous</button>' + "".join(f'<button type="button" aria-pressed="false" data-f="{sid(c)}">{esc(c)}</button>' for c in cats)
    cards = []
    used = []
    for i, a in enumerate(BLOG):
        vis, k = thumb(a["photo_tags"], f"b{i}", a["h1"], "(min-width: 960px) 30vw, 100vw", seed="bi" + a["slug"], exclude=used)
        if k:
            used.append(k)
        cards.append(f'<li class="post" data-tags="{sid(a["category"])}"><a href="/blog/{a["slug"]}"><span class="post-img">{vis}</span><span class="post-body"><span class="post-cat">{esc(a["category"])} · {a["read_min"]} min</span>'
                     f'<span class="post-t">{esc(a["h1"])}</span><span class="post-d">{esc(a["desc"])}</span></span></a></li>')
    body = f"""
<section class="ph ph-plain"><div class="wrap narrow-l">
<p class="kicker">{STRIPES}Conseils toiture</p>
<h1>Conseils de couvreur : prix, entretien, aides, réparations</h1>
<p class="lead">Les questions qu'on nous pose sur les chantiers, avec des réponses de couvreur : combien ça coûte, quand refaire, comment entretenir, quelles aides en 2026, que faire après une tempête.</p>
</div></section>
<section class="sec sec-tight"><div class="wrap">
<div class="filters" role="group" aria-label="Filtrer les articles">{filters}</div>
<ul class="posts" data-gal>{''.join(cards)}</ul></div></section>
{form_section()}
"""
    page("/blog", "Conseils toiture : prix, entretien, aides 2026 | Artisan Robin",
         "Guides et conseils de couvreur : prix d'une réfection au m², démoussage, gouttières, isolation et aides 2026, toiture après tempête, choisir son couvreur.",
         body, crumbs=[("Conseils", "/blog")], current="blog", priority="0.7", cls="p-blog")


def build_article(a):
    path = f"/blog/{a['slug']}"
    vis, k = visual(a["photo_tags"], "a" + a["slug"], a["h1"], eager=True, seed="ba" + a["slug"])
    image = URL + (big_src(k) if k else "/assets/og-image.jpg")
    toc = "".join(f'<li><a href="#{sid(s["h2"])}">{esc(s["h2"])}</a></li>' for s in a["sections"])
    secs = "".join(f'<section class="art-sec" aria-labelledby="{sid(s["h2"])}"><h2 id="{sid(s["h2"])}">{esc(s["h2"])}</h2>{s["html"]}</section>' for s in a["sections"])
    src = "".join(f'<li><a href="{esc(s["url"])}" rel="noopener nofollow">{esc(s["title"])}</a></li>' for s in a.get("sources", []))
    svc = "".join(f'<li><a href="/couverture/{x}"><span>{esc(SV.BY_SLUG[x]["name"])}</span><small>{esc(P_from(SV.BY_SLUG[x]["prices"][0]))}</small></a></li>' for x in a.get("services", []) if x in SV.BY_SLUG)
    others = [o for o in BLOG if o["slug"] != a["slug"] and o["category"] == a["category"]][:3]
    others += [o for o in BLOG if o["slug"] != a["slug"] and o not in others][:3 - len(others)]
    oth = "".join(f'<li><a href="/blog/{o["slug"]}"><span>{esc(o["h1"])}</span><small>{esc(o["category"])}</small></a></li>' for o in others)
    mid = pick_photos(a["photo_tags"], 3, "am" + a["slug"], exclude=([k] if k else []))
    mid_html = ('<ul class="strip strip-3">' + "".join(f"<li>{lb(x, '(min-width: 960px) 20vw, 33vw')}</li>" for x in mid) + "</ul>") if len(mid) == 3 else ""
    if mid_html and len(a["sections"]) > 3:
        cut = secs.find('<section class="art-sec"', len(secs) // 2)
        secs = secs[:cut] + mid_html + secs[cut:] if cut > 0 else secs + mid_html
    faq = [(f["q"], f["a"]) for f in a.get("faq", [])]
    body = f"""
<section class="ph ph-post">
<div class="wrap ph-grid">
<div class="ph-txt">
<p class="kicker">{STRIPES}{esc(a['category'])} · {a['read_min']} min de lecture</p>
<h1>{esc(a['h1'])}</h1>
<p class="lead">{esc(a['lead'])}</p>
<p class="byline">Par <strong>{esc(B['manager'])}</strong>, couvreur-zingueur, gérant d'Artisan Robin · Mis à jour le {date.today().strftime('%d/%m/%Y')}</p>
</div>
{vis}
</div>
</section>
<div class="wrap body-grid">
<article class="art art-post">{secs}
{f'<section class="art-sec sources" aria-labelledby="src-t"><h2 id="src-t">Sources</h2><ul>{src}</ul></section>' if src else ''}
<aside class="author"><div class="author-mark"><img src="/assets/logo-mark.svg" width="72" height="31" alt="" loading="lazy"></div><div><p class="author-n">{esc(B['manager'])}</p><p>Charpentier, couvreur et zingueur depuis plus de {B['years']} ans, gérant d'ARTISAN ROBIN COUVERTURE. Plus de {B['jobs']} chantiers de toiture en Seine-et-Marne et en Île-de-France.</p></div></aside>
</article>
<div class="aside-col">
<nav class="toc" aria-label="Sommaire"><h2>Sommaire</h2><ol>{toc}</ol></nav>
{aside_card(head="Une question sur votre toit ?")}
<nav class="related" aria-label="Pour aller plus loin">{f'<h2>Prestations</h2><ul>{svc}</ul>' if svc else ''}<h2>À lire aussi</h2><ul>{oth}</ul></nav>
</div>
</div>
{faq_html(faq) if faq else ''}
{form_section()}
"""
    sch = [article_schema(a, path, image)]
    if faq:
        sch.append(faq_schema(faq))
    page(path, a["title"], a["desc"], body, crumbs=[("Conseils", "/blog"), (a["h1"] if len(a["h1"]) < 60 else a["h1"][:57] + "…", path)],
         schema=sch, current="blog", priority="0.6", cls="p-post", og_image=image)


def build_legal():
    A = C.A_CONFIRMER
    ident = [f"<strong>{esc(B['name'])}</strong>"]
    if A["forme"]:
        ident.append(esc(A["forme"]))
    ident.append(f"{esc(B['street'])}, {B['postcode']} {B['city']}")
    if A["siret"]:
        ident.append(f"SIRET : {esc(A['siret'])}")
    ident.append(f"Téléphone : {B['phone']}, email : <a href=\"mailto:{B['email']}\">{B['email']}</a>")
    if A["dirigeant"]:
        ident.append(f"Directeur de la publication : {esc(A['dirigeant'])}")
    extra = ""
    if A["assureur"]:
        extra += f"<h2>Assurance décennale</h2><p>{esc(A['assureur'])}</p>"
    if A["mediateur"]:
        extra += f"<h2>Médiation de la consommation</h2><p>En cas de litige, vous pouvez recourir gratuitement au médiateur de la consommation : {esc(A['mediateur'])}.</p>"
    body = f"""
<section class="ph ph-plain"><div class="wrap narrow"><h1>Mentions légales</h1></div></section>
<section class="sec sec-tight"><div class="wrap narrow art legal">
<h2>Éditeur du site</h2><p>{'<br>'.join(ident)}</p>
{extra}
<h2>Hébergement</h2><p>Cloudflare, Inc., 101 Townsend St, San Francisco, CA 94107, États-Unis.</p>
<h2>Conception</h2><p>ALLOSITEWEB, Montreuil (<a href="https://allositeweb.com/" rel="noopener">allositeweb.com</a>).</p>
<h2>Propriété intellectuelle</h2><p>Les textes, photos et le logo de ce site appartiennent à {esc(B['name'])}. Toute reproduction sans autorisation est interdite.</p>
<h2>Données personnelles</h2><p>Voir notre <a href="/politique-de-confidentialite">politique de confidentialité</a>.</p>
<h2>Crédits</h2><p>Polices Montserrat et Inter (licence SIL Open Font License). Données communales : INSEE et Etalab (découpage administratif), GeoNames.</p>
</div></section>"""
    page("/mentions-legales", "Mentions légales | Artisan Robin Couverture", "Mentions légales du site artisanrobincouverture.fr : éditeur, hébergement, conception, propriété intellectuelle et crédits.",
         body, crumbs=[("Mentions légales", "/mentions-legales")], robots="noindex,follow", cls="p-legal")
    body2 = f"""
<section class="ph ph-plain"><div class="wrap narrow"><h1>Politique de confidentialité</h1></div></section>
<section class="sec sec-tight"><div class="wrap narrow art legal">
<h2>Les données collectées</h2><p>Le formulaire de devis recueille votre nom, votre téléphone, votre email s'il est renseigné, la commune des travaux, le type de travaux et la description de votre projet. Ces informations servent uniquement à répondre à votre demande et à établir un devis.</p>
<h2>Destinataire et conservation</h2><p>Elles sont transmises par email à {esc(B['name'])} et ne sont ni revendues ni utilisées à des fins publicitaires. Elles sont conservées le temps nécessaire au suivi de votre demande puis, si un contrat est conclu, pendant la durée des obligations légales.</p>
<h2>Vos droits</h2><p>Conformément au règlement général sur la protection des données, vous disposez d'un droit d'accès, de rectification, d'effacement et d'opposition, en écrivant à <a href="mailto:{B['email']}">{B['email']}</a>. Vous pouvez aussi adresser une réclamation à la CNIL.</p>
<h2>Cookies</h2><p>Ce site ne dépose aucun cookie de mesure d'audience ni de publicité. Les polices de caractères sont hébergées sur le site lui-même.</p>
</div></section>"""
    page("/politique-de-confidentialite", "Politique de confidentialité | Artisan Robin Couverture", "Politique de confidentialité d'artisanrobincouverture.fr : données du formulaire de devis, conservation, vos droits, cookies.",
         body2, crumbs=[("Confidentialité", "/politique-de-confidentialite")], robots="noindex,follow", cls="p-legal")


def build_404():
    body = f"""<section class="ph ph-plain"><div class="wrap narrow"><h1>Cette page n'existe pas</h1>
<p class="lead">L'adresse a peut-être changé. Voici les pages les plus consultées :</p>
<ul class="link-list">
<li><a href="/"><span>Accueil</span></a></li><li><a href="/couverture"><span>Nos travaux de couverture</span></a></li>
<li><a href="/tarifs"><span>Tarifs</span></a></li><li><a href="/realisations"><span>Réalisations</span></a></li>
<li><a href="/zones"><span>Zones d'intervention</span></a></li><li><a href="/contact"><span>Contact</span></a></li></ul>
<div class="cta-row">{tel_btn()}</div></div></section>"""
    page("/404.html", "Page introuvable | Artisan Robin Couverture", "Cette page n'existe pas.", body, robots="noindex,follow", cls="p-404")


# ---------------------------------------------------------------------------
# Fichiers techniques
# ---------------------------------------------------------------------------


def copy_assets():
    if os.path.exists(PUBLIC):
        shutil.rmtree(PUBLIC)
    os.makedirs(os.path.join(PUBLIC, "assets", "fonts"))
    for name, key in (("montserrat.woff2", "font_h"), ("inter.woff2", "font_b")):
        data = open(os.path.join(SITE, "fonts", name), "rb").read()
        fn = name.replace(".woff2", f".{hashlib.sha1(data).hexdigest()[:8]}.woff2")
        write(f"/assets/fonts/{fn}", data, binary=True)
        ASSETS[key] = f"/assets/fonts/{fn}"
    css = open(os.path.join(SITE, "site.css"), encoding="utf-8").read()
    css = css.replace("__FONT_H__", ASSETS["font_h"]).replace("__FONT_B__", ASSETS["font_b"])
    js = open(os.path.join(SITE, "site.js"), encoding="utf-8").read()
    js = js.replace("__PHONE__", B["phone_e164"]).replace("__WHATSAPP__", B["whatsapp"])
    for kind, data in (("css", css), ("js", js)):
        fn = f"/assets/site.{h(data)[:10]}.{kind}"
        write(fn, data)
        ASSETS[kind] = fn
    write("/assets/logo.svg", LG.svg("stacked", "color"))
    write("/assets/logo-h.svg", LG.svg("horizontal", "color"))
    write("/assets/logo-mark.svg", LG.svg("mark", "color"))
    write("/assets/logo-light.svg", LG.svg("stacked", "light"))
    write("/favicon.svg", LG.favicon())
    if os.path.isdir(IMG_OUT):
        shutil.copytree(IMG_OUT, os.path.join(PUBLIC, "assets", "img"), dirs_exist_ok=True)
    for f in ("og-image.jpg", "icon-512.png", "icon-192.png", "apple-touch-icon.png", "favicon.ico", "logo.png"):
        p = os.path.join(SITE, "brand", f)
        if os.path.exists(p):
            dest = f"/assets/{f}" if f.startswith(("og-", "icon-", "logo")) else f"/{f}"
            write(dest, open(p, "rb").read(), binary=True)
    # Ancienne adresse des images principales (partages, Google Images)
    for old in ("/images/logo-artisan-robin.png", "/images/logo-footer.png"):
        p = os.path.join(SITE, "brand", "logo.png")
        if os.path.exists(p):
            write(old, open(p, "rb").read(), binary=True)
    og = os.path.join(SITE, "brand", "og-image.jpg")
    if os.path.exists(og):
        write("/images/og-couvreur-default.jpg", open(og, "rb").read(), binary=True)


def tech_files():
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for p, prio in PAGES:
        sm.append(f"<url><loc>{URL}{p}</loc><lastmod>{TODAY}</lastmod><priority>{prio}</priority></url>")
    sm.append("</urlset>")
    write("/sitemap.xml", "\n".join(sm) + "\n")
    write("/robots.txt", f"User-agent: *\nAllow: /\nDisallow: /api/\n\nSitemap: {URL}/sitemap.xml\n")
    keep = {c["slug"] for c in ZONES}
    red = ["# Anciennes adresses -> nouvelles (301)"]
    for a, b in C.REDIRECTS:
        red.append(f"{a} {b} 301")
    red.append("/zone/couvreur-thorigny-sur-marne / 301")
    for s in C.OLD_ZONES:
        if s not in keep and s != "thorigny-sur-marne" and f"/zone/couvreur-{s}" not in dict(C.REDIRECTS):
            red.append(f"/zone/couvreur-{s} /zones 301")
    red.append("/fr / 301")
    red.append("/fr/* /:splat 301")
    write("/_redirects", "\n".join(red) + "\n")
    csp = ("default-src 'self'; script-src 'self' '" + EARLY_JS_HASH + "'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; "
           "font-src 'self'; connect-src 'self'; form-action 'self'; frame-ancestors 'self'; base-uri 'self'; object-src 'none'")
    write("/_headers", f"""/*
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
  X-Frame-Options: SAMEORIGIN
  Permissions-Policy: camera=(), microphone=(), geolocation=(), interest-cohort=()
  Content-Security-Policy: {csp}

/assets/*
  Cache-Control: public, max-age=31536000, immutable

/assets/img/*
  Cache-Control: public, max-age=2592000

/assets/og-image.jpg
  Cache-Control: public, max-age=86400

/assets/icon-*
  Cache-Control: public, max-age=86400

https://:project.:subdomain.workers.dev/*
  X-Robots-Tag: noindex

https://:version.:project.:subdomain.workers.dev/*
  X-Robots-Tag: noindex
""")
    man = {"name": "Artisan Robin Couverture", "short_name": "Artisan Robin", "start_url": "/", "display": "browser", "background_color": "#ffffff",
           "theme_color": "#141414", "icons": [{"src": "/assets/icon-192.png", "sizes": "192x192", "type": "image/png"}, {"src": "/assets/icon-512.png", "sizes": "512x512", "type": "image/png"}]}
    write("/site.webmanifest", json.dumps(man, ensure_ascii=False, indent=1))
    ll = ["# ARTISAN ROBIN COUVERTURE", "",
          f"> Charpentier, couvreur et zingueur à Thorigny-sur-Marne (77400) et dans {len(ZONES)} communes autour (vallée de la Marne, Marne-la-Vallée, Val d'Europe, Plaine de France). Réfection et réparation de toiture, zinguerie, charpente, isolation, urgences 7 j/7. Téléphone {B['phone']}. Email {B['email']}. Note Google {B['google_rating']}/5 ({B['google_count']} avis).",
          "", "## Prestations"]
    ll += [f"- [{s['name']}]({URL}/couverture/{s['slug']}): {s['short']} ({P(s['prices'][0])})" for s in SV.SERVICES]
    ll += ["", "## Pages utiles", f"- [Tarifs 2026]({URL}/tarifs)", f"- [Réalisations]({URL}/realisations)", f"- [Avis clients]({URL}/temoignages)", f"- [Contact et devis]({URL}/contact)"]
    ll += ["", "## Conseils"] + [f"- [{a['h1']}]({URL}/blog/{a['slug']})" for a in BLOG]
    ll += ["", "## Communes"] + [f"- [Couvreur {CM.a_(c['name'])}]({URL}/zone/couvreur-{c['slug']}) ({c['dist_label']} km)" for c in sorted(ZONES, key=lambda c: c["dist"])]
    write("/llms.txt", "\n".join(ll) + "\n")


def main():
    copy_assets()
    build_home()
    build_couverture()
    for s in SV.SERVICES:
        build_service(s)
    build_zones()
    for c in ZONES:
        build_zone(c)
    build_tarifs()
    build_realisations()
    build_temoignages()
    build_apropos()
    build_contact()
    build_blog_index()
    for a in BLOG:
        build_article(a)
    build_legal()
    build_404()
    tech_files()
    print(f"{len(PAGES)} pages indexables générées ({len(ZONES)} communes, {len(BLOG)} articles), photos : {len(POOL)}")


if __name__ == "__main__":
    main()
