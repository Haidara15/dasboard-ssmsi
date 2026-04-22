from dashboard.models import (
    Thematique,
    Graphique,
    SerieGraphique,
    Observation,
)


def run():
    print("=== Seed Violences sexuelles ===")

    thematique, _ = Thematique.objects.get_or_create(
        code="violences-sexuelles",
        defaults={
            "titre": "Violences sexuelles enregistrées",
            "sous_titre": "Analyse de démonstration",
            "chapeau": (
                "Cette thématique présente plusieurs indicateurs fictifs relatifs aux violences "
                "sexuelles enregistrées, afin de tester l’architecture de rendu des graphiques."
            ),
            "texte_methodologique": (
                "Les données présentées ici sont purement fictives et utilisées uniquement "
                "pour des tests techniques."
            ),
            "texte_source": "Source fictive — SSMSI (jeu de démonstration)",
            "ordre": 2,
            "actif": True,
        }
    )

    # =========================================================
    # 3. GRAPHIQUE 1 — ÉVOLUTION (LIGNE)
    # =========================================================

    graphique1, _ = Graphique.objects.get_or_create(
        code="vs-evolution",
        defaults={
            "thematique": thematique,
            "titre": "Évolution des violences sexuelles",
            "sous_titre": "Série annuelle fictive",
            "type_graphique": "ligne",
            "titre_axe_x": "Année",
            "titre_axe_y": "Nombre de victimes",
            "source": "Source fictive — SSMSI",
            "champ": "France entière",
            "note": "Données de démonstration.",
            "legende_visible": True,
            "ordre": 1,
            "actif": True,
        }
    )

    serie1, _ = SerieGraphique.objects.get_or_create(
        graphique=graphique1,
        code="victimes_total",
        defaults={
            "libelle": "Victimes",
            "ordre": 1,
            "visible": True,
        }
    )

    observations_g1 = [
        ("2019", "2019", 2019, 31200),
        ("2020", "2020", 2020, 32850),
        ("2021", "2021", 2021, 34120),
        ("2022", "2022", 2022, 35840),
        ("2023", "2023", 2023, 37210),
    ]

    for i, (code_x, libelle_x, ordre_x, valeur) in enumerate(observations_g1, start=1):
        Observation.objects.get_or_create(
            graphique=graphique1,
            serie=serie1,
            code_x=code_x,
            defaults={
                "libelle_x": libelle_x,
                "ordre_x": ordre_x,
                "valeur": valeur,
                "valeur_formatee": f"{valeur:,}".replace(",", " "),
            }
        )

    # =========================================================
    # 4. GRAPHIQUE 2 — RÉPARTITION PAR ÂGE (BARRES)
    # =========================================================

    graphique2, _ = Graphique.objects.get_or_create(
        code="vs-age",
        defaults={
            "thematique": thematique,
            "titre": "Répartition des victimes par âge",
            "sous_titre": "Distribution fictive par classe d'âge",
            "type_graphique": "barres",
            "titre_axe_x": "Nombre de victimes",
            "titre_axe_y": "Classe d'âge",
            "source": "Source fictive — SSMSI",
            "champ": "France entière",
            "note": "Données de démonstration.",
            "legende_visible": True,
            "ordre": 2,
            "actif": True,
        }
    )

    serie2, _ = SerieGraphique.objects.get_or_create(
        graphique=graphique2,
        code="victimes_age",
        defaults={
            "libelle": "Victimes",
            "ordre": 1,
            "visible": True,
        }
    )

    observations_g2 = [
        ("0-9", "0-9 ans", 1, 4200),
        ("10-17", "10-17 ans", 2, 9800),
        ("18-29", "18-29 ans", 3, 12400),
        ("30-44", "30-44 ans", 4, 7200),
        ("45-59", "45-59 ans", 5, 2900),
        ("60+", "60 ans ou plus", 6, 710),
    ]

    for i, (code_x, libelle_x, ordre_x, valeur) in enumerate(observations_g2, start=1):
        Observation.objects.get_or_create(
            graphique=graphique2,
            serie=serie2,
            code_x=code_x,
            defaults={
                "libelle_x": libelle_x,
                "ordre_x": ordre_x,
                "valeur": valeur,
                "valeur_formatee": f"{valeur:,}".replace(",", " "),
            }
        )

    # =========================================================
    # 5. GRAPHIQUE 3 — SEXE DES VICTIMES (CAMEMBERT)
    # =========================================================

    graphique3, _ = Graphique.objects.get_or_create(
        code="vs-sexe",
        defaults={
            "thematique": thematique,
            "titre": "Répartition des victimes par sexe",
            "sous_titre": "Structure fictive",
            "type_graphique": "camembert",
            "titre_axe_x": "",
            "titre_axe_y": "",
            "source": "Source fictive — SSMSI",
            "champ": "France entière",
            "note": "Données de démonstration.",
            "legende_visible": True,
            "ordre": 3,
            "actif": True,
        }
    )

    serie3, _ = SerieGraphique.objects.get_or_create(
        graphique=graphique3,
        code="victimes_sexe",
        defaults={
            "libelle": "Victimes",
            "ordre": 1,
            "visible": True,
        }
    )

    observations_g3 = [
        ("femmes", "Femmes", 1, 88.0),
        ("hommes", "Hommes", 2, 11.0),
        ("autres", "Autres / non renseigné", 3, 1.0),
    ]

    for i, (code_x, libelle_x, ordre_x, valeur) in enumerate(observations_g3, start=1):
        Observation.objects.get_or_create(
            graphique=graphique3,
            serie=serie3,
            code_x=code_x,
            defaults={
                "libelle_x": libelle_x,
                "ordre_x": ordre_x,
                "valeur": valeur,
                "valeur_formatee": str(valeur).replace(".", ",") + " %",
            }
        )

    # =========================================================
    # 6. GRAPHIQUE 4 — ÂGE x SEXE (COLONNES EMPILÉES)
    # =========================================================

    graphique4, _ = Graphique.objects.get_or_create(
        code="vs-age-sexe",
        defaults={
            "thematique": thematique,
            "titre": "Victimes par âge et sexe",
            "sous_titre": "Répartition fictive croisée",
            "type_graphique": "colonnes_empilees",
            "titre_axe_x": "Classe d'âge",
            "titre_axe_y": "Nombre de victimes",
            "source": "Source fictive — SSMSI",
            "champ": "France entière",
            "note": "Données de démonstration.",
            "legende_visible": True,
            "ordre": 4,
            "actif": True,
        }
    )

    serie4_femmes, _ = SerieGraphique.objects.get_or_create(
        graphique=graphique4,
        code="femmes",
        defaults={
            "libelle": "Femmes",
            "ordre": 1,
            "visible": True,
        }
    )

    serie4_hommes, _ = SerieGraphique.objects.get_or_create(
        graphique=graphique4,
        code="hommes",
        defaults={
            "libelle": "Hommes",
            "ordre": 2,
            "visible": True,
        }
    )

    observations_g4_femmes = [
        ("0-9", "0-9 ans", 1, 3200),
        ("10-17", "10-17 ans", 2, 7800),
        ("18-29", "18-29 ans", 3, 10900),
        ("30-44", "30-44 ans", 4, 6200),
        ("45-59", "45-59 ans", 5, 2400),
        ("60+", "60 ans ou plus", 6, 500),
    ]

    observations_g4_hommes = [
        ("0-9", "0-9 ans", 1, 1000),
        ("10-17", "10-17 ans", 2, 2000),
        ("18-29", "18-29 ans", 3, 1500),
        ("30-44", "30-44 ans", 4, 1000),
        ("45-59", "45-59 ans", 5, 500),
        ("60+", "60 ans ou plus", 6, 210),
    ]

    ordre_global = 1

    for code_x, libelle_x, ordre_x, valeur in observations_g4_femmes:
        Observation.objects.get_or_create(
            graphique=graphique4,
            serie=serie4_femmes,
            code_x=code_x,
            defaults={
                "libelle_x": libelle_x,
                "ordre_x": ordre_x,
                "valeur": valeur,
                "valeur_formatee": f"{valeur:,}".replace(",", " "),
            }
        )
        ordre_global += 1

    for code_x, libelle_x, ordre_x, valeur in observations_g4_hommes:
        Observation.objects.get_or_create(
            graphique=graphique4,
            serie=serie4_hommes,
            code_x=code_x,
            defaults={
                "libelle_x": libelle_x,
                "ordre_x": ordre_x,
                "valeur": valeur,
                "valeur_formatee": f"{valeur:,}".replace(",", " "),
            }
        )
        ordre_global += 1

    print("✔ Seed violences sexuelles terminé.")