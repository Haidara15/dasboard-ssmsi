from dashboard.models import (
    Thematique,
    Graphique,
    SerieGraphique,
    Observation,
)


def run():
    print("=== Seed Graphiques avancés ===")

    thematique, _ = Thematique.objects.get_or_create(
        code="graphiques-avances",
        defaults={
            "titre": "Galerie de graphiques avancés",
            "sous_titre": "Page de validation technique du moteur graphique",
            "chapeau": (
                "Cette thématique regroupe plusieurs cas graphiques de démonstration "
                "afin de tester le moteur de rendu."
            ),
            "texte_methodologique": (
                "Les données sont fictives et servent uniquement à valider la structure "
                "et les comportements de rendu."
            ),
            "texte_source": "Source fictive — Données de démonstration",
            "ordre": 99,
            "actif": True,
        }
    )

    # =========================================================
    # 3. GRAPHIQUE 1 — LIGNES MULTIPLES
    # =========================================================

    g1, _ = Graphique.objects.get_or_create(
        code="ga-lignes-multiples",
        defaults={
            "thematique": thematique,
            "titre": "Évolution comparée de plusieurs populations",
            "sous_titre": "Lignes multiples",
            "type_graphique": "ligne",
            "titre_axe_x": "Année",
            "titre_axe_y": "Nombre",
            "source": "Source fictive",
            "champ": "France entière",
            "note": "Test lignes multiples",
            "legende_visible": True,
            "ordre": 1,
            "actif": True,
        }
    )

    s1_1, _ = SerieGraphique.objects.get_or_create(
        graphique=g1,
        code="infractions",
        defaults={"libelle": "Infractions", "ordre": 1, "visible": True}
    )
    s1_2, _ = SerieGraphique.objects.get_or_create(
        graphique=g1,
        code="victimes",
        defaults={"libelle": "Victimes", "ordre": 2, "visible": True}
    )
    s1_3, _ = SerieGraphique.objects.get_or_create(
        graphique=g1,
        code="mis_en_cause",
        defaults={"libelle": "Mis en cause", "ordre": 3, "visible": True}
    )

    annees = ["2019", "2020", "2021", "2022", "2023"]
    infractions = [52000, 54800, 56100, 58900, 60200]
    victimes = [31200, 32850, 34120, 35840, 37210]
    mis_en_cause = [11800, 12100, 12450, 12980, 13320]

    for i, annee in enumerate(annees, start=1):
        Observation.objects.get_or_create(
            graphique=g1,
            serie=s1_1,
            code_x=annee,
            defaults={"libelle_x": annee, "ordre_x": int(annee), "valeur": infractions[i-1]}
        )
        Observation.objects.get_or_create(
            graphique=g1,
            serie=s1_2,
            code_x=annee,
            defaults={"libelle_x": annee, "ordre_x": int(annee), "valeur": victimes[i-1]}
        )
        Observation.objects.get_or_create(
            graphique=g1,
            serie=s1_3,
            code_x=annee,
            defaults={"libelle_x": annee, "ordre_x": int(annee), "valeur": mis_en_cause[i-1]}
        )

    # =========================================================
    # 4. GRAPHIQUE 2 — AIRE
    # =========================================================

    g2, _ = Graphique.objects.get_or_create(
        code="ga-aire",
        defaults={
            "thematique": thematique,
            "titre": "Évolution des victimes (aire)",
            "sous_titre": "Test graphique aire",
            "type_graphique": "aire",
            "titre_axe_x": "Année",
            "titre_axe_y": "Nombre de victimes",
            "source": "Source fictive",
            "champ": "France entière",
            "note": "Test aire",
            "legende_visible": True,
            "ordre": 2,
            "actif": True,
        }
    )

    s2_1, _ = SerieGraphique.objects.get_or_create(
        graphique=g2,
        code="victimes_aire",
        defaults={"libelle": "Victimes", "ordre": 1, "visible": True}
    )

    valeurs_aire = [28000, 30100, 32900, 35000, 37200]

    for i, annee in enumerate(annees, start=1):
        Observation.objects.get_or_create(
            graphique=g2,
            serie=s2_1,
            code_x=annee,
            defaults={"libelle_x": annee, "ordre_x": int(annee), "valeur": valeurs_aire[i-1]}
        )

    # =========================================================
    # 5. GRAPHIQUE 3 — COLONNES MULTIPLES NON EMPILÉES
    # =========================================================

    g3, _ = Graphique.objects.get_or_create(
        code="ga-colonnes-multiples",
        defaults={
            "thematique": thematique,
            "titre": "Victimes par âge et sexe",
            "sous_titre": "Colonnes multiples non empilées",
            "type_graphique": "colonnes",
            "titre_axe_x": "Classe d'âge",
            "titre_axe_y": "Nombre",
            "source": "Source fictive",
            "champ": "France entière",
            "note": "Test colonnes multiples",
            "legende_visible": True,
            "ordre": 3,
            "actif": True,
        }
    )

    s3_1, _ = SerieGraphique.objects.get_or_create(
        graphique=g3,
        code="femmes",
        defaults={"libelle": "Femmes", "ordre": 1, "visible": True}
    )
    s3_2, _ = SerieGraphique.objects.get_or_create(
        graphique=g3,
        code="hommes",
        defaults={"libelle": "Hommes", "ordre": 2, "visible": True}
    )

    classes_age = ["0-9", "10-17", "18-29", "30-44", "45-59", "60+"]
    femmes = [3200, 7800, 10900, 6200, 2400, 500]
    hommes = [1000, 2000, 1500, 1000, 500, 210]

    for i, age in enumerate(classes_age, start=1):
        Observation.objects.get_or_create(
            graphique=g3,
            serie=s3_1,
            code_x=age,
            defaults={"libelle_x": age, "ordre_x": i, "valeur": femmes[i-1]}
        )
        Observation.objects.get_or_create(
            graphique=g3,
            serie=s3_2,
            code_x=age,
            defaults={"libelle_x": age, "ordre_x": i, "valeur": hommes[i-1]}
        )

    # =========================================================
    # 6. GRAPHIQUE 4 — BARRES EMPILÉES
    # =========================================================

    g4, _ = Graphique.objects.get_or_create(
        code="ga-barres-empilees",
        defaults={
            "thematique": thematique,
            "titre": "Infractions par type d'espace et sexe",
            "sous_titre": "Barres horizontales empilées",
            "type_graphique": "barres_empilees",
            "titre_axe_x": "Nombre",
            "titre_axe_y": "Type d'espace",
            "source": "Source fictive",
            "champ": "France entière",
            "note": "Test barres empilées",
            "legende_visible": True,
            "ordre": 4,
            "actif": True,
        }
    )

    s4_1, _ = SerieGraphique.objects.get_or_create(
        graphique=g4,
        code="urbain",
        defaults={"libelle": "Femmes", "ordre": 1, "visible": True}
    )
    s4_2, _ = SerieGraphique.objects.get_or_create(
        graphique=g4,
        code="rural",
        defaults={"libelle": "Hommes", "ordre": 2, "visible": True}
    )

    espaces = ["Centre-ville", "Banlieue", "Périurbain", "Rural"]
    femmes_espace = [15200, 9800, 6100, 2900]
    hommes_espace = [4300, 3700, 2100, 1200]

    for i, espace in enumerate(espaces, start=1):
        Observation.objects.get_or_create(
            graphique=g4,
            serie=s4_1,
            code_x=espace,
            defaults={"libelle_x": espace, "ordre_x": i, "valeur": femmes_espace[i-1]}
        )
        Observation.objects.get_or_create(
            graphique=g4,
            serie=s4_2,
            code_x=espace,
            defaults={"libelle_x": espace, "ordre_x": i, "valeur": hommes_espace[i-1]}
        )

    # =========================================================
    # 7. GRAPHIQUE 5 — MIXTE COLONNES + LIGNE
    # =========================================================

    g5, _ = Graphique.objects.get_or_create(
        code="ga-mixte",
        defaults={
            "thematique": thematique,
            "titre": "Infractions et évolution annuelle",
            "sous_titre": "Colonnes + ligne avec double axe",
            "type_graphique": "colonnes",
            "titre_axe_x": "Année",
            "titre_axe_y": "Nombre d'infractions",
            "source": "Source fictive",
            "champ": "France entière",
            "note": "Test mixte",
            "legende_visible": True,
            "ordre": 5,
            "actif": True,
        }
    )

    s5_1, _ = SerieGraphique.objects.get_or_create(
        graphique=g5,
        code="nombre",
        defaults={"libelle": "Nombre", "ordre": 1, "visible": True}
    )
    s5_2, _ = SerieGraphique.objects.get_or_create(
        graphique=g5,
        code="evolution",
        defaults={"libelle": "Évolution (%)", "ordre": 2, "visible": True}
    )

    nb = [52000, 54800, 56100, 58900, 60200]
    evo = [0, 5.4, 2.4, 5.0, 2.2]

    for i, annee in enumerate(annees, start=1):
        Observation.objects.get_or_create(
            graphique=g5,
            serie=s5_1,
            code_x=annee,
            defaults={"libelle_x": annee, "ordre_x": int(annee), "valeur": nb[i-1]}
        )
        Observation.objects.get_or_create(
            graphique=g5,
            serie=s5_2,
            code_x=annee,
            defaults={"libelle_x": annee, "ordre_x": int(annee), "valeur": evo[i-1]}
        )

    print("✔ Seed graphiques avancés terminé.")