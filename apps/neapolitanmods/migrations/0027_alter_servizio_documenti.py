# Generated by Django 4.2.4 on 2023-10-11 08:53

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("neapolitanmods", "0026_alter_servizio_tipologia"),
    ]

    operations = [
        migrations.AlterField(
            model_name="servizio",
            name="documenti",
            field=models.FileField(max_length=255, null=True, upload_to=""),
        ),
    ]
