# Generated by Django 5.0.2 on 2024-02-19 23:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0004_rename_key_apikeys_api_key_remove_apikeys_space_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="data",
            name="_model",
            field=models.JSONField(default=dict),
        ),
    ]
