# Generated by Django 4.2.4 on 2023-10-10 07:15

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("neapolitanmods", "0015_alter_commessa_priorità"),
    ]

    operations = [
        migrations.AlterField(
            model_name="contatti",
            name="id_monday",
            field=models.BigIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name="contratti",
            name="id_monday",
            field=models.BigIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name="fatture",
            name="id_monday",
            field=models.BigIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name="servizio",
            name="id_monday",
            field=models.BigIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name="task",
            name="id_monday",
            field=models.BigIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name="utente",
            name="id_monday",
            field=models.BigIntegerField(null=True),
        ),
    ]
