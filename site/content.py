# -*- coding: utf-8 -*-
"""Contenus communs du site couvreur-thorignysurmarne.fr (ARTISAN ROBIN COUVERTURE) : entreprise, prix, étapes, FAQ, avis, secteurs, redirections."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SITE_URL = "https://couvreur-thorignysurmarne.fr"

BUSINESS = {
    "name": "ARTISAN ROBIN COUVERTURE",
    "short": "Artisan Robin",
    "trades": "Charpentier, couvreur, zingueur",
    "manager": "Dusty Robin",
    "phone": "06 66 55 35 62",
    "phone_e164": "+33666553562",
    "whatsapp": "33666553562",
    # Ligne fixe affichée sur les camionnettes et les bâches de chantier
    "phone2": "09 82 27 89 92",
    "phone2_e164": "+33982278992",
    "email": "contact@artisanrobincouverture.fr",
    # Adresse administrative actuelle. À remplacer si l'entreprise a désormais une adresse à Thorigny-sur-Marne.
    "street": "22 avenue Augustin Pilardeau",
    "postcode": "77290",
    "city": "Mitry-Mory",
    "dept": "Seine-et-Marne",
    "lat": 48.9781,
    "lon": 2.6197,
    # Ville principale ciblée par le site
    "main_city": "Thorigny-sur-Marne",
    "main_cp": "77400",
    "google_rating": "4,9",
    "google_rating_num": 4.9,
    "google_count": 68,
    "years": "15",
    "jobs": "500",
    "twitter": "https://x.com/artisanrobincouverture",
}

# Points à confirmer avec le client : vides = non affichés.
A_CONFIRMER = {
    "siret": "829 474 568 00013",  # relevé sur la camionnette de l'entreprise : à vérifier sur annuaire-entreprises.data.gouv.fr
    "forme": "",
    "dirigeant": "Dusty Robin",
    "assureur": "",
    "mediateur": "",
    "rge": False,       # passer à True seulement si la qualification RGE est confirmée (annuaire France Rénov')
}

PRIX = json.load(open(os.path.join(HERE, "data", "prix.json"), encoding="utf-8"))
PRIX.pop("_note", None)

# Grille de la page Tarifs : (titre, [clés de prix.json])
TARIFS = [
    ("Couverture neuve et réfection", ["refection_tuiles_meca", "refection_tuiles_plates", "refection_ardoise", "couverture_zinc", "bac_acier"]),
    ("Réparation, fuite et urgence", ["remaniement", "reparation", "recherche_fuite", "bachage"]),
    ("Entretien de la toiture", ["demoussage", "demoussage_hydrofuge", "ramonage"]),
    ("Zinguerie et cheminée", ["gouttiere_zinc", "gouttiere_pvc", "descente_zinc", "faitage", "solin", "souche_cheminee"]),
    ("Isolation et combles", ["sarking", "isolation_rampants", "isolation_combles_perdus", "amenagement_combles"]),
    ("Charpente, fenêtres de toit, toit plat, bardage", ["traitement_charpente", "charpente_neuve", "velux_remplacement", "velux_creation", "etancheite_epdm", "etancheite_bitume", "bardage"]),
]

TARIF_SOURCES = [
    ("Prix d'une couverture de toit (Habitatpresto)", "https://www.habitatpresto.com/mag/toiture/couverture-de-toit"),
    ("Prix d'une toiture de 140 m² en 2026 (ABC Travaux)", "https://abctravaux.org/prix-toiture-140m2/"),
    ("Prix d'un remaniement de toiture en 2026 (ABC Travaux)", "https://abctravaux.org/prix-remaniement-toiture/"),
    ("Prix d'une gouttière en zinc (Travaux.com)", "https://www.travaux.com/couverture-toiture/jobs/pose-gouttieres"),
    ("Prix des gouttières et de la pose en 2026 (Prix-travaux-m2)", "https://www.prix-travaux-m2.com/prix-gouttieres.php"),
]

WORK_TYPES = [
    "Fuite / urgence",
    "Réparation de toiture",
    "Réfection complète",
    "Démoussage / nettoyage",
    "Gouttières / zinguerie",
    "Isolation de toiture",
    "Velux / fenêtre de toit",
    "Charpente",
    "Cheminée / faîtage",
    "Toit plat / étanchéité",
    "Ramonage",
    "Bardage",
    "Aménagement de combles",
    "Autre",
]

STEPS = [
    ("Vous appelez ou écrivez", "Au 06 66 55 35 62 ou par le formulaire. Une fuite ? Dites-le : on passe en priorité, 7 jours sur 7."),
    ("On monte voir le toit", "Visite gratuite : tuiles, faîtage, solins, gouttières, charpente vue des combles. Photos à l'appui, on vous montre ce qu'on a vu."),
    ("Devis sous 24 heures", "Chaque poste a sa ligne : échafaudage, dépose, fournitures, main-d'œuvre, évacuation. Pas de forfait opaque."),
    ("Le chantier, à la date dite", "Protection du jardin et des façades, toit bâché chaque soir si la couverture est ouverte, chantier rangé et nettoyé."),
    ("Réception et garantie", "On contrôle ensemble le travail fini. Facture détaillée, attestation de garantie décennale, conseils d'entretien."),
]

METIERS = [
    ("Couvreur", "Tuiles mécaniques et petites tuiles plates, ardoise, zinc, bac acier : pose neuve, réfection complète, remaniement, réparation de fuite, démoussage.", "/couverture/pose-toiture", ["tuiles", "chantier", "echafaudage"]),
    ("Charpentier", "Diagnostic de charpente, traitement des bois, remplacement de chevrons et de pannes, renfort avant une couverture plus lourde, création d'ouvertures.", "/couverture/charpente", ["charpente", "chantier"]),
    ("Zingueur", "Gouttières, descentes, chéneaux, noues, solins, abergements de cheminée et de fenêtres de toit, couvertures zinc à joint debout.", "/couverture/zinguerie-gouttieres", ["zinc", "gouttiere"]),
]

HOME_FAQ = [
    ("Intervenez-vous en urgence à Thorigny-sur-Marne ?",
     "Oui, 7 jours sur 7. Après une tempête ou une infiltration, on bâche le toit pour mettre la maison hors d'eau, puis on chiffre la réparation définitive. Appelez le 06 66 55 35 62."),
    ("Le devis est-il gratuit ?",
     "Oui. La visite et le devis sont gratuits et sans engagement. Vous recevez un devis détaillé, poste par poste, sous 24 heures après la visite."),
    ("Combien coûte une réfection de toiture ?",
     "En Île-de-France, comptez 130 à 180 €/m² en tuiles mécaniques, 180 à 250 €/m² en petites tuiles plates et 160 à 300 €/m² en ardoise, fourniture et pose. Le prix ferme est fixé après visite."),
    ("Faut-il une autorisation pour refaire sa toiture ?",
     "À l'identique, en général non. Si vous changez de matériau, de couleur ou créez une fenêtre de toit, il faut une déclaration préalable en mairie. Près d'un monument historique, l'architecte des Bâtiments de France donne son avis."),
    ("Vos travaux sont-ils garantis ?",
     "Oui. Les travaux de couverture et de charpente sont couverts par la garantie décennale. L'attestation d'assurance est jointe au devis."),
    ("Dans quelles communes intervenez-vous ?",
     "À Thorigny-sur-Marne et dans les communes autour : Lagny-sur-Marne, Pomponne, Dampmart, Saint-Thibault-des-Vignes, Montévrain, Chessy, Bussy-Saint-Georges, Torcy, Chelles, Vaires-sur-Marne, Claye-Souilly et une cinquantaine d'autres."),
]

# Texte de l'accueil sur Thorigny-sur-Marne (faits tirés de data/communes_notes_A.json, sources citées dans le fichier)
THORIGNY_HOME = [
    "Thorigny-sur-Marne s'étage sur un coteau exposé plein sud, sur la rive droite de la Marne, face à Lagny. Autour de l'église Saint-Martin, le centre garde ses maisons de bourg ; sur les pentes, longtemps plantées de vigne, les quartiers pavillonnaires des Cerisiers, des Épinettes, des Samoreaux ou des Hauts de Vallières mêlent des maisons de toutes les époques, couvertes pour la plupart de tuiles en terre cuite.",
    "Au nord, les rues qui bordent la forêt régionale des Vallières partagent le même souci : feuilles et mousses encombrent tuiles, chéneaux et gouttières. Un nettoyage à l'automne et un démoussage régulier y évitent la plupart des infiltrations.",
    "En bas de la ville, les terrains des bords de Marne relèvent du plan de prévention des risques d'inondation de la vallée de la Marne, et d'anciennes carrières souterraines de gypse et de calcaire font l'objet d'un plan de prévention des mouvements de terrain. Avant un chantier, on vérifie ce que ces plans et le PLU imposent à votre adresse.",
]

# Avis publiés sur l'ancien site (12 avis Google à 5 étoiles). Citations courtes, exactes.
TESTIMONIALS = [
    ("Jean-Pierre M.", "Claye-Souilly", "Urgence et bâchage", "novembre 2024", "Robin est intervenu en urgence après la tempête.", "Toit bâché le jour même, réparation définitive dans la semaine."),
    ("Sylvie D.", "Aulnay-sous-Bois", "Réfection de toiture", "octobre 2024", "Devis clair, prix honnête, travail soigné.", "Réfection complète d'une toiture en ardoise, finie dans les délais."),
    ("Marc et Isabelle T.", "Fontenay-sous-Bois", "Zinguerie et gouttières", "septembre 2024", "Excellent artisan pour la pose de nos gouttières", "Gouttières et zinguerie reprises : propre, ponctuel, attentif."),
    ("Patrick L.", "Mitry-Mory", "Isolation de toiture", "août 2024", "Travaux d'isolation par l'extérieur réalisés avec soin.", "Équipe à l'heure, maison protégée, chantier nettoyé."),
    ("Nathalie R.", "Tremblay-en-France", "Réparation de toiture", "juillet 2024", "Robin a diagnostiqué le problème en 10 minutes", "Fuite persistante réparée le lendemain, plus aucune infiltration depuis."),
    ("François et Marie B.", "Villeparisis", "Pose de Velux", "juin 2024", "Travail soigné, étanchéité parfaite, finitions propres.", "Deux fenêtres de toit posées, quelques tuiles abîmées remplacées au passage."),
    ("Christophe V.", "Créteil", "Démoussage et entretien", "mai 2024", "Résultat bluffant, la toiture est comme neuve.", "Démoussage complet et traitement hydrofuge."),
    ("Amandine K.", "Le Blanc-Mesnil", "Réfection de toiture", "avril 2024", "Devis détaillé, respect du budget, travaux terminés en 3 jours", "Réfection d'une toiture en tuiles dans le délai annoncé."),
    ("Bernard et Colette F.", "Claye-Souilly", "Charpente et couverture", "mars 2024", "Travail exemplaire, Robin nous a bien expliqué chaque étape.", "Charpente reprise en partie et couverture zinc posée."),
    ("Stéphanie M.", "Aulnay-sous-Bois", "Gouttières et zinguerie", "février 2024", "Excellent rapport qualité/prix.", "Toutes les gouttières remplacées en zinc prépatiné."),
    ("Thierry O.", "Mitry-Mory", "Urgence après tempête", "janvier 2024", "Robin a répondu immédiatement", "Appel un dimanche soir, bâche posée le lendemain matin."),
    ("Isabelle et Gérard N.", "Fontenay-sous-Bois", "Isolation et Velux", "décembre 2023", "Notre maison est beaucoup plus confortable depuis.", "Isolation des combles et fenêtre de toit posées en un seul chantier."),
]

# Profils par secteur : bâti, toitures courantes, travaux typiques, exemple de budget.
GROUP_PROFILES = {
    "Vallée de la Marne, de Thorigny à Esbly": {
        "short": "Bords de Marne et coteaux",
        "habitat": [
            "Les vieux bourgs des bords de Marne gardent des maisons de pierre enduite et de meulière couvertes de petites tuiles plates ou de tuiles mécaniques anciennes, souvent avec un faîtage scellé au mortier. Sur les coteaux, les pavillons des années 1950 à 1990 sont presque tous en tuiles mécaniques terre cuite.",
            "Entre la rivière et les coteaux boisés, le bâti mêle maisons de bourg, villas de villégiature du début du XXe siècle et pavillons plus récents. L'humidité de la vallée et l'ombre des arbres font pousser vite mousses et lichens sur les versants nord.",
        ],
        "roofs": ["Petites tuiles plates des maisons anciennes", "Tuiles mécaniques terre cuite des pavillons", "Ardoise sur les villas et maisons bourgeoises", "Zinguerie à reprendre sur les maisons de plus de 40 ans"],
        "works": ["demoussage-nettoyage-toiture", "reparation-entretien", "zinguerie-gouttieres", "faitage-refection-cheminee", "pose-toiture"],
        "example": (110, "refection_tuiles_meca", "un pavillon des années 1970 en tuiles mécaniques, couverture refaite à neuf"),
    },
    "Villages de la Gondoire et de la Brie": {
        "short": "Villages briards",
        "habitat": [
            "Autour des vallées de la Gondoire et du ru de la Brosse, les villages ont gardé leurs corps de ferme, leurs maisons rurales en moellons enduits et leurs toits pentus en petites tuiles plates briardes. Des lotissements récents, en tuiles mécaniques, les ont agrandis.",
            "Le bâti ancien est celui de la Brie : longères, granges, maisons de bourg aux toits très pentus en tuiles plates, avec des lucarnes et des souches de cheminée en brique. Les maisons construites depuis les années 1980 ont des couvertures plus simples en tuiles à emboîtement.",
        ],
        "roofs": ["Petites tuiles plates sur fortes pentes", "Granges et dépendances à reprendre", "Lucarnes et souches de cheminée en brique", "Tuiles mécaniques des lotissements récents"],
        "works": ["pose-toiture", "charpente", "faitage-refection-cheminee", "reparation-entretien", "velux-fenetres-toit"],
        "example": (130, "refection_tuiles_plates", "une maison de bourg en petites tuiles plates, couverture refaite à l'identique"),
    },
    "Marne-la-Vallée et Val d'Europe": {
        "short": "Ville nouvelle",
        "habitat": [
            "Les quartiers de la ville nouvelle ont été construits par vagues depuis les années 1970 : maisons de ville et pavillons en tuiles béton ou terre cuite, ensembles à toits-terrasses, puis ZAC récentes aux règles d'aspect précises. Autour subsistent les anciens villages, avec leurs maisons de bourg.",
            "On y trouve à quelques rues d'écart des couvertures très différentes : tuiles béton des années 1980 devenues poreuses, tuiles terre cuite des lotissements plus récents, toits plats et terrasses à étancher, bacs acier sur les extensions et les garages.",
        ],
        "roofs": ["Tuiles béton des années 1980 à rénover", "Toits-terrasses et étanchéité", "Velux et fenêtres de toit des maisons de ville", "Règles de lotissement sur les teintes"],
        "works": ["demoussage-nettoyage-toiture", "etancheite-toiture", "velux-fenetres-toit", "pose-toiture", "isolation-toiture"],
        "example": (95, "refection_tuiles_meca", "une maison de ville des années 1980 en tuiles béton, recouverte en tuiles terre cuite"),
    },
    "Chelles, Vaires et la Marne aval": {
        "short": "Pavillonnaire des bords de Marne",
        "habitat": [
            "Les grands quartiers pavillonnaires sont nés des lotissements de l'entre-deux-guerres et de l'après-guerre : maisons en meulière ou en brique, pavillons enduits, toits en tuiles mécaniques à deux ou quatre pans, souvent agrandis au fil des décennies.",
            "Beaucoup de maisons ont entre 60 et 100 ans : couvertures en tuiles mécaniques d'origine, faîtages scellés fissurés, zinguerie d'époque, souches de cheminée en brique. Ce sont les toits qui arrivent à l'âge de la réfection.",
        ],
        "roofs": ["Tuiles mécaniques d'origine des années 1920 à 1960", "Villas en meulière et toits à croupes", "Souches de cheminée en brique", "Extensions en toit plat ou bac acier"],
        "works": ["pose-toiture", "reparation-entretien", "faitage-refection-cheminee", "zinguerie-gouttieres", "isolation-toiture"],
        "example": (120, "refection_tuiles_meca", "un pavillon des années 1930 en tuiles mécaniques, couverture refaite et isolée"),
    },
    "Plaine de France : Claye, Villeparisis, Mitry": {
        "short": "Plaine de France",
        "habitat": [
            "Entre les vieux centres en pierre enduite et les zones d'activité, la plaine s'est couverte de lotissements des années 1960 à 2000, en tuiles mécaniques terre cuite ou béton. Le plateau est très exposé au vent d'ouest : rives, faîtages et tuiles de bord souffrent à chaque tempête.",
            "Le bâti mêle corps de ferme, maisons de bourg et pavillons de toutes les époques. Sur ce plateau ouvert, ce sont les toitures exposées au vent qui demandent le plus d'interventions : tuiles soulevées, rives décollées, faîtières déplacées.",
        ],
        "roofs": ["Tuiles mécaniques des lotissements", "Rives et faîtages exposés au vent", "Corps de ferme et dépendances", "Gouttières pendantes à remplacer"],
        "works": ["urgence-bachage", "reparation-entretien", "faitage-refection-cheminee", "zinguerie-gouttieres", "pose-toiture"],
        "example": (110, "refection_tuiles_meca", "un pavillon des années 1980 en tuiles mécaniques, couverture refaite"),
    },
}

# Anciennes communes du site non reprises dans la nouvelle zone : redirigées vers la page Zones.
OLD_ZONES = """mitry-mory meaux villevaude claye-souilly villeparisis lagny-sur-marne chelles torcy pontault-combault roissy-en-brie annet-sur-marne compans dammartin-en-goele noisiel vaujours coubron courtry aulnay-sous-bois sevran livry-gargan villepinte le-blanc-mesnil drancy bondy noisy-le-grand montreuil bobigny pantin rosny-sous-bois gagny le-raincy clichy-sous-bois montfermeil neuilly-sur-marne creteil vitry-sur-seine champigny-sur-marne maisons-alfort ivry-sur-seine villejuif vincennes alfortville fontenay-sous-bois nogent-sur-marne le-perreux-sur-marne sucy-en-brie gressy le-mesnil-amelot thieux villeneuve-sous-dammartin mauregard saint-mesmes messy nantouillet juilly longperrier othis saint-mard moussy-le-vieux montge-en-goele vinantes marchemoret rouvres le-bourget dugny saint-pathus le-plessis-belleville nanteuil-le-haudouin lagny-le-sec silly-le-long ver-sur-launette ermenonville senlis mortefontaine survilliers saint-witz vemars villeron louvres puiseux-en-france fontenay-en-parisis chennevieres-les-louvres epiais-les-louvres le-thillay goussainville roissy-en-france bonneuil-en-france gonesse arnouville villiers-le-bel sarcelles garges-les-gonesse fosses marly-la-ville belloy-en-france jagny-sous-bois luzarches seugy viarmes asnieres-sur-oise noisy-sur-oise lisle-adam beaumont-sur-oise persan bernes-sur-oise mours presles montsoult baillet-en-france domont ecouen montmagny deuil-la-barre enghien-les-bains soisy-sous-montmorency eaubonne ermont franconville cormeilles-en-parisis sannois argenteuil bezons colombes gennevilliers aubervilliers la-courneuve le-pin brou-sur-chantereine thorigny-sur-marne villiers-sur-marne saint-thibault-des-vignes le-plessis-trevise ozoir-la-ferriere moussy-le-neuf asnieres-sur-seine auvers-sur-oise avon bagnolet bailly-romainvilliers boissy-saint-leger brie-comte-robert brunoy carrieres-sous-poissy carrieres-sur-seine cesson champs-sur-marne chanteloup-en-brie charenton-le-pont charny chateau-landon chennevieres-sur-marne chessy choisy-le-roi collegien combs-la-ville conflans-sainte-honorine corbeil-essonnes coulommiers croissy-beaubourg croissy-sur-seine dammarie-les-lys dampmart emerainville epinay-sous-senart epinay-sur-seine esbly evry-courcouronnes ferrieres-en-brie fontainebleau fontenay-tresigny gretz-armainvilliers guermantes issy-les-moulineaux jossigny jouarre le-mee-sur-seine lesigny lieusaint limeil-brevannes lognes longjumeau maisons-laffitte marne-la-vallee melun moissy-cramayel montgeron montigny-le-bretonneux montry moret-loing-et-orvanne mormant nangis nanterre noissy-le-grand noisy-le-sec obsonville orly paris penchard pierrefitte-sur-seine poissy pomponne pontcarre provins puteaux rebais romainville rueil-malmaison saint-cloud saint-denis saint-germain-en-laye saint-germain-sur-morin saint-mande saint-maur-des-fosses saint-ouen saint-soupplets sainte-genevieve-des-bois sartrouville savigny-le-temple seine-port stains suresnes tournan-en-brie tremblay-en-france trilport vaires-sur-marne val-de-briey varennes-sur-seine varreddes vaux-le-penil veneux-les-sablons versailles villenoy""".split()

# Redirections fixes (ancienne adresse -> nouvelle)
REDIRECTS = [
    ("/couverture/demoussage-nettoyage", "/couverture/demoussage-nettoyage-toiture"),
    ("/zone", "/zones"),
    ("/zone/couvreur-marne-la-vallee", "/zone/couvreur-torcy"),
    ("/zone/couvreur-noissy-le-grand", "/zone/couvreur-noisy-le-grand"),
    ("/devis", "/contact"),
    ("/plan-du-site", "/zones"),
    ("/index.html", "/"),
]
