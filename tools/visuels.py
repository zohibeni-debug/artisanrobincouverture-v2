# -*- coding: utf-8 -*-
"""Image de partage (1200 x 630), icônes et logo PNG, dessinés à partir du logo vectorisé (site/logo.py).
Rendu par Chromium (Playwright). Usage : python3 tools/visuels.py
"""
import base64, io, os, sys
from PIL import Image
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "site"))
import logo as LG  # noqa: E402

OUT = os.path.join(ROOT, "site", "brand")
os.makedirs(OUT, exist_ok=True)
font = base64.b64encode(open(os.path.join(ROOT, "site", "fonts", "montserrat.woff2"), "rb").read()).decode()
CSS = f"@font-face{{font-family:M;src:url(data:font/woff2;base64,{font})}}*{{margin:0;box-sizing:border-box}}body{{font-family:M,sans-serif}}"

OG = f"""<html><head><style>{CSS}
.og{{width:1200px;height:630px;display:grid;grid-template-columns:520px 1fr;background:#141414;color:#fff;position:relative;overflow:hidden}}
.l{{background:#fff;display:grid;place-items:center;padding:40px}}
.l svg{{width:430px}}
.r{{padding:70px 60px;display:flex;flex-direction:column;justify-content:center;gap:22px}}
.k{{color:#e3141d;font-weight:800;letter-spacing:.14em;font-size:17px;text-transform:uppercase}}
h1{{font-weight:800;font-size:56px;line-height:1.02;letter-spacing:-.02em}}
.t{{display:inline-block;background:#d10f18;color:#fff;font-weight:800;font-size:36px;padding:14px 26px;border-radius:8px;align-self:flex-start}}
.s{{font-size:22px;color:#cfcfcf;font-weight:600}}
.st{{position:absolute;left:520px;bottom:0;right:0;height:14px;background:repeating-linear-gradient(-55deg,#d10f18 0 26px,#141414 26px 36px)}}
</style></head><body><div class="og"><div class="l">{LG.svg("stacked", "color", title="")}</div>
<div class="r"><p class="k">Charpentier · Couvreur · Zingueur</p><h1>Couvreur à<br><span style="white-space:nowrap">Thorigny-sur-Marne</span></h1>
<p class="s">Réfection, réparation, zinguerie · Urgences 7 j/7 · Devis sous 24 h</p><p class="t">06 66 55 35 62</p></div><div class="st"></div></div></body></html>"""

ICON = f"""<html><head><style>{CSS}body{{background:transparent}}.i{{width:1024px;height:1024px;background:#fff;border-radius:__R__px;display:grid;place-items:center}}.i svg{{width:860px}}</style></head>
<body><div class="i">{LG.svg("mark", "color", title="")}</div></body></html>"""

LOGO = f"""<html><head><style>{CSS}body{{background:transparent}}.lg{{width:1200px;padding:20px}}</style></head><body><div class="lg">{LG.svg("stacked", "color", title="")}</div></body></html>"""

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1200, "height": 630})
    pg.set_content(OG); pg.wait_for_timeout(300)
    pg.screenshot(path="/tmp/og.png")
    Image.open("/tmp/og.png").convert("RGB").save(os.path.join(OUT, "og-image.jpg"), quality=88, optimize=True, progressive=True)
    for r, name in ((180, "icon"), (0, "apple")):
        pg2 = b.new_page(viewport={"width": 1024, "height": 1024})
        pg2.set_content(ICON.replace("__R__", str(r))); pg2.wait_for_timeout(200)
        pg2.screenshot(path=f"/tmp/{name}.png", omit_background=True)
    pg3 = b.new_page(viewport={"width": 1200, "height": 900})
    pg3.set_content(LOGO); pg3.wait_for_timeout(200)
    pg3.locator(".lg").screenshot(path="/tmp/logo.png", omit_background=True)
    b.close()
ic = Image.open("/tmp/icon.png").convert("RGBA")
ic.resize((512, 512), Image.LANCZOS).save(os.path.join(OUT, "icon-512.png"))
ic.resize((192, 192), Image.LANCZOS).save(os.path.join(OUT, "icon-192.png"))
Image.open("/tmp/apple.png").convert("RGB").resize((180, 180), Image.LANCZOS).save(os.path.join(OUT, "apple-touch-icon.png"))
ic.resize((64, 64), Image.LANCZOS).save(os.path.join(OUT, "favicon.ico"), sizes=[(16, 16), (32, 32), (48, 48)])
lg = Image.open("/tmp/logo.png").convert("RGBA")
lg = lg.crop(lg.getbbox()); lg.thumbnail((600, 600), Image.LANCZOS); lg.save(os.path.join(OUT, "logo.png"), optimize=True)
print(sorted(os.listdir(OUT)))
