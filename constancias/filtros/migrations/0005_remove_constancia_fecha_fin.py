# Generated by Django 5.1 on 2024-11-07 17:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('filtros', '0004_alter_constancia_rfc'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='constancia',
            name='fecha_fin',
        ),
    ]
