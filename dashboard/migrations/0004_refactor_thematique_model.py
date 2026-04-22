from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("dashboard", "0003_remove_seriegraphique_dimension_and_more"),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[
                migrations.RemoveField(
                    model_name="pageindicateur",
                    name="thematique",
                ),
                migrations.RenameField(
                    model_name="graphique",
                    old_name="page",
                    new_name="thematique",
                ),
                migrations.DeleteModel(
                    name="Thematique",
                ),
            ],
            state_operations=[
                migrations.RemoveField(
                    model_name="pageindicateur",
                    name="thematique",
                ),
                migrations.DeleteModel(
                    name="Thematique",
                ),
                migrations.RenameModel(
                    old_name="PageIndicateur",
                    new_name="Thematique",
                ),
                migrations.AlterModelTable(
                    name="thematique",
                    table="dashboard_pageindicateur",
                ),
                migrations.RenameField(
                    model_name="graphique",
                    old_name="page",
                    new_name="thematique",
                ),
            ],
        ),
    ]
