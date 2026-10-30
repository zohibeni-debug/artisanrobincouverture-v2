# -*- coding: utf-8 -*-
"""Les 13 pages prestations (adresses /couverture/<slug>, identiques à l'ancien site).

Dans les textes : [[p:clé]] est remplacé par la fourchette de prix de data/prix.json,
[[table:clé1,clé2]] par un tableau de prix.
"""

SERVICES = [
    {
        "slug": "pose-toiture",
        "name": "Pose et réfection de toiture",
        "nav": "Pose et réfection",
        "short": "Tuiles, ardoise, zinc, bac acier : couverture neuve ou refaite",
        "title": "Réfection de toiture à Thorigny-sur-Marne | Artisan Robin",
        "desc": "Réfection et pose de toiture à Thorigny-sur-Marne et alentour : tuiles, ardoise, zinc, bac acier. Écran sous-toiture, liteaux neufs, devis gratuit sous 24 h.",
        "h1": "Pose et réfection de toiture à Thorigny-sur-Marne",
        "lead": "Quand les réparations ne suffisent plus, on refait la couverture : dépose, contrôle de la charpente, écran sous-toiture, liteaux et tuiles neuves. Tuiles mécaniques, petites tuiles plates, ardoise, zinc ou bac acier, à Thorigny-sur-Marne et dans les communes autour.",
        "points": ["Dépose complète et évacuation des anciens matériaux", "Écran sous-toiture et liteaux neufs", "Faîtage, rives et zinguerie refaits dans la foulée", "Garantie décennale, attestation jointe au devis"],
        "prices": ["refection_tuiles_meca", "refection_tuiles_plates", "refection_ardoise", "couverture_zinc", "bac_acier"],
        "tags": ["tuiles", "echafaudage", "chantier", "avant-apres", "ardoise"],
        "type": "Réfection complète",
        "sections": [
            ("Réparer ou refaire : comment trancher", """
<p>On refait la couverture quand les réparations deviennent répétitives ou que le support est fatigué. Les signes qui ne trompent pas : plus de 10 à 15 % de tuiles fendues ou poreuses, des liteaux qui cèdent sous le pied, des traces d'humidité à plusieurs endroits des combles, une couverture de plus de 50 ans en tuiles mécaniques d'origine.</p>
<p>Avant de vous parler de réfection, on monte sur le toit et on passe dans les combles. Si un <a href="/couverture/reparation-entretien">remaniement</a> (tuiles déposées, triées, reposées) suffit, on vous le dit : il coûte deux à trois fois moins cher.</p>"""),
            ("Ce que comprend une réfection complète", """
<ol>
<li><strong>Échafaudage et protections</strong> : façades, menuiseries et jardin protégés ; filet ou garde-corps en bas de pente.</li>
<li><strong>Dépose</strong> de la couverture et des liteaux, tri et évacuation des déchets en filière agréée.</li>
<li><strong>Contrôle de la charpente</strong> : chevrons, pannes, traces d'insectes ou de pourriture. Les pièces abîmées sont remplacées ou renforcées.</li>
<li><strong>Écran sous-toiture</strong> HPV, contre-liteaux et liteaux neufs : la lame d'air ventile les bois et protège de la neige poudreuse.</li>
<li><strong>Pose de la couverture</strong> selon le DTU du matériau, fixations adaptées à l'exposition au vent.</li>
<li><strong>Points singuliers</strong> : faîtage à sec ventilé ou scellé, rives, noues, solins de cheminée, abergements de fenêtres de toit, gouttières.</li>
</ol>
<p>Le toit n'est jamais laissé ouvert : la partie découverte est bâchée chaque soir.</p>"""),
            ("Quel matériau choisir", """
<p>Le plus souvent, on refait à l'identique : le PLU et le voisinage l'imposent souvent, et c'est la charpente qui décide du poids admissible.</p>
<ul>
<li><strong>Tuiles mécaniques terre cuite</strong> : le standard des pavillons de Thorigny, Lagny ou Chelles. Durables, faciles à réparer. [[p:refection_tuiles_meca]].</li>
<li><strong>Petites tuiles plates</strong> : sur les maisons anciennes et les toits très pentus des villages briards. Pose à 3 recouvrements, plus de main-d'œuvre. [[p:refection_tuiles_plates]].</li>
<li><strong>Ardoise naturelle</strong> : villas des bords de Marne, maisons bourgeoises, lucarnes. Pose au crochet. [[p:refection_ardoise]].</li>
<li><strong>Zinc à joint debout</strong> : faibles pentes, extensions, toitures contemporaines. [[p:couverture_zinc]].</li>
<li><strong>Bac acier</strong> : garages, ateliers, annexes. [[p:bac_acier]].</li>
</ul>"""),
            ("Prix d'une réfection de toiture", """
<p>Les prix ci-dessous sont des fourchettes 2026 constatées en Île-de-France, fourniture et pose. Le prix ferme dépend de la surface, de la pente, de l'accès pour l'échafaudage, de l'état de la charpente et du nombre de points singuliers (cheminées, fenêtres de toit, noues).</p>
[[table:refection_tuiles_meca,refection_tuiles_plates,refection_ardoise,couverture_zinc,bac_acier]]
<p>Si vous refaites plus de la moitié de la toiture d'une maison chauffée, la réglementation impose en principe d'isoler en même temps. On vous chiffre les deux options : <a href="/couverture/isolation-toiture">isolation par l'intérieur ou sarking</a>.</p>"""),
            ("Démarches avant le chantier", """
<p>Refaire à l'identique ne demande généralement pas d'autorisation. Changer de matériau, de teinte ou créer une ouverture impose une déclaration préalable en mairie. Dans le périmètre d'un monument historique, l'architecte des Bâtiments de France donne son avis : c'est le cas autour de plusieurs églises et châteaux du secteur. Si l'échafaudage empiète sur le trottoir, une autorisation de voirie se demande quelques semaines avant. On vous indique ce qu'il faut déposer et on fournit les pièces techniques.</p>"""),
        ],
        "faq": [
            ("Combien de temps dure une réfection de toiture ?", "Pour un pavillon de 100 à 120 m² de toiture, comptez une à deux semaines selon la météo, le matériau et l'état de la charpente."),
            ("Peut-on rester dans la maison pendant les travaux ?", "Oui. La couverture est ouverte par zones et bâchée chaque soir ; seuls les combles doivent être accessibles et dégagés."),
            ("Faut-il changer la charpente ?", "Rarement. On remplace les pièces abîmées et on traite les bois si besoin. Un changement de matériau plus lourd peut demander un renfort."),
            ("Quelle garantie sur une toiture refaite ?", "La garantie décennale couvre les désordres qui compromettent l'étanchéité ou la solidité pendant dix ans après la réception."),
        ],
        "related": ["reparation-entretien", "isolation-toiture", "zinguerie-gouttieres", "faitage-refection-cheminee"],
    },
    {
        "slug": "reparation-entretien",
        "name": "Réparation et entretien de toiture",
        "nav": "Réparation et entretien",
        "short": "Fuites, tuiles cassées, remaniement, visite d'entretien",
        "title": "Réparation de toiture à Thorigny-sur-Marne | Artisan Robin",
        "desc": "Réparation de toiture à Thorigny-sur-Marne : recherche de fuite, tuiles cassées, faîtières, solins, remaniement. Intervention rapide, devis gratuit sous 24 h.",
        "h1": "Réparation et entretien de toiture à Thorigny-sur-Marne",
        "lead": "Une tache au plafond, une tuile glissée, une faîtière qui bouge : on trouve l'origine de la fuite et on répare durablement, sans refaire tout le toit. Entretien régulier pour que la couverture tienne ses 50 ans et plus.",
        "points": ["Recherche de fuite méthodique, photos à l'appui", "Tuiles, faîtières, rives et solins remplacés", "Remaniement quand la casse dépasse quelques tuiles", "Rapport d'état de la couverture remis après visite"],
        "prices": ["reparation", "recherche_fuite", "remaniement"],
        "tags": ["tuiles", "chantier", "urgence"],
        "type": "Réparation de toiture",
        "sections": [
            ("D'où vient la fuite ?", """
<p>Une tache au plafond apparaît rarement à l'aplomb de la fuite : l'eau court sur l'écran ou les chevrons avant de goutter. On remonte donc le chemin de l'eau, des combles vers la couverture. Les causes les plus fréquentes, dans l'ordre :</p>
<ul>
<li><strong>Solins et abergements</strong> autour des cheminées et des fenêtres de toit : mortier fissuré, bande zinc décollée.</li>
<li><strong>Tuiles fendues ou glissées</strong>, souvent après un coup de vent ou le passage d'un antenniste.</li>
<li><strong>Faîtage scellé</strong> dont le mortier s'est fissuré : les faîtières bougent et l'eau entre par le haut.</li>
<li><strong>Noues et chéneaux</strong> encombrés de feuilles ou percés, qui débordent sous les tuiles.</li>
<li><strong>Gouttières bouchées</strong> qui refoulent sous la première rangée.</li>
</ul>
<p>Coût d'une recherche de fuite : [[p:recherche_fuite]], souvent déduit si la réparation suit.</p>"""),
            ("Les réparations courantes", """
<p>La plupart des fuites se règlent en une intervention : tuiles remplacées par des modèles compatibles, faîtières rescellées ou passées en faîtage à sec ventilé, solin refait, abergement repris. Comptez [[p:reparation]] par intervention selon l'accès et le nombre de points à traiter.</p>
<p>Quand la casse est diffuse ou que les liteaux fatiguent, on passe au <strong>remaniement</strong> : les tuiles sont déposées, triées, les liteaux défectueux changés, puis tout est reposé en complétant avec des tuiles neuves. [[p:remaniement]], soit deux à trois fois moins qu'une réfection complète.</p>"""),
            ("L'entretien qui évite les grosses factures", """
<p>Une visite tous les deux à trois ans, et après chaque tempête, suffit à garder une couverture saine. On contrôle les tuiles et le faîtage, on nettoie noues et gouttières, on vérifie les solins et les fixations des rives, on regarde la charpente depuis les combles. Sur les coteaux boisés de Thorigny, de Dampmart ou de Pomponne, où les feuilles s'accumulent, un nettoyage des gouttières chaque automne évite la plupart des débordements.</p>
<p>Si la toiture est envahie de mousse, on propose un <a href="/couverture/demoussage-nettoyage-toiture">démoussage avec traitement</a>.</p>"""),
            ("Notre façon de travailler", """
<p>On vous montre ce qu'on a vu : photos des zones abîmées, explication de la cause, et deux options chiffrées quand il y en a deux (réparation ciblée ou remaniement). Pas de réfection complète vendue quand une réparation suffit.</p>"""),
        ],
        "faq": [
            ("Pouvez-vous intervenir sous la pluie ?", "Pour une urgence, on met la maison hors d'eau avec une bâche même par mauvais temps. La réparation définitive se fait par temps sec."),
            ("Mon assurance prend-elle en charge la réparation ?", "Après une tempête, la grêle ou le poids de la neige, oui en général, selon votre contrat. On vous fournit photos et devis pour le dossier."),
            ("Combien coûte le remplacement de quelques tuiles ?", "Une intervention ponctuelle coûte [[p:reparation]] selon l'accès, la hauteur et le nombre de points à traiter."),
            ("Trouvez-vous des tuiles identiques aux miennes ?", "Le plus souvent, oui : on identifie le modèle et on récupère des tuiles compatibles, neuves ou de réemploi pour les modèles anciens."),
        ],
        "related": ["urgence-bachage", "demoussage-nettoyage-toiture", "faitage-refection-cheminee", "pose-toiture"],
    },
    {
        "slug": "zinguerie-gouttieres",
        "name": "Zinguerie et gouttières",
        "nav": "Zinguerie et gouttières",
        "short": "Gouttières, descentes, chéneaux, noues et solins en zinc",
        "title": "Gouttière zinc et zinguerie à Thorigny-sur-Marne | Artisan Robin",
        "desc": "Gouttières zinc, descentes, chéneaux, noues et solins à Thorigny-sur-Marne et alentour. Pose, remplacement, réparation par un zingueur. Devis gratuit.",
        "h1": "Zinguerie et gouttières à Thorigny-sur-Marne",
        "lead": "Gouttières pendantes ou havraises, descentes, chéneaux, noues, solins : tout ce qui conduit l'eau du toit au sol. Façonné et posé par un zingueur, en zinc naturel ou prépatiné, aluminium ou PVC.",
        "points": ["Gouttières demi-rondes, havraises ou moulurées", "Descentes, dauphins et boîtes à eau", "Noues, chéneaux et solins façonnés sur place", "Pentes contrôlées, dilatation prévue"],
        "prices": ["gouttiere_zinc", "gouttiere_pvc", "descente_zinc"],
        "tags": ["gouttiere", "zinc", "echafaudage"],
        "type": "Gouttières / zinguerie",
        "sections": [
            ("Quand faut-il changer ses gouttières ?", """
<p>Une gouttière se change quand elle fuit aux jonctions malgré les réparations, qu'elle ne tient plus sa pente (l'eau stagne et déborde) ou que les crochets ont rouillé. Les zincs d'origine des pavillons des années 1960 à 1980 arrivent en fin de vie : soudures ouvertes, fond percé, talons qui fuient.</p>
<p>Une gouttière qui déborde n'abîme pas que la façade : l'eau ruisselle le long des murs, détrempe le pied de la maison et finit par remonter sous la première rangée de tuiles.</p>"""),
            ("Zinc, aluminium ou PVC", """
<ul>
<li><strong>Zinc</strong> : la référence, durable (40 à 50 ans et plus), soudé, réparable, compatible avec tous les styles. Naturel (il se patine en gris) ou prépatiné. [[p:gouttiere_zinc]].</li>
<li><strong>Aluminium laqué</strong> : profilé en continu sur place, sans jonction, en de nombreuses teintes.</li>
<li><strong>PVC</strong> : économique, mais il se dilate et devient cassant au soleil. Réservé aux annexes. [[p:gouttiere_pvc]].</li>
</ul>
<p>Pour les descentes : [[p:descente_zinc]] en zinc, avec dauphin en fonte en pied de façade côté rue.</p>"""),
            ("La pose dans les règles", """
<p>Une gouttière doit avoir une pente régulière vers la descente (de l'ordre de 5 mm par mètre), des crochets tous les 50 cm environ, et des joints de dilatation sur les grandes longueurs. Les noues et les chéneaux encaissés sont façonnés sur mesure : c'est là que se jouent la plupart des fuites des maisons anciennes.</p>
<p>La zinguerie, c'est aussi les <strong>solins</strong> et <strong>abergements</strong> qui raccordent la couverture aux cheminées, aux murs et aux fenêtres de toit : on les refait en même temps que les gouttières si nécessaire.</p>"""),
            ("Entretien", """
<p>Un nettoyage par an, à l'automne, après la chute des feuilles ; deux sous les grands arbres des coteaux de Thorigny et de Dampmart. Une crapaudine ou une grille pare-feuilles en tête de descente évite les bouchons. Voir aussi notre guide : <a href="/blog/gouttiere-bouchee-solutions">gouttière bouchée : causes et solutions</a>.</p>"""),
        ],
        "faq": [
            ("Combien coûte une gouttière zinc posée ?", "Comptez [[p:gouttiere_zinc]] selon le profil, la hauteur et l'accès, dépose de l'ancienne gouttière comprise. Prix ferme après visite."),
            ("Peut-on réparer une gouttière zinc percée ?", "Oui, par soudure à l'étain si le zinc est sain autour. Si le fond est piqué sur toute la longueur, il faut la remplacer."),
            ("Combien de descentes faut-il ?", "Une descente pour 8 à 12 mètres de gouttière environ, selon la surface de toit qu'elle draine et l'intensité des pluies."),
            ("Faut-il un échafaudage ?", "Sur un pavillon de plain-pied ou à un étage, une nacelle ou un échafaudage roulant suffit souvent. On le chiffre à part sur le devis."),
        ],
        "related": ["faitage-refection-cheminee", "reparation-entretien", "bardage-facade", "demoussage-nettoyage-toiture"],
    },
    {
        "slug": "isolation-toiture",
        "name": "Isolation de toiture",
        "nav": "Isolation de toiture",
        "short": "Sarking, rampants, combles perdus : la chaleur ne s'échappe plus",
        "title": "Isolation de toiture à Thorigny-sur-Marne | Artisan Robin",
        "desc": "Isolation de toiture à Thorigny-sur-Marne : sarking par l'extérieur, rampants, combles perdus. Prix 2026, aides en vigueur, devis gratuit sous 24 h.",
        "h1": "Isolation de toiture à Thorigny-sur-Marne",
        "lead": "Jusqu'à 30 % de la chaleur d'une maison mal isolée s'échappe par le toit. Selon votre chantier, on isole par l'extérieur (sarking) en refaisant la couverture, par l'intérieur sous les rampants, ou par soufflage dans les combles perdus.",
        "points": ["Sarking : isolation continue sans toucher aux pièces", "Rampants isolés avec pare-vapeur étanche", "Combles perdus par soufflage", "Résistance thermique conforme aux exigences en vigueur"],
        "prices": ["sarking", "isolation_rampants", "isolation_combles_perdus"],
        "tags": ["isolation", "charpente", "chantier"],
        "type": "Isolation de toiture",
        "sections": [
            ("Trois techniques, trois situations", """
<ul>
<li><strong>Le sarking</strong> (isolation par l'extérieur) : les panneaux isolants sont posés sur les chevrons, puis la couverture par-dessus. Aucune perte de volume, ponts thermiques supprimés, charpente apparente possible. C'est la bonne solution quand on refait la couverture. [[p:sarking]].</li>
<li><strong>Les rampants par l'intérieur</strong> : isolant entre et sous les chevrons, membrane pare-vapeur, plaques de plâtre. Pour des combles habités dont la couverture est saine. [[p:isolation_rampants]].</li>
<li><strong>Les combles perdus par soufflage</strong> : laine soufflée sur le plancher des combles non aménagés. Rapide et très efficace pour le prix. [[p:isolation_combles_perdus]].</li>
</ul>"""),
            ("Isoler en refaisant la toiture : l'obligation à connaître", """
<p>Quand on refait plus de la moitié de la couverture d'une maison chauffée, la réglementation impose en principe d'isoler en même temps, sauf impossibilité technique ou coût disproportionné. C'est aussi le moment le moins cher pour le faire : l'échafaudage est monté et la couverture est déposée. On vous chiffre la réfection seule et la réfection avec sarking pour comparer.</p>"""),
            ("Les aides en 2026 : ce qui a changé", """
<p>Depuis le 1<sup>er</sup> septembre 2026, MaPrimeRénov' ne finance plus l'isolation de la toiture réalisée seule (« par geste »). Elle reste aidée dans une rénovation d'ampleur accompagnée. Hors MaPrimeRénov', restent possibles la prime énergie (CEE), l'éco-prêt à taux zéro et la TVA à 5,5 %, sous conditions, notamment de recours à une entreprise qualifiée RGE pour certaines aides.</p>
<p>Le détail, avec les conditions et les montants : <a href="/blog/aides-isolation-toiture-2025">aides à l'isolation de toiture en 2026</a> et <a href="/blog/maprimerenov-2025-toiture">MaPrimeRénov' et toiture</a>.</p>"""),
            ("Les points qui font une bonne isolation", """
<p>Un isolant performant mal posé ne sert à rien. On soigne la continuité de l'isolant (pas de jour entre les panneaux), l'étanchéité à l'air du pare-vapeur côté chaud, la lame d'air sous la couverture pour ventiler les bois, et le traitement des points singuliers : sablières, pignons, fenêtres de toit, conduits de cheminée avec leur écart au feu.</p>"""),
        ],
        "faq": [
            ("Quelle épaisseur d'isolant pour une toiture ?", "Pour viser une résistance thermique de 6 à 7 m².K/W en rampants, comptez environ 20 à 30 cm selon l'isolant. En combles perdus, 30 à 40 cm de laine soufflée."),
            ("Le sarking est-il possible sur toutes les maisons ?", "Il demande de déposer la couverture et rehausse légèrement le toit. Le PLU peut l'encadrer : on vérifie avant de le proposer."),
            ("Combien de temps durent les travaux ?", "Une journée pour des combles perdus, quelques jours pour des rampants, une à deux semaines pour un sarking avec réfection."),
            ("L'isolation peut-elle être aidée en 2026 ?", "Pas par MaPrimeRénov' en geste isolé depuis septembre 2026, mais la prime CEE, l'éco-PTZ et la TVA réduite restent possibles sous conditions."),
        ],
        "related": ["pose-toiture", "amenagement-combles", "velux-fenetres-toit", "charpente"],
    },
    {
        "slug": "urgence-bachage",
        "name": "Urgence toiture et bâchage",
        "nav": "Urgence et bâchage",
        "short": "Fuite, tempête, tuiles envolées : hors d'eau 7 j/7",
        "title": "Urgence toiture et bâchage à Thorigny-sur-Marne | 7 j/7",
        "desc": "Urgence toiture à Thorigny-sur-Marne et alentour, 7 j/7 : bâchage, fuite, tuiles envolées après tempête. Mise hors d'eau rapide. Appelez le 07 64 07 31 49.",
        "h1": "Urgence toiture et bâchage à Thorigny-sur-Marne",
        "lead": "Tempête, chute d'arbre, infiltration soudaine : on intervient 7 jours sur 7 pour mettre votre maison hors d'eau avec une bâche arrimée, puis on chiffre la réparation définitive. Photos fournies pour votre assurance.",
        "points": ["Joignables 7 j/7 au 07 64 07 31 49", "Bâche lestée et arrimée, pas seulement posée", "Photos et constat pour l'assureur", "Réparation définitive chiffrée dans la foulée"],
        "prices": ["bachage", "recherche_fuite", "reparation"],
        "tags": ["urgence", "tuiles", "chantier"],
        "type": "Fuite / urgence",
        "sections": [
            ("Que faire en attendant notre arrivée", """
<ol>
<li><strong>Ne montez pas sur le toit</strong>, surtout mouillé ou par vent fort.</li>
<li>Coupez l'électricité de la zone touchée si l'eau approche des plafonniers ou des prises.</li>
<li>Placez des bassines, protégez meubles et sols, percez une poche d'eau au plafond seulement si vous savez le faire en sécurité.</li>
<li>Prenez des photos des dégâts, dedans et dehors, depuis le sol.</li>
<li>Appelez-nous au <a href="tel:+33764073149">07 64 07 31 49</a>, puis prévenez votre assureur.</li>
</ol>"""),
            ("Le bâchage : une mise hors d'eau qui tient", """
<p>Une bâche simplement posée s'envole à la première rafale. On utilise une bâche armée, déroulée par-dessus le faîtage quand c'est possible, lestée et arrimée sur les liteaux ou la charpente, sans percer la couverture saine. Elle protège la maison le temps de commander les matériaux et de planifier la réparation.</p>
<p>Prix d'un bâchage d'urgence : [[p:bachage]] selon la surface et l'accès. Si l'origine de la fuite est inconnue, une recherche de fuite coûte [[p:recherche_fuite]].</p>"""),
            ("Assurance : les bons réflexes", """
<p>Les dommages causés par la tempête, la grêle ou le poids de la neige sont en général couverts par l'assurance habitation, dans un délai de déclaration court fixé par votre contrat. En cas d'arrêté de catastrophe naturelle, le délai court à partir de sa publication. Conservez les factures de bâchage : elles font partie du sinistre. On vous remet photos, constat et devis de réparation pour l'expert. Plus de détails dans notre guide <a href="/blog/toiture-apres-tempete">toiture après une tempête</a>.</p>"""),
            ("Après l'urgence", """
<p>Une fois la maison hors d'eau, on revient par temps sec pour la réparation définitive : tuiles et faîtières remplacées, solins refaits, ou <a href="/couverture/reparation-entretien">remaniement</a> de la zone touchée. Si la tempête a révélé une couverture en fin de vie, on vous propose aussi le chiffrage d'une <a href="/couverture/pose-toiture">réfection</a>, sans pression.</p>"""),
        ],
        "faq": [
            ("Intervenez-vous le week-end ?", "Oui, 7 jours sur 7 pour les urgences : fuite active, tuiles envolées, arbre tombé sur le toit."),
            ("Combien coûte un bâchage d'urgence ?", "Comptez [[p:bachage]] selon la surface à couvrir, la hauteur et l'accès. Le montant est en général pris en compte par l'assurance en cas de sinistre couvert."),
            ("Combien de temps une bâche peut-elle rester ?", "Quelques semaines si elle est bien arrimée et contrôlée. Ce n'est pas une solution durable : la réparation doit suivre."),
            ("Vous occupez-vous de l'expert de l'assurance ?", "On vous fournit photos, constat et devis détaillé, et on peut être présent lors du passage de l'expert si besoin."),
        ],
        "related": ["reparation-entretien", "pose-toiture", "charpente", "faitage-refection-cheminee"],
    },
    {
        "slug": "charpente",
        "name": "Charpente",
        "nav": "Charpente",
        "short": "Diagnostic, traitement, renfort et remplacement des bois",
        "title": "Charpentier à Thorigny-sur-Marne : charpente bois | Artisan Robin",
        "desc": "Charpentier à Thorigny-sur-Marne : diagnostic, traitement curatif, remplacement de chevrons et pannes, renfort, création d'ouvertures. Devis gratuit.",
        "h1": "Charpente à Thorigny-sur-Marne",
        "lead": "La charpente porte tout le reste. On la diagnostique à chaque visite, on traite les bois attaqués, on remplace chevrons et pannes abîmés, on renforce avant une couverture plus lourde ou une ouverture. Charpentier et couvreur : un seul interlocuteur pour tout le toit.",
        "points": ["Diagnostic depuis les combles et sur le toit", "Traitement curatif insectes et champignons", "Remplacement ou doublage de chevrons, pannes, sablières", "Chevêtres pour fenêtres de toit et lucarnes"],
        "prices": ["traitement_charpente", "charpente_neuve"],
        "tags": ["charpente", "chantier", "echafaudage"],
        "type": "Charpente",
        "sections": [
            ("Les signes d'une charpente à reprendre", """
<ul>
<li>Un faîtage qui se creuse ou un versant qui ondule, visible depuis la rue.</li>
<li>Des bois qui sonnent creux, de la sciure (vrillettes) ou des galeries en surface (capricornes).</li>
<li>Des traces noires ou un bois spongieux là où une fuite a duré : pourriture, parfois mérule dans les cas graves.</li>
<li>Des fissures dans les murs en haut des pignons, signe de poussée de la charpente.</li>
</ul>"""),
            ("Ce que l'on fait", """
<p><strong>Traitement curatif</strong> : bûchage des parties atteintes, injection et pulvérisation d'un produit insecticide et fongicide. [[p:traitement_charpente]].</p>
<p><strong>Remplacement et renfort</strong> : chevrons doublés ou changés, panne remplacée, sablière reprise, contreventement ajouté. Pour une réfection lourde ou une charpente neuve : [[p:charpente_neuve]].</p>
<p><strong>Modifications</strong> : chevêtre pour une <a href="/couverture/velux-fenetres-toit">fenêtre de toit</a>, ouverture pour une lucarne, adaptation pour un <a href="/couverture/amenagement-combles">aménagement de combles</a>. Toute modification de structure se fait avec un calcul adapté.</p>"""),
            ("Charpentier et couvreur : l'intérêt d'un seul artisan", """
<p>Quand la couverture est déposée, la charpente est accessible : c'est le moment de la contrôler et de la reprendre. Un seul intervenant évite les allers-retours entre corps de métier, les responsabilités floues et les jours de toit ouvert. Les travaux de charpente sont couverts par la garantie décennale.</p>"""),
        ],
        "faq": [
            ("Faut-il traiter une charpente préventivement ?", "Sur une charpente saine et sèche, ce n'est pas systématique. On traite en curatif dès qu'on voit des insectes ou des champignons, et en préventif sur les bois neufs non traités."),
            ("Le termite est-il présent dans le secteur ?", "Des arrêtés préfectoraux délimitent les zones à termites. En cas de doute, le diagnostic termites avant vente indique la situation de votre commune."),
            ("Peut-on poser des tuiles plus lourdes sur ma charpente ?", "Pas sans vérification : passer de la tuile mécanique à la petite tuile plate ou à l'ardoise peut imposer un renfort."),
            ("Combien coûte le remplacement d'une charpente ?", "Pour une charpente traditionnelle neuve ou remplacée, comptez [[p:charpente_neuve]], selon la portée, la forme du toit et l'accès."),
        ],
        "related": ["pose-toiture", "amenagement-combles", "velux-fenetres-toit", "isolation-toiture"],
    },
    {
        "slug": "velux-fenetres-toit",
        "name": "Velux et fenêtres de toit",
        "nav": "Velux et fenêtres de toit",
        "short": "Pose, remplacement et réparation de fenêtres de toit",
        "title": "Pose de Velux à Thorigny-sur-Marne | Artisan Robin",
        "desc": "Pose, remplacement et réparation de Velux et fenêtres de toit (Velux, Fakro, Roto) à Thorigny-sur-Marne. Raccords étanches, finitions intérieures. Devis gratuit.",
        "h1": "Velux et fenêtres de toit à Thorigny-sur-Marne",
        "lead": "Création d'une fenêtre de toit, remplacement d'un Velux qui fuit ou ne ferme plus, réparation d'un raccord : on ouvre, on charpente, on raccorde à la couverture et on finit l'intérieur. Velux, Fakro, Roto.",
        "points": ["Création d'ouverture avec chevêtre", "Raccord d'étanchéité adapté à la couverture", "Remplacement en lieu et place, sans casse intérieure", "Volets, stores, motorisation"],
        "prices": ["velux_remplacement", "velux_creation"],
        "tags": ["velux", "tuiles", "isolation"],
        "type": "Velux / fenêtre de toit",
        "sections": [
            ("Remplacer ou créer", """
<p><strong>Remplacement</strong> : une fenêtre de toit de 20 à 30 ans devient moins étanche et isole mal. Les grands fabricants proposent des modèles de remplacement aux mêmes dimensions : on dépose l'ancienne, on pose la nouvelle avec son raccord, sans toucher aux finitions intérieures dans la plupart des cas. [[p:velux_remplacement]].</p>
<p><strong>Création</strong> : on découpe la couverture, on crée un chevêtre dans la charpente, on pose la fenêtre, son raccord et son isolation périphérique, puis les finitions intérieures. [[p:velux_creation]].</p>"""),
            ("Les fuites autour d'une fenêtre de toit", """
<p>Neuf fois sur dix, ce n'est pas la fenêtre qui fuit mais son raccord : tuiles mal recoupées, bavette décollée, gouttière haute bouchée par les feuilles, ou pose sur une pente inférieure au minimum du fabricant. On vérifie le raccord avant de conclure qu'il faut tout changer.</p>"""),
            ("Démarches et choix", """
<p>Créer une fenêtre de toit modifie l'aspect extérieur : une déclaration préalable est nécessaire. Côté choix, on vous conseille la taille (une surface vitrée d'au moins un sixième de la surface au sol pour une pièce à vivre est une bonne base), l'ouverture (rotation ou projection), le vitrage et les équipements : volet roulant solaire pour l'été, store occultant pour une chambre.</p>"""),
        ],
        "faq": [
            ("Faut-il une autorisation pour poser un Velux ?", "Oui, une déclaration préalable en mairie pour une création. Le remplacement à l'identique n'en demande généralement pas."),
            ("Combien de temps dure la pose ?", "Une demi-journée à une journée pour un remplacement, une à deux journées pour une création avec finitions."),
            ("Mon Velux fuit, faut-il le changer ?", "Pas forcément : la fuite vient souvent du raccord ou des tuiles autour. On diagnostique avant de proposer un remplacement."),
            ("Posez-vous des volets roulants sur Velux existant ?", "Oui, la plupart des fenêtres de toit récentes acceptent un volet roulant solaire ou électrique posé par l'extérieur."),
        ],
        "related": ["amenagement-combles", "isolation-toiture", "charpente", "reparation-entretien"],
    },
    {
        "slug": "etancheite-toiture",
        "name": "Étanchéité de toiture et toit plat",
        "nav": "Étanchéité et toit plat",
        "short": "Toits-terrasses, extensions, garages : EPDM et bitume",
        "title": "Étanchéité toit plat à Thorigny-sur-Marne | Artisan Robin",
        "desc": "Étanchéité de toit plat et toit-terrasse à Thorigny-sur-Marne : membrane EPDM, bitume, relevés, évacuations. Réparation de fuite et réfection. Devis gratuit.",
        "h1": "Étanchéité de toiture et toit plat à Thorigny-sur-Marne",
        "lead": "Extensions, garages, toits-terrasses des maisons de ville : un toit plat ne pardonne pas l'approximation. On refait l'étanchéité en membrane EPDM ou en bitume élastomère, relevés et évacuations compris.",
        "points": ["Membrane EPDM d'un seul tenant", "Bitume élastomère bicouche", "Relevés, costières et évacuations refaits", "Isolation du toit plat possible en même temps"],
        "prices": ["etancheite_epdm", "etancheite_bitume"],
        "tags": ["toit-plat", "zinc", "chantier"],
        "type": "Toit plat / étanchéité",
        "sections": [
            ("Pourquoi un toit plat fuit", """
<p>Les fuites viennent rarement du milieu de la surface. Elles naissent aux <strong>relevés</strong> (le long des murs et des acrotères), autour des <strong>évacuations</strong> bouchées qui laissent l'eau stagner, aux jonctions mal soudées et aux traversées (ventilations, conduits). Une membrane bitumineuse de plus de 20 ans, craquelée et cloquée, arrive en fin de vie.</p>"""),
            ("EPDM ou bitume", """
<ul>
<li><strong>EPDM</strong> : membrane caoutchouc souvent posée d'un seul tenant sur les petites surfaces, sans joint au milieu, très souple et durable. Idéale pour les extensions et garages. [[p:etancheite_epdm]].</li>
<li><strong>Bitume élastomère (SBS)</strong> : deux couches soudées au chalumeau, éprouvé sur les toits-terrasses. [[p:etancheite_bitume]].</li>
</ul>
<p>Dans les deux cas, on soigne la pente vers les évacuations, les relevés d'au moins 15 cm, les costières et le trop-plein. Les toitures-terrasses relèvent du DTU 43.1.</p>"""),
            ("Isoler en même temps", """
<p>Refaire l'étanchéité est l'occasion d'isoler le toit plat par-dessus (toiture chaude) : panneaux isolants posés sur le support, sous la nouvelle membrane. La pièce gagne en confort, été comme hiver.</p>"""),
        ],
        "faq": [
            ("Combien de temps dure une étanchéité EPDM ?", "Bien posée et entretenue, une membrane EPDM dure plusieurs décennies. Le point faible reste les évacuations à nettoyer."),
            ("Peut-on réparer plutôt que refaire ?", "Oui si la membrane est saine et la fuite localisée : on reprend la jonction ou le relevé. Si elle est craquelée partout, il faut refaire."),
            ("Un toit plat a-t-il besoin d'entretien ?", "Oui : nettoyage des évacuations et contrôle des relevés une à deux fois par an, surtout sous les arbres."),
            ("Faites-vous la couverture zinc des petites pentes ?", "Oui, le zinc à joint debout convient aux faibles pentes. Voir notre page pose et réfection de toiture."),
        ],
        "related": ["zinguerie-gouttieres", "isolation-toiture", "pose-toiture", "reparation-entretien"],
    },
    {
        "slug": "demoussage-nettoyage-toiture",
        "name": "Démoussage et nettoyage de toiture",
        "nav": "Démoussage et nettoyage",
        "short": "Brossage, anti-mousse, hydrofuge : un toit propre et protégé",
        "title": "Démoussage de toiture à Thorigny-sur-Marne | Artisan Robin",
        "desc": "Démoussage et nettoyage de toiture à Thorigny-sur-Marne : brossage, traitement anti-mousse, hydrofuge, gouttières nettoyées. Prix au m², devis gratuit.",
        "h1": "Démoussage et nettoyage de toiture à Thorigny-sur-Marne",
        "lead": "La mousse retient l'eau, soulève les tuiles et les fait éclater au gel. On l'enlève sans abîmer la couverture, on traite pour qu'elle ne revienne pas trop vite, et on applique un hydrofuge si la tuile le permet.",
        "points": ["Brossage manuel, pas de haute pression destructrice", "Traitement anti-mousse et anti-lichen", "Hydrofuge en option sur tuiles poreuses", "Gouttières et noues nettoyées dans la foulée"],
        "prices": ["demoussage", "demoussage_hydrofuge"],
        "tags": ["demoussage", "avant-apres", "tuiles"],
        "type": "Démoussage / nettoyage",
        "sections": [
            ("Pourquoi démousser", """
<p>Sur les versants nord et sous les arbres, nombreux sur les coteaux de Thorigny, Dampmart et Pomponne et le long de la Marne, la mousse s'installe vite. Elle agit comme une éponge : l'eau stagne, pénètre la tuile, gèle et la fait éclater. Les coussins de mousse soulèvent aussi les tuiles et bouchent gouttières et noues.</p>"""),
            ("Notre méthode", """
<ol>
<li><strong>Contrôle</strong> de la couverture : on remplace les tuiles cassées avant de traiter.</li>
<li><strong>Brossage</strong> et grattage des mousses, à la main. Le nettoyeur haute pression, mal utilisé, use la surface des tuiles et pousse l'eau sous la couverture : on ne s'en sert qu'à basse pression, quand le matériau le supporte.</li>
<li><strong>Traitement anti-mousse</strong> pulvérisé, qui agit dans les semaines suivantes.</li>
<li><strong>Hydrofuge</strong> en option, sur tuiles sèches et saines : il limite l'absorption d'eau et retarde le retour des mousses.</li>
<li><strong>Nettoyage</strong> des gouttières, des noues et des abords.</li>
</ol>"""),
            ("Prix et fréquence", """
<p>Démoussage et traitement : [[p:demoussage]]. Avec hydrofuge : [[p:demoussage_hydrofuge]]. Le prix ferme dépend de la surface, de la pente, de l'accès et de l'état de la couverture.</p>
<p>Comptez un démoussage tous les 5 à 10 ans selon l'exposition. Un toit à l'ombre de grands arbres en demande plus souvent. Pour aller plus loin : <a href="/blog/demoussage-toiture-prix-methodes">démoussage : prix, méthodes et fréquence</a>.</p>"""),
        ],
        "faq": [
            ("Le démoussage abîme-t-il les tuiles ?", "Non s'il est fait au brossage et à basse pression. La haute pression mal maîtrisée, elle, use la surface des tuiles."),
            ("L'hydrofuge est-il utile ?", "Sur des tuiles poreuses mais saines, oui : il réduit l'absorption d'eau. Sur des tuiles très usées, mieux vaut envisager un remaniement ou une réfection."),
            ("Quelle est la meilleure saison ?", "Le printemps et le début de l'automne, par temps sec et sans gel, pour que le traitement agisse."),
            ("Peut-on peindre une toiture en tuiles ?", "On ne le conseille pas sur la terre cuite : la peinture masque l'état réel des tuiles. Un hydrofuge incolore est préférable."),
        ],
        "related": ["reparation-entretien", "zinguerie-gouttieres", "pose-toiture", "faitage-refection-cheminee"],
    },
    {
        "slug": "ramonage-cheminee",
        "name": "Ramonage de cheminée",
        "nav": "Ramonage",
        "short": "Ramonage mécanique, certificat remis, contrôle du conduit",
        "title": "Ramonage de cheminée à Thorigny-sur-Marne | Artisan Robin",
        "desc": "Ramonage de cheminée, poêle et insert à Thorigny-sur-Marne : ramonage mécanique, certificat de ramonage remis, contrôle du conduit et de la souche.",
        "h1": "Ramonage de cheminée à Thorigny-sur-Marne",
        "lead": "Ramonage mécanique des conduits de cheminée, d'insert et de poêle, avec certificat remis le jour même. Couvreurs, on contrôle aussi la souche, le chapeau et le solin depuis le toit.",
        "points": ["Ramonage mécanique au hérisson", "Certificat de ramonage remis", "Contrôle de la souche, du chapeau, du solin", "Protection de la pièce, aucune salissure"],
        "prices": ["ramonage"],
        "tags": ["cheminee", "tuiles"],
        "type": "Ramonage",
        "sections": [
            ("Pourquoi c'est obligatoire", """
<p>Le ramonage élimine la suie et le bistre qui rétrécissent le conduit et peuvent s'enflammer : c'est la première prévention du feu de cheminée et de l'intoxication au monoxyde de carbone. Le règlement sanitaire départemental fixe la fréquence : pour un conduit de bois ou de fioul utilisé régulièrement, c'est en général deux ramonages par an, dont un pendant la saison de chauffe ; pour le gaz, un par an. Votre assureur peut demander le certificat après un sinistre.</p>"""),
            ("Comment se passe un ramonage", """
<p>On protège l'âtre et la pièce, on ramone mécaniquement le conduit au hérisson adapté à son diamètre, on récupère les suies et on contrôle le tirage. Le certificat de ramonage, qui précise le conduit traité, vous est remis à la fin. Prix : [[p:ramonage]] par conduit.</p>"""),
            ("Le conduit vu du toit", """
<p>Un conduit propre ne suffit pas si la souche fuit. Depuis le toit, on vérifie les joints de la souche en brique, le chapeau, la mitre et le solin qui raccorde la cheminée à la couverture. Ce sont des points de fuite fréquents sur les maisons de plus de 50 ans : voir <a href="/couverture/faitage-refection-cheminee">faîtage et réfection de cheminée</a>.</p>"""),
        ],
        "faq": [
            ("Quand faire ramoner ?", "Avant la saison de chauffe, à la fin de l'été ou au début de l'automne, puis une seconde fois pendant la saison pour le bois."),
            ("Le certificat est-il obligatoire ?", "Il prouve que le ramonage a été fait par un professionnel. Gardez-le : l'assureur peut le demander."),
            ("Ramonez-vous les poêles à granulés ?", "Oui, les conduits de poêles et d'inserts. L'entretien de l'appareil lui-même relève du chauffagiste."),
            ("Que faire si le conduit est bouché par un nid ?", "On le dégage et on pose un chapeau grillagé pour éviter que les oiseaux reviennent."),
        ],
        "related": ["faitage-refection-cheminee", "reparation-entretien", "zinguerie-gouttieres", "demoussage-nettoyage-toiture"],
    },
    {
        "slug": "bardage-facade",
        "name": "Pose de bardage",
        "nav": "Bardage",
        "short": "Bois, composite, fibres-ciment, zinc, avec ou sans isolation",
        "title": "Pose de bardage à Thorigny-sur-Marne | Artisan Robin",
        "desc": "Pose de bardage bois, composite, fibres-ciment ou zinc à Thorigny-sur-Marne, avec ou sans isolation par l'extérieur. Pignons, lucarnes, extensions. Devis gratuit.",
        "h1": "Pose de bardage à Thorigny-sur-Marne",
        "lead": "Pignons exposés, lucarnes, extensions, avancées de toit : le bardage protège et transforme une façade. Bois, composite, fibres-ciment ou zinc, sur ossature ventilée, avec isolation par l'extérieur si vous le souhaitez.",
        "points": ["Ossature ventilée, lame d'air conforme", "Bois, composite, fibres-ciment, zinc", "Isolation par l'extérieur possible", "Habillage de lucarnes, rives et sous-faces"],
        "prices": ["bardage"],
        "tags": ["zinc", "chantier", "echafaudage"],
        "type": "Bardage",
        "sections": [
            ("Où poser un bardage", """
<p>Sur un pignon battu par la pluie, une jouée de lucarne, une extension ou une façade à rafraîchir. Le bardage protège le mur, cache un support abîmé et peut accueillir une isolation par l'extérieur entre les tasseaux.</p>"""),
            ("Les matériaux", """
<ul>
<li><strong>Bois</strong> (douglas, mélèze, red cedar, bois traité) : chaleureux, il grise naturellement ou se lasure.</li>
<li><strong>Composite</strong> : peu d'entretien, teintes stables.</li>
<li><strong>Fibres-ciment</strong> : stable, incombustible, nombreuses finitions.</li>
<li><strong>Zinc</strong> : en cassettes ou à joint debout, pour les lucarnes et les façades contemporaines.</li>
</ul>
<p>Prix posé : [[p:bardage]] selon le matériau, la hauteur et l'isolation éventuelle.</p>"""),
            ("Les règles d'une bonne pose", """
<p>Le bardage se pose sur une ossature avec une lame d'air ventilée derrière, ouverte en bas et en haut, des grilles anti-rongeurs et un pare-pluie si on isole. Les angles, les tableaux de fenêtres et les jonctions avec la toiture sont traités par des pièces de finition, souvent en zinc. Un bardage modifie l'aspect de la façade : une déclaration préalable est nécessaire.</p>"""),
        ],
        "faq": [
            ("Faut-il une autorisation pour poser un bardage ?", "Oui, une déclaration préalable, car l'aspect extérieur change. Le PLU peut imposer des matériaux ou des teintes."),
            ("Le bardage bois demande-t-il de l'entretien ?", "Laissé brut, il grise sans entretien. Pour garder la teinte d'origine, une lasure tous les quelques années est nécessaire."),
            ("Peut-on isoler sous un bardage ?", "Oui : l'isolant se place entre les tasseaux, protégé par un pare-pluie, avec la lame d'air ventilée devant."),
            ("Posez-vous le bardage sur les lucarnes ?", "Oui, en bois, ardoise ou zinc, avec les raccords d'étanchéité à la couverture."),
        ],
        "related": ["zinguerie-gouttieres", "isolation-toiture", "pose-toiture", "charpente"],
    },
    {
        "slug": "amenagement-combles",
        "name": "Aménagement de combles",
        "nav": "Aménagement de combles",
        "short": "Une pièce de plus sous le toit : isolation, plancher, fenêtres",
        "title": "Aménagement de combles à Thorigny-sur-Marne | Artisan Robin",
        "desc": "Aménagement de combles à Thorigny-sur-Marne : faisabilité, renfort de charpente, isolation, plancher, fenêtres de toit, démarches. Devis gratuit.",
        "h1": "Aménagement de combles à Thorigny-sur-Marne",
        "lead": "Une chambre, un bureau ou une salle de jeux sous le toit : on vérifie la faisabilité, on adapte la charpente, on isole, on crée les fenêtres de toit et le plancher. L'ossature et la couverture faites par le même artisan.",
        "points": ["Étude de faisabilité : hauteur, charpente, plancher", "Transformation de fermettes si nécessaire", "Isolation des rampants et fenêtres de toit", "Démarches d'urbanisme préparées"],
        "prices": ["amenagement_combles", "velux_creation", "isolation_rampants"],
        "tags": ["isolation", "velux", "charpente"],
        "type": "Aménagement de combles",
        "sections": [
            ("Vos combles sont-ils aménageables ?", """
<p>Trois critères décident : la <strong>hauteur</strong> (au moins 1,80 m sous le faîtage sur une bonne partie de la surface pour que la pièce soit utile), la <strong>charpente</strong> (une charpente traditionnelle laisse l'espace libre ; des fermettes en W doivent être transformées) et le <strong>plancher</strong>, qui doit supporter une pièce habitée. Il faut aussi prévoir l'escalier.</p>"""),
            ("Les étapes", """
<ol>
<li>Visite et faisabilité, relevé des hauteurs.</li>
<li>Renfort ou transformation de la charpente si nécessaire.</li>
<li>Plancher porteur, création des <a href="/couverture/velux-fenetres-toit">fenêtres de toit</a>.</li>
<li><a href="/couverture/isolation-toiture">Isolation des rampants</a> et pare-vapeur.</li>
<li>Cloisons, doublages et finitions, ou coordination avec les autres corps d'état.</li>
</ol>
<p>Ordre de grandeur pour un aménagement complet : [[p:amenagement_combles]] de surface créée.</p>"""),
            ("Les démarches", """
<p>Créer de la surface de plancher demande une déclaration préalable au-delà de 5 m², et un permis de construire au-delà de 20 m² (40 m² en zone urbaine d'une commune dotée d'un PLU, sauf si la surface totale dépasse alors 150 m², où l'architecte devient obligatoire). Les fenêtres de toit modifient l'aspect extérieur. On prépare les pièces techniques de votre dossier.</p>"""),
        ],
        "faq": [
            ("Quelle hauteur minimum pour aménager des combles ?", "Comptez au moins 1,80 m sous le faîtage sur une partie suffisante de la surface ; les zones plus basses servent de rangements."),
            ("Peut-on aménager des combles à fermettes ?", "Oui, en transformant les fermettes par une charpente qui libère l'espace. C'est un chantier de charpente à part entière."),
            ("Faut-il un permis de construire ?", "Au-delà de 20 m² créés (40 m² en zone urbaine avec PLU), oui. En dessous, une déclaration préalable suffit."),
            ("Combien coûte un aménagement de combles ?", "Comptez [[p:amenagement_combles]] de surface aménagée, selon l'état de la charpente, l'isolation et les finitions."),
        ],
        "related": ["isolation-toiture", "velux-fenetres-toit", "charpente", "pose-toiture"],
    },
    {
        "slug": "faitage-refection-cheminee",
        "name": "Faîtage et cheminée",
        "nav": "Faîtage et cheminée",
        "short": "Faîtage scellé ou ventilé, solins, souches de cheminée",
        "title": "Faîtage et réfection de cheminée à Thorigny-sur-Marne",
        "desc": "Réfection de faîtage (scellé ou à sec ventilé), solins et souches de cheminée à Thorigny-sur-Marne et alentour. Fin des fuites par le haut du toit. Devis gratuit.",
        "h1": "Faîtage et réfection de cheminée à Thorigny-sur-Marne",
        "lead": "Le faîtage et la cheminée sont les deux points hauts du toit, et deux sources de fuite fréquentes. On rescelle ou on remplace le faîtage par un faîtage à sec ventilé, on refait les solins et on rénove les souches de cheminée.",
        "points": ["Faîtage scellé refait ou passé à sec ventilé", "Closoirs ventilés, faîtières fixées", "Solins zinc ou mortier refaits", "Souche rejointoyée ou remontée, chapeau posé"],
        "prices": ["faitage", "solin", "souche_cheminee"],
        "tags": ["cheminee", "tuiles", "zinc"],
        "type": "Cheminée / faîtage",
        "sections": [
            ("Le faîtage : scellé ou à sec", """
<p>Sur les maisons anciennes, les faîtières sont scellées au mortier. Avec les années, le mortier se fissure et se détache : les faîtières bougent, l'eau entre par le haut et coule le long des chevrons. Deux solutions :</p>
<ul>
<li><strong>Rescellement</strong> au mortier de chaux bâtarde, à l'identique, pour les toitures où l'aspect traditionnel compte.</li>
<li><strong>Faîtage à sec ventilé</strong> : closoir ventilé et faîtières fixées mécaniquement. Plus de mortier qui casse, et une ventilation de la sous-face qui assèche les bois.</li>
</ul>
<p>Prix : [[p:faitage]] selon le linéaire, la pente et le type de faîtières.</p>"""),
            ("Les solins de cheminée", """
<p>Le solin raccorde la couverture à la souche. Un solin au mortier fissuré ou une bande zinc décollée laissent passer l'eau le long de la cheminée, avec des traces sur le conduit dans les combles. On refait le solin avec abergement zinc façonné et bande de recouvrement engravée : [[p:solin]].</p>"""),
            ("Réfection de souche", """
<p>Briques gelées, joints creusés, chapeau absent ou fendu : on rejointoie, on remonte la souche si nécessaire, on pose un chapeau ou une mitre. Si la cheminée ne sert plus, on peut la condamner proprement ou la démolir sous la couverture et refaire la toiture à cet endroit. [[p:souche_cheminee]].</p>"""),
        ],
        "faq": [
            ("Comment savoir si mon faîtage fuit ?", "Mortier fissuré ou manquant entre les faîtières, faîtières décalées, traces d'humidité sur les chevrons en haut des combles."),
            ("Le faîtage à sec est-il autorisé partout ?", "Il est très répandu. Dans un secteur protégé, l'architecte des Bâtiments de France peut demander un faîtage scellé traditionnel."),
            ("Peut-on supprimer une cheminée inutilisée ?", "Oui : on démolit la souche sous la couverture et on refait la toiture à cet endroit, ou on la condamne en gardant une ventilation."),
            ("Combien coûte la réfection d'une souche ?", "Comptez [[p:souche_cheminee]] selon la hauteur, l'état des briques et l'accès."),
        ],
        "related": ["reparation-entretien", "ramonage-cheminee", "zinguerie-gouttieres", "pose-toiture"],
    },
]

BY_SLUG = {s["slug"]: s for s in SERVICES}
