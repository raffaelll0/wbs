# Generated by Django 4.2.4 on 2023-10-05 14:10

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("neapolitanmods", "0005_alter_commessa_priorità"),
    ]

    operations = [
        migrations.AlterField(
            model_name="commessa",
            name="tipologia",
            field=models.CharField(max_length=200, null=True),
        ),
    ]
