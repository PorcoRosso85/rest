# Generated by Django 5.0.2 on 2024-02-19 23:23

import app.models
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0004_rename_key_apikeys_api_key_remove_apikeys_space_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="FieldModel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("model", models.JSONField(default=dict)),
                (
                    "data",
                    models.ForeignKey(
                        default=app.models.get_default_data,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="model",
                        to="app.data",
                    ),
                ),
            ],
        ),
    ]
