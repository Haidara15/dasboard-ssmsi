from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render

from .models import Thematique, Graphique
from .services.import_xlsx import importer_xlsx


# =========================================================
# API GRAPHIQUE
# =========================================================

def graphique_api(request, code):
    graphique = get_object_or_404(Graphique, code=code, actif=True)

    observations = graphique.observations.all().order_by("ordre_x")

    labels_codes = []
    labels = []
    deja = set()

    for obs in observations:
        if obs.code_x not in deja:
            labels_codes.append(obs.code_x)
            labels.append(obs.libelle_x)
            deja.add(obs.code_x)

    series_data = []

    for serie in graphique.series.all().order_by("ordre"):
        obs_serie = {
            obs.code_x: obs.valeur
            for obs in observations.filter(serie=serie)
        }

        data = [obs_serie.get(code_x, None) for code_x in labels_codes]

        series_data.append({
            "code": serie.code,
            "libelle": serie.libelle,
            "data": data,
        })


    data = {
        "code": graphique.code,
        "titre": graphique.titre,
        "type_graphique": graphique.type_graphique,
        "legende_visible": graphique.legende_visible,

        "axe_x": graphique.titre_axe_x,
        "axe_y": graphique.titre_axe_y,

        "labels": labels,
        "series": series_data,
    }

    return JsonResponse(data)



# =========================================================
# PAGE D'ACCUEIL
# =========================================================

def accueil(request):
    thematiques = Thematique.objects.filter(actif=True).order_by("ordre", "titre")

    contexte = {
        "thematiques": thematiques,
    }
    return render(request, "dashboard/accueil.html", contexte)


# =========================================================
# PAGE DETAIL INDICATEUR
# =========================================================

def detail_indicateur(request, code):
    thematique = get_object_or_404(
        Thematique.objects,
        code=code,
        actif=True
    )

    graphiques = thematique.graphiques.filter(actif=True).order_by("ordre", "id")

    contexte = {
        "thematique": thematique,
        "graphiques": graphiques,
    }
    return render(request, "dashboard/detail_indicateur.html", contexte)


# =========================================================
# IMPORT XLSX
# =========================================================

