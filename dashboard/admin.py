from django.contrib import admin
from django.contrib import messages
from django.contrib.auth.models import Group
from django.contrib.admin.sites import NotRegistered
from django.core.paginator import Paginator
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import path
from django.utils import timezone

from unfold.admin import ModelAdmin, TabularInline

from .models import (
    Thematique,
    Graphique,
    SerieGraphique,
    Observation,
    TYPES_SERIE_UNIQUE,
)
from .services.export_template_xlsx import build_thematique_update_template
from .services.import_xlsx import importer_xlsx


# Retirer "Groupes" de l'admin
try:
    admin.site.unregister(Group)
except NotRegistered:
    pass


# Personnalisation de l'admin
admin.site.site_header = "Interstats - Administration"
admin.site.site_title = "SSMSI Admin"
admin.site.index_title = "Pilotage des thematiques, graphiques et donnees"


# =========================================================
# INLINES
# =========================================================

class SerieGraphiqueInline(TabularInline):
    model = SerieGraphique
    extra = 1
    fields = [
        "code",
        "libelle",
        "couleur",
        "ordre",
        "visible",
    ]
    ordering = ["ordre", "id"]

    def get_max_num(self, request, obj=None, **kwargs):
        if obj and obj.type_graphique in TYPES_SERIE_UNIQUE:
            return 1
        return None  # illimité

    def get_extra(self, request, obj=None, **kwargs):
        if obj and obj.type_graphique in TYPES_SERIE_UNIQUE:
            return 0 if obj.series.exists() else 1
        return 1


class ObservationInline(admin.TabularInline):
    model = Observation
    extra = 0
    fields = [
        "serie",
        "code_x",
        "libelle_x",
        "ordre_x",
        "valeur",
        "valeur_formatee",
    ]
    ordering = ["ordre_x", "id"]
    show_change_link = True


# =========================================================
# ADMIN : THEMATIQUE
# =========================================================

