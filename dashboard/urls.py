from django.urls import path
from .views import accueil, detail_indicateur, graphique_api

app_name = "dashboard"

urlpatterns = [
    path("", accueil, name="accueil"),
    path("indicateurs/<slug:code>/", detail_indicateur, name="detail_indicateur"),
    path("api/graphiques/<slug:code>/", graphique_api, name="graphique_api"),
]