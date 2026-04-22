from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.functions import Lower
from django.utils.text import slugify


def _build_unique_slug(model_class, base_slug, instance_pk=None):
    slug = base_slug or "item"
    candidate = slug
    index = 2

    queryset = model_class.objects.all()
    if instance_pk:
        queryset = queryset.exclude(pk=instance_pk)

    while queryset.filter(code=candidate).exists():
        candidate = f"{slug}-{index}"
        index += 1

    return candidate


# =========================================================
# 1. THÉMATIQUE = PAGE
# =========================================================

class Thematique(models.Model):

    code = models.SlugField(unique=True, blank=True)
    titre = models.CharField(max_length=255)
    sous_titre = models.CharField(max_length=255, blank=True)

    chapeau = models.TextField(blank=True)
    texte_methodologique = models.TextField(blank=True)
    texte_source = models.TextField(blank=True)

    date_mise_a_jour = models.DateField(null=True, blank=True)

    ordre = models.PositiveIntegerField(default=0)
    actif = models.BooleanField(default=True)

    class Meta:
        ordering = ["ordre", "titre"]
        constraints = [
            models.UniqueConstraint(
                Lower("titre"),
                name="dashboard_thematique_titre_ci_unique",
            ),
        ]

    def clean(self):
        super().clean()

        titre = (self.titre or "").strip()
        if not titre:
            return

        queryset = Thematique.objects.exclude(pk=self.pk).filter(titre__iexact=titre)
        if queryset.exists():
            raise ValidationError({
                "titre": "Une thematique avec ce titre existe deja.",
            })

    def save(self, *args, **kwargs):
        if not self.code:
            base_slug = slugify(self.titre) or "thematique"
            self.code = _build_unique_slug(Thematique, base_slug, instance_pk=self.pk)

        if self.ordre == 0:
            max_ordre = Thematique.objects.exclude(pk=self.pk).aggregate(
                models.Max("ordre")
            )["ordre__max"]
            self.ordre = (max_ordre or 0) + 1

        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.titre


# =========================================================
# 2. GRAPHIQUES
# =========================================================

class Graphique(models.Model):

    TYPE_GRAPHIQUE_CHOICES = [
        ("ligne", "Ligne"),
        ("barres", "Barres"),
        ("colonnes", "Colonnes"),
        ("barres_empilees", "Barres empilées"),
        ("colonnes_empilees", "Colonnes empilées"),
        ("aire", "Aire"),
        ("camembert", "Camembert"),
        ("anneau", "Anneau"),
        ("valeur_cle", "Valeur clé"),
    ]

    thematique = models.ForeignKey(
        Thematique,
        on_delete=models.CASCADE,
        related_name="graphiques"
    )

    code = models.SlugField(unique=True, blank=True)

    titre = models.CharField(max_length=255)
    sous_titre = models.CharField(max_length=255, blank=True)

    type_graphique = models.CharField(
        max_length=50,
        choices=TYPE_GRAPHIQUE_CHOICES
    )

    titre_axe_x = models.CharField(max_length=255, blank=True)
    titre_axe_y = models.CharField(max_length=255, blank=True)

    # Valeur clé
    icone = models.FileField(
        upload_to="graphiques_icones/",
        null=True,
        blank=True
    )
    texte_valeur_cle = models.TextField(blank=True)

    source = models.CharField(max_length=255, blank=True)
    champ = models.TextField(blank=True)
    note = models.TextField(blank=True)
    legende_visible = models.BooleanField(default=True)

    ordre = models.PositiveIntegerField(default=0)
    actif = models.BooleanField(default=True)

    class Meta:
        ordering = ["ordre", "id"]

    def save(self, *args, **kwargs):
        if not self.code:
            base_slug = slugify(f"{self.thematique.code}-{self.titre}") or "graphique"
            self.code = _build_unique_slug(Graphique, base_slug, instance_pk=self.pk)

        if self.ordre == 0:
            max_ordre = Graphique.objects.exclude(pk=self.pk).filter(
                thematique=self.thematique
            ).aggregate(
                models.Max("ordre")
            )["ordre__max"]
            self.ordre = (max_ordre or 0) + 1

        super().save(*args, **kwargs)

    def __str__(self):
        return self.titre


TYPES_SERIE_UNIQUE = {"camembert", "anneau", "valeur_cle"}


class SerieGraphique(models.Model):
    graphique = models.ForeignKey(
        Graphique,
        on_delete=models.CASCADE,
        related_name="series"
    )

    code = models.SlugField(blank=True)
    libelle = models.CharField(max_length=255)

    couleur = models.CharField(max_length=20, blank=True)

    ordre = models.PositiveIntegerField(default=0)
    visible = models.BooleanField(default=True)

    class Meta:
        unique_together = ("graphique", "code")
        ordering = ["ordre", "id"]

    def clean(self):
        super().clean()
        if self.graphique_id and self.graphique.type_graphique in TYPES_SERIE_UNIQUE:
            existe_deja = (
                SerieGraphique.objects
                .filter(graphique=self.graphique)
                .exclude(pk=self.pk)
                .exists()
            )
            if existe_deja:
                raise ValidationError(
                    f"Un graphique de type « {self.graphique.get_type_graphique_display()} »"
                    " n'accepte qu'une seule série."
                )

    def save(self, *args, **kwargs):
        if not self.code:
            base_slug = slugify(self.libelle) or "serie"
            code = base_slug
            index = 2

            queryset = SerieGraphique.objects.exclude(pk=self.pk).filter(graphique=self.graphique)
            while queryset.filter(code=code).exists():
                code = f"{base_slug}-{index}"
                index += 1

            self.code = code

        super().save(*args, **kwargs)

        if self.ordre == 0:
            max_ordre = SerieGraphique.objects.exclude(pk=self.pk).filter(
                graphique=self.graphique
            ).aggregate(
                models.Max("ordre")
            )["ordre__max"]
            self.ordre = (max_ordre or 0) + 1

        super().save(*args, **kwargs)

    def __str__(self):
        return self.libelle


# =========================================================
# 4. OBSERVATIONS = DONNÉES
# =========================================================

class Observation(models.Model):
    graphique = models.ForeignKey(
        Graphique,
        on_delete=models.CASCADE,
        related_name="observations"
    )

    serie = models.ForeignKey(
        SerieGraphique,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="observations"
    )

    code_x = models.CharField(max_length=100)
    libelle_x = models.CharField(max_length=255)
    ordre_x = models.PositiveIntegerField(null=True, blank=True)

    valeur = models.FloatField(null=True, blank=True)
    valeur_formatee = models.CharField(max_length=255, blank=True)

    infobulle = models.TextField(blank=True)
    metadonnees = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ["ordre_x", "id"]

    def save(self, *args, **kwargs):
        if self.ordre_x is None:
            dernier = Observation.objects.filter(
                graphique=self.graphique
            ).aggregate(
                models.Max("ordre_x")
            )["ordre_x__max"]

            self.ordre_x = (dernier or 0) + 1

        if not self.libelle_x:
            self.libelle_x = self.code_x

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.libelle_x} - {self.valeur}"



