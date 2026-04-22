from django.db import migrations, models
from django.db.models.functions import Lower


def deduplicate_thematique_titles(apps, schema_editor):
    Thematique = apps.get_model("dashboard", "Thematique")

    seen = {}
    for thematique in Thematique.objects.order_by("id"):
        key = (thematique.titre or "").strip().lower()
        if not key:
            continue

        count = seen.get(key, 0) + 1
        seen[key] = count

        if count == 1:
            continue

        thematique.titre = f"{thematique.titre} ({count})"
        thematique.save(update_fields=["titre"])


class Migration(migrations.Migration):

    dependencies = [
        ("dashboard", "0005_remove_graphique_axe_y_secondaire_actif_and_more"),
    ]

    operations = [
        migrations.RunPython(deduplicate_thematique_titles, migrations.RunPython.noop),
        migrations.AddConstraint(
            model_name="thematique",
            constraint=models.UniqueConstraint(
                Lower("titre"),
                name="dashboard_thematique_titre_ci_unique",
            ),
        ),
    ]
