from dashboard.models import (
    Thematique,
    Graphique,
    SerieGraphique,
    Observation,
)


def executer():
    print("=== Création du cas HOMICIDES ===")

    # =====================================================
    # 1. THEMATIQUE
    # =====================================================
    thematique, _ = Thematique.objects.get_or_create(
        code="homicides",
        defaults={
            "titre": "Homicides",
            "sous_titre": "Évolution et structure des homicides enregistrés",
            "chapeau": "Présentation des homicides enregistrés en France.",
            "texte_methodologique": "Les données peuvent faire l’objet de révisions.",
            "texte_source": "Source : SSMSI",
            "ordre": 1,
            "actif": True,
        }
    )

    print(f"Thematique : {thematique}")


    # =====================================================
    # 2. GRAPHIQUE
    # =====================================================
    graphique, _ = Graphique.objects.get_or_create(
        code="homicides-evolution",
        defaults={
            "thematique": thematique,
            "titre": "Évolution des homicides enregistrés",
            "type_graphique": "colonnes",
            "titre_axe_x": "Année",
            "titre_axe_y": "Nombre",
            "source": "SSMSI",
            "champ": "France entière",
            "note": "Données provisoires",
            "ordre": 1,
            "actif": True,
        }
    )

    print(f"Graphique : {graphique}")


    # =====================================================
    # 3. SERIES
    # =====================================================
    serie_nombre, _ = SerieGraphique.objects.get_or_create(
        graphique=graphique,
        code="nombre",
        defaults={
            "libelle": "Nombre",
            "ordre": 1,
            "visible": True,
        }
    )

    serie_evolution, _ = SerieGraphique.objects.get_or_create(
        graphique=graphique,
        code="evolution",
        defaults={
            "libelle": "Évolution (%)",
            "ordre": 2,
            "visible": True,
        }
    )

    print("Séries créées")


    # =====================================================
    # 6. DONNEES
    # =====================================================
    data_nombre = [
        ("2019", 809),
        ("2020", 863),
        ("2021", 887),
        ("2022", 910),
        ("2023", 884),
    ]

    data_evolution = [
        ("2019", 0),
        ("2020", 6.7),
        ("2021", 2.8),
        ("2022", 2.6),
        ("2023", -2.9),
    ]

    print("Création des observations...")

    ordre = 1

    for annee, valeur in data_nombre:
        Observation.objects.update_or_create(
            graphique=graphique,
            serie=serie_nombre,
            code_x=annee,
            defaults={
                "libelle_x": annee,
                "ordre_x": int(annee),
                "valeur": valeur,
                "valeur_formatee": str(valeur),
            }
        )
        ordre += 1

    for annee, valeur in data_evolution:
        Observation.objects.update_or_create(
            graphique=graphique,
            serie=serie_evolution,
            code_x=annee,
            defaults={
                "libelle_x": annee,
                "ordre_x": int(annee),
                "valeur": valeur,
                "valeur_formatee": f"{valeur} %",
            }
        )
        ordre += 1

    print("Observations créées")

    print("\n=== FIN ===")