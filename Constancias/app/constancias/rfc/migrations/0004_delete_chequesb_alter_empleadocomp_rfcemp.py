# Generated by Django 5.1.3 on 2024-11-15 05:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rfc', '0003_empleadocomp'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ChequesB',
        ),
        migrations.AlterField(
            model_name='empleadocomp',
            name='rfcemp',
            field=models.CharField(max_length=13),
        ),
    ]
