# Generated by Django 5.1 on 2024-11-07 00:05

import filtros.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('filtros', '0003_alter_constancia_fecha_fin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='constancia',
            name='rfc',
            field=models.CharField(max_length=13, validators=[
                                   filtros.models.validar_rfc]),
        ),
    ]
