# Generated by Django 5.1.4 on 2024-12-16 23:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('indiceCoincidencia', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='historialic',
            old_name='fecha_creacion',
            new_name='fecha',
        ),
    ]