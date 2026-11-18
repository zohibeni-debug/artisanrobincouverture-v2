# couvreur-thorignysurmarne.fr : site d'ARTISAN ROBIN COUVERTURE

Site du charpentier-couvreur-zingueur Artisan Robin consacré à **Thorigny-sur-Marne (77400)** et aux communes autour, publié sur `couvreur-thorignysurmarne.fr`. Le site historique `artisanrobincouverture.fr` reste en place à part. Les pages sont en HTML complet, lisibles par Google sans JavaScript. Le site est hébergé sur Cloudflare : un Worker sert les fichiers statiques et traite le formulaire de devis.

94 pages indexables, sans barre finale dans les adresses :
- l'accueil (couvreur à Thorigny-sur-Marne) ;
- la page Couverture et les 13 pages prestations `/couverture/<prestation>` ;
- la page Zones et 54 pages `/zone/couvreur-<commune>` (rayon d'environ 15 km) ;
- Tarifs (avec estimateur), Réalisations (galerie filtrable), Avis clients, À propos, Contact ;
- le blog et ses 18 articles `/blog/<article>`, réécrits pour 2026 ;
- mentions légales et politique de confidentialité.

Les 178 anciennes pages de communes hors de la nouvelle zone sont redirigées (301) vers `/zones`, `/zone/couvreur-thorigny-sur-marne` vers l'accueil, et `/fr/*` vers la même adresse sans `/fr` (voir `public/_redirects`).

## Ce que contient ce dépôt

| Dossier / fichier | Rôle |
|---|---|
| `public/` | Le site tel qu'il est mis en ligne |
| `src/worker.js` | Le formulaire de devis (`POST /api/devis`) |
| `site/content.py` | Coordonnées, points à confirmer, prix, étapes, FAQ, avis, profils de secteurs, redirections |
| `site/services.py` | Les 13 pages prestations |
| `site/communes.py`, `site/data/communes_*.json` | Les 55 communes : données INSEE / Etalab, coordonnées, notes locales sourcées |
| `site/data/blog/*.json` | Les 18 articles |
| `site/data/prix.json` | La grille de prix 2026, reprise partout |
| `site/photos.py` | Prépare les photos déposées dans `site/photos-src/` |
| `site/build.py` | Le générateur : produit `public/` |
| `site/logo.py`, `site/logo_parts.json` | Logo vectorisé (tracé depuis `site/brand-src/`) |
| `site/site.css`, `site/site.js` | Styles et scripts |
| `tools/verifier.py` | Contrôles : liens, balises, données structurées, anciennes adresses |
| `tools/visuels.py` | Image de partage, icônes et logo PNG |
| `tools/apercu_photos.py` | Aperçu local avec des emplacements photo factices (jamais publié) |

## Ajouter des photos

Déposez les photos dans `site/photos-src/`, un dossier par sujet : `tuiles`, `ardoise`, `zinc`, `gouttiere`, `echafaudage`, `chantier`, `demoussage`, `velux`, `charpente`, `urgence`, `isolation`, `cheminee`, `toit-plat`, `avant-apres`, `equipe`. Pour un avant/après, nommez la paire `xxx-avant.jpg` et `xxx-apres.jpg`. Les textes alternatifs, la commune et les photos du diaporama d'accueil se précisent dans `site/photos_manifest.json` :

```json
{ "chantier-lagny-01": { "alt": "Réfection d'une toiture en tuiles mécaniques à Lagny-sur-Marne", "city": "Lagny-sur-Marne", "hero": true } }
```

Les photos se placent ensuite toutes seules : diaporama et bande défilante de l'accueil, galeries de chaque prestation et de chaque commune, page Réalisations, articles.

## Modifier le site

```bash
python3 site/photos.py      # seulement si des photos ont été ajoutées
python3 site/build.py       # régénère public/
python3 tools/verifier.py   # doit afficher « ERREURS : 0 »
git add -A && git commit -m "…" && git push   # Cloudflare redéploie tout seul
```

Ne renommez pas les adresses des pages : ce sont celles que Google connaît déjà.

## Brancher Cloudflare (une seule fois)

Dans Cloudflare : **Compute**, puis **Workers & Pages**, puis **Create application**. Choisissez **Import a repository** (GitHub) et sélectionnez `zohibeni-debug/artisanrobincouverture-v2`.

- **Project name** : `artisanrobincouverture-v2`, exactement comme le `name` de `wrangler.jsonc` ;
- **Build command** : laisser vide ;
- **Deploy command** : `npx wrangler deploy`.

Le site apparaît d'abord sur une adresse provisoire en `.workers.dev`, non indexée par Google (en-tête `X-Robots-Tag: noindex` dans `public/_headers`).

## Formulaire de devis

Les demandes partent par email à `contact@artisanrobincouverture.fr` (valeur par défaut) :

1. **Cloudflare Email Service** (binding `EMAIL`), une fois le domaine géré par Cloudflare : **Compute > Email Service > Email Sending > Onboard Domain** ;
2. **Resend**, en secours : secret `RESEND_API_KEY`.

Réglages facultatifs (**Settings > Variables and Secrets**) : `DEVIS_TO` (destinataires séparés par des virgules), `DEVIS_FROM` (expéditeur vérifié), `RESEND_API_KEY`.

Tant qu'aucun envoi ne fonctionne, le formulaire propose au visiteur d'envoyer sa demande par WhatsApp ou par SMS au 06 66 55 35 62.

## Nom de domaine couvreur-thorignysurmarne.fr

1. Ajouter le domaine dans Cloudflare (formule Free), puis remplacer chez le registrar les serveurs DNS par ceux indiqués par Cloudflare.
2. Une fois le domaine « Active » : **Workers & Pages > artisanrobincouverture-v2 > Settings > Domains & Routes > Add > Custom domain**, entrer `couvreur-thorignysurmarne.fr`.
3. Pour le `www` : enregistrement A `www` → `192.0.2.0` (proxy orange), puis la règle **Redirect from WWW to root** dans **Rules > Redirect Rules**. Le site est déclaré sans `www`.
4. Formulaire : ajouter le domaine dans **Compute > Email Service > Email Sending > Onboard Domain** (expéditeur `devis@couvreur-thorignysurmarne.fr`), ou renseigner `RESEND_API_KEY`.
5. Search Console : propriété de domaine `couvreur-thorignysurmarne.fr`, puis soumettre `https://couvreur-thorignysurmarne.fr/sitemap.xml`.

## À confirmer avec le client

À confirmer avec le client (voir `A_CONFIRMER` et `BUSINESS` dans `site/content.py`) :
- l'adresse : le site garde le 22 avenue Augustin Pilardeau à Mitry-Mory tant qu'aucune adresse à Thorigny-sur-Marne n'est confirmée ;
- SIRET, forme juridique, assureur décennale, médiateur de la consommation (mentions légales) ;
- la qualification RGE : l'ancien site l'affichait, le nouveau ne l'affiche pas tant qu'elle n'est pas vérifiée dans l'annuaire France Rénov'.
