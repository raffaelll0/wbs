# Generated by Django 4.2.4 on 2023-10-10 09:38

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("neapolitanmods", "0017_aziende_id_commessa"),
    ]

    operations = [
        migrations.AddField(
            model_name="commessa",
            name="id_azienda",
            field=models.BigIntegerField(null=True),
        ),
    ]