@admin.register(Thematique)
class ThematiqueAdmin(ModelAdmin):
    list_display = ["titre", "code", "date_mise_a_jour", "ordre", "actif"]
    list_editable = ["ordre", "actif"]
    search_fields = ["titre", "code", "sous_titre", "chapeau"]
    ordering = ["ordre", "titre"]
    list_per_page = 30
    save_on_top = True
    actions = ["exporter_template_mise_a_jour"]

    @admin.action(description="Exporter un template XLSX de mise a jour")
    def exporter_template_mise_a_jour(self, request, queryset):
        if queryset.count() != 1:
            self.message_user(
                request,
                "Selectionnez exactement une thematique pour exporter son template.",
                level=messages.WARNING,
            )
            return None

        thematique = queryset.first()
        workbook = build_thematique_update_template(thematique)

        filename = f"template_mise_a_jour_{thematique.code}_{timezone.now().strftime('%Y%m%d')}.xlsx"
        response = HttpResponse(
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        response["Content-Disposition"] = f'attachment; filename="{filename}"'
        workbook.save(response)
        return response


# =========================================================
# ADMIN : GRAPHIQUE
# =========================================================

@admin.register(Graphique)
class GraphiqueAdmin(ModelAdmin):
    list_display = [
        "titre",
        "code",
        "thematique",
        "type_graphique",
        "ordre",
        "actif",
    ]
    list_filter = [
        "type_graphique",
        "actif",
    ]
    list_editable = ["ordre", "actif"]
    search_fields = [
        "titre",
        "code",
        "sous_titre",
        "source",
        "champ",
        "note",
        "thematique__titre",
    ]
    ordering = ["thematique__ordre", "thematique__titre", "ordre", "titre"]
    list_per_page = 30
    save_on_top = True
    empty_value_display = "-"

    # Champs modifiables via l'admin (éditoriaux uniquement)
    fieldsets = [
        ("Structure (cle technique)", {
            "fields": [
                "thematique",
                "code",
                "type_graphique",
                "ordre",
                "actif",
            ],
            "description": "Ces champs structurent le graphique. Modifier la structure via import xlsx.",
        }),
        ("Editorial", {
            "fields": [
                "titre",
                "sous_titre",
                "texte_valeur_cle",
                "source",
                "champ",
                "note",
                "legende_visible",
            ]
        }),
        ("Axes", {
            "fields": [
                "titre_axe_x",
                "titre_axe_y",
            ]
        }),
    ]

    # Structure des données : visible mais non modifiable via l'admin
    # → pour changer le type ou la structure, passer par le fichier xlsx
    readonly_fields = [
        "code",
    ]

    inlines = [SerieGraphiqueInline]

    class Media:
        js = ("js/admin_graphique.js",)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "thematique":
            kwargs["queryset"] = Thematique.objects.order_by("ordre", "titre")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


# =========================================================
# VUE STATISTIQUES ADMIN
# =========================================================

def admin_statistiques(request):
    if not request.user.is_staff:
        from django.contrib.auth.views import redirect_to_login
        return redirect_to_login(request.get_full_path())

    nb_thematiques = Thematique.objects.count()
    nb_thematiques_actives = Thematique.objects.filter(actif=True).count()
    nb_graphiques = Graphique.objects.count()
    nb_graphiques_actifs = Graphique.objects.filter(actif=True).count()
    nb_series = SerieGraphique.objects.count()
    nb_observations = Observation.objects.count()

    # --- Filtres graphiques ---
    f_g_thematique = request.GET.get("g_thematique", "")
    f_g_recherche = request.GET.get("g_recherche", "").strip()

    liste_graphiques = (
        Graphique.objects
        .select_related("thematique")
        .order_by("thematique__ordre", "thematique__titre", "ordre", "titre")
    )
    if f_g_thematique:
        liste_graphiques = liste_graphiques.filter(thematique__code=f_g_thematique)
    if f_g_recherche:
        liste_graphiques = liste_graphiques.filter(titre__icontains=f_g_recherche)

    paginator_g = Paginator(liste_graphiques, 25)
    page_g = paginator_g.get_page(request.GET.get("page_g", 1))

    # --- Filtres observations ---
    f_o_thematique = request.GET.get("o_thematique", "")
    f_o_graphique = request.GET.get("o_graphique", "")
    f_o_serie = request.GET.get("o_serie", "").strip()
    f_o_recherche = request.GET.get("o_recherche", "").strip()

    liste_observations = (
        Observation.objects
        .select_related("graphique", "graphique__thematique", "serie")
        .order_by(
            "graphique__thematique__ordre",
            "graphique__thematique__titre",
            "graphique__ordre",
            "graphique__titre",
            "ordre_x",
        )
    )
    if f_o_thematique:
        liste_observations = liste_observations.filter(graphique__thematique__code=f_o_thematique)
    if f_o_graphique:
        liste_observations = liste_observations.filter(graphique__code=f_o_graphique)
    if f_o_serie:
        liste_observations = liste_observations.filter(serie__libelle__icontains=f_o_serie)
    if f_o_recherche:
        liste_observations = liste_observations.filter(
            libelle_x__icontains=f_o_recherche
        ) | liste_observations.filter(
            code_x__icontains=f_o_recherche
        )

    paginator_o = Paginator(liste_observations, 50)
    page_o = paginator_o.get_page(request.GET.get("page_o", 1))

    thematiques_liste = Thematique.objects.order_by("ordre", "titre")
    graphiques_liste = Graphique.objects.select_related("thematique").order_by("thematique__ordre", "ordre", "titre")

    context = {
        **admin.site.each_context(request),
        "title": "Tableau de bord — Statistiques",
        "nb_thematiques": nb_thematiques,
        "nb_thematiques_actives": nb_thematiques_actives,
        "nb_graphiques": nb_graphiques,
        "nb_graphiques_actifs": nb_graphiques_actifs,
        "nb_series": nb_series,
        "nb_observations": nb_observations,
        # graphiques
        "page_g": page_g,
        "paginator_g": paginator_g,
        "f_g_thematique": f_g_thematique,
        "f_g_recherche": f_g_recherche,
        # observations
        "page_o": page_o,
        "paginator_o": paginator_o,
        "f_o_thematique": f_o_thematique,
        "f_o_graphique": f_o_graphique,
        "f_o_serie": f_o_serie,
        "f_o_recherche": f_o_recherche,
        # listes pour les selects
        "thematiques_liste": thematiques_liste,
        "graphiques_liste": graphiques_liste,
    }

    return render(request, "admin/statistiques.html", context)


# =========================================================
# VUE IMPORT XLSX ADMIN
# =========================================================

def admin_import_xlsx(request):
    if not request.user.is_staff:
        from django.contrib.auth.views import redirect_to_login
        return redirect_to_login(request.get_full_path())

    rapport = None
    fichier_nom = None

    if request.method == "POST":
        fichier = request.FILES.get("fichier")
        if not fichier:
            messages.error(request, "Aucun fichier sélectionné.")
        else:
            rapport = importer_xlsx(fichier)
            fichier_nom = fichier.name

    context = {
        **admin.site.each_context(request),
        "title": "Import de données (.xlsx)",
        "rapport": rapport,
        "fichier_nom": fichier_nom,
    }

    return render(request, "admin/import_xlsx.html", context)

