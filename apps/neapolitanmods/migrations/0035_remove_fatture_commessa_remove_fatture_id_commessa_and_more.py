# Generated by Django 4.2.4 on 2023-10-11 13:55

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("neapolitanmods", "0034_remove_fatture_commessa_fatture_commessa"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="fatture",
            name="commessa",
        ),
        migrations.RemoveField(
            model_name="fatture",
            name="id_commessa",
        ),
        migrations.RemoveField(
            model_name="fatture",
            name="parte_passiva",
        ),
    ]
