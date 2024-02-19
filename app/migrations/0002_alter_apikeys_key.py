# Generated by Django 5.0.2 on 2024-02-16 08:43

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="apikeys",
            name="key",
            field=models.CharField(default=uuid.uuid4, max_length=100, unique=True),
        ),
    ]